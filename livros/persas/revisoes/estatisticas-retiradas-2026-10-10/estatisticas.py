"""Reproducible, scoped lexical comparison. No inference of word origins."""
from pathlib import Path
from collections import Counter, defaultdict
import json, re, unicodedata as U, xml.etree.ElementTree as ET, csv
base=Path(__file__).resolve().parent
out=base/'fontes'
def lemma(s):
    return U.normalize('NFC',re.sub(r'\d+$','',s.strip())).replace('ϲ','σ')
def form(s):
    return ''.join(c for c in U.normalize('NFD',s).lower() if c.isalpha()).replace('ς','σ')
def lexical(w):
    s=w.get('lemma','');return bool(s and any(c.isalpha() for c in s) and not w.get('postag','').startswith('u') and w.get('form'))
def common(s):return not s[0].isupper()
def counts(path):
    return Counter(lemma(w.get('lemma')) for w in ET.parse(path).iter('word') if lexical(w) and common(w.get('lemma')))
tree=defaultdict(list)
for w in ET.parse(out/'persas-treebank.xml').iter('word'):
    if lexical(w) and w.get('cite'):
        tree[form(w.get('form'))].append((int(w.get('cite').split(':')[-1]),lemma(w.get('lemma'))))
tokens=[]
for line in json.loads((out/'linhas-extraidas.json').read_text(encoding='utf-8')):
    for raw in line['text'].split():
        if raw=='BREAKLINE' or not form(raw):continue
        n=line['n'];opts=tree.get(form(raw),[])
        nearest=min((abs(v-n) for v,l in opts),default=999)
        ls={l for v,l in opts if abs(v-n)==nearest}
        l=next(iter(ls)) if nearest<=3 and len(ls)==1 and not raw.endswith('-') else ''
        tokens.append({'verso':n,'forma':raw,'lema':l,'estado':'nome próprio' if l and not common(l) else 'analisado' if l else 'não classificado','distancia':nearest if l else ''})
target=Counter(x['lema'] for x in tokens if x['estado']=='analisado')
core={lemma(re.split(r'[ ,;]',r['headword'])[0]) for r in json.loads((out/'dcc-core.json').read_text(encoding='utf-8'))['rows'] if r['rank']<=500}
# Explicit lexical equivalences; no accent stripping of lemmas (εἰμί != εἶμι).
aliases={'οὐ':'οὐ','εἶπον':'λέγω','εἶδον':'ὁράω'}
corpora=out/'corpus-comparativo';works=[]
for m in json.loads((corpora/'manifest.json').read_text(encoding='utf-8')):
    if m['author']=='0085' and m['work']==2:continue
    group={'0085':'Ésquilo','0011':'Sófocles','0012':'épica'}[m['author']]
    c=counts(corpora/m['name']);works.append(dict(m,group=group,counts=c,total=sum(c.values())))
for m in json.loads((corpora/'pedalion-manifest.json').read_text(encoding='utf-8')):
    if 'error' in m:continue
    group={'Euripides':'Eurípides','Aristophanes':'comédia','Aeneas Tacticus':'militar','Heron':'técnica'}.get(m['author'],'prosa literária')
    c=counts(corpora/m['name']);works.append(dict(m,group=group,counts=c,total=sum(c.values())))
