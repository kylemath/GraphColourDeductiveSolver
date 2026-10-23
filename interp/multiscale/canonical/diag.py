# diagnose failure pickles: at R=0,1 enumerate all proper free-boundary assignments, report min tau / |t| needed.
import sys, glob, pickle, json, itertools
sys.path.insert(0, '/mnt/project-files/multiscale/canonical/')
from pi import *
for fn in sorted(glob.glob('/mnt/project-files/multiscale/canonical/fail_*.pkl')):
    d = pickle.load(open(fn, 'rb')); fl = d['fail']
    if fl is None: continue
    B2 = fl['B']; s = np.array(fl['s']); odd = fl['odd']; v = fl['v']; P = fl['P']; col = dict(fl['col'])
    adj = make(d['job'][0]); present = set(col) | {v}
    out = dict(f=fn.split('/')[-1], L=len(B2), odd=odd, nodd=fl['nodd'], plen=len(P), degv=len(adj[v]))
    for R in (0, 1):
        # free boundary = v plus (R=1) the two path ends
        FB = [v] if R == 0 else [v, P[0], P[-1]]
        best = None
        for cs in itertools.product(range(4), repeat=len(FB)):
            c2 = dict(col); c2.update(dict(zip(FB, cs)))
            if any(c2[x] == c2[y] for x in FB for y in adj[x] if y in present and y in c2): continue
            H = walk(B2, s, np.array([c2[b] for b in B2]))
            if H is None: continue
            if odd: r = float(np.max(np.abs(H - (H[0]+H[-1])/2))); key = (r,)
            else:
                Lb = len(H)-1; t = H[-1]-H[0]; r = mec(H[:-1] - np.arange(Lb)/Lb*t); key = (abs(t) > 2+1e-9, r, abs(t))
            if best is None or key < best: best = key
        out['R%d_best' % R] = [round(float(z), 4) for z in best] if best else None
    # previous disc (before the step) invariant values
    print(json.dumps(out), flush=True)
