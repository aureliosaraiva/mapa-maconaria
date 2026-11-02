# Taxonomia e vocabulários controlados

> Usados nos campos `ritos`, `potencias`, `paises`, `periodos`, `temas` das fontes (`schemas/fonte.schema.json`) e no front matter dos verbetes. Código = slug minúsculo sem acento. Novos códigos: a sessão propõe no relatório; a orquestradora incorpora aqui e no esquema. Até lá, use o mais próximo e anote em `observacoes`.

## Temas (`temas`)
| Código | Escopo |
|---|---|
| `origens` | Pedreiros operativos, guildas, Old Charges, Escócia (Schaw), teorias de origem (templária, rosacruz, comacina etc.) |
| `documentos_fundadores` | Old Charges, Constituições de Anderson, Ahiman Rezon, landmarks, Basic Principles, Ramsay |
| `ritual` | Textos de ritual, exposições, monitores, catecismos, cerimônias |
| `ritos` | Sistemas de graus e sua história |
| `graus` | Graus específicos (simbólicos e altos graus) |
| `simbolismo` | Símbolos, alegorias, lendas (Hiram, Templo de Salomão, colunas, esquadro e compasso...) |
| `principios` | Dogmas/princípios: GADU, VLS, landmarks, tolerância, segredo, filantropia, laicidade |
| `regularidade` | Regularidade, reconhecimento, liberal × tradicional, amity, cisões |
| `potencias` | Obediências, Grandes Lojas/Orientes, Supremos Conselhos, organizações internacionais |
| `mulheres` | Maçonaria feminina e mista, adoção, debates |
| `religiao` | Relação com Igreja Católica, protestantismo, islã, judaísmo, espiritismo; documentos eclesiásticos |
| `politica` | Revoluções, independências, república, liberalismo, perseguições |
| `antimaconaria` | Antimaçonaria, conspiracionismo, exposições hostis, perseguição |
| `sociabilidade` | Lojas como sociabilidade, filantropia, beneficência, clubes, sociologia |
| `ordens_anexas` | Arco Real, Marca, Críptica, Templários, Shriners, Estrela do Oriente, DeMolay, Arco-Íris etc. |
| `esoterismo` | Rosacrucianismo, hermetismo, ocultismo maçônico, ritos egípcios, Martinismo |
| `arte_cultura` | Música (Mozart), literatura, arquitetura, iconografia, cinema |
| `personalidades` | Biografias de maçons e de antimaçons |
| `historiografia` | Método, debates acadêmicos, centros de pesquisa, periódicos |

## Ritos (`ritos`)
`emulacao` (Emulation/Inglês) · `york` (Americano/York Rite e Webb) · `reaa` (Escocês Antigo e Aceito) · `frances_moderno` (Francês/Moderno, Groussier, Rito Francês Filosófico) · `rer` (Escocês Retificado) · `schroder` · `sueco` · `zinnendorf` · `brasileiro` · `adonhiramita` · `memphis_misraim` (e Memphis, Misraïm em separado quando preciso) · `escoces_filosofico` · `perfeicao` (Rito de Perfeição/Heredom) · `primitivo` · `irlandes` · `escoces_craft` (ritual das lojas escocesas) · `canadense` · `noachita` · `outros_ritos`.

