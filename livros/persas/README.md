# Persas: projeto editorial e prova integral

ConTeXt, A4 (210 × 297 mm), páginas espelhadas, notas na margem externa.

## Grid atual (prova de 14/36 pt)

Horizontal: margem interna de 17 mm + texto de 118 mm + intervalo de 4 mm
+ notas de 62 mm + margem externa de 9 mm = 210 mm.

Vertical: 18 mm até o cabeçalho; cabeçalho de 8 mm; intervalo de 6 mm;
texto de 231 mm; intervalo de 8 mm; rodapé de 6 mm; margem inferior de 20 mm.
O corpo do texto começa a 32 mm do topo. O filete ocupa o meio do intervalo.

Gentium Plus 14 pt / entrelinha uniforme de 36 pt no grego; 9 pt / 12 pt nas notas.
A família inclui negrito e itálico para os estilos das entradas.
Os números dos versos aparecem no primeiro verso e a cada cinco versos,
em uma faixa de 6 mm dentro do bloco de 118 mm. O grego dispõe dos 112 mm
restantes. Há 2 mm entre o número e o início do verso; o número fica do lado
do texto, separado do filete, inclusive nas páginas pares.

O PDF inicial do grid tem duas páginas: uma com guias e outra limpa. Os versos 1–30 se repetem
para conferir o espelhamento. As notas são rascunhos de composição, sujeitos
a revisão filológica. A coluna lateral é reservada exclusivamente a vocabulário
e gramática, sem comentários históricos, literários ou interpretativos.
O vocabulário pode incluir pequenas imagens quando elas ajudam a identificar
o referente. Cada imagem deve acompanhar o lema grego e permanecer dentro
dos 62 mm da coluna, com proporção preservada e espaço até a nota seguinte.
Vocabulário muito básico, como ἵππος, não entra nas notas. A imagem de cavalo
foi retirada da composição e permanece em `imagens/hippos.png` como estudo
anterior; sua origem e prompt estão em [imagens/README.md](imagens/README.md).

## Convenções editoriais acordadas

A coluna lateral contém somente vocabulário e gramática.
O início da obra deve cair sempre em página ímpar (recto), usando `\page[right]`.
A numeração de página fica no rodapé da margem externa: à direita na página
ímpar e à esquerda na par, junto ao limite externo da área de notas.
A página par da primeira prova apenas repete o trecho para conferir o espelhamento;
não é uma segunda abertura da obra.

### Cabeçalho, rodapé e identificação de falas

Na coluna principal do cabeçalho, o título da tragédia fica para dentro e o
autor para fora: PERSAS à esquerda e ÉSQUILO à direita nas ímpares; nas pares,
ÉSQUILO à esquerda e PERSAS à direita. A coluna externa mostra os números
do primeiro e do último verso realmente presentes na página.

No rodapé, a coluna principal contém uma barra de progresso em ocre. A fração
preenchida corresponde ao último verso da página dividido por 1076. A barra
fica completa no fim da obra. A coluna externa contém apenas o número da página.
Os intervalos e o progresso usam as mesmas marcas de verso do ConTeXt.

Mudanças de personagem mostram o nome sem tarja ou filete, somente em grego,
em maiúsculas de 10 pt, peso regular e bordô. O nome fica recuado 6 mm,
alinhado ao grego, com intervalo curto antes da primeira fala; blocos
consecutivos do mesmo personagem recebem apenas pausa entre estrofes.
Personagens: ΧΟΡΟΣ, ΑΤΟΣΣΑ, ΑΓΓΕΛΟΣ, ΕΙΔΩΛΟΝ ΔΑΡΕΙΟΥ/ΔΑΡΕΙΟΣ e ΞΕΡΞΗΣ.

### Estado da prova integral

`persas.tex` compõe 62 páginas de leitura e uma página final com o gráfico
lexical (página 63), sem o antigo apêndice estatístico retirado.
O texto começa na página 1. A prova contém 792 entradas marginais em 581
blocos. Os sentidos repetidos são omitidos quando o apoio à forma ou à
construção justifica conservar a entrada. O banco original de entradas permanece preservado para revisão.

A entrelinha do grego é uniforme: 36 pt, em fonte de 14 pt. As notas não
acrescentam espaço entre versos, não deslocam a linha de base do verso e não
forçam quebras de página. A coluna principal foi ampliada para 118 mm:
112 mm para o grego e 6 mm para os números. A maior largura natural medida
é 110,84 mm (verso 730). Cada verso ocupa uma única linha tipográfica;
a quebra manual do verso 720 foi retirada. Os sinais internos `lb` dos
versos 909 e 984 são registrados na extração, mas apresentados com espaço
na mesma linha, sem alterar as palavras.

As notas são escolhidas por altura real medida no ConTeXt e por intervalos
compatíveis nas linhas de base fixas. Os destaques do Acrobat, os exemplos
aprovados e as crases têm prioridade. Quando há várias entradas para um
verso, a primeira linha do bloco alinha-se ao verso; as demais seguem abaixo.
A composição conserva 30 dos 34 destaques na margem. Três destaques ficam
em reserva por espaço; ἤδη foi excluído como vocabulário fundamental. São
190 entradas em `notas-em-reserva.json`, além de 207 exclusões editoriais
(206 de vocabulário fundamental e uma entrada de preposição unificada).

O banco completo de 1.297 entradas da prova anterior está preservado em
`revisoes/notas-ampliadas-2026-10-10.json`. Todos os 34 destaques continuam
registrados e calibram a seleção ao longo de toda a tragédia. O PDF comentado
original está preservado em `revisoes/persas-comentado-2026-10-10.pdf`, com
extração e integração nos arquivos de highlights da mesma pasta.

