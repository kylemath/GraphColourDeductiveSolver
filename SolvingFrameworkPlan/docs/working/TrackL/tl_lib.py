#!/usr/bin/env python3
"""Track L library: primal states at a degree-5 hole (TrackH th_engine, read-only import) plus Tait-form objects
(TrackI ti_lib.primal_to_tait, read-only import) and region computations, for the sigma-type lemma and NRC.

Per hole: all states (colourings of T - h up to renaming), kind, frame j, roles, pi, pi^-1 (mirror move), N,
six role component counts c6 = (am, AB, aA, mB, aB, mA).
Tait objects of a DL state (colour 1 = a+m, 2 = a+A, 3 = a+B; v = 0 with half-edges e0..e4, colours 1,1,2,1,3):
  H = M2 u M3, F12 = M1 u M2, F13 = M1 u M3;  X/Y = F13-loops of v through e1,e3 / e0,e4;
  Xt/Yt = F12-loops of v through e0,e3 / e1,e2  (mirror images of X, Y).
Regions of S^2 - S for an edge set S of the Tait graph are computed in the primal: faces of the Tait graph are the
vertices of T - h; two faces are in the same region iff joined by primal edges whose duals are not in S.
"""
import sys, os
from collections import defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'TrackH'))
sys.path.insert(0, os.path.join(HERE, '..', 'TrackI'))
from th_engine import Hole            # noqa: E402
from ti_lib import Tait, triangle_faces   # noqa: E402

PAIRS = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
RIGID = (1, 1, 2, 1, 2, 1)


def ncomp(Hh, col, pair):
    left = {v for v in Hh.V if col[v] in pair}; n = 0; comps = []
    while left:
        s = next(iter(left)); K = Hh.comp(col, s, pair); left -= K; comps.append(K)
    return comps


def read_graphs(path, stride=1, off=0, maxg=10 ** 9, prefix=''):
    k = 0
    for ln, l in enumerate(open(path)):
        p = l.split()
        if len(p) < 3 or not p[0].startswith(prefix): continue
        if ln % stride != off: continue
        k += 1
        if k > maxg: break
        yield p[0], [list(map(int, r.split(','))) for r in p[2].split(';')]


class HoleData:
    """all states at hole h with kind, roles, pi, pi^-1, N, c6"""

    def __init__(self, rot, h):
        self.rot = rot; self.h = h
        Hh = Hole(rot, h); self.Hh = Hh
        S = len(Hh.states); self.S = S
        self.info = []; self.col = []
        for i in range(S):
            r, col = Hh.analyse_state(i); self.info.append(r); self.col.append(col)
        for i in range(S):
            r = self.info[i]; col = self.col[i]
            if r['kind'] == 'F': continue
            al, mu, A, B = r['roles']
            c6 = tuple(len(ncomp(Hh, col, pr)) for pr in [(al, mu), (A, B), (al, A), (mu, B), (al, B), (mu, A)])
            r['c6'] = c6; r['N'] = sum(c6)
            x = [Hh.X[(r['j'] + t) % 5] for t in range(5)]; r['x'] = x
            # pi^-1 = mirror move: swap K_{aB}(x_j), defined iff not inB (x_j notin K_aB(x_{j+2}))
            r['pinv'] = None
            if not r['inB']:
                K = Hh.comp(col, x[0], (al, B)); r['pinv'] = Hh.swap(col, K, al, B)

    def rigid(self, i):
        r = self.info[i]; return r['kind'] == 'DL' and r['c6'] == RIGID

    def extra(self, i):
        r = self.info[i]; return [k for k in range(6) if r['c6'][k] > RIGID[k]]

    def inshape(self, i):
        r = self.info[i]
        return (r['kind'] == 'DL' and r['N'] == 9 and r['pi'] is not None and r['pinv'] is not None
                and self.rigid(r['pi']) and self.rigid(r['pinv']))


def sphere_faces_ok(rot):
    n = len(rot); F = triangle_faces(rot); E = sum(len(r) for r in rot) // 2
    return n - E + len(F)


class TaitState:
    """Tait picture of DL state i of a HoleData, with primal back-references for region computations."""

    def __init__(self, hd, i):
        r = hd.info[i]; col = hd.col[i]; rot = hd.rot; h = hd.h
        al, mu, A, B = r['roles']; z = {al: 0, mu: 1, A: 2, B: 3}
        F = triangle_faces(rot)
        ef = defaultdict(list)
        for t, f in enumerate(F):
            a, b, c = sorted(f)
            for e in ((a, b), (a, c), (b, c)): ef[e].append(t)
        hf = {t for t, f in enumerate(F) if h in f}
        ren = {}

        def vid(t):
            if t in hf: return 0
            if t not in ren: ren[t] = len(ren) + 1
            return ren[t]
        x = r['x']
        linklab = {frozenset((x[t], x[(t + 1) % 5])): 'e%d' % t for t in range(5)}
        E = []; prim = []
        for (u, w), (f1, f2) in sorted(ef.items()):
            if h in (u, w): continue
            E.append((vid(f1), vid(f2), z[col[u]] ^ z[col[w]], linklab.get(frozenset((u, w)))))
            prim.append((u, w))
        self.E = E; self.prim = prim; self.T = Tait(E); self.r = r; self.col = col; self.hd = hd
        self.Vp = [v for v in range(len(rot)) if v != h]
        M = {c: {k for k, e in enumerate(E) if e[2] == c} for c in (1, 2, 3)}
        self.M = M
        self.H = M[2] | M[3]; self.F12 = M[1] | M[2]; self.F13 = M[1] | M[3]
        T = self.T
        self.X = set(T.trail(self.F13, T.lab['e1'])[0]); self.Y = set(T.trail(self.F13, T.lab['e4'])[0])
        self.Xt = set(T.trail(self.F12, T.lab['e0'])[0]); self.Yt = set(T.trail(self.F12, T.lab['e1'])[0])
        self.H0 = set(T.trail(self.H, T.lab['e2'])[0])

    def components(self, S):
        """list of edge-id sets, one per connected component of S"""
        T = self.T; par = {}

        def f(a):
            par.setdefault(a, a)
            while par[a] != a: par[a] = par[par[a]]; a = par[a]
            return a
        for k in S:
            a, b = T.E[k][0], T.E[k][1]; par[f(a)] = f(b)
        out = defaultdict(set)
        for k in S: out[f(T.E[k][0])].add(k)
        return list(out.values())

    def regions(self, S):
        """dict primal vertex -> region id of S^2 - S"""
        par = {v: v for v in self.Vp}

        def f(a):
            while par[a] != a: par[a] = par[par[a]]; a = par[a]
            return a
        for k, (u, w) in enumerate(self.prim):
            if k not in S: par[f(u)] = f(w)
        return {v: f(v) for v in self.Vp}

    def corner_region(self, S, t):
        """region of the corner x_t (corner (e_{t-1}, e_t) at v)"""
        return self.regions(S)[self.r['x'][t]]

    def verts(self, S):
        return {a for k in S for a in self.E[k][:2]}
