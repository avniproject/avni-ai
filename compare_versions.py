#!/usr/bin/env python3
"""
Compare OLD (user's introduced changes) vs NEW (dify/ canonical) workflow files.
Identify what's in OLD that's missing or different in NEW.
"""
import yaml, json

OLD = '/Users/himeshr/IdeaProjects/avni-ai/App Configurator [Staging] v3 old.yml'
NEW = '/Users/himeshr/IdeaProjects/avni-ai/dify/App Configurator [Staging] v3.yml'

old = yaml.safe_load(open(OLD))
new = yaml.safe_load(open(NEW))

old_nodes = {str(n['id']): n for n in old['workflow']['graph']['nodes']}
new_nodes = {str(n['id']): n for n in new['workflow']['graph']['nodes']}

# Known remap: old named IDs -> new UUIDs
REMAP = {
    '1774617440956start':             '47e94f80-07ea-4cf9-b0e3-36875cb6a80c',
    'd7e8f9a0-b1c2-4d3e-f4a5-b6c7d8e9f0a1': 'a3d80a70-5da7-4edc-9c32-66de6f9845e1',
    'spec-extractor-001':             '0e3ec62b-9e28-4d64-b0f6-60d5c6fb1a1c',
    'spec-saver-001':                 '61246b3d-16a0-4768-8b58-d9d3aa1c0441',
    'store-entities-node':            'ecd0bd72-6c77-4fb8-a362-0164343614af',
}

print(f"OLD: {len(old_nodes)} nodes, {len(old['workflow']['graph']['edges'])} edges")
print(f"NEW: {len(new_nodes)} nodes, {len(new['workflow']['graph']['edges'])} edges")

# For each node in OLD, find counterpart in NEW and check data diff
print("\n=== Node data differences (OLD vs NEW) ===")
diffs = []
for old_id, old_node in old_nodes.items():
    new_id = REMAP.get(old_id, old_id)
    if new_id in new_nodes:
        old_data = json.dumps(old_node.get('data', {}), sort_keys=True)
        new_data = json.dumps(new_nodes[new_id].get('data', {}), sort_keys=True)
        if old_data != new_data:
            diffs.append((old_id, new_id, old_node['data'].get('title', '')))
            # Show what's different
            old_d = old_node.get('data', {})
            new_d = new_nodes[new_id].get('data', {})
            all_keys = set(old_d) | set(new_d)
            for k in sorted(all_keys):
                ov = json.dumps(old_d.get(k, '<MISSING>'), sort_keys=True)
                nv = json.dumps(new_d.get(k, '<MISSING>'), sort_keys=True)
                if ov != nv:
                    # Truncate long values
                    ov_s = ov[:80] + '...' if len(ov) > 80 else ov
                    nv_s = nv[:80] + '...' if len(nv) > 80 else nv
                    print(f"  [{old_node['data'].get('title',old_id)}] .{k}")
                    print(f"    OLD: {ov_s}")
                    print(f"    NEW: {nv_s}")

if not diffs:
    print("  No data differences — OLD node content matches NEW exactly.")

# Nodes in OLD not covered by remap or direct match
missing_from_new = [old_id for old_id in old_nodes if REMAP.get(old_id, old_id) not in new_nodes]
print(f"\n=== Nodes in OLD with no counterpart in NEW ({len(missing_from_new)}) ===")
for nid in missing_from_new:
    n = old_nodes[nid]
    print(f"  {nid} [{n['data'].get('type','')}] {n['data'].get('title','')}")