- `notas.json`: entradas efetivamente compostas; cada chave identifica o verso.
- `notas-candidatas.json`: banco de opções para substituir ou ampliar a seleção.
- `selecao-para-revisao.csv`: banco completo, com situação `sim`, `reserva`, `fundamental` ou `unificada`.
- `notas-em-reserva.json`: entradas que não couberam na composição atual.
- `ajustar-margens.py`: medição de combinações e seleção com entrelinha fixa.
- `lexico-editorial.tsv`: lemas, formas básicas e sentidos em português.
- `ajustes-notas.json`: correções de contexto e quebras de composição.
- `convencoes.py`: apresentação dos paradigmas nominais e abreviações.
- `crases.json`: formas contraídas e seus desdobramentos.
- `preposicoes.json`: regência, posição e sentido conforme o contexto.
- `aplicar-repeticoes.py`: omissão de sentidos já apresentados.
- `fontes/selecao-margens.json`: contagens, critérios e parâmetros da prova atual.

### Revisão por destaques no Acrobat

O editor marcará no PDF as palavras do texto grego que devem receber uma
entrada marginal e os textos da margem que devem ser excluídos. A localização
do destaque distingue inclusão de exclusão. Incorporar as marcações ao banco
e à seleção, recompilar e conferir novamente o alinhamento e o espaço das notas.
Preservar a prova recebida como referência para essa revisão.

#### Calibração pela leitura de Felipe, páginas 1–8 (10/10/2026)

Referência: `output/pdf/persas-integral_felipe.pdf`, versos 1–158.
As oito páginas foram lidas e conferidas visualmente. As 123 marcações
(119 destaques e quatro riscos) estão preservadas, com texto selecionado,
comentário, coordenadas e versos correspondentes, em
`revisoes/felipe-2026-10-10.json`. Reproduzir a extração com
`extrair-revisao-felipe.py`. O registro distingue 105 marcações de inclusão
ou ampliação, 16 de exclusão e duas de revisão explicativa. São marcações,
não quantidades de entradas: uma palavra repartida entre versos pode ter
dois destaques; uma marca pode abranger duas notas ou uma construção inteira.
Esses pedidos estão registrados para revisão; o registro não altera por si
só o PDF nem significa que as novas notas já estejam compostas.

A revisão estabelece estes critérios para **toda a tragédia**:

- Selecionar pelo obstáculo real à leitura na passagem: forma, sentido,
  construção e repertório necessário. As listas de frequência ajudam a
  decidir, mas não são um filtro absoluto para as margens. Uma palavra
  classificada como básica no estudo estatístico ainda pode exigir uma nota
  quando sua forma ou seu emprego apresenta uma dificuldade relevante.
- Ser generoso com compostos, vocabulário poético e variantes dialetais ou
  flexionais: por exemplo, `ἁβροδιαίτων`, `εὐτλήμονι`, `τοκέες`,
  `τρομέονται`, `βυσσίνοις`, `μονόζυξ`. Explicar sentidos contextuais, como
  `τέλη` e `ῥεύματι`, sem limitar a entrada à tradução mais usual do lema.
- Retirar sentidos elementares de preposições (`ἐς + ac. = para`) e notas
  assinaladas como básicas (`φοβερὰν`, `ὄψιν`, `ἔθνος`, `λαός`, `φρήν`,
  `φόβῳ`, `πέπλοις`, `ἄνασσα`, `μῆτερ`, `γεραιά`). Isso não impede apoio
  para um emprego diferente ou uma dificuldade gramatical posterior.
- Uma repetição só deve permanecer se resolver uma dificuldade nova.
  Omitir o sentido repetido não basta para justificar uma nota. Os riscos
  em `ὄχλον`, `στρατοῦ` e `στρατῷ` pedem a retirada da entrada inteira.
- Para subjuntivo e optativo, acrescentar uma explicação curta do valor
  efetivo da construção, inclusive o efeito de `ἄν` quando houver.
  Examinar também negação, subordinação e contexto; não deduzir o sentido
  apenas do rótulo morfológico. As marcações em `μή`, `πύθηται`, `πέσῃ`,
  `θώμεθα` e `εἴ τι μή` calibram esse apoio sintático. Explicar o aspecto
  do aoristo e o valor do perfeito quando isso ajudar a leitura.
- Tratar palavras repartidas entre versos como uma só unidade lexical:
  `πορ-/θμόν`, `ποιμα-/νόριον`, `πήδη-/μα`, `εὐρυπόροι-/ο`,
  `πολιαι-/νομένας`, `πεί-/σμασι`, `λα-/οπόροις`, `πύθη-/ται`,
  `γυναικοπλη-/θής`, `ἑκά-/στα` e `εὐνα-/τῆρ᾽`. Não criar lemas
  separados para os fragmentos nem alterar a divisão dos versos da fonte.
- Confirmar que uma tradução omitida já apareceu **na edição efetivamente
  composta**, no mesmo sentido; candidatos e notas em reserva não contam.
  Felipe perguntou isso em `ἱππιοχάρμας` (v. 105): o sentido
  “combatente a cavalo” foi dado para `ἱππιοχάρμης` no v. 29, página 2.
  Essa presença anterior não dispensa revisar a análise e o emprego da
  forma no v. 105, nem justifica repetir automaticamente a mesma entrada.
  A conferência no LSJ (`fontes/estudo-lexical/lsj-target.json`, entrada
  `ἱππιοχάρμης`, II) identifica aqui emprego adjetival: `ἱππιοχάρμας`
  concorda com `κλόνους` (ac. pl. masc.), “tumultos de combate a cavalo”.
  Portanto, a nota atual de nome no nom. sing. está incorreta e a tradução
  omitida deve ser substituída por uma explicação desse emprego; não se
  trata simplesmente de repetir o sentido do v. 29.
