"""Build an auditable work-level index from the archived Diorisis 1.51 corpus."""
from pathlib import Path
from collections import Counter
import json,zipfile,re,unicodedata as U,csv,hashlib,time,argparse
base=Path(__file__).resolve().parent
out=base/'fontes/estudo-lexical'
letters=dict(zip('abgdezhqiklmncoprstufxyw','αβγδεζηθικλμνξοπρστυφχψω'))
marks={')':'\u0313','(':'\u0314','/':'\u0301','\\':'\u0301','=':'\u0342','+':'\u0308','|':'\u0345'}
def greek(s):
    s=re.sub(r'\d+$','',s.replace('*',''))
    # Beta breathing marks may precede the first letter of capitalized forms.
    s=re.sub(r'^([)(/=+|]+)([a-z])',r'\2\1',s)
    r=''
    for c in s:
        r+=letters.get(c,marks.get(c,c))
    r=U.normalize('NFC',r)
    r=r[:-1]+'ς' if r.endswith('σ') else r
    return r
catalog=list(csv.DictReader((out/'catalog.tsv').open(encoding='utf-8'),delimiter='\t'))
meta={(x['tlgAuthor'],x['tlgId']):x for x in catalog}
bytitle={(x['author'],x['title']):x for x in catalog}
parser=argparse.ArgumentParser()
parser.add_argument('--archive',default='C:/Users/logop/AppData/Local/Temp/DiorisisCorpus1.51.zip')
parser.add_argument('--updates',default='C:/Users/logop/AppData/Local/Temp/persas-diorisis-atualizado')
args=parser.parse_args()
updates=Path(args.updates)
archive=Path(args.archive)
works=[];start=time.time()
with zipfile.ZipFile(archive) as z:
    names=[n for n in z.namelist() if n.endswith('.json')]
    for i,n in enumerate(names):
        ids=re.search(r'\((\d{4})\).*\((\d{3})\)',n)
        if not ids:continue
        titlematch=re.match(r'(.+?) \((\d{4})\) - (.+) \((\d{3})\).json',n)
        m=bytitle.get((titlematch[1],titlematch[3])) if titlematch else meta.get(ids.groups())
        if not m:continue
        data=json.loads((updates/n).read_bytes() if (updates/n).exists() else z.read(n));c=Counter();ambiguous=0;proper=0
        for s in data['sentences']:
            for t in s['tokens']:
                if t['type']!='word':continue
                e=t.get('lemma')
                if not isinstance(e,dict) or not e.get('entry'):ambiguous+=1;continue
                if e.get('POS')=='proper':proper+=1;continue
                l=greek(e['entry'])
                if not any(x in letters.values() for x in l):continue
                c[l]+=1
        works.append(dict(m,file=n,version=data.get('version'),total=sum(c.values()),ambiguous_tokens=ambiguous,proper_tokens=proper,counts=dict(c)))
        if i%100==0:print('Indexed',i,'/',len(names),'elapsed',round(time.time()-start),flush=True)
(out/'diorisis-index.json').write_text(json.dumps(works,ensure_ascii=False),encoding='utf-8')
(out/'diorisis-archive-sha256.json').write_text(json.dumps({'source':'https://ndownloader.figshare.com/files/27831960','bytes':archive.stat().st_size,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'indexed_works':len(works)},indent=2),encoding='utf-8')
print('Done',len(works),sum(w['total'] for w in works),flush=True)
