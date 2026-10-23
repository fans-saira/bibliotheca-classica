from pathlib import Path
from urllib.request import urlopen
import concurrent.futures,xml.etree.ElementTree as ET,json
b=Path(__file__).resolve().parent/'fontes/corpus-comparativo';b.mkdir(exist_ok=True)
works=[('0085',i) for i in range(1,8)]+[('0011',i) for i in range(1,8)]+[('0006',i) for i in list(range(2,20))+list(range(40,53))]
works += [('0012',1),('0012',2),('0016',1),('0003',1),('0032',1),('0032',2),('0059',2),('0059',30),('0627',3),('0627',6),('0627',9)]
def get(work):
 author,number=work
 for v in [1,2]:
  name=f'tlg{author}.tlg{number:03d}.perseus-grc{v}.tb.xml';p=b/name
  try:
   if not p.exists():p.write_bytes(urlopen('https://raw.githubusercontent.com/PerseusDL/treebank_data/master/v2.1/Greek/texts/'+name,timeout=8).read())
   r=ET.parse(p).getroot();words=[w for w in r.iter('word') if w.get('lemma') and w.get('form') and not w.get('postag','').startswith('u')]
   return {'author':author,'work':number,'name':name,'tokens':len(words),'source':'https://raw.githubusercontent.com/PerseusDL/treebank_data/master/v2.1/Greek/texts/'+name}
  except Exception:pass
 return None
out=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
 for item in pool.map(get,works):
  if item:out.append(item);print(item['name'],item['tokens'],flush=True)
(b/'manifest.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print('TOTAL',len(out),flush=True)
