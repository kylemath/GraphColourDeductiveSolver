#!/usr/bin/env python3
"""dp_test.py -- [exploratory][sketch] disc-degree parity test for T - v (v of degree 5). stdlib only.
Companion to SolvingFrameworkPlan/docs/working/creative-intel-2026-10-05/disc-degree-parity.md.

Checks, for each graph:
  (a) the hand formula  N_{abc}(c) == O_a(c) + e_{ad}(w)  (mod 2) for every colouring c of D = T - v,
      N_S = #faces of D coloured with set S, O_a = #vertices of D of colour a with odd degree IN T,
      e_{ad}(w) = #link edges x_i x_{i+1} coloured {a,d}, d = the colour missing from {a,b,c};
  (b) Kempe classes of D (whole-component swaps in D, link vertices allowed), all 24 colour labels;
  (c) per class: does some link word occur with both values of the bit O_0 mod 2 (equivalently N_F mod 2)?
      Any such 'conflict' means no boundary correction beta(word, T) makes N_F mod 2 a Kempe invariant.
Usage:  python3 dp_test.py            -> icosahedron only (smoke, < 1 s)
        python3 dp_test.py --all      -> icosahedron, T4, A_3 (Studio; A_3 may be large)
Seen on the author's 1-second smoke run (T4, ico): formula holds; T4 one class, 168 conflicts; ico no conflicts."""
import sys, itertools, time
sys.path.insert(0, '.')
from pb_lib import T4F, from_faces, colourings, comps, swap, key, filled

ICO = [(0,1,2),(0,2,3),(0,3,4),(0,4,5),(0,5,1),(1,2,6),(2,3,7),(3,4,8),(4,5,9),(5,1,10),
       (6,7,2),(7,8,3),(8,9,4),(9,10,5),(10,6,1),(6,7,11),(7,8,11),(8,9,11),(9,10,11),(10,6,11)]

def link_order(adj, h):
    L = [min(adj[h], key=str)]
    while len(L) < 5:
        L.append([w for w in adj[h] & adj[L[-1]] if w not in L][0])
    return L

def faces_of(adj):
    fs = set()
    for a in adj:
        for b in adj[a]:
            for c in adj[a] & adj[b]: fs.add(frozenset((a, b, c)))
    return [tuple(f) for f in fs]  # all triangles; fine for these graphs (no separating triangles assumed)

def run(name, adj, h):
    t = time.time(); L = link_order(adj, h)
    F = [f for f in faces_of(adj) if h not in f]
    odd = {u: len(adj[u]) % 2 for u in adj}
    allc = {}
    for c in colourings(adj, h):
        for p in itertools.permutations(range(4)):
            d = {u: p[x] for u, x in c.items()}; allc[key(d)] = d
    ks = list(allc); idx = {k: i for i, k in enumerate(ks)}; par = list(range(len(ks)))
    def f(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    fviol = 0
    for k in ks:
        c = allc[k]; w = [c[x] for x in L]
        e = lambda a, b: sum(1 for i in range(5) if {w[i], w[(i + 1) % 5]} == {a, b})
        O = [sum(odd[u] for u in c if c[u] == a) for a in range(4)]
        for S in itertools.combinations(range(4), 3):
            N = sum(1 for fc in F if {c[u] for u in fc} == set(S)); d = (set(range(4)) - set(S)).pop()
            fviol += sum((N - O[a] - e(a, d)) % 2 for a in S)
        for a, b, K in comps(adj, c, h): par[f(idx[k])] = f(idx[key(swap(c, a, b, K))])
    cl = {}
    for k in ks: cl.setdefault(f(idx[k]), []).append(allc[k])
    out = []
    for cs in cl.values():
        byw = {}
        for c in cs:
            byw.setdefault(tuple(c[x] for x in L), set()).add(sum(odd[u] for u in c if c[u] == 0) % 2)
        out.append((len(cs), any(filled(adj, c, h) for c in cs), sum(1 for s in byw.values() if len(s) > 1)))
    print(f"{name}: colourings(24 labels)={len(ks)} formula_violations={fviol} classes={len(cl)} "
          f"(size, has_fill, same-word bit conflicts) per class={sorted(out)} [{time.time()-t:.2f}s]")

if __name__ == '__main__':
    run('icosahedron', from_faces(ICO), 0)
    if '--all' in sys.argv:
        run('T4', from_faces(T4F), 0)
        from pb_lib import a3
        adj, m = a3(); run('A_3', adj, m['v'])
