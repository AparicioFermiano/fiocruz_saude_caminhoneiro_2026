ai# CLAUDE.md — Agente de Criação de Curso EAD

Este arquivo instrui o Claude Code a construir um curso EAD em módulos e unidades para o projeto **Saúde da Caminhoneira e Caminhoneiro na APS**. Siga todas as seções na ordem em que aparecem ao criar ou modificar páginas do curso.

---

## 1. Projeto

Plataforma EAD (ensino a distância) sobre saúde de caminhoneiros. HTML + CSS + JS puros. Sem framework, sem build step, sem Node.js.

**Regras absolutas:**
- Nunca usar bibliotecas externas além de Tailwind Play CDN (`tailwind.js`) e fontes Google Fonts.
- Todo CSS customizado vai em `<style type="text/tailwindcss">` ou em `<style>` inline na página.
- Todo JS fica no `<script>` ao final do `<body>`, minificado.
- Imagens referenciadas como `images/nome-da-imagem.ext` — a pasta `images/` fica na raiz do projeto.
- Nenhum arquivo TypeScript, nenhum bundle, nenhum import de módulo ES.

---

## 2. Stack e Tailwind offline

```html
<!-- Dentro de qualquer modulo-XX/ — caminhos sempre relativos à própria pasta -->
<script src="./tailwind.js"></script>
<script src="./tailwind-config.js"></script>
```

- O `tailwind-config.js` já estende o tema com as cores e fontes do projeto (ver Seção 4).
- Classes Tailwind são usadas para layout e utilitários. Classes do Design System (`.btn`, `.card`, `.acc`, etc.) são declaradas em `<style type="text/tailwindcss">`.
- **Nunca** importar Tailwind de CDN externo — só do arquivo local `tailwind.js`.

---

## 3. Estrutura de Arquivos

Cada módulo é uma pasta **completamente independente** — nenhum arquivo externo é referenciado com `../`.

```
saude-caminhoneiros/
├── tailwind.js              ← Tailwind Play CDN (fonte original, não commitado)
├── tailwind-config.js       ← Tema fonte (cópia para cada módulo)
├── index.html               ← Landing page
├── cursos.html              ← Catálogo de cursos
│
├── modulo-01/               ← Módulo I (totalmente independente)
│   ├── tailwind.js          ← cópia do tailwind.js raiz
│   ├── tailwind-config.js   ← cópia do tailwind-config.js raiz
│   ├── images/              ← imagens exclusivas deste módulo
│   ├── js/
│   │   └── modulo.js        ← JS compartilhado entre unidades do módulo
│   ├── unidade-01.html
│   ├── unidade-02.html
│   └── ...
│
├── modulo-02/               ← Módulo II (mesma estrutura)
│   ├── tailwind.js
│   ├── tailwind-config.js
│   ├── images/
│   ├── js/
│   │   └── modulo.js
│   └── unidade-01.html
└── ...
```

**Regras de independência:**
- Todo `src=""` e `href=""` usa caminhos relativos dentro da própria pasta do módulo (`./tailwind.js`, `./images/foto.jpg`, `./js/modulo.js`).
- Nunca usar `../` para referenciar recursos de outro módulo ou da raiz.
- Ao criar um novo módulo: copiar `tailwind.js` e `tailwind-config.js` da raiz para a pasta do novo módulo.

**Nomenclatura:**
- Pastas de módulo: `modulo-01`, `modulo-02`, etc.
- Arquivos de unidade: `unidade-01.html`, `unidade-02.html`, etc.
- Imagens: prefixo do módulo, ex: `modulo1-cenario-ubs.jpg`

---

## 4. Design System — Tokens

### 4.1 Paleta de cores

