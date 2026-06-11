"""
Apply pending modifications to all modules:
1. M2: Add encerramento + Material de Apoio (missing)
2. All modules: Add back-to-top button, sidebar-toggle (hamburger), sidebar-overlay div
"""
import re
from pathlib import Path

BASE = Path(r"c:\Users\AparicioJunior\workspace\saude-caminhoneiros")

MODULES = {
    1: {"var": "m1", "on": "var(--m1-on-primary)"},
    2: {"var": "m2", "on": "#fff"},
    3: {"var": "m3", "on": "#fff"},
    4: {"var": "m4", "on": "#fff"},
    5: {"var": "m5", "on": "#fff"},
}

# ─── M2: Encerramento + Material de Apoio ────────────────────────────────────

M2_ENCERRAMENTO_BLOCK = '''
      <!-- ═══ ENCERRAMENTO ═══ -->
      <section id="encerramento" class="block" style="scroll-margin-top:80px;margin-bottom:2rem">
        <h2 class="block-title" style="color:var(--m2-primary-deep);margin-bottom:1.5rem">Encerramento do Módulo</h2>
        <div class="encerramento-card" style="background:var(--grad-m2-brand);color:#fff">
          <p>Ao longo deste módulo, você aprofundou seus conhecimentos sobre as Infecções Sexualmente Transmissíveis mais prevalentes no contexto do trabalho das caminhoneiras e dos caminhoneiros.</p>
          <p>Refletiu sobre os fatores de vulnerabilidade, as estratégias de prevenção combinada, o processo de testagem rápida para sífilis, gonorreia, clamídia e HIV, e as abordagens de manejo disponíveis na Atenção Primária à Saúde.</p>
          <p style="margin:0">Esperamos que este módulo tenha contribuído para uma prática clínica mais sensível e efetiva, reconhecendo as especificidades dessa população e fortalecendo o acesso ao cuidado integral em saúde sexual.</p>
        </div>
      </section>

      <!-- ═══ MATERIAL DE APOIO ═══ -->
      <section class="block" style="margin-bottom:2rem">
        <h2 class="block-title" style="color:var(--m2-primary-deep);margin-bottom:1.5rem">Material de Apoio</h2>
        <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:1rem;">
          <a href="media/pcdt_prep_hiv.pdf" download class="pdf-card" style="display:flex;align-items:center;gap:.75rem;padding:1rem 1.25rem;background:var(--bg-soft);border-radius:var(--r-sm);border:1px solid var(--brd);text-decoration:none;color:var(--fg1);">
            <i data-lucide="file-down" style="flex-shrink:0;color:var(--m2-primary);width:24px;height:24px;"></i>
            <span style="font-size:.9rem;line-height:1.4;">PCDT para Profilaxia Pré-Exposição (PrEP) ao HIV</span>
          </a>
          <a href="media/calendario_vacinacao_2026.pdf" download class="pdf-card" style="display:flex;align-items:center;gap:.75rem;padding:1rem 1.25rem;background:var(--bg-soft);border-radius:var(--r-sm);border:1px solid var(--brd);text-decoration:none;color:var(--fg1);">
            <i data-lucide="file-down" style="flex-shrink:0;color:var(--m2-primary);width:24px;height:24px;"></i>
            <span style="font-size:.9rem;line-height:1.4;">Calendário Nacional de Vacinação 2026</span>
          </a>
          <a href="media/pcdt_ist_2022.pdf" download class="pdf-card" style="display:flex;align-items:center;gap:.75rem;padding:1rem 1.25rem;background:var(--bg-soft);border-radius:var(--r-sm);border:1px solid var(--brd);text-decoration:none;color:var(--fg1);">
            <i data-lucide="file-down" style="flex-shrink:0;color:var(--m2-primary);width:24px;height:24px;"></i>
            <span style="font-size:.9rem;line-height:1.4;">PCDT para Atenção Integral às Pessoas com IST (2022)</span>
          </a>
          <a href="media/pcdt_pep_hiv_2021.pdf" download class="pdf-card" style="display:flex;align-items:center;gap:.75rem;padding:1rem 1.25rem;background:var(--bg-soft);border-radius:var(--r-sm);border:1px solid var(--brd);text-decoration:none;color:var(--fg1);">
            <i data-lucide="file-down" style="flex-shrink:0;color:var(--m2-primary);width:24px;height:24px;"></i>
            <span style="font-size:.9rem;line-height:1.4;">PCDT para Profilaxia Pós-Exposição (PEP) ao HIV, IST e Hepatites Virais</span>
          </a>
          <a href="media/rowley_chlamydia_gonorrhea_BLT.pdf" download class="pdf-card" style="display:flex;align-items:center;gap:.75rem;padding:1rem 1.25rem;background:var(--bg-soft);border-radius:var(--r-sm);border:1px solid var(--brd);text-decoration:none;color:var(--fg1);">
            <i data-lucide="file-down" style="flex-shrink:0;color:var(--m2-primary);width:24px;height:24px;"></i>
            <span style="font-size:.9rem;line-height:1.4;">Chlamydia, gonorrhea, trichomoniasis and syphilis: global prevalence (Rowley et al.)</span>
          </a>
          <a href="media/manual_imunobiologicos_6ed.pdf" download class="pdf-card" style="display:flex;align-items:center;gap:.75rem;padding:1rem 1.25rem;background:var(--bg-soft);border-radius:var(--r-sm);border:1px solid var(--brd);text-decoration:none;color:var(--fg1);">
            <i data-lucide="file-down" style="flex-shrink:0;color:var(--m2-primary);width:24px;height:24px;"></i>
            <span style="font-size:.9rem;line-height:1.4;">Manual dos Centros de Referência para Imunobiológicos Especiais (6ª ed.)</span>
          </a>
          <a href="media/guia_vigilancia_saude.pdf" download class="pdf-card" style="display:flex;align-items:center;gap:.75rem;padding:1rem 1.25rem;background:var(--bg-soft);border-radius:var(--r-sm);border:1px solid var(--brd);text-decoration:none;color:var(--fg1);">
            <i data-lucide="file-down" style="flex-shrink:0;color:var(--m2-primary);width:24px;height:24px;"></i>
            <span style="font-size:.9rem;line-height:1.4;">Guia de Vigilância em Saúde — Ministério da Saúde</span>
          </a>
          <a href="media/pcdt_hiv_modulo1_2024.pdf" download class="pdf-card" style="display:flex;align-items:center;gap:.75rem;padding:1rem 1.25rem;background:var(--bg-soft);border-radius:var(--r-sm);border:1px solid var(--brd);text-decoration:none;color:var(--fg1);">
            <i data-lucide="file-down" style="flex-shrink:0;color:var(--m2-primary);width:24px;height:24px;"></i>
            <span style="font-size:.9rem;line-height:1.4;">PCDT para Manejo da Infecção pelo HIV em Adultos — Módulo 1 (2024)</span>
          </a>
          <a href="media/sei_nota_distribuicao_preservativos.pdf" download class="pdf-card" style="display:flex;align-items:center;gap:.75rem;padding:1rem 1.25rem;background:var(--bg-soft);border-radius:var(--r-sm);border:1px solid var(--brd);text-decoration:none;color:var(--fg1);">
            <i data-lucide="file-down" style="flex-shrink:0;color:var(--m2-primary);width:24px;height:24px;"></i>
            <span style="font-size:.9rem;line-height:1.4;">Nota Técnica SEI — Distribuição de Preservativos e Insumos de Prevenção</span>
          </a>
        </div>
      </section>'''


