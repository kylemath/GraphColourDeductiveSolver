# Finite semigroup closure proving band filling for ALL L (uniform in L) at a given k (inserted rows).
# Words = pairs (a,b) of level rows with skeleton colour 0 (WLOG by global renaming; the top row is glued as pi(b), pi in a set PI).
# Element of a word of length m: (qa0,qa1,qb0,qb1,a0,b0, P[pi] for pi in PI), P[pi] = boolean 16x16 relation between the inner
# column states at column 0 and column m-1 (column validity and column-to-column compatibility included).
# Layers E_m = E_{m-1}.G ; the sequence of layers is eventually periodic; closed elements (qa0==qa1, qb0==qb1) of E_L are exactly the
# level pairs of length L; the pair is fillable with k rows for renaming pi iff trace(P[pi] . T(a_last,a0,pi b_last,pi b0)) != 0.
import sys, itertools, numpy as np, time, json, collections
from fill import build_T
from lev import PERMS

def lev_automaton():
    """states (g,d,x): g non-c letters since last c (c=0), d defect used, x last letter. returns dict state->list of (letter, newstate)"""
    st = {}
    S = [(g, d, x) for g in range(4) for d in range(2) for x in range(4)]
    for (g, d, x) in S:
        outs = []
        for y in range(4):
            if y == x: continue
            if y == 0:
                if g == 2: outs.append((y, (0, d, 0)))
                elif g in (1, 3) and d == 0: outs.append((y, (0, 1, 0)))
            else:
                if g + 1 <= 2: outs.append((y, (g+1, d, y)))
                elif g + 1 == 3 and d == 0: outs.append((y, (3, d, y)))
        st[(g, d, x)] = outs
    return st
def run(k, PI=None, maxm=60, verbose=True):
    T, n = build_T(k)
    if PI is None: PI = list(range(24))
    perms = [PERMS[p] for p in PI]; npi = len(perms)
    A = lev_automaton(); S = sorted(A); sid = {s: i for i, s in enumerate(S)}
    # generator letters: single columns (ya, yb).  Element of a one-letter word starting from states qa0,qb0: qa1 = succ, P = D(ya, pi yb).
    # Represent layer as dict key-> set? Use numpy: keys (N,6) int16 : qa0,qa1,qb0,qb1,a0,b0 ; P (N,npi,n) uint64
    ident = np.array([1 << i for i in range(n)], dtype=np.uint64)
    def D(xa, xb):
        # diagonal validity of column (xa, s, xb): from T: column valid iff some row entry... use T[xa, ya, xb, yb] rows nonzero for some ya,yb? simpler: recompute
        from fill import inner_states
        out = np.zeros(n, dtype=np.uint64)
        for i, s in enumerate(inner_states(k)):
            col = (xa,) + s + (xb,)
            if all(col[j] != col[j+1] for j in range(len(col)-1)): out[i] = np.uint64(1) << np.uint64(i)
        return out
    Dm = {(xa, xb): D(xa, xb) for xa in range(4) for xb in range(4)}
    keys = []; Ps = []
    for qa0 in S:
        for (ya, qa1) in A[qa0]:
            for qb0 in S:
                for (yb, qb1) in A[qb0]:
                    keys.append((sid[qa0], sid[qa1], sid[qb0], sid[qb1], ya, yb))
                    Ps.append(np.stack([Dm[(ya, p[yb])] for p in perms]))
    keys = np.array(keys, dtype=np.int16); Ps = np.array(Ps, dtype=np.uint64)
    def dedupe(keys, Ps):
        flat = np.concatenate([keys.astype(np.uint64).view(np.uint64), Ps.reshape(len(Ps), -1)], axis=1)
        _, idx = np.unique(flat, axis=0, return_index=True)
        return keys[idx], Ps[idx]
    keys, Ps = dedupe(keys, Ps)
    # transitions lookup: for state id -> list of (letter, newid)
    succ = {sid[s]: [(y, sid[t]) for (y, t) in A[s]] for s in S}
    lastx = np.array([s[2] for s in S])
    def step(keys, Ps):
        newk = []; newP = []
        # group by (qa1, qb1)
        qa1 = keys[:, 1]; qb1 = keys[:, 3]
        for ia in range(len(S)):
            ma = qa1 == ia
            if not ma.any(): continue
            for ib in range(len(S)):
                m = ma & (qb1 == ib)
                if not m.any(): continue
                K = keys[m]; P = Ps[m]; xa = lastx[ia]; xb = lastx[ib]
                for (ya, na) in succ[ia]:
                    for (yb, nb) in succ[ib]:
                        # P' = P . T(xa, ya, pi xb, pi yb)
                        Tt = np.stack([T[xa, ya, p[xb], p[yb]] for p in perms])  # (npi, n) rows bitmask
                        C = np.zeros_like(P)
                        for j in range(n):
                            bit = ((P >> np.uint64(j)) & np.uint64(1))        # (N, npi, n)
                            C |= bit * Tt[None, :, j][:, :, None]
                        K2 = K.copy(); K2[:, 1] = na; K2[:, 3] = nb
                        newk.append(K2); newP.append(C)
        keys2 = np.concatenate(newk); Ps2 = np.concatenate(newP)
        return dedupe(keys2, Ps2)
    def closed_check(keys, Ps):
        m = (keys[:, 0] == keys[:, 1]) & (keys[:, 2] == keys[:, 3])
        K = keys[m]; P = Ps[m]; bad = 0; ok_pis = collections.Counter(); nclosed = len(K)
        badlist = []
        for r in range(len(K)):
            xa = lastx[K[r, 1]]; xb = lastx[K[r, 3]]; a0 = K[r, 4]; b0 = K[r, 5]
            good = []
            for pi_i, p in enumerate(perms):
                Tt = T[xa, a0, p[xb], p[b0]]
                tr = False
                for i in range(n):
                    row = int(P[r, pi_i, i])
                    for j in range(n):
                        if (row >> j) & 1 and (int(Tt[j]) >> i) & 1: tr = True; break
                    if tr: break
                if tr: good.append(pi_i)
            if not good: bad += 1; badlist.append(tuple(int(v) for v in K[r]))
            else: ok_pis[len(good)] += 1
        return nclosed, bad, badlist
    seen = {}; layers = []
    for m in range(1, maxm+1):
        if m > 1:
            keys, Ps = step(keys, Ps)
        h = hash((keys.tobytes(), Ps.tobytes()))
        nclosed, bad, badlist = closed_check(keys, Ps)
        if verbose: print(json.dumps(dict(k=k, m=m, nelem=len(keys), nclosed=nclosed, bad=bad, badex=badlist[:3])), flush=True)
        layers.append((m, len(keys), nclosed, bad))
        if h in seen:
            print('PERIODIC: layer', m, 'equals layer', seen[h], '-> all lengths covered; period', m - seen[h], flush=True)
            return layers, seen[h], m
        seen[h] = m
    return layers, None, None
if __name__ == '__main__':
    k = int(sys.argv[1]); PI = None
    if len(sys.argv) > 2: PI = list(map(int, sys.argv[2].split(',')))
    run(k, PI)
