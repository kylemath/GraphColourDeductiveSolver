"""How do maximal A5v runs end?  For the first state beyond each end (successor of the last state,
predecessor of the first), classify E - M: number of components; if connected, the pairing of v's four
Q-edges into loops (relative to that state's frame k) and the loop parities.  endmech.py prefix"""
import sys, json, gzip
from collections import Counter
from ax_lib import G5, parse_line
from feat import succ, pred, a5bit
pref = sys.argv[1]
runs = json.load(gzip.open(pref + '_runs.json.gz', 'rt'))
def classify(g, M):
    S = set(range(g.m)) - set(M); c = g.ncomp(S)
    k = g.kidx(M)
    if c > 1: return f'Q disconnected ({c} comps)'
    L = g.loops(M)
    pairs = sorted(tuple(sorted(((s0 - k) % 5, (s1 - k) % 5))) for (s0, s1, verts, edges) in L)
    par = [len(verts) % 2 for (s0, s1, verts, edges) in sorted(L, key=lambda x: min((x[0]-k)%5, (x[1]-k)%5))]
    if pairs == [(1, 4), (2, 3)]:
        return 'DL pairing, wrong parity' if g.dl(M) is None else 'DL-good'
    return f'pairing {pairs}'
for kind in ('a5', 'free'):
    C = Counter(); CL = Counter()
    for r in runs:
        if r['kind'] != kind or r['closed']: continue
        g = G5(*parse_line(r['line'])); Ms = [frozenset(m) for m in r['M']]
        for side, M, reason in (('end', succ(g, Ms[-1]), r['end']), ('start', pred(g, Ms[0]), r['start'])):
            if reason == 'notDL':
                c = classify(g, M); C[(side, c)] += 1
                if len(Ms) >= 7: CL[(side, c)] += 1
            else:
                C[(side, reason)] += 1
                if len(Ms) >= 7: CL[(side, reason)] += 1
    print(kind, 'all runs:'); [print('   ', k, v) for k, v in sorted(C.items())]
    print(kind, 'runs of length >= 7:'); [print('   ', k, v) for k, v in sorted(CL.items())]
