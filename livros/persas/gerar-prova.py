from pathlib import Path
import xml.etree.ElementTree as ET

base = Path(__file__).resolve().parent
root = ET.parse(base / 'fontes/tlg0085.tlg002.1st1K-grc1.xml').getroot()
ns = {'t': 'http://www.tei-c.org/ns/1.0'}

def reading(node):
    text = node.text or ''
    for child in node:
        if child.tag.rsplit('}', 1)[-1] != 'note':
            text += reading(child)
        text += child.tail or ''
    return text

verses = []
for node in root.findall('.//t:l', ns):
    n = node.get('n', '')
    if n.isdigit() and 1 <= int(n) <= 30:
        verses.append((int(n), ' '.join(reading(node).split())))
assert len(verses) == 30, verses
notes = {
    1: r'\notagramatical{οἰχομένων}{οἴχομαι}{partir}{part., pres., méd., gen. pl. masc.}',
    8: r'\notagramatical{νόστῳ}{νόστος, -ου, ὁ}{retorno}{dat. sing.}',
    26: r'\notagramatical{ἠδ᾽}{ἠδέ}{e}{conj.}',
}
lines = []
for n, verse in verses:
    note = r'\inouter{' + notes[n] + '}' if n in notes else ''
    number = str(n) if n == 1 or n % 5 == 0 else ''
    lines.append(r'\noindent ' + note + r'\numeroverso{' + number + '}' + verse + r'\par')
(base / 'versos-1-30.tex').write_text('\n'.join(lines) + '\n', encoding='utf-8')
print('30 versos extraídos do TEI; notas críticas excluídas da leitura.')
