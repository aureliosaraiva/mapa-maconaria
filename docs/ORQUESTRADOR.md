# Roteiro do ciclo de orquestração

> Executado por uma **sessão nova a cada ciclo** (tarefa agendada recorrente) e também pela sessão orquestradora original. Cada ciclo é **curto e sem estado**: tudo o que precisa saber está em `docs/ORQUESTRACAO.md`. Responder e registrar em português do Brasil. Não criar PR; commit/push direto na `main`.

## 0. Preparar
1. `add_repo(owner="aureliosaraiva", repo="mapa-maconaria", access="push")` e clonar (siga a resposta do add_repo); `cd` no clone, `git checkout main && git pull --rebase origin main`.
2. Ler `docs/ORQUESTRACAO.md` (quadro de ondas e tabela **Sessões ativas**) e `docs/ESTADO.md`.

## 1. Conferir as sessões em andamento
Para cada linha da tabela **Sessões ativas** com status `em andamento`:
- Se o `git log` da `main` tem `[orq:<ID> concluída]` → marcar `concluída` no quadro e na tabela.
- Senão, `get_session(<session_id>)`:
  - `status_bucket` WORKING → nada a fazer.
  - FAILED/IDLE sem conclusão → `list_events(session_id, kinds=["result"], limit=100)` e ver o último `result`:
    - `usage_limit_reached` / "hit your … limit · resets HH:MM" → se o horário já passou, retomar com `send_message` ("limite renovado — retome a <ID>: `git pull --rebase origin main`, empurre o que estiver pronto, siga até o fechamento"); senão, deixar para o próximo ciclo.
    - outro erro → retomar uma vez com `send_message`; se já houve 2 retomadas sem progresso (sem commit `[<ID>]` novo), arquivar e recriar com o mesmo escopo (nova linha na tabela).
- Se o limite de uso **desta** sessão de ciclo for atingido, simplesmente pare: o próximo ciclo continua.

## 2. Preencher vagas
**Máximo de 3 sessões trabalhadoras `em andamento` ao mesmo tempo.** Se houver vaga, pegar a próxima ID `pendente` na **ordem de disparo** do quadro e:
1. `create_session(source_url="https://github.com/aureliosaraiva/mapa-maconaria", source_revision="main", outcome_branch="main", title="Maçonaria <ID> — <escopo curto>", tags=["mapa-maconaria","onda-<n>"], prompt=<modelo abaixo>)`.
2. **Imediatamente** registrar na tabela **Sessões ativas** (`<ID> | <session_id> | em andamento | <data>`) e mudar o status no quadro para `em andamento`; commit `[orq] dispara <ID>` e push (com rebase). Isso evita que outro ciclo dispare a mesma ID.

### Modelo de prompt
```
Você é a sessão trabalhadora **<ID>** do projeto Enciclopédia da Maçonaria. Trabalhe de forma totalmente autônoma (ninguém responde perguntas; decida com bom senso e registre decisões no relatório). Português do Brasil.
1. No repositório mapa-maconaria (já clonado): `git fetch origin main && git checkout main && git pull --rebase origin main`. Todo commit e push vai direto na `main` (decisão do autor), com `git pull --rebase origin main` antes de cada push. Leia CLAUDE.md, docs/ESTADO.md, docs/taxonomia.md, docs/verbetes-guia.md e, em docs/ORQUESTRACAO.md, as instruções comuns da sua onda e a linha **<ID>** (escopo e arquivos que só você edita).
2. Anexe o acervo privado: `add_repo` owner aureliosaraiva, repo fontes-maconaria, access push; depois `scripts/acervo_sync.sh pull`. Leia os textos em ../fontes-maconaria/txt/<source_id>.txt antes de afirmar.
3. Execute o escopo com profundidade. Commits + push frequentes (a cada 3–5 verbetes ou ~15 fontes): o limite de uso pode cortar a sessão a qualquer momento e o que não foi empurrado se perde. Mensagens `[<ID>] ...`.
4. Feche conforme o CLAUDE.md: validadores com 0 erros; relatório docs/sessoes/<ID>.md; sua linha no docs/ORQUESTRACAO.md como `concluída` com link; bloqueios no PENDENCIAS (## <ID>); `scripts/acervo_sync.sh push`; push final com mensagem `[orq:<ID> concluída] <resumo>`.
Não crie pull request. Não edite arquivos de outras sessões.
```

## 3. Consolidar (quando uma onda inteira concluir)
- Atualizar `docs/ESTADO.md`: números (`python3 scripts/validar_fontes.py --json`, contagem de verbetes e de textos no acervo), sessões concluídas, próximos passos.
- Incorporar à `docs/taxonomia.md` os códigos propostos nos relatórios (seção "proposta para a taxonomia").
- Quando todas as IDs do quadro estiverem `concluída`: definir a próxima onda no quadro (seguindo `docs/PLANO.md`: onda 4 = integração, QA, i18n) ou, se o plano estiver cumprido, desativar a tarefa agendada (`update_trigger enabled=false`, id em `docs/ESTADO.md`) e registrar no ESTADO.

## 4. Fechar o ciclo
Commit/push das mudanças do quadro (`[orq] ciclo <data hora>: <resumo>`). Não deixar nada sem push. Fim.
