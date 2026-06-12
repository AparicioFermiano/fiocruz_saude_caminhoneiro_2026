"""
Two tasks:
1. Redesign M2 vulnerability section with responsive interactive tooltip grid
2. Update course name everywhere: add "do" and apply consistent naming
"""
import re
from pathlib import Path

BASE = Path(r"c:\Users\AparicioJunior\workspace\saude-caminhoneiros")

# ─── 1. M2: Replace vuln section ─────────────────────────────────────────────

NEW_VULN = '''      <!-- BLOCO: Fatores de vulnerabilidade -->
      <section id="s2-2" class="block" style="scroll-margin-top:80px;margin-bottom:4rem;">
        <h2 class="block-title" style="margin-bottom:2rem;font-size:1.7rem;color:var(--m2-primary-deep);">Fatores de vulnerabilidade das pessoas caminhoneiras</h2>
        <div style="display:flex;justify-content:center;margin-bottom:1.75rem">
          <div style="background:var(--grad-m2-brand);color:#fff;padding:.75rem 2.5rem;border-radius:999px;font-family:var(--font-display);font-weight:800;font-size:.92rem;letter-spacing:.07em;text-transform:uppercase;box-shadow:0 4px 20px rgba(63,86,166,.3)">PESSOAS CAMINHONEIRAS</div>
        </div>
        <p style="text-align:center;font-size:.82rem;color:var(--fg3);margin-bottom:1.25rem;margin-top:-.5rem">Clique em cada fator para saber mais</p>
        <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:1rem">

          <div style="position:relative">
            <button onclick="toggleVuln(this,'vf-1')" style="width:100%;display:flex;align-items:center;gap:.75rem;padding:.8rem 1rem;background:var(--card);border:2px solid #e2e8f0;border-radius:var(--r-md);cursor:pointer;text-align:left;box-shadow:var(--sh-sm);transition:border-color .2s">
              <span style="background:#DE6847;color:#fff;border-radius:50%;min-width:1.75rem;height:1.75rem;display:inline-flex;align-items:center;justify-content:center;font-size:.72rem;font-weight:800;flex-shrink:0">1</span>
              <span style="font-size:.88rem;color:var(--fg1);line-height:1.4;flex:1;font-weight:600">M&#xFA;ltiplos parceiros sexuais</span>
              <i data-lucide="info" style="width:.9rem;height:.9rem;flex-shrink:0;color:#94a3b8"></i>
            </button>
            <div id="vf-1" style="display:none;position:absolute;top:calc(100% + 6px);left:0;right:0;background:#fff;border:1.5px solid #e2e8f0;border-radius:var(--r-md);padding:.9rem 1rem 1rem;box-shadow:0 8px 28px rgba(0,0,0,.13);z-index:40;font-size:.84rem;color:var(--fg2);line-height:1.65">
              <button onclick="closeVuln('vf-1')" style="float:right;margin:-.1rem -.2rem .3rem .5rem;background:none;border:none;cursor:pointer;color:#94a3b8;padding:.15rem"><i data-lucide="x" style="width:.8rem;height:.8rem"></i></button>
              A mobilidade profissional e os longos per&#xED;odos afastados de casa aumentam as chances de rela&#xE7;&#xF5;es com parceiros eventuais, elevando significativamente o risco de ISTs.
            </div>
          </div>

          <div style="position:relative">
            <button onclick="toggleVuln(this,'vf-2')" style="width:100%;display:flex;align-items:center;gap:.75rem;padding:.8rem 1rem;background:var(--card);border:2px solid #e2e8f0;border-radius:var(--r-md);cursor:pointer;text-align:left;box-shadow:var(--sh-sm);transition:border-color .2s">
              <span style="background:#C84E5F;color:#fff;border-radius:50%;min-width:1.75rem;height:1.75rem;display:inline-flex;align-items:center;justify-content:center;font-size:.72rem;font-weight:800;flex-shrink:0">2</span>
              <span style="font-size:.88rem;color:var(--fg1);line-height:1.4;flex:1;font-weight:600">Antecedente prisional</span>
              <i data-lucide="info" style="width:.9rem;height:.9rem;flex-shrink:0;color:#94a3b8"></i>
            </button>
            <div id="vf-2" style="display:none;position:absolute;top:calc(100% + 6px);left:0;right:0;background:#fff;border:1.5px solid #e2e8f0;border-radius:var(--r-md);padding:.9rem 1rem 1rem;box-shadow:0 8px 28px rgba(0,0,0,.13);z-index:40;font-size:.84rem;color:var(--fg2);line-height:1.65">
              <button onclick="closeVuln('vf-2')" style="float:right;margin:-.1rem -.2rem .3rem .5rem;background:none;border:none;cursor:pointer;color:#94a3b8;padding:.15rem"><i data-lucide="x" style="width:.8rem;height:.8rem"></i></button>
              A passagem por sistemas prisionais est&#xE1; associada &#xE0; maior exposi&#xE7;&#xE3;o a ISTs, em raz&#xE3;o das condi&#xE7;&#xF5;es de vulnerabilidade social e menor acesso a a&#xE7;&#xF5;es de preven&#xE7;&#xE3;o.
            </div>
          </div>

          <div style="position:relative">
            <button onclick="toggleVuln(this,'vf-3')" style="width:100%;display:flex;align-items:center;gap:.75rem;padding:.8rem 1rem;background:var(--card);border:2px solid #e2e8f0;border-radius:var(--r-md);cursor:pointer;text-align:left;box-shadow:var(--sh-sm);transition:border-color .2s">
              <span style="background:#A35272;color:#fff;border-radius:50%;min-width:1.75rem;height:1.75rem;display:inline-flex;align-items:center;justify-content:center;font-size:.72rem;font-weight:800;flex-shrink:0">3</span>
              <span style="font-size:.88rem;color:var(--fg1);line-height:1.4;flex:1;font-weight:600">Uso irregular de preservativo</span>
              <i data-lucide="info" style="width:.9rem;height:.9rem;flex-shrink:0;color:#94a3b8"></i>
            </button>
            <div id="vf-3" style="display:none;position:absolute;top:calc(100% + 6px);left:0;right:0;background:#fff;border:1.5px solid #e2e8f0;border-radius:var(--r-md);padding:.9rem 1rem 1rem;box-shadow:0 8px 28px rgba(0,0,0,.13);z-index:40;font-size:.84rem;color:var(--fg2);line-height:1.65">
              <button onclick="closeVuln('vf-3')" style="float:right;margin:-.1rem -.2rem .3rem .5rem;background:none;border:none;cursor:pointer;color:#94a3b8;padding:.15rem"><i data-lucide="x" style="width:.8rem;height:.8rem"></i></button>
              A baixa ades&#xE3;o ao uso do preservativo nas rela&#xE7;&#xF5;es espor&#xE1;dicas &#xE9; fator de risco diretamente associado &#xE0; transmiss&#xE3;o de ISTs nessa popula&#xE7;&#xE3;o.
            </div>
          </div>

          <div style="position:relative">
            <button onclick="toggleVuln(this,'vf-4')" style="width:100%;display:flex;align-items:center;gap:.75rem;padding:.8rem 1rem;background:var(--card);border:2px solid #e2e8f0;border-radius:var(--r-md);cursor:pointer;text-align:left;box-shadow:var(--sh-sm);transition:border-color .2s">
              <span style="background:#7F6291;color:#fff;border-radius:50%;min-width:1.75rem;height:1.75rem;display:inline-flex;align-items:center;justify-content:center;font-size:.72rem;font-weight:800;flex-shrink:0">4</span>
              <span style="font-size:.88rem;color:var(--fg1);line-height:1.4;flex:1;font-weight:600">Consumo de &#xE1;lcool/drogas il&#xED;citas</span>
              <i data-lucide="info" style="width:.9rem;height:.9rem;flex-shrink:0;color:#94a3b8"></i>
            </button>
            <div id="vf-4" style="display:none;position:absolute;top:calc(100% + 6px);left:0;right:0;background:#fff;border:1.5px solid #e2e8f0;border-radius:var(--r-md);padding:.9rem 1rem 1rem;box-shadow:0 8px 28px rgba(0,0,0,.13);z-index:40;font-size:.84rem;color:var(--fg2);line-height:1.65">
              <button onclick="closeVuln('vf-4')" style="float:right;margin:-.1rem -.2rem .3rem .5rem;background:none;border:none;cursor:pointer;color:#94a3b8;padding:.15rem"><i data-lucide="x" style="width:.8rem;height:.8rem"></i></button>
              O uso de subst&#xE2;ncias psicoativas prejudica a percep&#xE7;&#xE3;o de risco e a tomada de decis&#xE3;o, levando a comportamentos sexuais de maior risco.
            </div>
          </div>

          <div style="position:relative">
            <button onclick="toggleVuln(this,'vf-5')" style="width:100%;display:flex;align-items:center;gap:.75rem;padding:.8rem 1rem;background:var(--card);border:2px solid #e2e8f0;border-radius:var(--r-md);cursor:pointer;text-align:left;box-shadow:var(--sh-sm);transition:border-color .2s">
              <span style="background:#557497;color:#fff;border-radius:50%;min-width:1.75rem;height:1.75rem;display:inline-flex;align-items:center;justify-content:center;font-size:.72rem;font-weight:800;flex-shrink:0">5</span>
              <span style="font-size:.88rem;color:var(--fg1);line-height:1.4;flex:1;font-weight:600">Baixa percep&#xE7;&#xE3;o de vulnerabilidade &#xE0;s ISTs</span>
              <i data-lucide="info" style="width:.9rem;height:.9rem;flex-shrink:0;color:#94a3b8"></i>
            </button>
            <div id="vf-5" style="display:none;position:absolute;top:calc(100% + 6px);left:0;right:0;background:#fff;border:1.5px solid #e2e8f0;border-radius:var(--r-md);padding:.9rem 1rem 1rem;box-shadow:0 8px 28px rgba(0,0,0,.13);z-index:40;font-size:.84rem;color:var(--fg2);line-height:1.65">
              <button onclick="closeVuln('vf-5')" style="float:right;margin:-.1rem -.2rem .3rem .5rem;background:none;border:none;cursor:pointer;color:#94a3b8;padding:.15rem"><i data-lucide="x" style="width:.8rem;height:.8rem"></i></button>
              Muitos caminhoneiros n&#xE3;o se reconhecem como grupo vulner&#xE1;vel, o que reduz a procura espont&#xE2;nea por servi&#xE7;os de testagem e preven&#xE7;&#xE3;o.
            </div>
          </div>

          <div style="position:relative">
            <button onclick="toggleVuln(this,'vf-6')" style="width:100%;display:flex;align-items:center;gap:.75rem;padding:.8rem 1rem;background:var(--card);border:2px solid #e2e8f0;border-radius:var(--r-md);cursor:pointer;text-align:left;box-shadow:var(--sh-sm);transition:border-color .2s">
              <span style="background:#428C84;color:#fff;border-radius:50%;min-width:1.75rem;height:1.75rem;display:inline-flex;align-items:center;justify-content:center;font-size:.72rem;font-weight:800;flex-shrink:0">6</span>
              <span style="font-size:.88rem;color:var(--fg1);line-height:1.4;flex:1;font-weight:600">Rela&#xE7;&#xF5;es sexuais com profissionais do sexo</span>
              <i data-lucide="info" style="width:.9rem;height:.9rem;flex-shrink:0;color:#94a3b8"></i>
            </button>
            <div id="vf-6" style="display:none;position:absolute;top:calc(100% + 6px);left:0;right:0;background:#fff;border:1.5px solid #e2e8f0;border-radius:var(--r-md);padding:.9rem 1rem 1rem;box-shadow:0 8px 28px rgba(0,0,0,.13);z-index:40;font-size:.84rem;color:var(--fg2);line-height:1.65">
              <button onclick="closeVuln('vf-6')" style="float:right;margin:-.1rem -.2rem .3rem .5rem;background:none;border:none;cursor:pointer;color:#94a3b8;padding:.15rem"><i data-lucide="x" style="width:.8rem;height:.8rem"></i></button>
              O contato frequente com profissionais do sexo em pontos de parada nas rodovias representa um importante fator de exposi&#xE7;&#xE3;o &#xE0;s ISTs.
            </div>
          </div>

        </div>
      </section>'''

