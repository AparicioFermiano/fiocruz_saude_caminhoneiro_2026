"""
Targeted M3/M4 reconstruction using ONLY post-edit reads.
For M3: only reads after JSONL 218 (first Edit at JSONL 218 replaced head)
For M4: only reads after JSONL 227 (first Edit at JSONL 227 replaced head)
Uses "later read wins" to ensure we get the newest content for each line.
"""
import json, re
from pathlib import Path

JSONL = Path(r"C:\Users\AparicioJunior\.claude\projects\c--Users-AparicioJunior-workspace-saude-caminhoneiros\d69d46f7-64c8-484e-bfcd-8c71406dda50.jsonl")
BASE = Path(r"c:\Users\AparicioJunior\workspace\saude-caminhoneiros")

with open(JSONL, encoding='utf-8') as f:
    all_lines = f.readlines()

print(f"Loaded {len(all_lines)} JSONL lines")

def parse_read_content(raw):
    lines_dict = {}
    for line in raw.split('\n'):
        m = re.match(r'^(\d+)\t(.*)$', line)
        if m:
            lines_dict[int(m.group(1))] = m.group(2)
    return lines_dict

ORIGINAL_SESSION_END = 1600

def get_reads_after(mod, after_jsonl, before_jsonl=ORIGINAL_SESSION_END):
    """Get all Read results for a module after a specific JSONL line."""
    reads = []
    i = 0
    while i < len(all_lines):
        try:
            obj = json.loads(all_lines[i])
            if i < after_jsonl or i >= before_jsonl:
                i += 1
                continue
            msg = obj.get('message', {})
            if msg.get('role') == 'assistant':
                for item in msg.get('content', []):
                    if isinstance(item, dict) and item.get('type') == 'tool_use' and item.get('name') == 'Read':
                        fp = item.get('input', {}).get('file_path', '')
                        if f'modulo {mod}' in fp.lower() and 'index.html' in fp:

                            tool_id = item.get('id', '')
                            offset = item.get('input', {}).get('offset', 0)
                            limit = item.get('input', {}).get('limit', '?')

                            for j in range(i+1, min(i+6, len(all_lines))):
                                res_obj = json.loads(all_lines[j])
                                msg2 = res_obj.get('message', {})
                                for ritem in msg2.get('content', []):
                                    if isinstance(ritem, dict) and ritem.get('type') == 'tool_result':

                                        rid = ritem.get('tool_use_id', '')
                                        if tool_id and rid and rid != tool_id:
                                            continue
                                        c = ritem.get('content', '')
                                        if isinstance(c, str) and len(c) > 50:
                                            parsed = parse_read_content(c)
                                            if parsed and len(parsed) >= 3:
                                                reads.append((i+1, parsed, offset, limit))
        except Exception:
            pass
        i += 1
    return reads

def get_all_edits(mod):
    """Get all Edit operations for a module."""
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
                            old = item.get('input', {}).get('old_string', '')
                            new = item.get('input', {}).get('new_string', '')
                            ops.append((i+1, old, new))
        except Exception:
            pass
    return ops

def reconstruct(mod, first_edit_jsonl):
    print(f"\n{'='*60}")
    print(f"=== Module {mod} (using reads after JSONL {first_edit_jsonl}) ===")

    reads = get_reads_after(mod, first_edit_jsonl)
    print(f"Found {len(reads)} post-edit reads")

    if not reads:
        print("No reads found!")
        return None

    for jsonl_line, d, offset, limit in sorted(reads, key=lambda x: x[0])[:10]:
        if d:
            min_ln, max_ln = min(d.keys()), max(d.keys())
            non_empty = sum(1 for v in d.values() if v.strip())
            print(f"  JSONL {jsonl_line}: lines {min_ln}-{max_ln} ({non_empty} non-empty)")

    if len(reads) > 10:
        print(f"  ... and {len(reads)-10} more reads")

    combined = {}
    for jsonl_line, d, offset, limit in sorted(reads, key=lambda x: x[0]):
        for ln, content_line in d.items():
            if ln not in combined or jsonl_line > combined[ln][1]:
                combined[ln] = (content_line, jsonl_line)

    if not combined:
        return None

    max_line = max(combined.keys())
    min_line = min(combined.keys())
    print(f"\nCoverage: lines {min_line}-{max_line}")

    gaps = []
    in_gap = False
    gap_start = None
    for ln in range(1, max_line + 1):
        if ln not in combined:
            if not in_gap:
                gap_start = ln
                in_gap = True
        else:
            if in_gap:
                gaps.append((gap_start, ln - 1))
                in_gap = False
    if in_gap:
        gaps.append((gap_start, max_line))

    if gaps:
        print(f"Gaps ({len(gaps)} total):")
        for g_start, g_end in gaps[:10]:
            print(f"  Lines {g_start}-{g_end} ({g_end - g_start + 1} lines)")
        if len(gaps) > 10:
            print(f"  ... and {len(gaps)-10} more gaps")

    result_lines = []
    for i in range(1, max_line + 1):
        if i in combined:
            result_lines.append(combined[i][0])
        else:
            result_lines.append('')

    stitched = '\n'.join(result_lines)
    print(f"\nStitched: {len(result_lines)} lines, {len(stitched)} chars")

    all_edits = get_all_edits(mod)
    print(f"Total edits: {len(all_edits)}")

    content = stitched
    applied, failed, skipped = 0, 0, 0
    seen = set()
    for jsonl_line, old, new in all_edits:
        sig = old[:80]
        if sig in seen:
            skipped += 1
            continue
        seen.add(sig)
        if old in content:
            content = content.replace(old, new, 1)
            applied += 1
            print(f"  Applied edit at JSONL {jsonl_line} (old={len(old)}, new={len(new)})")
        else:
            failed += 1
            print(f"  FAILED edit at JSONL {jsonl_line} (old={len(old)}, starts: {old[:60]!r})")

    print(f"\nEdits: {applied} applied, {failed} failed, {skipped} skipped (dupes)")
    print(f"Final: {content.count(chr(10))+1} lines, {len(content)} chars")
    print(f"DOCTYPE: {'<!DOCTYPE html>' in content}")
    print(f"</html>: {'</html>' in content}")
    print(f"<main>: {'<main' in content}")

    lines = content.split('\n')
    print(f"\nFirst 10 lines:")
    for i, l in enumerate(lines[:10]):
        print(f"  {i+1}: {l[:100]}")
    print(f"\nLast 10 lines:")
    for i, l in enumerate(lines[-10:]):
        print(f"  {len(lines)-10+i+1}: {l[:100]}")

    return content

m2_content = reconstruct(2, 216)

m3_content = reconstruct(3, 218)

m4_content = reconstruct(4, 227)

for mod, content in [(2, m2_content), (3, m3_content), (4, m4_content)]:
    if content and '<!DOCTYPE html>' in content and content.count('\n') > 50:
        path = BASE / f'modulo {mod}' / 'index.html'
        path.write_text(content, encoding='utf-8')
        print(f"\nSaved M{mod} to {path}")
    else:
        print(f"\nM{mod}: NOT SAVED (invalid or too small)")
