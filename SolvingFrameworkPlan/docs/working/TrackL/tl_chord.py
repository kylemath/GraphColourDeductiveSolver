#!/usr/bin/env python3
"""Track L [data]: sigma-type lemma in the planar chord model (all rigid DL Tait instances, TrackH/TrackI model,
instances from TrackI ti_lib.chord_instances, imported read-only).

For a rigid u with c = pi(u) DL and N(c) = 9 with the extra chain in P1 (k(F12^X) = 2, k(H^X) = 1), the {2,3}-factor
of c is H_c = F12 ^ X = H ^ Y (two curves: H0_c through v via e0, e2 [= e'2, e'4 in c's frame], and a free curve C').
sigma-type <=> C' lies on the side of H0_c containing e1 (= e'3), not on the side containing e3, e4 (= e'0, e'1).
The embedding: H is the circle v=0,u1..uN drawn counter-clockwise; chord ends in I are inside, in O outside.
usage: tl_chord.py NMAX"""
import sys, os
from collections import Counter, defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'TrackI'))
from ti_lib import chord_instances, analyse   # noqa: E402


def faces_of(E, N, I_set):
    """rotation system of the chord model and its faces as lists of darts; returns face id per dart (edge id, end)"""
    # darts: (k, s) = edge k traversed from end s (0: from E[k][0], 1: from E[k][1])
    rot = defaultdict(list)
    inc = defaultdict(dict)
    for k, (a, b, c, l) in enumerate(E):
        inc[a][k] = 0; inc[b][k] = 1
    for x in range(N + 1):
        ks = list(inc[x].keys())
        def other(k):
            a, b = E[k][0], E[k][1]; return b if a == x else a
        if x == 0:
            lab = {E[k][3]: k for k in ks}
            order = [lab['e2'], lab['e3'], lab['e4'], lab['e0'], lab['e1']]
        else:
            nxt = [k for k in ks if E[k][2] != 1 and other(k) == (x + 1) % (N + 1)]
            prv = [k for k in ks if E[k][2] != 1 and other(k) == (x - 1) % (N + 1)]
            ch = [k for k in ks if E[k][2] == 1]
            assert len(nxt) == 1 and len(prv) == 1 and len(ch) == 1, (x, ks)
            if x in I_set: order = [nxt[0], ch[0], prv[0]]
            else: order = [nxt[0], prv[0], ch[0]]
        rot[x] = order
    # face tracing: dart d = (k, x) leaving x along k; next dart around face: at y = other end, take the edge after k
    # in clockwise order = before k in the ccw rotation
    face = {}; nf = 0
    for x in rot:
        for k in rot[x]:
            if (k, x) in face: continue
            d = (k, x)
            while d not in face:
                face[d] = nf
                kk, xx = d; a, b = E[kk][0], E[kk][1]; y = b if a == xx else a
                r = rot[y]; i = r.index(kk); d = (r[(i - 1) % len(r)], y)
            nf += 1
    return face, rot, nf


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


def main():
    NMAX = int(sys.argv[1])
    for N in range(3, NMAX + 1, 2):
        st = Counter()
        for E, (mask, mi, mo) in chord_instances(N):
            r = analyse(E)
            if r is None or not r['rigid']: continue
            st['rigid'] += 1
            Hc = r['F12X']
            key = (r['kHX'], r['kF12X'])
            if r['img_dl']: st[('img_DL', key)] += 1
            if r['kF12X'] != 2: continue
            I_set = {u for u in range(1, N + 1) if mask >> (u - 1) & 1}
            face, rot, nf = faces_of(E, N, I_set)
            assert nf == len(E) - (N + 1) + 2, 'Euler'
            cs = comps(E, Hc); assert len(cs) == 2
            lab = r['T'].lab
            H0 = [c for c in cs if lab['e2'] in c][0]; Cp = [c for c in cs if lab['e2'] not in c][0]
            assert lab['e0'] in H0
            f = regions(E, face, nf, H0)
            # corner (e0,e1) at v: face to the ... use the face on each side: dart leaving v along e1 has on its left the
            # corner (e1, next ccw) ; simpler: e1 is not in H0, so both faces of e1 are in the e1-side region.
            k1 = lab['e1']; k3 = lab['e3']
            s1 = f(face[(k1, E[k1][0])]); s3 = f(face[(k3, E[k3][0])])
            assert s1 != s3
            kc = next(iter(Cp)); sc = f(face[(kc, E[kc][0])])
            side = 'e1side(sigma)' if sc == s1 else ('e3side(AB)' if sc == s3 else '??')
            st[('DL' if r['img_dl'] else 'nDL', 'kHX=%d' % r['kHX'], side)] += 1
        print('N', N, dict(sorted(st.items(), key=str)), flush=True)


if __name__ == '__main__':
    main()
