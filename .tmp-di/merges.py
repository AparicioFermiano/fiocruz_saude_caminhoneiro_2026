# -*- coding: utf-8 -*-
import re,unicodedata,docx,sys
from docx.oxml.ns import qn
def norm(s):
    s=unicodedata.normalize('NFKC',s).lower()
    s=re.sub(r'[^\w]','',s,flags=re.UNICODE)
    return s
def di_paras(m):
    d=docx.Document(f".tmp-di/docx/mod{m}_di.docx")
    pm={p._p:p for p in d.paragraphs}
    out=[]
    for ch in d.element.body.iterchildren():
        if ch.tag==qn('w:p'):
            p=pm.get(ch)
            if p is None: continue
            t=re.sub(r'\s+',' ',p.text).strip()
            if len(t)<25: continue
            if re.match(r'^(Reflexão|Saiba mais|Dica|Atenção|Quadro|Figura|Tabela|Fonte|\d+\.\d)',t): continue
            out.append(t)
    return out
def html_ps(m):
    h=open(f"modulo-{m}/index.html",encoding='utf-8').read()
    h=re.split(r'MODAIS|class="overlay"',h)[0]
    ps=re.findall(r'<p[ >].*?</p>',h,re.S)
    out=[]
    for x in ps:
        t=re.sub(r'\s+',' ',re.sub(r'<[^>]+>','',x)).strip()
        if len(t)>=25: out.append(t)
    return out
for m in [1,2,3,4,5]:
    di=di_paras(m); dn=[norm(x) for x in di]
    hp=html_ps(m)
    merges=[]
    for t in hp:
        n=norm(t)
        # which DI paras are substrings of this <p>?
        idxs=[i for i,d in enumerate(dn) if len(d)>=25 and d in n]
        if len(idxs)>=2:
            merges.append((t,[di[i] for i in idxs]))
    out=open(f".tmp-di/mod{m}_merges.txt","w",encoding='utf-8')
    out.write(f"MOD{m}: {len(merges)} <p> com parágrafos fundidos\n\n")
    for t,parts in merges:
        out.write("HTML<p>: "+t[:90]+"\n")
        for pp in parts: out.write("   DI▸ "+pp[:90]+"\n")
        out.write("\n")
    print(f"mod{m}: {len(merges)} <p> fundidos")
