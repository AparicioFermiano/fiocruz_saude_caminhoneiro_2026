# -*- coding: utf-8 -*-
import docx, re
def clean(s): return re.sub(r'\s+',' ',s).strip()
d=docx.Document(".tmp-di/docx/mod1_di.docx")
for i,t in enumerate(d.tables):
    rows=len(t.rows); cols=len(t.columns)
    first=clean(t.rows[0].cells[0].text)[:60]
    print(f"TBL{i}: {rows}x{cols} | first='{first}'")
