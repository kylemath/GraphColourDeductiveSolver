#!/usr/bin/env python3
"""studiointel rsst_contain.py -- [exploratory] does triangulation T contain an RSST configuration?
Containment = injective map phi of the configuration's vertices (r+1..n of the free completion) into V(T) with
 deg_T(phi(u)) = the configuration degree of u, phi an isomorphism onto an INDUCED subgraph, and every configuration face
 (three configuration vertices mutually adjacent and a face of the free completion) mapped to a face of T.
Prints, per graph: which configurations (index, ring) occur, and per-hole hard-state survival."""
import sys, json, itertools
sys.path.insert(0, 'routeb')
import rsst_parse

def load_T(p):
    F = [tuple(f) for f in json.load(open(p))['faces']]
    adj = {}
    for f in F:
        for i in range(3): adj.setdefault(f[i], set()).add(f[(i + 1) % 3]); adj.setdefault(f[(i + 1) % 3], set()).add(f[i])
    faces = {frozenset(f) for f in F}
    return adj, faces

def prep_conf(c):
    r, n = c['r'], c['n']; U = list(range(r + 1, n + 1))
    deg = {u: len(c['adj'][u]) for u in U}
    E = {u: set(w for w in c['adj'][u] if w > r) for u in U}
    cf = set()
    for u in U:
        L = c['adj'][u]
        for i in range(len(L)):
            a, b = L[i], L[(i + 1) % len(L)]
            if a > r and b > r: cf.add(frozenset((u, a, b)))
    order = [U[0]]; seen = {U[0]}
    while len(order) < len(U):          # connected BFS-ish order maximising adjacency to placed vertices
        best = max((u for u in U if u not in seen), key=lambda u: (len(E[u] & seen), deg[u]))
        order.append(best); seen.add(best)
    return {'U': U, 'deg': deg, 'E': E, 'faces': cf, 'order': order, 'r': r}

def contains(adj, tfaces, P):
    degT = {u: len(a) for u, a in adj.items()}; order = P['order']; phi = {}; used = set()
    def rec(i):
        if i == len(order):
            return all(frozenset(phi[x] for x in f) in tfaces for f in P['faces'])
        u = order[i]; placed = [w for w in order[:i]]
        nbr = [w for w in placed if w in P['E'][u]]
        cands = (adj[phi[nbr[0]]] if nbr else adj.keys())
        for t in cands:
            if t in used or degT[t] != P['deg'][u]: continue
            ok = True
            for w in placed:
                if (w in P['E'][u]) != (phi[w] in adj[t]): ok = False; break
            if not ok: continue
            phi[u] = t; used.add(t)
            if rec(i + 1): return True
            del phi[u]; used.discard(t)
        return False
    return rec(0)

if __name__ == '__main__':
    confs = rsst_parse.parse('routeb/rsst/unavoidable.conf'); P = [prep_conf(c) for c in confs]
    for p in sys.argv[1:]:
        adj, tf = load_T(p)
        hits = [(i, confs[i]['r']) for i in range(len(confs)) if contains(adj, tf, P[i])]
        minring = min((r for _, r in hits), default=None)
        print(json.dumps({'graph': p, 'n': len(adj), 'n_hits': len(hits), 'min_ring': minring,
                          'hits_ring_le10': sum(1 for _, r in hits if r <= 10), 'hits_ring_le12': sum(1 for _, r in hits if r <= 12),
                          'first_hits': hits[:5]}), flush=True)
