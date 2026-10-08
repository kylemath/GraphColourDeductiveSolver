#!/usr/bin/env python3
"""Track L [data]: the F12 figure-eight model (exhaustive planar model of every DL Tait state with k(F12) = 1).

c's frame: F12 = Xt u Yt, Xt = v -e0- w1 ... w_{2p} -e3- v (colours 1,2,...,1), Yt = v -e1- y1 ... y_m -e2- v
(colours 1,2,...,2; m odd).  Regions: Rt inside Xt (corners x4, x0; contains e4), Qt inside Yt (corner x2), Ot outer
(corners x1, x3).  Every w_i / y_i carries one colour-3 chord into an adjacent region; chords are non-crossing per region.
Embedding: rotation at v ccw = e0..e4; on Xt (travelled v->w1->..->v) Ot is on the left, Rt on the right; on Yt
(v->y1->..->v) Qt on the left, Ot on the right.

For every instance: DL test (p(F13) = (e1e3)(e0e4)), k(H), k(F13), u = pi~(c) = switch 1<->2 on Xt; u rigid iff
k(H^Xt) = k(H^Yt) = 1 and p(H^Xt) = (e0e2)(e3e4).  At states with k(H) = 2, k(F13) = 1: side of the free {2,3}-cycle C'
relative to H0 (e3 side = sigma-type; e0/e1 side = AB-type).
usage: tl_fig8.py NMAX   (NMAX = max number of cubic vertices 2p + m)"""
import sys, os
from collections import Counter, defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'TrackI'))
from ti_lib import Tait, P   # noqa: E402


def ncm(points):
    if not points:
        yield []; return
    a = points[0]
    for k in range(1, len(points), 2):
        for m1 in ncm(points[1:k]):
            for m2 in ncm(points[k + 1:]):
                yield [(a, points[k])] + m1 + m2


DL12 = P(('e0', 'e3'), ('e1', 'e2')); DL13 = P(('e1', 'e3'), ('e0', 'e4'))
URIG = P(('e0', 'e2'), ('e3', 'e4'))


def instances(p, m):
    W = list(range(1, 2 * p + 1)); Yv = list(range(2 * p + 1, 2 * p + m + 1))
    Xpath = [0] + W + [0]; Ypath = [0] + Yv + [0]
    base = []
    labX = {0: 'e0', 2 * p: 'e3'}; labY = {0: 'e1', m: 'e2'}
    for i in range(2 * p + 1):
        base.append((Xpath[i], Xpath[i + 1], 1 if i % 2 == 0 else 2, labX.get(i)))
    for i in range(m + 1):
        base.append((Ypath[i], Ypath[i + 1], 1 if i % 2 == 0 else 2, labY.get(i)))
    nW = len(W); nY = len(Yv)
    for mw in range(1 << nW):
        inR = [w for w in W if mw >> (w - 1) & 1]; WO = [w for w in W if not mw >> (w - 1) & 1]
        if (len(inR) + 1) % 2: continue
        for my in range(1 << nY):
            inQ = [y for k, y in enumerate(Yv) if my >> k & 1]; YO = [y for k, y in enumerate(Yv) if not my >> k & 1]
            if len(inQ) % 2 or (len(WO) + len(YO)) % 2: continue
            for mR in ncm(inR + ['v']):
                for mQ in ncm(inQ):
                    for mO in ncm(WO + YO[::-1]):
                        E = list(base)
                        for (s, t) in mR:
                            if s == 'v': s, t = t, s
                            E.append((s, 0, 3, 'e4') if t == 'v' else (s, t, 3, None))
                        for (s, t) in mQ + mO: E.append((s, t, 3, None))
                        side = {}
                        for w in inR: side[w] = 'R'
                        for w in WO: side[w] = 'O'
                        for y in inQ: side[y] = 'Q'
                        for y in YO: side[y] = 'O'
                        yield E, (p, m, side)


def rotation(E, p, m, side):
    inc = defaultdict(list)
    for k, (a, b, c, l) in enumerate(E): inc[a].append(k); inc[b].append(k)
    rot = {}
    lab = {E[k][3]: k for k in range(len(E)) if E[k][3]}
    rot[0] = [lab['e0'], lab['e1'], lab['e2'], lab['e3'], lab['e4']]
    n = 2 * p + m
    for x in range(1, n + 1):
        if x <= 2 * p:
            path = [0] + list(range(1, 2 * p + 1)) + [0]; i = x
        else:
            path = [0] + list(range(2 * p + 1, n + 1)) + [0]; i = x - 2 * p
        prv, nxt = path[i - 1], path[i + 1]
        ks = inc[x]
        def oth(k): a, b = E[k][0], E[k][1]; return b if a == x else a
        kc = [k for k in ks if E[k][2] == 3][0]
        kn = [k for k in ks if E[k][2] != 3 and oth(k) == nxt and k != kc]
        kp = [k for k in ks if E[k][2] != 3 and oth(k) == prv and k != kc]
        # when prv == nxt == 0 cannot happen (path length >= 2 for n>=1 on each loop) except p=0 or m small; handle by labels
        if x <= 2 * p:
            kn = [k for k in kn if not (nxt == 0 and E[k][3] != 'e3')]; kp = [k for k in kp if not (prv == 0 and E[k][3] != 'e0')]
            left = side[x] == 'O'
        else:
            kn = [k for k in kn if not (nxt == 0 and E[k][3] != 'e2')]; kp = [k for k in kp if not (prv == 0 and E[k][3] != 'e1')]
            left = side[x] == 'Q'
        assert len(kn) == 1 and len(kp) == 1, (x, kn, kp)
        rot[x] = [kn[0], kc, kp[0]] if left else [kn[0], kp[0], kc]
    return rot


