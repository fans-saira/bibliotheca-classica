"""Prepare editorial candidates from verified text forms and Perseus morphology.

The TSV supplies manually selected lemmas and Portuguese glosses. The treebank
is a different edition: match actual word forms, never replace reading text.
The final PDF geometry determines which candidates fit at their verse baseline.
"""
from pathlib import Path
import json, re, unicodedata, xml.etree.ElementTree as ET
from convencoes import format_entry

base = Path(__file__).resolve().parent
def norm(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s).lower()
                   if c.isalpha()).replace('ς', 'σ')

lexicon = {}
for row in (base/'lexico-editorial.tsv').read_text(encoding='utf-8').splitlines():
    if row and not row.startswith('#'):
        lemma, forms, gloss = row.split('|')
        lexicon[norm(lemma)] = (forms, gloss)

words = {}
for w in ET.parse(base/'fontes/persas-treebank.xml').iter('word'):
    if w.get('cite') and w.get('lemma'):
        d = dict(w.attrib)
        d['n'] = int(d['cite'].split(':')[-1])
        words.setdefault(norm(d['form']), []).append(d)

cases = {'n':'nom.', 'g':'gen.', 'd':'dat.', 'a':'ac.', 'v':'voc.'}
numbers = {'s':'sing.', 'p':'pl.', 'd':'dual'}
genders = {'m':'masc.', 'f':'fem.', 'n':'neut.'}
tenses = {'p':'pres.', 'i':'imperf.', 'a':'aor.', 'r':'perf.',
          'l':'mais-que-perf.', 'f':'fut.', 't':'fut. perf.'}
moods = {'i':'ind.', 's':'subj.', 'o':'opt.', 'm':'imper.'}
voices = {'a':'voz at.', 'm':'voz méd.', 'p':'voz pass.', 'e':'voz méd./pass.'}
overrides = {
    'εἵλετο': ('αἱρέω', 'escolher', 'v. aor., ind., voz méd., 3ª sing.'),
    'θώμεθα': ('τίθημι', 'pôr, considerar', 'v. aor., subj., voz méd., 1ª pl.'),
    'ἔταφον': ('τέθηπα', 'estar atônito', 'v. aor., ind., voz at., 3ª pl.'),
}

def morphology(d, forms):
    tag = d['postag']
    if len(tag) != 9:
        return None
    if tag[0]=='v':
        # A missing tense/mood/voice cannot yield an invented complete analysis.
        if tag[3] not in tenses or tag[4] not in 'isomnp' or tag[5] not in voices:
            return None
        voice = voices[tag[5]]
        if tag[5]=='e' and forms.endswith('ομαι'):
            voice = 'voz méd.'
        parts = [({'p':'part.', 'n':'inf.'}.get(tag[4], 'v.')), tenses[tag[3]]]
        if tag[4] in moods:
            parts.append(moods[tag[4]])
        parts.append(voice)
        if tag[4]=='p':
            if tag[7] not in cases or tag[2] not in numbers or tag[6] not in genders:
                return None
            parts += [cases[tag[7]], numbers[tag[2]], genders[tag[6]]]
        elif tag[4]!='n':
            if tag[1] not in '123' or tag[2] not in numbers:
                return None
            parts.append(tag[1]+'ª '+numbers[tag[2]])
    else:
        if tag[7] not in cases or tag[2] not in numbers or tag[6] not in genders:
            return None
        # Some adjectives are substantivized in the treebank's POS inventory.
        f = forms.split('/')
        adjective = tag[0]=='a' or len(f)==3 or (len(f)==2 and f[-1].endswith(('ον','ές')))
        parts = ['adj.' if adjective else 'subst.', cases[tag[7]], numbers[tag[2]], genders[tag[6]]]
        if tag[8]=='c': parts.insert(1,'compar.')
        if tag[8]=='s': parts.insert(1,'superl.')
    result = ', '.join(parts)
    return result if result.endswith('.') else result+'.'

