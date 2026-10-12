#!/usr/bin/env python3
"""Track Q: extract the exact-surgery data of the first law R-cycle of each graph (tn_eng --dump):
colourings of the cycle states, pair-graph parts, ground set U of admissible edges, forced link edges.
usage: tq_data.py FILE OUTDIR   (FILE: graph lines 'name n adj;...', h = 0)  -> OUTDIR/<name>_data.json"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from tn_lib import Engine
from tn_forest import parse_dump, cycles_in_R_law
from tq_exact import build
ed = Engine(dump=True, maxstates=200000)
for l in open(sys.argv[1]):
    if l.startswith('{'): l = json.loads(l)['graph']
    p = l.split()
    if len(p) < 3: continue
    rot = [list(map(int, r.split(','))) for r in p[2].split(';')]
    n = len(rot); E = {frozenset((u, v)) for u in range(1, n) for v in rot[u] if v != 0}
    js, tn, dump = ed.run(l); S = parse_dump(dump); cyc = cycles_in_R_law(S)
    if not cyc: print('no law cycle', p[0]); continue
    C = cyc[0]; cols = [[-1 if ch == '-' else int(ch) for ch in S[x]['col']] for x in C]
    U, parts, forced = build(n, E, cols)
    d = dict(src=p[0], n=n, graph=l.strip(), ncyc=len(cyc), Nprof=''.join(str(S[x]['N']) for x in C), E=sorted(tuple(sorted(e)) for e in E),
             cols=cols, U=U, parts=[(t, a, b, sorted(P)) for t, a, b, P in parts], forced=forced)
    json.dump(d, open(os.path.join(sys.argv[2], p[0] + '_data.json'), 'w'))
    print(p[0], 'n', n, '|E|', len(E), 'e', len(E) - (3 * (n - 1) - 8), 'U', len(U), 'parts', len(parts), 'cycles', len(cyc), d['Nprof'])
