"""Generate the complete reading text from the retained TEI source."""
from pathlib import Path
import json
import unicodedata
import xml.etree.ElementTree as ET
from convencoes import format_entry,entries

base = Path(__file__).resolve().parent
root = ET.parse(base / 'fontes/tlg0085.tlg002.1st1K-grc1.xml').getroot()
notes = {n:format_entry(e) for n,e in json.loads((base / 'notas.json').read_text(encoding='utf-8')).items()}

def tag(node):
    return node.tag.rsplit('}', 1)[-1]

def reading(node):
    text = node.text or ''
    for child in node:
        kind = tag(child)
        if kind == 'lb':
            text += ' BREAKLINE '
        elif kind == 'gap':
            text += '[…]'
        elif kind != 'note':
            text += reading(child)
        text += child.tail or ''
    return ' '.join(text.split())

def tex(text):
    for old, new in [('&', r'\&'), ('%', r'\%'), ('#', r'\#'), ('_', r'\_')]:
        text = text.replace(old, new)
    return text.replace(' BREAKLINE ', ' ')

def key(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text).lower()
                   if not unicodedata.combining(c)).replace('ς', 'σ')

speakers = {
    key('Χορός'): ('chorus', 'Χορός', 'CORO'),
    key('Ἄτοσσα'): ('atossa', 'Ἄτοσσα', 'ATOSSA'),
    key('Ἄγγελος'): ('messenger', 'Ἄγγελος', 'MENSAGEIRO'),
    key('Δαρεῖος'): ('darius', 'Δαρεῖος', 'DARIO'),
    key('Ειδωλον Δαρειου'): ('darius', 'Εἴδωλον Δαρείου', 'SOMBRA DE DARIO'),
    key('Ξέρξης'): ('xerxes', 'Ξέρξης', 'XERXES'),
}
sections = {
    1: ('Párodo', '1–154'),
    155: ('Primeiro Episódio', '155–531'),
    532: ('Primeiro Estásimo', '532–597'),
    598: ('Segundo Episódio', '598–622'),
    623: ('Segundo Estásimo / Canto de Evocação', '623–680'),
    681: ('Terceiro Episódio', '681–851'),
    852: ('Terceiro Estásimo', '852–907'),
    908: ('Éxodo', '908–1077'),
}
output, records = [], []
current_actor = None
for node in root.iter():
    if tag(node) == 'speaker':
        raw = reading(node)
        actor, greek, portuguese = speakers[key(raw)]
        if actor != current_actor:
            capitals=''.join(c for c in unicodedata.normalize('NFD',greek.upper())
                             if not unicodedata.combining(c))
            output.append(r'\falante{' + capitals + '}')
        else:
            output.append(r'\pausaestrofe')
        current_actor = actor
    elif tag(node) == 'l':
        n = int(node.attrib['n'])
        if n in sections:
            title, span = sections[n]
            heading = r'\parte{' + title + '}{' + span + '}'
            at = len(output) - 1 if output and output[-1].startswith((r'\falante', r'\pausaestrofe')) else len(output)
            output.insert(at, heading)
        verse = reading(node)
        note = ''
        if str(n) in notes:
            parts=[]
            for entry in entries(notes[str(n)]):
                assert entry['forma'] in verse, (n, entry['forma'], verse)
                macro = r'\notagramaticalquebrada' if entry.get('quebra') else r'\notagramatical'
                fields=('forma','lema','sentido','analise')
                if entry.get('tipo')=='crase':
                    macro=r'\desdobramentoquebrado' if entry.get('quebra') else r'\desdobramento'
                    fields=('forma','lema')
                elif entry.get('tipo')=='preposicao':
                    macro=r'\preposicao'+entry['posicao']
                    fields=('forma','caso','sentido')
                    if entry.get('exibir_lema'):
                        macro=r'\preposicaolema'+entry['posicao']
                        fields=('forma','lema','caso','sentido')
                parts.append(macro + ''.join(
                    '{' + (tex(entry[field]).replace('/', r'/\allowbreak ')
                           if field=='lema' else tex(entry.get('forma_exibida',entry[field]) if field=='forma' else entry[field])) + '}'
                    for field in fields))
            note=r'\crlf '.join(parts)
        command=r'\verso'
        reading_tex=tex(verse)
        output.append(command+'{' + str(n) + '}{' + note + '}{' + reading_tex + '}')
        records.append({'n': n, 'speaker': current_actor, 'text': verse})

numbers = [r['n'] for r in records]
assert numbers == sorted(set(numbers)), 'Unexpected duplicate or out-of-order line IDs'
assert numbers[0] == 1 and numbers[-1] == 1076
assert len(records) == 1063
assert all(r['text'] for r in records), 'Empty line without a represented gap'
(base / 'texto-integral.tex').write_text('\n'.join(output) + '\n', encoding='utf-8')
(base / 'fontes/linhas-extraidas.json').write_text(
    json.dumps(records, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
audit = {
    'source_lines': len(records), 'first': numbers[0], 'last': numbers[-1],
    'numbering_gaps': sorted(set(range(1, 1077)) - set(numbers)),
    'represented_lacunae': [r['n'] for r in records if '[…]' in r['text']],
    'annotated_lines': sorted(map(int, notes)),
}
(base / 'fontes/auditoria-extracao.json').write_text(
    json.dumps(audit, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(audit, ensure_ascii=False))
