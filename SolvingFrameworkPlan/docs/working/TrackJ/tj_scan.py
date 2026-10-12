#!/usr/bin/env python3
"""Track J task 3 [data]: census-wide near-rigid statistics with the C engine (no dump).
Per hole the engine reports R = #{DL states with N <= 9}, Rrun = longest pi-run inside R, Rcyc = a pi-cycle inside R,
inshape = #N = 9 DL states with pi and pi^-1 rigid, inshape_sigma_closed = #in-shape states whose P1 link-free swap
partner is in-shape, plus the near-rigid class test (a class all of whose states are on all-DL cycles with N <= 9).
usage: tj_scan.py OUT.jsonl FILE [FILE...]   (keeps only notable holes: Rrun >= 4, Rcyc, inshape_sigma_closed > 0)
"""
import sys, json, subprocess, os
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
out = open(sys.argv[1], 'w'); T = Counter(); top = []
for f in sys.argv[2:]:
    p = subprocess.Popen([os.path.join(HERE, 'tj_eng'), '--allholes'], stdin=open(f), stdout=subprocess.PIPE, text=True)
    for l in p.stdout:
        d = json.loads(l)
        if 'err' in d: T['err'] += 1; continue
        T['holes'] += 1; T['R'] += d['R']; T['inshape'] += d['inshape']; T['inshape_sigma_closed'] += d['inshape_sigma_closed']; T['inshape_extraAB'] += d.get('inshape_extraAB', 0); T['inshape_extraP23'] += d.get('inshape_extraP23', 0)
        T['Rrun_%d' % d['Rrun']] += 1; T['Rcyc'] += d['Rcyc']; T['allDLcyc'] += d['ncyc']
        nr = [c for c in d['cls'] if c[0] == c[3] and c[6] == 0]
        T['near_rigid_closed_class'] += len(nr)
        if d['Rrun'] >= 4 or d['Rcyc'] or d['inshape_sigma_closed'] or nr:
            out.write(json.dumps(dict((k, d[k]) for k in ('name', 'hole', 'states', 'R', 'Rrun', 'Rcyc', 'inshape', 'inshape_sigma_closed', 'ncyc'))) + '\n'); out.flush()
    p.wait()
    print('FILE', f, dict(sorted(T.items())), flush=True)
print('SUMMARY', dict(sorted(T.items())), flush=True)
