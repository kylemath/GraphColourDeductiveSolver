#!/usr/bin/env python3
"""Track S library: near-rigid pi-runs on triangulated spheres, and planar (Jordan-level) quantities along them.

Reuses read-only: TrackL tl_lib.HoleData (TrackH th_engine states, roles, pi, pi^-1, N, role counts c6).

A state is near-rigid if it is rigid (DL, c6 = (1,1,2,1,2,1)) or in-shape (DL, N = 9, pi and pi^-1 rigid).
An R-run is a maximal pi-path of DL states with N <= 9.  Phi(u) = pi(pi(u)) on rigid u with pi(u) in R, pi^2(u) rigid.
"""
import sys, os
from collections import defaultdict, deque
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'TrackL'))
sys.path.insert(0, os.path.join(HERE, '..', 'TrackH'))
sys.path.insert(0, os.path.join(HERE, '..', 'TrackI'))
from tl_lib import HoleData, RIGID   # noqa: E402

ROLEPAIRS = ['am', 'AB', 'aA', 'mB', 'aB', 'mA']


def load_graphs(path, names=None):
    out = {}
    for l in open(path):
        p = l.split()
        if len(p) < 3: continue
        if names is not None and p[0] not in names: continue
        out[p[0]] = [list(map(int, r.split(','))) for r in p[2].split(';')]
    return out


def inR(hd, i):
    r = hd.info[i]
    return r['kind'] == 'DL' and r['N'] <= 9


def runs(hd):
    """maximal pi-paths inside R (cycles reported with flag)"""
    S = hd.S
    R = [i for i in range(S) if inR(hd, i)]
    Rs = set(R)
    pre = {}
    for i in R:
        p = hd.info[i]['pi']
        if p is not None and p in Rs: pre[p] = i
    out = []; seen = set()
    for i in R:
        if i in pre or i in seen: continue
        run = [i]; seen.add(i); x = hd.info[i]['pi']
        while x is not None and x in Rs and x not in seen:
            run.append(x); seen.add(x); x = hd.info[x]['pi']
        out.append((run, False))
    for i in R:            # leftover = cycles
        if i in seen: continue
        cyc = [i]; seen.add(i); x = hd.info[i]['pi']
        while x != i: cyc.append(x); seen.add(x); x = hd.info[x]['pi']
        out.append((cyc, True))
    return out


def phi_steps(hd):
    """all (u, c, u2) with u rigid, c = pi(u) DL N=9, u2 = pi(c) rigid"""
    out = []
    for u in range(hd.S):
        if not hd.rigid(u): continue
        c = hd.info[u]['pi']
        if c is None or not inR(hd, c) or hd.info[c]['N'] != 9: continue
        u2 = hd.info[c]['pi']
        if u2 is None or not hd.rigid(u2): continue
        out.append((u, c, u2))
    return out


# ---------------- primal geometry ----------------

class Geo:
    """faces/darts of the triangulated sphere T (rotation system rot, assumed a consistent cyclic order)."""

    def __init__(self, rot, h):
        self.rot = rot; self.h = h; n = len(rot); self.n = n
        self.pos = [{w: k for k, w in enumerate(r)} for r in rot]
        # dart (a,b) -> face id ; face = left face with c = rot[b][pos[b][a]-1]
        self.dface = {}; faces = []
        for a in range(n):
            for b in rot[a]:
                if (a, b) in self.dface: continue
                cyc = [(a, b)]; x, y = a, b
                while True:
                    r = rot[y]; z = r[(self.pos[y][x] - 1) % len(r)]
                    x, y = y, z
                    if (x, y) == (a, b): break
                    cyc.append((x, y))
                fid = len(faces); faces.append(tuple(d[0] for d in cyc))
                for d in cyc: self.dface[d] = fid
        self.faces = faces
        assert all(len(f) == 3 for f in faces), 'not a triangulation'
        assert n - sum(len(r) for r in rot) // 2 + len(faces) == 2, 'not a sphere'
        self.hfaces = [f for f in range(len(faces)) if h in faces[f]]
        # link in rotation order of h
        self.X = list(rot[h])

    def potential(self, circ):
        """circ: dict dart (a,b) -> +1 meaning one unit of flow a->b (antisymmetric implied).
        Returns face function phi with phi(left(d)) - phi(right(d)) = circ(d), phi(face 0) = 0; None if not a circulation."""
        F = len(self.faces); phi = [None] * F; phi[0] = 0; dq = deque([0])
        val = defaultdict(int)
        for (a, b), w in circ.items(): val[(a, b)] += w; val[(b, a)] -= w
        # adjacency over faces
        while dq:
            f = dq.popleft(); fa = self.faces[f]
            for k in range(3):
                a, b = fa[k], fa[(k + 1) % 3]
                # dart (a,b) has left face f ; right face = face of (b,a)
                g = self.dface[(b, a)]
                want = phi[f] - val[(a, b)]
                if phi[g] is None: phi[g] = want; dq.append(g)
                elif phi[g] != want: return None
        return phi


def pair_components(hd, col, pair):
    Hh = hd.Hh
    left = {v for v in Hh.V if col[v] in pair}; comps = []
    while left:
        s = next(iter(left)); K = Hh.comp(col, s, pair); left -= K; comps.append(K)
    return comps


def role_cols(hd, i):
    r = hd.info[i]; al, mu, A, B = r['roles']
    return {'a': al, 'm': mu, 'A': A, 'B': B}
