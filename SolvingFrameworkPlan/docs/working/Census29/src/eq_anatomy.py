#!/usr/bin/env python3
"""Census29: anatomy of quarter-floor equality classes with N > 8 (engine 2 = uv_lib.Hole: kempe_py + escape.pi_of, independent of picyc).
For each (graph, hole): the classes of size <= 64, their pi-cycles (L, w) and the state-type word along each cycle
(F = filled with its pi kind, D = DL, 1 = Lock1 only, 2 = Lock2 only, 0 = no lock).  usage: eq_anatomy.py FILE graph:hole ..."""
import sys, os
from collections import Counter
sys.path.insert(0, '/Users/kylemathewson/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/local-runs/27-studio-positive-config/jobuv')
from uv_lib import Hole
R = {l.split()[0]: [list(map(int, x.split(','))) for x in l.split()[2].split(';')] for l in open(sys.argv[1])}
for a in sys.argv[2:]:
    name, h = a.rsplit(':', 1)
    for mirror in (False, True):
        H = Hole(name, int(h), mirror, rot=R[name]); sp = H.sp; sp.build_graph(); cl, n = sp.classes(); size = Counter(cl)
        for c in range(n):
            if size[c] > 64: continue
            mem = [k for k in range(H.S) if cl[k] == c]; F = sum(H.filled(k) for k in mem)
            print('%s hole %s %s class N=%d F=%d' % (name, h, 'mirror' if mirror else 'plantri', size[c], F))
            for z in sorted({H.cyc[k] for k in mem}):
                cy = H.cycles[z]; t = ''
                for k in cy:
                    if H.filled(k): t += 'F(%s)' % H.kind[k]
                    else: l1, l2 = H.locks(k); t += 'D' if l1 and l2 else ('1' if l1 else ('2' if l2 else '0'))
                    t += ' '
                print('   pi-cycle L=%d w=%d lambda=%s : %s' % (len(cy), H.W[z], [H.lam[k] for k in cy], t))
