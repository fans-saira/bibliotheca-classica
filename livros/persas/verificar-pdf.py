"""Verify complete text, page ranges and geometry; build visual QA sheets."""
from pathlib import Path
import json
import re
import sys
import unicodedata
import pdfplumber
from convencoes import entries
from PIL import Image, ImageDraw

base = Path(__file__).resolve().parent
build = Path(sys.argv[1])
records = json.loads((base / 'fontes/linhas-extraidas.json').read_text(encoding='utf-8'))
notes = json.loads((base/'notas.json').read_text(encoding='utf-8'))
note_checks = []
verse_positions = {}
mm = 72 / 25.4
grid=json.loads((base/'fontes/grid-atual.json').read_text(encoding='utf-8'))
main_width=grid['main_mm']
even_left=grid['outer_mm']+grid['notes_mm']+grid['gap_mm']
odd_margin=grid['inner_mm']+main_width+grid['gap_mm']
transition_verses=set()
transition=False
for line in (base/'texto-integral.tex').read_text(encoding='utf-8').splitlines():
    if line.startswith(('\\falante','\\pausaestrofe','\\parte')):transition=True
    m=re.match(r'\\verso\{(\d+)\}',line)
    if m:
        if transition:transition_verses.add(int(m[1]))
        transition=False
spacing_checks=[]
speaker_labels=[]
def compact(s):
    return re.sub(r'\s+', '', unicodedata.normalize('NFC', s))