records = json.loads((base/'fontes/linhas-extraidas.json').read_text(encoding='utf-8'))
candidates = {}
seen = {}
previous_text = ''
for record in records:
    n = record['n']
    options = []
    for index,raw in enumerate(record['text'].split()):
        form = raw.strip('.,:;—†<>[]!?')
        if form.endswith('-') or form=='BREAKLINE' or (index==0 and previous_text.endswith('-')):
            continue  # Do not gloss a partial word as if it were complete.
        if form[0].isupper():
            continue  # Proper names are not lexical glosses of homographs.
        matches = [d for d in words.get(norm(form),[]) if abs(d['n']-n)<=20
                   and norm(d['lemma']) in lexicon]
        if not matches:
            continue
        d = min(matches,key=lambda d: abs(d['n']-n))
        k = norm(d['lemma'])
        forms, gloss = lexicon[k]
        analysis = morphology(d,forms)
        if form in {'ἦρξεν','παιώνιος'}:
            continue
        if form=='ἄφθογγος' and n==206:
            analysis='adj., nom. sing. fem.'
        if form=='φρένας':
            analysis='subst., ac. pl. fem.'
        if form=='ταρφύς':
            analysis='adj., nom. pl. masc.'
        if form=='προσήμεναι':
            analysis='part., pres., voz méd., nom. pl. fem.'
        if form in overrides:
            forms,gloss,analysis = overrides[form]
        if not analysis:
            continue
        # Repeat distant lexical support, especially for a different inflection.
        previous = seen.get(k)
        if previous and (n-previous[0]<120 or previous[1]==analysis):
            continue
        options.append({'forma':form,'lema':forms,'sentido':gloss,
                        'analise':analysis,'morfologia_fonte':d['postag'],
                        'verso_treebank':d['n'],'chave':k})
    if options:
        candidates[str(n)] = options
        for option in options:
            seen[option['chave']] = (n,option['analise'])
    previous_text = record['text']

approved = {
 '1': {'forma':'οἰχομένων','lema':'οἴχομαι','sentido':'partir','analise':'part., pres., voz méd., gen. pl. masc.'},
 '8': {'forma':'νόστῳ','lema':'νόστος/νόστου','sentido':'retorno','analise':'subst., dat. sing. masc.'},
 '26': {'forma':'ἠδ᾽','lema':'ἠδέ','sentido':'e','analise':'conj.'},
}
for n,entry in approved.items():
    candidates[n] = [entry]
adjustments = json.loads((base/'ajustes-notas.json').read_text(encoding='utf-8'))
for n,fields in adjustments.items():
    if n in candidates:
        target=next((e for e in candidates[n] if n=='209' and e['forma']=='δέμας'),candidates[n][0])
        target.update(fields)
crases=json.loads((base/'crases.json').read_text(encoding='utf-8'))
for record in records:
    for token in record['text'].split():
        word=token.strip('.,:;—†<>[]!?')
        if word in crases:
            candidates.setdefault(str(record['n']),[]).insert(0,{
                'forma':word,'lema':crases[word],'sentido':'','analise':'','tipo':'crase',
                **({'quebra':True} if record['n']==780 else {})})
candidates={n:[format_entry(e) for e in options] for n,options in candidates.items()}
prepositions=json.loads((base/'preposicoes.json').read_text(encoding='utf-8'))
for n,(form,case,meaning,position) in prepositions.items():
    candidates.setdefault(n,[]).append({'forma':form,'lema':form,'sentido':meaning,
        'analise':'','tipo':'preposicao','caso':case,'posicao':position})
(base/'notas-candidatas.json').write_text(json.dumps(candidates,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# First pass measures the most compact candidate for each available verse.
notes = {n:next((e for e in opts if e.get('tipo')=='crase'),
               min(opts,key=lambda x:sum(len(x[f]) for f in ('forma','lema','sentido','analise'))))
         for n,opts in sorted(candidates.items(),key=lambda x:int(x[0]))}
for n,entry in approved.items():notes[n]=format_entry(entry)
(base/'notas.json').write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'{len(lexicon)} lemas selecionados; {sum(map(len,candidates.values()))} candidatos; {len(notes)} versos com candidato.')
