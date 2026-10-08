#!/usr/bin/env python3
"""Track I: along every all-DL pi-cycle at the TrackH test-bed holes: the chain count N(c) of each state (in pi order),
whether the state has a Kempe move leaving DL ('x'), and the chain-parity law at each step.
usage: ti_cycleN.py TESTBEDS.txt TESTBEDS.jsonl"""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'TrackH'))
from th_engine import Hole
from ti_chains import nchains
G = {}
for l in open(sys.argv[1]):
    p = l.split()
    if len(p) >= 3: G[p[0]] = [list(map(int, r.split(','))) for r in p[2].split(';')]
for l in open(sys.argv[2]):
    d = json.loads(l)
    if d['name'] not in G: continue
    H = Hole(G[d['name']], d['hole']).build()
    for cyc in H.allDL_cycles():
        Ns = [nchains(H, H.col(i)) for i in cyc]
        ex = ['x' if any(H.info[m[4]]['kind'] != 'DL' for m in H.moves[i]) else '.' for i in cyc]
        law = all(((Ns[(t + 1) % len(cyc)] - Ns[t]) % 2 == 1) for t in range(len(cyc)))
        print(d['surface'], d['name'], 'h', d['hole'], 'len', len(cyc), 'N:', ' '.join(map(str, Ns)), '| exits:', ''.join(ex),
              '| law(alternation) holds' if law else '| law FAILS', flush=True)
