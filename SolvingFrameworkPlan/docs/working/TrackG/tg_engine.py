#!/usr/bin/env python3
"""Track G [exploratory]: per-hole state data for the stream-function experiment.

Engine: kempe_py.Space (bitmask Kempe engine, no planarity used, so it runs on any triangulated surface).
pi follows TrackF/LockParity.md 5.2 (and lpc_detail.py): at an unfilled state with link (alpha, mu, alpha, A, B) at
x_j..x_{j+4}, pi = swap of K_{alpha A}(x_{j+2}), defined iff x_j not in it. On the sphere, at DL states this is R3 of
escape.pi_of (Lock2 => not inA).

For every state we record: kind F / DL / S (single lock or no lock), j, L1, L2, inA, inB, pi, a feature vector
(features computed in the frame of the state, so psi = theta . phi is a genuine function of the state),
Kempe-graph distances to filled / to non-DL, class id, and, off the sphere, Z/2-homology bits of the lock cycles.
"""
import sys, os, itertools
from collections import deque, Counter
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '../../../..'))
sys.path.insert(0, os.path.join(ROOT, 'backgroundMaterial/planemap-structural/longtable/local-runs/common'))
from kempe_py import Space  # noqa: E402

FEATS = (['j%d' % t for t in range(5)] +
         ['szAA', 'szAB', 'szAM', 'szMA', 'szMB', 'szAB2'] +           # |K_aA(x2)|,|K_aB(x2)|,|K_amu(x2)|,|K_muA(x1)|,|K_muB(x1)|,|K_AB(x3)|
         ['odAA', 'odAB', 'odAM', 'odMA', 'odMB', 'odAB2'] +           # odd-degree (in G) counts in the same components
         ['ncl_a', 'ncl_m', 'ncl_A', 'ncl_B'] +                       # colour-class sizes by role
         ['nc_aM', 'nc_aA', 'nc_aB', 'nc_MA', 'nc_MB', 'nc_AB'] +     # number of Kempe chains per role pair
         ['len1', 'len2', 'lenA', 'lenB'] +                           # shortest lock chains (mu-A x1->x3, mu-B x1->x4); a-A x2->x0, a-B x2->x0 (0 if absent)
         ['dg%d' % t for t in range(5)] +                             # deg(x_{j+t}) ring word in the frame
         ['kdeg', 'dF', 'dS'])                                        # Kempe degree, distance to filled, to single-lock/non-DL unfilled
FEATSETS = {
    'ring': ['j%d' % t for t in range(5)] + ['dg%d' % t for t in range(5)],
    'lockpar': ['odAA', 'odAB', 'odAM', 'odMA', 'odMB', 'odAB2'],
    'comp': ['szAA', 'szAB', 'szAM', 'szMA', 'szMB', 'szAB2', 'odAA', 'odAB', 'odAM', 'odMA', 'odMB', 'odAB2'],
    'global': ['ncl_a', 'ncl_m', 'ncl_A', 'ncl_B', 'nc_aM', 'nc_aA', 'nc_aB', 'nc_MA', 'nc_MB', 'nc_AB'],
    'chains': ['len1', 'len2', 'lenA', 'lenB'],
    'dist': ['kdeg', 'dF', 'dS'],
}
FEATSETS['local'] = FEATSETS['ring'] + FEATSETS['comp'] + FEATSETS['chains']
FEATSETS['all'] = list(FEATS)


def read_graphs(path, names=None):
    out = {}
    for l in open(path):
        p = l.split()
        if len(p) < 3 or (names is not None and p[0] not in names): continue
        out[p[0]] = [list(map(int, r.split(','))) for r in p[2].split(';')]
    return out


def faces_of(rot):
    F = set()
    for v, r in enumerate(rot):
        for i in range(len(r)):
            F.add(frozenset((v, r[i], r[(i + 1) % len(r)])))
    F = list(F); e2f = {}
    for fi, f in enumerate(F):
        for a, b in itertools.combinations(sorted(f), 2): e2f.setdefault((a, b), []).append(fi)
    assert all(len(x) == 2 for x in e2f.values()), 'not a closed triangulated surface'
    return F, e2f