NEW_VULN_JS = '''  <script>
  window.toggleVuln=function(btn,id){document.querySelectorAll('[id^="vf-"]').forEach(function(p){if(p.id!==id)p.style.display='none';});var p=document.getElementById(id);if(!p)return;p.style.display=p.style.display==='block'?'none':'block';};
  window.closeVuln=function(id){var p=document.getElementById(id);if(p)p.style.display='none';};
  </script>
'''

m2_path = BASE / "modulo-2" / "index.html"
m2 = m2_path.read_text(encoding="utf-8")

# Replace the vuln section using regex (handles any whitespace variations)
m2_new = re.sub(
    r'[ \t]*<!-- BLOCO: Fatores de vulnerabilidade -->.*?</section>',
    NEW_VULN,
    m2,
    flags=re.DOTALL
)

if m2_new == m2:
    print("WARNING: vuln section not found in M2!")
else:
    print(f"M2 vuln section replaced. Old length: {len(m2)}, New length: {len(m2_new)}")

# Add JS before </body>
if 'window.toggleVuln' not in m2_new:
    m2_new = m2_new.replace('</body>', NEW_VULN_JS + '</body>')
    print("M2: toggleVuln JS added")
else:
    print("M2: toggleVuln already present")

m2_path.write_text(m2_new, encoding="utf-8")

