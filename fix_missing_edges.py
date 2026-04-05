#!/usr/bin/env python3
"""
Merge missing edges into the current Dify YAML using raw string replacement.
No yaml.dump - reads and writes raw text only.
"""
import re, uuid, subprocess, yaml

INPUT = '/Users/himeshr/IdeaProjects/avni-ai/dify/App Configurator [Staging] v3.yml'

# The node ID remap: old named IDs -> UUIDs that Dify has on server
# These come from fix_node_uuids.py output (HEAD~2 commit)
REMAP = {
    'org-name-assigner':          'a2a567f5-2561-4d32-9e9a-bd87977bf876',
    'store-entities-node':        '25263b32-3d9c-48d8-8b65-a3ac59b09348',
    'build-patch-body-node':      '6a82d9d6-b4bb-469e-8ef3-2cead76406b6',
    'corrections-prompt-answer':  '2aec3688-840b-4764-9b24-053c481cf7cb',
    'progress-generating-spec':   '57618321-2885-4f02-8799-357f4c930787',
    'progress-downloading-bundle':'81598ae0-f377-4824-8d1d-dac6e3ee622d',
    'progress-uploading-bundle':  '3be38f48-21fd-4fc1-b683-afa0f1852d94',
    'spec-extractor-001':         'e5031c06-d598-41ea-89bd-418c8760ef12',
    'spec-saver-001':             '18c872d0-3910-476b-8125-41d3990fa66b',
    'upload-error-check':         '62b26511-73a8-409f-bd0e-a5ae10a0eca7',
    'upload-err-400-answer':      '6074d8af-a887-49c7-9600-cd7a39b7da9a',
    'upload-err-401-answer':      'df5ce36e-f8b2-4317-a9c5-7b2bc31dfdcc',
    'upload-err-403-answer':      '3253f6da-b185-4c99-9649-57b55121ad3c',
    'upload-err-404-answer':      '0913d6f0-d87d-4643-b696-b246007dc457',
    'upload-err-500-answer':      '44ab76d0-bb30-438b-921c-b71ef483066c',
    'check-bundle-verdict':       '83e06f10-4357-46e0-b0cc-242228740e6c',
    'check-error-verdict':        'c522b7ba-bf3c-40d8-82ec-870ac46f205f',
    'increment-retry-code':       '2cd3d54a-626b-4baa-86b5-fc244555cd38',
    'save-retry-count':           '0994a503-b86e-419f-925d-3bc1dc7db02c',
    'check-max-retries':          'c08d56f9-1ff9-462b-a3cf-e2de48566b82',
    'max-retries-exhausted-answer':'41dbefd6-cc48-49c2-ae2e-8444773c6404',
    'upload-error-report-answer': '58d9287e-6a07-4b76-8221-a2fe263566f0',
    'delete-confirm-prompt-answer':'045318f4-d7da-4963-90d0-98294cb60931',
    'delete-confirm-human-input': '12bd8582-9fed-48d1-9ea6-552c23c90ddb',
    'delete-implementation-http': 'b5f60a64-a35a-41f8-85e5-bc5fc632c445',
    'delete-result-check':        '47bbee22-967d-4206-8d2f-f639936f0304',
    'delete-success-answer':      '6877ddae-ae78-49e8-af6f-b0ac0e742daf',
    'delete-failure-answer':      'b1029877-df56-4bc2-b8fd-e5c7e01d4280',
    'delete-cancelled-answer':    '57544709-393a-4760-991b-fc0149ae7f67',
}

uuid_re = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.I)

def remap(val):
    return REMAP.get(str(val), str(val))

# Get git HEAD version edges (has old named IDs)
git_raw = subprocess.run(
    ['git', 'show', 'HEAD:dify/App Configurator [Staging] v3.yml'],
    capture_output=True, text=True, cwd='/Users/himeshr/IdeaProjects/avni-ai'
)
git_data = yaml.safe_load(git_raw.stdout)
git_edges = git_data['workflow']['graph']['edges']

# Load current file (what Dify has - 41 edges)
with open(INPUT) as f:
    current_text = f.read()
current_data = yaml.safe_load(current_text)
current_edge_ids = {e['id'] for e in current_data['workflow']['graph']['edges']}
current_node_ids = {n['id'] for n in current_data['workflow']['graph']['nodes']}

print(f"Current: {len(current_edge_ids)} edges, {len(current_node_ids)} nodes")

# Build missing edges with remapped IDs
missing_edge_yaml = []
added = 0
skipped = 0
for e in git_edges:
    eid = str(e['id'])
    # Skip if already present
    if eid in current_edge_ids:
        continue
    
    src = remap(e['source'])
    tgt = remap(e['target'])
    
    # Verify both nodes exist on server
    if src not in current_node_ids:
        print(f"  SKIP (src not found): {src}")
        skipped += 1
        continue
    if tgt not in current_node_ids:
        print(f"  SKIP (tgt not found): {tgt}")
        skipped += 1
        continue
    
    # Give a fresh UUID if edge id was named
    if not uuid_re.match(eid):
        eid = str(uuid.uuid4())
    
    # Build edge YAML block
    data = e.get('data', {})
    data_lines = ['    - data:']
    for k, v in data.items():
        if isinstance(v, bool):
            data_lines.append(f"        {k}: {'true' if v else 'false'}")
        elif isinstance(v, str):
            data_lines.append(f"        {k}: {v}")
        else:
            data_lines.append(f"        {k}: {v}")
    
    handle = e.get('sourceHandle', 'source')
    z = e.get('zIndex', 0)
    
    edge_block = f"""    - data:
"""
    for k, v in data.items():
        if isinstance(v, bool):
            edge_block += f"        {k}: {'true' if v else 'false'}\n"
        else:
            edge_block += f"        {k}: {v}\n"
    
    edge_block += f"""      id: {eid}
      selected: false
      source: '{src}'
      sourceHandle: {handle}
      target: '{tgt}'
      targetHandle: target
      type: custom
      zIndex: {z}
"""
    missing_edge_yaml.append(edge_block)
    added += 1
    print(f"  + {src[:20]} --[{handle}]--> {tgt[:20]}")

print(f"\nAdding {added} edges, skipping {skipped}")

if added == 0:
    print("Nothing to add.")
else:
    # Insert edges before the 'nodes:' line
    insertion = ''.join(missing_edge_yaml)
    # Find '    nodes:' and insert before it
    current_text = current_text.replace('    nodes:\n', insertion + '    nodes:\n', 1)
    
    with open(INPUT, 'w') as f:
        f.write(current_text)
    
    # Quick verify (count edge entries)
    edge_count = current_text.count('\n      id: ')
    print(f"Written. Approx edge+node id count: {edge_count}")
    
    # YAML parse check
    try:
        verify = yaml.safe_load(current_text)
        edges = verify['workflow']['graph']['edges']
        nodes = verify['workflow']['graph']['nodes']
        print(f"YAML valid: {len(edges)} edges, {len(nodes)} nodes")
    except Exception as ex:
        print(f"YAML parse error: {ex}")