## Potências e organizações (`potencias`) — semente, ampliar
- **Brasil:** `gob` (Grande Oriente do Brasil), `cmsb` (Confederação da Maçonaria Simbólica do Brasil — Grandes Lojas estaduais), `comab` (Confederação Maçônica do Brasil — Grandes Orientes estaduais independentes), `glomaron`/outras regionais (usar `gl_<uf>` / `go_<uf>`, ex. `gl_sp`, `go_sp`), `sc_reaa_br` (Supremo Conselho do Brasil, 1832), `mista_br`, `feminina_br`.
- **Reino Unido/Irlanda:** `ugle`, `gl_escocia`, `gl_irlanda`, `antients`, `moderns` (históricas, até 1813).
- **França:** `godf`, `glnf`, `gldf`, `glff`, `droit_humain`, `glmf`.
- **EUA/Canadá:** `gl_estaduais_eua`, `prince_hall`, `sc_sj` (Supremo Conselho Jurisdição Sul), `sc_njn` (Norte).
- **Ibérica/Latina:** `gol` (Grande Oriente Lusitano), `glrp` (GL Legal de Portugal/GLRP), `gle` (Gran Logia de España), `goe` (Gran Oriente Español, hist.), `goi` (Grande Oriente d'Italia), `gl_argentina`, `gl_chile`, `gl_mexico`/`gl_york_mexico`, `gl_cuba`, demais `gl_<pais>`.
- **Internacionais:** `clipsas`, `cmi` (Conferência Mundial de Grandes Lojas), `cimal` (Confederação Interamericana), `sc_mundo` (Supremos Conselhos — conferências).
- **Paramaçônicas/anexas:** `arco_real`, `marca`, `cryptic`, `templarios_maconicos`, `shriners`, `estrela_oriente`, `demolay`, `arco_iris`, `filhas_jo`, `amaranth`.

## Países (`paises`)
ISO 3166-1 alfa-2 minúsculo (`br`, `pt`, `gb`, `fr`, `us`, `es`, `it`, `de`, `ar`...); `mundo` para geral; `al` (América Latina) para panoramas.

## Períodos (`periodos`)
`medieval` (<1600) · `p1600_1716` · `p1717_1750` · `p1751_1813` · `p1814_1870` · `p1871_1918` · `p1919_1945` · `p1946_1989` · `p1990_hoje`.

## Tipos (`tipo`) e categorias (`categoria`) de fonte
- `tipo`: `livro`, `capitulo`, `artigo`, `tese`, `dissertacao`, `documento` (constituição, ata, bula, regulamento), `ritual`, `exposicao` (exposé), `periodico` (número/coleção), `site`, `pagina`, `verbete` (enciclopédia), `audiovisual`, `acervo`, `dataset`.
- `categoria`: `primaria_historica` (documento de época), `ritual_publicado`, `oficial_potencia` (publicação institucional), `academica`, `tese`, `historiografia_maconica` (AQC, Pietre-Stones, autores maçons pesquisadores), `enciclopedia`, `divulgacao`, `eclesiastica`, `antimaconica` (fonte hostil, usada como documento), `acervo_museu`, `imprensa`, `audiovisual`.

## Idiomas
ISO 639-1: `pt`, `en`, `fr`, `es`, `it`, `de`, `nl`, `sv`, `la` (latim), `ru`, `pl`... Buscar sempre em pt, en, fr, es, it, de, no mínimo.

## Sementes de verbetes (lista não exaustiva, para cobertura)
- **Documentos:** Manuscrito Regius (~1390), Cooke (~1450), Old Charges (família), Estatutos Schaw (1598/99), Edinburgh Register House MS (1696), Constituições de Anderson (1723/1738), Prichard *Masonry Dissected* (1730), Discurso de Ramsay (1737), *In eminenti* (1738), *Providas* (1751), *Ahiman Rezon* (1756), *Three Distinct Knocks* (1760), *Jachin and Boaz* (1762), Constituições de 1786 (REAA, atribuídas), Preston *Illustrations* (1772), Webb *Monitor* (1797), Morgan *Illustrations* (1826), landmarks de Mackey (1858), *Morals and Dogma* (1871), *Humanum genus* (1884), Convento de Lausanne (1875), *Basic Principles* UGLE (1929), Código de Direito Canônico 1917 c.2335 e 1983, Declaração da CDF (1983), constituições do GOB/CMSB.
- **Eventos (mundo):** fundação da Grande Loja de Londres (1717), Grande Loja da Irlanda (c.1725), Escócia (1736), Antients (1751), GOdF (1773), Convento de Wilhelmsbad (1782), Iluminados da Baviera (1776–85), Revolução Francesa e Barruel, independência dos EUA, União de 1813 (UGLE), caso Morgan e Partido Antimaçônico (1826–38), Supremo Conselho de Charleston (1801), independências latino-americanas e Loja Lautaro, Risorgimento, GOdF suprime a obrigação do GADU (1877) e ruptura com UGLE, fraude de Léo Taxil (1885–97), Prince Hall (1775/1784/1791), *Protocolos* (1903), perseguição nazista/fascista/franquista/soviética, Vichy, caso P2 (1981), Le Droit Humain (1893), femininas.
- **Brasil:** Areópago de Itambé (1796), Conjuração Baiana (1798), Revolução Pernambucana (1817), Loja Comércio e Artes (1815/1821), fundação do GOB (17/6/1822), D. Pedro I grão-mestre e fechamento (1822), José Bonifácio × Gonçalves Ledo, Supremo Conselho (1832), Questão Religiosa (1872–75: D. Vital, D. Macedo Costa, Rio Branco), Abolição e maçonaria, Proclamação da República, cisão de 1927 e criação das Grandes Lojas (Mário Behring), cisão de 1973 e COMAB, Estado Novo e maçonaria, ditadura militar, Palácio do Lavradio, maçonaria feminina/mista no Brasil.
- **Portugal e mundo lusófono:** Grande Oriente Lusitano (1802), Intendência e perseguição, Revolução de 1820, República de 1910, Salazar e a lei de 1935, Angola/Moçambique.
- **Ritos e graus:** um verbete por rito (lista acima) + verbetes dos graus simbólicos + graus de cada rito (ex.: 33 graus do REAA, graus capitulares/crípticos/cavalaria do York, 7 graus do Rito Moderno, 6 classes do RER, 90/99 de Memphis-Misraïm).
- **Símbolos/conceitos:** GADU, VLS, esquadro e compasso, letra G, avental, luvas, colunas J e B, pavimento mosaico, Templo de Salomão, Hiram Abiff, acácia, delta/olho, pedra bruta/pedra polida, régua de 24 polegadas, maço e cinzel, câmara de reflexão, VITRIOL, loja/oficina/oriente, tronco de beneficência, ágape, tolerância, regularidade, iniciação, juramento, sigilo.
