#!/usr/bin/env python3
"""studiointel causal_test.py -- [exploratory] does removing the small reducible configurations (RSST #0 Birkhoff diamond, ring 6;
RSST #1 = 2.122, ring 7) change the radius at a radius-5 hole? For each certificate graph: seeded greedy flips (core class kept:
min degree >= 5, max degree <= 8, no separating triangle; flips may not change the degree of the hole or of any link vertex) that strictly reduce the number of occurrences of configs #0 and #1,
until none remain (or no reducing flip exists). Then the exact radius (fast engine) at the former radius-5 hole (if still degree 5)
and the max over all degree-5 holes. Several seeds per graph."""
import sys, os, json, random
sys.path.insert(0, 'routeb'); sys.path.insert(0, 'fast')
import graphs, radius, fast, rsst_parse, rsst_contain as RC

confs = rsst_parse.parse('routeb/rsst/unavoidable.conf'); P = [RC.prep_conf(confs[i]) for i in (0, 1)]

def count_occ(F, P_, cap=1000):
    adj = graphs.adjacency(F); tf = {frozenset(f) for f in F}; degT = {u: len(a) for u, a in adj.items()}
    order = P_['order']; found = set(); phi = {}; used = set()
    def rec(i):
        if len(found) >= cap: return
        if i == len(order):
            if all(frozenset(phi[x] for x in f) in tf for f in P_['faces']): found.add(frozenset(phi.values()))
            return
        u = order[i]; placed = order[:i]; nbr = [w for w in placed if w in P_['E'][u]]
        for t in (adj[phi[nbr[0]]] if nbr else adj.keys()):
            if t in used or degT[t] != P_['deg'][u]: continue
            if any((w in P_['E'][u]) != (phi[w] in adj[t]) for w in placed): continue
            phi[u] = t; used.add(t); rec(i + 1); del phi[u]; used.discard(t)
    rec(0); return len(found)

def occ(F): return count_occ(F, P[0]) + count_occ(F, P[1])

def legal(F):
    dg = graphs.degrees(F)
    return min(dg.values()) >= 5 and max(dg.values()) <= 8 and graphs.n_separating_triangles(F) == 0

def clean(F, rng, maxsteps=40, protect=frozenset()):
    cur = F; c = occ(cur); steps = 0
    while c > 0 and steps < maxsteps:
        es = sorted({(min(f[i], f[(i + 1) % 3]), max(f[i], f[(i + 1) % 3])) for f in cur for i in range(3)}); rng.shuffle(es)
        best = None
        for a, b in es:
            if a in protect or b in protect: continue
            fa = [f for f in cur if a in f and b in f]; cd = {x for f in fa for x in f} - {a, b}
            if cd & protect: continue
            nf = graphs.flip(cur, a, b)
            if nf is None or not legal(nf): continue
            c2 = occ(nf)
            if c2 < c: best = (c2, nf); break
        if best is None: return cur, c, steps
        c, cur = best; steps += 1
    return cur, c, steps

if __name__ == '__main__':
    out = open(sys.argv[1], 'w'); seeds = int(sys.argv[2])
    for spec in sys.argv[3:]:
        path, hole = spec.split(':'); hole = int(hole)
        F = [tuple(f) for f in json.load(open(path))['faces']]
        base = fast.analyse(F, hole)['rho']
        for s in range(seeds):
            rng = random.Random(1000 * s + hole); prot = frozenset(graphs.adjacency(F)[hole] | {hole}); G, c, steps = clean(F, rng, protect=prot)
            dg = graphs.degrees(G); row = {'graph': path.split('/')[-1][:16], 'hole': hole, 'seed': s, 'rho_before': base, 'occ_left': c, 'flips': steps}
            if c == 0:
                row['hole_degree_after'] = dg[hole]
                row['rho_hole_after'] = fast.analyse(G, hole)['rho'] if dg[hole] == 5 else None
                rh = {h: fast.analyse(G, h)['rho'] for h in sorted(dg) if dg[h] == 5}
                row['max_rho_after'] = max((99 if v is None else v) for v in rh.values()); row['rho_after_hist'] = {str(k): list(rh.values()).count(k) for k in set(rh.values())}
                row['graph_after_sha256'] = radius.graph_hash(G)
                if row['max_rho_after'] >= 5:
                    os.makedirs('causal_graphs', exist_ok=True); json.dump({'faces': [list(f) for f in G]}, open('causal_graphs/%s.json' % row['graph_after_sha256'][:16], 'w'))
            out.write(json.dumps(row) + '\n'); out.flush(); print(json.dumps(row), flush=True)
