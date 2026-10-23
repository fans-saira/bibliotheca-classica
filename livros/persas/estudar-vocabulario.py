"""Hierarchical lexical screening; preserves evidence and does not equate absence with uniqueness."""
from pathlib import Path
import json,csv,re,unicodedata as U,collections,xml.etree.ElementTree as ET
base=Path(__file__).resolve().parent;b=base/'fontes/estudo-lexical'
def norm(x):return U.normalize('NFC',x).replace('ϲ','σ')
alias={'πιστόν':'πιστός','εἶδον':'ὁράω','εἶπον':'λέγω','ἐς':'εἰς','οὕτω':'οὕτως','ἠέ':'ἤ','πέρ':'περ','ποτέ':'ποτε','πού':'που','πάτηρ':'πατήρ','στρατία':'στρατιά','ἔπειμι':'ἔπειμι','προσεῖδον':'προσοράω','εἰσεῖδον':'εἰσοράω'}
alias.update({'κτέομαι':'κτάομαι','κεῖνος':'ἐκεῖνος'})
def canon(x):return alias.get(norm(x),norm(x))
rows=list(csv.DictReader((b/'tokens-conferidos.csv').open(encoding='utf-8-sig')));target=collections.Counter(canon(r['lema']) for r in rows if r['estado']=='analisado')
core_major={canon(r['lema']) for r in json.loads((b/'major-core.json').read_text(encoding='utf-8'))}
core_dcc={canon(re.split('[ ,;]',r['headword'])[0]) for r in json.loads((base/'fontes/dcc-core.json').read_text(encoding='utf-8'))['rows'] if r['rank']<=500}
logeion=json.loads((b/'logeion-frequency.json').read_text(encoding='utf-8'))
core_logeion={canon(r['lema']) for r in logeion if r['rank']<=1000}
core=core_major|core_dcc|core_logeion
works=json.loads((b/'diorisis-index.json').read_text(encoding='utf-8'))
# Add manually annotated Medea, absent from this release of Diorisis.
c=collections.Counter(canon(w.get('lemma','')) for w in ET.parse(base/'fontes/corpus-comparativo/pedalion-euripides_medea.xml').iter('word') if w.get('lemma') and not w.get('postag','').startswith('u') and not w.get('lemma')[0].isupper())
works.append({'author':'Euripides','title':'Medea','genre':'Tragedy','date':'-431','total':sum(c.values()),'counts':dict(c),'file':'pedalion-euripides_medea.xml'})
for w in works:
 c=collections.Counter()
 for l,n in w['counts'].items():c[canon(l)]+=n
 w['counts']=c
trag=[w for w in works if w['author'] in ['Aeschylus','Sophocles','Euripides'] and w['title'] not in ['Persians','Prometheus Bound','Rhesus','Ichneutae']]
other=[w for w in works if w['author'] not in ['Aeschylus','Sophocles','Euripides'] and w['date'].lstrip('-').isdigit() and int(w['date'])<=-300]
early=[w for w in works if w['author'] in ['Homer','Hesiod']]
tragcount=collections.Counter();othercount=collections.Counter();earlycount=collections.Counter();latecount=collections.Counter()
for w in trag:tragcount.update(w['counts'])
for w in other:othercount.update(w['counts'])
for w in early:earlycount.update(w['counts'])
for w in works:
 if w['author']!='Aeschylus':latecount.update(w['counts'])
nt=sum(tragcount.values());no=sum(othercount.values())
lsj=json.loads((b/'lsj-target.json').read_text(encoding='utf-8'))
for k,v in list(lsj.items()):lsj.setdefault(canon(k),v)
archaic=r'(?<![A-Za-z.])(?:Il|Od|Hes|Archil|Alcm|Sapph|Alc|Tyrt|Mimn|Sol|Hippon|Stesich|Anacr|Xenoph|Heraclit)\.'
# Verified pre-456 odes, excluding uncertain dates and posthumous chronological cases.
pindar_o={1,2,3,6,7,8,9,10,11,12,13};pindar_p={1,4,5,6,7,9,10,12}
def earlyrefs(text):
 refs=re.findall(archaic,text)
 for book,n in re.findall(r'Pi\.([OP])\.(\d+)',text):
  if int(n) in (pindar_o if book=='O' else pindar_p):refs.append('Pi.'+book+'.'+n)
 return sorted(set(refs))
detail=[]
for l,n in sorted(target.items()):
 entries=lsj.get(l,{}).get('entries',[]);text=' '.join(e['definition'] for e in entries)
 plays=[w for w in trag if w['counts'][l]];authors={w['author'] for w in plays}
 density=(tragcount[l]/nt)/(othercount[l]/no) if othercount[l] else (999 if tragcount[l] else 0)
 er=earlyrefs(text)
 refs=set(re.findall(r'\b([A-Z][a-z]*)(?:\.[A-Z][a-z]*)*\.\d',text))
 foreign=refs-{'A','Id','EM','Hsch','Suid','Et','Sch'}
 # A short headword supported only by Aeschylus in LSJ and no independent corpus occurrence.
 exclusive=(bool(re.search(r'\bA\.(?:Pers|Ag|Ch|Eu|Supp|Th|Fr)\.',text)) and not foreign and not latecount[l] and not re.search(r'\b(?:Hom|Trag|Poet|Ep|Lyr)\.',text) and len(text)<700)
 typical=len(plays)>=3 and len(authors)>=2 and (density>=2 or bool(re.search(r'(?:only|chiefly|mostly|esp\.).{0,35}Trag|Trag.{0,40}(?:word|only|chiefly)',text)))
 if all(canon(k) in core for k in l.split('+')):category='1_basico';reason='repertório pedagógico Major/DCC'
 elif typical:category='2_tragedia';reason='recorrência entre autores trágicos e concentração no gênero'
 elif exclusive:category='3_esquilo_candidato';reason='LSJ cita apenas Ésquilo; sem ocorrência independente no corpus'
 elif er and bool(re.search(r'\b(?:Ep|Hom|Poet|Lyr)\.|poet\.|poetical',text)):category='4_outros_candidato';reason='marca épica/poética no LSJ e atestação arcaica datável; sentido exige conferência'
 else:category='5_pendente';reason='evidência insuficiente para as quatro classes'
 detail.append({'lema':l,'ocorrencias':n,'classe':category,'razao':reason,'tragedias':[(w['author'],w['title'],w['counts'][l]) for w in plays],'autores_tragicos':sorted(authors),'razao_densidade':round(density,3),'ocorrencias_anteriores_epica':earlycount[l],'referencias_anteriores_lsj':er,'ocorrencias_outros_autores':latecount[l],'lsj_autores_citados':sorted(refs),'lsj':entries})
(b/'triagem-lexical.json').write_text(json.dumps({'total_occurrences':sum(target.values()),'total_lemmas':len(target),'core_major':len(core_major),'core_dcc':len(core_dcc),'core_union':len(core),'tragedies':[(w['author'],w['title']) for w in trag],'detail':detail},ensure_ascii=False,indent=2),encoding='utf-8')
if __name__=='__main__':
 print('base',sum(target.values()),len(target),'core',len(core),'trag',len(trag))
 for k in sorted({r['classe'] for r in detail}):
  ds=[r for r in detail if r['classe']==k];print(k,len(ds),sum(r['ocorrencias'] for r in ds))
