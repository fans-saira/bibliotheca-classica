"""Maximum-count non-overlapping marginal selection at fixed verse baselines."""
from pathlib import Path
import bisect, json, re, sys, unicodedata
import pdfplumber

base = Path(__file__).resolve().parent
build = Path(sys.argv[1])
notes = json.loads((base/'notas.json').read_text(encoding='utf-8'))
records = json.loads((base/'fontes/linhas-extraidas.json').read_text(encoding='utf-8'))
def compact(s):
    return re.sub(r'\s+', '', unicodedata.normalize('NFC',s))

heights = {int(n):float(h)*72/72.27 for n,h in re.findall(
    r'NOTEHEIGHT\s+> (\d+):([\d.]+)pt', (build/'persas.log').read_text(encoding='utf-8'))}
positions = {}
cursor = 0
with pdfplumber.open(build/'persas.pdf') as pdf:
    for page_no,page in enumerate(pdf.pages,1):
        left = 25 if page_no%2 else 73
        crop = page.crop((left*72/25.4,32*72/25.4,(left+112)*72/25.4,264*72/25.4)).filter(
            lambda obj: obj.get('object_type')!='char' or 13.8<obj['size']<14.1)
        chars = [c for line in crop.extract_text_lines(x_tolerance=1,y_tolerance=2)
                 for c in line['chars'] if not c['text'].isspace()]
        text = compact(''.join(c['text'] for c in chars))
        local = 0
        while cursor<len(records):
            record=records[cursor]
            needle=compact(record['text'].replace('BREAKLINE',''))
            at=text.find(needle,local)
            if at<0: break
            positions[record['n']]={'page':page_no,'top':chars[at]['top'],
                                    'baseline':page.height-chars[at]['matrix'][5]}
            local=at+len(needle)
            cursor+=1
assert cursor==len(records), (cursor,len(records))
(base/'fontes/posicoes-versos.json').write_text(json.dumps(positions,indent=2)+'\n',encoding='utf-8')

selected=[]
for page_no in sorted({p['page'] for p in positions.values()}):
    jobs=[]
    mandatory={1,8,26}
    for key,entry in notes.items():
        n=int(key); p=positions[n]
        if p['page']!=page_no:continue
        start=p['top']+2.3
        end=start+heights[n]
        if end>264*72/25.4:continue
        # Extra four points preserve readable separation between entries.
        jobs.append((end+4,start,n,10000+(1000000 if n in mandatory or entry.get('tipo')=='crase' or entry.get('obrigatoria') else 0)))
    jobs.sort()
    ends=[j[0] for j in jobs]
    scores=[0];choices=[[]]
    for i,(end,start,n,weight) in enumerate(jobs):
        previous=bisect.bisect_right(ends,start,0,i)
        take=scores[previous]+weight
        if take>scores[-1]:
            scores.append(take);choices.append(choices[previous]+[n])
        else:
            scores.append(scores[-1]);choices.append(choices[-1])
    selected.extend(choices[-1])

final={str(n):notes[str(n)] for n in sorted(selected)}
assert all(int(n) in selected for n,e in notes.items() if e.get('tipo')=='crase'), 'Required crasis lost'
assert all(int(n) in selected for n,e in notes.items() if e.get('obrigatoria')), 'Highlighted word lost'
(base/'notas.json').write_text(json.dumps(final,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
report={'candidate_verses':len(notes),'selected_entries':len(final),
        'reserved_verses':sorted(set(map(int,notes))-set(selected)),
        'minimum_gap_pt':4,'criterion':'maximum count per page at fixed source verse baseline'}
(base/'fontes/selecao-margens.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'{len(final)} entradas acomodadas; {len(notes)-len(final)} versos candidatos reservados.')
