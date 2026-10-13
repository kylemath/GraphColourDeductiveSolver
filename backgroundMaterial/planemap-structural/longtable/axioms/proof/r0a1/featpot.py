"""Shared-weight potential search: phi(M) = w . feat(M) with features read off the normal form (H = 0..n-1):
#even H-edges (M0-type), #odd H-edges (M1-type), #inside cubic chords, #outside cubic chords (sides from a
valid circle 2-colouring, f1 inside), one-hot v-edge index.  LP: phi(M') - phi(M) >= 1 on every arc of D of
every census class.  usage: featpot.py n1 n2 ..."""
import sys, json
import numpy as np, networkx as nx
from scipy.optimize import linprog
from r0lib import G5, analyse

def sides(g):
    n = g.n
    VPOS = {4: n + .25, 1: n + .5, 3: n + .75}
    items = {}
    for e, (a, b) in enumerate(g.E):
        if e in g.fidx:
            s = g.fidx[e]
            if s in (1, 3, 4): items[e] = (g.other(e, 0), VPOS[s])
        elif abs(a - b) != 1: items[e] = tuple(sorted((a, b)))
    def cross(c, d):
        a1, b1 = c; a2, b2 = d
        if len({a1, b1, a2, b2}) < 4: return False
        return (a1 < a2 < b1) != (a1 < b2 < b1)
    cg = nx.Graph(); cg.add_nodes_from(items)
    ks = list(items)
    for i in range(len(ks)):
        for j in range(i + 1, len(ks)):
            if cross(items[ks[i]], items[ks[j]]): cg.add_edge(ks[i], ks[j])
    f1, f3, f4 = g.fv[1], g.fv[3], g.fv[4]
    cg.add_edge(f1, f3); cg.add_node('d'); cg.add_edge(f3, 'd'); cg.add_edge('d', f4)
    col = {}
    for comp in [nx.node_connected_component(cg, f1)] + [c for c in nx.connected_components(cg) if f1 not in c]:
        root = f1 if f1 in comp else next(iter(comp))
        col[root] = 0
        for a, b in nx.bfs_edges(cg, root): col[b] = 1 - col[a]
    return {e: col[e] for e in items if e not in g.fidx}   # 0 = inside (f1 side)

rows = []
for n in map(int, sys.argv[1:]):
    for l in open(f'out/census_n{n}_p.jsonl'):
        r = json.loads(l); g = G5(r['n'], [tuple(e) for e in r['edges']], r['fv'])
        sd = sides(g); A = analyse(g)
        def feat(M):
            f = np.zeros(9)
            for e in range(g.m):
                if not (M >> e & 1): continue
                a, b = g.E[e]
                if e in g.fidx: f[4 + g.fidx[e]] += 1
                elif abs(a - b) == 1: f[0 if min(a, b) % 2 == 0 else 1] += 1
                else: f[2 + sd[e]] += 1
            return f
        F = [feat(M) for M in A['P']]
        for i, j in A['arcs']: rows.append(F[i] - F[j])
res = linprog(np.zeros(9), A_ub=np.array(rows), b_ub=-np.ones(len(rows)), bounds=[(None, None)] * 9, method='highs')
print(len(rows), 'arcs; LP status', res.status, res.message[:60], res.x if res.status == 0 else '')
