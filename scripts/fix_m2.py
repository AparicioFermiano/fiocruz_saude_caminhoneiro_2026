"""
Fix M2: strip everything from the first Lucide script tag onward and close cleanly.
All JS is already in scripts.min.js — no inline <script> block needed.
Then re-apply mobile elements (back-to-top, sidebar-toggle, sidebarOverlay).
"""
from pathlib import Path

BASE = Path(r"c:\Users\AparicioJunior\workspace\saude-caminhoneiros")
path = BASE / "modulo 2" / "index.html"

content = path.read_text(encoding="utf-8")
print(f"Original: {len(content)} chars, {content.count(chr(10))+1} lines")

LUCIDE_TAG = '  <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>'

cut = content.find(LUCIDE_TAG)
if cut == -1:
    print("ERROR: Lucide script tag not found")
    exit(1)

print(f"Cutting at char {cut} (line ~{content[:cut].count(chr(10))+1})")

clean = content[:cut].rstrip()

# Ensure main is closed before the modals close properly
# The clean body content should end with </div> (closing the page-layout div)
print(f"Last 200 chars of clean body:\n{clean[-200:]!r}")

CLOSING = """
  <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>
  <script src="js/scripts.min.js"></script>

  <!-- Botão voltar ao topo -->
  <button id="backToTop" class="back-to-top" onclick="window.scrollTo({top:0,behavior:'smooth'})" aria-label="Voltar ao topo" style="background:var(--m2-primary);color:#fff">
    <i data-lucide="chevron-up"></i>
  </button>

  <!-- Sidebar toggle (hambúrguer — visível apenas no mobile) -->
  <button class="sidebar-toggle" onclick="openSidebar()" aria-label="Abrir menu de navegação" style="background:var(--m2-primary);color:#fff">
    <i data-lucide="menu"></i>
  </button>

  <!-- Overlay da sidebar (mobile) -->
  <div id="sidebarOverlay" class="sidebar-overlay" onclick="closeSidebar()"></div>

</body>
</html>"""

result = clean + CLOSING
path.write_text(result, encoding="utf-8")
print(f"\nSaved: {len(result)} chars, {result.count(chr(10))+1} lines")
print(f"</body> count: {result.count('</body>')}")
print(f"Has backToTop: {'id=\"backToTop\"' in result}")
print(f"Has sidebarOverlay: {'id=\"sidebarOverlay\"' in result}")
print(f"Has sidebar-toggle: {'sidebar-toggle' in result}")
