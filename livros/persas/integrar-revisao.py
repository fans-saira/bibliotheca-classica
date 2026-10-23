"""Integrate the preserved Acrobat review and broaden the opening vocabulary."""
from pathlib import Path
import json,unicodedata
from convencoes import format_entry,entries
base=Path(__file__).resolve().parent
lexical_additions='''ἤδη|ἤδη|já
ἄγαν|ἄγαν|muito, excessivamente
ἔσωθεν|ἔσωθεν|por dentro
ἰσχύς|ἰσχύς/ἰσχύος|força
ἀφικνέομαι|ἀφικνέομαι|chegar
βαίνω|βαίνω|ir, avançar
πεζός|πεζός/πεζή/πεζόν|a pé
βάδην|βάδην|a passo
ἔφορος|ἔφορος/ἐφόρου|supervisor
ἱπποβάτης|ἱπποβάτης/ἱπποβάτου|cavaleiro
ἱππιοχάρμης|ἱππιοχάρμης/ἱππιοχάρμου|combatente a cavalo
ἐσθλός|ἐσθλός/ἐσθλή/ἐσθλόν|valoroso
πέμπω|πέμπω|enviar
ἑλειοβάτης|ἑλειοβάτης/ἑλειοβάτου|habitante dos pântanos
ἕπομαι|ἕπομαι|seguir
ὄχλος|ὄχλος/ὄχλου|multidão
ἐπίπαν|ἐπίπαν|inteiramente
ἠπειρογενής|ἠπειρογενής/ἠπειρογενές|nascido no continente
ἅρμα|ἅρμα/ἅρματος|carro de guerra
φύλαξ|φύλαξ/φύλακος|guardião
ἄναξ|ἄναξ/ἄνακτος|soberano
χώρα|χώρα/χώρας|terra, país
στρατιά|στρατιά/στρατιᾶς|exército
κακόμαντις|κακόμαντις/κακόμαντι|que pressente desgraças
θυμός|θυμός/θυμοῦ|ânimo, coração
πολεμέω|πολεμέω|guerrear
πόλεμος|πόλεμος/πολέμου|guerra
φοβερός|φοβερός/φοβερά/φοβερόν|terrível
δεινός|δεινός/δεινή/δεινόν|temível
δόξα|δόξα/δόξης|reputação
ψυχή|ψυχή/ψυχῆς|alma, coragem
ἐρέτης|ἐρέτης/ἐρέτου|remador
πλῆθος|πλῆθος/πλήθους|multidão
ἀνάριθμος|ἀνάριθμος/ἀνάριθμον|inumerável
ὄψις|ὄψις/ὄψεως|aspecto, visão
ἔθνος|ἔθνος/ἔθνους|povo
πομπή|πομπή/πομπῆς|escolta
ἄνθος|ἄνθος/ἄνθους|flor
χρόνος|χρόνος/χρόνου|tempo'''
p=base/'lexico-editorial.tsv'; text=p.read_text(encoding='utf-8')
existing={line.split('|')[0] for line in text.splitlines() if line and not line.startswith('#')}
for row in lexical_additions.splitlines():
 if row.split('|')[0] not in existing:text+=row+'\n'
p.write_text(text,encoding='utf-8')
# Load only the selector's definitions; do not replace reviewed annotations.
selector=base/'selecionar-notas.py'
ns={'__file__':str(selector)}
exec(compile(selector.read_text(encoding='utf-8').split('records =')[0],str(selector),'exec'),ns)
norm=ns['norm']; words=ns['words']; lexicon=ns['lexicon']; morphology=ns['morphology']
notes=json.loads((base/'notas.json').read_text(encoding='utf-8'))
candidates=json.loads((base/'notas-candidatas.json').read_text(encoding='utf-8'))
notes={n:format_entry(e) for n,e in notes.items()}
candidates={n:[format_entry(e) for e in es] for n,es in candidates.items()}
records=json.loads((base/'fontes/linhas-extraidas.json').read_text(encoding='utf-8'))
highlights=json.loads((base/'revisoes/highlights-extraidos.json').read_text(encoding='utf-8'))
requested={}; review=[]
for h in highlights:
 if h['action']!='incluir':raise ValueError('An exclusion requires matching to its original marginal entry.')
 word=h['text'].strip('.,:;')
 record=next(r for r in records if r['n']<=64 and word in r['text'].split() or r['n']<=64 and word in [t.strip('.,:;') for t in r['text'].split()])
 requested.setdefault(str(record['n']),set()).add(word)
 review.append({'page_commented':h['page'],'verse':record['n'],'word':word,'action':'incluir'})
