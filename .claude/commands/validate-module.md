# Validar módulo

Verifica se um módulo segue o design system e os padrões do projeto.

## Uso
```
/validate-module <número>
```

## Verificações realizadas

### Estrutura de arquivos
- [ ] `tailwind.js` presente
- [ ] `tailwind-config.js` presente
- [ ] `index.html` presente
- [ ] Pasta `images/` presente (se há imagens)
- [ ] Nenhum `design-system.css` referenciado no HTML

### HTML
- [ ] `<!DOCTYPE html>` e `<html lang="pt-BR">`
- [ ] Google Fonts (Baloo 2 + Mukta)
- [ ] Um único bloco `<style type="text/tailwindcss">`
- [ ] `:root` com variáveis CSS do módulo
- [ ] JS ao final do `<body>`
- [ ] Sem `style=""` inline para cores e fontes (usar classes Tailwind)

### Design system
- [ ] Hero com gradiente correto do módulo
- [ ] Botões usam variantes do módulo (btn--mX)
- [ ] Accordions abrem/fecham corretamente
- [ ] Modal funcional (se houver)
- [ ] Hotspot funcional (se houver)
- [ ] Lucide icons carregam

### Responsividade
- [ ] Layout não quebra em 375px
- [ ] Layout adequado em 1280px
