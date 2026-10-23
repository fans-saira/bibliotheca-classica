# Bibliotheca Classica

Projeto de edições de textos clássicos. A primeira edição em preparação é
*Persas*, de Ésquilo, com texto grego e apoio de vocabulário e gramática na margem.

## Repositório do projeto

- GitHub: https://github.com/fans-saira/bibliotheca-classica
- Remote `origin`: `git@github.com:fans-saira/bibliotheca-classica.git`
- Branch principal: `main`.

## Organização do repositório

- [`html/`](html/README.md): projeto web em HTML, separado das edições impressas.
- [`livros/`](livros/README.md): projetos de livros, cada um em sua própria pasta.
- [`livros/persas/`](livros/persas/README.md): primeira edição, com seus fontes,
  dados lexicais, revisões e [PDF atual](livros/persas/output/pdf/persas-integral.pdf).

O código da aplicação HTML ainda não está presente neste checkout; sua pasta
foi reservada com documentação. Novos livros entram em `livros/<identificador>/`.

## Persas

A diagramação utiliza ConTeXt no Ubuntu/WSL2, em páginas A4 espelhadas.
As medidas do grid, fontes, origem do texto, instruções de compilação e
convenções editoriais estão em [livros/persas/README.md](livros/persas/README.md).

- Fonte da prova integral: [livros/persas/persas.tex](livros/persas/persas.tex).
- Gerador integral: [livros/persas/gerar-edicao.py](livros/persas/gerar-edicao.py).
- Entradas marginais: [livros/persas/notas.json](livros/persas/notas.json).
- PDF integral: [prova atual](livros/persas/output/pdf/persas-integral.pdf), incluída no repositório.
- Fonte da primeira prova do grid: [livros/persas/grid-a4.tex](livros/persas/grid-a4.tex).
- Gerador do trecho: [livros/persas/gerar-prova.py](livros/persas/gerar-prova.py).
- Prova em PDF: `livros/persas/output/pdf/persas-grid-a4.pdf` (arquivo gerado localmente).

As decisões editoriais acordadas devem ser registradas no README da edição
durante o trabalho. A prova aplica as convenções de apresentação acordadas,
com entradas alinhadas aos versos e seleção de vocabulário que exclui palavras
muito básicas. O formato de vocabulário ilustrado está documentado para uso futuro.
A prova integral contém 62 páginas de leitura em fonte 14 pt / entrelinha uniforme
de 36 pt, com 792 entradas marginais, seguidas pelo gráfico de pizza lexical na página 63.
O gráfico apresenta os resultados conservadores do novo estudo; o antigo
apêndice estatístico permanece retirado.
Cada verso ocupa uma única linha. As notas não acrescentam espaço entre versos;
a coluna principal foi ampliada para 118 mm. As partes têm faixa clara e título
com versos na mesma linha; os personagens aparecem sem faixa, apenas em grego
maiúsculo, junto à primeira fala. As 259 entradas excedentes
permanecem no banco de reserva para revisão.
Os candidatos adicionais ficam em [livros/persas/notas-candidatas.json](livros/persas/notas-candidatas.json).

A coluna de notas foi ampliada para 62 mm. O filtro de vocabulário fundamental
e as exclusões editoriais estão documentados no README da edição.

A revisão de Felipe até a página 8 (versos 1–158) foi lida e registrada em
`livros/persas/revisoes/felipe-2026-10-10.json`, com 123 marcações. Seus critérios
passam a orientar toda a obra: ampliar o apoio para dificuldades lexicais e
sintáticas, cortar sentidos básicos e repetições sem dificuldade nova, e
explicar o valor contextual do subjuntivo e do optativo. Frequência não é
um veto automático à inclusão de uma nota. Os detalhes estão na seção de
revisão por destaques do README da edição. A rodada de 11/10/2026 incorporou as correções ao banco e recompilou o PDF,
com regência contextual e explicações dos modos. Dez entradas pedidas na
abertura permanecem em reserva por espaço, além de duas propostas adicionais
do v. 162; os detalhes estão no registro de aplicação e no README da edição.

O novo estudo lexical está documentado em `livros/persas/README.md`, com classificação
por ocorrência em `livros/persas/fontes/estudo-lexical/classificacao-por-ocorrencia.csv`.
As categorias são aplicadas em ordem, sem contar a mesma ocorrência duas vezes.
Os resultados conservadores distinguem o repertório básico, o uso trágico,
a atestação exclusiva em Ésquilo e usos épicos/líricos anteriores ou contemporâneos.
Casos gerais ou sem atribuição demonstrada permanecem numa classe residual.

A prova atual usa entrelinha de 36 pt, solicitada em 11/10/2026; a versão
de 48 pt foi preservada para comparação. As margens foram recompostas e
verificadas para a nova paginação.

A prova de 36 pt apresenta as oito partes da tragédia, com títulos e intervalos de versos no início de cada parte.
