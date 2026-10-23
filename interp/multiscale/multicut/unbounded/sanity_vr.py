# Sanity (4): the vortex-restricted invariant allows at most nodd(enclosed) cut positions (creation only at vortex
# steps, <= dn each; reassignment/merging never adds), so on a closed walk it implies tau_{J = nodd} <= 1 with cuts
# anywhere.  Here: the minimum number of cuts K_min (uncapped, cuts anywhere) for the c* strips and smeared t = 2
# slopes of ../sanity2.py.  A walk is rejected by the vortex-restricted invariant whenever nodd < K_min.
import sys, random, math, json
sys.path.insert(0, '/mnt/project-files/multiscale/multicut/unbounded/')
import vr, mc          # vr patches mc.Frontier (uncapped, NB = BIG)
BIG = vr.BIG
def kmin(H, odd, var):
    vr.FrontierVR.NB = BIG; return mc.ncuts(H, odd, BIG, var)
def cstar(x, y): return [(0, 1), (2, 3), (1, 0), (3, 2)][y % 4][x % 2]
out = {'cstar': [], 'slopes': []}
for m in [4, 8, 16, 32]:
    for w in [2, 3]:
        bd = [(x, 0) for x in range(m)] + [(m, y) for y in range(w)] + [(x, w) for x in range(m, 0, -1)] + [(0, y) for y in range(w, 0, -1)]
        def deg_in(p):
            x, y = p; return sum(1 for (a, b) in [(x+1, y), (x-1, y), (x, y+1), (x, y-1), (x+1, y+1), (x-1, y-1)] if 0 <= a <= m and 0 <= b <= w)
        fl = [(-1 if (deg_in(p)-2) % 2 else 1) for p in bd]; s = [1]
        for i in range(1, len(bd)): s.append(s[-1]*fl[i])
        cols = [cstar(x, y) for (x, y) in bd]; L = len(bd)
        H = mc.int_walk([cols[i] ^ cols[(i+1) % L] for i in range(L)], s)
        r = dict(m=m, w=w, L=L, t=round(abs(mc.cz(H[-1])), 3), nodd_enclosed=0, Kmin_nc=kmin(H, False, 'nc'), Kmin_any=kmin(H, False, 'any'))
        out['cstar'].append(r); print('cstar', r, flush=True)
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
rng = random.Random(3)
for L in (12, 24, 48, 96, 192):
    for r0 in (0.9, 1.2):
        for rep in range(3):
            H = slope_walk(L, r0, rng)
            if H is None: continue
            r = dict(L=L, r0=r0, Kmin_nc=kmin(H, False, 'nc'), Kmin_any=kmin(H, False, 'any'))
            out['slopes'].append(r); print('slope', r, flush=True)
# vacuity of the UNRESTRICTED uncapped measure: fraction of random lattice closed walks (t = 0) and t = 2 walks of
# radius up to 6 accepted with cuts anywhere and no cap
rng = random.Random(7); acc = {'nc': 0, 'any': 0}; tot = 0; ks = {'nc': [], 'any': []}
for trial in range(300):
    L = rng.randrange(20, 80); H = [(0, 0)]
    for i in range(L - 2): d = rng.choice(DIRS); H.append((H[-1][0]+d[0], H[-1][1]+d[1]))
    # close greedily back to 0
    while H[-1] != (0, 0):
        best = min(DIRS, key=lambda d: abs(mc.cz((H[-1][0]+d[0], H[-1][1]+d[1]))))
        H.append((H[-1][0]+best[0], H[-1][1]+best[1]))
    if mc.ncuts(H, False, 1) is not None: continue
    tot += 1
    for var in ('nc', 'any'):
        k = kmin(H, False, var)
        if k is not None: acc[var] += 1; ks[var].append(k)
out['random_t0'] = dict(walks_circumradius_gt1=tot, accepted_uncapped_anywhere=acc, Kmin_max={v: max(ks[v], default=None) for v in ks},
                        Kmin_mean={v: round(sum(ks[v])/max(1, len(ks[v])), 2) for v in ks})
print('random', out['random_t0'], flush=True)
json.dump(out, open('/mnt/project-files/multiscale/multicut/unbounded/sanity_vr.json', 'w'), indent=0)
