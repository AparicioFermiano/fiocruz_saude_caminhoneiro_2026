"""
Reconstruct module HTML files using structured patches from JSONL.
The structuredPatch in toolUseResult shows the complete diff for each edit.
By applying all patches to an empty base, we can reconstruct each file.
"""
import json
from pathlib import Path

JSONL = Path(r"C:\Users\AparicioJunior\.claude\projects\c--Users-AparicioJunior-workspace-saude-caminhoneiros\d69d46f7-64c8-484e-bfcd-8c71406dda50.jsonl")
BASE = Path(r"c:\Users\AparicioJunior\workspace\saude-caminhoneiros")

with open(JSONL, encoding='utf-8') as f:
    all_lines = f.readlines()

def reconstruct_from_patch(structured_patch):
    """
    Reconstruct the AFTER-edit content from a structuredPatch.
    Each hunk has {oldStart, oldLines, newStart, newLines, lines: [...]}.
    Lines starting with '+' are new, ' ' are context (kept), '-' are removed.
    Collect '+' and ' ' lines to get the new content.
    """
    result_lines = []
    for hunk in structured_patch:
        lines = hunk.get('lines', [])
        for line in lines:
            if isinstance(line, str):
                if line.startswith('+') or line.startswith(' '):
                    result_lines.append(line[1:])
    return '\n'.join(result_lines)

def reconstruct_before_from_patch(structured_patch):
    """Reconstruct the BEFORE-edit content from a structuredPatch."""
    result_lines = []
    for hunk in structured_patch:
        lines = hunk.get('lines', [])
        for line in lines:
            if isinstance(line, str):
                if line.startswith('-') or line.startswith(' '):
                    result_lines.append(line[1:])
    return '\n'.join(result_lines)

def get_all_edits_with_patches(mod):
    """Return list of (jsonl_line, old_string, new_string, structured_patch) for a module."""
    results = []
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

                            for j in range(i+1, min(i+5, len(all_lines))):
                                res_obj = json.loads(all_lines[j])
                                tr = res_obj.get('toolUseResult', {})
                                if tr and tr.get('filePath', ''):
                                    patch = tr.get('structuredPatch', [])
                                    results.append((i+1, old, new, patch))
                                    break
        except Exception:
            pass
    return results

for mod in range(2, 6):
    edits = get_all_edits_with_patches(mod)
    if not edits:
        print(f"M{mod}: No edits found with patches")
        continue

    print(f"M{mod}: {len(edits)} edits found")

    last_good = None
    for edit_data in reversed(edits):
        _, old, new, patch = edit_data
        if patch:
            last_good = edit_data
            break

    if last_good:
        jsonl_line, old, new, patch = last_good
        after_content = reconstruct_from_patch(patch)
        lc = after_content.count('\n')
        print(f"  Last edit at JSONL {jsonl_line}: patch reconstructs {lc} lines, {len(after_content)} chars")
        print(f"  Preview: {after_content[:200]}")

        if '<!DOCTYPE html>' in after_content and '</html>' in after_content:
            path = BASE / f'modulo {mod}' / 'index.html'
            path.write_text(after_content, encoding='utf-8')
            print(f"  SAVED complete HTML")
        else:
            print(f"  NOT a complete HTML file")
    else:
        print(f"  No edits with non-empty patches")
