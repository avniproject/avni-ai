#!/usr/bin/env python3
"""Replace non-UUID edge IDs in the Dify YAML with valid UUIDv4 values."""
import re, uuid

uuid_re = re.compile(
    r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.I
)

INPUT = '/Users/himeshr/IdeaProjects/avni-ai/dify/App Configurator [Staging] v3.yml'

with open(INPUT) as f:
    lines = f.readlines()

# Locate edges section boundaries
in_edges = False
edges_start = edges_end = None
for i, line in enumerate(lines):
    if re.match(r'^    edges:\s*$', line):
        in_edges = True
        edges_start = i
    elif in_edges and re.match(r'^    nodes:\s*$', line):
        edges_end = i
        break

print(f"Edges section: lines {edges_start}–{edges_end}")

# Within edges section, replace `      id: <non-uuid>` lines
replaced = 0
for i in range(edges_start, edges_end):
    m = re.match(r'^(      id: )(.+)(\n?)$', lines[i])
    if m:
        val = m.group(2).strip()
        if not uuid_re.match(val):
            new_id = str(uuid.uuid4())
            lines[i] = m.group(1) + new_id + m.group(3)
            replaced += 1

print(f"Replaced {replaced} edge IDs")

with open(INPUT, 'w') as f:
    f.writelines(lines)

print("Done.")