- A marcação atual de `ἤδη` no v. 9 deve ser respeitada como pedido de
  apoio, apesar da exclusão anterior. A decisão editorial específica mais
  recente prevalece sobre o filtro geral de vocabulário fundamental.

As marcações são uma amostra de calibração, não o limite da revisão.
Aplicar o mesmo julgamento aos trechos ainda não marcados, mantendo as
convenções de abreviação, o alinhamento marginal, a entrelinha uniforme e
um verso por linha. Não sacrificar explicações difíceis para preencher a
margem com entradas fáceis. A seleção automática por quantidade de entradas
e altura é apoio de composição; não substitui a escolha filológica.

A morfologia usa como apoio o **Perseus Treebank 2.1**, anotado por Francesco
Mambrini e normalizado por Giuseppe G. A. Celano. A base usa outra edição,
a de Smyth: as formas foram confrontadas com o texto de Sidgwick e não
substituem suas leituras. Ajustes de lema, caso, número, gênero e voz estão
registrados separadamente. `méd./pass.` identifica formas morfologicamente
sincréticas quando a seleção conserva essa análise. Os sentidos em português
e a escolha dos lemas foram preparados para esta prova.

O TEI contém 1063 elementos de verso, numerados de 1 a 1076. Seus saltos de
numeração são preservados: 124, 669, 674, 679, 869, 874, 879, 889, 895, 899,
989, 1019 e 1029 não têm elemento próprio na fonte. A lacuna explícita do
v. 982 aparece como `[…]`. Quebras internas (`lb`) são conservadas nos dados, mas não criam segunda
linha no PDF. Sinais críticos e palavras partidas entre versos seguem a fonte. As notas críticas do TEI não entram
no texto de leitura; o XML integral continua preservado para consulta.

`fontes/auditoria-extracao.json` registra a contagem e os saltos.
`fontes/linhas-extraidas.json` registra o texto e personagem de cada verso.
`verificar-pdf.py` confere a presença dos 1063 versos em sequência, os intervalos
dos cabeçalhos, o tamanho A4 e os limites físicos dos caracteres no PDF.
As 66 páginas da prova atual são renderizadas e revistas visualmente. A verificação
confere cada entrada marginal completa, seus limites horizontais, a ausência
de colisões e a coincidência da linha de base com o verso original.

### Cor e decoração: primeira proposta

- Texto grego e análise gramatical em preto.
- Palavras das entradas, nomes dos personagens e fólio em bordô `#7E3F38`.
- Cabeçalhos e título em preto na prova integral; na primeira prova,
  o título de abertura recebeu bordô.
- Pequeno meandro sob o título em ocre `#B48A48`, desenhado em MetaPost.
- Filete entre texto e notas em cinza quente `#B9ADA0`.

Esta paleta é uma proposta de composição, ainda sujeita à avaliação do editor.

### Formas verbais

**Forma no texto** ← lema de dicionário (*sentido*); tipo da forma e análise
gramatical abreviados. Identificar tempo, modo, voz, pessoa e número conforme
a forma; para particípios, identificar também caso, número e gênero.

Exemplo:

**οἰχομένων** ← οἴχομαι (*partir*); part., pres., méd., gen. pl. masc.

### Formas nominais

**Forma no texto** ← nominativo, terminação do genitivo, artigo grego
(*sentido*); caso e número. Quando o radical mudar, escrever a forma completa
do genitivo. O artigo indica classe e gênero: não acrescentar `subst.`,
`masc.`, `fem.` ou `neut.` às entradas de substantivos.

**νόστῳ** ← νόστος, -ου, ὁ (*retorno*); dat. sing.

**φρὴν** ← φρήν, φρενός, ἡ (*mente, coração*); nom. sing.

Adjetivos e particípios conservam suas variações básicas separadas por `/`
e a indicação abreviada de gênero na análise.

### Preposições e formas contraídas

Preposta: **ἐπὶ** *+ gen.* = *a bordo de*.

Posposta: *gen.* + **πέρι** = *acerca de*.

Desdobrar crases sem comentário redundante: **κοὔτε** ← καὶ οὔτε (v. 14).

### Repetições

Apresentar o sentido na primeira entrada efetivamente composta. Nas ocorrências
seguintes do mesmo lema e sentido, conservar apenas o apoio à análise da forma,
sobretudo verbal. Omitir entradas repetidas que não acrescentem informação
gramatical. Um sentido diferente exigido pelo contexto pode ser apresentado.
Nas preposições, considerar também o caso regido.

### Vocabulário ilustrado

Substantivos concretos selecionados por sua dificuldade podem entrar com uma
imagem. Abaixo dela,
colocar o lema no formato nominativo, genitivo abreviado, artigo, em caracteres gregos:

ἵππος, -ου, ὁ

Esse exemplo define apenas o formato da legenda. Por ser vocabulário básico,
ἵππος não deve aparecer na composição atual.

Preservar a proporção da imagem e a largura da coluna, sem sobrepor a nota
seguinte. A imagem deve ajudar a identificar o referente da palavra.

### Tipografia e abreviações

- A forma do texto aparece em **negrito**; o sentido, em *itálico*.
- No chat e em Markdown, um asterisco de cada lado indica itálico; dois,
  negrito. Na composição, aplicar os estilos tipográficos correspondentes.
- Diagramar a seta como **←**, substituindo a sequência textual `<-`.
- Usar vírgulas nos paradigmas de substantivos e `/` nos de adjetivos.
- Manter os números dos versos na faixa própria, sem cruzar o filete.
- Não repetir números de verso nas notas marginais.
- Omitir explicações já evidentes pela relação forma ← lema, como a elisão
  em **ἠδ᾽** ← ἠδέ. Não acrescentar “elisão da vogal final” nesse caso.
