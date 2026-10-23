"""Apply the reviewed opening and explicit contextual grammar to the bank.

The fit pass records requested entries that need further space; this script
does not treat a bare fragment of a split word as an independent lemma.
"""
from pathlib import Path
import json
from convencoes import entries, format_entry

base = Path(__file__).resolve().parent
bank = json.loads((base/'revisoes/notas-ampliadas-2026-10-10.json').read_text(encoding='utf-8'))
bank = {n: [dict(e) for e in entries(g)] for n, g in bank.items()}
records = json.loads((base/'fontes/linhas-extraidas.json').read_text(encoding='utf-8'))
texts = {r['n']: r['text'] for r in records}
review = json.loads((base/'revisoes/felipe-2026-10-10.json').read_text(encoding='utf-8'))

# Requested lexical forms, including complete display forms for split words.
# verse | anchor | display | dictionary forms | contextual meaning | analysis
rows = '''
9|ἤδη||ἤδη|já|adv.
28|εὐτλήμονι||εὐτλήμων/εὐτλῆμον|resistente, intrépido|adj., dat. sing. fem.
47|τέλη||τέλος, -ους, τό|destacamento|ac. pl.
49|πελάτης||πελάτης, -ου, ὁ|habitante|nom. sing.
54|σύρδην||σύρδην|em massa|adv.
62|πόθῳ||πόθος, -ου, ὁ|saudade|dat. sing.; causa: por saudade
63|ἄλοχοί||ἄλοχος, -ου, ἡ|esposa|nom. pl.
63|ἡμερολεγδὸν||ἡμερολεγδόν|contando os dias|adv.
64|τείνοντα||τείνω|alongar|part., pres., at., ac. sing. masc.; com χρόνον: tempo que se prolonga
68|πορ-|πορθμόν|πορθμός, -οῦ, ὁ|estreito marítimo|ac. sing.; continua no v. 69
71|πολύγομφον||πολύγομφος/-ον|preso por muitas cavilhas|adj., ac. sing. neut.
74|ποιμα-|ποιμανόριον|ποιμανόριον, -ου, τό|rebanho humano|ac. sing.; continua no v. 75
76|διχόθεν||διχόθεν|em duas divisões|adv.
76|πεζονόμον||πεζονόμος/-ον|que avança por terra|adj., ac. sing. neut.
78|ἐχυροῖσι||ἐχυρός/-ά/-όν|forte|adj., dat. pl. masc.; dat. com πεποιθώς: confiando em
80|γενεᾶς||γενεά, -ᾶς, ἡ|linhagem|gen. sing.; χρυσογόνου γενεᾶς: de linhagem nascida do ouro
81|κυανοῦν||κυάνεος/-α/-ον|escuro|adj., ac. sing. neut.; forma contraída
82|φονίου||φόνιος/-α/-ον|sanguinário|adj., gen. sing. masc.
87|δόκιμος||δόκιμος/-ον|capaz, aprovado|adj., nom. sing. masc.
88|ῥεύματι||ῥεῦμα, ῥεύματος, τό|torrente|dat. sing.; aqui, torrente de homens
89|ἐχυροῖς||ἐχυρός/-ά/-όν|forte|adj., dat. pl. neut.
93|δολόμητιν||δολόμητις/δολόμητι|de intenção enganadora|adj., ac. sing. fem.
93|ἀπάταν||ἀπάτη, -ης, ἡ|engano|ac. sing.; forma dórica
95|πήδη-|πήδημα|πήδημα, πηδήματος, τό|salto|ac. sing.; continua no v. 96
96|εὐπετῶς||εὐπετῶς|facilmente|adv.
99|τόθεν||τόθεν|de lá|adv.
99|ὕπερθέν||ὕπερθεν|por cima|adv.
100|νιν||νιν|o, a|pron., ac. sing.; aqui, o homem capturado
100|ἄνατον||ἄνατος/-ον|sem dano|adj., ac. sing. masc.
101|θεόθεν||θεόθεν|por determinação divina|adv.
104|πυργοδαΐκτους||πυργοδάικτος/-ον|que destroem torres|adj., ac. pl. masc.
107|ἀναστάσεις||ἀνάστασις, ἀναστάσεως, ἡ|devastação|ac. pl.; aqui, destruição de cidades
108|ἔμαθον||μανθάνω|aprender|aor., ind., at., 3ª p.; + inf.: aprender a
108|εὐρυπόροι-|εὐρυπόροιο|εὐρύπορος/-ον|de amplas vias|adj., gen. sing. fem.; gen. poético em -οιο; continua no v. 109
109|πολιαι-|πολιαινομένας|πολιαίνω|embranquecer|part., pres., méd./pass., gen. sing. fem.; forma dórica; continua no v. 110
110|λάβρῳ||λάβρος/-α/-ον|impetuoso|adj., dat. sing. neut.
111|ἄλσος||ἄλσος, -ους, τό|bosque|ac. sing.; aqui, o mar figurado como bosque
112|πίσυνοι||πίσυνος/-ον|confiante|adj., nom. pl. masc.; + dat.: confiando em
112|λεπτοδόμοις||λεπτοδόμος/-ον|de delicada feitura|adj., dat. pl. neut.
112|πεί-|πείσμασι|πεῖσμα, πείσματος, τό|cordame|dat. pl.; continua no v. 113
113|λα-|λαοπόροις|λαοπόρος/-ον|que transporta homens|adj., dat. pl. fem.; continua no v. 114
115|μελαγχίτων||μελαγχίτων/μελαγχῖτον|vestido de negro|adj., nom. sing. fem.
117|ὀᾶ||ὀᾶ|ai!|interj.
118|πύθη-|πύθηται|πυνθάνομαι|saber, descobrir|aor., subj., méd., 3ª s.; μή + subj.: temor de que; continua no v. 119
120|πόλισμ᾽|πόλισμα|πόλισμα, πολίσματος, τό|cidade|nom. sing. neut.
121|ᾄσεται||ᾄδω|cantar|fut., ind., méd., 3ª s.
122|γυναικοπλη-|γυναικοπληθής|γυναικοπληθής/-ές|repleto de mulheres|adj., nom. sing. masc.; continua no v. 123
123|ὅμιλος||ὅμιλος, -ου, ὁ|multidão|nom. sing.
126|ἱππηλάτας||ἱππηλάτης, -ου, ὁ|cavaleiro|nom. sing.; forma dórica em -ας
128|σμῆνος||σμῆνος, -ους, τό|enxame|nom./ac. sing.; σμῆνος ὥς: como um enxame
130|ἀμφίζευκτον||ἀμφίζευκτος/-ον|ligado a ambas as margens|adj., ac. sing. masc.
133|λέκτρα||λέκτρον, -ου, τό|leito conjugal|nom. pl.
135|ἑκά-|ἑκάστα|ἕκαστος/-η/-ον|cada um|adj., nom. sing. fem.; forma dórica; continua no v. 136
136|φιλάνορι||φιλάνωρ/φίλανορ|que ama o marido|adj., dat. sing. masc.
137|αἰχμάεντα||αἰχμήεις/αἰχμήεσσα/αἰχμῆεν|armado de lança|adj., ac. sing. masc.
137|θοῦρον||θοῦρος/-α/-ον|impetuoso|adj., ac. sing. masc.
137|εὐνα-|εὐνατῆρα|εὐνατήρ, εὐνατῆρος, ὁ|companheiro de leito|ac. sing.; continua no v. 138
139|μονόζυξ||μονόζυξ|sem par|adj., nom. sing. fem.
141|στέγος||στέγος, -ους, τό|edifício, abrigo|ac. sing.; complemento de ἐνεζόμενοι
143|θώμεθα||τίθημι|pôr|aor., subj., méd., 1ª p.; exortação: dediquemos; φροντίδα θέσθαι: ocupar-se de
143|χρεία||χρεία, -ας, ἡ|necessidade|nom. sing.
143|προσήκει||προσήκω|incumbir, caber|pres., ind., at., 3ª s.; χρεία προσήκει: é necessário
144|ἄρα||ἄρα|então, afinal|partícula; reforça a pergunta
148|δορικράνου||δορίκρανος/-ον|de ponta de lança|adj., gen. sing. fem.
150|ἥδε||ὅδε/ἥδε/τόδε|esta|pron. demonstr., nom. sing. fem.; aqui, a rainha que se aproxima
153|προσφθόγγοις||πρόσφθογγος/-ον|de saudação|adj., dat. pl. masc.
153|χρεὼν||χρεών|é preciso|impessoal; + ac. e inf.: é preciso que alguém faça
155|ὑπερτάτη||ὑπέρτατος/-η/-ον|supremo|adj., superl., voc. sing. fem.
157|εὐνάτειρα||εὐνάτειρα, -ας, ἡ|companheira de leito|nom. sing.
157|ἔφυς||φύω|ser por natureza|aor., ind., at., 2ª s.; aqui: foste
158|εἴ τι μὴ||εἰ μή|a menos que|εἴ τι μή: salvo se, por acaso
162|ἀδείμαντος||ἀδείμαντος/-ον|sem temor|adj., nom. sing. fem.; + gen.: sem temor por; οὐδαμῶς: de modo algum
162|ἐμαυτῆς||ἐμαυτοῦ/ἐμαυτῆς|de mim mesma|pron. reflex., gen. sing. fem.; complemento de ἀδείμαντος: por mim mesma
'''