body_parts, page_data = [], []
with pdfplumber.open(build / 'persas.pdf') as pdf:
    total_pages=len(pdf.pages)
    appendix_pages=[]
    for n, page in enumerate(pdf.pages, 1):
        left = grid['inner_mm'] if n % 2 else even_left
        crop = page.crop((left*mm, 32*mm, (left+main_width)*mm, 264*mm)).filter(
            lambda obj:obj.get('object_type')!='char' or 13.8<obj['size']<14.1)
        body = crop.extract_text(x_tolerance=1, y_tolerance=2) or ''
        head = page.crop((0, 17*mm, page.width, 27*mm)).extract_text() or ''
        ranges = re.findall(r'(\d+)–(\d+)', head)
        if not ranges:
            text=page.extract_text() or ''
            assert 'PERSAS' in head and 'ÉSQUILO' in head, ('Missing appendix header',n)
            assert all(0 <= c['x0'] < c['x1'] <= page.width+.1 and 0 <= c['top'] < c['bottom'] <= page.height+.1 for c in page.chars),('Clipped appendix',n)
            appendix_pages.append({'page':n,'text':text})
            continue
        assert len(ranges) == 1, (n, head)
        first, last = map(int, ranges[0])
        body_parts.append(compact(body))
        assert abs(page.width-210*mm)<.1 and abs(page.height-297*mm)<.1
        assert all(0 <= c['x0'] < c['x1'] <= page.width + .1
                   and 0 <= c['top'] < c['bottom'] <= page.height + .1
                   for c in page.chars), f'Clipped text on page {n}'
        footer_box = ((odd_margin if n % 2 else 0)*mm, 270*mm,
                      page.width if n % 2 else even_left*mm, 279*mm)
        folio = (page.crop(footer_box).extract_text() or '').strip()
        assert folio == str(n), (n, 'Wrong outer folio', folio)
        page_data.append({'page': n, 'first': first, 'last': last})
        # Read each complete entry in the outer column, then compare its actual
        # PDF baseline with the Greek verse. This also catches overlapping text.
        margin_left = odd_margin if n%2 else grid['outer_mm']
        margin = page.crop((margin_left*mm,32*mm,(margin_left+grid['notes_mm'])*mm,264*mm))
        note_chars=[c for line in margin.extract_text_lines(x_tolerance=1,y_tolerance=2)
                    for c in line['chars'] if not c['text'].isspace()]
        # extract_text expands Latin ligatures once; raw char sequences can
        # contain duplicate fi glyph expansions in pdfplumber.
        note_text=compact(margin.extract_text(x_tolerance=1,y_tolerance=2) or '')
        bold_groups={}
        for c in note_chars:
            if 'Bold' in c['fontname']:
                bold_groups.setdefault(round(c['matrix'][5],2),[]).append(c)
        anchors={compact(''.join(c['text'] for c in sorted(cs,key=lambda c:c['x0']))):cs[0]
                 for cs in bold_groups.values()}
        heights={int(v):float(h)*72/72.27 for v,h in re.findall(r'NOTEHEIGHT\s+> (\d+):([\d.]+)pt',
                 (build/'persas.log').read_text(encoding='utf-8'))}
        all_note_chars=[c for c in page.chars if 32*mm<=c['top']<=264*mm and 8.8<c['size']<9.1]
        assert all(margin_left*mm-.1<=c['x0'] and c['x1']<=(margin_left+grid['notes_mm'])*mm+.1
                   for c in all_note_chars), ('Text outside marginal column',n)
        body_chars=[c for line in crop.extract_text_lines(x_tolerance=1,y_tolerance=2)
                    for c in line['chars'] if not c['text'].isspace()]
        main_text=compact(''.join(c['text'] for c in body_chars))
        labels=page.crop((left*mm,32*mm,(left+main_width)*mm,264*mm)).filter(
            lambda c:c.get('object_type')!='char' or 9.8<c['size']<10.1)
        for label in labels.extract_text_lines():
            text=label['text'].strip()
            assert text==text.upper() and not any('A'<=c<='Z' for c in text),('Wrong speaker label',n,text)
            speaker_labels.append(text)
        last_bottom=None
        body_cursor=0
        for record in records:
            key=str(record['n'])
            if not first<=record['n']<=last:continue
            verse_needle=compact(record['text'].replace('BREAKLINE',''))
            verse_at=main_text.find(verse_needle,body_cursor)
            assert verse_at>=0,(n,key)
            body_cursor=verse_at+len(verse_needle)
            vc=body_chars[verse_at]
            verse_chars=body_chars[verse_at:verse_at+len(verse_needle)]
            assert len({round(c['matrix'][5],2) for c in verse_chars})==1,('Verse wrapped',n,key)
            assert all(left*mm-.1<=c['x0'] and c['x1']<=(left+main_width)*mm+.1 for c in verse_chars),('Verse exceeds column',n,key)
            prev_key=str(records[records.index(record)-1]['n']) if record!=records[0] else None
            if prev_key and prev_key in verse_positions and verse_positions[prev_key]['page']==n and record['n'] not in transition_verses:
                gap=page.height-vc['matrix'][5]-verse_positions[prev_key]['baseline']
                assert abs(gap-grid['leading_pt']*72/72.27)<.15,('Nonuniform Greek spacing',key,gap)
                spacing_checks.append(gap)
            verse_positions[key]={'page':n,'top':vc['top'],'baseline':page.height-vc['matrix'][5]}
            if key not in notes:continue
            group=entries(notes[key])
            entry=group[0]
            group_contents=[]
            for item in group:
                content=item.get('forma_exibida',item['forma'])+' ← '+item['lema']
                if item.get('tipo')=='preposicao':
                    shown_form=item['forma']+(' ← '+item['lema'] if item.get('exibir_lema') else '')
                    content=(shown_form+' + '+item['caso'] if item['posicao']=='preposta'
                             else item['caso']+' + '+item['forma'])+' = '+item['sentido']
                elif item.get('tipo')!='crase':
                    if item['sentido']:content+=' ('+item['sentido']+')'
                    content+='; '+item['analise']
                group_contents.append(content)
            content=' '.join(group_contents)
            needle=compact(content)
            at=note_text.find(needle)
            assert at>=0, ('Missing, clipped or overlapping marginal entry', n, key, needle)
            matching=[cs[0] for cs in bold_groups.values()
                      if compact(''.join(c['text'] for c in sorted(cs,key=lambda c:c['x0'])))==compact(entry.get('forma_exibida',entry['forma']))]
            assert matching,('Marginal anchor missing',n,key)
            start=min(matching,key=lambda c:abs(c['matrix'][5]-body_chars[verse_at]['matrix'][5]))
            delta=abs(start['matrix'][5]-body_chars[verse_at]['matrix'][5])
            assert delta<.15, ('Misaligned marginal entry',n,key,delta)
            if last_bottom is not None:
                assert start['top']-last_bottom>1, ('Marginal collision',n,key)
            last_bottom=start['top']+heights[record['n']]
            note_checks.append({'verse':record['n'],'page':n,'baseline_error_pt':round(delta,3),'entries':len(group)})

