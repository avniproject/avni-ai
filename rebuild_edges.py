#!/usr/bin/env python3
"""Rebuild the complete YAML from Dify's fresh download + missing original edges,
with node ID remapping applied and correct dataset ID."""
import yaml, uuid, subprocess, sys

INPUT = '/Users/himeshr/IdeaProjects/avni-ai/dify/App Configurator [Staging] v3.yml'
CORRECT_DATASET_ID = 'df1bfaa2-38ad-457c-8237-6980e83245d9'

# Load fresh download (current state of file)
with open(INPUT) as f:
    fresh = yaml.safe_load(f)

fresh_node_ids = {n['id'] for n in fresh['workflow']['graph']['nodes']}
fresh_edge_ids = {e['id'] for e in fresh['workflow']['graph']['edges']}

# Build a map: old-named-id -> new-uuid from the fresh download's nodes
# The fresh download has nodes with UUIDs that replaced the named IDs.
# We need to know WHICH uuid replaced which named id.
# Strategy: get original YAML from git (before any UUID changes) and match by node title/type.

orig_raw = subprocess.run(
    ['git', 'show', 'HEAD~3:dify/App Configurator [Staging] v3.yml'],
    capture_output=True, text=True, cwd='/Users/himeshr/IdeaProjects/avni-ai'
)
orig = yaml.safe_load(orig_raw.stdout)
orig_nodes = {n['id']: n for n in orig['workflow']['graph']['nodes']}
orig_edges = orig['workflow']['graph']['edges']

# Build title+type -> uuid mapping from fresh nodes
fresh_by_title_type = {}
for n in fresh['workflow']['graph']['nodes']:
    key = (n['data'].get('title',''), n['data'].get('type',''))
    fresh_by_title_type[key] = n['id']

# Build old-id -> new-uuid remap
remap = {}
for old_id, on in orig_nodes.items():
    key = (on['data'].get('title',''), on['data'].get('type',''))
    new_id = fresh_by_title_type.get(key)
    if new_id and old_id != new_id:
        remap[old_id] = new_id
    elif old_id == new_id or new_id is None:
        remap[old_id] = old_id  # unchanged

print("Node ID remap:")
for old, new in remap.items():
    if old != new:
        print(f"  {old} -> {new}")

# Find missing edges
missing_edges = [e for e in orig_edges if e['id'] not in fresh_edge_ids]
print(f"\nMissing edges to add: {len(missing_edges)}")

def remap_id(val):
    val = str(val)
    return remap.get(val, val)

# Rebuild missing edges with remapped source/target
new_edges = []
for e in missing_edges:
    new_e = dict(e)
    old_src = str(e['source'])
    old_tgt = str(e['target'])
    new_src = remap_id(old_src)
    new_tgt = remap_id(old_tgt)
    new_e['source'] = new_src
    new_e['target'] = new_tgt
    # Give it a fresh UUID id if it had a named/invalid id
    import re
    uuid_re = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.I)
    if not uuid_re.match(new_e['id']):
        new_e['id'] = str(uuid.uuid4())
    print(f"  + {new_src[:16]} --[{e.get('sourceHandle','')}]--> {new_tgt[:16]}")
    new_edges.append(new_e)

# Add missing edges to fresh download
fresh['workflow']['graph']['edges'].extend(new_edges)

# Fix dataset ID
for n in fresh['workflow']['graph']['nodes']:
    if n['data'].get('type') == 'knowledge-retrieval':
        n['data']['dataset_ids'] = [CORRECT_DATASET_ID]
        print(f"\nFixed dataset ID on node {n['id']}")

# Fix app name
fresh['app']['name'] = 'App Configurator [Staging] v3'

total_edges = len(fresh['workflow']['graph']['edges'])
total_nodes = len(fresh['workflow']['graph']['nodes'])
print(f"\nFinal: {total_edges} edges, {total_nodes} nodes")

with open(INPUT, 'w') as f:
    yaml.dump(fresh, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

print("Written to", INPUT)