groups=defaultdict(Counter);totals=Counter()
for w in works:groups[w['group']].update(w['counts']);totals[w['group']]+=w['total']
trag=groups['Ésquilo']+groups['Sófocles']+groups['Eurípides'];nt=sum(trag.values())
other=groups['Sófocles']+groups['Eurípides'];no=sum(other.values())
def rate(c,n,l):return c[l]/n*10000
sets={'básico DCC':set(),'recorrente na tragédia':set(),'preferência por Ésquilo':set(),'mais frequente fora da tragédia':set()}
detail=[]
for l in sorted(target):
    if aliases.get(l,l) in core:sets['básico DCC'].add(l)
    plays=[w for w in works if w['group'] in ['Ésquilo','Sófocles','Eurípides'] and w['counts'][l]]
    if len(plays)>=3 and len({w['group'] for w in plays})>=2:sets['recorrente na tragédia'].add(l)
    aesplays=[w for w in plays if w['group']=='Ésquilo']
    ar=(groups['Ésquilo'][l]+.5)/totals['Ésquilo'];orr=(other[l]+.5)/no
    if groups['Ésquilo'][l]>=3 and len(aesplays)>=2 and ar/orr>=4:sets['preferência por Ésquilo'].add(l)
    contexts=[g for g in ['épica','comédia','militar','técnica','prosa literária'] if groups[g][l]>=5 and (groups[g][l]+.5)/totals[g]>=4*(trag[l]+.5)/nt]
    if contexts:sets['mais frequente fora da tragédia'].add(l)
    detail.append({'lema':l,'ocorrencias':target[l],'classes':[k for k,v in sets.items() if l in v],'contextos':contexts,'frequencias_por_10000':{g:round(rate(c,totals[g],l),3) for g,c in groups.items()}})
