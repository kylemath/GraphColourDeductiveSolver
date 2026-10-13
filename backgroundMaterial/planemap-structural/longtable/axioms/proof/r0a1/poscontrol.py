"""Positive control for r0sat.py: put the planar C30#0 graph (Ham cycle only through ADJACENT v-edges) into
the 'adj' normal form (H through f0, f1) and fix its chords; the closed L = 20 walk of D must be found (SAT),
with the planarity clauses on.  Also: the same graph in 'adj' mode with L = 10 must be UNSAT (D has only the
20-cycle).  usage: poscontrol.py"""
import time
from pysat.solvers import Glucose4
from c30 import from_line, TU
from r0sat import R0Enc, verify

g = from_line(open(TU).readline()); n = g.n
# a Hamiltonian cycle through f0 and f1: leave v by f1, return by f0
start, end = g.other(g.fv[1], 0), g.other(g.fv[0], 0)
path = None
vis = [False] * n; vis[0] = vis[start] = True; cur = [start]
def dfs(x):
    global path
    if path: return
    if x == end and len(cur) == n - 1: path = list(cur); return
    for e in g.inc[x]:
        y = g.other(e, x)
        if not vis[y]:
            vis[y] = True; cur.append(y); dfs(y); cur.pop(); vis[y] = False
dfs(start)
pos = {0: 0}; pos.update({x: i + 1 for i, x in enumerate(path)})
chords = []; vch = {}
Hset = {frozenset((path[i], path[i + 1])) for i in range(n - 2)}
for e, (a, b) in enumerate(g.E):
    if e in g.fidx:
        s = g.fidx[e]
        if s in (2, 3, 4): vch[s] = pos[g.other(e, 0)]
    elif frozenset((a, b)) not in Hset:
        chords.append(tuple(sorted((pos[a], pos[b]))))
print('C30#0 in adj normal form: v-chords', vch, '#cubic chords', len(chords))
for L in (20, 10):
    enc = R0Enc(n, L, 'adj', True, True)
    units = []
    for e in enc.pe:
        if enc.pres[e] is None: continue
        if e[0] == 'c': units.append(enc.pres[e] if (e[1], e[2]) in chords else -enc.pres[e])
        else: units.append(enc.pres[e] if vch[int(e[0][1])] == e[2] else -enc.pres[e])
    t0 = time.time()
    s = Glucose4(bootstrap_with=enc.clauses() + [[u] for u in units])
    r = s.solve()
    print(f'L={L}: {"SAT" if r else "UNSAT"} ({time.time()-t0:.1f}s)')
    if r:
        edges, N = enc.decode(s.get_model()); info, _ = verify(enc, edges, N); print('   verify:', info)
