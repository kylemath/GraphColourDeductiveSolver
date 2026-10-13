"""Cross-check of r0enum.py against the SAT normal form of PROOF-ATTEMPT-1 (sat_t1v.Enc with no loops/cuts =
R0 without planarity): enumerate all (chord set, labels f1 f3 f4) admitting a closed R0 sequence of length
exactly L, and compare with the r0enum records having L in R0_L.  usage: xcheck_sat.py n L"""
import sys, json
sys.path.insert(0, '../proof')
from sat_t1v import Enc
from pysat.solvers import Cadical153
n, L = int(sys.argv[1]), int(sys.argv[2])
enc = Enc(n, L, 0, eager=0, closed=True)
s = Cadical153(bootstrap_with=enc.cl)
sat = set()
while s.solve():
    E, M, fv = enc.decode(s.get_model())
    ch = frozenset(enc.edges[e] for e in E if enc.X[e] is not None and 0 not in enc.edges[e])
    lab = tuple(max(enc.edges[fv[x]]) for x in (1, 3, 4))
    sat.add((ch, lab))
    s.add_clause([-enc.X[e] for e in E if enc.X[e] is not None] + [-enc.lab[x][fv[x]] for x in (1, 3, 4)])
mine = set()
for l in open(f'out/r0enum_n{n}.jsonl'):
    d = json.loads(l)
    if L not in d['R0_L']: continue
    t = list(map(int, d['line'].split())); m = t[1]
    E = [(t[2 + 2 * i], t[3 + 2 * i]) for i in range(m)]; fv = t[2 + 2 * m:]
    ch = frozenset(tuple(sorted(e)) for e in E[n:] if 0 not in e)
    lab = tuple(max(E[fv[x]]) for x in (1, 3, 4))
    mine.add((ch, lab))
print(f'n={n} L={L}: SAT {len(sat)}  r0enum {len(mine)}  equal {sat == mine}')
