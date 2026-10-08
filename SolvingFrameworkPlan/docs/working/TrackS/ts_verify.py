#!/usr/bin/env python3
"""Track S: data check of the matching form of near-rigid runs (Lemmas S1-S4 of README.md).

For every DL state t of every pi-run inside Q = {DL, F13 connected} (and in particular every R-run), in the Tait dual
(colour 2 = M_t, colour 3 = M_{t-1}, colour 1 = C_t; Q_t = E - M_t = F13(t)):
  V1  Q_t has exactly two perfect matchings (v covered once), using v-edges e_j and e_{j+4};
  V2  colour-3 class of t = colour-2 class of pi^{-1}(t)  (M_{t-1}; transport)  -- when pi^{-1}(t) is DL;
  V3  colour-2 class of pi(t) is the PM of Q_t through e_j, the colour-3 class of t is the PM through e_{j+4};
  V4  M_{t+1} xor M_{t-1} = Y_t (the F13-loop of v through e_j, e_{j+4});
  V5  (primal, any graph) P2(pi t) = P2(pi^-1 t) xor delta(K_aA(x_j)) as primal edge sets, whenever #aA(t) = 2.
usage: ts_verify.py GRAPHFILE name:hole ...  |  GRAPHFILE stride off maxg"""
import sys, json
from collections import Counter
from ts_lib import load_graphs, HoleData
from tl_lib import TaitState
import os
TAIT = os.environ.get('TS_TAIT') == '1'   # hypothesis by Tait connectivity of F13 (needed off the sphere)


def pms_of_fig8(T, Q):
    """perfect matchings of the subgraph Q (edge ids) in which v=0 has degree 4 and others degree 2 (or 0)"""
    out = []
    vq = [k for k in Q if 0 in T.E[k][:2]]
    for k0 in vq:
        M = {k0}; covered = {0, T.other(k0, 0)}; ok = True
        # walk every loop; alternate starting from matched edges
        # simple propagation: repeatedly, for an uncovered vertex with a unique available Q-edge, take it
        verts = {a for k in Q for a in T.E[k][:2]}
        changed = True
        while changed and ok:
            changed = False
            for x in verts:
                if x in covered: continue
                av = [k for k in T.inc[x] if k in Q and T.other(k, x) not in covered]
                if len(av) == 0: ok = False; break
                if len(av) == 1:
                    M.add(av[0]); covered |= {x, T.other(av[0], x)}; changed = True
        if ok and covered >= verts:
            # remaining choice-free check: every vertex covered exactly once
            cnt = Counter(a for k in M for a in T.E[k][:2])
            if all(cnt[x] == 1 for x in verts): out.append(frozenset(M))
        elif ok:
            # undetermined cycles remain (Q disconnected) -> mark
            out.append(None)
    return out


def primal_P2(hd, i):
    r = hd.info[i]; col = hd.col[i]; al, mu, A, B = r['roles']
    P = set()
    for v in hd.Hh.V:
        for w in hd.Hh.adj[v]:
            if v < w and {col[v], col[w]} in ({al, A}, {mu, B}): P.add((v, w))
    return P


def main():
    a = sys.argv
    if ':' in a[2]:
        G = load_graphs(a[1], {s.rsplit(':', 1)[0] for s in a[2:]})
        specs = [(s.rsplit(':', 1)[0], int(s.rsplit(':', 1)[1])) for s in a[2:]]
    else:
        s, off, mx = int(a[2]), int(a[3]), int(a[4]); G = {}; specs = []
        for ln, l in enumerate(open(a[1])):
            if ln % s != off: continue
            p = l.split(); rot = [list(map(int, r.split(','))) for r in p[2].split(';')]
            G[p[0]] = rot; specs += [(p[0], h) for h in range(len(rot)) if len(rot[h]) == 5]
            if len(G) >= mx: break
    C = Counter()
    for nm, h in specs:
        hd = HoleData(G[nm], h)
        info = hd.info
        isQ = lambda i: info[i]['kind'] == 'DL' and info[i]['c6'][2] + info[i]['c6'][3] == 3
        pre = {}
        for i in range(hd.S):
            if info[i]['kind'] == 'DL' and info[i]['pi'] is not None: pre[info[i]['pi']] = i
        TS = {}

        def ts(i):
            if i not in TS: TS[i] = TaitState(hd, i)
            return TS[i]
        for t in range(hd.S):
            if not isQ(t): continue
            St = ts(t); T = St.T; E = St.E
            if TAIT and T.ncomp(St.F13) != 1: continue
            M = {k for k, e in enumerate(E) if e[2] == 2}; M3 = {k for k, e in enumerate(E) if e[2] == 3}
            Q = set(range(len(E))) - M
            pm = pms_of_fig8(T, Q)
            C['states'] += 1
            vlab = lambda P: sorted(E[k][3] for k in P if E[k][3])
            ok1 = len(pm) == 2 and None not in pm and sorted(sum((vlab(P) for P in pm), [])) == ['e0', 'e4']
            C['V1_fail'] += not ok1
            pj = [P for P in pm if P is not None and 'e0' in vlab(P)]
            p4 = [P for P in pm if P is not None and 'e4' in vlab(P)]
            C['V3b_fail'] += not (p4 and p4[0] == frozenset(M3))
            Y = set(St.Y)
            u = info[t]['pi']
            if u is not None and info[u]['kind'] == 'DL':
                Su = ts(u); Mn = {k for k, e in enumerate(Su.E) if e[2] == 2}
                C['V3a_n'] += 1; C['V3a_fail'] += not (pj and pj[0] == frozenset(Mn))
                C['V4_n'] += 1; C['V4_fail'] += (Mn ^ M3) != Y
                C['disjoint_fail'] += bool(Mn & M)
            p = pre.get(t)
            if p is not None and info[p]['kind'] == 'DL':
                Sp = ts(p); Mp = {k for k, e in enumerate(Sp.E) if e[2] == 2}
                C['V2_n'] += 1; C['V2_fail'] += Mp != M3
            # V5 primal
            if u is not None and info[u]['kind'] != 'F' and p is not None and info[t]['c6'][2] == 2:
                x = info[t]['x']; col = hd.col[t]; al, mu, A, B = info[t]['roles']
                K0 = hd.Hh.comp(col, x[0], (al, A))
                d = {(v, w) for v in hd.Hh.V for w in hd.Hh.adj[v] if v < w and ((v in K0) != (w in K0))}
                C['V5_n'] += 1; C['V5_fail'] += primal_P2(hd, u) != (primal_P2(hd, p) ^ d)
        print(nm, h, dict(C), flush=True)
    print('TOTAL', json.dumps(dict(C)))


if __name__ == '__main__':
    main()
