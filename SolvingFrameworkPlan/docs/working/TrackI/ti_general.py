#!/usr/bin/env python3
"""Track I: the chain-parity law  N(pi c) - N(c) == [pi c DL] (mod 2)  on TrackH's general-graph LPC counterexamples
(hole = vertex 0).  On a sphere the law is a theorem (Track I Theorem 6); these graphs are not surfaces.
usage: ti_general.py FILE..."""
import sys, os
from collections import Counter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'TrackH'))
from th_engine import Hole
from ti_chains import nchains
for f in sys.argv[1:]:
    for l in open(f):
        p = l.split()
        if len(p) < 3: continue
        rot = [list(map(int, r.split(','))) for r in p[2].split(';')]
        H = Hole(rot, 0).build(); st = Counter()
        cyc = H.allDL_cycles()
        for c in cyc:
            for i in c:
                t = H.info[i]['pi']; d = (nchains(H, H.col(t)) - nchains(H, H.col(i))) % 2
                st[('N', nchains(H, H.col(i)), 'step_parity', d, 'img', H.info[t]['kind'])] += 1
        print(os.path.basename(f), p[0], 'allDL cycles', [len(c) for c in cyc], dict(st))
