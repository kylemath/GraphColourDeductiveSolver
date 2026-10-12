#!/usr/bin/env python3
"""Track S: Tait words (kH kF13 kF12, dual components on the surface) of all all-DL pi-cycles at given holes.
usage: ts_tait_holes.py GRAPHFILE name:hole ..."""
import sys, json
from ts_lib import load_graphs, HoleData
from tl_lib import TaitState
from ts_qcyc import cycles
G = load_graphs(sys.argv[1], {s.rsplit(':', 1)[0] for s in sys.argv[2:]})
for spec in sys.argv[2:]:
    nm, h = spec.rsplit(':', 1); h = int(h); hd = HoleData(G[nm], h)
    for c in cycles(hd):
        ks = []
        for q in c:
            St = TaitState(hd, q); T = St.T; ks.append('%d%d%d' % (T.ncomp(St.H), T.ncomp(St.F13), T.ncomp(St.F12)))
        isq = all(x[1] == '1' for x in ks)
        print(json.dumps(dict(g=nm, h=h, L=len(c), chainQ=all(hd.info[q]['c6'][2] + hd.info[q]['c6'][3] == 3 for q in c),
                              taitQ=isq, rigid=isq and '111' in ks, word=' '.join(ks), N=[hd.info[q]['N'] for q in c])), flush=True)
