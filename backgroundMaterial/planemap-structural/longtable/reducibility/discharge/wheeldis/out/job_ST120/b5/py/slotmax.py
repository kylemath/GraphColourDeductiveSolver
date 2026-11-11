#!/usr/bin/env python3
"""ST-120 B5 M5 probe: max number of possible fits into u at a hub w_i (letter L, anchor L-2) when every slot the
view reads is an independent letter (u = 9, ring-3 slots OPEN). A relaxation of spec §8.4's c+."""
import os, sys, itertools
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(H, '..', '..', '..', 'job_RSST1SHOT', 'code'))
import rcore as R
if len(sys.argv) > 1:                       # optional parts file (parts71.txt format), e.g. cert/parts79.txt
    sys.path.insert(0, H); import export_cert as E; R.PARTS[:] = E.load_parts_file(sys.argv[1])
FULL = R.FULL
def ring3_hat(n, t): return 3 <= t <= n - 2
def ring3_fan(n, t): return 2 <= t <= n - 2
for L in (5, 6, 7, 8):
    parts = [p for tag, p in R.PARTS if len(p) == L]
    n = L
    # per part: list of (slot, (lo,hi)) conditions or None if impossible
    conds = []
    for p in parts:
        cs = []; ok = True
        for j in range(n):
            t = (n - 2 + j) % n
            sp, hat, fans = p[j]
            if sp != FULL:
                if t == 0:
                    if not (sp[0] <= 9 <= sp[1]): ok = False
                else: cs.append((('s', t), sp))
            if hat != FULL and not ring3_hat(n, t): cs.append((('h', t), hat))
            if any(f != FULL for f in fans):
                if t == 0: ok = False if not (sp[0] <= 9 <= sp[1]) else ok
                elif not ring3_fan(n, t):
                    for k, f in enumerate(fans):
                        if f != FULL: cs.append((('f', t, k), f))
        if ok: conds.append(cs)
    slots = sorted(set(s for cs in conds for s, _ in cs))
    best = [0, None]
    def rec(k, asg, alive):
        ub = sum(alive)
        if ub <= best[0]: return
        if k == len(slots):
            best[0] = ub; best[1] = dict(asg); return
        s = slots[k]
        for v in (5, 6, 7, 8, 9):
            asg[s] = v
            al = list(alive)
            for q, cs in enumerate(conds):
                if al[q] and any(sl == s and not (r[0] <= v <= r[1]) for sl, r in cs): al[q] = False
            rec(k + 1, asg, al)
        del asg[s]
    rec(0, {}, [True] * len(conds))
    print('hub', L, 'parts', len(parts), 'candidates', len(conds), 'slots', len(slots), 'max possible', best[0], best[1])
