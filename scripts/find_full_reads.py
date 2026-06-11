import json
from pathlib import Path

JSONL = Path(r"C:\Users\AparicioJunior\.claude\projects\c--Users-AparicioJunior-workspace-saude-caminhoneiros\d69d46f7-64c8-484e-bfcd-8c71406dda50.jsonl")

with open(JSONL, encoding='utf-8') as f:
    all_lines = f.readlines()

# Look for Read tool_use that reads module HTML files
# Then check the subsequent tool_result for the content
reads = {}
for i, line in enumerate(all_lines):
    try:
        obj = json.loads(line)
        msg = obj.get('message', {})
        if msg.get('role') == 'assistant':
            for item in msg.get('content', []):
                if isinstance(item, dict) and item.get('type') == 'tool_use' and item.get('name') == 'Read':
                    fp = item.get('input', {}).get('file_path', '')
                    for m in range(1, 6):
                        if f'modulo {m}' in fp.lower() and 'index.html' in fp:
                            reads[i] = (m, fp)
    except Exception:
        pass

print("Read operations for module HTML files:")
for line_idx, (mod, fp) in reads.items():
    # The result should be in the NEXT few lines
    for j in range(line_idx+1, min(line_idx+5, len(all_lines))):
        try:
            res_obj = json.loads(all_lines[j])
            res_msg = res_obj.get('message', {})
            for item in res_msg.get('content', []):
                if isinstance(item, dict) and item.get('type') == 'tool_result':
                    c = item.get('content', '')
                    if isinstance(c, str) and len(c) > 500:
                        print(f"  JSONL line {line_idx+1}: Read M{mod} -> result at line {j+1}: {len(c)} chars")
                        print(f"    Preview: {c[:150]}")
        except Exception:
            pass
