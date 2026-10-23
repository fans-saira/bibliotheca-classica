"""Publish conservative, disjoint occurrence classifications and an auditable residual.

Run conferir-lemas-estudo.py and estudar-vocabulario.py first. Automatic
screening is not a philological verdict; explicit LSJ reading decisions below
override it and are exported verbatim for review.
"""
from pathlib import Path
import csv,json,collections,importlib.util,hashlib

base=Path(__file__).resolve().parent
b=base/'fontes/estudo-lexical'
spec=importlib.util.spec_from_file_location('study',base/'estudar-vocabulario.py')
s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
details={d['lema']:d for d in s.detail}
decisions={}

def mark(words,category,reason):
    for l in words.split():
        if l not in details:raise ValueError('Unknown lemma: '+l)
        decisions[l]={'classe':category,'fundamento':reason,
                      'fonte':'LSJ; entrada do lema e referências nela citadas'}

mark('στάγμα ἀκάκης ἀγρέτης','5_residual',
     'Retirado da exclusividade: documentação externa, inscrição ou conjectura insuficientemente segura.')
mark('γάποτος γοεδνός δίρρυμος λινόδεσμος μέσακτος μειλικτήριος νεόκοτος οἰακοστροφέω ταγέω τοξουλκός τριτόσπορος χρυσεόστολμος ἁμάρτιον',
     '3_esquilo','Entrada do LSJ documenta este lema literário apenas em Ésquilo; referências Id. e remissões resolvidas na revisão.')
mark('δίεμαι δύσβατος εὐθυντήριος εὔθυνος ζευκτήριος κολπίας στόμωμα ἀναπομπός ἐφέτης ἱπποβάτης ἄκτωρ ἁλίτυπος μονόζυξ',
     '3_esquilo','Sentido da passagem, distinto das outras acepções do lema, documentado apenas em Ésquilo na entrada do LSJ.')
for l,sense,ref in [
 ('δίεμαι','temer','LSJ II; A.Pers.701'),
 ('δύσβατος','percorrido em sofrimento','LSJ II; A.Pers.1069'),
 ('εὐθυντήριος','que dirige/governa','LSJ I; A.Pers.764'),
 ('εὔθυνος','castigador/julgador','LSJ I; A.Pers.828'),
 ('ζευκτήριος','que une por um jugo','LSJ acepção adjetival; A.Pers.736'),
 ('κολπίας','que se avoluma em pregas','LSJ 1; A.Pers.1060'),
 ('στόμωμα','entrada/embocadura do Ponto','LSJ I; A.Pers.878'),
 ('ἀναπομπός','que envia para cima, do Hades','LSJ I; A.Pers.650'),
 ('ἐφέτης','comandante','LSJ I; A.Pers.79'),
 ('ἱπποβάτης','cavaleiro','LSJ I; A.Pers.26'),
 ('ἄκτωρ','líder','LSJ I; A.Pers.557'),
 ('ἁλίτυπος','batido pelo mar','LSJ uso adjetival; A.Pers.946'),
 ('μονόζυξ','solitário','LSJ I; A.Pers.139')]:
    decisions[l].update(sentido=sense,referencia=ref)

mark('γυναικοπληθής δάκρυμα δέργμα δέσμωμα δυσπόνητος εὐνατήριον κένανδρος κωπήρης λιβάς ναύφρακτος νεολαία πάνδυρτος παντάλας στύφλος σφαδάζω ταγός τοξόδαμνος ψυχαγωγός ἀγή ἀνακωκύω ἀντίποινα ἁλίρροθος ἄνανδρος ἑστιοῦχος ἐπιστενάζω ὑποσπανίζομαι ῥαχίζω οὐρίζω',
     '2_tragedia','LSJ documenta uso equivalente em Ésquilo e em outro tragediógrafo; complemento lexical à comparação quantitativa.')

