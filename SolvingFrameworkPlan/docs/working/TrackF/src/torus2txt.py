#!/usr/bin/env python3
"""Torus triangulations from local-runs/18-torus-floor (faces) -> oriented rotation systems ('name n rot' lines).
Also writes, per graph, which degree-5 holes had a targetless class (a Kempe class with 0 filled states) in that run."""
import sys, json, gzip, itertools, collections
def orient(F):
    F = [tuple(f) for f in F]; E = collections.defaultdict(list)
    for i, f in enumerate(F):
        for a, b in itertools.combinations(f, 2): E[frozenset((a, b))].append(i)
    o = [None] * len(F); o[0] = F[0]; st = [0]
    while st:
        i = st.pop(); a, b, c = o[i]
        for x, y in ((a, b), (b, c), (c, a)):
            for k in E[frozenset((x, y))]:
                if k == i or o[k] is not None: continue
                z = [v for v in F[k] if v not in (x, y)][0]; o[k] = (y, x, z); st.append(k)
    return o
def rotation(n, O):
    nxt = collections.defaultdict(dict)
    for a, b, c in O: nxt[a][b] = c; nxt[b][c] = a; nxt[c][a] = b
    rot = []
    for v in range(n):
        s = min(nxt[v]); r = [s]
        while True:
            w = nxt[v][r[-1]]
            if w == s: break
            r.append(w)
        assert len(r) == len(nxt[v]); rot.append(r)
    return rot
out = open(sys.argv[2], 'w'); meta = open(sys.argv[3], 'w'); k = 0
for path in sys.argv[4:]:
    for l in gzip.open(path, 'rt'):
        d = json.loads(l)
        if not d.get('holes'): continue
        n = d['n']; rot = rotation(n, orient(d['faces']))
        tl = [h['v'] for h in d['holes'] if 'classes' in h and any(c[1] == 0 for c in h['classes'])]
        ok = [h['v'] for h in d['holes'] if 'classes' in h]
        name = f"torus{k}"; k += 1
        out.write(f"{name} {n} " + ";".join(",".join(map(str, r)) for r in rot) + "\n")
        meta.write(json.dumps({'graph': name, 'family': d['family'], 'targetless_holes': tl, 'analysed_holes': ok}) + "\n")
