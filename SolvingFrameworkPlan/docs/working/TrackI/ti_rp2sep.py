#!/usr/bin/env python3
"""Track I: at the RP^2 rigid -> rigid steps (out/cycitems.jsonl records with 'tait'), is the curve X separating?
X (the F13-trail of v through e1, e3) is turned into a closed curve on the surface by routing it through the star of
h across the spokes h x_{j+2}, h x_{j+3} (the e2 side).  X separates iff deleting the primal edges it crosses splits
T into two components.  Also re-evaluates the band-surgery step: lambda(B3',N)+lambda(B1,N) for N^H vs N^F (the
two sides of Lemma R) are recomputed directly from the dual.
usage: ti_rp2sep.py GRAPHFILE RECORDS.jsonl"""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'TrackH'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from th_engine import Hole
from ti_lib import Tait, triangle_faces
from collections import defaultdict, Counter

def tait_with_primal(rot, h, col, roles, j):
    al, mu, A, B = roles; z = {al: 0, mu: 1, A: 2, B: 3}
    F = triangle_faces(rot); ef = defaultdict(list)
    for t, f in enumerate(F):
        a, b, c = sorted(f)
        for e in ((a, b), (a, c), (b, c)): ef[e].append(t)
    hf = {t for t, f in enumerate(F) if h in f}; ren = {}
    def vid(t):
        if t in hf: return 0
        if t not in ren: ren[t] = len(ren) + 1
        return ren[t]
    X = rot[h]; x = [X[(j + t) % 5] for t in range(5)]
    linklab = {frozenset((x[t], x[(t + 1) % 5])): 'e%d' % t for t in range(5)}
    E = []; prim = []
    for (u, w), (f1, f2) in sorted(ef.items()):
        if h in (u, w): continue
        E.append((vid(f1), vid(f2), z[col[u]] ^ z[col[w]], linklab.get(frozenset((u, w))))); prim.append((u, w))
    return E, prim, x

graphs = {}
for l in open(sys.argv[1]):
    p = l.split()
    if len(p) >= 3: graphs[p[0]] = [list(map(int, r.split(','))) for r in p[2].split(';')]
st = Counter()
for l in open(sys.argv[2]):
    d = json.loads(l)
    if 'tait' not in d: continue
    rot = graphs[d['graph']]; h = d['hole']; Hh = Hole(rot, h)
    r, col = Hh.analyse_state(d['state'])
    E, prim, x = tait_with_primal(rot, h, col, r['roles'], r['j'])
    T = Tait(E); F13 = {k for k, e in enumerate(E) if e[2] in (1, 3)}
    Xp, back = T.trail(F13, T.lab['e1'])
    cut = {frozenset(prim[k]) for k in Xp} | {frozenset((h, x[2])), frozenset((h, x[3]))}
    adj = defaultdict(list)
    for u in range(len(rot)):
        for w in rot[u]:
            if frozenset((u, w)) not in cut: adj[u].append(w)
    seen = {0}; stck = [0]
    while stck:
        u = stck.pop()
        for w in adj[u]:
            if w not in seen: seen.add(w); stck.append(w)
    sep = len(seen) < len(rot)
    st['separating' if sep else 'NON-separating'] += 1
    if not sep: continue
    side0 = seen                                   # primal vertex set of one side
    # circle points: a (=v_I end e2), w_1..w_2p (trail order), b (=v_O end); ends = transverse edges (colour 2) / e2,e4,e0
    ws = [];  xx = 0; k0 = Xp[0]
    for k in Xp[:-1]:
        xx = T.other(k, xx); ws.append(xx)
    pts = ['a'] + ws + ['b']; pos = {q: i for i, q in enumerate(pts)}
    def side_of(k): u, w = prim[k]; return u in side0
    M = {c: {k for k, e in enumerate(E) if e[2] == c} for c in (1, 2, 3)}
    Xs = set(Xp)
    def ends_matching(Sset, vO):          # pairing of circle points by paths of Sset \ X
        Soff = Sset - Xs; res = {}
        starts = [('a', T.lab['e2']), ('b', T.lab[vO])] + [(w, next(t for t in T.inc[w] if t in Soff)) for w in ws]
        for q, k in starts:
            if q in res: continue
            y = T.other(k, 0 if q in ('a', 'b') else q); kk = k
            while y != 0 and y not in ws:
                kk = next(t for t in T.inc[y] if t in Soff and t != kk); y = T.other(kk, y)
            q2 = ('a' if kk == T.lab['e2'] else 'b') if y == 0 else y
            res[q] = q2; res[q2] = q
        return res
    def crossing(match, sideval, sidemap):
        prs = {tuple(sorted((pos[q], pos[r]))) for q, r in match.items() if sidemap[q] == sideval}
        prs = sorted(prs)
        return any(a < c < b < d for a, b in prs for c, d in prs)
    sidemap = {'a': side_of(T.lab['e2']), 'b': side_of(T.lab['e4'])}
    for w in ws: sidemap[w] = side_of(next(t for t in T.inc[w] if t in M[2]))
    for name, Sset, vO in (('H', M[2] | M[3], 'e4'), ('F12', M[1] | M[2], 'e0')):
        m = ends_matching(Sset, vO)
        cr = [crossing(m, sv, sidemap) for sv in (sidemap['a'], not sidemap['a'])]
        st[name + '_crossing_inside' ] += cr[0]; st[name + '_crossing_outside'] += cr[1]
        st[name + '_any_crossing'] += any(cr)
    st['a_b_same_side'] += sidemap['a'] == sidemap['b']
print(dict(st))
