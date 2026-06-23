import re
from pathlib import Path

BASE = Path(r'c:\Users\AparicioJunior\workspace\saude-caminhoneiros')

def ref(text, pdf=None):
    icon = (
        f' <a href="media/{pdf}" download title="Baixar PDF" '
        'style="display:inline-flex;align-items:center;vertical-align:middle;'
        'margin-left:.35rem;color:inherit;opacity:.55;transition:opacity .15s;" '
        'onmouseover="this.style.opacity=1" onmouseout="this.style.opacity=.55">'
        '<i data-lucide="file-down" style="width:1rem;height:1rem;"></i></a>'
        if pdf else ''
    )
    return f'<li>{text}{icon}</li>'

REFS = {
    1: [
        ref('BRASIL. Ministério da Saúde. <strong>Política Nacional de Promoção da Saúde</strong>. Brasília, DF: Ministério da Saúde, 2014.', 'politica_nacional_promocao_saude.pdf'),
        ref('BRASIL. Conselho Nacional de Secretários de Saúde (CONASS). <strong>Vigilância em Saúde</strong>: parte 1. Brasília, DF: CONASS, 2011. (Coleção Para Entender a Gestão do SUS, v. 5).', 'livro_conass_vigilancia.pdf'),
        ref('SILVA, A. C. et al. <strong>Saúde e qualidade de vida de caminhoneiros</strong>. Curitiba: Editora Científica Digital, 2022.', 'saude_caminhoneiros_editoracientifica.pdf'),
        ref('BRASIL. Ministério da Saúde. Secretaria de Atenção à Saúde. <strong>Política Nacional de Atenção Integral à Saúde do Homem</strong>: princípios e diretrizes. Brasília, DF: Ministério da Saúde, 2008.', 'politica_nacional_atencao_saude_homem.pdf'),
        ref('BRASIL. Ministério da Saúde. <strong>Política Nacional de Atenção Integral à Saúde da Mulher</strong>: princípios e diretrizes. Brasília, DF: Ministério da Saúde, 2004.', 'politica_nac_atencao_mulher.pdf'),
        ref('BRASIL. Ministério da Saúde. <strong>Política Nacional de Promoção da Saúde (PNPS)</strong>: revisão da Portaria MS/GM n.° 687, de 30 de março de 2006. Brasília, DF: Ministério da Saúde, 2014.', 'pnps_revisao_portaria_687.pdf'),
        ref('FREITAS, C. M. et al. Conquistas, limites e obstáculos à redução de riscos ambientais à saúde nos 30 anos do SUS. <strong>Ciência &amp; Saúde Coletiva</strong>, v. 23, n. 6, p. 1981–1996, 2018.', 'freitas_riscos_ambientais.pdf'),
        ref('BRASIL. Ministério da Saúde. Secretaria de Atenção à Saúde. <strong>Acolhimento à demanda espontânea: queixas mais comuns na Atenção Básica</strong>. Brasília, DF: Ministério da Saúde, 2013. (Cadernos de Atenção Básica, n. 28, v. 2).', 'acolhimento_demanda_espontanea_cab28.pdf'),
        ref('STARFIELD, B. <strong>Atenção Primária: equilíbrio entre necessidades de saúde, serviços e tecnologia</strong>. Brasília, DF: UNESCO; Ministério da Saúde, 2002.'),
    ],
    2: [
        ref('BRASIL. Ministério da Saúde. Secretaria de Atenção Primária à Saúde. Nota Técnica n.° 8/2020 — <strong>Cartão de Saúde do Caminhoneiro e da Caminhoneira</strong>. Brasília: MS, 2021.', 'sei_nota_distribuicao_preservativos.pdf'),
        ref('BRASIL. Ministério da Saúde. Secretaria de Vigilância em Saúde. <strong>Protocolo Clínico e Diretrizes Terapêuticas para Atenção Integral às Pessoas com Infecções Sexualmente Transmissíveis (IST)</strong>. Brasília: MS, 2022.', 'pcdt_ist_2022.pdf'),
        ref('BRASIL. Ministério da Saúde. Secretaria de Vigilância em Saúde e Ambiente. <strong>Manual dos Centros de Referência para Imunobiológicos Especiais</strong>. 6. ed. Brasília: Ministério da Saúde, 2023.', 'manual_imunobiologicos_6ed.pdf'),
        ref('BRASIL. Ministério da Saúde. <strong>Protocolo Clínico e Diretrizes Terapêuticas para Manejo da Infecção pelo HIV em Adultos — Módulo 1</strong>. Brasília: Ministério da Saúde, 2024.', 'pcdt_hiv_modulo1_2024.pdf'),
        ref('BRASIL. Ministério da Saúde. Secretaria de Ciência, Tecnologia, Inovação e Complexo da Saúde. <strong>Protocolo Clínico e Diretrizes Terapêuticas para Profilaxia Pós-Exposição (PEP) ao HIV, IST e Hepatites Virais</strong>. Brasília: MS, 2021.', 'pcdt_pep_hiv_2021.pdf'),
        ref('BRASIL. Ministério da Saúde. Secretaria de Vigilância em Saúde e Ambiente. <strong>Guia de Vigilância em Saúde</strong>, v. 2, 6. ed. rev. Brasília: Ministério da Saúde, 2024.', 'guia_vigilancia_saude.pdf'),
        ref('BRASIL. Ministério da Saúde. Secretaria de Ciência, Tecnologia, Inovação e Complexo da Saúde. <strong>Protocolo Clínico e Diretrizes Terapêuticas para Profilaxia Pré-Exposição (PrEP) ao HIV</strong>. Brasília: MS, 2022.', 'pcdt_prep_hiv.pdf'),
        ref('BRASIL. Ministério da Saúde. <strong>Instrução Normativa do Calendário Nacional de Vacinação 2026</strong>. Brasília: MS, 2026.', 'calendario_vacinacao_2026.pdf'),
        ref('ROWLEY, J. et al. Chlamydia, gonorrhea, trichomoniasis and syphilis: global prevalence and incidence estimates, 2016. <strong>Bulletin of the World Health Organization</strong>, v. 97, n. 8, p. 548–562, 2019.', 'rowley_chlamydia_gonorrhea_BLT.pdf'),
    ],
    3: [
        ref('APA (ASSOCIAÇÃO AMERICANA DE PSIQUIATRIA). <strong>Manual diagnóstico e estatístico de transtornos mentais</strong>. Tradução de Maria Inês Corrêa Nascimento et al. 5. ed. Porto Alegre: Artmed, 2014.', 'DSM-V.pdf'),
    ],
    4: [
        ref('BRASIL. Ministério da Saúde. <strong>Plano de Ações Estratégicas para o Enfrentamento das Doenças Crônicas e Agravos Não Transmissíveis no Brasil 2021–2030</strong>. Brasília: MS, 2021.', 'plano_dant_2022_2030.pdf'),
        ref('SOCIEDADE BRASILEIRA DE CARDIOLOGIA; SOCIEDADE BRASILEIRA DE HIPERTENSÃO; SOCIEDADE BRASILEIRA DE NEFROLOGIA. <strong>7.ª Diretrizes Brasileiras de Hipertensão Arterial</strong>. Arquivos Brasileiros de Cardiologia, 2016.', 'diretriz_has_sbc_2020.pdf'),
    ],
    5: [
        ref('BRASIL. Ministério da Saúde. <strong>Prevenção do suicídio: manual dirigido a profissionais das equipes de saúde mental</strong>. Brasília, DF: Ministério da Saúde, 2006.', 'manual_prevencao_suicidio_saude.pdf'),
        ref('BRASIL. Ministério da Saúde. Secretaria de Atenção Primária à Saúde. <strong>O cuidado à saúde do homem em contexto de violência e a proteção de meninas e mulheres no âmbito da APS</strong>: caderno didático do curso. Brasília: MS, 2022.', 'cuidado_saude_homem_violencia.pdf'),
        ref('VASCONCELOS, M. F. F.; SEFFNER, F.; MELO, M. R. "Gente é mais que homem": gênero e cuidados em álcool e outras drogas. <strong>Educar em Revista</strong>, v. 36, e75406, 2020.', 'vasconcelos_genero_masculinidades.pdf'),
    ],
}