# Conservative positive register. An early citation by itself is insufficient.
# These usages have epic/lyric register evidence or an equivalent archaic
# poetic use, rather than an unrelated old homonym or an exclusively later ode.
mark('αἰνός γυῖον εὐρύπορος ζόφος θοός θοῦρος κίω κλόνος κοιρανέω κραιπνός κῦδος λιγύς νημερτής νώνυμος πινύσκω πιφαύσκω πλαγκτός πολύγομφος πορφύρεος προσαυδάω στονόεις στεῦμαι τέθηπα τίπτε ταρφύς τυτθός τῆλε φερεσσακής ἀίω ἀγήνωρ ἀγαυός ἀείρω ἀλύσκω ἀμύσσω ἀυτή ἀφνειός ἄγχι ἄποτμος ἄρειος ἄρουρα ἄφαρ ἐκθρῴσκω ἐκφθίνω ἔντεα ἦτορ ἰαχή ἰσόθεος ἰωή ἰύζω ἱκάνω ὀπάζω ὄρνυμι ὄρχαμος ὑδρηλός ῥεῖθρον φάλαρον δουρικλυτός χοιράς κατερείκω χλιδανός λακίς γηραλέος ἀναΐσσω νησιώτης φιλόφρων',
     '4_outros','Uso épico/lírico equivalente documentado em fonte anterior a 456 a.C.; não é mera presença antiga do lema.')
for l,ref in {
 'χοιράς':'Archil.128; Pi.P.10.52 (498 a.C.)',
 'κατερείκω':'Sapph.62', 'χλιδανός':'Sapph.Supp.21.8',
 'λακίς':'Alc.18.8', 'γηραλέος':'Xenoph.; Anacr.; Pi.P.4 (462 a.C.)',
 'νησιώτης':'Pi.P.10.47 (498 a.C.); Pi.P.9.55 (474 a.C.)',
 'φιλόφρων':'Pi.P.1.94 (470 a.C.)',
 'ἰύζω':'Pi.P.4.237 (462 a.C.): grito de dor',
 'ἔντεα':'Pi.P.4.235 (462 a.C.): arreios',
 'φάλαρον':'Il.16.106: ornamento metálico',
}.items():decisions[l]['referencia']=ref

mark('μυριοταγός παρασαίνω πατρωνύμιος πύργινος ἐκπιδύομαι πολυβαφής θεότρεπτος ἀναΐσσω',
     '5_residual','Leitura conjectural ou variante textual: conservada no texto da edição, mas retirada das atribuições contextuais seguras.')
mark('νησιώτης φιλόφρων φάλαρον','5_residual',
     'Atestação antiga e sentido compatível confirmados; isso não demonstra que o vocabulário seja típico de um contexto literário distinto.')
mark('δαρειογενής αἰγυπτογενής σουσιγενής περσονόμος','3_esquilo',
     'Composto lexical, não nome próprio: uso literário documentado apenas em Ésquilo na entrada do LSJ.')
mark('ἀσιατογενής','5_residual',
     'Também atestado em Crítias, posterior ao recorte; portanto não exclusivo de Ésquilo nem elegível para a categoria 4.')
mark('ὠγύγιος','4_outros',
     'No sentido de primevo, remete ao registro mítico arcaico: Hes.Th.806; sentido equivalente nos dois usos de Persas.')
mark('παιώνιος','3_esquilo',
     'LSJ II, A.Pers.605: relativo ao péã de vitória, distinto da acepção medicinal compartilhada com outros autores.')
decisions['παιώνιος'].update(sentido='próprio do péã de vitória',referencia='LSJ II; A.Pers.605')

labels={'1_basico':'Básico fundamental','2_tragedia':'Tragédia, após o básico',
        '3_esquilo':'Ésquilo, após as anteriores','4_outros':'Outros contextos anteriores/contemporâneos',
        '5_residual':'Geral não fundamental / atribuição não demonstrada'}

def decide(row,core):
    if row['estado']=='nome próprio':return 'nome_proprio','Nome próprio excluído do denominador lexical comum',''
    if row['estado']!='analisado':return '5_residual','Leitura corrupta: lema não resolvido',''
    l=s.canon(row['lema']);d=details[l]
    if all(s.canon(k) in core for k in l.split('+')):
        return '1_basico','União Major, DCC e faixa de frequência Logeion',''
    decision=decisions.get(l)
    if decision:return decision['classe'],decision['fundamento'],decision.get('sentido','')
    if d['classe']=='2_tragedia':return '2_tragedia',d['razao'],''
    if d['classe']=='3_esquilo_candidato':return '3_esquilo','LSJ: apenas referências literárias a Ésquilo; ausência nos demais autores do corpus consultado',''
    return '5_residual','Uso geral ou caracterização contextual/sentido ainda não demonstrados',''

