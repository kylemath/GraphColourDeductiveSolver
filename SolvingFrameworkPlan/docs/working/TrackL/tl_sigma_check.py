#!/usr/bin/env python3
"""Track L [data]: step-by-step check of the proof of the sigma-type lemma (TrackL/SigmaType.md).

chi(XY) := |X| + |Y| - e(X,Y) for the pair graph G[{X,Y}] of T - h (= #components - cycle rank).
Role order of pairs: am, AB, aA, mB, aB, mA.
Checks, at every DL state u with pi(u) = c defined (c any kind):
  S0 (star identity, any graph): chi_c(a_c A_c) + chi_c(A_c B_c) == chi_u(am) + chi_u(mA)
       [pi swaps alpha<->A on K; c's roles are (alpha, B, mu, A) in u's colour names, so a_cA_c = {alpha,mu},
        A_cB_c = {mu,A}]; also chi_c(a_c B_c) + chi_c(m_c B_c)?? not needed.
       The mirror form at pi^-1:  chi(a_c B_c) + chi(A_c B_c) for c = pi~(u'), u' = pi(c)... checked as S0m:
       for every DL c with pi(c) = u' defined: chi_c(aB) + chi_c(AB) == chi_u'(a'B') + chi_u'(A'B') ... (see below)
  S1 rigid => all six pair graphs are trees/forests with chi = counts (1,1,2,1,2,1)
  S2 at DL c with P2 counts (2,1): chi(aA) = 2, chi(mB) = 1 (forests)   [and the mirror: P3 counts (2,1) => forests]
  S3 at DL c = pi(u), u rigid, P2(c) minimal: chi(AB) == 0
  S4 at in-shape c: extra chain is am (sigma-type), chi vector == (2,0,2,1,2,1)
usage: tl_sigma_check.py GRAPHFILE STRIDE OFFSET MAXGRAPHS"""
import sys
from collections import Counter
from tl_lib import HoleData, read_graphs, RIGID


def chis(hd, i):
    r = hd.info[i]; col = hd.col[i]; al, mu, A, B = r['roles']; Hh = hd.Hh
    out = []
    for p, q in [(al, mu), (A, B), (al, A), (mu, B), (al, B), (mu, A)]:
        V = [v for v in Hh.V if col[v] in (p, q)]
        e = sum(1 for v in V for w in Hh.adj[v] if w > v and col[w] in (p, q))
        out.append(len(V) - e)
    return tuple(out)


def main():
    gf, stride, off, maxg = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    T = Counter()
    for name, rot in read_graphs(gf, stride, off, maxg):
        for h in [v for v in range(len(rot)) if len(rot[v]) == 5]:
            hd = HoleData(rot, h); T['holes'] += 1
            X = {}
            def chi(i):
                if i not in X: X[i] = chis(hd, i)
                return X[i]
            for u in range(hd.S):
                ru = hd.info[u]
                if ru['kind'] == 'F': continue
                if ru['kind'] == 'DL':
                    T['DL'] += 1
                    xu = chi(u)
                    if hd.rigid(u):
                        T['S1_rigid'] += 1; T['S1_fail'] += xu != RIGID
                    c6 = ru['c6']
                    if (c6[2], c6[3]) == (2, 1):
                        T['S2_P2min'] += 1; T['S2_fail'] += (xu[2], xu[3]) != (2, 1)
                    if (c6[4], c6[5]) == (2, 1):
                        T['S2m_P3min'] += 1; T['S2m_fail'] += (xu[4], xu[5]) != (2, 1)
                # S0: star identity for pi (u DL or not, as long as pi defined and c unfilled)
                c = ru.get('pi')
                if ru['kind'] == 'DL' and c is not None and hd.info[c]['kind'] != 'F':
                    xu = chi(u); xc = chi(c)
                    T['S0_steps'] += 1
                    T['S0_fail'] += (xc[2] + xc[1]) != (xu[0] + xu[5])
                    # second star identity (colour B of u): chi(aB)+chi(AB) of u == chi_c(a_c mu_c) + chi_c(mu_c B_c)
                    #   c roles (alpha,B,mu,A): {B,alpha} = a_c m_c, {B,A} = m_c B_c
                    T['S0b_fail'] += (xc[0] + xc[3]) != (xu[4] + xu[1])
                    T['S0c_fail'] += (xc[4], xc[5]) != (xu[2], xu[3])     # J2
                    if hd.rigid(u) and hd.info[c]['kind'] == 'DL':
                        rc = hd.info[c]
                        if (rc['c6'][2], rc['c6'][3]) == (2, 1):
                            T['S3_cases'] += 1; T['S3_fail'] += xc[1] != 0
                            if rc['N'] == 9:
                                T['S3_N9'] += 1; T['S3_N9_notsigma'] += hd.extra(c) != [0]
            for i in range(hd.S):
                if hd.inshape(i):
                    T['S4_inshape'] += 1
                    T['S4_fail'] += hd.extra(i) != [0] or chi(i) != (2, 0, 2, 1, 2, 1)
    print(gf, stride, off, dict(sorted(T.items())), flush=True)


if __name__ == '__main__':
    main()