PRIMARY_DEEP = {
    1: 'var(--m1-primary-deep)', 2: 'var(--m2-primary-deep)',
    3: 'var(--m3-primary-deep)', 4: 'var(--m4-primary-deep)', 5: 'var(--m5-primary-deep)',
}
PRIMARY = {
    1: 'var(--m1-primary)', 2: 'var(--m2-primary)',
    3: 'var(--m3-primary)', 4: 'var(--m4-primary)', 5: 'var(--m5-primary)',
}

def build_refs_section(mod):
    items = '\n          '.join(REFS[mod])
    pd = PRIMARY_DEEP[mod]
    return (
        '\n\n      <!-- REFERENCIAS BIBLIOGRAFICAS -->'
        '\n      <section class="block referencias-section" style="margin-bottom:2rem">'
        f'\n        <h2 class="block-title" style="color:{pd};margin-bottom:1.5rem">Referências Bibliográficas</h2>'
        '\n        <ol class="referencias-list">'
        f'\n          {items}'
        '\n        </ol>'
        '\n      </section>'
    )

def build_css(mod):
    bg = PRIMARY[mod]
    on = 'var(--m1-on-primary)' if mod == 1 else '#fff'
    return (
        '.referencias-list{list-style:decimal;padding-left:1.5rem;display:flex;flex-direction:column;gap:.85rem}'
        '.referencias-list li{font-size:.88rem;line-height:1.65;color:var(--fg2)}'
        '.sidebar-toggle{display:none;position:fixed;bottom:5.5rem;right:1.75rem;z-index:151;'
        'width:3rem;height:3rem;border-radius:999px;border:none;cursor:pointer;'
        'align-items:center;justify-content:center;box-shadow:var(--sh-md);'
        'transition:transform .18s,box-shadow .18s}'
        '.sidebar-toggle:hover{transform:translateY(-2px);box-shadow:var(--sh-lg)}'
        '.sidebar-toggle svg{width:1.3rem;height:1.3rem}'
        '.sidebar-overlay{position:fixed;inset:0;background:rgba(0,0,0,.45);'
        'z-index:189;backdrop-filter:blur(2px);display:none}'
        '.sidebar-overlay.is-open{display:block}'
        '@media(max-width:768px){'
        '.page-layout{grid-template-columns:1fr!important;padding:1.5rem 1rem 4rem}'
        '.sidebar{position:fixed;left:0;top:0;bottom:0;width:min(280px,85vw);z-index:190;'
        'transform:translateX(-100%);transition:transform .28s cubic-bezier(.4,0,.2,1);'
        'overflow-y:auto;padding:1rem 0;box-shadow:0 0 40px rgba(0,0,0,.18);background:var(--card)}'
        '.sidebar.is-open{transform:translateX(0)}'
        f'.sidebar-toggle{{display:flex;background:{bg};color:{on}}}'
        '.hs-btn{font-size:.62rem!important;width:36px!important;height:36px!important}'
        '.hs-btn svg{width:.8rem!important;height:.8rem!important}'
        '.hero-nav__inner{justify-content:center}'
        '.hero-nav__name{text-align:center;font-size:.8rem}'
        '.hero__title{text-align:center;margin-left:auto;margin-right:auto}'
        '.hero__kicker{margin-left:auto;margin-right:auto}'
        '.hero__btns{justify-content:center}'
        '}'
        '@media(min-width:769px){'
        '.sidebar-toggle{display:none!important}'
        '.sidebar-overlay{display:none!important}'
        '}'
    )

