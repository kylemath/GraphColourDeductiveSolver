#!/usr/bin/env python3
"""Track S: along all-DL pi-cycles (and R-runs), report per state (P1,P2,P3) chain counts, i.e. k(H), k(F13), k(F12):
#P1 = 1 + k(H), #P2 = 2 + k(F13), #P3 = 2 + k(F12).  Tests whether 'Q_t = F13 connected at every state' can hold on
a sphere cycle (the matching-graph form of NRC).  usage: ts_cyc_q.py GRAPHFILE name:hole ..."""
import sys
from ts_lib import load_graphs, HoleData
G = load_graphs(sys.argv[1], {s.rsplit(':', 1)[0] for s in sys.argv[2:]})
for spec in sys.argv[2:]:
    nm, h = spec.rsplit(':', 1); h = int(h); hd = HoleData(G[nm], h)
    # own all-DL cycle finder
    info = hd.info; on = set()
    for i in range(hd.S):
        if info[i]['kind'] != 'DL' or i in on: continue
        path = []; posd = {}; k = i
        while k is not None and info[k]['kind'] == 'DL' and k not in posd and k not in on:
            posd[k] = len(path); path.append(k); k = info[k]['pi']
        for q in path: on.add(q)
        if k is not None and k in posd:
            c = path[posd[k]:]
            w = []
            for q in c:
                c6 = info[q]['c6']; w.append('%d%d%d' % (c6[0] + c6[1] - 1, c6[2] + c6[3] - 2, c6[4] + c6[5] - 2))
            print(nm, h, 'cycle L=%d' % len(c), 'kH,kF13,kF12:', ' '.join(w),
                  '| all Q conn:', all(x[1] == '1' and x[2] == '1' for x in w), flush=True)
