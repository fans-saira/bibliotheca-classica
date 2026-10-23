"""Fit marginal entries to fixed verse baselines; never change Greek spacing."""
from pathlib import Path
from itertools import combinations
import json,re,sys,bisect,unicodedata as U
import pdfplumber
import importlib.util
from convencoes import entries,format_entry
base=Path(__file__).resolve().parent
bank=json.loads((base/'revisoes/notas-rodada-felipe-2026-10-11.json').read_text(encoding='utf-8'))
original_count=sum(len(entries(g)) for g in bank.values())
spec=importlib.util.spec_from_file_location('filtro_editorial',base/'filtro-editorial.py')
filter_module=importlib.util.module_from_spec(spec);spec.loader.exec_module(filter_module)
bank=filter_module.apply(bank)
records=json.loads((base/'fontes/linhas-extraidas.json').read_text(encoding='utf-8'))
def norm(s):return ''.join(c for c in U.normalize('NFD',s).lower() if c.isalpha()).replace('ς','σ')
highlight_names={(h['verse'],norm(h['word'])):h['word'] for h in json.loads((base/'revisoes/highlights-integrados.json').read_text(encoding='utf-8'))}
highlights=set(highlight_names)
def tex(s):
    for a,b in [('&',r'\&'),('%',r'\%'),('#',r'\#'),('_',r'\_')]:s=s.replace(a,b)
    return s
def render(e):
    macro=r'\notagramaticalquebrada' if e.get('quebra') else r'\notagramatical';fields=('forma','lema','sentido','analise')
    if e.get('tipo')=='crase':macro=r'\desdobramentoquebrado' if e.get('quebra') else r'\desdobramento';fields=('forma','lema')
    elif e.get('tipo')=='preposicao':macro=r'\preposicao'+e['posicao'];fields=('forma','caso','sentido')
    if e.get('tipo')=='preposicao' and e.get('exibir_lema'):
        macro=r'\preposicaolema'+e['posicao'];fields=('forma','lema','caso','sentido')
    return macro+''.join('{'+(tex(e[k]).replace('/',r'/\allowbreak ') if k=='lema' else tex(e.get('forma_exibida',e[k]) if k=='forma' else e[k]))+'}' for k in fields)
options=[]
for key,g in bank.items():
    es=entries(g)
    for e in es:
        e.pop('reservar_espaco',None);e.pop('obrigatoria',None)
        if e.get('sentido_original'):e['sentido']=e['sentido_original']
        format_entry(e)
    for size in range(1,len(es)+1):
        for indices in combinations(range(len(es)),size):
            subset=[es[i] for i in indices];mask=sum(1<<i for i in indices);n=int(key)
            score=sum(100+(1000000 if (n,norm(e['forma'])) in highlights else 0)
                      +(100000 if n in (1,8,26) else 0)+(10000 if e.get('tipo')=='crase' else 0)
                      +(2000000 if e.get('prioridade_editorial') else 0)
                      +(30000000 if e.get('gramatica_obrigatoria') else 0) for e in subset)
            options.append({'id':100000+len(options),'verse':n,'indices':list(indices),'score':score,'entries':subset})
