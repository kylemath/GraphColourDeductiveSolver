#!/usr/bin/env python3
"""Track J: print the longest pi-runs inside R = {DL, N <= 9} at given holes: N along the run extended by 3 states on each
side, extra-chain pairs at N = 9 states, and where the run ends (state kind / N of the next pi-image).
usage: tj_runs.py GRAPHFILE name:hole [name:hole ...]"""
import sys
from tj_lib import Engine, read_graphs, ROLE, RIGID
G = {nm: line for nm, line, rot in read_graphs(sys.argv[1])}
for spec in sys.argv[2:]:
    nm, h = spec.rsplit(':', 1); h = int(h)
    E = Engine(dump=True, hole=h); js, S = E.run(G[nm])[0]; E.close()
    R = {s['i'] for s in S if s['kind'] == 1 and s['N'] <= 9}
    pre = {s['pi']: s['i'] for s in S if s['kind'] == 1 and s['pi'] >= 0}
    best = []
    for i in R:
        if pre.get(i) in R: continue
        run = [i]; x = S[i]['pi']
        while x in R and x != i: run.append(x); x = S[x]['pi']
        if len(run) > len(best): best = run
    def lab(x):
        s = S[x]
        if s['kind'] != 1: return 'FDSZ'[s['kind']]
        ex = [ROLE[r] for r in range(6) if s['c6'][r] > RIGID[r]]
        return '%d%s' % (s['N'], ('(' + ','.join(ex) + ')') if s['N'] == 9 else '')
    after = S[best[-1]]['pi']; before = pre.get(best[0])
    print(nm, 'h', h, 'run', len(best), ':', ('[' + lab(before) + '] ') if before is not None else '[start] ', ' '.join(lab(x) for x in best), ' [' + (lab(after) if after >= 0 else 'undef') + ']')
