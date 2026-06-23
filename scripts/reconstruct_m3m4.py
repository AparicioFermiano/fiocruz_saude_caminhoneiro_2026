"""
Reconstruct M3 and M4 using all available reads and edits.
Uses a progressive approach: start from earliest reads, apply edits,
then incorporate later reads to fill gaps.
"""
import json, re
from pathlib import Path

JSONL = Path(r"C:\Users\AparicioJunior\.claude\projects\c--Users-AparicioJunior-workspace-saude-caminhoneiros\d69d46f7-64c8-484e-bfcd-8c71406dda50.jsonl")
BASE = Path(r"c:\Users\AparicioJunior\workspace\saude-caminhoneiros")

with open(JSONL, encoding='utf-8') as f:
    all_lines = f.readlines()

def parse_read_content(raw):
    lines_dict = {}
    for line in raw.split('\n'):
        m = re.match(r'^(\d+)\t(.*)$', line)
        if m:
            lines_dict[int(m.group(1))] = m.group(2)
    return lines_dict

def get_all_reads_for_mod(mod):
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
                            for j in range(i+1, min(i+6, len(all_lines))):
                                res_obj = json.loads(all_lines[j])
                                msg2 = res_obj.get('message', {})
                                for ritem in msg2.get('content', []):
                                    if isinstance(ritem, dict) and ritem.get('type') == 'tool_result':
                                        c = ritem.get('content', '')
                                        if isinstance(c, str) and len(c) > 200:
                                            parsed = parse_read_content(c)
                                            if parsed and len(parsed) > 5:
                                                reads.append((i+1, parsed))
        except Exception:
            pass
    return reads

def get_edit_ops_for_mod(mod):
    ops = []
    for i, line in enumerate(all_lines):
        try:
            obj = json.loads(line)
            msg = obj.get('message', {})
            if msg.get('role') == 'assistant':
                for item in msg.get('content', []):
                    if isinstance(item, dict) and item.get('type') == 'tool_use' and item.get('name') in ('Edit', 'Write'):
                        fp = item.get('input', {}).get('file_path', '')
                        if f'modulo {mod}' in fp.lower() and 'index.html' in fp:
                            name = item.get('name')
                            old = item.get('input', {}).get('old_string', '')
                            new = item.get('input', {}).get('new_string', '')
                            content = item.get('input', {}).get('content', '')
                            if name == 'Write':
                                ops.append((i+1, 'Write', '', content))
                            else:
                                ops.append((i+1, 'Edit', old, new))
        except Exception:
            pass
    return ops

def reconstruct_mod(mod):
    all_reads = get_all_reads_for_mod(mod)
    all_ops = get_edit_ops_for_mod(mod)

    print(f"\n{'='*60}")
    print(f"Module {mod}: {len(all_reads)} reads, {len(all_ops)} ops")

    if not all_reads:
        return None

    write_content = None
    write_jsonl = None
    for jsonl_line, op, old, new in all_ops:
        if op == 'Write':
            write_content = new
            write_jsonl = jsonl_line
            break

    edit_lines = [op[0] for op in all_ops]

    first_edit = edit_lines[0] if edit_lines else 0
    second_edit = edit_lines[1] if len(edit_lines) > 1 else 999999

    if write_content:
        print(f"  Using Write at JSONL {write_jsonl} as baseline ({len(write_content)} chars)")
        content = write_content

        applied, failed = 0, 0
        seen = set()
        for jsonl_line, op, old, new in all_ops:
            if jsonl_line <= write_jsonl:
                continue
            if op != 'Edit':
                continue
            sig = old[:60]
            if sig in seen:
                continue
            seen.add(sig)
            if old in content:
                content = content.replace(old, new, 1)
                applied += 1
            else:
                failed += 1
        print(f"  Applied {applied} edits, {failed} failed")
        print(f"  Final: {content.count(chr(10))} lines, {len(content)} chars")
        return content

    combined = {}
    read_timestamps = {}

    for jsonl_line, d in sorted(all_reads, key=lambda x: x[0]):
        for ln, content_line in d.items():
            if ln not in combined or not combined[ln].strip():
                combined[ln] = content_line
                read_timestamps[ln] = jsonl_line

    if not combined:
        return None

    max_line = max(combined.keys())

    result_lines = []
    for i in range(1, max_line + 1):
        result_lines.append(combined.get(i, ''))

    stitched = '\n'.join(result_lines)
    empty_lines = sum(1 for l in result_lines if not l)
    print(f"  Stitched: {len(result_lines)} lines, {len(stitched)} chars, {empty_lines} empty gaps")

    content = stitched
    applied, failed = 0, 0
    seen = set()
    for jsonl_line, op, old, new in all_ops:
        if op != 'Edit':
            continue
        sig = old[:60]
        if sig in seen:
            continue
        seen.add(sig)
        if old in content:
            content = content.replace(old, new, 1)
            applied += 1
        else:
            failed += 1

    print(f"  Applied {applied} edits, {failed} failed")
    print(f"  Final: {content.count(chr(10))} lines, {len(content)} chars")
    return content

for mod in [3, 4]:
    result = reconstruct_mod(mod)
    if result:
        has_doctype = '<!DOCTYPE html>' in result
        has_closing = '</html>' in result
        lc = result.count('\n')
        print(f"  Validating: DOCTYPE={has_doctype}, </html>={has_closing}, lines={lc}")

        if has_doctype and lc > 100:

            if not has_closing:

                tail = result[-500:]
                print(f"  File tail: {tail!r}")
                if '</body>' not in tail:
                    result = result + '\n</body>\n</html>'
                elif '</html>' not in tail:
                    result = result + '\n</html>'

            path = BASE / f'modulo {mod}' / 'index.html'
            path.write_text(result, encoding='utf-8')
            print(f"  SAVED ({result.count(chr(10))} lines)")
        else:
            print(f"  NOT SAVED - incomplete")
