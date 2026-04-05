#!/usr/bin/env python3
"""Replace new named (non-UUID, non-numeric) node IDs with valid UUIDv4 values,
updating all references in both nodes and edges sections."""
import re, uuid, yaml

INPUT = '/Users/himeshr/IdeaProjects/avni-ai/dify/App Configurator [Staging] v3.yml'

uuid_re = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.I)
num_re = re.compile(r'^\d+$')

# Load to find which node IDs need replacing
with open(INPUT) as f:
    content = f.read()

data = yaml.safe_load(content)
nodes = data['workflow']['graph']['nodes']

# Build replacement map: old_id -> new_uuid
# Only replace named (non-numeric, non-UUID, non loop-start) node IDs
replacements = {}
for n in nodes:
    nid = str(n['id'])
    if not uuid_re.match(nid) and not num_re.match(nid) and not nid.endswith('start'):
        replacements[nid] = str(uuid.uuid4())

print(f"Replacing {len(replacements)} node IDs:")
for old, new in replacements.items():
    print(f"  {old} -> {new}")

# Replace all occurrences in the entire file content
# Use word-boundary-aware replacement to avoid partial matches
new_content = content
for old, new in replacements.items():
    # Replace as bare YAML value (surrounded by whitespace/quotes/newline/colon)
    # Patterns where node IDs appear:
    #   id: <id>
    #   source: <id>
    #   target: <id>
    #   - <id>          (variable_selector lists)
    # Use a pattern that matches the id as a whole word token
    escaped = re.escape(old)
    new_content = re.sub(
        r'(?<![a-zA-Z0-9_-])' + escaped + r'(?![a-zA-Z0-9_-])',
        new,
        new_content
    )

with open(INPUT, 'w') as f:
    f.write(new_content)

# Verify
data2 = yaml.safe_load(new_content)
nodes2 = data2['workflow']['graph']['nodes']
edges2 = data2['workflow']['graph']['edges']

still_bad_nodes = [n['id'] for n in nodes2
                   if not uuid_re.match(str(n['id'])) and not num_re.match(str(n['id'])) and not str(n['id']).endswith('start')]
still_bad_edges = [e['id'] for e in edges2 if not uuid_re.match(str(e['id']))]

print(f"\nRemaining non-UUID node IDs: {len(still_bad_nodes)}")
for x in still_bad_nodes: print(f"  {x}")
print(f"Remaining non-UUID edge IDs: {len(still_bad_edges)}")
for x in still_bad_edges: print(f"  {x}")
print("YAML valid: OK")
