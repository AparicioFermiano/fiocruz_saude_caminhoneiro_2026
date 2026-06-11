import json
from pathlib import Path

JSONL = Path(r"C:\Users\AparicioJunior\.claude\projects\c--Users-AparicioJunior-workspace-saude-caminhoneiros\d69d46f7-64c8-484e-bfcd-8c71406dda50.jsonl")
BASE = Path(r"c:\Users\AparicioJunior\workspace\saude-caminhoneiros")

with open(JSONL, encoding='utf-8') as f:
    all_lines = f.readlines()

def normalize_path(p):
    return p.replace('\\', '/')

def get_module_ops(mod):
    ops = []
    target = f'modulo {mod}/index.html'
    for line in all_lines:
        try:
            obj = json.loads(line)
            msg = obj.get('message', {})
            if msg.get('role') == 'assistant':
                for item in msg.get('content', []):
                    if isinstance(item, dict) and item.get('type') == 'tool_use':
                        name = item.get('name', '')
                        inp = item.get('input', {})
                        fp = normalize_path(inp.get('file_path', ''))
                        if target in fp:
                            if name == 'Write':
                                ops.append(('Write', inp.get('content', '')))
                            elif name == 'Edit':
                                ops.append(('Edit', inp.get('old_string', ''), inp.get('new_string', '')))
        except Exception:
            pass
    return ops

def reconstruct(mod):
    ops = get_module_ops(mod)
    if not ops:
        return None, ['no ops']

    content = ''
    errors = []

    for i, op in enumerate(ops):
        if op[0] == 'Write':
            content = op[1]
        elif op[0] == 'Edit':
            old, new = op[1], op[2]
            if not content and i == 0:
                content = old
            if old in content:
                content = content.replace(old, new, 1)
            else:
                errors.append(f"Edit {i+1}: old not found ({len(old)} chars, starts: {repr(old[:60])})")

    return content, errors

for mod in range(1, 6):
    content, errors = reconstruct(mod)
    for e in errors:
        print(f"M{mod} WARN: {e}")
    if content:
        path = BASE / f'modulo {mod}' / 'index.html'
        path.write_text(content, encoding='utf-8')
        lc = content.count('\n')
        print(f"M{mod}: {lc} lines, {len(content)} chars -> SAVED")
    else:
        print(f"M{mod}: FAILED")
