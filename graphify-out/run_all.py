import sys, json, glob
from pathlib import Path
from graphify.detect import detect, save_manifest
from graphify.extract import collect_files, extract
from graphify.build import build_from_json
from graphify.cluster import cluster, score_all
from graphify.analyze import god_nodes, surprising_connections, suggest_questions
from graphify.report import generate
from graphify.export import to_json
from graphify.diagnostics import diagnose_extraction, format_diagnostic_report
from datetime import datetime, timezone
from graphify.cli import _stamped_manifest_files

root = Path('.')
print("Detecting...")
detection = detect(root)
Path('graphify-out/.graphify_detect.json').write_text(json.dumps(detection, ensure_ascii=False), encoding='utf-8-sig')

code_files = []
for f in detection.get('files', {}).get('code', []):
    code_files.extend(collect_files(Path(f)) if Path(f).is_dir() else [Path(f)])

print("Extracting...")
if code_files:
    ast = extract(code_files, cache_root=root)
else:
    ast = {'nodes':[],'edges':[],'input_tokens':0,'output_tokens':0}

sem = {'nodes':[],'edges':[],'hyperedges':[],'input_tokens':0,'output_tokens':0}

# Merge
seen = {n['id'] for n in ast['nodes']}
merged_nodes = list(ast['nodes'])
for n in sem['nodes']:
    if n['id'] not in seen:
        merged_nodes.append(n)
        seen.add(n['id'])

merged_edges = ast['edges'] + sem['edges']
merged = {
    'nodes': merged_nodes,
    'edges': merged_edges,
    'hyperedges': sem.get('hyperedges', []),
    'input_tokens': sem.get('input_tokens', 0),
    'output_tokens': sem.get('output_tokens', 0),
}
Path('graphify-out/.graphify_extract.json').write_text(json.dumps(merged, indent=2, ensure_ascii=False), encoding='utf-8')
print(f"Merged: {len(merged_nodes)} nodes, {len(merged_edges)} edges")

print("Building graph...")
G = build_from_json(merged, root=root, directed=False)
if G.number_of_nodes() == 0:
    print('ERROR: Graph is empty - extraction produced no nodes.')
    sys.exit(1)

communities = cluster(G)
cohesion = score_all(G, communities)
tokens = {'input': merged.get('input_tokens', 0), 'output': merged.get('output_tokens', 0)}
gods = god_nodes(G)
surprises = surprising_connections(G, communities)
labels = {cid: 'Community ' + str(cid) for cid in communities}
questions = suggest_questions(G, communities, labels)

to_json(G, communities, 'graphify-out/graph.json')

# Diagnostics
summary = diagnose_extraction(merged, directed=False, root='.')
flags = [f'{summary[k]} {label}' for k, label in (
    ('dangling_endpoint_edges', 'dangling-endpoint edges'),
    ('missing_endpoint_edges', 'missing-endpoint edges'),
    ('self_loop_edges', 'self-loop edges'),
    ('directed_same_endpoint_collapsed_edges', 'collapsed (directed) edges'),
    ('undirected_same_endpoint_collapsed_edges', 'collapsed (undirected) edges'),
) if summary.get(k, 0)]
if flags:
    print('GRAPH HEALTH WARNING: ' + '; '.join(flags))

report = generate(G, communities, cohesion, labels, gods, surprises, detection, tokens, root, suggested_questions=questions)
Path('graphify-out/GRAPH_REPORT.md').write_text(report, encoding="utf-8")

# Manifest
_corpus = detection.get('all_files') or detection['files']
_manifest_files = _stamped_manifest_files(_corpus, merged, root)
_sem_types = ('document', 'paper', 'image')
_dispatched = {f for t, fl in detection['files'].items() if t in _sem_types for f in fl}
_stamped = {f for fl in _manifest_files.values() for f in fl}
_cleared = _dispatched - _stamped
_scan = {f for fl in _corpus.values() for f in fl}
save_manifest(_manifest_files, root=root, scan_corpus=_scan, clear_semantic=_cleared or None)

cost_path = Path('graphify-out/cost.json')
if cost_path.exists():
    cost = json.loads(cost_path.read_text(encoding="utf-8"))
else:
    cost = {'runs': [], 'total_input_tokens': 0, 'total_output_tokens': 0}

cost['runs'].append({
    'date': datetime.now(timezone.utc).isoformat(),
    'input_tokens': tokens['input'],
    'output_tokens': tokens['output'],
    'files': detection.get('total_files', 0),
})
cost['total_input_tokens'] += tokens['input']
cost['total_output_tokens'] += tokens['output']
cost_path.write_text(json.dumps(cost, indent=2, ensure_ascii=False), encoding="utf-8")
print("Done.")
