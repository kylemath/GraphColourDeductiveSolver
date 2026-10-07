#!/usr/bin/env python3
"""Track F: re-run the LPC census holes that have a targetless class of size >= MINSIZE with the independent Python
engine (lpc_detail.py), compare the full class list with kclass2's census record, and collect the pi-orbit structure
of every targetless class (paths / cycles; check violators == ends of non-cyclic pi-orbits).
usage: lpc_pi.py SURFACE MINSIZE OUT.jsonl   (reads out/lpc/census_SURFACE.{jsonl,graphs.txt})"""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
import lpc_detail
K = 'cls[size,filled,DL,unfilledNonDL,minKdeg,maxKdeg,lockParityViolations]'
surf, mins, outp = sys.argv[1], int(sys.argv[2]), sys.argv[3]
base = os.path.join(os.path.dirname(__file__), '..', 'out', 'lpc', 'census_' + surf)
G = {}
for l in open(base + '.graphs.txt'):
    p = l.split(); G[p[0]] = [list(map(int, r.split(','))) for r in p[2].split(';')]
fo = open(outp, 'w'); agg = dict(surface=surf, holes=0, mismatch=0, pid_bad=0, tl=0, ends_ne_viol=0, tl_with_cycle=0, maxpath=0, maxcycle=0)
for l in open(base + '.jsonl'):
    d = json.loads(l)
    if not any(c[1] == 0 and c[0] >= mins for c in d[K]): continue
    res, _ = lpc_detail.analyse(G[d['graph']], d['hole'], False)
    agg['holes'] += 1
    if sorted(map(list, d[K])) != res['cls'] or d['states'] != res['states']: agg['mismatch'] += 1
    agg['pid_bad'] += sum(res['pid_bad'])
    for q in res['pi']:
        agg['tl'] += 1; agg['ends_ne_viol'] += not q['ends_eq_viol']; agg['tl_with_cycle'] += bool(q['cycles'])
        agg['maxpath'] = max([agg['maxpath']] + q['paths']); agg['maxcycle'] = max([agg['maxcycle']] + q['cycles'])
    fo.write(json.dumps(dict(graph=d['graph'], hole=d['hole'], pi=res['pi'])) + '\n'); fo.flush()
print(json.dumps(agg), flush=True)
