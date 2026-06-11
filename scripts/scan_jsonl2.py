import json
from pathlib import Path

JSONL2 = Path(r"C:\Users\AparicioJunior\.claude\projects\c--Users-AparicioJunior-workspace-saude-caminhoneiros\74f40bc9-16f3-488b-9ed6-e7830b63d452.jsonl")

with open(JSONL2, encoding='utf-8') as f:
    all_lines = f.readlines()

print(f"JSONL2 total lines: {len(all_lines)}")

for i, line in enumerate(all_lines):
    try:
        obj = json.loads(line)
        msg = obj.get('message', {})
        if msg.get('role') == 'assistant':
            for item in msg.get('content', []):
                if isinstance(item, dict) and item.get('type') == 'tool_use':
                    name = item.get('name', '')
                    inp = item.get('input', {})
                    fp = inp.get('file_path', '')
                    if name in ('Write', 'Edit') and 'index.html' in fp:
                        c = inp.get('content', '') or inp.get('old_string', '') or ''
                        print(f"Line {i+1}: {name} {fp[-45:]} ({len(c)} chars)")
    except Exception:
        pass
