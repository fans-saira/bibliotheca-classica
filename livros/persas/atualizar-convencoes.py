"""Apply the latest conventions without discarding the current selection."""
from pathlib import Path
import csv,json
from convencoes import format_entry

base=Path(__file__).resolve().parent
def read(name):return json.loads((base/name).read_text(encoding='utf-8'))
def save(name,data):
    (base/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

notes=read('notas.json')
candidates=read('notas-candidatas.json')
# A former verse-level override had attached the noun analysis of δέμας to
# an alternative verb at the same verse. Preserve the proper alternative.
for entry in candidates.get('209',[]):
    if entry['lema']=='τίλλω':
        entry['analise']='part., pres., at., ac. sing. masc.'
        entry['sentido']='arrancar'
notes={n:format_entry(e) for n,e in notes.items()}
candidates={n:[format_entry(e) for e in options] for n,options in candidates.items()}
crases=read('crases.json')
crasis_verses=[]
for record in read('fontes/linhas-extraidas.json'):
    for token in record['text'].split():
        word=token.strip('.,:;—†<>[]!?')
        if word not in crases:continue
        key=str(record['n'])
        entry={'forma':word,'lema':crases[word],'sentido':'','analise':'','tipo':'crase'}
        if record['n']==780:entry['quebra']=True
        if not any(e.get('tipo')=='crase' and e['forma']==word for e in candidates.get(key,[])):
            candidates.setdefault(key,[]).append(entry)
        notes[key]=entry
        crasis_verses.append(record['n'])
notes=dict(sorted(notes.items(),key=lambda x:int(x[0])))
for n,(word,case,meaning,position) in read('preposicoes.json').items():
    entry={'forma':word,'lema':word,'sentido':meaning,'analise':'',
           'tipo':'preposicao','caso':case,'posicao':position}
    if not any(e.get('tipo')=='preposicao' and e['forma']==word for e in candidates.get(n,[])):
        candidates.setdefault(n,[]).append(entry)
    if n not in {'1','8','26'} and notes.get(n,{}).get('tipo')!='crase':notes[n]=entry
notes=dict(sorted(notes.items(),key=lambda x:int(x[0])))
save('notas.json',notes);save('notas-candidatas.json',candidates)
save('fontes/crases-selecionadas.json',sorted(set(crasis_verses)))
print(f'{len(notes)} entradas antes de acomodar; {len(crasis_verses)} ocorrências de crase desdobradas.')
