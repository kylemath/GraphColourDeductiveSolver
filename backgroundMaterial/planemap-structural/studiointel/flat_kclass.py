#!/usr/bin/env python3
"""studiointel flat_kclass.py -- [exploratory] flat-annulus test (Math 16:15 item (c)): for each graph, each degree-5 hole v, flat(v) =
largest r such that every vertex at distance 1..r from v has degree 6. For holes with flat >= MINFLAT: kappa(T - v) = number of Kempe
classes of canonical 4-colourings of T - v (fast/kempe_classes), with per-class (size, #filled, #DL). Alerts on kappa >= 2.
usage: flat_kclass.py OUT.jsonl MINFLAT graph.json ..."""
import sys, os, json, subprocess, tempfile
sys.path.insert(0, '.')
import graphs
BIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fast', 'kempe_classes')
def flat(adj, v):
    deg = {u: len(a) for u, a in adj.items()}; seen = {v}; layer = [v]; r = 0
    while True:
        nxt = sorted({w for u in layer for w in adj[u]} - seen)
        if not nxt or any(deg[w] != 6 for w in nxt): return r
        seen |= set(nxt); layer = nxt; r += 1
if __name__ == '__main__':
    out = open(sys.argv[1], 'a'); mf = int(sys.argv[2])
    for p in sys.argv[3:]:
        F = [tuple(f) for f in json.load(open(p))['faces']]; adj = graphs.adjacency(F)
        labels = sorted(adj); m = {u: i for i, u in enumerate(labels)}
        holes = [(v, flat(adj, v)) for v in labels if len(adj[v]) == 5]
        print(p, 'flat profile', sorted(f for _, f in holes), flush=True)
        for v, fl in holes:
            if fl < mf: continue
            with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as fh:
                fh.write('%d %d\n' % (len(labels), len(F)))
                for f in F: fh.write('%d %d %d\n' % tuple(m[x] for x in f))
            r = json.loads(subprocess.run([BIN, fh.name, str(m[v]), '2000000000'], capture_output=True, text=True).stdout)
            os.unlink(fh.name)
            row = {'graph': p, 'hole': v, 'flat': fl, **r}; out.write(json.dumps(row) + '\n'); out.flush()
            print(json.dumps({k: row[k] for k in row if k != 'classes'}), 'classes', len(r.get('classes', [])), flush=True)
            if r.get('n_classes', 1) >= 2: print('ALERT multi-class', p, v, flush=True)
