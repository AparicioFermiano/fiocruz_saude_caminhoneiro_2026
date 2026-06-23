"""
Reconstruct M2, M3, M4 by stitching together Read tool results
from the JSONL conversation history.

Strategy:
1. Find all Read results for each module in time windows between edits
2. Parse their line numbers to understand coverage
3. Stitch overlapping reads to get complete file content
4. Apply remaining edits
"""
import json, re
from pathlib import Path

JSONL = Path(r"C:\Users\AparicioJunior\.claude\projects\c--Users-AparicioJunior-workspace-saude-caminhoneiros\d69d46f7-64c8-484e-bfcd-8c71406dda50.jsonl")
BASE = Path(r"c:\Users\AparicioJunior\workspace\saude-caminhoneiros")

with open(JSONL, encoding='utf-8') as f:
    all_lines = f.readlines()

def parse_read_content(raw):
    """Parse Read tool output with line numbers into {line_num: content} dict."""
    lines_dict = {}
    for line in raw.split('\n'):
        m = re.match(r'^(\d+)\t(.*)$', line)
        if m:
            lines_dict[int(m.group(1))] = m.group(2)
    return lines_dict

def get_all_reads_for_mod(mod, after_jsonl=0, before_jsonl=999999):
    """Get all Read tool results for a module in a JSONL line range."""
    reads = []
    for i, line in enumerate(all_lines):
        if i < after_jsonl or i >= before_jsonl:
            continue
        try:
            obj = json.loads(line)
            msg = obj.get('message', {})
            if msg.get('role') == 'assistant':
                for item in msg.get('content', []):
                    if isinstance(item, dict) and item.get('type') == 'tool_use' and item.get('name') == 'Read':
                        fp = item.get('input', {}).get('file_path', '')
                        if f'modulo {mod}' in fp.lower() and 'index.html' in fp:

                            for j in range(i+1, min(i+6, len(all_lines))):
                                res_obj = json.loads(all_lines[j])
                                msg2 = res_obj.get('message', {})
                                for ritem in msg2.get('content', []):
                                    if isinstance(ritem, dict) and ritem.get('type') == 'tool_result':
                                        c = ritem.get('content', '')
                                        if isinstance(c, str) and len(c) > 200:
                                            parsed = parse_read_content(c)
                                            if parsed and len(parsed) > 10:
                                                reads.append((i+1, parsed))
        except Exception:
            pass
    return reads

def get_edit_ops_for_mod(mod, after_jsonl=0):
    """Get all Edit operations for a module after a given JSONL line."""
    ops = []
    for i, line in enumerate(all_lines):
        if i < after_jsonl:
            continue
        try:
            obj = json.loads(line)
            msg = obj.get('message', {})
            if msg.get('role') == 'assistant':
                for item in msg.get('content', []):
                    if isinstance(item, dict) and item.get('type') == 'tool_use' and item.get('name') == 'Edit':
                        fp = item.get('input', {}).get('file_path', '')
                        if f'modulo {mod}' in fp.lower() and 'index.html' in fp:
                            old = item.get('input', {}).get('old_string', '')
                            new = item.get('input', {}).get('new_string', '')
                            ops.append((i+1, old, new))
        except Exception:
            pass
    return ops

def stitch_reads(reads):
    """Stitch multiple {line_num: content} dicts into a complete file."""
    combined = {}
    for jsonl_line, d in reads:
        for ln, content in d.items():
            if ln not in combined:
                combined[ln] = content
    if not combined:
        return ''
    max_line = max(combined.keys())
    result = []
    for i in range(1, max_line + 1):
        result.append(combined.get(i, ''))
    return '\n'.join(result)

def get_first_edit_jsonl(mod):
    """Get the JSONL line of the first Edit for a module."""
    for i, line in enumerate(all_lines):
        try:
            obj = json.loads(line)
            msg = obj.get('message', {})
            if msg.get('role') == 'assistant':
                for item in msg.get('content', []):
                    if isinstance(item, dict) and item.get('type') == 'tool_use' and item.get('name') == 'Edit':
                        fp = item.get('input', {}).get('file_path', '')
                        if f'modulo {mod}' in fp.lower() and 'index.html' in fp:
                            return i
        except Exception:
            pass
    return 0

for mod in [2, 3, 4]:
    print(f"\n{'='*60}")
    print(f"=== Module {mod} ===")

    first_edit_idx = get_first_edit_jsonl(mod)
    print(f"First edit at JSONL line {first_edit_idx+1}")

    all_reads = get_all_reads_for_mod(mod, after_jsonl=first_edit_idx+1)
    print(f"Found {len(all_reads)} reads after first edit")

    all_edits = get_edit_ops_for_mod(mod, after_jsonl=first_edit_idx+1)
    print(f"Found {len(all_edits)} subsequent edits")

    if not all_reads:
        print("No reads found - cannot reconstruct")
        continue

    edit_lines = [op[0] for op in all_edits]
    second_edit_line = edit_lines[0] if edit_lines else 999999

    baseline_reads = [(jl, d) for jl, d in all_reads if jl < second_edit_line]
    print(f"Baseline reads (before 2nd edit at line {second_edit_line}): {len(baseline_reads)}")

    if not baseline_reads:

        baseline_reads = all_reads
        print("Using all reads for stitching")

    stitched = stitch_reads(baseline_reads)
    lc = stitched.count('\n')
    print(f"Stitched baseline: {lc} lines, {len(stitched)} chars")

    if not stitched or lc < 10:
        print("Stitched content too small, skipping")
        continue

    lines_dict = {}
    for jl, d in baseline_reads:
        lines_dict.update(d)
    if lines_dict:
        min_ln = min(lines_dict.keys())
        max_ln = max(lines_dict.keys())
        covered = len(lines_dict)
        print(f"Coverage: lines {min_ln}-{max_ln}, {covered} lines covered out of {max_ln-min_ln+1}")

    content = stitched
    applied = 0
    failed = 0

    seen_ops = set()
    for op_line, old, new in all_edits:
        sig = (old[:50], new[:50])
        if sig in seen_ops:
            continue
        seen_ops.add(sig)
        if old in content:
            content = content.replace(old, new, 1)
            applied += 1
        else:
            failed += 1

    lc = content.count('\n')
    print(f"After applying edits: {lc} lines, {len(content)} chars ({applied} applied, {failed} failed)")

    has_doctype = '<!DOCTYPE html>' in content
    has_closing = '</html>' in content
    print(f"Valid HTML: DOCTYPE={has_doctype}, </html>={has_closing}")

    if has_doctype and has_closing and lc > 100:
        path = BASE / f'modulo {mod}' / 'index.html'
        path.write_text(content, encoding='utf-8')
        print(f"SAVED to {path}")
    else:
        print("Content incomplete, not saving")
        print(f"Preview first 300 chars: {content[:300]}")
