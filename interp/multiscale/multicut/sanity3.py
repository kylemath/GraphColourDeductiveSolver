# Part 2: (a) c* parallelogram discs (t = 0), (b) smeared slopes (t = 2 spread over L), (c) t = 0 loosening vs circumradius
#         (random t = 0 walks, Opus bandfill t = 0 rows), (d) odd J = 2 vs twocut.py on the localdetrend odd failures.
import sys, random, math, json, itertools, glob, pickle, numpy as np
sys.path.insert(0, '/mnt/project-files/multiscale/multicut/'); sys.path.insert(0, '/mnt/project-files/multiscale/localdetrend/'); sys.path.insert(0, '/mnt/project-files/multiscale/canonical/')
import mc, ld
from pi import make, signs
out = {}
def lab_sg_to_H(lab, sg): return mc.int_walk(lab, sg)
def tv(H, odd, J, var):
    v = mc.tau_value(H, odd, J, var, hi=2.5, tol=2e-3); return ">2.5" if v == float("inf") else round(v, 3)
# (c) t = 0 loosening on random walks: #walks with circumradius > 1 but tau_J <= 1
rng = random.Random(5); cnt = {}; tot = 0
for trial in range(4000):
    L = rng.randrange(6, 40)
    D6 = [(1, 0), (0, 1), (-1, -1), (-1, 0), (0, -1), (1, 1)]
    H = [(0, 0)]
    for i in range(L - 2):
        d = rng.choice(D6); H.append((H[-1][0] + d[0], H[-1][1] + d[1]))
    clos = None
    for a in D6:
        for b in D6:
            if (H[-1][0]+a[0]+b[0], H[-1][1]+a[1]+b[1]) == (0, 0): clos = a
    if clos is None: continue
    H.append((H[-1][0]+clos[0], H[-1][1]+clos[1])); H.append((0, 0))
    if mc.ncuts(H, False, 1) is not None: continue           # circumradius <= 1 already
    if mc.ncuts(H, False, 4, 'any') is None and mc.ncuts(H, False, 4, 'nc') is None: tot += 1; continue
    tot += 1
    for J in (2, 3, 4):
        for var in ('nc', 'any'):
            if mc.ncuts(H, False, J, var) is not None: cnt['%s%d' % (var, J)] = cnt.get('%s%d' % (var, J), 0) + 1
out['t0_random'] = dict(rejected_by_circumradius=tot, accepted=cnt); print('t0 random', out['t0_random'], flush=True)
B = '/mnt/project-files/multiscale/opus_attack/bandfill/'; orows = []
for c in json.load(open(B+'counterexamples.json')):
    for nm, r in (('A', c['A_rows_depth_w_to_seam'][-1]), ('B', c['B_rows_seam_to_depth_w'][0])): orows.append((c['L'], nm, [int(x) for x in r]))
d = json.load(open(B+'sphere_L18_w4.json'))
for nm, r in (('A', d['A_rows_bottom_to_seam'][-1]), ('B', d['B_rows_seam_to_top'][0])): orows.append((18, 'sphere_'+nm, [int(x) for x in r]))
op = []
for L, nm, r in orows:
    H = mc.int_walk([r[i] ^ r[(i+1) % L] for i in range(L)], [1]*L); t = abs(mc.cz(H[-1]))
    rr = dict(L=L, side=nm, t=round(t, 3))
    for J in (1, 2, 3, 4):
        for var in ('nc', 'any'): rr['%s%d' % (var, J)] = tv(H, False, J, var)
    op.append(rr); print('opus', rr, flush=True)
out['opus'] = op
# (d) odd J = 2 on the localdetrend odd failures (twocut.py: 1.0 / 1.0 / 0.87 at R <= 1)
dd = []
for fn in sorted(glob.glob('/mnt/project-files/multiscale/localdetrend/fail_*keep.pkl')):
    D = pickle.load(open(fn, 'rb')); fl = D['fail']
    if fl is None: continue
    adj = make(D['job'][0]); B2 = fl['B']; s = [int(x) for x in fl['s']]; v = fl['v']; P = fl['P']; col = dict(fl['col']); present = set(col) | {v}
    res = dict(f=fn.split('/')[-1], odd=fl['odd'], nodd=fl['nodd'], L=len(B2))
    for R in (0, 1):
        FB = [v] if R == 0 else [v, P[0], P[-1]]; best = {}
        for cs in itertools.product(range(4), repeat=len(FB)):
            c2 = dict(col); c2.update(dict(zip(FB, cs)))
            if any(c2[x] == c2[y] for x in FB for y in adj[x] if y in present and y in c2): continue
            L = len(B2); lab = [c2[B2[i]] ^ c2[B2[(i+1) % L]] for i in range(L)]
            if 0 in lab: continue
            H = mc.int_walk(lab, s)
            if not fl['odd'] and abs(mc.cz(H[-1])) > 2 + 1e-9: continue
            for J in (1, 2, 3):
                v_ = tv(H, fl['odd'], J, 'nc'); best[J] = min(best.get(J, 99), 99 if isinstance(v_, str) else v_)
        res['R%d' % R] = best
    dd.append(res); print('fail', res, flush=True)
out['fails'] = dd
json.dump(out, open('/mnt/project-files/multiscale/multicut/sanity3.json', 'w'), indent=0)