added = []
for row in rows.strip().splitlines():
    n, anchor, display, lemma, meaning, analysis = row.split('|')
    assert anchor in texts[int(n)], (n, anchor)
    import re
    analysis = re.sub(r'; continua no v\. \d+', '', analysis)
    e = {'forma': anchor, 'lema': lemma, 'sentido': meaning,
         'analise': analysis, 'revisao_felipe': True, 'prioridade_editorial': True}
    if display:
        e['forma_exibida'] = display
    opts = bank.setdefault(n, [])
    opts[:] = [old for old in opts if old['forma'] != anchor]
    opts.append(e)
    added.append({'verse': int(n), 'form': anchor, 'display': display or anchor})

# Latest highlights override the old basic-word veto. Existing entries requested
# by the review receive the same priority as new ones.
requested = set()
for a in review['annotations']:
    for segment in a['verse_segments']:
        n = str(segment['verse'])
        mark = segment['marked'].strip('.,:;')
        for e in bank.get(n, []):
            if e['forma'] in mark or mark in e['forma']:
                e['revisao_felipe'] = True
                e['prioridade_editorial'] = True
                requested.add((int(n), e['forma']))

excluded_forms = {2: ['ἐς'], 48: ['φοβερὰν', 'ὄψιν'], 53: ['ὄχλον'],
                  56: ['ἔθνος'], 59: ['ἄνθος', 'αἴας'], 92: ['λαός'],
                  103: ['όν'], 116: ['φρὴν', 'φόβῳ'], 125: ['πέπλοις'],
                  129: ['στρατοῦ'], 155: ['ἄνασσα'], 156: ['μῆτερ', 'γεραιά'],
                  158: ['στρατῷ']}
