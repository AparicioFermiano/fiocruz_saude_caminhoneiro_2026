# -*- coding: utf-8 -*-
from pypdf import PdfReader
for m in [1,2,3,4,5]:
    r=PdfReader(f'material/modulo-{m}-conteudo.pdf')
    txt="\n".join(p.extract_text() or "" for p in r.pages)
    open(f".tmp-di/mod{m}_pdf.txt","w",encoding='utf-8').write(txt)
    print(f"mod{m}: {len(txt)} chars, {len(r.pages)} pages")
