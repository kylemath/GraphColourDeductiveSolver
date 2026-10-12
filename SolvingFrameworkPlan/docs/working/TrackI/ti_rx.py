#!/usr/bin/env python3
"""Track I: candidate next target RX ('no all-DL pi-cycle contains a rigid state', sphere) and the N-profile of all-DL
pi-cycles.  For every degree-5 hole: all-DL pi-cycles (TrackH engine), the chain counts N along them, the number of
rigid (N=8) states on them, and the minimum N on each cycle.  Also: for every rigid DL state, the length of the DL run
pi(c), pi^2(c), ... before the first non-DL state (or 'cycle').
usage: ti_rx.py GRAPHFILE STRIDE MAXGRAPHS [prefix]"""
import sys, os
from collections import Counter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'TrackH'))
from th_engine import Hole
from ti_chains import nchains
gf, stride, maxg = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]); filt = sys.argv[4] if len(sys.argv) > 4 else ''
st = Counter(); runs = Counter(); k = 0; minN = Counter()
for ln, l in enumerate(open(gf)):
    if ln % stride: continue
    p = l.split()
    if len(p) < 3 or not p[0].startswith(filt): continue
    rot = [list(map(int, r.split(','))) for r in p[2].split(';')]; k += 1
    if k > maxg: break
    for h in [v for v in range(len(rot)) if len(rot[v]) == 5]:
        H = Hole(rot, h); S = len(H.states); info = []; N = []
        for i in range(S):
            r, col = H.analyse_state(i); info.append(r); N.append(nchains(H, col) if r['kind'] == 'DL' else None)
        H.info = info
        for cyc in H.allDL_cycles():
            st['cycles'] += 1; st['cycle_states'] += len(cyc)
            st['rigid_on_cycles'] += sum(1 for i in cyc if N[i] == 8)
            minN[min(N[i] for i in cyc)] += 1
        for i in range(S):
            if N[i] != 8: continue
            L = 0; s = info[i]['pi']; seen = {i}
            while s is not None and info[s]['kind'] == 'DL' and s not in seen:
                seen.add(s); L += 1; s = info[s]['pi']
            runs['cycle' if (s in seen) else L] += 1
print(gf, filt, 'graphs', min(k, maxg), dict(st), 'minN per cycle', dict(sorted(minN.items())),
      'rigid: #DL states after it before exit', dict(sorted(runs.items(), key=str)), flush=True)
