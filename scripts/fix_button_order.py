"""
Fix backToTop button ordering in all modules.

Bug: buttons (backToTop, sidebar-toggle, sidebarOverlay) were placed AFTER the
<script> tags. scripts.min.js runs `const _btt = document.getElementById("backToTop")`
at load time — before the button is in the DOM — so _btt is null and the scroll
handler never fires.

Fix: move the mobile elements block to BEFORE the <script> tags.
"""
from pathlib import Path
import re

BASE = Path(r"c:\Users\AparicioJunior\workspace\saude-caminhoneiros")

def swap_buttons_before_scripts(content: str, label: str) -> str:
    """
    Find the two-script block (lucide + scripts.min.js), the mobile-elements
    block that follows, and swap their order.
    Returns modified content (or original if structure not found).
    """
    lines = content.split('\n')

    lucide_idx = next(
        (i for i, l in enumerate(lines) if 'unpkg.com/lucide' in l),
        None
    )
    if lucide_idx is None:
        print(f"  {label}: WARNING — lucide script not found")
        return content

    scripts_idx = next(
        (i for i in range(lucide_idx, min(lucide_idx + 5, len(lines)))
         if 'scripts.min.js' in lines[i]),
        None
    )
    if scripts_idx is None:
        print(f"  {label}: WARNING — scripts.min.js not found near lucide")
        return content

    script_block = lines[lucide_idx:scripts_idx + 1]

    body_idx = next(
        (i for i in range(scripts_idx + 1, len(lines)) if lines[i].strip() == '</body>'),
        None
    )
    if body_idx is None:
        print(f"  {label}: WARNING — </body> not found after scripts")
        return content

    mobile_block = lines[scripts_idx + 1: body_idx]

    while mobile_block and mobile_block[0].strip() == '':
        mobile_block = mobile_block[1:]

    if not mobile_block:
        print(f"  {label}: nothing between scripts and </body> — skipping")
        return content

    if 'backToTop' not in '\n'.join(mobile_block):
        print(f"  {label}: WARNING — backToTop not in mobile block — skipping")
        return content

    before = lines[:lucide_idx]
    after  = lines[body_idx:]

    new_lines = before + mobile_block + [''] + script_block + [''] + after
    print(f"  {label}: swapped OK (backToTop at line {lucide_idx+1}, now before scripts)")
    return '\n'.join(new_lines)

for mod_num in [1, 2, 3, 5]:
    label = f"M{mod_num}"
    path = BASE / f"modulo {mod_num}" / "index.html"
    original = path.read_text(encoding="utf-8")
    fixed = swap_buttons_before_scripts(original, label)
    if fixed != original:
        path.write_text(fixed, encoding="utf-8")
    else:
        print(f"  {label}: no change")

print("\nFixing M4...")

path4 = BASE / "modulo 4" / "index.html"
c4 = path4.read_text(encoding="utf-8")
lines4 = c4.split('\n')

first_body = next((i for i, l in enumerate(lines4) if l.strip() == '</body>'), None)
first_html  = next((i for i, l in enumerate(lines4) if l.strip() == '</html>'), None)

print(f"  First </body> at line {first_body+1}, first </html> at line {first_html+1}")

dica2_start = next(
    (i for i in range(first_html + 1, len(lines4))
     if 'id="modalDica2"' in lines4[i]),
    None
)
modal_dica2_lines = []
if dica2_start is not None:

    overlay_start = next(
        (i for i in range(dica2_start, -1, -1) if '<div class="overlay"' in lines4[i]),
        dica2_start
    )

    depth = 0
    overlay_end = None
    for i in range(overlay_start, len(lines4)):
        opens  = lines4[i].count('<div')
        closes = lines4[i].count('</div>')
        depth += opens - closes
        if depth <= 0 and i > overlay_start:
            overlay_end = i
            break
    if overlay_end:

        comment_line = overlay_start - 1
        if comment_line >= 0 and '<!-- MODAL' in lines4[comment_line]:
            overlay_start = comment_line
        modal_dica2_lines = lines4[overlay_start:overlay_end + 1]
        print(f"  modalDica2: lines {overlay_start+1}–{overlay_end+1} ({len(modal_dica2_lines)} lines)")
    else:
        print("  WARNING: modalDica2 closing </div> not found")
else:
    print("  WARNING: modalDica2 not found outside </html>")

c4_clean_lines = lines4[:first_body]

while c4_clean_lines and c4_clean_lines[-1].strip() == '':
    c4_clean_lines.pop()

lucide_idx4 = next(
    (i for i, l in enumerate(c4_clean_lines) if 'unpkg.com/lucide' in l),
    None
)

insert_before = lucide_idx4
if insert_before and insert_before > 0 and '<!--' in c4_clean_lines[insert_before - 1]:
    insert_before -= 1

if modal_dica2_lines and insert_before is not None:
    c4_clean_lines = (c4_clean_lines[:insert_before]
                      + ['']
                      + modal_dica2_lines
                      + ['']
                      + c4_clean_lines[insert_before:])
    print("  modalDica2 inserted before scripts")

c4_fixed = swap_buttons_before_scripts('\n'.join(c4_clean_lines), 'M4')
c4_fixed = c4_fixed.rstrip() + '\n\n</body>\n</html>\n'

path4.write_text(c4_fixed, encoding="utf-8")

btt_pos    = c4_fixed.find('id="backToTop"')
lucide_pos = c4_fixed.find('unpkg.com/lucide')
body_count = c4_fixed.count('</body>')
html_count = c4_fixed.count('</html>')
dica2_count = c4_fixed.count('id="modalDica2"')

print(f"\nM4 verification:")
print(f"  backToTop before lucide: {btt_pos < lucide_pos} (btt={btt_pos}, lucide={lucide_pos})")
print(f"  </body>: {body_count}, </html>: {html_count}")
print(f"  modalDica2: {dica2_count}")
print(f"  Total lines: {c4_fixed.count(chr(10))+1}")

print("\n=== Final verification all modules ===")
for mod_num in [1, 2, 3, 4, 5]:
    path = BASE / f"modulo {mod_num}" / "index.html"
    c = path.read_text(encoding="utf-8")
    btt   = c.find('id="backToTop"')
    luc   = c.find('unpkg.com/lucide')
    ok    = 'OK' if 0 <= btt < luc else 'FAIL'
    lines = c.count('\n') + 1
    print(f"  M{mod_num}: {ok}  btt={btt} lucide={luc}  lines={lines}")
