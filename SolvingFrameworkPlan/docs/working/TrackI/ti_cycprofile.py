#!/usr/bin/env python3
"""Track I: profile of every all-DL pi-cycle at every degree-5 hole: N along the cycle (pi order), exits ('x' = the state
has a Kempe move to a non-DL state), the chain-parity alternation, and exits at the near-rigid states (N <= 9).
usage: ti_cycprofile.py GRAPHFILE STRIDE MAXGRAPHS [prefix]"""
import sys, os
from collections import Counter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'TrackH'))
from th_engine import Hole
from ti_chains import nchains
gf, stride, maxg = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]); filt = sys.argv[4] if len(sys.argv) > 4 else ''
st = Counter(); k = 0
for ln, l in enumerate(open(gf)):
    if ln % stride: continue
    p = l.split()
    if len(p) < 3 or not p[0].startswith(filt): continue
    rot = [list(map(int, r.split(','))) for r in p[2].split(';')]; k += 1
    if k > maxg: break
    for h in [v for v in range(len(rot)) if len(rot[v]) == 5]:
        H = Hole(rot, h).build()
        for cyc in H.allDL_cycles():
            Ns = [nchains(H, H.col(i)) for i in cyc]
            ex = ['x' if any(H.info[m[4]]['kind'] != 'DL' for m in H.moves[i]) else '.' for i in cyc]
            alt = all((Ns[(t + 1) % len(cyc)] - Ns[t]) % 2 == 1 for t in range(len(cyc)))
            st['cycles'] += 1; st['alternating'] += alt
            for n, e in zip(Ns, ex):
                st[('N<=9' if n <= 9 else 'N>=10', 'exit' if e == 'x' else 'noexit')] += 1
            print(p[0], 'h', h, 'len', len(cyc), 'N', ' '.join(map(str, Ns)), '|', ''.join(ex), flush=True)
print('SUMMARY', gf, filt, dict(sorted(st.items(), key=str)), flush=True)