JS_EXTRA = (
    'window.openSidebar=()=>{'
    'const s=document.querySelector(".sidebar"),o=document.getElementById("sidebarOverlay");'
    's&&s.classList.add("is-open");o&&o.classList.add("is-open")};'
    'window.closeSidebar=()=>{'
    'const s=document.querySelector(".sidebar"),o=document.getElementById("sidebarOverlay");'
    's&&s.classList.remove("is-open");o&&o.classList.remove("is-open")};'
    'document.querySelectorAll(".sidebar-nav__link").forEach(a=>a.addEventListener("click",closeSidebar));'
)

MOD_MAIN_CLOSE = {
    1: '\n    </main>',
    2: '\n    </main>',
    3: '\n    </main>',
    4: '\n      </main>',
    5: '\n    </main>',
}

for mod in range(1, 6):
    folder = BASE / f'modulo {mod}'

    html_path = folder / 'index.html'
    content = html_path.read_text(encoding='utf-8')

    content = re.sub(
        r'\s*<!-- .*?MATERIAL DE APOIO.*?-->.*?</section>',
        '',
        content,
        flags=re.DOTALL
    )

    main_close = MOD_MAIN_CLOSE[mod]
    refs_html = build_refs_section(mod)
    content = content.replace(main_close, refs_html + main_close, 1)

    hamburger = (
        '\n  <div class="sidebar-overlay" id="sidebarOverlay" onclick="closeSidebar()"></div>'
        '\n  <button class="sidebar-toggle" aria-label="Menu" onclick="openSidebar()">'
        '<i data-lucide="menu"></i></button>'
    )
    if 'sidebar-overlay' not in content:
        content = content.replace(
            '  <button id="backToTop"',
            hamburger + '\n  <button id="backToTop"',
            1
        )

    html_path.write_text(content, encoding='utf-8')
    print(f'M{mod} HTML ok')

    css_path = folder / 'css/styles.min.css'
    css = css_path.read_text(encoding='utf-8')
    if '.referencias-list' not in css:
        css_path.write_text(css + build_css(mod), encoding='utf-8')
        print(f'M{mod} CSS  ok')
    else:
        print(f'M{mod} CSS  skip (already present)')

    js_path = folder / 'js/scripts.min.js'
    js = js_path.read_text(encoding='utf-8')
    if 'openSidebar' not in js:
        js_path.write_text(js + JS_EXTRA, encoding='utf-8')
        print(f'M{mod} JS   ok')
    else:
        print(f'M{mod} JS   skip (already present)')
    print()

print('All done.')
