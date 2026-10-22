# Task 1 on the canonical failure instances: at R = 0 and R = 1 enumerate the proper free-boundary colourings and
# report, for each measure, the best value over colourings with |t| <= 2 (and the 'keep' colouring, i.e. only v
# recoloured, for every measure). Also: the longest fixed arc alone (R = 0), as in cert.py.
import sys, glob, pickle, json, itertools
sys.path.insert(0, '/mnt/project-files/multiscale/localdetrend/'); sys.path.insert(0, '/mnt/project-files/multiscale/canonical/')
from pi import *
import ld
rows = []
for fn in sorted(glob.glob('/mnt/project-files/multiscale/canonical/fail_*.pkl')):
    d = pickle.load(open(fn, 'rb')); fl = d['fail']
    if fl is None: continue
    B2 = fl['B']; s = np.array(fl['s']); odd = fl['odd']; v = fl['v']; P = fl['P']; col = dict(fl['col'])
    adj = make(d['job'][0]); present = set(col) | {v}
    out = dict(f=fn.split('/')[-1][5:-4], L=len(B2), n=len(present), odd=odd, nodd=fl['nodd'], plen=len(P))
    for R in (0, 1):
        FB = [v] if R == 0 else [v, P[0], P[-1]]
        best = {}
        for cs in itertools.product(range(4), repeat=len(FB)):
            c2 = dict(col); c2.update(dict(zip(FB, cs)))
            if any(c2[x] == c2[y] for x in FB for y in adj[x] if y in present and y in c2): continue
            H = ld.walk_from(B2, s, c2)
            if H is None: continue
            if odd:
                m = ld.measures(H, True); m = dict(fp=m['fp'], step=m['step'])
            else:
                m = ld.measures(H, odd); m = dict(hodge=m['hodge'], strip=m['strip'], step=m['step']) if m['t'] <= 2 + 1e-9 else {}
            for k, val in m.items():
                if k not in best or val < best[k]: best[k] = round(float(val), 4)
        out['R%d_best' % R] = best
    print(json.dumps(out), flush=True); rows.append(out)
json.dump(rows, open('/mnt/project-files/multiscale/localdetrend/measures_fail.json', 'w'), indent=0)
