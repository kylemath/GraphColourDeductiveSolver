#!/usr/bin/env python3
"""A_rsst_defects [exploratory]: which of RSST's 633 unavoidable configurations appear in a defect patch?

Patch: built from a ring signature with b8b/rings.py Layered exactly as defect_verify.py does (SIG rings, then SEA
all-6 rings). Only vertices strictly inside the outer ring have their full neighbourhood (and exact degree) present;
the outer ring is excluded as an image of any configuration vertex (its degree is set to -1).
Containment (same notion as studiointel/rsst_contain.py): injective map phi of the configuration's interior vertices
into the patch, exact degrees, isomorphism onto an INDUCED subgraph, every configuration face (three interior
vertices pairwise adjacent and a face of the free completion) mapped to a face of the patch.
Unlike rsst_contain.py we enumerate every embedding (deduplicated by image set) so we can report where it sits.

Usage: rsst_in_defect.py NAME SIG [NAME SIG ...]      (SEA = 6 rings; env SEA overrides)
       rsst_in_defect.py --icosa                       (closed icosahedron, positive control)
Output: one JSON line per patch."""
import sys, os, json, collections
HERE = os.path.dirname(os.path.abspath(__file__))
PS = os.path.abspath(os.path.join(HERE, *(['..'] * 7)))          # .../planemap-structural
WD = os.path.abspath(os.path.join(HERE, '..', '..', '..'))       # wheeldis
sys.path.insert(0, os.path.join(PS, 'studiointel', 'routeb'))
sys.path.insert(0, os.path.join(os.path.dirname(WD), 'b8b')); sys.path.insert(0, os.path.dirname(WD))
import rsst_parse
from rings import Layered

CONFS = rsst_parse.parse(os.path.join(PS, 'studiointel', 'routeb', 'rsst', 'unavoidable.conf'))

def prep(c):
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
    while len(order) < len(U):
        best = max((u for u in U if u not in seen), key=lambda u: (len(E[u] & seen), deg[u]))
        order.append(best); seen.add(best)
    # faces closed once all three placed: index by last-placed vertex
    pos = {u: i for i, u in enumerate(order)}
    fby = collections.defaultdict(list)
    for f in cf: fby[max(f, key=lambda x: pos[x])].append(f)
    return {'U': U, 'deg': deg, 'E': E, 'order': order, 'fby': fby, 'degset': set(deg.values())}

PREP = [prep(c) for c in CONFS]

def embeddings(adj, degT, tfaces, P, cap=10**6):
    order = P['order']; phi = {}; used = set(); out = set()
    def rec(i):
        if len(out) >= cap: return
        if i == len(order):
            out.add(frozenset(phi.values())); return
        u = order[i]; placed = order[:i]
        nbr = [w for w in placed if w in P['E'][u]]
        cands = adj[phi[nbr[0]]] if nbr else list(adj)
        for t in cands:
            if t in used or degT[t] != P['deg'][u]: continue
            if any((w in P['E'][u]) != (phi[w] in adj[t]) for w in placed): continue
            phi[u] = t
            if all(frozenset(phi[x] for x in f) in tfaces for f in P['fby'][u]):
                used.add(t); rec(i + 1); used.discard(t)
            del phi[u]
    rec(0)
    return out

def build_patch(sig, sea):
    rings = sig.split('|'); L = Layered(int(rings[0]))
    for k in range(1, len(rings)): L.add_ring([int(ch) for ch in rings[k]])
    for _ in range(sea): L.add_ring([6] * len(L.ring()))
    outer = set(L.ring())
    adj = collections.defaultdict(set); faces = set()
    for a, b, c in L.tris:
        for x, y in ((a, b), (b, c), (c, a)): adj[x].add(y); adj[y].add(x)
        faces.add(frozenset((a, b, c)))
    degT = {}
    for v in adj:
        if v in outer: degT[v] = -1
        else:
            assert len(adj[v]) == L.deg[v]; degT[v] = L.deg[v]
    return dict(adj), degT, faces, outer

def icosa():
    import itertools
    # icosahedron: vertices 0 (top), 1..5 upper, 6..10 lower, 11 bottom
    F = []
    for i in range(5):
        a, b = 1 + i, 1 + (i + 1) % 5; c, d = 6 + i, 6 + (i + 1) % 5
        F += [(0, a, b), (a, c, b), (b, c, d), (c, 11, d)]
    adj = collections.defaultdict(set)
    for f in F:
        for x, y in itertools.combinations(f, 2): adj[x].add(y); adj[y].add(x)
    return dict(adj), {v: len(adj[v]) for v in adj}, {frozenset(f) for f in F}, set()

def analyse(name, adj, degT, faces, outer):
    Y = sorted(v for v in degT if degT[v] not in (-1, 6))
    dist = {v: 0 for v in Y}; fr = list(Y); r = 0
    while fr:
        r += 1; nf = []
        for x in fr:
            for y in adj[x]:
                if y not in dist: dist[y] = r; nf.append(y)
        fr = nf
    inner_deg = collections.Counter(d for d in degT.values() if d != -1)
    present = set(inner_deg)
    hits = []
    for i, (c, P) in enumerate(zip(CONFS, PREP)):
        if not P['degset'] <= present: continue
        emb = embeddings(adj, degT, faces, P)
        if not emb: continue
        locs = []
        for S in sorted(emb, key=lambda s: sorted(s)):
            locs.append({'n5': sum(degT[v] == 5 for v in S), 'n7': sum(degT[v] == 7 for v in S),
                         'n6': sum(degT[v] == 6 for v in S), 'maxdistY': max(dist.get(v, 99) for v in S)})
        hits.append({'idx': i, 'name': c['name'], 'ring': c['r'], 'type': 'C' if c['k_contract'] > 0 else 'D',
                     'size': c['n'] - c['r'], 'n_emb': len(emb), 'locs': locs[:4]})
    return {'patch': name, 'nV': len(adj), 'n_inner': sum(1 for v in degT if degT[v] != -1),
            'Y': {'n5': sum(degT[v] == 5 for v in Y), 'n7': sum(degT[v] == 7 for v in Y)},
            'charge': sum(6 - degT[v] for v in Y), 'n_hits': len(hits),
            'n_D': sum(h['type'] == 'D' for h in hits), 'n_C': sum(h['type'] == 'C' for h in hits),
            'min_ring': min((h['ring'] for h in hits), default=None), 'hits': hits}

if __name__ == '__main__':
    sea = int(os.environ.get('SEA', '6'))
    if sys.argv[1] == '--icosa':
        print(json.dumps(analyse('icosahedron', *icosa()))); sys.exit()
    a = sys.argv[1:]
    for name, sig in zip(a[::2], a[1::2]):
        print(json.dumps(analyse(name, *build_patch(sig, sea))), flush=True)
