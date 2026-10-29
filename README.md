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
  css/ js/            a página carrega styles.min.css e scripts.min.js
  images/ media/
scripts/minify.ps1    gera um .min a partir de um .css ou .js (-Source, -Dest)
.claude/              comandos do Claude Code para criar e validar módulos
```

**Atenção:** os `.min` foram editados direto e têm o que `styles.css` e `scripts.js` não têm (botão de voltar ao topo, menu lateral no celular, lista de referências). Rodar o `minify.ps1` sobre a fonte hoje apaga isso da página.

## Publicar

Copie a pasta do módulo para o servidor ou ambiente do curso. Não há build.

## Homologação

Não há ambiente de homologação.
