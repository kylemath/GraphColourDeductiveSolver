# failure diagnostics: at R = 0 / 1 (v; v + path ends), min #cuts (J up to 8) per variant, and the cut positions/gaps
import sys, pickle, itertools, glob
sys.path.insert(0, '/mnt/project-files/multiscale/multicut/'); sys.path.insert(0, '/mnt/project-files/multiscale/canonical/')
import mc; from pi import make
for fn in sys.argv[1:]:
    D = pickle.load(open(fn, 'rb')); fl = D['fail']; adj = make(D['spec'].split(':')[0])
    B2 = fl['B']; s = [int(x) for x in fl['s']]; v = fl['v']; P = fl['P']; col = dict(fl['col']); present = set(col) | {v}; L = len(B2)
    out = []
    for R in (0, 1):
        FB = [v] if R == 0 else [v, P[0], P[-1]]; best = {}
        for cs in itertools.product(range(4), repeat=len(FB)):
            c2 = dict(col); c2.update(dict(zip(FB, cs)))
            if any(c2[x] == c2[y] for x in FB for y in adj[x] if y in present and y in c2): continue
            lab = [c2[B2[i]] ^ c2[B2[(i+1) % L]] for i in range(L)]
            if 0 in lab: continue
            H = mc.int_walk(lab, s); t = abs(mc.cz(H[-1]))
            best['tmin'] = min(best.get('tmin', 99), round(t, 2))
            for var in ('nc', 'any', 'nc_t2'):
                if var == 'nc_t2' and not fl['odd'] and t > 2 + 1e-9: continue
                vv = var[:2] if var != 'any' else 'any'; n = mc.ncuts(H, fl['odd'], 8, vv)
                if n is not None and n < best.get(var, (99,))[0]:
                    cp = mc.cut_positions(H, fl['odd'], 8, vv); pv = B2.index(v)
                    best[var] = (n, round(t, 2), [((c - pv + L//2) % L) - L//2 for c in cp])
        out.append((R, best))
    print(fn.split('/')[-1], 'L', L, 'odd', fl['odd'], 'nodd', fl['nodd'], out, flush=True)
