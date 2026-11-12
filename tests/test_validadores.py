"""Testes dos validadores com dados sintéticos (tests/fixtures/). Rodar:
    python3 -m unittest discover -s tests -v
Cada teste copia as fixtures para uma pasta temporária, estraga algo e confere o resultado."""
import contextlib
import io
import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))
import anticopia  # noqa: E402
import validar_linha_do_tempo  # noqa: E402
import validar_verbetes  # noqa: E402

FIX = RAIZ / "tests" / "fixtures"


def rodar(mod, *args):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        rc = mod.main(list(args))
    return rc, out.getvalue()


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        shutil.copytree(FIX / "data", self.tmp / "data")
        shutil.copytree(FIX / "acervo", self.tmp / "acervo")
        os.environ["ANTICOPIA_REFS"] = str(self.tmp / "acervo" / "txt")

    def tearDown(self):
        shutil.rmtree(self.tmp)
        os.environ.pop("ANTICOPIA_REFS", None)

    def verbete(self, rel):
        return self.tmp / "data" / "verbetes" / rel

    def editar(self, rel, velho, novo):
        p = self.verbete(rel)
        t = p.read_text(encoding="utf-8")
        self.assertIn(velho, t)
        p.write_text(t.replace(velho, novo), encoding="utf-8")


class TestVerbetes(Base):
    def test_fixtures_passam(self):
        rc, out = rodar(validar_verbetes, "--raiz", str(self.tmp))
        self.assertEqual(rc, 0, out)
        self.assertIn("sensivel: true", out)

    def test_estrito_acusa_link_inexistente(self):
        rc, out = rodar(validar_verbetes, "--raiz", str(self.tmp), "--estrito")
        self.assertEqual(rc, 1)
        self.assertIn("verbete-inexistente", out)

    def test_fonte_fora_do_catalogo(self):
        self.editar("potencias/potencia-exemplo.md", "fontes: [exemplo-2001-alfa]", "fontes: [exemplo-2001-alfa, nao-existe-2000-x]")
        rc, out = rodar(validar_verbetes, "--raiz", str(self.tmp))
        self.assertEqual(rc, 1)
        self.assertIn("nao-existe-2000-x", out)

    def test_nota_nao_definida_e_sem_fonte(self):
        self.editar("potencias/potencia-exemplo.md", "obediência fictícia[^a]", "obediência fictícia[^a][^b]")
        self.editar("potencias/potencia-exemplo.md", "[^a]: exemplo-2001-alfa, p. 40–41.", "[^a]: ver o livro, p. 40.")
        rc, out = rodar(validar_verbetes, "--raiz", str(self.tmp))
        self.assertEqual(rc, 1)
        self.assertIn("[^b] chamada no texto mas não definida", out)
        self.assertIn("não cita nenhum source_id", out)

    def test_id_e_categoria_coerentes(self):
        self.editar("ritos/rito-exemplo.md", "categoria: ritos", "categoria: graus")
        rc, out = rodar(validar_verbetes, "--raiz", str(self.tmp))
        self.assertEqual(rc, 1)
        self.assertIn("diferente da pasta", out)

    def test_conteudo_ritual_reservado(self):
        self.editar("eventos/evento-exemplo.md", "que este verbete não reproduz", "e a palavra de passe é \"XYZ\"")
        rc, out = rodar(validar_verbetes, "--raiz", str(self.tmp))
        self.assertEqual(rc, 1)
        self.assertIn("regra 5", out)

    def test_termo_da_lista_privada(self):
        lista = self.tmp / "lista.txt"
        lista.write_text("Rito Exemplo\n", encoding="utf-8")
        os.environ["ALERTA_RITUAL_EXTRA"] = str(lista)
        try:
            rc, out = rodar(validar_verbetes, "--raiz", str(self.tmp))
        finally:
            os.environ.pop("ALERTA_RITUAL_EXTRA")
        self.assertEqual(rc, 1)
        self.assertIn("lista privada", out)
        self.assertNotIn("Rito Exemplo”", out)  # o termo não é ecoado

    def test_citacao_longa(self):
        self.editar("potencias/potencia-exemplo.md", "Pratica o", "\"um dois três quatro cinco seis sete oito nove dez onze doze treze catorze quinze\" Pratica o")
        rc, out = rodar(validar_verbetes, "--raiz", str(self.tmp))
        self.assertEqual(rc, 1)
        self.assertIn("citação entre aspas", out)

    def test_sem_verbetes_passa(self):
        shutil.rmtree(self.tmp / "data" / "verbetes")
        (self.tmp / "data" / "conexoes.json").unlink()
        rc, out = rodar(validar_verbetes, "--raiz", str(self.tmp))
        self.assertEqual(rc, 0, out)

    def test_conexao_com_fonte_inexistente(self):
        p = self.tmp / "data" / "conexoes.json"
        d = json.loads(p.read_text())
        d["conexoes"][0]["fontes"] = ["fantasma-1900-x"]
        p.write_text(json.dumps(d))
        rc, out = rodar(validar_verbetes, "--raiz", str(self.tmp))
        self.assertEqual(rc, 1)
        self.assertIn("fantasma-1900-x", out)


