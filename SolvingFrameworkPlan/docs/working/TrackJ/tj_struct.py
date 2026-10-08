#!/usr/bin/env python3
"""Track J task 1 [data]: structure of N = 9 DL states, checked on sphere triangulations (every degree-5 hole).

Checks / tallies (all DL states satisfy D on the sphere; we record it):
  X1  extra chain: at a DL state with N = 9, c6 - (1,1,2,1,2,1) is a unit vector; which role pair; is the extra
      component link-free (the pair graph has a link-free component)?
  X2  pi-transport identity (any graph, hand): for every DL state c with pi defined,
      (#aA, #mB)(c) == (#aB, #mA)(pi c)   [P2 of c = P3 of pi c, same components].
  X3  corollary: a DL state with N = 9 whose pi-image and pi-preimage are both rigid has its extra chain in P1 (am or AB).
  X4  Kempe neighbourhood (distinct targets != self): rigid -> {pi, pi^-1} (H5);  N = 9 -> which targets; the link-free
      swap Z of the extra component: target kind, N, c6; whether Z(c) is DL with N = 9.
  X5  Remark 7 at N = 9 states: link-free moves preserve N + L1 + L2 mod 2.
usage: tj_struct.py GRAPHFILE STRIDE OFFSET MAXGRAPHS [prefix] > log
"""
import sys
from collections import Counter
from tj_lib import Engine, read_graphs, nholes, RIGID, ROLE


def main():
    gf, stride, off, maxg = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    pref = sys.argv[5] if len(sys.argv) > 5 else ''
    import os
    h0 = os.environ.get('TJ_HOLE0') == '1'   # general graphs: hole 0 only
    E = Engine(dump=True, allholes=not h0, hole=0)
    T = Counter(); k = 0
    for gi, (name, line, rot) in enumerate(read_graphs(gf, pref)):
        if gi % stride != off: continue
        k += 1
        if k > maxg: break
        for js, S in E.run(line, 1 if h0 else nholes(rot)):
            if S is None: T['err'] += 1; continue
            T['holes'] += 1
            pre = {}
            for s in S:   # pi^-1 = mirror move: swap K_{aB}(x_j) (role pair 4, component containing x_j); defined iff not inB
                if s['kind'] and not s['inB']:
                    for (x, pr, lm) in s['mv']:
                        if pr == 4 and (lm >> s['j']) & 1: pre[s['i']] = x
            pre = {k: v for k, v in pre.items()}
            rig = lambda s: s['kind'] == 1 and s['c6'] == RIGID
            for s in S:
                if s['kind'] != 1: continue
                T['DL'] += 1
                T['D_ok'] += (s['inA'] == 0 and s['inB'] == 0)
                if s['pi'] >= 0:
                    t = S[s['pi']]
                    if t['kind'] != 0:
                        ok = (s['c6'][2], s['c6'][3]) == (t['c6'][4], t['c6'][5])
                        T['X2_checked'] += 1; T['X2_fail'] += (not ok)
                tg = {}
                for (x, pr, lm) in s['mv']:
                    if x != s['i']: tg.setdefault(x, []).append((pr, lm))
                deg = len(tg)
                if s['N'] == 8:
                    T['rigid'] += 1
                    T['rigid_deg_' + str(deg)] += 1
                    T['rigid_targets_not_pi'] += sum(1 for x in tg if x != s['pi'] and x != pre.get(s['i'], -2))
                    continue
                if s['N'] != 9: continue
                T['nine'] += 1
                ex = [r for r in range(6) if s['c6'][r] - RIGID[r] == 1]
                if len(ex) != 1 or sum(s['c6']) - 8 != 1: T['X1_shape_fail'] += 1; continue
                r = ex[0]; T['X1_extra_' + ROLE[r]] += 1
                # link-free components of the extra pair
                lf = [(x, lm) for (x, pr, lm) in s['mv'] if pr == r and lm == 0]
                T['X1_linkfree_comps_%d' % len(lf)] += 1
                p = s['pi']; q = pre.get(s['i'])
                pr_rig = p >= 0 and rig(S[p]); q_rig = q is not None and rig(S[q])
                if pr_rig and q_rig:
                    T['X3_bothrigid'] += 1; T['X3_bothrigid_extra_' + ROLE[r]] += 1
                    T['X3_fail'] += r not in (0, 1)
                T['nine_deg_%d_extra_%s' % (deg, ROLE[r])] += 1
                for (x, lm) in lf:
                    z = S[x]
                    kind = 'FDSZ'[z['kind']]
                    T['Z_target_%s' % kind] += 1
                    if z['kind'] == 1:
                        T['Z_target_DL_N%d' % z['N']] += 1
                        if pr_rig and q_rig and r in (0, 1):
                            T['X4_inclass_shape_Ztarget_DL_N%d' % z['N']] += 1
                            if z['N'] == 9:
                                zp, zq = z['pi'], pre.get(z['i'])
                                zr = (zp >= 0 and rig(S[zp])) + (zq is not None and rig(S[zq]))
                                T['NRI_Ztarget_N9_rigidnbrs_%d' % zr] += 1
                                if zr == 2: T['NRI_FAIL'] += 1; print('NRI_FAIL', name, js['hole'], s['i'], x, flush=True)
                    if z['kind']:
                        T['X5_checked'] += 1
                        T['X5_fail'] += ((s['N'] + s['L1'] + s['L2']) - (z['N'] + z['L1'] + z['L2'])) % 2
                # composition of the neighbourhood
                others = [x for x in tg if x != p and x != q and x not in [y for y, _ in lf]]
                T['nine_other_targets_%d' % len(others)] += 1
        if k % 20 == 0:
            print('progress', k, dict(sorted(T.items())), flush=True)
    print('SUMMARY', gf, pref, 'stride', stride, 'off', off, 'graphs', min(k, maxg), dict(sorted(T.items())), flush=True)
    E.close()


if __name__ == '__main__':
    main()
