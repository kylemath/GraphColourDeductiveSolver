#!/usr/bin/env python3
"""studiointel graphs.py -- graph builders for the R* adversary search. stdlib only.
A triangulation is a list of faces, each a tuple (a,b,c) oriented counter-clockwise (every edge appears once in each direction).
Builders: A_r (five-fold symmetric stack), GC(k,l) (Goldberg-Coxeter dual of the icosahedron), flip, degree/triangle checks."""
import itertools, math, json, sys
from fractions import Fraction

def adjacency(faces):
    adj = {}
    for f in faces:
        for i in range(3):
            adj.setdefault(f[i], set()).add(f[(i + 1) % 3]); adj.setdefault(f[(i + 1) % 3], set()).add(f[i])
    return adj

def check_triangulation(faces):
    """sphere triangulation: every directed edge once, V-E+F=2, simple. returns (ok, message)"""
    de = {}
    for f in faces:
        for i in range(3):
            e = (f[i], f[(i + 1) % 3])
            if e in de: return False, 'directed edge twice %s' % (e,)
            de[e] = 1
    for (a, b) in de:
        if (b, a) not in de: return False, 'edge without twin'
    V = len({x for f in faces for x in f}); E = len(de) // 2; F = len(faces)
    if V - E + F != 2: return False, 'Euler %d' % (V - E + F)
    return True, 'ok'

def degrees(faces):
    return {v: len(a) for v, a in adjacency(faces).items()}

def n_separating_triangles(faces):
    adj = adjacency(faces); fs = {frozenset(f) for f in faces}
    cnt = 0
    for a in adj:
        for b in adj[a]:
            if b <= a: continue
            for c in adj[a] & adj[b]:
                if c <= b: continue
                if frozenset((a, b, c)) not in fs: cnt += 1
    return cnt

def relabel(faces):
    m = {}
    for f in faces:
        for x in f:
            if x not in m: m[x] = len(m)
    return [tuple(m[x] for x in f) for f in faces]

def A_r(r):
    """v=0, layers L_1..L_r of 5 vertices, v' last. n=5r+2. antiprism stack. hole at v=0 is the five-fold centre."""
    L = lambda i, j: 1 + 5 * (i - 1) + (j % 5)
    top, bot = 0, 5 * r + 1
    faces = []
    for j in range(5): faces.append((top, L(1, j), L(1, j + 1)))
    for i in range(1, r):
        for j in range(5):
            faces.append((L(i, j), L(i + 1, j), L(i, j + 1)))      # down-pointing pair
            faces.append((L(i, j + 1), L(i + 1, j), L(i + 1, j + 1)))
    for j in range(5): faces.append((bot, L(r, j + 1), L(r, j)))
    return faces

def icosahedron():
    return A_r(2)

def _ico3d():
    p = (1 + 5 ** 0.5) / 2
    V = []
    for s1 in (1, -1):
        for s2 in (1, -1):
            V += [(0, s1, s2 * p), (s1, s2 * p, 0), (s2 * p, 0, s1)]
    # faces: triples of mutually adjacent vertices (edge length 2)
    d2 = lambda a, b: sum((x - y) ** 2 for x, y in zip(a, b))
    fs = []
    for a, b, c in itertools.combinations(range(12), 3):
        if all(abs(d2(V[x], V[y]) - 4) < 1e-9 for x, y in ((a, b), (b, c), (a, c))):
            n = [(V[b][i] - V[a][i]) for i in range(3)]; m = [(V[c][i] - V[a][i]) for i in range(3)]
            cr = (n[1] * m[2] - n[2] * m[1], n[2] * m[0] - n[0] * m[2], n[0] * m[1] - n[1] * m[0])
            out = sum(cr[i] * V[a][i] for i in range(3))
            fs.append((a, b, c) if out > 0 else (a, c, b))   # CCW seen from outside
    assert len(fs) == 20
    return V, fs

