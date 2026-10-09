# Saúde da caminhoneira e do caminhoneiro (Fiocruz, 2026)

Curso on-line da Fiocruz em HTML, CSS e JavaScript. Cinco módulos, cada um uma página independente:

1. O cuidado da caminhoneira e do caminhoneiro na Atenção Primária à Saúde
2. Cuidado integral nas infecções sexualmente transmissíveis (IST)
3. Saúde mental da caminhoneira e do caminhoneiro
4. Cuidado integral com doenças crônicas e outras afecções
5. As violências nas estradas

## Abrir

```bash
python -m http.server 8000
```

Acesse <http://localhost:8000/modulo-1/> (troque por `modulo-2` … `modulo-5`).

Servir por HTTP em vez de abrir o arquivo direto evita bloqueio do navegador a scripts e mídia locais.

## Estrutura

```
modulo-N/
  index.html          o módulo
  css/ js/ images/ media/
scripts/              scripts Python/PowerShell usados na montagem e revisão do conteúdo
.claude/              comandos do Claude Code para criar e validar módulos
```

O `style.min.css` e o `modulo.min.js` de cada módulo saem ao salvar, pela extensão
`emeraldwalk.runonsave` do VS Code (configurada em `.vscode/settings.json`). A lista de extensões
recomendadas é a do workspace (`../.vscode/extensions.json`), e não mais a deste repositório.

## Publicar

Copie a pasta do módulo para o servidor ou ambiente do curso. Não há build.

## Homologação

Não há ambiente de homologação.
