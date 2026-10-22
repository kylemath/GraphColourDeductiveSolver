# (4) vortices in the band: one edge flip inside the band (between inner rows p and p+1, at columns 0-1) creates a 5,5,7,7 quadrupole.
# Boundary rows stay straight degree-6, so the level/Z3/offset hypotheses are unchanged.  Minimal k over pi for all level pairs.
import sys, itertools, numpy as np, collections, json, time
from lev import gen_level, PERMS
from fill import build_T, inner_states, canon_a
def build_T_flip(k, p):
    """like build_T but the diagonal between rows p and p+1 (0<=p<=k) is flipped: r_{p+1}(i) ~ r_p(i+1) replaced by r_p(i) ~ r_{p+1}(i+1).
       rows 0..k+1; the flipped diagonal must have both vertices interior -> 1<=p, p+1<=k."""
    S = inner_states(k); n = len(S)
    def colok(x, s, y):
        col = (x,) + s + (y,); return all(col[j] != col[j+1] for j in range(len(col)-1))
    T = np.zeros((4, 4, 4, 4, n), dtype=np.uint64)
    for xa in range(4):
        for ya in range(4):
            if xa == ya: continue
            for xb in range(4):
                for yb in range(4):
                    if xb == yb: continue
                    for i, s in enumerate(S):
                        if not colok(xa, s, xb): continue
                        m = 0
                        for j, t in enumerate(S):
                            if not colok(ya, t, yb): continue
                            if any(s[q] == t[q] for q in range(k)): continue
                            lo = (xa,) + s + (xb,); hi = (ya,) + t + (yb,)
                            bad = False
                            for q in range(k+1):
                                if q == p:
                                    if lo[q] == hi[q+1]: bad = True
                                else:
                                    if lo[q+1] == hi[q]: bad = True
                            if bad: continue
                            m |= 1 << j
                        T[xa, ya, xb, yb, i] = m
    return T, n
def fill_batch2(a, B, T, Tf, n):
    L = len(a); Nb = B.shape[0]
    P = np.tile(np.array([1 << i for i in range(n)], dtype=np.uint64), (Nb, 1))
    for i in range(L):
        TT = Tf if i == 0 else T
        Ti = TT[a[i], a[(i+1) % L], B[:, i], B[:, (i+1) % L]]
        C = np.zeros_like(P)
        for j in range(n): C |= (((P >> np.uint64(j)) & np.uint64(1)) * Ti[:, j][:, None]).astype(np.uint64)
        P = C
    tr = np.zeros(Nb, dtype=bool)
    for i in range(n): tr |= ((P[:, i] >> np.uint64(i)) & np.uint64(1)).astype(bool)
    return tr
def run(L, kmax=3):
    lev = gen_level(L); B = np.array(lev, dtype=np.int64)
    # rotation canon only for a: the flip breaks rotation symmetry of the band, but the pair (a,b) may be rotated together: so a canonical under rotation+renaming is fine
    can = sorted(set(canon_a(r) for r in lev))
    out = {}
    for k in range(2, kmax+1):
        T, n = build_T(k)
        for p in range(1, k):
            Tf, _ = build_T_flip(k, p)
            # min over k' <= k?  we compute "fillable with exactly k inserted rows and the flip at level p": report fraction unfillable
            nbad = 0; tot = 0
            for a in can:
                okk = np.zeros(len(lev), dtype=bool)
                for pi in PERMS:
                    okk |= fill_batch2(a, np.array(pi)[B], T, Tf, n)
                nbad += int((~okk).sum()); tot += len(lev)
            out[f'k{k}_p{p}'] = (nbad, tot)
            print(json.dumps(dict(L=L, k=k, p=p, unfillable=nbad, pairs=tot)), flush=True)
    return out
if __name__ == '__main__':
    for L in map(int, sys.argv[1].split(',')): run(L)