def GC(k, l):
    """Goldberg-Coxeter (k,l) triangulation: n = 10(k^2+kl+l^2)+2, degrees 5 (x12) and 6."""
    assert k >= 1 and l == 0, 'chiral/(k,k) types are reached by leapfrog() and composition, not by this lattice clipping'
    V3, F3 = _ico3d()
    # Eisenstein lattice points a + b*w, w = e^{i pi/3}; big triangle P0=(0,0), P1=(k,l), P2=(-l,k+l) (CCW)
    P = [(0, 0), (k, l), (-l, k + l)]
    def bary(a, b):
        (x0, y0), (x1, y1), (x2, y2) = P
        det = (x1 - x0) * (y2 - y0) - (x2 - x0) * (y1 - y0)
        l1 = Fraction((a - x0) * (y2 - y0) - (x2 - x0) * (b - y0), det)
        l2 = Fraction((x1 - x0) * (b - y0) - (a - x0) * (y1 - y0), det)
        return (1 - l1 - l2, l1, l2)
    inside = lambda a, b: all(t >= 0 for t in bary(a, b))
    amin = min(p[0] for p in P) - 1; amax = max(p[0] for p in P) + 1
    bmin = min(p[1] for p in P) - 1; bmax = max(p[1] for p in P) + 1
    pts = [(a, b) for a in range(amin, amax + 1) for b in range(bmin, bmax + 1) if inside(a, b)]
    pset = set(pts)
    tris = []
    for (a, b) in pts:
        if (a + 1, b) in pset and (a, b + 1) in pset: tris.append(((a, b), (a + 1, b), (a, b + 1)))
        if (a + 1, b) in pset and (a, b + 1) in pset and (a + 1, b + 1) in pset: tris.append(((a + 1, b), (a + 1, b + 1), (a, b + 1)))
    key = {}
    def vid(face, a, b):
        la = bary(a, b)
        pos = tuple(sum(float(la[i]) * V3[face[i]][c] for i in range(3)) for c in range(3))
        kk = tuple(round(x * 1e6) for x in pos)
        if kk not in key: key[kk] = len(key)
        return key[kk]
    faces = []
    for f in F3:
        for t in tris:
            faces.append(tuple(vid(f, *q) for q in t))
    return faces

def leapfrog(faces):
    """GC(1,1) multiplier: vertices V u F; each old v keeps its degree, each face vertex gets degree 6. n' = 3n-4."""
    fid = {f: ('f', i) for i, f in enumerate(faces)}
    face_of = {}
    for f in faces:
        for i in range(3): face_of[(f[i], f[(i + 1) % 3])] = f
    out = []
    for f in faces:
        for i in range(3):
            a, b = f[i], f[(i + 1) % 3]
            g = face_of[(b, a)]
            out.append((a, fid[g], fid[f]))
    return relabel(out)

def flip(faces, a, b):
    """flip edge ab: faces (a,b,c) and (b,a,d) -> (c,d... ) new edge cd. returns new faces or None if c,d already adjacent."""
    fa = [f for f in faces if any((f[i], f[(i + 1) % 3]) == (a, b) for i in range(3))][0]
    fb = [f for f in faces if any((f[i], f[(i + 1) % 3]) == (b, a) for i in range(3))][0]
    c = [x for x in fa if x not in (a, b)][0]; d = [x for x in fb if x not in (a, b)][0]
    if d in adjacency(faces)[c]: return None
    rest = [f for f in faces if f is not fa and f is not fb]
    return rest + [(a, d, c), (b, c, d)]

if __name__ == '__main__':
    for name, fs in (('icosahedron', icosahedron()), ('A_3', A_r(3)), ('A_4', A_r(4)), ('L(ico)=GC(1,1)', leapfrog(icosahedron())), ('GC(2,0)', GC(2, 0)), ('GC(3,0)', GC(3, 0)), ('L(A_3)', leapfrog(A_r(3)))):
        ok, msg = check_triangulation(fs); dg = degrees(fs)
        from collections import Counter
        print(name, 'n=%d' % len(dg), ok, msg, dict(Counter(dg.values())), 'sep-triangles', n_separating_triangles(fs))
