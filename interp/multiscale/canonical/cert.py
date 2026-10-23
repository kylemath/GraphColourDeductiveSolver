# Lower-bound certificate for R: with free set ball(v,R), the longest fixed boundary arc keeps its colours; for every
# admissible holonomy branch (even: t in {0, +-2e}; odd: centre q in (1/2)Lambda) the arc alone must fit, so
# min_branch radius(arc) > 1 proves that no recolouring within R satisfies the pair. Reports the least R not certified.
import sys, glob, pickle, json
sys.path.insert(0, '/mnt/project-files/multiscale/canonical/')
from pi import *
TS = [0j] + [2*u*z for u in (1, -1) for z in (1, W3, W3*W3)]
QS = [complex(a + b*W3)/2 for a in range(-12, 13) for b in range(-12, 13)]
def certify(adj, fl, Rmax=40):
    B2 = fl['B']; s = np.array(fl['s']); odd = fl['odd']; v = fl['v']; col = dict(fl['col']); L = len(B2)
    present = set(col) | {v}; nb = lambda x: [y for y in adj[x] if y in present]
    out = []
    for R in range(0, Rmax+1):
        pass
        F = ball(nb, v, R); fixed = [b not in F for b in B2]
        # longest cyclic run of consecutive fixed vertices
        best = (0, 0); i = 0
        if all(fixed): runs = [(0, L)]
        else:
            st = next(j for j in range(L) if not fixed[j]); runs = []; j = st + 1; cur = None
            for kk in range(1, L+1):
                idx = (st + kk) % L
                if fixed[idx]:
                    if cur is None: cur = [kk, kk]
                    else: cur[1] = kk
                else:
                    if cur: runs.append((cur[0]+st, cur[1]-cur[0]+1)); cur = None
            if cur: runs.append((cur[0]+st, cur[1]-cur[0]+1))
        if not runs: out.append((R, 0.0)); break
        a, ln = max(runs, key=lambda r: r[1])
        idx = [(a + j) % L for j in range(ln)]
        # heights along the arc (relative), using gauge signs with sign flips across the wrap for odd walks
        H = [0j]; sg = []
        for j in range(ln-1):
            p = idx[j]; sgn = s[p]
            if odd and (a + j) % (2*L) >= L and False: pass
            if (a + j) >= L and odd: sgn = -sgn   # crossing index 0 flips the gauge on an odd walk
            H.append(H[-1] + sgn*EV[col[B2[p]] ^ col[B2[idx[j+1]]]])
        H = np.array(H); pos = np.array([a + j for j in range(ln)])
        if odd: r = min(float(np.max(np.abs(H - q))) for q in QS)
        else:
            bs = set(B2); odds = [x for x in present if x not in bs and len(adj[x]) % 2]
            ts = TS
            if len(odds) == 2 and all(o not in F for o in odds) and col.get(odds[0]) != col.get(odds[1]): ts = TS[1:]
            r = min(mec(H - pos/L*t) for t in ts)
        out.append((R, round(r, 4), ln, L))
        if r <= 1 + 1e-9: break
    return out
if __name__ == '__main__':
    for fn in sorted(glob.glob('/mnt/project-files/multiscale/canonical/fail_*.pkl')):
        d = pickle.load(open(fn, 'rb')); fl = d['fail']
        if fl is None: continue
        adj = make(d['job'][0]); c = certify(adj, fl)
        print(json.dumps(dict(f=fn.split('/')[-1], L=len(fl['B']), odd=fl['odd'], nodd=fl['nodd'], certified_upto=c[-2][0] if len(c) > 1 else None, last=c[-1], first=c[0])), flush=True)
