#!/usr/bin/env python3
"""Track F: independent Python check of Kempe classes of 4-colourings of a whole triangulation (no hole) or of T - h."""
import sys
def read(path, name):
    for l in open(path):
        p = l.split()
        if p[0] == name: return [list(map(int, r.split(','))) for r in p[2].split(';')]
def colourings(adj, verts):
    order = []; seen = set()
    for s in verts:
        if s in seen: continue
        seen.add(s); q = [s]
        for u in q:
            order.append(u)
            for w in adj[u]:
                if w in verts and w not in seen: seen.add(w); q.append(w)
    out = []; c = {}
    def rec(i):
        if i == len(order): out.append(dict(c)); return
        v = order[i]; forb = {c[w] for w in adj[v] if w in c}
        for a in range(4):
            if a not in forb: c[v] = a; rec(i + 1); del c[v]
    rec(0); return out, order
def norm(c, order):
    mp = {}; return tuple(mp.setdefault(c[v], len(mp)) for v in order)
if __name__ == '__main__':
    rot = read(sys.argv[1], sys.argv[2]); h = int(sys.argv[3]) if len(sys.argv) > 3 else -1
    verts = set(range(len(rot))) - {h}; adj = {v: [w for w in rot[v] if w != h] for v in verts}
    cols, order = colourings(adj, sorted(verts, key=lambda v: (v not in rot[h], v)) if h >= 0 else sorted(verts))
    states = {}
    for c in cols: states.setdefault(norm(c, order), c)
    keys = list(states); idx = {k: i for i, k in enumerate(keys)}; par = list(range(len(keys)))
    def f(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for k in keys:
        c = states[k]
        for p in range(4):
            for q in range(p + 1, 4):
                left = {v for v in verts if c[v] in (p, q)}
                while left:
                    s = left.pop(); comp = {s}; st = [s]
                    while st:
                        u = st.pop()
                        for w in adj[u]:
                            if w in left: left.discard(w); comp.add(w); st.append(w)
                    d = dict(c)
                    for v in comp: d[v] = q if c[v] == p else p
                    a, b = f(idx[k]), f(idx[norm(d, order)])
                    if a != b: par[a] = b
    from collections import Counter
    cl = Counter(f(i) for i in range(len(keys)))
    print(sys.argv[2], 'hole', h, 'states', len(keys), 'classes', len(cl), 'size histogram', sorted(Counter(cl.values()).items()))
