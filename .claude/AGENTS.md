# Agentes do Projeto — Saúde da Caminhoneira e Caminhoneiro

## Contexto do Projeto
Plataforma EAD (HTML + CSS + JS puros) sobre saúde de caminhoneiros na APS.
Sem framework, sem build step, sem Node.js.
Stack: Tailwind Play CDN local (`tailwind.js`) + Google Fonts + Lucide icons.

## Regras absolutas
1. Cada módulo é **completamente independente** — sem caminhos `../`
2. CSS vai em `<style type="text/tailwindcss">` inline na página
3. JS vai em `<script>` minificado ao final do `<body>`
4. `tailwind.js` e `tailwind-config.js` com caminho relativo (`./tailwind.js`)
5. Nunca referenciar `design-system.css` externo — os módulos são self-contained
6. Usar **exatamente** os componentes do `material/snippets.html` para animações
7. Imagens em `images/` com `alt`, `width`, `height` explícitos

## Design System

### Fontes
- Display (títulos, badges, botões): **Baloo 2** (500, 600, 700, 800)
- Body (texto corrido): **Mukta** (300, 400, 500, 600, 700)

### Cores por módulo
| Módulo | Tema | Primary | Deep | Surface |
|--------|------|---------|------|---------|
| 1 | Amarelo | `#FECF08` | `#D4AA00` | `#FFFDE8` |
| 2 | Azul | `#3F56A6` | `#293872` | `#EEF0FA` |
| 3 | Verde | `#187848` | `#0E6238` | `#EAF6EF` |
| 4 | Vermelho | `#E11B12` | `#9A1009` | `#FEE9E8` |
| 5 | Preto | `#1A1A1A` | `#000000` | `#F5F5F5` |

### Componentes disponíveis (via snippets.html)
- Hero (hero-wrap, hero-nav, hero-body)
- Botões (btn, variantes por módulo btn--mX)
- Badges (badge--soft, badge--orange, badge--ch)
- Bigbtns (brand, reflexao, cta, dica)
- Accordion (acc, acc__body)
- Modal + Overlay
- Hotspot (hs-scene, hs-point, hs-btn, hs-popover)
- Flashcard (flip 3D)
- Timeline
- Quiz (questão de fixação)
- Carrossel de fotos
- Navegação por abas
- Destaque textual (hbox)
- Sidenav (toc)

## Comandos disponíveis
- `/new-module` — Cria estrutura de novo módulo
- `/validate-module` — Valida conformidade com design system

## Estrutura de arquivos esperada por módulo
```
modulo X/
├── tailwind.js          ← Tailwind Play CDN (local)
├── tailwind-config.js   ← Tema do módulo
├── index.html           ← Página principal (self-contained)
├── images/              ← Imagens do módulo
└── (unidade-01.html, unidade-02.html, ...)  ← Futuro
```
