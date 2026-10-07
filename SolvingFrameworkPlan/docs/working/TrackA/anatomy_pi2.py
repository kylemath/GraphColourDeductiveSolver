#!/usr/bin/env python3
"""Track A task 2: pi-orbit pattern of every pi-cycle inside every equality class (both orientations): sequence of
(state type F/L1/L2/DL/N0, lambda) along pi, canonical up to rotation; plus graph dedup by invariant.
Also, from picyc hist (all holes of all graphs): number of (w = 0, L = 4) pi-cycles that sit in holes WITHOUT a 4-state class."""
import sys, json, glob, subprocess, os, tempfile
from collections import Counter
sys.path.insert(0, '/Users/kylemathewson/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/local-runs/27-studio-positive-config/jobuv')
from uv_lib import Hole
from anatomy_pi import ROT
from tracka_lib import rot_line
from holes import PICYC
def typ(H, k):
    if H.filled(k): return 'F'
    l = H.locks(k) if hasattr(H, 'locks') else None
    return l
pats = Counter(); recs = 0
EQ = [json.loads(l) for l in open('anat/anat-pi.jsonl')]
EQ = [r for r in EQ if 4 * r['F'] == r['N']]
done = set()
for r in EQ:
    key = (r['name'], r['hole'], r['mirror'])
    if key in done: continue
    done.add(key)
    H = Hole(r['name'], int(r['hole']), r['mirror'], rot=ROT[r['name']]); sp = H.sp; sp.build_graph(); cl, n = sp.classes()
    from collections import Counter as C2
    sz = C2(cl)
    for c in range(n):
        mem = [k for k in range(H.S) if cl[k] == c]
        if 4 * sum(H.filled(k) for k in mem) != len(mem): continue
        for z in sorted({H.cyc[k] for k in mem}):
            seq = []
            for k in H.cycles[z]:
                if H.filled(k): t = 'F'
                else:
                    lk = H.locks(k); t = {(True, True): 'DL', (True, False): 'L1', (False, True): 'L2', (False, False): 'N0'}[(bool(lk[0]), bool(lk[1]))]
                seq.append('%s%+d' % (t, H.lam[k]))
            L = len(seq); can = min(tuple(seq[i:] + seq[:i]) for i in range(L)); pats[(r['mirror'], can)] += 1; recs += 1
print('pi-cycles in equality classes:', recs)
for k, v in pats.most_common(): print(' mirror=%s' % k[0], ' '.join(k[1]), v)
