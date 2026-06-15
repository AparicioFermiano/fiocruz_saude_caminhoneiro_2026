# -*- coding: utf-8 -*-
import re,unicodedata,docx,sys
from docx.oxml.ns import qn
from html.parser import HTMLParser
m=int(sys.argv[1])
def norm(s):
    s=unicodedata.normalize('NFKC',s).lower()
    s=re.sub(r'[^\w]','',s,flags=re.UNICODE)
    return s
# DI paragraphs (prose only: skip table rows, skip headings/boxes)
d=docx.Document(f".tmp-di/docx/mod{m}_di.docx")
pm={p._p:p for p in d.paragraphs}
di=[]
for ch in d.element.body.iterchildren():
    if ch.tag==qn('w:p'):
        p=pm.get(ch)
        if p is None: continue
        t=re.sub(r'\s+',' ',p.text).strip()
        if len(t)<40: continue          # skip short (headings/labels)
        if re.match(r'^(Reflexão|Saiba mais|Dica|Atenção|Quadro|Figura|Tabela|Fonte)',t): continue
        di.append(t)
# HTML <p> texts in body (before modais)
html=open(f"modulo-{m}/index.html",encoding='utf-8').read()
body=html.split('═══════════════════ MODAIS')[0] if 'MODAIS' in html else html
# crude: get <p ...>...</p> text
ps=re.findall(r'<p[ >][^>]*>(.*?)</p>', body, re.S)
def strip(x): return re.sub(r'\s+',' ',re.sub(r'<[^>]+>','',x)).strip()
hp=[strip(x) for x in ps if len(strip(x))>=40]
print(f"MOD{m}: DI prose paragraphs={len(di)} | HTML <p>={len(hp)}\n")
# align: for each DI para, find HTML p that startswith same 30 norm chars
hpn=[norm(x) for x in hp]
for i,t in enumerate(di):
    key=norm(t)[:35]
    matches=[j for j,x in enumerate(hpn) if key and key in x]
    status="OK" if matches else "??"
    # check if this DI para is split (its end not matching the hp end) 
    print(f"[{status}] DI#{i}: {t[:75]}")