summary={'data':'2026-10-10','tokens_impressos':len(tokens),'tokens_analisados':sum(target.values()),'lemas_analisados':len(target),'nomes_proprios':sum(x['estado']=='nome próprio' for x in tokens),'nao_classificados':sum(x['estado']=='não classificado' for x in tokens),'categorias':{k:{'lemas':len(v),'ocorrencias':sum(target[l] for l in v),'percentual_lemas':round(100*len(v)/len(target),1),'percentual_ocorrencias':round(100*sum(target[l] for l in v)/sum(target.values()),1)} for k,v in sets.items()},'corpus':[dict((k,v) for k,v in w.items() if k!='counts') for w in works],'totais_corpus':dict(totals),'lemas':detail}
(out/'estatisticas-lexicais.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
with (out/'tokens-estatisticas.csv').open('w',encoding='utf-8-sig',newline='') as f:
    wr=csv.DictWriter(f,fieldnames=tokens[0].keys());wr.writeheader();wr.writerows(tokens)
def pct(n,d):return f'{100*n/d:.1f}'.replace('.',',')
def thousands(n):return f'{n:,}'.replace(',','.')
def tex(s):return s.replace('&',r'\&').replace('%',r'\%').replace('_',r'\_')
t=[r'\page',r'\setupbackgrounds[page][background=appendixfurniture]',r'\switchtobodyfont[11pt]',r'\setupinterlinespace[line=15pt]',r'\setupalign[flushleft,nothyphenated,verytolerant,stretch]',r'{\switchtobodyfont[20pt]\color[accent]{O vocabulário de Persas}}\par',r'\blank[5mm]',r'{\bf Levantamento preliminar}\par',r'\blank[2mm]',f"Este levantamento reúne {thousands(len(target))} lemas em {thousands(sum(target.values()))} ocorrências analisadas, sem nomes próprios.",r'\par\blank[3mm]',r'\starttabulate[|p(56mm)|r|r|]',r'\NC \bf Categoria \NC \bf Lemas \NC \bf Ocorrências \NC\NR',r'\HL']
for k,v in summary['categorias'].items():t.append(r'\NC '+tex(k)+r'\NC '+str(v['lemas'])+' ('+str(v['percentual_lemas']).replace('.',',')+r'\%) \NC '+str(v['ocorrencias'])+' ('+str(v['percentual_ocorrencias']).replace('.',',')+r'\%) \NC\NR')
t += [r'\stoptabulate',r'\blank[3mm]',r'As categorias se sobrepõem: seus percentuais não devem ser somados. Lema é a entrada do dicionário; ocorrência é cada aparição de uma forma no texto.\par',r'\blank[3mm]',r'{\bf Como ler as categorias}\par',r'\blank[2mm]',r'{\bf Básico DCC.} Pertencimento à lista de 500 palavras do Dickinson College Commentaries; os 24 numerais suplementares foram excluídos. É uma referência pedagógica, não uma medida absoluta de facilidade.\par',r'\blank[2mm]',r'{\bf Recorrente na tragédia.} Presença em pelo menos três outras peças e em dois autores da amostra. Esta recorrência aproxima um núcleo trágico; não prova que uma palavra seja fácil para o leitor.\par',r'\blank[2mm]',r'{\bf Preferência por Ésquilo.} Pelo menos três ocorrências em duas outras peças atribuídas a Ésquilo, com frequência relativa quatro vezes maior que na amostra de Sófocles e Eurípides.\par',r'\blank[2mm]',r'{\bf Mais frequente fora da tragédia.} Pelo menos cinco ocorrências em um contexto comparado e frequência relativa quatro vezes maior que na amostra trágica. Indica distribuição lexical, não a origem ou o sentido da palavra nesta passagem.\par',r'\page',r'{\switchtobodyfont[18pt]\color[accent]{Corpus e limites}}\par',r'\blank[4mm]',r'{\bf O texto analisado}\par',r'\blank[2mm]',f"Das {len(tokens)} unidades gráficas do texto de Sidgwick, {sum(target.values())} receberam lema comum, {summary['nomes_proprios']} foram identificadas como nomes próprios e {summary['nao_classificados']} ficaram sem classificação. A cobertura de identificação é {pct(sum(target.values())+summary['nomes_proprios'],len(tokens))}"+r'\%.\par',r'\blank[2mm]',r'As formas foram confrontadas com o Perseus Treebank de Persas, baseado em outra edição. Exigimos uma análise lexical única na posição mais próxima, a no máximo três versos. Divergências, ambiguidades e fragmentos ficam fora dos denominadores. Crases e elisões seguem a segmentação gráfica e os lemas disponíveis no treebank.\par',r'\blank[3mm]',r'{\bf Amostra de comparação}\par',r'\blank[2mm]',r'Persas foi excluída da amostra de referência. Usamos seis outras peças atribuídas a Ésquilo (incluindo Prometeu acorrentado, de autoria discutida), cinco de Sófocles e Medeia, de Eurípides. A amostra de Eurípides é pequena e a comparação entre autores permanece provisória.\par',r'\blank[2mm]',r'Fora da tragédia: Ilíada e Odisseia; Acarnenses e Tesmoforiantes; o trecho anotado da Poliorcética de Eneias Tático; De automatis de Herão; trechos e obras de Longo, Luciano e o discurso 24 de Lísias. São amostras de extensão e época diferentes.\par',r'\blank[2mm]',r'As frequências são divididas pelo total de ocorrências comuns de cada corpus. Nos testes de preferência, acrescentamos 0,5 ao número de ocorrências para estabilizar razões quando há zeros. Não confundimos ausência na amostra com exclusividade ou criação de Ésquilo.\par',r'\blank[3mm]',r'Para as margens, adotamos um recorte editorial mais restrito: 175 lemas fundamentais (os primeiros 150 da lista de frequência DCC e 25 acréscimos). O sentido básico é dispensado; formas difíceis podem conservar análise gramatical. Esse recorte não equivale à categoria de 500 palavras da tabela.\par',r'\blank[2mm]',r'{\bf Fontes e reprodução}\par',r'\blank[2mm]',r'Dickinson College Commentaries: Greek Core Vocabulary (CC BY-SA 3.0). Perseus Dependency Treebank 2.1 (CC BY-SA 3.0 US). Pedalion Trees: Toon Van Hal, Alek Keersmaekers e colaboradores (CC BY-SA 4.0). Dados consultados em 10 de outubro de 2026.\par',r'\blank[2mm]',r'O projeto conserva a lista de lemas, as contagens por corpus, a classificação de cada unidade e o programa de cálculo. Este apêndice será atualizado depois da revisão filológica das análises e da ampliação dos corpora.\par']
(base/'estatisticas.tex').write_text('\n'.join(t)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in summary.items() if k not in ['corpus','lemas']},ensure_ascii=False,indent=2))
