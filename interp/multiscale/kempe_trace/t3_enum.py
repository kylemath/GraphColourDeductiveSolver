# How many distinct trace sets can a collar of width w reach (boundary word fixed)?  SAT enumeration with blocking clauses.
import json, sys, time
sys.path.insert(0, '/mnt/project-files/multiscale/kempe_trace'); sys.path.insert(0, '/mnt/project-files/multiscale/opus_attack/bandfill')
from kt import *; from collar import Collar; from t2_tubes import annulus
from pysat.solvers import Cadical153
CAP = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
def enum(adj, S, col, bd, w, cap=CAP):
    C = Collar(adj, S, col, bd, w); L = len(bd)
    s = Cadical153(bootstrap_with=C.cls); sigs = {}; ncol = 0; t0 = time.time()
    while ncol < cap and s.solve():
        mod = set(l for l in s.get_model() if l > 0); ncol += 1
        c2 = dict(C.col); lits = []
        for v in C.free:
            c = next(c for c in range(4) if C.xv[v, c] in mod); c2[v] = c; lits.append(-C.xv[v, c])
        s.add_clause(lits)
        tr = traces(adj, S, c2, bd); key = str(sorted(tr.items())); sm = summary(tr, L)
        if key not in sigs: sigs[key] = dict(count=0, nsingle=sm['nsingle'], depth=sm['depth'], maxspan=sm['maxspan'])
        sigs[key]['count'] += 1
    s.delete()
    base = str(sorted(traces(adj, S, col, bd).items()))
    return dict(w=w, nfree=len(C.free), ncolourings=ncol, exhausted=ncol < cap, ndistinct=len(sigs), base_present=base in sigs,
                singles=sorted(set(v['nsingle'] for v in sigs.values())), depths=sorted(set(v['depth'] for v in sigs.values())),
                spans=sorted(set(v['maxspan'] for v in sigs.values())), sec=round(time.time()-t0, 1))
d = json.load(open('/mnt/project-files/multiscale/opus_attack/bandfill/sphere_L18_w4.json'))
adj = [set(a) for a in d['adj']]; L = 18; n = len(adj); A = set(d['A']); B = set(range(n)) - A; m = d['seam_row_A']
colA = {int(k): v for k, v in d['colA'].items()}; colB = {int(k): v for k, v in d['colB'].items()}
bdA = [m*L + i for i in range(L)]; bdB = [(m+1)*L + i for i in range(L)]
out = []
for nm, S, c, bd in (('A', A, colA, bdA), ('B', B, colB, bdB)):
    for w in (2, 3, 4):
        r = enum(adj, S, c, bd, w); r['case'] = 'opus_' + nm; print(r, flush=True); out.append(r)
        json.dump(out, open('t3_enum.json', 'w'), indent=1)
# random easy sides from t2 (same sphere) for comparison, if available
try:
    t2 = json.load(open('t2_tubes.json'))
    for rec in t2['sphere_random'][:3]:
        cA = {int(k): v for k, v in rec['colA'].items()}
        for w in (2, 3):
            r = enum(adj, A, cA, bdA, w); r['case'] = f"easy_trial{rec['trial']}_A"; print(r, flush=True); out.append(r)
    json.dump(out, open('t3_enum.json', 'w'), indent=1)
except Exception as ex: print('no t2 yet', ex)
