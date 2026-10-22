# Direct band-filling check between level rows a (bottom) and pi(b) (top) with k inserted rows, by boolean column transfer.
# Band rows r_0=a, r_1..r_k inserted, r_{k+1}=pi b.  Adjacencies: r_n(i)~r_n(i+1), r_n(i)~r_{n+1}(i), r_{n+1}(i)~r_n(i+1).
import sys, itertools, numpy as np, collections, json, time
from lev import gen_level, rot, PERMS

def inner_states(k): return list(itertools.product(range(4), repeat=k))
def build_T(k):
    """T[xa, ya, xb, yb][s, s'] : column i has (xa, s, xb), column i+1 has (ya, s', yb); 1 iff both columns valid & compatible.
       Returned as uint64 bitmask rows: T[xa,ya,xb,yb,s] = bitmask over s'. Column validity included on both sides."""
    S = inner_states(k); n = len(S)
    def colok(x, s, y):
        col = (x,) + s + (y,)
        return all(col[j] != col[j+1] for j in range(len(col)-1))
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
                            # row adjacency inner: s_n != t_n ; diagonals: r_{n+1}(i) != r_n(i+1)
                            if any(s[q] == t[q] for q in range(k)): continue
                            lo = (xa,) + s + (xb,); hi = (ya,) + t + (yb,)
                            if any(lo[q+1] == hi[q] for q in range(k+1)): continue
                            m |= 1 << j
                        T[xa, ya, xb, yb, i] = m
    return T, n
def fill_batch(a, B, T, n):
    """a: tuple length L; B: array (Nb, L) of top rows. returns bool array: cyclic trace nonzero."""
    L = len(a); Nb = B.shape[0]
    # P: (Nb, n) bitmask rows, start identity
    P = np.tile(np.array([1 << i for i in range(n)], dtype=np.uint64), (Nb, 1))
    for i in range(L):
        Ti = T[a[i], a[(i+1) % L], B[:, i], B[:, (i+1) % L]]   # (Nb, n) rows of bitmasks (for s), each bitmask over s'
        C = np.zeros_like(P)
        for j in range(n):
            C |= (((P >> j) & 1) * Ti[:, j][:, None]).astype(np.uint64)
        P = C
    tr = np.zeros(Nb, dtype=bool)
    for i in range(n): tr |= ((P[:, i] >> i) & 1).astype(bool)
    return tr
def canon_a(r):
    return min(tuple(p[c] for c in rot(r, k)) for p in PERMS for k in range(len(r)))
def run(L, kmax=3):
    lev = gen_level(L); levset = set(lev)
    can = sorted(set(canon_a(r) for r in lev))
    B = np.array(lev, dtype=np.int64)
    Ts = {k: build_T(k) for k in range(0, kmax+1)}
    # for each canonical a, each b: minimal k over pi.  Also which pi work at that k.
    hist = collections.Counter(); worst = []
    need = {}
    piok = collections.Counter()
    for a in can:
        best = np.full(len(lev), 99, dtype=int)
        okpi_at_best = [set() for _ in lev]
        for k in range(0, kmax+1):
            T, n = Ts[k]
            okk = np.zeros(len(lev), dtype=bool)
            for pi_i, p in enumerate(PERMS):
                Bp = np.array(p)[B]
                ok = fill_batch(a, Bp, T, n)
                newly = ok & (best > k)
                for j in np.where(ok & (best >= k))[0]: okpi_at_best[j].add(pi_i)
                okk |= ok
            best[(best > k) & okk] = k
            if (best <= k).all(): break
        for j, b in enumerate(lev):
            hist[int(best[j])] += 1
            if best[j] >= 3 or best[j] == 99: worst.append((a, b, int(best[j])))
        need[a] = best
        # does a pi with pi(c_b)=c_a always work?  record, for pairs, whether identity-type pi suffices (skeleton colour match)
    return can, lev, need, hist, worst
if __name__ == '__main__':
    for L in map(int, sys.argv[1].split(',')):
        t0 = time.time()
        can, lev, need, hist, worst = run(L)
        print(json.dumps(dict(L=L, nlevel=len(lev), ncanon=len(can), hist=dict(sorted(hist.items())), nworst=len(worst), worst=worst[:6], sec=round(time.time()-t0,1))), flush=True)

def skel_colours(r):
    L = len(r); out = set()
    for c in range(4):
        pos = [i for i in range(L) if r[i] == c]
        if not pos: continue
        gaps = [(pos[(j+1) % len(pos)] - pos[j]) % L or L for j in range(len(pos))]
        odd = [g for g in gaps if g != 3]
        if len(odd) == 0 or (len(odd) == 1 and odd[0] in (2, 4)): out.add(c)
    return out
def run2(L, kmax=3):
    """per pair: minimal k, and the set of pi working at that k; summary of skeleton-colour matching"""
    lev = gen_level(L); can = sorted(set(canon_a(r) for r in lev)); B = np.array(lev, dtype=np.int64)
    Ts = {k: build_T(k) for k in range(0, kmax+1)}
    hist = collections.Counter(); match_some = collections.Counter(); match_all = collections.Counter(); npi_hist = collections.Counter()
    worst = []
    for a in can:
        Sa = skel_colours(a)
        best = np.full(len(lev), 99, dtype=int); okpi = [[] for _ in lev]
        for k in range(0, kmax+1):
            T, n = Ts[k]; okk = np.zeros(len(lev), dtype=bool)
            for pi_i, p in enumerate(PERMS):
                ok = fill_batch(a, np.array(p)[B], T, n)
                for j in np.where(ok & (best >= 99))[0]: okpi[j].append(pi_i)
                okk |= ok
            best[(best == 99) & okk] = k
            if (best < 99).all(): break
        for j, b in enumerate(lev):
            kk = int(best[j]); hist[kk] += 1
            Sb = skel_colours(b); pis = okpi[j]
            ms = any(PERMS[p][cb] in Sa for p in pis for cb in Sb)
            ma = all((p in pis) for p in range(24) for cb in Sb if PERMS[p][cb] in Sa)
            match_some[(kk, ms)] += 1; match_all[(kk, ma)] += 1; npi_hist[(kk, len(pis))] += 1
            if kk >= 3: worst.append((a, b, kk, pis))
    return dict(L=L, nlevel=len(lev), ncanon=len(can), hist=dict(sorted(hist.items())),
                match_some=sorted((str(k), v) for k, v in match_some.items()), match_all=sorted((str(k), v) for k, v in match_all.items()),
                npi=sorted((str(k), v) for k, v in npi_hist.items()), worst=[(w[0], w[1], w[2]) for w in worst[:5]], nworst=len(worst))
