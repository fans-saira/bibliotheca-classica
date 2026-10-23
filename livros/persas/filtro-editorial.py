"""Editorial exclusions and merged entries requested in the PDF review."""
from pathlib import Path
import json,unicodedata as U
from convencoes import entries,format_entry
base=Path(__file__).resolve().parent
def head(s):return U.normalize('NFC',s.split('/')[0].split(',')[0].strip())
policy=json.loads((base/'vocabulario-fundamental.json').read_text(encoding='utf-8'))
basic={x['lema'] for x in policy['lemas']}
basic.update({'φοβερός','ὄψις','ἔθνος','ἄνθος','λαός','φρήν','φόβος','πέπλος','ἄνασσα','γεραιός'})
aliases={'πιστόν':'πιστός','εἶδον':'ὁράω','ἐς':'εἰς'}
def apply(bank):
    final={};excluded=[];grammar=[]
    for n,g in bank.items():
        kept=[]
        for raw in entries(g):
            e=format_entry(raw)
            if e.get('sentido_original'):e['sentido']=e['sentido_original']
            e.pop('reservar_espaco',None);e.pop('obrigatoria',None)
            # Previous forced breaks belonged to the narrow 48 mm column.
            e.pop('quebra',None)
            if e.get('tipo')=='preposicao' and e.get('posicao')=='preposta' and (e['forma'],e['sentido']) in {('ἐν','em'),('ἄνευ','sem'),('ἀφ᾽','desde'),('ἐξ','a partir de')}:
                excluded.append({'verse':int(n),'forma':e['forma'],'lema':e['lema'],'motivo':'sentido elementar da preposição'});continue
            if e['forma'] in ('κατέφθιτο','μακαρίτας'):e['quebra']=True
            l=head(e.get('lema_base',e['lema']));l=aliases.get(l,l)
            if l in basic and not e.get('revisao_felipe') and not e.get('explicacao_contextual') and e.get('tipo') not in ('crase','preposicao','forma'):
                a=e.get('analise','');tag=e.get('morfologia_fonte','')
                verb=tag.startswith('v') or any(s in a for s in ['pres.','aor.','imperf.','perf.','fut.','part.','inf.'])
                difficult=(verb and not ('pres.' in a and 'ind.' in a and 'at.' in a)) or 'compar.' in a or 'superl.' in a
                if difficult:
                    e['sentido']='';e.pop('sentido_original',None);e['apoio_apenas_morfologico']=True
                    grammar.append({'verse':int(n),'forma':e['forma'],'lema':l})
                else:
                    excluded.append({'verse':int(n),'forma':e['forma'],'lema':l,'motivo':'vocabulário fundamental'});continue
            if n=='19' and e['forma']=='ἐπὶ' and e.get('tipo')=='preposicao':
                excluded.append({'verse':19,'forma':'ἐπὶ','lema':'ἐπί','motivo':'unificada com ἐφ᾽ no verso 18'});continue
            if n=='18' and e['forma']=='ἐφ᾽' and e.get('tipo')=='preposicao':
                e.update(lema='ἐπί',sentido='sobre, a bordo de',exibir_lema=True,abrange_versos=[18,19],prioridade_editorial=True)
            kept.append(e)
        if kept:final[n]=kept[0] if len(kept)==1 else {'tipo':'grupo','forma':kept[0]['forma'],'entradas':kept}
    (base/'fontes/filtro-editorial.json').write_text(json.dumps({'fundamental_lemmas':len(basic),'excluded_entries':excluded,'morphology_only':grammar,'criterion':policy['criterio']},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return final
