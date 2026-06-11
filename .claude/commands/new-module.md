# Criar novo módulo

Cria a estrutura completa de um novo módulo baseada no design system.

## Uso
```
/new-module <número> <tema-cor> "<Título do Módulo>"
```

## Parâmetros
- `número`: número do módulo (01, 02, etc.)
- `tema-cor`: yellow | blue | green | red | black
- `título`: título completo do módulo

## O que criar
1. Pasta `modulo-XX/` na raiz
2. Copiar `tailwind.js` de outro módulo existente
3. Criar `tailwind-config.js` com as cores do tema do módulo
4. Criar `index.html` com a estrutura padrão do design system:
   - Hero com gradiente do módulo
   - Seções de conteúdo com accordions
   - Footer com logos institucionais
5. Criar pasta `images/` vazia

## Checklist de qualidade
- [ ] `<!DOCTYPE html>` e `<html lang="pt-BR">`
- [ ] Google Fonts (Baloo 2 + Mukta) no `<head>`
- [ ] `tailwind.js` e `tailwind-config.js` com caminho relativo
- [ ] Um único `<style type="text/tailwindcss">` com `:root` + componentes
- [ ] Nenhum link para `design-system.css` externo
- [ ] JS minificado ao final do `<body>`
- [ ] Logo e imagens em `images/` com `alt`, `width`, `height`
- [ ] Responsivo: testar em 375px e 1280px

## Cores por tema
| Tema | Primary | Deep | Surface | On-primary |
|------|---------|------|---------|------------|
| yellow | #FECF08 | #D4AA00 | #FFFDE8 | #524000 |
| blue | #3F56A6 | #293872 | #EEF0FA | #ffffff |
| green | #187848 | #0E6238 | #EAF6EF | #ffffff |
| red | #E11B12 | #9A1009 | #FEE9E8 | #ffffff |
| black | #1A1A1A | #000000 | #F5F5F5 | #ffffff |
