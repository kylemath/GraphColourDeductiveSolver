# Diagnostic: two-cut odd measure. Pieces H[0..j1], H[j1+1..j2] - u, r_p(H[j2+1..L-1]) - u  (p = q + u/2, u in {+-2e})
# or the mirror order H, r_p(H), r_p(H) + u (p = q - u/2). Min over cuts/u/order of the union circumradius.
import sys, math, itertools, functools, numpy as np
sys.path.insert(0, '/mnt/project-files/multiscale/localdetrend/'); sys.path.insert(0, '/mnt/project-files/multiscale/canonical/')
import ld; from pi import mec, W3
US = [2*w*z for w in (1, -1) for z in (1, W3, W3*W3)]
def tau_two(H, T=1.0):
    L = len(H)-1; q = (H[0]+H[-1])/2; P = H[:L]
    @functools.lru_cache(None)
    def rad(a, b): return float(mec(P[a:b+1])) if b >= a else 0.0
    best = (9, None)
    # prefix window
    jmax = max([j for j in range(L) if rad(0, j) <= T+1e-9] or [-1])
    for u in US:
        for order in (0, 1):
            p = q + u/2 if order == 0 else q - u/2
            for j1 in range(-1, jmax+1):
                for j2 in range(j1, L-1):
                    if rad(j1+1, j2) > T+1e-9: break
                    if rad(j2+1, L-1) > T+1e-9: continue
                    mid = P[j1+1:j2+1]; end = P[j2+1:]
                    if order == 0: pts = np.concatenate([P[:j1+1], mid - u, (2*p - end) - u])
                    else: pts = np.concatenate([P[:j1+1], 2*p - mid, (2*p - end) + u])
                    r = float(mec(pts))
                    if r < best[0]: best = (r, (j1, j2, u, order))
    return best
if __name__ == '__main__':
    import pickle; from pi import make
    for fn in sys.argv[1:]:
        d = pickle.load(open(fn, 'rb')); fl = d['fail']; adj = make(d['job'][0])
        B2 = fl['B']; s = np.array(fl['s']); v = fl['v']; P = fl['P']; col = dict(fl['col']); present = set(col)|{v}
        for R in (0, 1):
            FB = [v] if R == 0 else [v, P[0], P[-1]]; best = (9, None)
            for cs in itertools.product(range(4), repeat=len(FB)):
                c2 = dict(col); c2.update(dict(zip(FB, cs)))
                if any(c2[x] == c2[y] for x in FB for y in adj[x] if y in present and y in c2): continue
                H = ld.walk_from(B2, s, c2)
                if H is None: continue
                r = tau_two(H); best = min(best, r, key=lambda z: z[0])
            print(fn.split('/')[-1], 'L', len(B2), 'odd', fl['odd'], 'nodd', fl['nodd'], 'R', R, 'two-cut best', best, flush=True)
