"""Census of R0 at small n: all (G, rotation) classes with a Hamiltonian cycle through two non-adjacent
v-edges (normal form), with the PM digraph analysis.  usage: census.py n [nonplanar]"""
import sys, json, time
from r0lib import normal_form_graphs, IsoBucket, analyse
n = int(sys.argv[1]); planar = 'nonplanar' not in sys.argv
t0 = time.time()
B = IsoBucket(); ndiag = 0
for g, pm, vch in normal_form_graphs(n, planar=planar):
    ndiag += 1
    if not planar and g.planar_rot(): continue
    B.add(g)
reps = B.reps()
print(f'n={n} planar={planar}: chord diagrams {ndiag}, classes {len(reps)} ({time.time()-t0:.1f}s)', flush=True)
tot = dict(classes=len(reps), bad=0, withcyc=0)
out = []
for g in reps:
    if planar: assert g.planar_rot()
    A = analyse(g)
    rec = dict(n=n, edges=g.E, fv=g.fv, npm=len(A['P']), narcs=len(A['arcs']), nham=len(A['ham']),
               cyc_scc_sizes=sorted(len(c) for c in A['cyc']), bad=len(A['bad']))
    out.append(rec)
    tot['bad'] += rec['bad'] > 0; tot['withcyc'] += bool(A['cyc'])
print(json.dumps(tot), f'({time.time()-t0:.1f}s)')
with open(f'out/census_n{n}_{"p" if planar else "np"}.jsonl', 'w') as f:
    for r in out: f.write(json.dumps(r) + '\n')
