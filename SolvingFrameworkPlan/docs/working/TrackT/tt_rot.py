#!/usr/bin/env python3
"""Track T: role of the rotation at v.  Take a sphere hole's Tait dual G (planar, cubic except v) but relabel the
v-edges f0..f4 by every cyclic order (24 = 4! orders with f0 fixed; the planar one and its mirror among them).
For each order run the matching dynamics from every Hamiltonian DL-type state and record:
  law violations (consecutive DL-type states with k(H) of equal parity), longest R-run (k(H) alternating 1,2),
  longest NRC-M window, closed orbits.
usage: tt_rot.py GRAPHFILE stride off maxg > out.jsonl"""
import sys, json, itertools
from tt_lib import G5, tait_dual, ham_states, run_from, run_back
from tt_abstract import rrun_len
from tt_runs import nrcm_len


def stats(g):
    hs = ham_states(g); seen = set(); viol = 0; steps = 0; rr = 0; nm = 0; closed = []
    for P, M in hs:
        if (P, M) in seen or g.dl_info(P, M) is None: continue
        fw, cl = run_from(g, P, M, maxlen=200)
        if cl is not True and g.dl_info(*fw[-1]) is None: fw = fw[:-1]
        bw = run_back(g, P, M, maxlen=200) if cl is not True else [(P, M)]
        st = list(reversed(bw))[:-1] + fw
        for s in st: seen.add(s)
        w = [g.kH(*s) for s in st]
        if cl is True:
            closed.append(''.join(str(min(x, 9)) for x in w)); w2 = w + w[:1]
        else:
            w2 = w
        # the law N(pi c) - N(c) odd with N = 5 + k(H) + k(F12) + k(F13) reduces to k(H) parity alternation
        # only when F12 = Q_{t-1} is connected at both states: skip the first state of an open run
        for i in range(0 if cl is True else 1, len(w2) - 1):
            steps += 1; viol += (w2[i] - w2[i + 1]) % 2 == 0
        rr = max(rr, rrun_len(w + w if cl is True else w)); nm = max(nm, nrcm_len(w))
    return dict(steps=steps, viol=viol, rrun=rr, nrcm=nm, closed=closed[:4], nclosed=len(closed))


def main():
    path, s, off, mx = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]); k = 0
    for ln, l in enumerate(open(path)):
        if ln % s != off: continue
        k += 1
        if k > mx: break
        p = l.split(); rot = [list(map(int, r.split(','))) for r in p[2].split(';')]
        for h in range(len(rot)):
            if len(rot[h]) != 5: continue
            g0 = tait_dual(rot, h)
            for perm in itertools.permutations(range(1, 5)):
                order = (0,) + perm
                fv = [g0.fv[i] for i in order]
                g = G5(g0.n, g0.E, fv)
                planar = order in ((0, 1, 2, 3, 4), (0, 4, 3, 2, 1))
                r = stats(g); r.update(g=p[0], h=h, order=order, planar=planar)
                print(json.dumps(r), flush=True)


if __name__ == '__main__':
    main()
