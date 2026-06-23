"""
Reconstruct module HTML files using Read tool results from JSONL
combined with subsequent Edit operations.
"""
import json, re
from pathlib import Path

JSONL = Path(r"C:\Users\AparicioJunior\.claude\projects\c--Users-AparicioJunior-workspace-saude-caminhoneiros\d69d46f7-64c8-484e-bfcd-8c71406dda50.jsonl")
BASE = Path(r"c:\Users\AparicioJunior\workspace\saude-caminhoneiros")

with open(JSONL, encoding='utf-8') as f:
    all_lines = f.readlines()

def get_tool_results_after(start_line):
    """Get tool_result content from user messages near start_line."""
    results = []
    for i in range(start_line, min(start_line + 5, len(all_lines))):
        try:
            obj = json.loads(all_lines[i])
            msg = obj.get('message', {})
            if msg.get('role') == 'user':
                for item in msg.get('content', []):
                    if isinstance(item, dict) and item.get('type') == 'tool_result':
                        c = item.get('content', '')
                        if isinstance(c, str) and len(c) > 1000:
                            results.append(c)
        except Exception:
            pass
    return results

def strip_line_numbers(text):
    """Remove line number prefixes like '1\t', '2\t', '123\t' from Read tool output."""
    lines = text.split('\n')
    clean = []
    for line in lines:

        m = re.match(r'^\d+\t(.*)$', line)
        if m:
            clean.append(m.group(1))
        else:
            clean.append(line)
    return '\n'.join(clean)

def get_reads_for_mod(mod):
    """Collect all Read results for a module, ordered by JSONL line."""
    reads = []
    for i, line in enumerate(all_lines):
        try:
            obj = json.loads(line)
            msg = obj.get('message', {})
            if msg.get('role') == 'assistant':
                for item in msg.get('content', []):
                    if isinstance(item, dict) and item.get('type') == 'tool_use' and item.get('name') == 'Read':
                        fp = item.get('input', {}).get('file_path', '')
                        if f'modulo {mod}' in fp.lower() and 'index.html' in fp:

                            for r in get_tool_results_after(i + 1):
                                if len(r) > 500:
                                    reads.append((i+1, r))
        except Exception:
            pass
    return reads

def get_edit_ops_for_mod(mod):
    """Get all Edit operations for a module in order."""
    ops = []
    for i, line in enumerate(all_lines):
        try:
            obj = json.loads(line)
            msg = obj.get('message', {})
            if msg.get('role') == 'assistant':
                for item in msg.get('content', []):
                    if isinstance(item, dict) and item.get('type') == 'tool_use' and item.get('name') == 'Edit':
                        fp = item.get('input', {}).get('file_path', '')
                        if f'modulo {mod}' in fp.lower() and 'index.html' in fp:
                            inp = item.get('input', {})
                            ops.append((i+1, inp.get('old_string', ''), inp.get('new_string', '')))
        except Exception:
            pass
    return ops

for mod in range(2, 6):
    reads = get_reads_for_mod(mod)

    full_reads = []
    for jsonl_line, raw in reads:
        first_line = raw.split('\n')[0]

        if re.match(r'^1\t<!DOCTYPE', first_line) or raw.startswith('<!DOCTYPE'):
            full_reads.append((jsonl_line, raw))

    if full_reads:

        best_jsonl_line, best_raw = max(full_reads, key=lambda x: len(x[1]))
        content = strip_line_numbers(best_raw)
        print(f"M{mod}: Found full Read at JSONL line {best_jsonl_line}: {len(best_raw)} chars -> {len(content)} clean chars, {content.count(chr(10))} lines")

        edit_ops = get_edit_ops_for_mod(mod)
        applied = 0
        failed = 0
        for (op_line, old, new) in edit_ops:
            if op_line > best_jsonl_line:
                if old in content:
                    content = content.replace(old, new, 1)
                    applied += 1
                else:
                    failed += 1

        print(f"  Applied {applied} edits, {failed} failed")
        print(f"  Final: {content.count(chr(10))} lines, {len(content)} chars")

        path = BASE / f'modulo {mod}' / 'index.html'
        path.write_text(content, encoding='utf-8')
        print(f"  Saved to {path}")
    else:
        print(f"M{mod}: No full Read found (from line 1)")

        if reads:
            print(f"  Available reads: {[(r[0], len(r[1])) for r in reads[:5]]}")
