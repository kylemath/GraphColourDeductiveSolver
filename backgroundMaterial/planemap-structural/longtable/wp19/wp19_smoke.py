# Smoke test on already-analysed discovery graphs (orders 12-18); not a WP19 phase.
import json, sys, time
sys.path.insert(0, '.')
import wp19_run as R
m = json.load(open('../wp11-run-manifest.json'))
gs = [(g['order'], g['graph_index'], g['ascii']) for g in m['discovery_graphs']]
dl = time.monotonic() + 3600
graphs = [R.work((o, i, a, dl)) for o, i, a in gs]
out = {"phase": "SMOKE", "declaration": "WP19-preregistered-conjectures-declaration.md",
       "declaration_sha256": R.sha(R.DECL.read_bytes()),
       "source_sha256": {str(p.relative_to(R.ROOT)): R.sha(p.read_bytes()) for p in R.SOURCES},
       "input_sha256": "smoke", "caps": {"mixed": 6, "kempe": 7}, "truncated": False,
       "graphs": graphs, "summary": {}}
json.dump(out, open(sys.argv[1], 'w'))
print('graphs', len(graphs), 'm', sorted({(g['order'], g['graph_index']): g['m'] for g in graphs}.items())[-6:])
print('kills', [(g['order'], g['graph_index'], [k['stmt'] for k in g['kills']]) for g in graphs if g['kills']])
