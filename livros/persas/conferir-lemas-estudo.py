"""Reconstruct lexical words across lyric verse hyphens and reconcile lemmatization."""
from pathlib import Path
import csv,json,re,unicodedata as U,collections,difflib,zipfile
base=Path(__file__).resolve().parent;b=base/'fontes/estudo-lexical'
fix=json.loads((b/'correcoes-lemas.json').read_text(encoding='utf-8'))
rows=list(csv.DictReader((base/'fontes/tokens-estatisticas.csv').open(encoding='utf-8-sig')))
source=[];joins=[]
for row in rows:
    parts=re.split('[—–]',row['forma'])
    for raw in parts:
        r=dict(row);r['verso']=int(r['verso']);r['verso_final']=r['verso'];r['forma']=raw.strip('<>†‡');r['source']='Perseus Treebank'
        if not any(c.isalpha() for c in raw):continue
        if len(parts)>1:r['lema']='';r['estado']='não classificado'
        if source and source[-1]['forma'].endswith('-'):
            prev=source[-1];joins.append({'first':prev['forma'],'second':r['forma'],'verso':prev['verso'],'verso_final':r['verso']})
            prev['forma']=prev['forma'][:-1]+r['forma'];prev['verso_final']=r['verso'];prev['lema']='';prev['estado']='não classificado';continue
        source.append(r)
letters=dict(zip('abgdezhqiklmncoprstufxyw','αβγδεζηθικλμνξοπρστυφχψω'));marks={')':'\u0313','(':'\u0314','/':'\u0301','\\':'\u0301','=':'\u0342','+':'\u0308','|':'\u0345'}
def greek(s):
    s=re.sub(r'\d+$','',s.replace('*',''));s=re.sub(r'^([)(/=+|]+)([a-z])',r'\2\1',s)
    r=U.normalize('NFC',''.join(letters.get(c,marks.get(c,c)) for c in s));return r[:-1]+'ς' if r.endswith('σ') else r
# Escapes above are literals in generated source; normalize them in the authoring step.
def norm(s):return ''.join(c for c in U.normalize('NFD',s).lower() if c.isalpha()).replace('ς','σ')
file=b/'diorisis-persas-1.6.json'
data=json.loads(file.read_bytes());d=[]
for s in data['sentences']:
    for t in s['tokens']:
        if t['type']=='word' and isinstance(t.get('lemma'),dict):
            d.append({'forma':greek(t['form']),'lema':greek(t['lemma'].get('entry','')),'proper':t['lemma'].get('POS')=='proper','pos':t['lemma'].get('POS')})
seq=difflib.SequenceMatcher(None,[norm(r['forma']) for r in source],[norm(r['forma']) for r in d],autojunk=False);aligned={}
for block in seq.get_matching_blocks():
    for i in range(block.size):aligned[block.a+i]=d[block.b+i]