excluded = []
for n, forms in excluded_forms.items():
    old = bank.get(str(n), [])
    excluded.extend({'verse': n, 'form': e['forma']} for e in old if e['forma'] in forms)
    bank[str(n)] = [e for e in old if e['forma'] not in forms]

# Values of moods are checked in their actual clauses, not inferred from the
# morphology alone. Correct clear homograph/alignment errors at the same time.
mode_notes = {
    (125, 'πέσῃ'): 'temor de que; segue a construção com μή do v. 118',
    (163, 'ἀντρέψῃ'): 'μή + subj.: temor de que derrube',
    (174, 'θέλῃ'): 'relativa com ἄν + subj.: tudo o que a capacidade permitir',
    (228, 'ἐκτελοῖτο'): 'opt. de desejo, sem ἄν: que se cumpra',
    (230, 'μόλωμεν'): 'εὖτ᾽ ἄν + subj.: quando chegarmos; evento futuro',
    (267, 'φράσαιμ᾽'): 'opt. + ἄν: poderia relatar',
    (360, 'ἐκσωσοίατο'): 'opt. em discurso indireto após verbo no passado: salvariam a vida',
    (365, 'λήξῃ'): 'εὖτ᾽ ἄν + subj.: quando cessar; evento futuro',
    (365, 'λάβῃ'): 'εὖτ᾽ ἄν + subj.: quando a escuridão tomar; evento futuro',
    (430, 'στοιχηγοροίην'): 'εἰ + opt.: mesmo se eu enumerasse; hipótese',
    (430, 'ἐκπλήσαιμί'): 'οὐκ ἄν + opt.: não conseguiria completar',
    (451, 'ἐκσῳζοίατο'): 'opt. na subordinada eventual em contexto passado: quando escapassem',
    (526, 'πέλοι'): 'εἴ + opt.: na esperança de que algo seja melhor',
    (529, 'μόλῃ'): 'ἐάν + subj.: se vier; condição futura',
    (601, 'εὐροῇ'): 'ὅταν + subj.: sempre que a sorte corre bem',
    (632, 'εἴποι'): 'ἄν + opt.: poderia dizer',
    (650, 'ἀνείης'): 'opt. de desejo, sem ἄν: que deixes subir',
    (664, 'κλύῃς'): 'ὅπως + subj.: para que ouças; finalidade',
    (786, 'φανεῖμεν'): 'οὐκ ἄν + opt.: não apareceríamos',
    (789, 'πράσσοιμεν'): 'πῶς ἄν + opt.: como poderíamos agir?',
    (826, 'ἐκχέῃ'): 'μηδέ + subj.: que ninguém dissipe; proibição',
}
regency_notes = {
    (7, 'ἐφορεύειν'): '+ gen.: vigiar, governar algo; χώρας é o complemento',
    (49, 'στεῦται'): '+ inf.: vangloriar-se de que fará; ἀμφιβαλεῖν é inf. fut.',
    (78, 'πεποιθὼς'): '+ dat.: confiar em; perfeito com valor de estado',
    (128, 'ἐκλέλοιπεν'): 'perf.: abandonou e permanece ausente',
    (149, 'κεκράτηκεν'): 'perf.: obteve a vitória e a conserva',
    (158, 'μεθέστηκε'): '+ dat.: mudar de disposição para com; aqui, στρατῷ',
    (824, 'μέμνησθ᾽'): '+ gen.: lembrar-se de; Ἀθηνῶν, Ἑλλάδος',
    (826, 'ἐρασθεὶς'): '+ gen.: desejar; ἄλλων é o complemento',
}
for n, opts in bank.items():
    for e in opts:
        key = (int(n), e['forma'])
        if e.get('lema')=='εἶμι' and e['forma'] not in ('ἴτε','ἰόντ᾽','ἴθι','εἶμι','ὧν','ἢν'):
            e.update(lema='εἰμί', sentido='', apoio_apenas_morfologico=True)
        if key == (105, 'ἱππιοχάρμας'):
            e.update(lema='ἱππιοχάρμης', lema_base='ἱππιοχάρμης',
                     sentido='de combate a cavalo', analise='adj., ac. pl. masc.; concorda com κλόνους',
                     tipo='adjetivo', revisao_felipe=True, prioridade_editorial=True)
            e.pop('artigo', None)
        if key == (162, 'οὖσ᾽'):
            e.update(lema='εἰμί', sentido='ser, estar', analise='part., pres., nom. sing. fem.', revisao_felipe=True)
        if key == (513, 'ἐκλείπω'):
            e['analise'] = 'pres., ind., at., 1ª s.'
        if key == (622, 'προπέμψω'):
            e['analise'] = 'fut., ind., at., 1ª s.'
        if key in mode_notes:
            e['analise'] += '; ' + mode_notes[key]
            e['explicacao_contextual'] = True
            e['prioridade_editorial'] = True
        if key in regency_notes:
            e['analise'] += '; ' + regency_notes[key]
            e['explicacao_contextual'] = True
            e['prioridade_editorial'] = True
    # Interjection ὦ is not a subjunctive of εἰμί.
    bank[n] = [e for e in opts if not (e['forma'] == 'ὦ' and 'subj.' in e['analise'])
               and not (e['forma'] in ('ἂν','ἄν') and e['analise'].startswith('adj.'))
               and not (e['forma'] in ('ὧν','ἢν') and e.get('lema')=='εἶμι')]
    for e in bank[n]:
        if (int(n),e['forma']) in {(49,'στεῦται'),(125,'πέσῃ'),(143,'θώμεθα'),(162,'ἀδείμαντος')}:
            e['gramatica_obrigatoria'] = True

for n, opts in bank.items():
    for e in opts:
        if e.get('sentido_original') and not e.get('revisao_felipe'):
            e['sentido'] = e['sentido_original']
        e.pop('sentido_original', None)
    opts.sort(key=lambda e: texts[int(n)].index(e['forma']))
bank = {n: {'tipo': 'grupo', 'forma': es[0]['forma'], 'entradas': [format_entry(e) for e in es]}
        for n, es in bank.items() if es}
(base/'revisoes/notas-rodada-felipe-2026-10-11.json').write_text(
    json.dumps(bank, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
(base/'revisoes/aplicacao-felipe-2026-10-11.json').write_text(json.dumps({
    'status': 'banco_revisado_antes_da_composicao', 'added_or_rewritten': added,
    'explicit_exclusions': excluded,
    'mood_explanations': [{'verse': n, 'form': f, 'explanation': t} for (n, f), t in mode_notes.items()],
    'regency_and_aspect': [{'verse': n, 'form': f, 'explanation': t} for (n, f), t in regency_notes.items()],
}, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print('Banco revisado:', sum(len(entries(g)) for g in bank.values()), 'entradas.')
