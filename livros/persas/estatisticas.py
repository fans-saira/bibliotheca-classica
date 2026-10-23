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
# These frequency-based classes are diagnostics, not the revised editorial taxonomy.
summary['publication_status']='Retirado da edição; análise histórica de frequência, não classificação editorial validada.'
(out/'estatisticas-lexicais.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(base/'estatisticas.tex').write_text('% Apêndice retirado: classificação lexical em revisão.\n',encoding='utf-8')
print('Dados diagnósticos atualizados; apêndice não publicado. Consulte fontes/criterios-classificacao-lexical.json.')
