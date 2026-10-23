"""Preserve Acrobat annotations and map marked Greek to the printed verses.

Read-only for the PDFs. The resulting register is a revision queue, not a
claim that its requests have already been incorporated into the edition.
"""
from pathlib import Path
import collections
import hashlib
import json
import unicodedata

import pdfplumber
from pypdf import PdfReader

base = Path(__file__).resolve().parent
source = base / 'output/pdf/persas-integral_felipe.pdf'
records = json.loads((base / 'fontes/linhas-extraidas.json').read_text(encoding='utf-8'))


def compact(text):
    return ''.join(unicodedata.normalize('NFC', text).split())


by_text = {compact(r['text'].replace('BREAKLINE', '')): r for r in records}
reader = PdfReader(source)
annotations = []
with pdfplumber.open(source) as pdf:
    for pn, (page, parsed) in enumerate(zip(reader.pages[:8], pdf.pages[:8]), 1):
        greek = [c for c in parsed.chars if 13.8 < c['size'] < 14.1]
        groups = collections.defaultdict(list)
        for c in greek:
            groups[round(c['matrix'][5], 2)].append(c)
        lines = []
        for baseline, chars in groups.items():
            chars.sort(key=lambda c: c['x0'])
            text = ''.join(c['text'] for c in chars)
            record = by_text.get(compact(text))
            if record:
                lines.append({'verse': record['n'], 'text': record['text'], 'chars': chars,
                              'baseline': baseline})
        assert lines, ('No verses mapped', pn)
        for reference in page.get('/Annots', []):
            annotation = reference.get_object()
            subtype = str(annotation.get('/Subtype'))
            if subtype == '/Popup':
                continue
            points = [float(v) for v in annotation.get('/QuadPoints', [])]
            quads = []
            for start in range(0, len(points), 8):
                quad = points[start:start + 8]
                quads.append((min(quad[0::2]), parsed.height - max(quad[1::2]),
                              max(quad[0::2]), parsed.height - min(quad[1::2])))
            if not quads:
                x0, y0, x1, y1 = map(float, annotation['/Rect'])
                quads = [(x0, parsed.height - y1, x1, parsed.height - y0)]

            def selected(c):
                x = (c['x0'] + c['x1']) / 2
                y = (c['top'] + c['bottom']) / 2
                return any(x0 <= x <= x1 and top <= y <= bottom
                           for x0, top, x1, bottom in quads)

            chars = [c for c in parsed.chars if selected(c)]
            selected_lines = collections.defaultdict(list)
            for c in chars:
                selected_lines[round(c['matrix'][5], 2)].append(c)
            fragments = []
            for baseline in sorted(selected_lines, reverse=True):
                row = sorted(selected_lines[baseline], key=lambda c: c['x0'])
                fragments.append(''.join(c['text'] for c in row).strip())
            segments = []
            for line in sorted(lines, key=lambda line: line['verse']):
                marked = ''.join(c['text'] for c in line['chars'] if selected(c)).strip()
                if marked:
                    segments.append({'verse': line['verse'], 'marked': marked, 'text': line['text']})
            comment = str(annotation.get('/Contents', '')).strip()
            action = 'incluir_ou_ampliar' if segments else 'excluir'
            if 'Qual é o sentido' in comment:
                action = 'conferir_remissao_e_sentido'
            elif 'subjuntivo e optativo' in comment:
                action = 'explicar_valor_da_construcao'
            if subtype == '/StrikeOut':
                action = 'excluir'
            annotations.append({'id': len(annotations) + 1, 'page': pn,
                                'subtype': subtype, 'comment': comment,
                                'selected_text': '\n'.join(fragments),
                                'verse_segments': segments, 'quads_top_left': quads,
                                'action': action, 'status': 'registrado_para_revisao'})

assert len(annotations) == 123
special = next(a for a in annotations if a['action'] == 'conferir_remissao_e_sentido')
special['editorial_check'] = {
    'previous_printed_gloss': {'verse': 29, 'page': 2, 'meaning': 'combatente a cavalo'},
    'current_verse': 105,
    'problem': 'A análise nominal no nominativo singular confunde dois empregos do lema.',
    'required_revision': 'adj., ac. pl. masc., concordando com κλόνους; de combate a cavalo',
    'evidence': 'fontes/estudo-lexical/lsj-target.json: ἱππιοχάρμης, II',
}
result = {'source': str(source), 'sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
          'reviewed_pages': [1, 8], 'reviewed_verses': [1, 158],
          'annotation_count': len(annotations),
          'action_counts': dict(collections.Counter(a['action'] for a in annotations)),
          'note': 'Marcações registradas; este arquivo não modifica o PDF nem as notas compostas.',
          'annotations': annotations}
destination = base / 'revisoes/felipe-2026-10-10.json'
destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({k: v for k, v in result.items() if k != 'annotations'}, ensure_ascii=False))