- A primeira linha da entrada marginal deve ter a mesma linha de base que
  o verso contendo a palavra original. Não deslocar a entrada para outra linha
  para resolver colisões. Não acrescentar espaços entre versos para acomodar
  notas: ajustar a seleção na margem, mantendo a entrelinha uniforme.

| Termo | Abreviação |
| --- | --- |
| substantivo | indicado pelo artigo grego |
| particípio | part. |
| infinitivo | inf. |
| conjunção | conj. |
| presente | pres. |
| voz média | méd. |
| voz ativa | at. |
| genitivo | gen. |
| dativo | dat. |
| singular | sing. |
| plural | pl. |
| masculino | masc. |
| feminino | fem. |
| neutro | neut. |

Abreviações adicionais: adj., nom., ac., voc., aor., perf., imperf.,
ind., subj., opt., imper., pass., compar., superl., adv. e indecl.
`dual` é escrito por extenso. Pessoa e número dos verbos finitos aparecem como `3ª s.` ou `3ª p.`.
Nos nomes e particípios, conservar `sing.` e `pl.`; indicar gênero nos adjetivos
e particípios, mas não nos substantivos com artigo.

Outros termos gramaticais também devem ser abreviados consistentemente.
O padrão aprovado está aplicado às entradas da prova atual. A entrada de
νόστῳ está alinhada ao v. 8, sem referência numérica na margem. Para evitar
colisão entre notas de versos consecutivos, a primeira amostra retirou ἐφορεύειν.
Na prova atual de entrelinha fixa, essa entrada está no banco de reserva. A primeira prova do grid conserva três entradas;
a prova integral usa a seleção ampliada descrita acima.

## Fonte

Scaife: https://scaife.perseus.org/reader/urn:cts:greekLit:tlg0085.tlg002.1st1K-grc1:1-30/

TEI obtido em:
https://raw.githubusercontent.com/OpenGreekAndLatin/First1KGreek/master/data/tlg0085/tlg002/tlg0085.tlg002.1st1K-grc1.xml

Edição de Arthur Sidgwick, *Aeschyli Tragoediae*, Oxford, Clarendon Press, 1902.
Digitalização Perseus / First1KGreek, CC BY-SA 4.0, conforme o cabeçalho TEI.
O XML foi preservado integralmente. O gerador mantém a numeração e retira
as notas críticas da leitura de cada verso; não modifica as palavras gregas.

Apoio morfológico:
https://github.com/PerseusDL/treebank_data/blob/master/v2.1/Greek/texts/tlg0085.tlg002.perseus-grc2.tb.xml

