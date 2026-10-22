# Transfer-matrix check of band filling on the straight triangular-lattice cylinder of circumference L (all degree 6).
# rows = proper colourings of C_L; r -> r' allowed iff r'(i) != r(i), r(i+1). Level row: boundary walk (constant sign) within
# distance 1 of some half-lattice centre.  C(w): for every A-row a that is w steps below a level row and every B-row b that is
# w steps above a level row, some renaming pi gives a path a -> pi b of exactly 2w+1 steps (recolour w rows on each side).
import sys, itertools, numpy as np, scipy.sparse as sp, json, math
sys.path.insert(0, '/mnt/project-files/multiscale/levelling')
INC = {1: (2, 0), 2: (0, 2), 3: (-2, -2)}
def n2(p): return (p[0]*p[0]+p[1]*p[1]-p[0]*p[1])/4.0
def rows(L):
    out = []
    def rec(pref):
        if len(pref) == L:
            if pref[-1] != pref[0]: out.append(tuple(pref))
            return
        for c in range(4):
            if c != pref[-1]: rec(pref+[c])
    for c in range(4): rec([c])
    return out
def walk(r):
    H = [(0, 0)]
    for i in range(len(r)):
        d = INC[r[i] ^ r[(i+1) % len(r)]]; H.append((H[-1][0]+d[0], H[-1][1]+d[1]))
    return H
def tau(r):
    H = walk(r); As = [h[0] for h in H]; Bs = [h[1] for h in H]
    return math.sqrt(min(max(n2((h[0]-A, h[1]-B)) for h in H) for A in range(min(As)-2, max(As)+3) for B in range(min(Bs)-2, max(Bs)+3))), H[-1]
PERMS = list(itertools.permutations(range(4)))
def run(L, wmax=6):
    R = rows(L); idx = {r: i for i, r in enumerate(R)}; N = len(R)
    I, J = [], []
    for i, r in enumerate(R):
        ch = [[c for c in range(4) if c != r[k] and c != r[(k+1) % L]] for k in range(L)]
        for r2 in itertools.product(*ch):
            if all(r2[k] != r2[(k+1) % L] for k in range(L)): I.append(i); J.append(idx[r2])
    M = sp.csr_matrix((np.ones(len(I), dtype=np.int8), (I, J)), shape=(N, N)); MT = M.T.tocsr()
    taus = [tau(r) for r in R]
    lev = np.array([t[0] <= 1+1e-9 for t in taus])
    perm_of = np.array([[idx[tuple(p[c] for c in r)] for r in R] for p in PERMS])   # 24 x N
    canon = sorted(set(int(perm_of[:, i].min()) for i in range(N)))
    ts = sorted(set(taus[i][1] for i in range(N) if lev[i]))
    res = dict(L=L, N=N, nlevel=int(lev.sum()), level_t=[list(t) for t in ts])
    step = lambda v, A: (A.T @ v.astype(np.int8)) > 0   # v: indicator of current set -> next set via A (rows->succ)
    # level-to-level distance
    def reach_exact(src_vec, k, A):
        v = src_vec.copy(); out = [v]
        for _ in range(k): v = (A.T @ v.astype(np.int32)) > 0; out.append(v)
        return out
    levidx = np.where(lev)[0]
    canon_lev = sorted(set(int(perm_of[:, i].min()) for i in levidx))
    dLL = 0
    for a in canon_lev:
        e = np.zeros(N, bool); e[a] = True; lay = reach_exact(e, 3*L+6, M)
        orb = [np.zeros(N, bool) for _ in lay]
        for k, v in enumerate(lay): orb[k] = v[perm_of].any(axis=0) if False else np.zeros(N,bool)
        # first k at which all level rows are hit up to renaming
        for k, v in enumerate(lay):
            if k == 0: continue
            hit = v[perm_of.T].any(axis=1)   # hit[j]: some pi with pi(R_j)... perm_of.T[j] = images of j
            if hit[levidx].all(): dLL = max(dLL, k); break
        else: dLL = None; break
    res['dLL'] = dLL
    # C(w)
    lv = lev.copy(); DA = lv.copy(); UB = lv.copy(); Cw = {}
    for w in range(0, wmax+1):
        if w > 0:
            DA = (M @ DA.astype(np.int32)) > 0     # a with a->(something in DA)
            UB = (MT @ UB.astype(np.int32)) > 0    # b with (UB)->b
        ok = True; bad = 0
        Ub = np.where(UB)[0]
        for a in sorted(set(int(perm_of[:, i].min()) for i in np.where(DA)[0])):
            e = np.zeros(N, bool); e[a] = True; v = e
            for _ in range(2*w+1): v = (MT @ v.astype(np.int32)) > 0
            hit = v[perm_of.T].any(axis=1)
            if not hit[Ub].all(): ok = False; bad += 1
        Cw[w] = (ok, bad, int(DA.sum()), int(UB.sum()))
        if ok: break
    res['C'] = Cw
    return res
if __name__ == '__main__':
    for L in map(int, sys.argv[1].split(',')):
        print(json.dumps(run(L)), flush=True)
