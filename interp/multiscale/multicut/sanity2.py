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
# (a) c* parallelogram (claims.py (b))
def cstar(x, y): return [(0, 1), (2, 3), (1, 0), (3, 2)][y % 4][x % 2]
rows = []
for m in [4, 8, 16, 32]:
    for w in [2, 3]:
        bd = [(x, 0) for x in range(m)] + [(m, y) for y in range(w)] + [(x, w) for x in range(m, 0, -1)] + [(0, y) for y in range(w, 0, -1)]
        def deg_in(p):
            x, y = p; return sum(1 for (a, b) in [(x+1, y), (x-1, y), (x, y+1), (x, y-1), (x+1, y+1), (x-1, y-1)] if 0 <= a <= m and 0 <= b <= w)
        fl = [(-1 if (deg_in(p)-2) % 2 else 1) for p in bd]; s = [1]
        for i in range(1, len(bd)): s.append(s[-1]*fl[i])
        cols = [cstar(x, y) for (x, y) in bd]; L = len(bd)
        H = mc.int_walk([cols[i] ^ cols[(i+1) % L] for i in range(L)], s)
        r = dict(m=m, w=w, L=L, t=round(abs(mc.cz(H[-1])), 3))
        for J in (1, 2, 3, 4):
            for var in ('nc', 'any'): r['%s%d' % (var, J)] = tv(H, False, J, var)
        rows.append(r); print('cstar', r, flush=True)
out['cstar'] = rows
# (b) smeared slopes: lattice walk tracking p(i) = 2 i / L * e within r0, closing at 2e (t = 2).  signs +1 (labels free)
DIRS = [(1, 0), (0, 1), (-1, -1), (-1, 0), (0, -1), (1, 1)]
def slope_walk(L, r0, rng, tdir=(2, 0)):
    for _ in range(2000):
        H = [(0, 0)]; ok = True
        for i in range(1, L+1):
            tgt = i / L * mc.cz(tdir)
            opts = [(H[-1][0]+d[0], H[-1][1]+d[1]) for d in DIRS]
            opts = [p for p in opts if abs(mc.cz(p) - tgt) <= r0 + 1e-9 and (i < L or p == tdir)]
            if i == L - 1: opts = [p for p in opts if any((p[0]+d[0], p[1]+d[1]) == tdir for d in DIRS)]
            if not opts: ok = False; break
            H.append(rng.choice(opts))
        if ok: return H
    return None
rng = random.Random(3); sl = []
for L in (12, 24, 48, 96, 192):
    for r0 in (0.9, 1.2):
        for rep in range(3):
            H = slope_walk(L, r0, rng)
            if H is None: continue
            Hc = np.array([mc.cz(p) for p in H])
            r = dict(L=L, r0=r0, hodge=round(ld.tau_hodge(Hc), 3), step=round(ld.tau_step_full(Hc)[0], 3))
            for J in (2, 3, 4):
                for var in ('nc', 'any'): r['%s%d' % (var, J)] = tv(H, False, J, var)
            sl.append(r); print('slope', r, flush=True)
out['slopes'] = sl
# (c) t = 0 loosening on random walks: #walks with circumradius > 1 but tau_J <= 1
rng = random.Random(5); cnt = {}; tot = 0
for trial in range(20000):
    L = rng.randrange(6, 40)
    while True:
        col = [rng.randrange(4) for _ in range(L)]
        if all(col[i] != col[(i+1) % L] for i in range(L)): break
    sg = [rng.choice((1, -1)) for _ in range(L)]
    H = mc.int_walk([col[i] ^ col[(i+1) % L] for i in range(L)], sg)
    if H[-1] != (0, 0): continue
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
json.dump(out, open('/mnt/project-files/multiscale/multicut/sanity2.json', 'w'), indent=0)
