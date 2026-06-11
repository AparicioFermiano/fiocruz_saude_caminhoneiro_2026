"""
Remove the standalone "Material de Apoio" section from all modules.
The DI only uses "Saiba Mais" callouts embedded in content sections —
there is no dedicated Material de Apoio block in any DI document.
"""
import re
from pathlib import Path

BASE = Path(r"c:\Users\AparicioJunior\workspace\saude-caminhoneiros")

for mod_num in range(1, 6):
    path = BASE / f"modulo {mod_num}" / "index.html"
    content = path.read_text(encoding="utf-8")
    original_len = len(content)

    # Find the start of the Material de Apoio block (comment marker)
    marker = "<!-- ═══ MATERIAL DE APOIO ═══ -->"
    start = content.find(marker)
    if start == -1:
        print(f"M{mod_num}: no Material de Apoio marker found, skipping")
        continue

    # The block ends at the </section> that closes the <section> opened right after the marker.
    # Walk forward from start to find the opening <section> tag, then track depth to find its close.
    after_marker = content[start:]

    # Find the <section ... > opening tag
    sec_open = re.search(r'<section\b', after_marker)
    if not sec_open:
        print(f"M{mod_num}: could not find <section> after marker")
        continue

    # Track nesting depth starting from that <section>
    scan = after_marker[sec_open.start():]
    depth = 0
    pos = 0
    end_rel = None
    for m in re.finditer(r'<(/?section)\b', scan):
        tag = m.group(1)
        if not tag.startswith('/'):
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                end_rel = m.end()  # position right after </section>
                break

    if end_rel is None:
        print(f"M{mod_num}: could not find closing </section>")
        continue

    # Absolute end position in original content
    block_start = start          # include the comment line
    block_end = start + sec_open.start() + end_rel

    # Also eat any leading newline/whitespace before the comment
    while block_start > 0 and content[block_start - 1] == '\n':
        block_start -= 1

    removed = content[block_start:block_end]
    content = content[:block_start] + content[block_end:]

    path.write_text(content, encoding="utf-8")
    removed_lines = removed.count('\n')
    print(f"M{mod_num}: removed {removed_lines} lines ({original_len - len(content):+d} chars)")
    print(f"  Removed block preview: {repr(removed.strip()[:60]).encode('ascii','replace').decode()}")

print("\nVerifying — 'Material de Apoio' should not appear in any module:")
for mod_num in range(1, 6):
    path = BASE / f"modulo {mod_num}" / "index.html"
    c = path.read_text(encoding="utf-8")
    found = "Material de Apoio" in c or "MATERIAL DE APOIO" in c
    lines = c.count('\n') + 1
    print(f"  M{mod_num}: {lines} lines — Material de Apoio present: {found}")
