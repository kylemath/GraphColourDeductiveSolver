# Inner LP for net2: for fixed hard shares (R2, R3) and fixed own-term choices, minimise the max row bound over
# (P, th7, th6). Variables: t, th7, th6, P, y (max over candidate sets), M2 (per R2 view), M3 (per R3 view).
#   y_c >= P_i;  c1(7-row) = -60 + sum y;  c1(6-row) = sum y - sum P_out;  c2(6-row) = c1 + sum M2
#   M2_v >= sh * (c1(R) - th7);  M3_v >= sh * (c2(Z) - th6);  M >= 0
#   7-row: own + sum M2 + sum M3 <= t (own = th7 or c1);  6-row: th6 or c2 <= t;  5-row: 60 - sum P <= t
import numpy as np, time
from scipy.optimize import linprog
from scipy.sparse import csr_matrix, vstack, hstack, coo_matrix
import net3 as N2

def uniq_rows(a):
    u, inv = np.unique(a, axis=0, return_inverse=True); return u, inv.reshape(-1)

def solve(B, sh2, sh3, own7, own6, fix=None, verbose=True, Pmax=60.0):
    """sh2: (n7, 7) float shares, sh3: (n6, 6). own7 / own6: bool, use theta as own term. fix: dict(th7=, th6=) to fix thetas."""
    T0 = time.time(); A7, A6 = B['A7'], B['A6']; NP = N2.NPAR
    IN7 = np.sort(A7['IN'], 2); IN6 = np.sort(A6['IN'], 2)
    K = max(IN7.shape[2], IN6.shape[2])
    pad = lambda a: np.concatenate([a, np.repeat(a[:, :, -1:], K - a.shape[2], 2)], 2)
    cands, cinv = uniq_rows(np.concatenate([pad(IN7).reshape(-1, K), pad(IN6).reshape(-1, K)]))
    nY = len(cands); zc = np.flatnonzero((cands == N2.ZERO).all(1))
    cs7 = cinv[:A7['n'] * 7].reshape(A7['n'], 7); cs6 = cinv[A7['n'] * 7:].reshape(A6['n'], 6)
    nV2, nV3 = B['nV2'], B['nV3']
    oT, o7, o6, oP = 0, 1, 2, 3; oY = oP + NP; oM2 = oY + nY; oM3 = oM2 + nV2; nv = oM3 + nV3
    rows_i, rows_j, rows_v, rhs = [], [], [], []; nrow = [0]
    def add(ri, cj, vals, b):
        """ri: local row ids 0..m-1 (array), cj col ids, vals; b: rhs per local row."""
        m = len(b); rows_i.append(ri + nrow[0]); rows_j.append(cj); rows_v.append(vals); rhs.append(b); nrow[0] += m
    # y >= P
    ci, pi = np.nonzero(cands != N2.ZERO); pv = cands[ci, pi]; pairs = np.unique(np.stack([ci, pv], 1), axis=0)
    m = len(pairs); r = np.arange(m)
    add(np.r_[r, r], np.r_[oP + pairs[:, 1], oY + pairs[:, 0]], np.r_[np.ones(m), -np.ones(m)], np.zeros(m))
    # helper: per-row counts matrix of y columns (excluding zero sets)
    def ycount(cs):
        n, d = cs.shape; rr = np.repeat(np.arange(n), d); cc = cs.reshape(-1)
        keep = ~np.isin(cc, zc)
        return csr_matrix((np.ones(keep.sum()), (rr[keep], oY + cc[keep])), shape=(n, nv))
    def vcount(v, off, n):
        rr, cc = np.nonzero(v >= 0)
        return csr_matrix((np.ones(len(rr)), (rr, off + v[rr, cc])), shape=(n, nv))
    C1_7 = ycount(cs7)                                                  # c1 + 60
    OUTP = A6['OUT']; rr, cc = np.nonzero(OUTP != N2.ZERO)
    C1_6 = ycount(cs6) - csr_matrix((np.ones(len(rr)), (rr, oP + OUTP[rr, cc])), shape=(A6['n'], nv))
    IN2_7 = vcount(A7['r2v'], oM2, A7['n']); IN3_7 = vcount(A7['r3v'], oM3, A7['n']); IN2_6 = vcount(A6['r2v'], oM2, A6['n'])
    C2_6 = C1_6 + IN2_6
    blocks = []; brhs = []
    def emit(Mat, b):
        Mat = Mat.tocsr(); Mat.sum_duplicates()
        # dedupe identical rows
        key = np.concatenate([Mat.indptr[1:, None] - Mat.indptr[:-1, None]], 1)
        blocks.append(Mat); brhs.append(np.asarray(b, float))
    e_t = lambda n, c=-1.0: csr_matrix((np.full(n, c), (np.arange(n), np.zeros(n, int))), shape=(n, nv))
    e_col = lambda n, col, vals: csr_matrix((vals, (np.arange(n), np.full(n, col))), shape=(n, nv))
    # M2 >= sh*(c1(R) - th7):  sh*C1_7[R] - sh*th7 - M2_v <= 60 sh
    src = A7['src']; sh = sh2[src[:, 0], src[:, 1]]; k = sh > 0; s_ = src[k]; shv = sh[k]
    Mt = C1_7[s_[:, 0]].multiply(shv[:, None]) + e_col(len(shv), o7, -shv) + e_col(len(shv), 0, np.zeros(len(shv)))
    Mt = Mt.tocsr() - csr_matrix((np.ones(len(shv)), (np.arange(len(shv)), oM2 + s_[:, 2])), shape=(len(shv), nv))
    emit(Mt, 60 * shv)
    # M3 >= sh*(c2(Z) - th6)
    src = A6['src']; sh = sh3[src[:, 0], src[:, 1]]; k = sh > 0; s_ = src[k]; shv = sh[k]
    Mt = C2_6[s_[:, 0]].multiply(shv[:, None]).tocsr() + e_col(len(shv), o6, -shv)
    Mt = Mt - csr_matrix((np.ones(len(shv)), (np.arange(len(shv)), oM3 + s_[:, 2])), shape=(len(shv), nv))
    emit(Mt, np.zeros(len(shv)))
    # 7-rows
    live = ~A7['excused']; n = A7['n']; has2 = (A7['tgt2'] >= 0).any(1); th = own7 & has2
    base = IN2_7 + IN3_7 + e_t(n)
    OWN = C1_7.multiply((~th)[:, None]) + e_col(n, o7, th.astype(float))
    emit((base + OWN)[live], (60.0 * (~th))[live])
    # 6-rows
    live = ~A6['excused']; n = A6['n']; has3 = (A6['tgt3'] >= 0).any(1); th = own6 & has3
    OWN = C2_6.multiply((~th)[:, None]) + e_col(n, o6, th.astype(float)) + e_t(n)
    emit(OWN.tocsr()[live], np.zeros(int(live.sum())))
    # 5-rows
    n = len(B['P5']); rr, cc = np.nonzero(B['P5'] != N2.ZERO)
    emit(-csr_matrix((np.ones(len(rr)), (rr, oP + B['P5'][rr, cc])), shape=(n, nv)) + e_t(n), -60.0 * np.ones(n))
    Y = csr_matrix((np.concatenate(rows_v), (np.concatenate(rows_i), np.concatenate(rows_j))), shape=(nrow[0], nv))
    A = vstack([Y] + blocks).tocsr(); b = np.concatenate([np.concatenate(rhs)] + brhs)
    # dedupe rows
    A.sum_duplicates(); A.eliminate_zeros()
    Ac = A.tocoo(); keyrows = {}
    rowdata = [None] * A.shape[0]
    indptr, ind, dat = A.indptr, A.indices, A.data
    keys = [(tuple(ind[indptr[i]:indptr[i + 1]]), tuple(np.round(dat[indptr[i]:indptr[i + 1]], 9)), round(b[i], 9)) for i in range(A.shape[0])]
    _, first = np.unique(np.array([hash(k) for k in keys]), return_index=True)
    A = A[np.sort(first)]; b = b[np.sort(first)]
    bounds = [(None, None), (-120, 120), (-120, 120)] + [(0, Pmax)] * NP + [(0, None)] * (nY + nV2 + nV3)
    if fix:
        if 'th7' in fix: bounds[o7] = (fix['th7'], fix['th7'])
        if 'th6' in fix: bounds[o6] = (fix['th6'], fix['th6'])
    c = np.zeros(nv); c[oT] = 1
    res = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')
    if verbose: print('  LP2: %d rows, %d vars, status %d, t = %s [%.1fs]' % (A.shape[0], nv, res.status, res.fun if res.status == 0 else None, time.time() - T0), flush=True)
    if res.status != 0: return None
    x = res.x
    return dict(t=float(x[oT]), th7=float(x[o7]), th6=float(x[o6]), P=x[oP:oP + NP].copy(), M2=x[oM2:oM3], M3=x[oM3:], res=res)