out=[]
for i,r in enumerate(s.rows,1):
    category,reason,sense=decide(r,s.core)
    out.append({'id':i,'verso':r['verso'],'verso_final':r['verso_final'],
                'forma':r['forma'],'lema':s.canon(r['lema']),
                'sentido_distintivo':sense,'classe':category,
                'fundamento':reason,'estado_lema':r['estado']})
common=[r for r in out if r['classe']!='nome_proprio'];denom=len(common)
counts=collections.Counter(r['classe'] for r in common)
summary=[{'classe':k,'nome':v,'ocorrencias':counts[k],
          'percentual':round(100*counts[k]/denom,3),
          'lemas_distintos_na_classe':len({r['lema'] for r in common if r['classe']==k and r['lema']})}
         for k,v in labels.items()]
# Lemmas can occur in more than one class if different meanings are used;
# occurrences always have exactly one class. Do not sum the lemma columns.
lemmas=[]
for l,d in details.items():
    rr=[r for r in common if r['lema']==l]
    lemmas.append({'lema':l,'ocorrencias':len(rr),'classes':' | '.join(sorted({r['classe'] for r in rr})),
                   'versos':' '.join(r['verso'] for r in rr),
                   'referencias_anteriores_lsj':' | '.join(d['referencias_anteriores_lsj']),
                   'decisao_editorial':decisions.get(l,{}).get('fundamento',''),
                   'referencia_revisada':decisions.get(l,{}).get('referencia',''),
                   'tragedias_comparativas':len(d['tragedias']),
                   'razao_densidade_tragica':d['razao_densidade']})
for name,data in [('classificacao-por-ocorrencia.csv',out),('classificacao-por-lema.csv',lemmas)]:
    with (b/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=data[0].keys());w.writeheader();w.writerows(data)
(b/'decisoes-revisadas.json').write_text(json.dumps(decisions,ensure_ascii=False,indent=2),encoding='utf-8')
variants={
 'Major_DCC':s.core_major|s.core_dcc,
 'principal_Major_DCC_Logeion1000':s.core,
 'ampliado_Major_DCC_Logeion2000':s.core_major|s.core_dcc|{s.canon(r['lema']) for r in s.logeion if r['rank']<=2000}}
sensitivity=[]
for name,core in variants.items():
    cc=collections.Counter(decide(r,core)[0] for r in s.rows if r['estado']!='nome próprio')
    sensitivity.append({'criterio':name,'lemas_no_repertorio':len(core),
                        'ocorrencias':dict(cc),'percentuais':{k:round(100*cc[k]/denom,3) for k in labels}})
result={'status':'levantamento conservador; atribuições contextuais e exclusividade dependem da documentação consultada',
        'data':'2026-10-10','fim_do_recorte_cronologico':'456 a.C.',
        'palavras_texto':len(out),'nomes_proprios':len(out)-denom,
        'denominador_ocorrencias_comuns':denom,'lemas_comuns_resolvidos':len(details),
        'leitura_nao_resolvida':1,'repertorio_basico':len(s.core),
        'categorias':summary,'sensibilidade':sensitivity,
        'tragedias_comparadas':s.trag and [(w['author'],w['title']) for w in s.trag],
        'lemas_em_mais_de_uma_classe':[r['lema'] for r in lemmas if ' | ' in r['classes']],
        'advertencia':'Os percentuais não demonstram invenção de palavras por Ésquilo, origem histórica ou influência direta. Categoria 3 significa exclusividade de atestação literária do lema/sentido no LSJ consultado, corroborada pelo corpus, não prova universal. O residual contém também vocabulário geral pouco frequente, não apenas palavras desconhecidas.'}
assert len(out)==5187 and sum(counts.values())==denom
assert all(r['classe'] in labels or r['classe']=='nome_proprio' for r in out)
assert not result['lemas_em_mais_de_uma_classe'], 'Check sense splits before reporting lemma percentages'
for r in summary:r['percentual_lemas']=round(100*r['lemas_distintos_na_classe']/len(details),3)
(b/'resultado-lexical.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'denominador':denom,'lemas':len(details),'categorias':summary,'sensibilidade':sensitivity},ensure_ascii=False,indent=2))
