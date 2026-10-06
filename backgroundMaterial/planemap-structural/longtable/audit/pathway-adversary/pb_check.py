#!/usr/bin/env python3
"""P-E check of P-B claims on T4 (faces from MathConjectureR.md) and the order-14 graph (plantri).
Audit code; radius by radius_probe.py (pure swaps in T - x). [exploratory]"""
import json, sys
from radius_probe import radius
T4 = [(0,1,2),(0,1,5),(0,2,3),(0,3,4),(0,4,5),(1,2,6),(1,5,10),(1,6,10),(2,3,7),(2,6,11),(2,7,11),(3,4,8),(3,7,8),
      (4,5,9),(4,8,9),(5,9,10),(6,10,15),(6,11,15),(7,8,12),(7,11,12),(8,9,13),(8,12,13),(9,10,14),(9,13,14),
      (10,14,15),(11,12,16),(11,15,16),(12,13,16),(13,14,16),(14,15,16)]
def rot_from_faces(F):
    n = 1 + max(max(f) for f in F); A = [set() for _ in range(n)]
    for a, b, c in F: A[a] |= {b, c}; A[b] |= {a, c}; A[c] |= {a, b}
    assert sum(len(s) for s in A) // 2 == 3 * n - 6 and len(F) == 2 * n - 4
    return [sorted(s) for s in A]
def d5(rot):
    deg = [len(r) for r in rot]; V = [v for v in range(len(rot)) if deg[v] == 5]
    seen = set(); comps = []
    for s in V:
        if s in seen: continue
        st = [s]; seen.add(s); c = [s]
        while st:
            a = st.pop()
            for b in rot[a]:
                if deg[b] == 5 and b not in seen: seen.add(b); st.append(b); c.append(b)
        comps.append(sorted(c))
    icosa = [v for v in V if all(deg[w] == 5 for w in rot[v])]
    return dict(deg5=len(V), d5_components=[len(c) for c in comps], icosahedral=icosa)
out = {}
for name, rot in (('T4', rot_from_faces(T4)),
                  ('order14', [[ord(c) - 97 for c in p] for p in open(sys.argv[1]).read().split()[1].split(',')])):
    s = d5(rot); s['radii'] = {}
    for x in range(len(rot)):
        if len(rot[x]) == 5:
            r = radius(rot, x); s['radii'][x] = dict(states=r['states'], hist=r['radius_hist'], targetless=r['targetless'])
    out[name] = s
print(json.dumps(out, indent=1))