manual={94:{'ἀλύξει;':'ἀλύσκω'},96:{'εὐπετῶς':'εὐπετής'},143:{'θώμεθα,':'τίθημι'},155:{'ὑπερτάτη,':'ὑπέρτατος'},165:{'φραστός':'φραστός'},167:{'μήτ᾽':'μήτε'},218:{'ἀγάθ᾽':'ἀγαθός'},292:{'μήτ᾽':'μήτε'},344:{'μάχῃ;':'μάχη'},371:{'πᾶσιν':'πᾶς'},490:{'βορᾶς':'βορέας','ἐδέξαντ᾽:':'δέχομαι'},589:{'βασιλεία':'βασίλειος'},613:{'μέτα,':'μετά'},648:{'ἤθη.':'ἦθος'},685:{'ἐδεξάμην.':'δέχομαι'},752:{'οὑμὸς':'ἐμός','τοῦ':'ὁ'},774:{'ἦρξεν,':'ἄρχω'},784:{'ἐμοὶ':'ἐγώ'},875:{'πόρον':'πόρος'},915:{'εἴθ᾽':'εἴθε'},1028:{'τραπέντα':'τρέπω'},1053:{'οἴ,':'οἴ'},1060:{'ἀκμῇ':'ἀκμή'}}
additional={30: {'Μασίστης,': 'Μασίστης'}, 42: {'οἵτ᾽': 'ὅς+τε'}, 43: {'Μιτρογαθὴς': 'Μιτρογαθής'}, 49: {'πελάτης': 'πελάτης'}, 61: {'Ἀσιᾶτις': 'Ἀσιᾶτις'}, 81: {'κυανοῦν': 'κυάνεος'}, 93: {'δολόμητιν': 'δολομήτης', 'δ᾽': 'δέ', 'ἀπάταν': 'ἀπάτη', 'θεοῦ': 'θεός'}, 94: {'τίς': 'τίς', 'ἀνὴρ': 'ἀνήρ', 'θνατὸς': 'θνητός'}, 95: {'τίς': 'τίς', 'ὁ': 'ὁ', 'κραιπνῷ': 'κραιπνός', 'ποδὶ': 'πούς', 'πήδημα': 'πήδημα'}, 96: {'τόδ᾽': 'ὅδε', 'ἀνᾴσσων;': 'ἀναΐσσω'}, 97: {'φιλόφρων': 'φιλόφρων', 'γὰρ': 'γάρ', 'παρασαίνει': 'παρασαίνω'}, 98: {'βροτὸν': 'βροτός', 'εἰς': 'εἰς', 'ἄρκυας': 'ἄρκυς', 'Ἄτα,': 'Ἄτη'}, 99: {'τόθεν': 'τόθεν', 'οὐκ': 'οὐ', 'ἔστιν': 'εἰμί', 'ὕπερθέν': 'ὕπερθεν'}, 100: {'νιν': 'νιν', 'ἄνατον': 'ἄνατος', 'ἐξαλύξαι.': 'ἐξαλύσκω'}, 161: {'με': 'ἐγώ'}, 223: {'κάτοχ᾽': 'κάτοχος', 'ἀμαυροῦσθαι': 'ἀμαυρόω'}, 230: {'κεῖνο': 'ἐκεῖνος'}, 239: {'χερῶν': 'χείρ'}, 245: {'κιόντων': 'κίω'}, 246: {'εἴσει': 'οἶδα', 'ναμερτῆ': 'νημερτής'}, 250: {'μέγας': 'μέγας'}, 269: {'πολέα': 'πολύς'}, 270: {'γᾶσδ᾽': 'γῆ+δέ', 'ἦλθεν': 'ἔρχομαι', 'αἴας': 'αἶα'}, 277: {'πλαγκτοῖς': 'πλαγκτός'}, 282: {'δᾴος,': 'δάιος'}, 283: {'ἤνυσαν,': 'ἀνύω'}, 289: {'ἔκτισσαν': 'κτίζω'}, 306: {'ἰθαγενὴς': 'ἰθαγενής'}, 316: {'πυρσὴν': 'πυρσός'}, 317: {'πορφυρᾷ': 'πορφύρεος'}, 327: {'ἔπαρχος,': 'ἔπαρχος'}, 359: {'ἐπενθορόντες': 'ἐπενθρῴσκω'}, 415: {'θ᾽': 'τε'}, 436: {'αὐτοὺς': 'αὐτός'}, 516: {'ἐνήλλου': 'ἐνάλλομαι'}, 532: {'μὲν': 'μέν'}, 535: {'Ἀγβατάνων': 'Ἀγβάτανα'}, 549: {'Ἀσὶς': 'Ἀσίς', 'ἐκκεκενωμένα.': 'ἐκκενόω'}, 558: {'δὲ': 'δέ'}, 563: {'ἠδ᾽': 'ἠδέ'}, 569: {'ληφθέντες': 'λαμβάνω'}, 571: {'ἔρρουσι:': 'ἔρρω'}, 621: {'ἀγκαλεῖσθε,': 'ἀνακαλέω'}, 635: {'σαφηνῆ': 'σαφηνής'}, 638: {'διαμβοάσω;': 'διαμβοάω'}, 645: {'τὸν': 'ὁ'}, 666: {'δεσποτᾶν': 'δεσπότης'}, 677: {'γὰρ': 'γάρ'}, 713: {'ἀκούσει': 'ἀκούω'}, 730: {'στένειν.': 'στένω'}, 740: {'ἐπέσκηψεν': 'ἐπισκήπτω'}, 749: {'δὲ': 'δέ', 'ἁπάντων': 'ἅπας'}, 816: {'αἱματοσταγὴς': 'αἱματοσταγής'}, 834: {'παντὶ': 'πᾶς'}, 841: {'ψυχὴν': 'ψυχή', 'ἡδονῇ': 'ἡδονή'}, 845: {'κακῶν': 'κακός'}, 859: {'πολίσματα': 'πόλισμα'}, 860: {'ἐπέρθομεν.': 'πέρθω'}, 932: {'ἐγών,': 'ἐγώ'}, 945: {'λαοπαθέα': 'λαοπαθής'}, 951: {'ναύφαρκτος': 'ναύφρακτος'}, 959: {'Ἀγδαβάτας,': 'Ἀγδαβάτας'}, 987: {'ἴυγγά': 'ἰυγή', 'δῆτ᾽': 'δῆτα'}, 988: {'ὑπορίνεις,': 'ὑπορίνω'}, 990: {'ἄλαστ᾽': 'ἄλαστος'}, 1006: {'ἔθεσθ᾽': 'τίθημι'}, 1011: {'Ἰαόνων': 'Ἰάων'}, 1016: {'μέγ᾽': 'μέγας', 'ἄλαστε,': 'ἄλαστος'}, 1039: {'διαίνομαι': 'διαίνω', 'γοεδνὸς': 'γοεδνός', 'ὤν.': 'εἰμί'}, 1047: {'αἰαῖ': 'αἰαῖ', 'αἰαῖ,': 'αἰαῖ', 'δύα': 'δύη', 'δύα.': 'δύη'}, 1052: {'ἀμμεμίξεται,': 'ἀναμείγνυμι'}, 1054: {'βόα': 'βοάω'}, 213: {'πράξασ': 'πράσσω', 'οὐχ': 'οὐ'}}
additional.update({79:{'χρυσογόνου':'χρυσόγονος'},662:{'φάλαρον':'φάλαρον'}})
additional.update({6:{'Δαρειογενὴς':'δαρειογενής'},12:{'Ἀσιατογενὴς':'ἀσιατογενής'},
35:{'Αἰγυπτογενής,':'αἰγυπτογενής'},37:{'ὠγυγίους':'ὠγύγιος'},
145:{'Δαρειογενής,':'δαρειογενής'},393:{'παιᾶν᾽':'παιάν'},
605:{'παιώνιος:':'παιώνιος'},644:{'Σουσιγενῆ':'σουσιγενής'},
919:{'περσονόμου':'περσονόμος'},975:{'ὠγυγίους':'ὠγύγιος'}})
additional.update({101:{'Μοῖρ᾽':'Μοῖρα'},103:{'Πέρσαις':'Πέρσης'},
332:{'Πέρσαις':'Πέρσης'},655:{'Πέρσαις,':'Πέρσης'},711:{'Πέρσαις':'Πέρσης'},
884:{'Μύκονος,':'Μύκονος'},1007:{'Ἄτα.':'Ἄτη'}})
for n,forms in additional.items():manual.setdefault(n,{}).update(forms)
result=[];changes=[];disagreements=[]
for i,r in enumerate(source):
    orig=r['lema'];r['lema']=fix['mappings'].get(orig,orig);match=aligned.get(i)
    if orig in fix['proper_names'] or (match and match['proper']):r['estado']='nome próprio';r['source']='conferência com Diorisis atualizado'
    elif not r['lema'] and match and match['lema']:
        r['lema']=match['lema'];r['estado']='analisado';r['source']='Diorisis 1.6; alinhamento na sequência';changes.append({'verso':r['verso'],'forma':r['forma'],'lema':r['lema']})
    for o in fix['token_overrides']:
        if r['verso']==o['verso'] and r['forma']==o['forma']:r['lema']=o['lema'];r['source']='correção de sentido em contexto'
    if r['forma'] in manual.get(r['verso'],{}):r['lema']=manual[r['verso']][r['forma']];r['estado']='analisado';r['source']='conferência editorial de forma e contexto'
    if r['lema'] and r['lema'][0].isupper():r['estado']='nome próprio'
    if r['lema']=='πιστόν':r['lema']='πιστός'
    if match and match['lema'] and r['lema'] and norm(r['lema'])!=norm(match['lema']) and r['estado']=='analisado':disagreements.append({'verso':r['verso'],'forma':r['forma'],'treebank':r['lema'],'diorisis':match['lema']})
    result.append(r)
with (b/'tokens-conferidos.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=result[0].keys());w.writeheader();w.writerows(result)
(b/'conferencia-lemas.json').write_text(json.dumps({'source_graphic_units':len(rows),'lexical_words':len(source),'joined_fragments':joins,'aligned_diorisis':len(aligned),'filled_gaps':changes,'disagreements':disagreements,'manual_overrides':manual,'states':dict(collections.Counter(r['estado'] for r in result))},ensure_ascii=False,indent=2),encoding='utf-8')
print('states',collections.Counter(r['estado'] for r in result),'joins',len(joins),'filled',len(changes),'disagreements',len(disagreements))
print('Unknown',[(r['verso'],r['forma']) for r in result if r['estado']=='não classificado'])