# ─── 2. Course name replacement in all modules ───────────────────────────────

NEW_FULL = "ATENÇÃO À SAÚDDE DA CAMINHONEIRA E DO CAMINHONEIRO NA ATENÇÃO PRIMÁRIA"
NEW_SHORT = "ATENÇÃO À SAÚDDE DA CAMINHONEIRA E DO CAMINHONEIRO"

# Fix: correcting the accents
NEW_FULL   = "ATENÇÃO À SAÚDE DA CAMINHONEIRA E DO CAMINHONEIRO NA ATENÇÃO PRIMÁRIA"
NEW_SHORT  = "ATENÇÃO À SAÚDE DA CAMINHONEIRA E DO CAMINHONEIRO"

# Actually let's just use the plain string
NEW_FULL  = "ATENÇÃO À SAÚDE DA CAMINHONEIRA E DO CAMINHONEIRO NA ATENÇÃO PRIMÁRIA"
NEW_SHORT = "ATENÇÃO À SAÚDE DA CAMINHONEIRA E DO CAMINHONEIRO"

files = [BASE / f"modulo-{i}" / "index.html" for i in range(1, 6)]

for path in files:
    if not path.exists():
        print(f"NOT FOUND: {path}")
        continue

    content = path.read_text(encoding="utf-8")
    original = content

    # Pattern A: multiline "e Caminhoneiro\n...na Atenção Primária"
    content = re.sub(
        r'Atenção à Saúde da Caminhoneira e Caminhoneiro\s*\n\s*na Atenção Primária',
        NEW_FULL, content
    )
    # Pattern B: multiline "Caminhoneira\n...e Caminhoneiro na Atenção Primária"
    content = re.sub(
        r'Atenção à Saúde da Caminhoneira\s*\n\s*e Caminhoneiro na Atenção Primária',
        NEW_FULL, content
    )
    # Pattern C: single line full name
    content = content.replace(
        "Atenção à Saúde da Caminhoneira e Caminhoneiro na Atenção Primária",
        NEW_FULL
    )
    # Pattern D: single line without "na Atenção Primária" (sidebar brand)
    content = content.replace(
        "Atenção à Saúde da Caminhoneira e Caminhoneiro",
        NEW_SHORT
    )

    if content != original:
        path.write_text(content, encoding="utf-8")
        print(f"Updated course name: {path.parent.name}/{path.name}")
    else:
        print(f"No course name changes: {path.parent.name}/{path.name}")

# ─── 3. Verification ─────────────────────────────────────────────────────────

print("\n=== Verification ===")
for path in files:
    if not path.exists():
        continue
    c = path.read_text(encoding="utf-8")
    old_count = c.count("e Caminhoneiro na Atenção") + c.count("e Caminhoneiro\n")
    new_count = c.count(NEW_FULL) + c.count(NEW_SHORT)
    vuln_fn = "toggleVuln" in c if "modulo-2" in str(path) else "N/A"
    print(f"  {path.parent.name}: old_name_occurrences={old_count} | new_name_occurrences={new_count} | toggleVuln={vuln_fn}")

print("\nDone.")
