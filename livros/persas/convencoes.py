"""Editorial display conventions, shared by selection and regeneration."""
import re
import unicodedata

def plain(s):
    return ''.join(c for c in unicodedata.normalize('NFD',s) if not unicodedata.combining(c))

def genitive_display(nominative, genitive):
    """Shorten regular endings; retain the full form for a changed stem."""
    nom,gen=plain(nominative),plain(genitive)
    if nom.endswith('μα'):return genitive
    if nom.endswith('ας') and gen.endswith(('αντος','ατος')):return genitive
    for ending in ('ον','ος','ης','ας','η','α'):
        if nom.endswith(ending):
            if ending in ('η','α','ης','ας') and not gen.endswith(('ης','ας','ου')):continue
            stem=nom[:-len(ending)]
            if gen.startswith(stem):
                # Third-declension neuters in -ας do not share the stem here.
                return '-'+genitive[len(stem):]
    if genitive.startswith(nominative) and not nom.endswith('μα'):
        return '-'+genitive[len(nom):]
    for ending,replacement in [('ις','ιος'),('υς','υος')]:
        if nom.endswith(ending) and gen==nom[:-len(ending)]+replacement:
            return '-'+genitive[len(nom)-len(ending):]
    return genitive

def entries(entry):
    return entry['entradas'] if entry.get('tipo')=='grupo' else [entry]

def adjective_display(lemma):
    forms=lemma.split('/')
    if len(forms)<2:return lemma
    nom=plain(forms[0])
    if nom in ('μεγας','πας','πολυς'):return lemma
    ending=next((s for s in ('ους','εις','ων','ην','ος','ης','ας','υς','ις','ον','η','α') if nom.endswith(s)),None)
    if not ending:return lemma
    stem=nom[:-len(ending)]
    result=[forms[0]]
    for form in forms[1:]:
        short=plain(form)
        result.append('-'+form[len(stem):] if short.startswith(stem) and len(short)>len(stem) else form)
    return '/'.join(result)

def format_entry(entry):
    e=dict(entry)
    if e.get('tipo')=='grupo':
        e['entradas']=[format_entry(x) for x in e['entradas']]
        e['forma']=e['entradas'][0]['forma']
        return e
    if e.get('tipo') in ('crase','preposicao'):return e
    analysis=e['analise'].replace('voz ','')
    analysis=re.sub(r'([123]ª)\s+sing\.',r'\1 s.',analysis)
    analysis=re.sub(r'([123]ª)\s+pl\.',r'\1 p.',analysis)
    analysis=re.sub(r'^v\.[, ]*','',analysis)
    if analysis.startswith('adj.'):
        e['lema_base']=e.get('lema_base',e['lema'])
        e['lema']=adjective_display(e['lema_base'])
    if analysis.startswith('subst.') or e.get('artigo') or e.get('tipo')=='nome':
        gender=e.get('artigo')
        if not gender:
            match=re.search(r'(masc\.|fem\.|neut\.)',analysis)
            assert match,(e,'Noun without gender information')
            gender={'masc.':'ὁ','fem.':'ἡ','neut.':'τό'}[match[0]]
        lemma=e.get('lema_base',e['lema'])
        forms=lemma.split('/')
        if forms[0]=='ἀντίποινα':gender='τά'
        if len(forms)==2:
            e['lema']=forms[0]+', '+genitive_display(*forms)+', '+gender
        else:
            e['lema']=lemma+', '+gender
        e['lema_base']=lemma
        e['artigo']=gender
        e['tipo']='nome'
        analysis=re.sub(r',?\s*(masc\.|fem\.|neut\.)','',analysis).rstrip(', ')
        analysis=re.sub(r'^subst\.,?\s*','',analysis)
        if not analysis.endswith('.'):analysis+='.'
    e['analise']=analysis
    return e