| Token CSS | Hex | Uso |
|---|---|---|
| `--primary` | `#187848` | Cor principal, links, botões |
| `--primary-deep` | `#0E6238` | Hover, hero background |
| `--accent-green` | `#43B64A` | Destaques, ícones ativos |
| `--cta` | `#F5A623` | Botões de chamada, badges laranja |
| `--cta-deep` | `#E08C0E` | Hover do CTA |
| `--background` | `#F3F6F4` | Fundo da página |
| `--foreground` | `#1E2A23` | Texto principal |
| `--card` | `#FFFFFF` | Fundo de cards |
| `--secondary` | `#EAF6EF` | Fundo suave verde |
| `--muted` | `#ECF1EE` | Fundo neutro |
| `--muted-foreground` | `#6B7771` | Texto secundário |
| `--border` | `#E2EAE5` | Bordas |
| `--brand-yellow` | `#FECF08` | Amarelo da marca |
| `--brand-red` | `#E11B12` | Vermelho da marca |
| `--brand-blue` | `#3F56A6` | Azul da marca |

**Variáveis de gradiente:**
```css
--grad-hero:   linear-gradient(115deg, #1E8A52 0%, #157a48 60%, #0E6238 100%);
--grad-brand:  linear-gradient(135deg, #2A9D5C 0%, #187848 55%, #0E6238 100%);
--grad-bright: linear-gradient(135deg, #4FC65A 0%, #2E9E58 100%);
--grad-cta:    linear-gradient(180deg, #F8B23E 0%, #F5A623 100%);
```

**Sombras:**
```css
--sh-sm:    0 2px 8px rgba(15,55,33,.08);
--sh-md:    0 8px 24px rgba(15,55,33,.10);
--sh-lg:    0 18px 48px rgba(15,55,33,.16);
--sh-cta:   0 10px 22px rgba(245,166,35,.35);
--sh-brand: 0 12px 28px rgba(24,120,72,.28);
```

### 4.2 Tipografia

| Família | Variável | Uso |
|---|---|---|
| Baloo 2 (500–800) | `--font-display` | Títulos, badges, botões, nav |
| Mukta (300–700) | `--font-body` | Corpo do texto |