if sys.argv[1]=='prepare':
    lines=[r'\medirnota{'+str(o['id'])+'}{'+r'\crlf '.join(render(e) for e in o['entries'])+'}' for o in options]
    lines += [r'\setbox\scratchbox\hbox{'+tex(r['text'].replace('BREAKLINE',' '))+r'}\writestatus{VERSEWIDTH}{'+str(r['n'])+r':\the\wd\scratchbox}' for r in records]
    (base/'medicoes-notas.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    (base/'notas.json').write_text('{}\n',encoding='utf-8')
    print(f'{len(options)} combinações de notas para medir.')
    sys.exit()
build=Path(sys.argv[2]);mm=72/25.4
height_log=Path(sys.argv[3]) if len(sys.argv)>3 else build/'persas.log'
heights={int(n):float(h)*72/72.27 for n,h in re.findall(r'NOTEHEIGHT\s+> (\d+):([\d.]+)pt',height_log.read_text(encoding='utf-8'))}
def compact(s):return re.sub(r'\s+','',U.normalize('NFC',s))
positions={};cursor=0
with pdfplumber.open(build/'persas.pdf') as pdf:
    for pn,page in enumerate(pdf.pages,1):
        left=25 if pn%2 else 73
        # Grid values are read from the layout configuration below.
        grid=json.loads((base/'fontes/grid-atual.json').read_text(encoding='utf-8'))
        left=grid['inner_mm'] if pn%2 else grid['outer_mm']+grid['notes_mm']+grid['gap_mm']
        crop=page.crop((left*mm,32*mm,(left+grid['main_mm'])*mm,264*mm)).filter(lambda c:c.get('object_type')!='char' or 13.8<c['size']<14.1)
        chars=[c for line in crop.extract_text_lines(x_tolerance=1,y_tolerance=2) for c in line['chars'] if not c['text'].isspace()]
        text=compact(''.join(c['text'] for c in chars));local=0
        while cursor<len(records):
            r=records[cursor];needle=compact(r['text'].replace('BREAKLINE',''));at=text.find(needle,local)
            if at<0:break
            positions[r['n']]={'page':pn,'top':chars[at]['top'],'baseline':page.height-chars[at]['matrix'][5]}
            assert len({round(c['matrix'][5],2) for c in chars[at:at+len(needle)]})==1,('Verso quebrado',r['n'])
            local=at+len(needle);cursor+=1
assert cursor==len(records),(cursor,len(records))
chosen=[]
for page in sorted({p['page'] for p in positions.values()}):
    jobs=[]
    for o in options:
        p=positions[o['verse']]
        if p['page']!=page:continue
        start=p['top']+2.3;end=start+heights[o['id']]
        # Leave clearance above the footer even for a multi-entry note on the
        # last line of a densely composed page.
        if end<=253*mm:jobs.append((end+4,start,o['id'],o['score']))
    jobs.sort();ends=[j[0] for j in jobs];scores=[0];choices=[[]]
    for i,(end,start,oid,weight) in enumerate(jobs):
        prev=bisect.bisect_right(ends,start,0,i);take=scores[prev]+weight
        if take>scores[-1]:scores.append(take);choices.append(choices[prev]+[oid])
        else:scores.append(scores[-1]);choices.append(choices[-1])
    chosen.extend(choices[-1])
byid={o['id']:o for o in options};final={};selected=set()
for oid in chosen:
    o=byid[oid];es=o['entries'];n=o['verse']
    final[str(n)]=es[0] if len(es)==1 else {'tipo':'grupo','forma':es[0]['forma'],'entradas':es}
    selected.update((n,i) for i in o['indices'])
pending={}
for key,g in bank.items():
    es=[e for i,e in enumerate(entries(g)) if (int(key),i) not in selected]
    if es:pending[key]=es
missing=[{'verse':n,'word':highlight_names[n,word]} for n,word in sorted(highlights) if not any(norm(e['forma'])==word for e in entries(final.get(str(n),{'forma':''})))]
(base/'notas.json').write_text(json.dumps(dict(sorted(final.items(),key=lambda x:int(x[0]))),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(base/'notas-em-reserva.json').write_text(json.dumps(pending,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
report={'candidate_entries':sum(len(entries(g)) for g in bank.values()),'selected_blocks':len(final),'selected_entries':len(selected),'reserve_entries':sum(len(es) for es in pending.values()),'highlighted_forms_selected':len(highlights)-len(missing),'highlighted_forms_in_reserve':missing,'font_pt':14,'leading_pt':grid['leading_pt'],'minimum_gap_pt':4,'criterion':'Weighted interval selection at fixed Greek baselines; marked forms, approved examples and crases prioritized; no added vertical space or verse wrapping.'}
report.update(original_bank_entries=original_count,editorially_excluded_entries=original_count-report['candidate_entries'])
audit=json.loads((base/'fontes/filtro-editorial.json').read_text(encoding='utf-8'))
excluded={(x['verse'],norm(x['forma'])) for x in audit['excluded_entries']}
report['highlighted_forms_editorially_excluded']=[x for x in missing if (x['verse'],norm(x['word'])) in excluded]
report['highlighted_forms_in_reserve']=[x for x in missing if (x['verse'],norm(x['word'])) not in excluded]
(base/'fontes/selecao-margens.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
