"""
Extract the largest reads for each module and reconstruct full HTML.
Strategy: find the last FULL read (from line 1) for each module,
then apply all subsequent edits.
"""
import json, re
from pathlib import Path

JSONL = Path(r"C:\Users\AparicioJunior\.claude\projects\c--Users-AparicioJunior-workspace-saude-caminhoneiros\d69d46f7-64c8-484e-bfcd-8c71406dda50.jsonl")
BASE = Path(r"c:\Users\AparicioJunior\workspace\saude-caminhoneiros")

with open(JSONL, encoding='utf-8') as f:
    all_lines = f.readlines()

def get_tool_result_after(idx):
    """Get ALL tool_result items from the user messages after idx."""
    results = []
    for i in range(idx + 1, min(idx + 6, len(all_lines))):
        try:
            obj = json.loads(all_lines[i])
            tr = obj.get('toolUseResult')
            if tr:
                results.append(('TR', tr))
            msg = obj.get('message', {})
            for item in msg.get('content', []):
                if isinstance(item, dict) and item.get('type') == 'tool_result':
                    results.append(('MSG', item))
        except Exception:
            pass
    return results

def strip_linenum(text):
    lines = text.split('\n')
    out = []
    for line in lines:
        m = re.match(r'^\d+\t(.*)$', line)
        out.append(m.group(1) if m else line)
    return '\n'.join(out)

# Extract the M2 Read at JSONL line 580 (index 579)
print("=== Extracting M2 read at JSONL 580 ===")
for idx in range(578, 583):
    obj = json.loads(all_lines[idx])
    msg = obj.get('message', {})
    for item in msg.get('content', []):
        if isinstance(item, dict) and item.get('type') == 'tool_result':
            c = item.get('content', '')
            if len(c) > 1000:
                print(f"  JSONL line {idx+1}: {len(c)} chars")
                lines = c.split('\n')
                print(f"  First line: {lines[0][:100]}")
                print(f"  Last line: {lines[-1][:100]}")
                print(f"  Total lines in raw: {len(lines)}")
                # Get the last line number
                last_with_num = None
                for l in reversed(lines):
                    m = re.match(r'^(\d+)\t', l)
                    if m:
                        last_with_num = int(m.group(1))
                        break
                print(f"  Last line number shown: {last_with_num}")

print()

# Extract the M5 Read at JSONL line 601 (index 600)
print("=== Extracting M5 read at JSONL 601 ===")
for idx in range(599, 605):
    obj = json.loads(all_lines[idx])
    msg = obj.get('message', {})
    for item in msg.get('content', []):
        if isinstance(item, dict) and item.get('type') == 'tool_result':
            c = item.get('content', '')
            if len(c) > 1000:
                print(f"  JSONL line {idx+1}: {len(c)} chars")
                lines = c.split('\n')
                print(f"  First line: {lines[0][:100]}")
                print(f"  Last line: {lines[-1][:100]}")
                last_with_num = None
                for l in reversed(lines):
                    m = re.match(r'^(\d+)\t', l)
                    if m:
                        last_with_num = int(m.group(1))
                        break
                print(f"  Last line number shown: {last_with_num}")