```html
<!-- Importar no <head> de cada página -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;600;700;800&family=Mukta:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

### 4.3 Border radius e base

```css
--radius: 14px;   /* cards, inputs */
/* Botões e badges usam border-radius: 999px */
/* Modais: 24px */
/* Accordions: 14px */
```

---

## 5. Design System — Componentes

Declare os componentes abaixo em `<style type="text/tailwindcss">` em cada página onde forem usados. **Nunca** criar um arquivo CSS separado para componentes — cada página é autocontida.

### 5.1 Variáveis CSS (colar em todo `:root`)

```css
:root {
  --background:#F3F6F4;--foreground:#1E2A23;--card:#FFFFFF;--card-foreground:#1E2A23;
  --primary:#187848;--primary-deep:#0E6238;--primary-foreground:#FFFFFF;
  --secondary:#EAF6EF;--secondary-foreground:#0E6238;
  --accent-green:#43B64A;--cta:#F5A623;--cta-deep:#E08C0E;--cta-foreground:#FFFFFF;
  --muted:#ECF1EE;--muted-foreground:#6B7771;
  --brand-yellow:#FECF08;--brand-red:#E11B12;--brand-blue:#3F56A6;
  --border:#E2EAE5;--input:#D8E2DC;--ring:#187848;
  --destructive:#E11B12;--success:#2E9E58;--radius:14px;
  --grad-hero:linear-gradient(115deg,#1E8A52 0%,#157a48 60%,#0E6238 100%);
  --grad-brand:linear-gradient(135deg,#2A9D5C 0%,#187848 55%,#0E6238 100%);
  --grad-bright:linear-gradient(135deg,#4FC65A 0%,#2E9E58 100%);
  --grad-cta:linear-gradient(180deg,#F8B23E 0%,#F5A623 100%);
  --sh-sm:0 2px 8px rgba(15,55,33,.08);--sh-md:0 8px 24px rgba(15,55,33,.10);
  --sh-lg:0 18px 48px rgba(15,55,33,.16);--sh-cta:0 10px 22px rgba(245,166,35,.35);
  --sh-brand:0 12px 28px rgba(24,120,72,.28);
  --font-display:'Baloo 2',system-ui,sans-serif;
  --font-body:'Mukta',system-ui,-apple-system,sans-serif;
  --ease:cubic-bezier(.4,0,.2,1);
}
```

### 5.2 Reset base

```css
*{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:96px}
body{margin:0;background:var(--background);color:var(--foreground);font-family:var(--font-body);font-size:17px;line-height:1.72;-webkit-font-smoothing:antialiased}
h1,h2,h3,h4{font-family:var(--font-display);line-height:1.18;margin:0;letter-spacing:-.01em}
p{margin:0 0 1.15em}a{color:var(--primary);text-decoration:none}img{max-width:100%;display:block}
```

### 5.3 Botões

```css
.btn{--_bg:var(--primary);--_fg:#fff;--_bd:transparent;display:inline-flex;align-items:center;justify-content:center;gap:.55em;font-family:var(--font-display);font-weight:700;font-size:1rem;line-height:1;padding:.82em 1.4em;border-radius:999px;border:1.5px solid var(--_bd);background:var(--_bg);color:var(--_fg);cursor:pointer;transition:transform .18s var(--ease),box-shadow .18s var(--ease),background .18s var(--ease);white-space:nowrap}
.btn svg{width:1.1em;height:1.1em}.btn:hover{transform:translateY(-2px)}.btn:active{transform:translateY(0) scale(.98)}
.btn--primary{--_bg:var(--primary);box-shadow:var(--sh-brand)}.btn--primary:hover{--_bg:var(--primary-deep)}
.btn--cta{background:var(--grad-cta);color:#fff;box-shadow:var(--sh-cta)}.btn--cta:hover{filter:brightness(1.03)}
.btn--outline{--_bg:transparent;--_fg:var(--primary);--_bd:var(--primary)}.btn--outline:hover{--_bg:var(--secondary)}
.btn--ghost{--_bg:transparent;--_fg:var(--primary);--_bd:transparent}.btn--ghost:hover{--_bg:var(--secondary)}
.btn--secondary{--_bg:var(--secondary);--_fg:var(--primary-deep)}.btn--secondary:hover{--_bg:#d9efe2}
.btn--sm{font-size:.85rem;padding:.6em 1em}.btn--lg{font-size:1.12rem;padding:.95em 1.7em}
.btn--icon{padding:.7em;width:2.9em;height:2.9em;border-radius:999px}
.btn--block{width:100%}.btn:disabled{opacity:.5;cursor:not-allowed;transform:none;box-shadow:none}
```

### 5.4 Card

```css
.card{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);box-shadow:var(--sh-sm)}
```

### 5.5 Badge / Eyebrow

```css
.eyebrow{font-family:var(--font-display);font-weight:700;font-size:.78rem;letter-spacing:.14em;text-transform:uppercase}
.badge{display:inline-flex;align-items:center;gap:.4em;font-family:var(--font-display);font-weight:700;font-size:.74rem;letter-spacing:.06em;padding:.42em .9em;border-radius:999px;white-space:nowrap}
.badge--module{background:rgba(255,255,255,.16);color:#fff;border:1.5px solid rgba(255,255,255,.45);text-transform:uppercase}
.badge--orange{background:var(--cta);color:#fff;text-transform:uppercase;letter-spacing:.08em}
.badge--soft{background:var(--secondary);color:var(--primary-deep)}
```

### 5.6 Header fixo

```css
.site-header{position:fixed;top:4px;left:0;right:0;z-index:110;background:rgba(255,255,255,.92);backdrop-filter:saturate(1.4) blur(10px);border-bottom:1px solid var(--border)}
.site-header__inner{max-width:1240px;margin:0 auto;padding:.7rem 1.5rem;display:flex;align-items:center;gap:1.2rem}
.brand__pill{display:inline-flex;align-items:center;gap:.5rem;background:var(--grad-bright);color:#fff;font-family:var(--font-display);font-weight:800;font-size:.92rem;padding:.42rem .9rem;border-radius:999px;box-shadow:var(--sh-sm)}
.brand__title{font-family:var(--font-display);font-weight:700;font-size:.98rem;color:var(--primary-deep);line-height:1.1}
.brand__sub{font-size:.76rem;color:var(--muted-foreground);line-height:1.1}
.nav{margin-left:auto;display:flex;gap:.3rem}
.nav a{display:inline-flex;align-items:center;gap:.45rem;font-family:var(--font-display);font-weight:600;font-size:.92rem;color:var(--foreground);padding:.5rem .85rem;border-radius:10px;transition:background .15s var(--ease),color .15s var(--ease)}
.nav a:hover,.nav a.is-active{background:var(--secondary);color:var(--primary-deep)}
```

### 5.7 Hero

```css
.hero{position:relative;overflow:hidden;color:#fff;padding:8.5rem 1.5rem 4.5rem;isolation:isolate}
.hero__bg{position:absolute;inset:0;z-index:-3;background:#0E6238}
.hero__overlay{position:absolute;inset:0;z-index:-2;background:var(--grad-hero);opacity:.9}
.hero__pattern{position:absolute;inset:0;z-index:-1;opacity:.5;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='54' height='54' viewBox='0 0 54 54'%3E%3Cg fill='none' stroke='%23ffffff' stroke-width='2' stroke-linecap='round' opacity='0.18'%3E%3Cpath d='M27 19v16M19 27h16'/%3E%3C/g%3E%3C/svg%3E")}
.hero__inner{max-width:1240px;margin:0 auto;position:relative}
.hero__title{font-size:clamp(2.4rem,1.5rem+3.4vw,4.2rem);font-weight:800;max-width:17ch;text-shadow:0 2px 18px rgba(7,40,25,.35);margin:.6rem 0 0}
.hero__actions{display:flex;flex-wrap:wrap;gap:.8rem;margin-top:2rem}
```

### 5.8 Layout Shell (2 colunas: sidenav + conteúdo)

```css
.shell{max-width:1240px;margin:0 auto;padding:3rem 1.5rem 6rem;display:grid;grid-template-columns:300px 1fr;gap:2.5rem;align-items:start}
.sidenav{position:sticky;top:104px;background:var(--card);border:1px solid var(--border);border-top:4px solid var(--primary);border-radius:18px;box-shadow:var(--sh-md);padding:1.3rem 1.2rem;max-height:calc(100vh - 130px);overflow:auto}
.sidenav__head{display:flex;align-items:center;gap:.5rem;font-family:var(--font-display);font-weight:700;font-size:.78rem;letter-spacing:.14em;text-transform:uppercase;color:var(--muted-foreground);padding-bottom:.7rem;margin-bottom:.5rem;border-bottom:1px solid var(--border)}
.toc{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:.1rem}
.toc a{display:flex;gap:.6rem;align-items:baseline;padding:.5rem .65rem;border-radius:10px;font-size:.95rem;color:var(--foreground);transition:background .15s var(--ease),color .15s var(--ease)}
.toc a:hover{background:var(--secondary)}.toc a.is-active{background:#FFF6E8;color:var(--primary-deep);font-weight:600;box-shadow:inset 3px 0 0 var(--cta)}
.toc .dot{width:7px;height:7px;border-radius:999px;background:var(--accent-green);flex:0 0 auto;transform:translateY(.55em)}
.toc .num{font-weight:700;color:var(--primary);font-family:var(--font-display);flex:0 0 auto}
.content{min-width:0;max-width:840px}.content section{scroll-margin-top:100px;margin-bottom:3rem}
```

### 5.9 Cabeçalho de seção

```css
.section-h{display:flex;align-items:center;gap:.8rem;margin-bottom:1.1rem}
.section-h::before{content:"";width:6px;align-self:stretch;min-height:1.6em;border-radius:999px;background:var(--accent-green)}
.section-h h2{font-size:clamp(1.5rem,1.2rem+1.2vw,2rem);color:var(--primary)}
```

### 5.10 Accordion (`<details>`)

```css
.accordion{display:flex;flex-direction:column;gap:.7rem;margin:1.5rem 0}
.acc{background:var(--card);border:1px solid var(--border);border-radius:14px;overflow:hidden;transition:box-shadow .2s var(--ease),border-color .2s var(--ease)}
.acc[open]{box-shadow:var(--sh-md);border-color:#CDE6D8}
.acc>summary{list-style:none;cursor:pointer;display:flex;align-items:center;gap:.85rem;padding:1.05rem 1.2rem;font-family:var(--font-display);font-weight:700;font-size:1.08rem;color:var(--primary-deep);transition:background .15s var(--ease)}
.acc>summary::-webkit-details-marker{display:none}.acc>summary:hover{background:var(--secondary)}
.acc__icon{width:2.1rem;height:2.1rem;border-radius:999px;background:var(--secondary);color:var(--primary);display:grid;place-items:center;flex:0 0 auto}
.acc__chev{margin-left:auto;color:var(--primary);transition:transform .25s var(--ease);flex:0 0 auto}
.acc[open] .acc__chev{transform:rotate(180deg)}
.acc__body{padding:0 1.2rem 1.2rem 4.15rem;color:var(--muted-foreground)}
.acc__body p:last-child{margin-bottom:0}
```

### 5.11 Botões grandes (BigBtn)

```css
.bigbtns{display:grid;gap:1rem;margin:1.6rem 0}
.bigbtn{display:flex;align-items:center;gap:1.1rem;text-align:left;width:100%;cursor:pointer;padding:1.2rem 1.4rem;border:none;border-radius:18px;color:#fff;background:var(--grad-bright);box-shadow:var(--sh-md);transition:transform .2s var(--ease),box-shadow .2s var(--ease)}
.bigbtn:hover{transform:translateY(-3px);box-shadow:var(--sh-lg)}.bigbtn:active{transform:translateY(0)}
.bigbtn--brand{background:var(--grad-brand)}.bigbtn--cta{background:var(--grad-cta)}
.bigbtn__icon{width:3.4rem;height:3.4rem;border-radius:999px;flex:0 0 auto;background:rgba(255,255,255,.22);display:grid;place-items:center}
.bigbtn__title{display:block;font-family:var(--font-display);font-weight:800;font-size:1.18rem;line-height:1.15}
.bigbtn__sub{display:block;font-size:.95rem;opacity:.9;line-height:1.2}
.bigbtn__arrow{flex:0 0 auto;transition:transform .2s var(--ease)}.bigbtn:hover .bigbtn__arrow{transform:translateX(5px)}
```

### 5.12 Modal / Overlay

```css
.overlay{position:fixed;inset:0;z-index:200;display:grid;place-items:center;padding:1.5rem;background:rgba(10,45,28,.55);backdrop-filter:blur(6px);opacity:0;visibility:hidden;transition:opacity .22s var(--ease),visibility .22s var(--ease)}
.overlay.is-open{opacity:1;visibility:visible}
.modal{width:min(640px,100%);background:var(--card);border-radius:24px;overflow:hidden;box-shadow:var(--sh-lg);transform:translateY(14px) scale(.98);transition:transform .26s var(--ease)}
.overlay.is-open .modal{transform:none}
.modal__head{position:relative;padding:1.6rem 1.8rem 1.4rem;color:#fff;background:var(--grad-bright)}
.modal__close{position:absolute;top:1rem;right:1rem;width:2.2rem;height:2.2rem;border:none;cursor:pointer;border-radius:999px;background:rgba(255,255,255,.18);color:#fff;display:grid;place-items:center}
.modal__close:hover{background:rgba(255,255,255,.32)}
.modal__title{font-size:1.45rem;font-weight:800;line-height:1.15}
.modal__body{padding:1.7rem 1.8rem 1.9rem;color:var(--muted-foreground)}
.modal__actions{margin-top:1.3rem;display:flex;gap:.7rem;flex-wrap:wrap}
```

### 5.13 Callout

```css
.callout{background:var(--card);border:1px solid var(--border);border-radius:18px;padding:1.5rem 1.6rem;box-shadow:var(--sh-sm);margin:1.6rem 0}
.callout--soft{background:var(--secondary);border-color:#CDE6D8}
```

### 5.14 Hotspot (imagem interativa)

```css
.hotspot-fig{position:relative;border-radius:18px;border:1px solid var(--border);box-shadow:var(--sh-md);margin:1.6rem 0;background:#dfeee6}
.hotspot{position:absolute;transform:translate(-50%,-50%);width:2.9rem;height:2.9rem;border-radius:999px;border:3px solid #fff;cursor:pointer;display:grid;place-items:center;color:#fff;font-family:var(--font-display);font-weight:800;font-size:1.15rem;background:var(--primary);box-shadow:0 6px 16px rgba(7,40,25,.4);transition:transform .18s var(--ease),background .18s var(--ease);z-index:2}
.hotspot::after{content:"";position:absolute;inset:-9px;border-radius:999px;border:2px solid currentColor;opacity:.55;animation:pulse 2.2s var(--ease) infinite}
.hotspot:hover{transform:translate(-50%,-50%) scale(1.12);background:var(--primary-deep)}
.hotspot.is-active{background:var(--cta)}
@keyframes pulse{0%{transform:scale(1);opacity:.55}70%{transform:scale(1.5);opacity:0}100%{opacity:0}}
.balloon{position:absolute;z-index:20;width:min(310px,78vw);background:var(--popover,#fff);border-radius:16px;box-shadow:var(--sh-lg);border:1px solid var(--border);padding:1.1rem 1.2rem;transform:translateX(-50%);display:none}
.balloon.is-open{display:block}
.balloon__title{font-family:var(--font-display);font-weight:700;font-size:1.05rem;color:var(--primary-deep);margin-bottom:.35rem;line-height:1.2}
.balloon__txt{font-size:.92rem;line-height:1.55;color:var(--muted-foreground)}
```

### 5.15 Barra de progresso de leitura

```css
.progress-rail{position:fixed;top:0;left:0;right:0;height:4px;z-index:120}
.progress-fill{height:100%;width:0;background:linear-gradient(90deg,#2A9D5C 0%,#43B64A 35%,#FECF08 65%,#F5A623 85%,#E11B12 100%);transition:width .12s linear}
```

### 5.16 Back to top

```css
.totop{position:fixed;right:1.4rem;bottom:1.4rem;z-index:90;width:3rem;height:3rem;border:none;cursor:pointer;border-radius:999px;background:var(--primary);color:#fff;display:grid;place-items:center;box-shadow:var(--sh-brand);opacity:0;transform:translateY(12px);pointer-events:none;transition:opacity .25s var(--ease),transform .25s var(--ease)}
.totop.is-shown{opacity:1;transform:none;pointer-events:auto}.totop:hover{background:var(--primary-deep)}
```

### 5.17 Responsivo

```css
@media(max-width:920px){
  .shell{grid-template-columns:1fr;gap:1.5rem}
  .sidenav{position:relative;top:0;max-height:none}
  .nav{display:none}
}
```

---

## 6. Templates de Página

### 6.1 Página de Módulo (`modulo-N-slug.html`)

Estrutura obrigatória:
1. `<head>` com fontes, Tailwind, variáveis CSS e estilos de componentes
2. Barra de progresso de leitura
3. Header fixo com logo + nav
4. Hero com: badge de módulo, número, título, subtítulo, carga horária, botão CTA
5. Shell com sidenav (TOC das unidades) e `.content` com seções
6. Cada seção começa com `.section-h` + `h2`
7. Accordions para conteúdo expandível
8. Botões BigBtn para navegar à próxima unidade
9. Back to top
10. JS minificado ao final

**Hero de módulo:**
```html
<section class="hero">
  <div class="hero__bg"></div>
  <div class="hero__overlay"></div>
  <div class="hero__pattern"></div>
  <div class="hero__inner">
    <span class="badge badge--module">Módulo N</span>
    <h1 class="hero__title">Título do Módulo</h1>
    <p style="opacity:.88;font-size:1.15rem;margin-top:.7rem;max-width:54ch">Subtítulo descritivo.</p>
    <div class="hero__actions">
      <a href="unidade-1-slug.html" class="btn btn--cta btn--lg">Iniciar módulo</a>
      <a href="curso-slug.html" class="btn btn--ghost-light">← Voltar ao curso</a>
    </div>
  </div>
</section>
```

### 6.2 Página de Unidade (`unidade-N-slug.html`)

Estrutura obrigatória:
1. Mesmo cabeçalho e setup do módulo
2. Hero menor com badge de unidade + título + objetivo de aprendizagem
3. Shell: sidenav com TOC das seções da unidade + conteúdo
4. Conteúdo rico: textos, callouts, figuras, accordions, hotspots (se houver imagem interativa)
5. Botão "Próxima unidade" ao final (`.bigbtn--cta`)
6. JS minificado

### 6.3 Página de Curso (`curso-slug.html`)

Lista de módulos como cards clicáveis com número, título, descrição e quantidade de unidades.

---

## 7. Workflow — Como Criar o Curso

Quando o usuário fornecer o conteúdo do curso (PDF, HTM ou texto), siga estes passos em ordem:

### Passo 1 — Ler e estruturar o conteúdo
1. Leia todo o material disponibilizado.
2. Identifique a hierarquia: **Curso → Módulos → Unidades → Seções**.
3. Para cada unidade, anote: título, objetivos, textos, listas, tabelas, imagens referenciadas.

### Passo 2 — Planejar arquivos
Antes de criar qualquer arquivo, liste os arquivos que serão gerados:
```
curso-saude-caminhoneiros.html
modulo-1-introducao.html
  unidade-1-1-contexto.html
  unidade-1-2-perfil.html
modulo-2-saude.html
  ...
```

### Passo 3 — Gerar páginas
Para cada página, nesta ordem:
1. HTML completo com `<!DOCTYPE html>`, `<html lang="pt-BR">`, `<head>` completo.
2. `<style type="text/tailwindcss">` com `:root`, reset, e todos os componentes usados nessa página.
3. Conteúdo semântico no `<body>`.
4. `<script>` com JS minificado ao final.

### Passo 4 — JS do módulo

O JS compartilhado fica em `modulo-XX/js/modulo.js` e é carregado em todas as unidades do módulo:

```html
<script src="./js/modulo.js"></script>
```

O `modulo.js` contém as funções comuns: progresso de leitura, TOC ativo, back-to-top, openModal/closeModal, hotspots. JS específico de uma única unidade pode ser adicionado em um `<script>` extra após o `modulo.js`.

Conteúdo padrão de `modulo.js` (já minificado):

```js
(function(){
  var fill=document.querySelector('.progress-fill'),
      totop=document.querySelector('.totop'),
      toc=document.querySelectorAll('.toc a'),
      secs=document.querySelectorAll('.content section');
  function upd(){
    var s=document.documentElement,t=s.scrollTop||document.body.scrollTop,
        h=s.scrollHeight-s.clientHeight;
    if(fill)fill.style.width=(h>0?t/h*100:0)+'%';
    if(totop){t>300?totop.classList.add('is-shown'):totop.classList.remove('is-shown');}
    if(toc.length&&secs.length){
      var cur='';
      secs.forEach(function(s){if(s.getBoundingClientRect().top<=120)cur=s.id;});
      toc.forEach(function(a){a.classList.toggle('is-active',a.getAttribute('href')==='#'+cur);});
    }
  }
  window.addEventListener('scroll',upd,{passive:true});
  if(totop)totop.addEventListener('click',function(){window.scrollTo({top:0,behavior:'smooth'});});
  upd();
})();
```

JS do accordion (se houver hotspots):

```js
document.querySelectorAll('.hotspot').forEach(function(h){
  h.addEventListener('click',function(){
    var id=h.dataset.balloon,b=document.getElementById(id);
    if(!b)return;
    var open=b.classList.contains('is-open');
    document.querySelectorAll('.balloon').forEach(function(x){x.classList.remove('is-open');});
    document.querySelectorAll('.hotspot').forEach(function(x){x.classList.remove('is-active');});
    if(!open){b.classList.add('is-open');h.classList.add('is-active');}
  });
});
document.querySelectorAll('.balloon__close').forEach(function(b){
  b.addEventListener('click',function(){
    b.closest('.balloon').classList.remove('is-open');
    document.querySelectorAll('.hotspot').forEach(function(h){h.classList.remove('is-active');});
  });
});
```

---

## 8. Regras de Qualidade

- **Nunca** usar `style=""` inline para cores e fontes — usar sempre as classes de componente ou variáveis CSS.
- **Nunca** duplicar o bloco `:root` — uma única declaração por página.
- Todos os `id` de seção usados no TOC devem ser únicos e em kebab-case.
- Imagens sempre com `alt` descritivo, `width` e `height` explícitos para evitar CLS.
- Links internos sempre relativos ao arquivo atual (ex: `../modulo-2.html`).
- Não criar `README.md` ou arquivos de documentação — tudo fica neste `CLAUDE.md`.

---

## 9. Arquivos de Referência do Design System

Os arquivos abaixo estão em `material/` e devem ser lidos para extrair padrões visuais adicionais:

| Arquivo | Conteúdo |
|---|---|
| `material/theme.css` | Tokens CSS, reset, badges, botões, card |
| `material/theme-components.css` | Header, hero, shell, sidenav, TOC, accordion, bigbtn, modal, hotspot, callout |
| `material/Guia de Estilo - Design System (offline) (2).html` | Guia visual completo (abrir no navegador para inspecionar) |
| `material/Material Autoinstrucional - Saude da Caminhoneira e Caminhoneiro (2).htm` | Conteúdo do curso (abrir no navegador para ler) |

**Para ler o conteúdo dos arquivos `.html` / `.htm` bundled:** abra-os no navegador, pois são bundles que descompactam em runtime. Não tente parsear o HTML raw desses arquivos.

---

## 10. Checklist antes de entregar cada página

- [ ] `<!DOCTYPE html>` e `<html lang="pt-BR">` presentes
- [ ] Fontes Google Fonts carregadas no `<head>`
- [ ] `tailwind.js` e `tailwind-config.js` referenciados com caminho correto (relativo)
- [ ] Um único bloco `<style type="text/tailwindcss">` com `:root` + componentes usados
- [ ] Conteúdo fiel ao material do curso (sem inventar informações)
- [ ] TOC do sidenav reflete as seções reais da página
- [ ] JS minificado ao final do `<body>`
- [ ] Imagens em `images/` com `alt`, `width`, `height`
- [ ] Links de navegação (próxima unidade, voltar ao módulo) corretos
- [ ] Responsivo funciona em 375px (mobile) e 1280px (desktop)