def null_homologous(cycle_vertices, e2f, nF):
    """Z/2: is the closed walk (list of vertices, implicitly closed) a boundary? 2-colour faces, flipping across cycle edges."""
    C = set()
    for a, b in zip(cycle_vertices, cycle_vertices[1:] + cycle_vertices[:1]):
        e = (min(a, b), max(a, b)); C ^= {e}
    nb = [[] for _ in range(nF)]
    for e, (f, g) in e2f.items():
        par = 1 if e in C else 0; nb[f].append((g, par)); nb[g].append((f, par))
    lab = [-1] * nF; lab[0] = 0; q = [0]
    for f in q:
        for g, p in nb[f]:
            if lab[g] < 0: lab[g] = lab[f] ^ p; q.append(g)
            elif lab[g] != lab[f] ^ p: return False
    return True


class HoleData:
    def __init__(self, rot, h, homology=False):
        self.rot = rot; self.h = h; L = rot[h]; assert len(L) == 5
        adj = {v: set(x) for v, x in enumerate(rot)}
        self.sp = sp = Space(adj, h, link=L)
        self.N = sp.N; S = len(sp.states); self.S = S
        self.deg_of_idx = [len(rot[sp.order[i]]) for i in range(sp.N)]
        self.oddmask = 0
        for i in range(sp.N):
            if self.deg_of_idx[i] % 2: self.oddmask |= 1 << i
        self.linkdeg = [len(rot[x]) for x in L]
        if homology: self.F, self.e2f = faces_of(rot)
        self.homology = homology
        sp.build_graph(); sp.classes(); self.cl = sp.cl
        self.kind = [None] * S; self.info = [None] * S; self.pi = [None] * S
        for k in range(S): self._state(k)
        self._dists()

    # BFS shortest path inside mask from bit a to bit b (vertex indices); returns list of idx or None
    def _path(self, M, a, b):
        nbm = self.sp.nbm; prev = {a: None}; q = deque([a])
        while q:
            u = q.popleft()
            if u == b: break
            m = nbm[u] & M
            while m:
                low = m & -m; w = low.bit_length() - 1; m ^= low
                if w not in prev: prev[w] = u; q.append(w)
        if b not in prev: return None
        p = [b]
        while prev[p[-1]] is not None: p.append(prev[p[-1]])
        return p[::-1]

    def _state(self, k):
        sp = self.sp; s = sp.states[k]; li = sp.linki
        c = [s[li[t]] for t in range(5)]; cnt = Counter(c)
        if len(cnt) <= 3: self.kind[k] = 'F'; return
        j = next(t for t in range(5) if c[t] == c[(t + 2) % 5])
        x = [li[(j + t) % 5] for t in range(5)]
        al, mu, A, B = c[j], c[(j + 1) % 5], c[(j + 3) % 5], c[(j + 4) % 5]
        cm = sp.cmasks(s)
        def K(v, p, q): return sp.flood(1 << v, cm[p] | cm[q])
        KMA = K(x[1], mu, A); KMB = K(x[1], mu, B)
        L1 = bool(KMA >> x[3] & 1); L2 = bool(KMB >> x[4] & 1)
        KAA = K(x[2], al, A); KAB = K(x[2], al, B); KAM = K(x[2], al, mu); KAB2 = K(x[3], A, B)
        inA = bool(KAA >> x[0] & 1); inB = bool(KAB >> x[0] & 1)
        pc = lambda m: bin(m).count('1')
        od = lambda m: pc(m & self.oddmask)
        ncomp = lambda p, q: len(sp.components(s, p, q, cm))
        def plen(M, a, b):
            p = self._path(M, a, b); return (len(p) - 1) if p else 0
        f = dict(zip(['j%d' % t for t in range(5)], [1 if t == j else 0 for t in range(5)]))
        f.update(szAA=pc(KAA), szAB=pc(KAB), szAM=pc(KAM), szMA=pc(KMA), szMB=pc(KMB), szAB2=pc(KAB2),
                 odAA=od(KAA), odAB=od(KAB), odAM=od(KAM), odMA=od(KMA), odMB=od(KMB), odAB2=od(KAB2),
                 ncl_a=pc(cm[al]), ncl_m=pc(cm[mu]), ncl_A=pc(cm[A]), ncl_B=pc(cm[B]),
                 nc_aM=ncomp(al, mu), nc_aA=ncomp(al, A), nc_aB=ncomp(al, B), nc_MA=ncomp(mu, A), nc_MB=ncomp(mu, B), nc_AB=ncomp(A, B),
                 len1=plen(KMA, x[1], x[3]) if L1 else 0, len2=plen(KMB, x[1], x[4]) if L2 else 0,
                 lenA=plen(KAA, x[2], x[0]) if inA else 0, lenB=plen(KAB, x[2], x[0]) if inB else 0)
        for t in range(5): f['dg%d' % t] = self.linkdeg[(j + t) % 5]
        f['kdeg'] = len(sp.G[k])
        D1fail = L1 != (not inB); D2fail = L2 != (not inA)
        inf = dict(j=j, L1=L1, L2=L2, inA=inA, inB=inB, D1fail=D1fail, D2fail=D2fail, f=f)
        if self.homology:
            # Z/2 classes of the closed chains through h: C1 = h x1 (mu-A chain) x3 h, C1' = h x1 (mu-B) x4 h,
            # C2A = h x2 (a-A chain) x0 h, C2B = h x2 (a-B) x0 h (shortest paths; None if chain absent)
            o = sp.order; hh = self.h
            def hcls(M, a, b):
                p = self._path(M, a, b)
                if p is None: return None
                return 0 if null_homologous([hh] + [o[i] for i in p], self.e2f, len(self.F)) else 1
            inf['H'] = dict(C_MA=hcls(KMA, x[1], x[3]), C_MB=hcls(KMB, x[1], x[4]),
                            C_AA=hcls(KAA, x[2], x[0]), C_AB=hcls(KAB, x[2], x[0]))
        self.info[k] = inf
        self.kind[k] = 'DL' if (L1 and L2) else 'S'
        if not inA:
            self.pi[k] = sp.index[sp.swap(s, KAA, al, A)]

    def _dists(self):
        G = self.sp.G; S = self.S
        def bfs(src):
            d = [-1] * S; q = deque(src)
            for s in src: d[s] = 0
            while q:
                u = q.popleft()
                for t in G[u]:
                    if d[t] < 0: d[t] = d[u] + 1; q.append(t)
            return d
        self.dF = bfs([k for k in range(S) if self.kind[k] == 'F'])
        self.dS = bfs([k for k in range(S) if self.kind[k] == 'S'])
        for k in range(S):
            if self.info[k] is not None:
                self.info[k]['f']['dF'] = self.dF[k]; self.info[k]['f']['dS'] = self.dS[k]

    def allDL_cycles(self):
        """list of all-DL pi-cycles (lists of states)."""
        seen = set(); cycles = []
        for i in range(self.S):
            if self.kind[i] != 'DL' or i in seen: continue
            path = []; pos = {}; k = i
            while k is not None and self.kind[k] == 'DL' and k not in pos and k not in seen:
                pos[k] = len(path); path.append(k); k = self.pi[k]
            seen.update(path)
            if k is not None and k in pos: cycles.append(path[pos[k]:])
        return cycles

    def dl_steps(self):
        """DL->DL pi-steps (s, pi s), with flag 'on an all-DL cycle'."""
        oncyc = set(x for c in self.allDL_cycles() for x in c)
        out = []
        for k in range(self.S):
            if self.kind[k] == 'DL' and self.pi[k] is not None and self.kind[self.pi[k]] == 'DL':
                out.append((k, self.pi[k], k in oncyc))
        return out
