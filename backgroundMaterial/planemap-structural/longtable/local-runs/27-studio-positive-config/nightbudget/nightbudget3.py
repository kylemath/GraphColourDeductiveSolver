#!/usr/bin/env python3
"""[exploratory] NightBudget pass 3: for every literal-R state r with a failing sigma-image ((5,5,5,5,6) holes, both orientations),
does r have a sigma'-exit (link-free swap) to a lockless state, and to one outside sigma(R)? Counts by (source, k, image kind)."""
import sys, os, json
from collections import Counter
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import nightbudget as NB
from uv_lib import Hole
def job(args):
    src, name, rot, _ = args; C = Counter()
    for h, pat in NB.holes_of(rot):
        if pat != (5, 5, 5, 5, 6): continue
        for mirror in (False, True):
            H = Hole(name, h, mirror, rot=[list(x) for x in rot]); S = H.S; pi = H.pi; pinv = H.pinv
            filled = [H.filled(k) for k in range(S)]; DL = H.DL
            N0 = [not filled[k] and filled[pi[k]] and filled[pinv[k]] for k in range(S)]
            DD = [DL[k] and DL[pi[k]] for k in range(S)]
            R = [DL[k] and (DD[k] or DD[pinv[k]]) and H.frame(k)[1] == 3 for k in range(S)]
            sig = {k: H.sigma(k) for k in range(S) if R[k]}; img = set(sig.values())
            lm = 0
            for i in H.sp.linki: lm |= 1 << i
            deg = [len(H.rot[x]) for x in H.L]
            for r, s in sig.items():
                if N0[s]: continue
                j = H.frame(r)[0]; k = [(t - j) % 5 for t in range(5) if deg[t] >= 6][0]
                kind = 'fixed' if s == r else 'DL' if DL[s] else 'Lock-only'
                ex = [t for t, p, q, K in H.sp.moves(r) if t != r and not K & lm and N0[t]]
                C[('census' if src == 'census' else 'other', k, kind, 'lockless sigma-prime exit' if ex else 'none', 'outside sigma(R)' if any(t not in img for t in ex) else '-')] += 1
    return C
if __name__ == '__main__':
    T = Counter()
    with Pool(2) as P:
        for C in P.imap_unordered(job, NB.sources()): T.update(C)
    with open(os.path.join(HERE, 'nightbudget3-summary.txt'), 'w') as f:
        for k, v in sorted(T.items(), key=lambda t: str(t[0])): f.write('%7d %s\n' % (v, k))
    print(open(os.path.join(HERE, 'nightbudget3-summary.txt')).read())
