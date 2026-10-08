"""Track I review: step-by-step check of Lemmas 1, 2, 4, (P-i), (P-ii), (L1)-(L4), Lemma R
conclusion and Lemma 5, in an independently built Tait graph G = (T*)/h*.

Everything here is computed from the surface faces and the primal colouring only.
"""
from collections import defaultdict
from ri_core import component


class UF:
    def __init__(s, n):
        s.p = list(range(n))
    def f(s, x):
        while s.p[x] != x:
            s.p[x] = s.p[s.p[x]]; x = s.p[x]
        return x
    def u(s, a, b):
        a, b = s.f(a), s.f(b)
        if a != b:
            s.p[a] = b


class Tait:
    """G built from surface s, hole h; vertices: 0 = v, 1.. = triangles avoiding h.
    edges: one per edge of T-h; endpoints (gv1, gv2); prim = (u, w) primal ends (T-h indices)."""
    def __init__(self, s, h, ix, xabs):
        # xabs: link vertices (surface ids) relative to the frame j: x_0..x_4
        self.fid = {}
        k = 1
        for f in sorted(s.faces, key=lambda f: tuple(sorted(f))):
            if h not in f:
                self.fid[f] = k; k += 1
        self.nv = k
        self.ends = []; self.prim = []
        self.inc = defaultdict(list)
        self.vedge = {}
        for e, fs in s.ef.items():
            if h in e:
                continue
            u, w = tuple(e)
            gv = [0 if h in f else self.fid[f] for f in fs]
            eid = len(self.ends)
            self.ends.append(tuple(gv)); self.prim.append((ix[u], ix[w]))
            for g in gv:
                self.inc[g].append(eid)
            if gv[0] == 0 or gv[1] == 0:
                assert gv.count(0) == 1, 'loop at v'
                for t in range(5):
                    if e == frozenset((xabs[t], xabs[(t + 1) % 5])):
                        self.vedge[t] = eid
        assert len(self.vedge) == 5 and len(self.inc[0]) == 5
        self.e = [self.vedge[t] for t in range(5)]
        self.tof = {eid: t for t, eid in self.vedge.items()}
        for g in range(1, self.nv):
            assert len(self.inc[g]) == 3

    def other(self, eid, g):
        a, b = self.ends[eid]
        return b if a == g else a

    def kcomp(self, S):
        uf = UF(self.nv)
        for e in S:
            uf.u(*self.ends[e])
        verts = set()
        for e in S:
            verts.update(self.ends[e])
        return len({uf.f(g) for g in verts}), uf, verts

    def pairing(self, S):
        """pairing of v-edges in S (as frozenset of frozensets of t-indices)."""
        vs = [t for t in range(5) if self.e[t] in S]
        pairs = set(); done = set()
        for t in vs:
            if t in done:
                continue
            eid = self.e[t]; g = self.other(eid, 0); steps = 0
            while g != 0:
                nx = [x for x in self.inc[g] if x in S and x != eid]
                assert len(nx) == 1, ('deg', len(nx))
                eid = nx[0]; g = self.other(eid, g); steps += 1
                assert steps < 10 ** 6
            s2 = self.tof[eid]
            pairs.add(frozenset((t, s2))); done.update((t, s2))
        return frozenset(pairs)


def P(*ps):
    return frozenset(frozenset(p) for p in ps)


def crossing(pairing, order):
    pos = {t: i for i, t in enumerate(order)}
    ps = [tuple(sorted((pos[a], pos[b]))) for a, b in (tuple(p) for p in pairing)]
    for i in range(len(ps)):
        for k in range(i + 1, len(ps)):
            a, b = ps[i]; c, d = ps[k]
            if (a < c < b) != (a < d < b):
                return True
    return False


def ncycles(n_pts, M1, M2):
    """number of cycles of the union of two perfect matchings (dicts point->point)."""
    seen = set(); k = 0
    for p in M1:
        if p in seen:
            continue
        k += 1; q = p
        while True:
            seen.add(q); q = M1[q]; seen.add(q); q = M2[q]
            if q == p:
                break
    return k


