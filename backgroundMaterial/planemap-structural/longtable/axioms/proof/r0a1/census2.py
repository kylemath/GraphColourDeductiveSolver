"""Planar census with the fast generator.  usage: census2.py n  -> out/census_n{n}_p.jsonl
Per class: #PM, #arcs of D, #Ham arcs, sizes of cyclic SCCs, #Ham arcs inside an SCC (R0 violations)."""
import sys, json, time
from r0lib import planar_normal_forms, IsoBucket, analyse
n = int(sys.argv[1])
t0 = time.time()
B = IsoBucket(); nd = 0
for g, pm, vch in planar_normal_forms(n):
    nd += 1; B.add(g)
reps = B.reps()
print(f'n={n}: planar chord diagrams {nd}, classes {len(reps)} ({time.time()-t0:.1f}s)', flush=True)
tot = dict(n=n, diagrams=nd, classes=len(reps), bad=0, withcyc=0, maxscc=0)
with open(f'out/census_n{n}_p.jsonl', 'w') as f:
    for g in reps:
        A = analyse(g)
        rec = dict(n=n, edges=g.E, fv=g.fv, npm=len(A['P']), narcs=len(A['arcs']), nham=len(A['ham']),
                   cyc=sorted(len(c) for c in A['cyc']), bad=len(A['bad']))
        f.write(json.dumps(rec) + '\n')
        tot['bad'] += rec['bad'] > 0; tot['withcyc'] += bool(A['cyc'])
        tot['maxscc'] = max([tot['maxscc']] + rec['cyc'])
print(json.dumps(tot), f'({time.time()-t0:.1f}s)', flush=True)
