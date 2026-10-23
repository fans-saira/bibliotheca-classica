"""Retain inflectional support without repeating a previously printed gloss."""
from pathlib import Path
import json
from convencoes import entries

base=Path(__file__).resolve().parent
path=base/'notas.json'
notes=json.loads(path.read_text(encoding='utf-8'))
seen=set(); final={}; removed=[]; abbreviated=[]
for n,original in sorted(notes.items(),key=lambda x:int(x[0])):
    kept=[]
    for item in entries(original):
        e=dict(item)
        gloss=e.get('sentido_original',e.get('sentido',''))
        lemma=e.get('lema_base',e['lema']).split('/')[0].split(',')[0].strip()
        if e.get('tipo')=='crase':
            kept.append(e)
            continue
        key=(lemma,gloss,e.get('caso',''))
        if key in seen and gloss:
            simple_case=e.get('analise','').replace(',','').replace(' ','') in ('nom.sing.','ac.sing.','dat.sing.','gen.sing.')
            if e.get('tipo')=='nome' and simple_case and not e.get('revisao_felipe') and not e.get('explicacao_contextual'):
                removed.append({'verse':int(n),'form':e['forma'],'reason':'repetição nominal sem dificuldade nova'})
                continue
            if (e.get('tipo')=='preposicao' or e.get('analise','') in ('adv.','conj.','prep.')) and not e.get('highlight'):
                removed.append({'verse':int(n),'form':e['forma']})
                continue
            e['sentido_original']=gloss
            e['sentido']=''
            abbreviated.append({'verse':int(n),'form':e['forma']})
        else:
            e['sentido']=gloss
            e.pop('sentido_original',None)
            seen.add(key)
        kept.append(e)
    if kept:
        if len(kept)>1:
            final[n]={**original,'tipo':'grupo','forma':kept[0]['forma'],'entradas':kept}
        else:
            final[n]={**kept[0],**{k:original[k] for k in ('reservar_espaco','obrigatoria') if k in original}}
path.write_text(json.dumps(final,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(base/'fontes/repeticoes.json').write_text(json.dumps({
    'glosses_omitted':abbreviated,'redundant_entries_removed':removed,
    'criterion':'same dictionary lemma and meaning; prepositions also distinguished by case'
},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'{sum(len(entries(e)) for e in final.values())} entradas; {len(abbreviated)} sentidos repetidos omitidos; {len(removed)} entradas redundantes retiradas.')