def check_state(s, h, ix, nbr, col, st, stp, Kset, Np, Nc):
    """returns dict of step results (True = holds)."""
    x = st['x']
    V_inv = {i: v for v, i in ix.items()}
    xabs = [V_inv[i] for i in x]
    T = Tait(s, h, ix, xabs)
    al, mu, A, B = st['al'], st['mu'], st['A'], st['B']
    name = {al ^ mu: 1, al ^ A: 2, al ^ B: 3}
    colour = [name[col[u] ^ col[w]] for (u, w) in T.prim]
    E = range(len(T.ends))
    M = {i: {e for e in E if colour[e] == i} for i in (1, 2, 3)}
    H = M[2] | M[3]; F12 = M[1] | M[2]; F13 = M[1] | M[3]
    r = {}
    r['vcol'] = [colour[T.e[t]] for t in range(5)] == [1, 1, 2, 1, 3]
    kH = T.kcomp(H)[0]; k12 = T.kcomp(F12)[0]; k13 = T.kcomp(F13)[0]
    from ri_core import n_components
    cnt = lambda p, q: n_components(nbr, col, p, q)
    r['L1dict'] = (cnt(al, mu) + cnt(A, B) == 1 + kH and cnt(al, A) + cnt(mu, B) == 2 + k13
                   and cnt(al, B) + cnt(mu, A) == 2 + k12 and Nc == 5 + kH + k12 + k13)
    p12 = T.pairing(F12); p13 = T.pairing(F13)
    r['L0'] = (not crossing(p12, [0, 1, 2, 3])) and (not crossing(p13, [0, 1, 3, 4]))
    r['L2lock1'] = (st['L1'] == (p12 == P((0, 3), (1, 2))))
    r['L2lock2'] = (st['L2'] == (p13 == P((1, 3), (0, 4))))
    # region R and C
    inK = lambda u: u in Kset
    C = {e for e in E if inK(T.prim[e][0]) != inK(T.prim[e][1])}
    r['L4C_sub_F13'] = C <= F13
    r['L4C_v'] = {t for t in range(5) if T.e[t] in C} == {1, 3}
    # pi colouring = 1<->3 on C
    if stp is not None:
        colp = stp['col']
        ok = True
        for e in E:
            u, w = T.prim[e]
            nv = name[colp[u] ^ colp[w]]
            exp = colour[e] if e not in C else {1: 3, 3: 1}[colour[e]]
            if nv != exp:
                ok = False; break
        r['L4a'] = ok
    # whole components: every cubic vertex has C-degree 0 or 2
    cdeg = defaultdict(int)
    for e in C:
        for g in T.ends[e]:
            cdeg[g] += 1
    r['L4b_whole'] = all(d in (0, 2) for g, d in cdeg.items() if g != 0) and cdeg[0] == 2
    # trace X from e1
    X = [T.e[1]]; g = T.other(T.e[1], 0); seq = []
    while g != 0:
        seq.append(g)
        nx = [y for y in T.inc[g] if y in C and y != X[-1]]
        assert len(nx) == 1
        X.append(nx[0]); g = T.other(nx[0], g)
    r['L4b_X_e3'] = X[-1] == T.e[3]
    nZ = 0
    # components of C other than X
    restC = C - set(X)
    kz = T.kcomp(restC)[0] if restC else 0
    r['holed'] = kz > 0
    rigid_like = (kH == 1 and k12 == 1 and k13 == 1)
    if rigid_like:
        r['L4b_rigidCX'] = (restC == set())
    HdC = H ^ C; FdC = F12 ^ C
    pHdC = T.pairing(HdC)
    if stp is not None:
        r['L4d'] = (stp['DL'] == (pHdC == P((1, 4), (2, 3))))
        r['L4d_lock1'] = stp['L1']
        # 4c: counts of pi(c) via its own frame
        kHd = T.kcomp(HdC)[0]; kFd = T.kcomp(FdC)[0]
        r['L4c_N'] = (Np == 5 + kHd + k13 + kFd)
    r['L0_HdC'] = not crossing(pHdC, [1, 2, 3, 4])
    # ---------------- the model
    Cverts = set()
    for e in C:
        Cverts.update(T.ends[e])
    Cverts.discard(0)
    pts = list(Cverts) + ['a', 'b']
    # circles: sequences
    circles = [['a'] + seq + ['b']]
    seen = set(seq)
    for g0 in Cverts:
        if g0 in seen:
            continue
        cyc = [g0]; seen.add(g0)
        prevE = None; g = g0
        while True:
            nx = [y for y in T.inc[g] if y in C and y != prevE]
            y = nx[0]; g2 = T.other(y, g)
            prevE = y
            if g2 == g0:
                break
            cyc.append(g2); seen.add(g2); g = g2
        circles.append(cyc)
    circ_of = {}; pos = {}
    for ci, cyc in enumerate(circles):
        for i, p in enumerate(cyc):
            circ_of[p] = ci; pos[p] = i
    def endpt(eid, g):
        # point represented when arriving at g via eid
        if g == 0:
            t = T.tof[eid]
            return {1: 'a', 2: 'a', 3: 'b', 4: 'b', 0: 'b'}[t]
        return g
    B1 = {}; B3 = {}
    for e in C:
        g1, g2 = T.ends[e]
        p1 = endpt(e, g1); p2 = endpt(e, g2)
        (B1 if colour[e] == 1 else B3)[p1] = p2
        (B1 if colour[e] == 1 else B3)[p2] = p1
    B3['a'] = 'b'; B3['b'] = 'a'
    r['B_perfect'] = (set(B1) == set(pts) and set(B3) == set(pts))
    trans = {}
    for g0 in Cverts:
        tw = [y for y in T.inc[g0] if colour[y] == 2]
        assert len(tw) == 1
        trans[g0] = tw[0]
    def side_in_R(eid):
        u, w = T.prim[eid]
        return inK(u)
    def paths(S, o):
        Npair = {}; single2 = {}; side = {}
        for p in pts:
            if p == 'a':
                eid = T.e[2]; g = 0
            elif p == 'b':
                eid = T.e[o]; g = 0
            else:
                eid = trans[p]; g = p
            side[p] = side_in_R(eid)
            first = eid; length = 1
            cur = T.other(eid, g)
            while True:
                if cur == 0:
                    t = T.tof[eid]
                    q = 'a' if t == 2 else ('b' if t == o else None)
                    assert q is not None
                    break
                if cur in Cverts:
                    q = cur; break
                nx = [y for y in T.inc[cur] if y in S and y not in C and y != eid]
                assert len(nx) == 1
                eid = nx[0]; cur = T.other(eid, cur); length += 1
            Npair[p] = q
            single2[p] = (length == 1 and colour[first] == 2)
        return Npair, single2, side
    NH, sH, sideH = paths(H, 4)
    NF, sF, sideF = paths(F12, 0)
    r['N_sym'] = all(NH[NH[p]] == p for p in pts) and all(NF[NF[p]] == p for p in pts)
    r['labels_same'] = sideH == sideF
    Ipts = [p for p in pts if sideH[p]]
    r['Pi'] = all(sH[p] and sF[p] and NH[p] == NF[p] for p in Ipts)
    # (P-ii)
    def noncrossing_O(Npair):
        Opts = [p for p in pts if not sideH[p]]
        ok_same = all(circ_of[p] == circ_of[Npair[p]] for p in Opts)
        if not ok_same:
            return False, False
        prs = {tuple(sorted((pos[p], pos[Npair[p]]))) + (circ_of[p],) for p in Opts}
        prs = list(prs)
        for i in range(len(prs)):
            for k in range(i + 1, len(prs)):
                a, b, c1 = prs[i]; c, d, c2 = prs[k]
                if c1 != c2:
                    continue
                if (a < c < b) != (a < d < b):
                    return True, False
        return True, True
    sameH, ncH = noncrossing_O(NH); sameF, ncF = noncrossing_O(NF)
    r['Pii_samecircle'] = sameH and sameF
    r['Pii_noncross'] = ncH and ncF
    r['Pii_noncross_H'] = ncH; r['Pii_noncross_F'] = ncF
    # f_S
    def fS(S):
        k, uf, verts = T.kcomp(S)
        roots = {uf.f(g) for g in verts}
        croots = {uf.f(g) for g in Cverts | {0} if g in verts}
        return len(roots - croots)
    fH = fS(H); fF = fS(F12)
    lam = lambda Bm, Nm: ncycles(len(pts), Bm, Nm)
    l3H = lam(B3, NH); l1H = lam(B1, NH); l3F = lam(B3, NF); l1F = lam(B1, NF)
    kHdC = T.kcomp(HdC)[0]; kFdC = T.kcomp(FdC)[0]
    r['Lm1'] = l3H == kH - fH
    r['Lm2'] = l1H == kHdC - fH + (pHdC == P((1, 2), (3, 4)))
    r['Lm3'] = l3F == kFdC - fF
    r['Lm4'] = l1F == k12 - fF + (p12 == P((1, 2), (3, 0)))
    r['LemmaR_concl'] = ((l3H + l1H) - (l3F + l1F)) % 2 == 0
    r['Lemma5'] = (kH + k12 + kHdC + kFdC) % 2 == int(pHdC == P((1, 4), (2, 3)))
    return r
