#!/usr/bin/env python3
"""Track S: independent check (TrackJ C engine tj_eng, read-only) of the sphere Q-cycle at C30#0:
all-DL pi-cycles at the hole with (#aA,#mB) = (2,1) and (#aB,#mA) = (2,1) at every state.  usage: ts_qcheck_c.py GRAPHFILE name:hole"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'TrackJ'))
from tj_lib import Engine
G = {l.split()[0]: l for l in open(sys.argv[1]) if len(l.split()) >= 3}
for spec in sys.argv[2:]:
    nm, h = spec.rsplit(':', 1); h = int(h)
    E = Engine(dump=True, hole=h); js, S = E.run(G[nm])[0]; E.close()
    on = set()
    for s in S:
        if s['kind'] != 1 or s['i'] in on: continue
        path = []; pos = {}; k = s['i']
        while k >= 0 and S[k]['kind'] == 1 and k not in pos and k not in on:
            pos[k] = len(path); path.append(k); k = S[k]['pi']
        on.update(path)
        if k >= 0 and k in pos:
            c = path[pos[k]:]
            q = all(S[x]['c6'][2] == 2 and S[x]['c6'][3] == 1 and S[x]['c6'][4] == 2 and S[x]['c6'][5] == 1 for x in c)
            print(nm, h, 'cycle L', len(c), 'N', [S[x]['N'] for x in c], 'P2,P3 minimal at all states:', q)