for record in records:
 n=record['n']; key=str(n)
 for raw in record['text'].split():
  form=raw.strip('.,:;—†<>[]!?')
  if not form or form=='BREAKLINE' or form.endswith('-') or form[0].isupper():continue
  matches=[d for d in words.get(norm(form),[]) if abs(d['n']-n)<=20 and norm(d['lemma']) in lexicon and norm(d['lemma'])!=norm('ἵππος')]
  if not matches:continue
  d=min(matches,key=lambda d:abs(d['n']-n)); lemma,gloss=lexicon[norm(d['lemma'])]
  analysis='adv.' if d['postag'].startswith('d') else morphology(d,lemma)
  if not analysis:continue
  if form=='εἵλετο':analysis='aor., ind., méd., 3ª s.'
  if form=='σοῦνται':analysis='pres., ind., méd., 3ª p.'
  if form=='ἀφικνεῖται':analysis='pres., ind., méd., 3ª s.'
  if form=='ἕπεται':analysis='pres., ind., méd., 3ª s.'
  e=format_entry({'forma':form,'lema':lemma,'sentido':gloss,'analise':analysis,'verso_treebank':d['n'],'morfologia_fonte':d['postag']})
  if not any(x['forma']==form for x in candidates.get(key,[])):candidates.setdefault(key,[]).append(e)
# Epic nominative article, requested explicitly rather than a noun gloss.
candidates.setdefault('18',[]).append({'forma':'τοὶ','lema':'οἱ','sentido':'','analise':'art., nom. pl. masc.','tipo':'forma'})
seen_forms=set()
for n in sorted(candidates,key=int):
 opts=candidates.get(n,[])
 if not opts:continue
 unique={e['forma']:e for e in opts}
 for old in entries(notes[n]) if n in notes else []:unique[old['forma']]=old
 selected=[]
 for e in unique.values():
  shape=(e.get('lema_base',e['lema']),e['forma'],e['analise'],e.get('caso',''))
  if shape in seen_forms and e.get('tipo')!='crase' and e['forma'] not in requested.get(n,set()):continue
  seen_forms.add(shape)
  selected.append(e)
 if not selected:
  notes.pop(n,None)
  continue
 text=next(r['text'] for r in records if str(r['n'])==n)
 selected.sort(key=lambda e:text.index(e['forma']))
 for e in selected:
  if e['forma'] in requested.get(n,set()):e['highlight']=True
  if 'sentido_original' in e:e['sentido']=e.pop('sentido_original')
 note={'tipo':'grupo','forma':selected[0]['forma'],'entradas':selected} if len(selected)>1 else selected[0]
 note['reservar_espaco']=True
 note['obrigatoria']=True
 notes[n]=note
for n,forms in requested.items():
 assert forms<=set(e['forma'] for e in entries(notes[n])),(n,forms)
# Restore full glosses until the final selection determines the first appearance.
for note in notes.values():
 for e in entries(note):
  if 'sentido_original' in e:e['sentido']=e.pop('sentido_original')

for name,data in [('notas.json',notes),('notas-candidatas.json',candidates),('revisoes/highlights-integrados.json',review)]:
 (base/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(len(review),'highlights integrados;',sum(len(entries(e)) for n,e in notes.items() if int(n)<=64),'entradas nos primeiros 64 versos; apoio ampliado a toda a tragédia.')
