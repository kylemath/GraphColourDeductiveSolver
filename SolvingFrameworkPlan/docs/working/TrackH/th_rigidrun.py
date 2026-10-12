#!/usr/bin/env python3
"""Track H: along pi, how long can runs of RIGID DL states be on a triangulated surface?
(Rigid = pair-graph component counts (1,1,2,1,2,1); a class made only of rigid states is a single all-DL pi-cycle with
no filled state -- the shape of both general-graph LPC counterexamples.)  For every degree-5 hole of every STRIDE-th
graph: the pi-successor type of each rigid state (rigid / DL non-rigid / single-lock / lockless) and the longest run of
consecutive rigid states along pi.
usage: th_rigidrun.py GRAPHFILE MAXGRAPHS STRIDE OUT.jsonl"""
import sys, json
from collections import Counter
from th_engine import Hole
from th_rigidscan_lib import counts

gf, maxg, stride, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
fo = open(out, 'a'); k = 0
for ln, l in enumerate(open(gf)):
    if ln % stride: continue
    p = l.split()
    if len(p) < 3: continue
    rot = [list(map(int, r.split(','))) for r in p[2].split(';')]
    k += 1
    if k > maxg: break
    for h in [v for v in range(len(rot)) if len(rot[v]) == 5]:
        H = Hole(rot, h); S = len(H.states); info = [None] * S; rig = [False] * S
        for i in range(S):
            r, col = H.analyse_state(i); info[i] = r
            if r['kind'] == 'DL': rig[i] = counts(H, col, r['roles']) == [1, 1, 2, 1, 2, 1]
        nxt = Counter(); longest = 0
        for i in range(S):
            if not rig[i]: continue
            t = info[i]['pi']
            nxt['rigid' if t is not None and rig[t] else (info[t]['kind'] if t is not None else 'undef')] += 1
            L = 0; s = i; seen = set()
            while s is not None and rig[s] and s not in seen and L < S:
                seen.add(s); L += 1; s = info[s]['pi']
            longest = max(longest, L)
        fo.write(json.dumps(dict(graph=p[0], hole=h, rigid=sum(rig), next=dict(nxt), longest=longest)) + '\n'); fo.flush()