class TestLinhaDoTempo(Base):
    def test_fixtures_passam(self):
        rc, out = rodar(validar_linha_do_tempo, "--raiz", str(self.tmp))
        self.assertEqual(rc, 0, out)
        self.assertIn('"fragmentos": 2', out)

    def test_erros(self):
        p = self.tmp / "data" / "linha_do_tempo" / "T02.json"
        d = json.loads(p.read_text())
        d["eventos"].append({"data": "1800-13", "titulo": "x", "fontes": ["nada-1-x"]})
        d["eventos"].append({"id": "ev-gama", "data": 1900, "data_fim": 1800, "titulo": "y", "fontes": ["exemplo-1723-gama"]})
        p.write_text(json.dumps(d))
        rc, out = rodar(validar_linha_do_tempo, "--raiz", str(self.tmp))
        self.assertEqual(rc, 1)
        self.assertIn("nada-1-x", out)
        self.assertIn("duplicado", out)
        self.assertIn("data_fim anterior", out)

    def test_json_invalido(self):
        (self.tmp / "data" / "linha_do_tempo" / "T03.json").write_text("{eventos: ")
        rc, out = rodar(validar_linha_do_tempo, "--raiz", str(self.tmp))
        self.assertEqual(rc, 1)
        self.assertIn("JSON inválido", out)

    def test_sem_fragmentos_passa(self):
        shutil.rmtree(self.tmp / "data" / "linha_do_tempo")
        rc, _ = rodar(validar_linha_do_tempo, "--raiz", str(self.tmp))
        self.assertEqual(rc, 0)


class TestAnticopia(Base):
    def test_fixtures_passam(self):
        rc, out = rodar(anticopia, "--raiz", str(self.tmp))
        self.assertEqual(rc, 0, out)

    def test_copia_do_acervo_e_erro(self):
        self.editar("potencias/potencia-exemplo.md", "Pratica o", "Esta frase longa existe apenas para que o detector anti-cópia encontre. Pratica o")
        rc, out = rodar(anticopia, "--raiz", str(self.tmp))
        self.assertEqual(rc, 1)
        self.assertIn("exemplo-2001-alfa", out)

    def test_redacao_proxima_e_aviso(self):
        self.editar("potencias/potencia-exemplo.md", "Pratica o", "O texto integral fictício do livro Alfa foi lido. Pratica o")
        rc, out = rodar(anticopia, "--raiz", str(self.tmp))
        self.assertEqual(rc, 0, out)
        self.assertIn("redação próxima", out)


if __name__ == "__main__":
    unittest.main()
