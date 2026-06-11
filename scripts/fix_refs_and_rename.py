"""
Two tasks:
1. Wrap bare URLs in <section id="referencias"> with <a> hyperlinks
2. Rename "modulo X" folders → "modulo-X" and fix DSM-V.pdf → dsm-v.pdf
"""
import re
import os
from pathlib import Path

BASE = Path(r"c:\Users\AparicioJunior\workspace\saude-caminhoneiros")

# ─── Task 1: add hyperlinks to referencias ───────────────────────────────────

URL_RE = re.compile(
    r'(?<!["\'])'                      # not inside an existing href/src
    r'(https?://\S+|www\.\S+)',        # http/https or www URLs
    re.IGNORECASE
)

def clean_href(url: str) -> str:
    """Strip trailing punctuation and add https:// if needed."""
    # Remove trailing sentence punctuation (. , ; )
    cleaned = url.rstrip('.,;)')
    if cleaned.lower().startswith('www.'):
        cleaned = 'https://' + cleaned
    return cleaned


def linkify_referencias(content: str, mod_label: str) -> str:
    """
    Within <section id="referencias">...</section>, replace bare URLs with
    <a href="..." target="_blank" rel="noopener noreferrer">...</a>.
    Skips URLs that are already inside an href or src attribute.
    """
    sec_start = content.find('<section id="referencias"')
    if sec_start == -1:
        print(f"  {mod_label}: references section not found")
        return content

    # Find closing </section> for this block (depth tracking)
    depth = 0
    sec_end = None
    for m in re.finditer(r'<(/?section)\b', content[sec_start:]):
        if not m.group(1).startswith('/'):
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                sec_end = sec_start + m.end()
                break

    if sec_end is None:
        print(f"  {mod_label}: could not find closing </section>")
        return content

    section_html = content[sec_start:sec_end]

    def replace_url(match):
        url = match.group(1)
        # Skip if already preceded by href=" or src="
        start = match.start()
        preceding = section_html[max(0, start - 8):start]
        if 'href=' in preceding or 'src=' in preceding:
            return url
        href = clean_href(url)
        return f'<a href="{href}" target="_blank" rel="noopener noreferrer">{url}</a>'

    new_section = URL_RE.sub(replace_url, section_html)
    changed = new_section.count('<a href=') - section_html.count('<a href=')
    print(f"  {mod_label}: {changed} URL(s) linked")

    return content[:sec_start] + new_section + content[sec_end:]


for mod_num in range(1, 6):
    path = BASE / f"modulo {mod_num}" / "index.html"
    original = path.read_text(encoding="utf-8")
    fixed = linkify_referencias(original, f"M{mod_num}")
    if fixed != original:
        path.write_text(fixed, encoding="utf-8")


# ─── Task 2: rename files with uppercase ──────────────────────────────────────

# Rename DSM-V.pdf → dsm-v.pdf in modulo 3
dsm_old = BASE / "modulo 3" / "media" / "DSM-V.pdf"
dsm_new = BASE / "modulo 3" / "media" / "dsm-v.pdf"
if dsm_old.exists():
    dsm_old.rename(dsm_new)
    print(f"\nRenamed: DSM-V.pdf → dsm-v.pdf")
else:
    print(f"\nDSM-V.pdf already renamed or not found")


# ─── Task 3: rename "modulo X" folders → "modulo-X" ──────────────────────────

print()
for mod_num in range(1, 6):
    old_path = BASE / f"modulo {mod_num}"
    new_path = BASE / f"modulo-{mod_num}"
    if old_path.exists():
        old_path.rename(new_path)
        print(f"Renamed: 'modulo {mod_num}' → 'modulo-{mod_num}'")
    elif new_path.exists():
        print(f"'modulo-{mod_num}' already exists")
    else:
        print(f"WARNING: neither 'modulo {mod_num}' nor 'modulo-{mod_num}' found")


# ─── Verify ──────────────────────────────────────────────────────────────────

print("\n=== Verification ===")
for mod_num in range(1, 6):
    path = BASE / f"modulo-{mod_num}" / "index.html"
    if not path.exists():
        print(f"modulo-{mod_num}: MISSING index.html")
        continue
    c = path.read_text(encoding="utf-8")
    refs_links = c.count('href=', c.find('<section id="referencias"'))
    # Count only within referencias section
    sec_start = c.find('<section id="referencias"')
    sec_end = c.find('</section>', sec_start) + len('</section>')
    links_in_refs = c[sec_start:sec_end].count('<a href=')
    print(f"modulo-{mod_num}: OK — {links_in_refs} hyperlinks in referencias")

print("\nDone.")
