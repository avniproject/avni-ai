#!/usr/bin/env python3
"""
Full UUIDv4 remap: replace ALL non-UUIDv4 node IDs with deterministic UUIDv4 values,
then update all references (edges source/target, variable_selectors) consistently.
Uses raw text replacement — no yaml.dump.
"""
import re, uuid, random, yaml

INPUT  = '/Users/himeshr/IdeaProjects/avni-ai/dify/App Configurator [Staging] v3.yml'
OUTPUT = '/Users/himeshr/Downloads/AppConfigV3_final.yml'

uuid4_re = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$', re.I)

def make_v4(seed_str):
    """Deterministic UUIDv4 from a seed string."""
    rng = random.Random(seed_str)
    return str(uuid.UUID(int=rng.getrandbits(128), version=4))

# Load YAML to get node IDs
data = yaml.safe_load(open(INPUT))
nodes = data['workflow']['graph']['nodes']

# Build remap for every non-UUIDv4 node ID
remap = {}
for n in nodes:
    nid = str(n['id'])
    if not uuid4_re.match(nid):
        title = n.get('data', {}).get('title', '')
        ntype = n.get('data', {}).get('type', '')
        remap[nid] = make_v4(f"{nid}::{title}::{ntype}")

print(f"Remapping {len(remap)} non-UUIDv4 node IDs:")
for old, new in remap.items():
    print(f"  {old} -> {new}")

# Read raw text
with open(INPUT) as f:
    text = f.read()

# Replace node IDs in text, longest first to avoid partial matches
for old_id in sorted(remap, key=len, reverse=True):
    new_id = remap[old_id]
    escaped = re.escape(old_id)
    text = re.sub(r'(?<![a-zA-Z0-9_\-])' + escaped + r'(?![a-zA-Z0-9_\-])', new_id, text)

# Replace non-UUIDv4 edge IDs (in edges section only)
lines = text.splitlines(keepends=True)
in_edges = False
for i, line in enumerate(lines):
    if re.match(r'^    edges:\s*$', line):
        in_edges = True
    elif re.match(r'^    nodes:\s*$', line):
        in_edges = False
    if in_edges:
        m = re.match(r'^(      id: )(.+)\n?$', line)
        if m:
            val = m.group(2).strip().strip("'\"")
            if not uuid4_re.match(val):
                lines[i] = m.group(1) + make_v4(f"edge::{val}") + '\n'

text = ''.join(lines)

with open(OUTPUT, 'w') as f:
    f.write(text)

# Verify
print("\nVerifying...")
data2 = yaml.safe_load(open(OUTPUT))
edges2 = data2['workflow']['graph']['edges']
nodes2 = data2['workflow']['graph']['nodes']

bad_nids  = [n['id'] for n in nodes2 if not uuid4_re.match(str(n['id']))]
bad_eids  = [e['id'] for e in edges2 if not uuid4_re.match(str(e['id']))]
bad_srcs  = [(e['id'][:8], e['source']) for e in edges2 if not uuid4_re.match(str(e['source']))]
bad_tgts  = [(e['id'][:8], e['target']) for e in edges2 if not uuid4_re.match(str(e['target']))]

print(f"Nodes : {len(nodes2)} total | bad ids: {len(bad_nids)}")
print(f"Edges : {len(edges2)} total | bad ids: {len(bad_eids)} | bad src: {len(bad_srcs)} | bad tgt: {len(bad_tgts)}")
for x in bad_nids[:5]:  print(f"  BAD NODE: {x}")
for x in bad_srcs[:5]:  print(f"  BAD SRC:  {x}")
for x in bad_tgts[:5]:  print(f"  BAD TGT:  {x}")

if not bad_nids and not bad_eids and not bad_srcs and not bad_tgts:
    print(f"\nSUCCESS — {OUTPUT}")
else:
    print("\nWARNING: some IDs still non-UUIDv4")