cursor_page = 0
cursor = 0
failures = []
verses_by_page = [[] for _ in page_data]
for record in records:
    needle = compact(record['text'].replace('BREAKLINE', ''))
    found = False
    for p in range(cursor_page, len(body_parts)):
        pos = body_parts[p].find(needle, cursor if p == cursor_page else 0)
        if pos >= 0:
            cursor_page, cursor = p, pos+len(needle)
            verses_by_page[p].append(record['n'])
            if not page_data[p]['first'] <= record['n'] <= page_data[p]['last']:
                failures.append({'verse': record['n'], 'page': p+1, 'reason': 'Wrong header range'})
            found = True
            break
    if not found:
        failures.append({'verse': record['n'], 'reason': 'Text not found in sequence', 'text': record['text']})

for i, data in enumerate(page_data):
    assert verses_by_page[i], ('Empty body page', i+1)
    assert (data['first'], data['last']) == (min(verses_by_page[i]), max(verses_by_page[i])), data
    if i:
        assert data['first'] > page_data[i-1]['last'], (i, data)
assert page_data[0]['first']==1 and page_data[-1]['last']==1076
assert len(appendix_pages)==1 and appendix_pages[0]['page']==total_pages, 'Gráfico deve ocupar somente a última página'
assert total_pages==len(page_data)+1, 'Páginas extras após o gráfico'
assert 'O vocabulário' in appendix_pages[0]['text'], 'Gráfico lexical ausente'
with pdfplumber.open(build/'persas.pdf') as clean_pdf:
    end_text=clean_pdf.pages[-1].extract_text() or ''
    assert not any(t in end_text for t in ['Texto grego:', 'Digitalização:', 'Apoio morfológico:', 'Seleção de vocabulário']), 'Créditos retirados reapareceram'
report = {'pages': total_pages, 'reading_pages':len(page_data),'appendix_pages':[p['page'] for p in appendix_pages], 'source_lines': len(records),
          'unwrapped_verses':len(verse_positions),'uniform_spacing_checks':len(spacing_checks),'speaker_labels':speaker_labels,
          'failures': failures, 'page_ranges': page_data,
          'verified_marginal_entries':sum(c['entries'] for c in note_checks),'marginal_checks':note_checks}
assert len(note_checks)==len(notes),(len(note_checks),len(notes))
(build / 'verificacao-integral.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(build / 'posicoes-versos.json').write_text(json.dumps(verse_positions,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

images = sorted(p for p in build.glob('atual-*.png') if int(p.stem.rsplit('-',1)[-1])<=total_pages)
for offset in range(0, len(images), 12):
    sheet = Image.new('RGB', (1200, 1320), 'white')
    draw = ImageDraw.Draw(sheet)
    for j, file in enumerate(images[offset:offset+12]):
        im = Image.open(file).convert('RGB')
        im.thumbnail((280, 396))
        x, y = (j % 4)*300+10, (j//4)*440+25
        sheet.paste(im,(x,y))
        draw.text((x,y-20),str(offset+j+1),fill='black')
    sheet.save(build / f'contato-{offset//12+1}.png')
print(json.dumps({'pages':total_pages,'reading_pages':len(page_data),'verified_source_lines':len(records)-len(failures),
                  'verified_marginal_entries':report['verified_marginal_entries'],'failures':failures},ensure_ascii=False))
if failures:
    sys.exit(1)
