# per-pair minimal k, grouped by the hidden tilt (max cyclic run of equal edge labels) of a and b.
import sys, json, time, numpy as np, collections
from lev import gen_level, PERMS
from fill import build_T, fill_batch, canon_a
def maxrun(r):
    L = len(r); lab = [r[i] ^ r[(i+1) % L] for i in range(L)]
    best = 0
    for s in range(L):
        c = 1
        while c < L and lab[(s+c) % L] == lab[s]: c += 1
        best = max(best, c)
    return best
def run3(L, kmax):
    lev = gen_level(L); can = sorted(set(canon_a(r) for r in lev)); B = np.array(lev, dtype=np.int64)
    Ts = {k: build_T(k) for k in range(kmax+1)}
    runs = np.array([maxrun(r) for r in lev])
    hist = collections.Counter()
    for a in can:
        ra = maxrun(a); best = np.full(len(lev), 99, dtype=int)
        for k in range(kmax+1):
            T, n = Ts[k]; okk = np.zeros(len(lev), dtype=bool)
            for p in PERMS: okk |= fill_batch(a, np.array(p)[B], T, n)
            best[(best == 99) & okk] = k
            if (best < 99).all(): break
        for j in range(len(lev)): hist[(ra, int(runs[j]), int(best[j]))] += 1
    out = collections.defaultdict(dict)
    for (ra, rb, k), v in sorted(hist.items()): out[f'{ra},{rb}'][str(k)] = v
    return dict(L=L, kmax=kmax, nlevel=len(lev), ncanon=len(can), by_run=dict(out))
if __name__ == '__main__':
    L = int(sys.argv[1]); kmax = int(sys.argv[2]); t = time.time()
    r = run3(L, kmax); r['sec'] = round(time.time() - t, 1); print(json.dumps(r), flush=True)