def faces(E, rot):
    face = {}; nf = 0
    for x in rot:
        for k in rot[x]:
            for d0 in [(k, x)]:
                if d0 in face: continue
                d = d0
                while d not in face:
                    face[d] = nf
                    kk, xx = d; a, b = E[kk][0], E[kk][1]; y = b if a == xx else a
                    if a == b: raise ValueError('loop')
                    r = rot[y]; i = r.index(kk); d = (r[(i - 1) % len(r)], y)
                nf += 1
    return face, nf


def regions(E, face, nf, S):
    par = list(range(nf))
    def f(a):
        while par[a] != a: par[a] = par[par[a]]; a = par[a]
        return a
    for k, (a, b, c, l) in enumerate(E):
        if k not in S: par[f(face[(k, a)])] = f(face[(k, b)])
    return f


def comps(E, S):
    par = {}
    def f(a):
        par.setdefault(a, a)
        while par[a] != a: par[a] = par[par[a]]; a = par[a]
        return a
    for k in S: par[f(E[k][0])] = f(E[k][1])
    out = defaultdict(set)
    for k in S: out[f(E[k][0])].add(k)
    return list(out.values())


def analyse(E, p, m, side, want_side=True):
    T = Tait(E)
    M = {c: {k for k, e in enumerate(E) if e[2] == c} for c in (1, 2, 3)}
    H = M[2] | M[3]; F12 = M[1] | M[2]; F13 = M[1] | M[3]
    if T.pairing(F13) != DL13: return None
    assert T.pairing(F12) == DL12
    Xt = set(T.trail(F12, T.lab['e0'])[0]); Yt = set(T.trail(F12, T.lab['e1'])[0])
    r = dict(T=T, M=M, H=H, F12=F12, F13=F13, Xt=Xt, Yt=Yt)
    r['kH'] = T.ncomp(H); r['k13'] = T.ncomp(F13)
    HX = H ^ Xt; HY = H ^ Yt
    r['kHX'] = T.ncomp(HX); r['kHY'] = T.ncomp(HY); r['pHX'] = T.pairing(HX)
    r['u_rigid'] = r['kHX'] == 1 and r['kHY'] == 1 and r['pHX'] == URIG
    r['u_DL'] = r['pHX'] == URIG
    if want_side and r['kH'] == 2:
        rot = rotation(E, p, m, side); face, nf = faces(E, rot)
        nV = 2 * p + m + 1
        assert nf == len(E) - nV + 2, 'Euler'
        cs = comps(E, H)
        H0 = [c for c in cs if T.lab['e2'] in c][0]; Cp = [c for c in cs if T.lab['e2'] not in c][0]
        f = regions(E, face, nf, H0)
        k1, k3 = T.lab['e1'], T.lab['e3']
        s1 = f(face[(k1, E[k1][0])]); s3 = f(face[(k3, E[k3][0])])
        assert s1 != s3
        kc = next(iter(Cp)); sc = f(face[(kc, E[kc][0])])
        r['side'] = 'sigma(e3)' if sc == s3 else ('AB(e1)' if sc == s1 else '??')
        r['H0'] = H0; r['Cp'] = Cp; r['face'] = face; r['regf'] = f
    return r


def main():
    NMAX = int(sys.argv[1])
    for n in range(1, NMAX + 1):
        st = Counter()
        for p in range(0, n // 2 + 1):
            m = n - 2 * p
            if m < 1 or m % 2 == 0: continue
            for E, (pp, mm, side) in instances(p, m):
                r = analyse(E, pp, mm, side)
                if r is None: continue
                st['DL'] += 1
                if r['kH'] != 2 or r['k13'] != 1: continue
                st[('kH2k13=1', 'u_rigid' if r['u_rigid'] else ('uDL' if r['u_DL'] else 'uNDL'), r['kHX'], r['kHY'], r['side'])] += 1
        print('n', n, dict(sorted(st.items(), key=str)), flush=True)


if __name__ == '__main__':
    main()
