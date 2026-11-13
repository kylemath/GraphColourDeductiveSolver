# Inner solver: for FIXED forward shares (hard attention) and a fixed per-row choice of the own term (theta or c1), the row bounds
# are convex piecewise-linear in (push table P, theta), so min over (P, theta) of the max final charge is an LP:
#   y_c >= P_i (i in candidate set c)                      [upper bound of a max over hidden letters]
#   c1(R) = -60 + sum_k y_{cs(R,k)}
#   M_v >= 0,  M_v >= share(R,j) * (c1(R) - theta)       for every admissible neighbour row R, slot j with view v
#   7-row X:  own(X) + sum_{7-slots} M_{v(X,k)} <= t,  own = theta (X has a 7 neighbour) or c1(X)
#   5-row:    60 - sum P <= t;   6-row: -sum out P + sum y <= t
# All of this is an upper bound of the network's exact final charge (min(c1, theta) <= both choices).
import numpy as np, collections, time
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
import net as NT

def cs_index(B):
    """distinct candidate sets (tuple of param indices) for the 7-row slots and the 6-row in-slots."""
    P7 = np.sort(B['P7'], axis=2); I6 = np.sort(B['I6'], axis=2)
    allc = np.concatenate([P7.reshape(-1, 4), I6.reshape(-1, 4)])
    uniq, inv = np.unique(allc, axis=0, return_inverse=True)
    inv = inv.reshape(-1)
    n7 = P7.shape[0] * 7
    return uniq, inv[:n7].reshape(P7.shape[0], 7), inv[n7:].reshape(I6.shape[0], 6)

def solve(B, shares, own_theta, Pmax=60.0, fixP=None, verbose=True, t_floor=None):
    """shares: (N,7) float array (rows sum to 1 over 7-slots, 0 elsewhere). own_theta: (N,) bool, use theta as own term.
    Returns dict(t, P, theta, M)."""
    T0 = time.time()
    uniq, cs7, cs6 = cs_index(B)
    zero_cs = [i for i, c in enumerate(uniq) if (c == NT.ZERO).all()]
    NP = NT.NPAR; NY = len(uniq); NV = B['nview']
    # variable layout: [t, theta, P(NP), y(NY), M(NV)]
    iT, iTh = 0, 1; oP = 2; oY = oP + NP; oM = oY + NY; nv = oM + NV
    Ai, Aj, Av, b = [], [], [], []
    def row(coefs, rhs):
        r = len(b); b.append(rhs)
        for j, v in coefs.items(): Ai.append(r); Aj.append(j); Av.append(v)
    # y_c >= P_i
    for c, cand in enumerate(uniq):
        for i in set(cand.tolist()):
            if i != NT.ZERO: row({oP + i: 1.0, oY + c: -1.0}, 0.0)
    ZY = set(zero_cs)
    def c1terms(csrow):
        d = collections.Counter()
        for c in csrow:
            if c not in ZY: d[oY + int(c)] += 1.0
        return d
    live = ~B['excused']
    # M_v >= share * (c1(R) - theta): dedupe by (view, share, c1 key)
    seen = set(); nM = 0
    sh = shares[B['srow'], B['sslot']]
    for e in np.flatnonzero(sh > 0):
        r = int(B['srow'][e]); v = int(B['sview'][e]); s = float(sh[e])
        key = (v, s, tuple(sorted(cs7[r][~B['is7'][r]].tolist())))
        if key in seen: continue
        seen.add(key)
        d = c1terms(cs7[r][~B['is7'][r]]); co = {j: s * x for j, x in d.items()}; co[iTh] = -s; co[oM + v] = -1.0
        row(co, 60.0 * s); nM += 1
    # 7-rows
    seen = set(); nX = 0
    for r in np.flatnonzero(live):
        r = int(r); vs = tuple(sorted(B['vX'][r][B['is7'][r]].tolist()))
        th = bool(own_theta[r]) and bool(B['has7'][r])
        key = (th, vs) if th else (th, vs, tuple(sorted(cs7[r][~B['is7'][r]].tolist())))
        if key in seen: continue
        seen.add(key)
        co = collections.Counter()
        for v in vs: co[oM + v] += 1.0
        if th: co[iTh] += 1.0; rhs = 0.0
        else:
            for j, x in c1terms(cs7[r][~B['is7'][r]]).items(): co[j] += x
            rhs = 60.0
        co[iT] -= 1.0; row(dict(co), rhs); nX += 1
    # 5-rows: 60 - sum P <= t
    for r in range(len(B['P5'])):
        co = collections.Counter()
        for i in B['P5'][r]:
            if i != NT.ZERO: co[oP + int(i)] -= 1.0
        co[iT] -= 1.0; row(dict(co), -60.0)
    # 6-rows
    for r in range(len(B['O6'])):
        co = collections.Counter()
        for i in B['O6'][r]:
            if i != NT.ZERO: co[oP + int(i)] -= 1.0
        for c in cs6[r]:
            if int(c) not in ZY: co[oY + int(c)] += 1.0
        co[iT] -= 1.0; row(dict(co), 0.0)
    A = coo_matrix((Av, (Ai, Aj)), shape=(len(b), nv)).tocsr()
    cobj = np.zeros(nv); cobj[iT] = 1.0
    bounds = [(t_floor, None), (-120.0, 120.0)] + [(0.0, Pmax)] * NP + [(0.0, None)] * NY + [(0.0, None)] * NV
    if fixP is not None:
        for i in range(NP): bounds[oP + i] = (float(fixP[i]), float(fixP[i]))
    res = linprog(cobj, A_ub=A, b_ub=np.array(b), bounds=bounds, method='highs')
    if verbose: print('  LP: %d rows (M %d, X %d), %d vars, status %d, t = %s [%.1fs]' % (len(b), nM, nX, nv, res.status, res.fun if res.status == 0 else None, time.time() - T0), flush=True)
    if res.status != 0: return None
    x = res.x
    return dict(t=float(x[iT]), theta=float(x[iTh]), P=x[oP:oP + NP].copy(), M=x[oM:oM + NV].copy(), res=res)