def mobile_elements(mod_num):
    m = MODULES[mod_num]
    var = m["var"]
    on = m["on"]
    return f'''
  <!-- Botão voltar ao topo -->
  <button id="backToTop" class="back-to-top" onclick="window.scrollTo({{top:0,behavior:'smooth'}})" aria-label="Voltar ao topo" style="background:var(--{var}-primary);color:{on}">
    <i data-lucide="chevron-up"></i>
  </button>

  <!-- Sidebar toggle (hambúrguer — visível apenas no mobile) -->
  <button class="sidebar-toggle" onclick="openSidebar()" aria-label="Abrir menu de navegação" style="background:var(--{var}-primary);color:{on}">
    <i data-lucide="menu"></i>
  </button>

  <!-- Overlay da sidebar (mobile) -->
  <div id="sidebarOverlay" class="sidebar-overlay" onclick="closeSidebar()"></div>

'''


def apply_to_module(mod_num, path):
    content = path.read_text(encoding='utf-8')
    original_len = len(content)
    changes = []

    # ── 1. M2 only: add encerramento before </main> ──────────────────────────
    if mod_num == 2 and 'id="encerramento"' not in content:
        # Find the last </section> before </main>
        # Unique: the Saiba mais section closes then </main>
        old = '      </section>\n\n    </main>\n  </div>\n\n  <!-- MODAL SOBREPOSTO (REFLEXÃO) -->'
        if old in content:
            new = M2_ENCERRAMENTO_BLOCK + '\n\n    </main>\n  </div>\n\n  <!-- MODAL SOBREPOSTO (REFLEXÃO) -->'
            content = content.replace(old, new, 1)
            changes.append('M2 encerramento + Material de Apoio added')
        else:
            changes.append('M2 encerramento: old_string NOT FOUND')

    # ── 2. All modules: add mobile elements (back-to-top, toggle, overlay) ───
    if 'id="backToTop"' not in content:
        elements = mobile_elements(mod_num)
        # Insert BEFORE </body>
        if '</body>' in content:
            content = content.replace('</body>', elements + '</body>', 1)
            changes.append('Mobile elements (back-to-top, sidebar-toggle, overlay) added')
        else:
            changes.append('Mobile elements: </body> NOT FOUND')

    if changes:
        path.write_text(content, encoding='utf-8')
        print(f"M{mod_num}: {len(content)} chars ({len(content)-original_len:+d})")
        for c in changes:
            print(f"  OK: {c}")
    else:
        print(f"M{mod_num}: no changes needed ({len(content)} chars)")


for mod_num in range(1, 6):
    path = BASE / f"modulo {mod_num}" / "index.html"
    if not path.exists():
        print(f"M{mod_num}: FILE NOT FOUND")
        continue
    apply_to_module(mod_num, path)

print("\nDone. Verifying...")
for mod_num in range(1, 6):
    path = BASE / f"modulo {mod_num}" / "index.html"
    content = path.read_text(encoding='utf-8')
    has_enc = 'id="encerramento"' in content
    has_btt = 'id="backToTop"' in content
    has_sov = 'id="sidebarOverlay"' in content
    has_stg = 'sidebar-toggle' in content
    print(f"M{mod_num}: encerramento={has_enc}, back-to-top={has_btt}, overlay={has_sov}, toggle={has_stg}")