Copyright Perseus Digital Library, Tufts University. Licença CC BY-SA 3.0 US,
conforme o [README do repositório](https://github.com/PerseusDL/treebank_data).
O XML está preservado em `fontes/persas-treebank.xml`; o crédito aparece
também no colofão do PDF. Consultas lexicais complementares: LSJ via Scaife ATLAS.

## Compilação

Gerar o texto integral a partir do XML e das notas:

```sh
python3 gerar-edicao.py
```

No Ubuntu/WSL, em um diretório acessível pelo Linux, compilar a edição completa:

```sh
context --batchmode persas.tex
```

`texto-integral.tex` e `grafico-lexical.tex` precisam acompanhar `persas.tex`. O PDF resultante é
`persas.pdf`, copiado para `output/pdf/persas-integral.pdf` no projeto.
No Windows/Google Drive, copiar os três fontes para o diretório de compilação
em C: antes de chamar o WSL. Não é necessário recompilar o PDF do grid.

Para recompilar a prova revista, executar `gerar-edicao.py` e `gerar-grafico-lexical.py`,
copiar `persas.tex`, `texto-integral.tex` e `grafico-lexical.tex` para o diretório
de compilação e executar ConTeXt. Não rodar `selecionar-notas.py`,
`integrar-revisao.py` nem `acomodar-notas.py` sobre a prova revista: são etapas
anteriores e podem substituir as decisões atuais.

Se mudar o grid, a fonte ou a entrelinha, executar `ajustar-margens.py prepare`,
gerar o texto e compilar com `medicoes-notas.tex`. Essa etapa deixa temporariamente
`notas.json` vazio para medir o texto sem notas e todas as combinações do banco
preservado. Executar depois `ajustar-margens.py select CAMINHO_DA_COMPILACAO`,
`aplicar-repeticoes.py` e `gerar-edicao.py`, e recompilar. O programa conserva
as entradas não selecionadas em reserva. Para a prova final, executar
`verificar-pdf.py CAMINHO_DA_COMPILACAO`: além do texto e das margens, ele
confere que nenhum verso quebrou e que a entrelinha é uniforme entre versos
sem mudança de fala ou pausa estrófica.

Para a primeira prova de 30 versos:

```sh
context --batchmode grid-a4.tex
```

O arquivo `versos-1-30.tex` precisa estar no mesmo diretório.
Quando houver entradas ilustradas, copiar também os arquivos de imagem usados.
Para regenerar o trecho a partir do XML, execute `python3 gerar-prova.py`.

Ambiente verificado: Ubuntu 24.04.3, ConTeXt LMTX 2023.05.05 e LuaMetaTeX.
Como o WSL não traduz automaticamente esta unidade G: do Google Drive,
a compilação da prova usou uma cópia temporária em
`C:/Users/logop/AppData/Local/Temp/persas-context-grid`.
Os fontes definitivos continuam nesta pasta do projeto.

## Estatísticas lexicais: critérios em revisão

O apêndice anterior foi retirado da edição. Seus percentuais não representam
as categorias editoriais solicitadas e não devem ser citados como resultados
válidos. Fontes e análises anteriores estão preservadas em
`revisoes/estatisticas-retiradas-2026-10-10/`. `estatisticas.py` conserva o
cálculo diagnóstico de frequência, mas não volta a publicar esse apêndice.

A classificação deve considerar o lema **e o sentido da ocorrência**:

- **Grego geral/básico:** levantar um repertório pedagógico amplo, com revisão
  de sentidos. Os 500 itens DCC são apenas uma referência parcial.
- **Compartilhado pela tragédia:** usos equivalentes em diferentes
  tragediógrafos. Sua presença em Ésquilo não os torna exclusivos dele.
- **Exclusivo de Ésquilo:** lema ou sentido documentado como exclusivo do
  autor. Uma frequência maior, ou ausência na pequena amostra atual, não
  comprova exclusividade. Esses casos precisam de investigação lexical.
- **Usos de outros contextos:** indicar o contexto concreto e conferir o
  sentido empregado em Persas. Frequência em prosa ou épica, isoladamente,
  não permite classificar o uso na tragédia.

Usos compartilhados não entram na categoria exclusiva de Ésquilo. Um lema
pode ter sentidos de categorias diferentes; por isso a revisão deve partir
das ocorrências. Casos sem evidência suficiente ficam pendentes. Os números
serão recalculados após essa revisão, antes de retornar ao fim do texto.
Critérios registrados em `fontes/criterios-classificacao-lexical.json`.

### Estudo lexical — resultado conservador de 10 de outubro de 2026

O levantamento atual substitui os números do apêndice retirado. Ele contabiliza
5.187 palavras gráficas reconstruídas do texto desta edição: foram reunidos
31 fragmentos de palavras separados entre versos, sem alterar os versos da
edição. Crases permanecem uma ocorrência gráfica; seus componentes entram
na verificação do repertório básico. Pontuação e identificação do personagem
não entram na contagem.

O denominador principal é **4.860 ocorrências de vocabulário comum**.
Foram separados **327 nomes próprios, gentílicos e adjetivos geográficos**,
incluindo personificações divinas identificadas no contexto. Compostos lexicais
como δαρειογενής e περσονόμος, e usos comuns como παιάν, foram conferidos e
reintegrados ao vocabulário. Existem **1.635 lemas comuns resolvidos**. A leitura
corrupta διαγόεν, v. 676, continua sem lema e entra no residual das ocorrências.

| Classe, aplicada nesta ordem | Ocorrências | % das ocorrências | Lemas | % dos lemas |
| --- | ---: | ---: | ---: | ---: |
| Básico fundamental | 3.290 | 67,70% | 550 | 33,64% |
| Característico da tragédia, descontado o básico | 785 | 16,15% | 450 | 27,52% |
| Atestação exclusiva em Ésquilo na documentação consultada, descontadas as anteriores | 123 | 2,53% | 103 | 6,30% |
| Usos épicos/líricos anteriores ou contemporâneos, descontadas as anteriores | 74 | 1,52% | 62 | 3,79% |
| Geral não fundamental / atribuição contextual não demonstrada | 588 | 12,10% | 470 | 28,75% |

As ocorrências têm exatamente uma classe e totalizam 100%. Cada lema resolvido
tem uma classe nesta versão; o programa verifica isso antes de publicar a coluna
de lemas. Se uma revisão introduzir sentidos de classes distintas para o mesmo
lema, essa coluna terá de ser recalculada por unidades de lema e sentido. O
denominador dos lemas exclui a leitura não resolvida; o das ocorrências a inclui.

**Básico fundamental.** Repertório operacional de **1.286 lemas**, pela união
da lista pedagógica de Wilfred Major, dos primeiros 500 itens DCC e dos primeiros
1.000 itens de frequência Logeion. Variantes de lema são conciliadas. Não se
trata de uma lista universal de tudo que um leitor deve saber, nem de uma
definição baseada somente em frequência. Major fornece a referência pedagógica;
DCC e Logeion complementam a cobertura. A presença no repertório é avaliada
pelo lema; sentidos especializados de palavras básicas ainda precisam de
revisão semântica. A lista maior usada aqui não altera automaticamente o filtro
editorial das margens, que conserva suas decisões próprias.

**Tragédia.** Comparação com 25 outras peças: cinco de Ésquilo, sete de Sófocles
e treze de Eurípides. Persas não serve como evidência comparativa de si mesma.
Prometeu acorrentado e Reso foram separados por atribuição discutida; Ichneutae
foi separado por ser drama satírico. A versão disponível do Diorisis não contém
todas as tragédias de Eurípides; Medeia foi acrescentada pelo Pedalion.
O critério quantitativo exige presença em três outras peças, em dois autores,
e densidade relativa pelo menos duas vezes maior que no conjunto não trágico
anterior a 300 a.C., ou marca trágica explícita no LSJ. Entradas raras com usos
equivalentes em diferentes tragediógrafos, documentadas pelo LSJ, complementam
essa triagem. Esta classe ainda inclui inferências de distribuição feitas
por lema: não equivale a uma conferência manual de todos os sentidos em todas
as peças. As datas agregadas e a lematização automática do corpus são limitações
da comparação, não provas de origem histórica de uma palavra.

**Ésquilo.** Foram aceitos lemas com atestação literária apenas em Ésquilo nas
entradas do LSJ consultadas, corroborados pela ausência de ocorrência independente
no corpus, ou sentidos específicos da passagem que o LSJ documenta apenas nele.
A ausência no corpus, sozinha, não basta. Uma concentração maior no autor não
é exclusividade. Por exemplo, δίεμαι nos vv. 700–701 significa “temer” (LSJ II,
A.Pers.701), enquanto o uso homérico citado pelo LSJ significa deslocar-se
rapidamente. εὐθυντήριος, v. 764, é “que governa”, distinto do uso substantivado
na construção naval em Eurípides. A categoria significa **exclusividade de
atestação na documentação consultada**, não comprovação universal de que
Ésquilo inventou o lema ou o sentido. Palavras dependentes de conjecturas ou
variantes inseguras foram deixadas no residual. As decisões e as acepções
distintivas estão registradas separadamente para revisão.

**Outros contextos.** Registro positivo conservador de usos épicos ou líricos
equivalentes ao da passagem, documentados antes do fim da vida de Ésquilo,
**456 a.C.** Homero, Hesíodo e poetas arcaicos fornecem as referências; odes de
Píndaro só são usadas quando a data cabe no recorte. Obras ou coleções de data
incerta não foram admitidas apenas pela data global de seu catálogo. Não basta
que o lema apareça cedo: φιλόφρων e νησιώτης, por exemplo, têm atestação antiga,
mas foram deixados no residual porque isso não demonstra tipicidade literária.
O levantamento não atribuiu classes positivas à prosa médica, filosófica ou
historiográfica sem evidência cronológica e semântica suficiente. Portanto,
**1,52% é uma parcela positivamente documentada, não uma estimativa exaustiva
de todos os usos pertencentes a outros contextos**. O residual contém palavras
gerais pouco frequentes e também possíveis atribuições ainda não demonstradas.

**Sensibilidade ao tamanho do repertório básico.** A troca da faixa Logeion
altera o primeiro grupo e os grupos seguintes, respeitando os descontos:

| Repertório básico | Lemas no repertório | Básico no texto | Tragédia no texto |
| --- | ---: | ---: | ---: |
| Major + DCC | 1.126 | 65,68% | 16,15% |
| Major + DCC + Logeion 1.000 — critério principal | 1.286 | 67,70% | 16,15% |
| Major + DCC + Logeion 2.000 — faixa ampliada | 2.103 | 72,86% | 12,82% |

Os números são resultados de uma classificação conservadora e auditável.
As classes 2–4 e os sentidos especializados da classe 1 permanecem sujeitos
a revisão filológica antes de serem tratados como percentuais finais para
publicação. O PDF apresenta uma página final de gráfico, identificada como
levantamento preliminar, e continua sem o antigo apêndice estatístico.

O gráfico da página 67 é vetorial, composto em MetaPost pelo ConTeXt. Mostra
as porcentagens das ocorrências nas quatro classes e no residual, com barras
de escala comum de 0 a 100%. `gerar-grafico-lexical.py` lê os resultados do
estudo e gera `grafico-lexical.tex`; os percentuais não são redigitados.
O cabeçalho conserva título e autor, e o rodapé mantém o progresso completo
e a página na margem externa. A versão anterior, de 66 páginas, está
preservada em `revisoes/persas-sem-grafico-2026-10-10.pdf`.

Arquivos para examinar o levantamento:

- `fontes/estudo-lexical/classificacao-por-ocorrencia.csv`: palavra, verso,
  lema, sentido distintivo, classe e fundamento da classificação.
- `fontes/estudo-lexical/classificacao-por-lema.csv`: frequência na peça,
  versos, referências e evidência comparativa.
- `fontes/estudo-lexical/resultado-lexical.json`: contagens e sensibilidade.
- `fontes/estudo-lexical/decisoes-revisadas.json`: decisões sobre os lemas
  conferidos diretamente, incluindo exclusões de candidatos automáticos.
- `fontes/estudo-lexical/triagem-lexical.json`: triagem quantitativa e entradas
  do LSJ usadas como evidência; seus candidatos não são o resultado final.
- `fontes/estudo-lexical/conferencia-lemas.json`: junções e correções de análise.

Fontes principais:

- [Wilfred E. Major (2008), core vocabulary para o ensino do grego](https://camws.org/cpl/cplonline/files/Majorcplonline.pdf).
- [DCC, Greek Core Vocabulary](https://dcc.dickinson.edu/greek-core-list).
- [Logeion, lista de frequência publicada em 2024](https://voices.uchicago.edu/logeion/2024/01/02/placeholder-frequency-list/).
- [Diorisis Ancient Greek Corpus, arquivo JSON e metadados](https://figshare.com/articles/dataset/The_Diorisis_Ancient_Greek_Corpus_JSON_/12251468).
- [LSJ, versão digital e arquivos do dicionário](https://github.com/perseids-project/lsj-js).
- [Pedalion Trees](https://github.com/pedalion/pedalion-trees).

O índice recompilado contém 816 obras e 8.118.532 ocorrências comuns lematizadas.
O estudo utiliza atualizações Diorisis registradas por obra, com o texto de
Persas 1.6 conservado localmente. O índice derivado e as fontes congeladas
permitem repetir a classificação sem conexão à internet. Para reconstruir o
índice bruto, `indexar-corpus-lexical.py` aceita `--archive` e `--updates`, para
o ZIP Diorisis e a pasta de atualizações. A confirmação das palavras desta
edição e a classificação são executadas assim:

```text
python livros/persas/conferir-lemas-estudo.py
python livros/persas/finalizar-estudo-lexical.py
```

`manifesto-fontes.json` registra hashes dos arquivos usados. A validação
confere cobertura integral, soma das classes, precedência do básico e
conciliação das contagens por ocorrência e por lema. Ela não substitui a
conferência filológica dos sentidos.

### Créditos e fontes conservados na documentação

Texto grego: A. Sidgwick, *Aeschyli Tragoediae* (Oxford, 1902).
Digitalização: Perseus / First1KGreek, CC BY-SA 4.0.
Apoio morfológico: F. Mambrini, Perseus Treebank 2.1, CC BY-SA 3.0 US.
Fontes comparativas: Perseus Treebank, Pedalion Trees e DCC; os dados,
metadados e licenças permanecem em `fontes/`.
O bloco de créditos da última página de leitura e a seção “Corpus e limites”
foram retirados do PDF a pedido do usuário.

## Revisão das margens — 10 de outubro de 2026

A coluna de notas passa de 48 para 62 mm, preservando os 112 mm de grego e
a entrelinha uniforme. A prova anterior está arquivada em
`revisoes/persas-prova-14-32-margem48-2026-10-10.pdf`.

A entrada do verso 18 apresenta `ἐφ᾽ ← ἐπί + gen. = sobre, a bordo de`;
ela cobre também a ocorrência do verso 19. A segunda entrada foi unificada.

`vocabulario-fundamental.json` registra 175 lemas: os primeiros 150 por
frequência da lista DCC e 25 acréscimos editoriais, incluindo πόλεμος e μέγας.
Trata-se de um recorte inicial para esta edição, sujeito à revisão; a lista
DCC de 500 palavras do antigo apêndice é uma referência parcial, não
a definição do vocabulário básico. O filtro não
exclui automaticamente formas difíceis: pode manter análise verbal sem
repetir o sentido básico, além de desdobramentos de crases e preposições
contextuais. `fontes/filtro-editorial.json` registra cada decisão.

O fluxo aplica `filtro-editorial.py` antes de medir e selecionar as notas.
Exclusão editorial e reserva por falta de espaço são estados distintos.

Verificação desta prova: 66 páginas, 1.063 versos em uma linha cada, 900 entradas
sem sobreposição ou transbordamento. Todas as páginas foram renderizadas e
inspecionadas; relatório em `fontes/verificacao-integral.json`.

## Rodada de Felipe — 11 de outubro de 2026

A prova foi recompilada a partir das marcações das primeiras oito páginas e
da regra adicional de explicitar a **regência** na margem. Adjetivos e verbos
recebem, quando a construção exige apoio, o caso ou a forma de complemento
com o sentido contextual. Exemplo composto no v. 162:

**ἀδείμαντος** ← ἀδείμαντος/-ον (*sem temor*); adj., nom. sing. fem.;
+ gen.: sem temor por; οὐδαμῶς: de modo algum.

O apoio sintático não se limita às preposições. Esta rodada inclui regência
em ἐφορεύειν, στεῦται, πεποιθώς, πίσυνοι e μέμνησθ᾽, entre as entradas
efetivamente selecionadas. O banco registra ainda outras explicações para
composição futura. Subjuntivo e optativo têm valores verificados na passagem:
temor, exortação, desejo, possibilidade, condição, tempo ou finalidade,
conforme a construção. Não atribuir um mesmo valor a todas as ocorrências.

As exclusões pedidas na abertura foram aplicadas. As formas poéticas e os
compostos recebem mais apoio; palavras repartidas entre versos são mostradas
completas na nota, por meio de `forma_exibida`, mantendo `forma` como âncora
no verso da fonte. O emprego adjetival de ἱππιοχάρμας foi corrigido. Foram
corrigidas também análises espúrias de ὦ e ἄν e a confusão entre εἶμι e εἰμί;
formas elementares do presente de εἰμί foram retiradas das margens.

A fonte permanece em 14 pt. A entrelinha passa a 48 pt, uniformemente,
para reduzir versos por página e acomodar explicações mais completas.
São 102 páginas de texto e o gráfico na página 103. Todos os 1.063 versos
foram conferidos em sequência, em uma linha cada, e todas as 928 entradas
compostas passaram na verificação de conteúdo, alinhamento e limites físicos.
As páginas foram renderizadas e inspecionadas, com conferência em detalhe
dos novos blocos sintáticos e da página do gráfico.

A rodada **ainda tem reservas**: dez entradas pedidas na abertura e duas
propostas adicionais do v. 162 não couberam na seleção. Permanecem no banco,
com a lista nominal em `revisoes/aplicacao-felipe-2026-10-11.json`:
πελάτης (49), ἡμερολεγδόν (63), πήδημα (95), ἐκλέλοιπεν (128),
ἀποπεμψαμένα (138), ἄρα e πράσσει (144), πολιαινομένας (109),
λαοπόροις (113), εὐνάτειρα (157), ἐμαυτῆς e οὖσα (162).
A regência de ἀδείμαντος foi composta no v. 162; suas duas notas adicionais
não foram necessárias para explicar a regência nessa passagem. Não declarar
essas reservas como marcações já atendidas. O banco geral tem 109 entradas
em reserva; as retiradas por redundância são registradas separadamente.

`rodada-felipe.py` produz o banco revisado. `ajustar-margens.py` mede e
seleciona a partir dele; a medição deve ser refeita se o banco ou o filtro
for alterado. `aplicar-repeticoes.py` corta redundâncias após a seleção real,
e `gerar-edicao.py` compõe as notas. O relatório final está em
`fontes/verificacao-integral.json`. A prova anterior foi preservada em
`revisoes/persas-antes-rodada-felipe-2026-10-11.pdf`.

## Prova de entrelinha 38 pt — 11 de outubro de 2026

A pedido do editor, a entrelinha de 48 pt foi reduzida para **38 pt**,
com a fonte grega em 14 pt. A proposta intermediária de 40 pt foi substituída
antes da entrega. As notas continuam em 9/12 pt. A prova anterior de 48 pt
está preservada em `revisoes/persas-14-48-2026-10-11.pdf`.

As margens foram medidas e selecionadas novamente para a paginação mais
compacta. A nova prova contém 78 páginas de texto e o gráfico na página 79,
com 877 entradas compostas. A reserva geral passou a 162 entradas, sem
confundir reserva de composição com exclusão editorial. O banco revisado
permanece conservado. A regência de ἀδείμαντος continua composta no v. 162.

Os 1.063 versos passaram na conferência de sequência, entrelinha uniforme,
uma linha por verso, alinhamento das margens e ausência de colisões ou
transbordamento. Todas as páginas foram renderizadas e conferidas visualmente.
Na conclusão desta rodada, `fontes/verificacao-integral.json` correspondia à prova de 38 pt; as contagens
na seção da rodada de 48 pt descrevem a prova anterior.

## Prova de 36 pt e divisão em partes — 11 de outubro de 2026

Fonte grega mantida em 14 pt; entrelinha reduzida para 36 pt. A versão de 38 pt foi preservada em `revisoes/persas-14-38-2026-10-11.pdf`.

- **Párodo:** v. 1–154.
- **Primeiro Episódio:** v. 155–531.
- **Primeiro Estásimo:** v. 532–597.
- **Segundo Episódio:** v. 598–622.
- **Segundo Estásimo / Canto de Evocação:** v. 623–680.
- **Terceiro Episódio:** v. 681–851.
- **Terceiro Estásimo:** v. 852–907.
- **Éxodo:** v. 908–1077.

Os títulos precedem o primeiro verso de cada parte, junto à tarja de personagem quando houver. Há espaço apenas para essa hierarquia estrutural; os versos corridos mantêm distância uniforme. O intervalo do Éxodo segue o solicitado (908–1077); a numeração do texto-fonte termina em 1076 e não foi alterada.

Prova atual: 75 páginas de leitura e gráfico na página 76; 812 entradas em 595 blocos; 238 candidatas em reserva antes da retirada de redundâncias. A seleção foi conferida nas posições efetivas da composição anotada, com folga acima do rodapé. Para replicar, preservar o log de medição das opções e executar novamente `ajustar-margens.py select BUILD LOG_DE_MEDICAO` após a primeira composição anotada, seguido de `aplicar-repeticoes.py`, geração e compilação.

O registro atual em `fontes/verificacao-integral.json` corresponde à prova de 36 pt, com as oito transições conferidas na mesma página de seu primeiro verso.


## Abertura compacta e gráfico de pizza — 11 de outubro de 2026

A abertura usa uma caixa vertical para o título e o meandro, com intervalo de 2 mm entre eles, sem herdar a entrelinha de 36 pt do texto grego. A entrelinha dos versos permanece em 36 pt, fonte 14 pt. As margens foram recompostas nas posições efetivas da nova abertura.

O gráfico de barras foi substituído por uma pizza vetorial gerada pelo ConTeXt/MetaPost, com legenda e percentuais. Os dados do estudo permanecem os mesmos. O rótulo ambíguo “Uso geral / atribuição pendente” foi substituído por “Ainda não classificados”: são 588 ocorrências (12,10%) sem atribuição demonstrada às quatro categorias solicitadas. Esse setor cinza expõe a lacuna do levantamento e não constitui um quinto contexto literário. Sua remoção ou redistribuição sem estudo adicional falsearia a composição do total.

A prova mantém 75 páginas de texto e o gráfico completo na página 76. Verificação geométrica e textual concluída, seguida de inspeção visual da abertura e do gráfico. A versão anterior foi conservada em `revisoes/persas-14-36-antes-pizza-2026-10-11.pdf`.

## Hierarquia das partes e falantes — 11 de outubro de 2026

Divisão estrutural numa única linha: **Párodo — versos 1–154**, por exemplo. A faixa de fundo claro, com 6 mm, agora pertence às partes. O título usa negrito de 11 pt e o intervalo, peso regular de 9,5 pt. Antes da faixa há 4 mm; depois, 1 mm. A conferência dos limites reais dos glifos confirmou que o espaço após cada título não supera o espaço anterior.

O nome do falante perdeu a faixa e o filete: grego em maiúsculas de 10 pt, peso regular, recuado 6 mm e alinhado à fala. O intervalo explícito abaixo do nome é de 1,5 mm, sem a cola de entrelinha de 36 pt aplicada às mudanças de falante na prova anterior. A caixa da primeira linha usa estruto menor; a fonte continua em 14 pt e as distâncias entre versos corridos continuam em 36 pt, verificadas no PDF. As 176 mudanças de falante foram verificadas: distância entre limites dos glifos do nome e da primeira fala entre 1,18 e 3,74 pt, sem nomes isolados na página anterior.

Estado atual: 62 páginas de leitura e gráfico de pizza na página 63; 792 entradas em 581 blocos e 259 candidatas em reserva antes da retirada de redundâncias. A versão anterior está preservada em `revisoes/persas-antes-hierarquia-2026-10-11.pdf`. O registro `fontes/verificacao-integral.json` inclui as oito partes, seus intervalos de espaçamento e a conferência das mudanças de falante. Inspeção visual de todas as páginas concluída.

A recompilação deve completar os passes do ConTeXt para resolver a página e o lado das notas externas; uma única passagem após a reseleção pode conservar posições de margem da paginação anterior.


## Organização no repositório — 23 de outubro de 2026

A edição foi transferida para `livros/persas/`, separada da implementação web em `html/`. Fontes, scripts, dados e revisões continuam reunidos nesta pasta; o PDF atual está em `output/pdf/persas-integral.pdf`, relativo à pasta da edição. A cópia antiga em `output/pdf/`, na raiz do checkout, foi mantida apenas para compatibilidade local e fica fora do versionamento.

Os scripts usam caminhos relativos ao próprio arquivo. O baixador do corpus e a leitura do PDF comentado foram ajustados para essa organização. Os comandos executados a partir da raiz do repositório devem usar o prefixo `livros/persas/`.
