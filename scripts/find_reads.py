import json
from pathlib import Path

JSONL = Path(r"C:\Users\AparicioJunior\.claude\projects\c--Users-AparicioJunior-workspace-saude-caminhoneiros\d69d46f7-64c8-484e-bfcd-8c71406dda50.jsonl")

with open(JSONL, encoding='utf-8') as f:
    all_lines = f.readlines()

print(f"Total JSONL lines: {len(all_lines)}")

for i, line in enumerate(all_lines[:600]):
    try:
        obj = json.loads(line)
        msg = obj.get('message', {})
        if msg.get('role') == 'user':
            for item in msg.get('content', []):
                if isinstance(item, dict) and item.get('type') == 'tool_result':
                    c = item.get('content', '')
                    if isinstance(c, str) and len(c) > 3000 and ('DOCTYPE' in c or '<html' in c or 'class="block"' in c):
                        print(f"Line {i+1}: tool_result {len(c)} chars")

                        for m in range(1, 6):
                            if f'Módulo {m}' in c or f'odulo {m}' in c:
                                print(f"  -> Module {m}")
                                break
                        print(f"  Preview: {c[:200]}")
    except Exception:
        pass
