# Tetrahedral vector SDP on a band around a closing seam; outer rows pinned to the renamed level colourings.
import sys, time, math, pickle, itertools, collections
sys.path.insert(0,'/mnt/project-files/multiscale/closing/round2'); sys.path.insert(0,'/mnt/project-files/multiscale/closing')
from band import *
import numpy as np, cvxpy as cp
TT = np.array([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]])/np.sqrt(3)
G4 = TT@TT.T

def load(fn):
    d = pickle.load(open(fn,'rb')); T = Tri(d['adj']); n = len(T.adj); A = set(d['A']); B = set(range(n))-A
    return T, A, B, d['colA'], d['colB'], d.get('R')

def close(T, A, B, colA, colB, Rmax=6):
    """best renaming, conflict-form R, and a repaired colouring phased to stay near the old one"""
    n = len(T.adj); allv = set(range(n)); data = []
    for p in PERMS:
        col = dict(colA); col.update({v: p[colB[v]] for v in B}); K = conflicts(T, A, col); data.append((len(K), p, col, K))
    data.sort(key=lambda t: t[0])
    for R in range(Rmax+1):
        for nk, p, col, K in data:
            d = multi_bfs(T.adj, list(K), allv); free = [v for v in range(n) if d.get(v,99) <= R]
            new = phased_repair(T, col, free)
            if new is not None:
                c2 = dict(col); c2.update(new); return dict(R=R, p=p, col=col, K=K, new=c2, data=data)
    return None

def phased_repair(T, col, free):
    from pysat.solvers import Glucose4
    fs = set(free); enc = CNF(sorted(fs))
    for v in fs:
        for w in T.adj[v]:
            if w in fs:
                if w > v: enc.neq(v, w)
            else: enc.cls.append([-enc.x(v, col[w])])
    s = Glucose4(bootstrap_with=enc.cls); s.set_phases([enc.x(v,c)*(1 if c==col[v] else -1) for v in enc.verts for c in range(4)])
    ok = s.solve()
    if not ok: s.delete(); return None
    mod = set(l for l in s.get_model() if l > 0); s.delete()
    return {v: next(c for c in range(4) if enc.x(v,c) in mod) for v in enc.verts}

def sdp(T, col, free, obj='zero', eps=1e-6, iters=20000):
    """Gram over 4 corners + free vertices; edges dot = -1/3; non-free neighbours pinned to corners of col.
       returns (status, X numpy or None, seconds)"""
    free = sorted(free); ix = {v: 4+j for j, v in enumerate(free)}; N = 4+len(free)
    X = cp.Variable((N,N), PSD=True); cons = [cp.diag(X) == 1, X[:4,:4] == G4]
    I, J, Ip, Cp = [], [], [], []
    for v in free:
        for w in T.adj[v]:
            if w in ix:
                if w > v: I.append(ix[v]); J.append(ix[w])
            else: Ip.append(col[w]); Cp.append(ix[v])
    if I: cons.append(X[I, J] == -1/3)
    if Ip: cons.append(X[Ip, Cp] == -1/3)
    if obj == 'old':
        o = cp.Maximize(cp.sum(X[[col[v] for v in free], [ix[v] for v in free]]))
    else: o = cp.Minimize(0)
    pr = cp.Problem(o, cons); t0 = time.time()
    try: pr.solve(solver='SCS', eps=eps, max_iters=iters)
    except BaseException as e:
        try: pr.solve(solver='CLARABEL')
        except BaseException: return 'error', None, time.time()-t0
    Xv = X.value if pr.status in ('optimal','optimal_inaccurate') else None
    return pr.status, Xv, time.time()-t0

def resid(T, col, free, Xv):
    """max violation of edge constraints, and of PSD (min eig) — feasibility sanity"""
    free = sorted(free); ix = {v: 4+j for j, v in enumerate(free)}; m = 0
    for v in free:
        for w in T.adj[v]:
            a = Xv[ix[v], ix[w]] if w in ix else Xv[col[w], ix[v]]
            m = max(m, abs(a+1/3))
    return m, float(np.linalg.eigvalsh((Xv+Xv.T)/2)[0])

def vec_metrics(free, Xv):
    free = sorted(free); out = {}
    for j, v in enumerate(free):
        d = Xv[:4, 4+j]; a = int(np.argmax(d))
        p = 0.75*(d @ TT)                       # projection onto the corner span
        out[v] = dict(near=a, dist=math.sqrt(max(0.0, 2-2*d[a])), proj=float(np.linalg.norm(p)), p=p)
    return out

def frame_angle(P):
    """P: 3x3 rows = projected vectors of a triangle. min over ordered corner triples of the Procrustes rotation angle."""
    best = 1e9
    for tri in itertools.permutations(range(4), 3):
        Q = TT[list(tri)]                       # want R with R q_i ~ p_i
        U, S, Vt = np.linalg.svd(P.T @ Q); D = np.diag([1,1,np.sign(np.linalg.det(U@Vt))])
        Rm = U@D@Vt; ang = math.degrees(math.acos(max(-1,min(1,(np.trace(Rm)-1)/2))))
        best = min(best, ang)
    return best

def seam_geometry(T, A, B, colA, p):
    cA = Cluster(T, A); cB = Cluster(T, B); n = len(T.adj); allv = set(range(n))
    # label every vertex by nearest A-walk index (multi-source BFS)
    lab = {}; dist = {}; q = collections.deque()
    for i, v in enumerate(cA.walk): lab[v] = i; dist[v] = 0; q.append(v)
    while q:
        v = q.popleft()
        for w in T.adj[v]:
            if w not in dist: dist[w] = dist[v]+1; lab[w] = lab[v]; q.append(w)
    return cA, cB, lab

def offset_profile(T, cA, cB, colA, colBp):
    """o(i) = H_A(u_i) - sigma*H_B(w) averaged over seam edges u_i w; best sigma and centre. returns per-A-walk-index |o-c|."""
    HA = cA.walk_heights(colA); HB = cB.walk_heights(colBp)
    hA = {v: HA[i] for i, v in enumerate(cA.walk)}; hB = {v: HB[i] for i, v in enumerate(cB.walk)}
    best = None
    for sg in (1, -1):
        o = {}
        for i, u in enumerate(cA.walk):
            ws = [w for w in T.adj[u] if w in hB]
            if ws: o[i] = np.mean([[hA[u][0]-sg*hB[w][0], hA[u][1]-sg*hB[w][1]] for w in ws], axis=0)
        arr = np.array(list(o.values()))
        # centre minimising max hex norm (grid search)
        cx = np.linspace(arr[:,0].min(), arr[:,0].max(), 25); cy = np.linspace(arr[:,1].min(), arr[:,1].max(), 25)
        nm = lambda d: np.sqrt(np.maximum(0,(d[:,0]**2+d[:,1]**2-d[:,0]*d[:,1])/4))
        r, c = min(((nm(arr-np.array([x,y])).max(), (x,y)) for x in cx for y in cy), key=lambda t: t[0])
        if best is None or r < best[0]: best = (r, c, o, sg)
    r, c, o, sg = best
    # reference = most frequent (rounded) offset: the value on which the two sides glue
    cc = collections.Counter(tuple(np.round(x).astype(int)) for x in o.values()); c = np.array(cc.most_common(1)[0][0], float)
    nm1 = lambda d: math.sqrt(max(0,(d[0]**2+d[1]**2-d[0]*d[1])/4))
    return dict(radius=r, sigma=sg, dev={i: nm1(o[i]-np.array(c)) for i in o})

# ---------------- Burer-Monteiro low-rank solver (fast; zero penalty = feasible SDP point, Gram of Y)
from scipy.optimize import minimize
def bm(T, col, free, d=12, init='rand', seed=0, iters=4000, Y0=None):
    free = sorted(free); ix = {v: j for j, v in enumerate(free)}; m = len(free)
    C = np.zeros((4, d)); C[:, :3] = TT
    I, J, Pv, Pc = [], [], [], []
    for v in free:
        for w in T.adj[v]:
            if w in ix:
                if w > v: I.append(ix[v]); J.append(ix[w])
            else: Pv.append(ix[v]); Pc.append(col[w])
    I, J, Pv, Pc = map(np.array, (I, J, Pv, Pc)); Cp = C[Pc]
    import scipy.sparse as sp
    ne = len(I); np_ = len(Pv)
    SI = sp.csr_matrix((np.ones(ne), (I, np.arange(ne))), shape=(m, ne)); SJ = sp.csr_matrix((np.ones(ne), (J, np.arange(ne))), shape=(m, ne))
    SP = sp.csr_matrix((np.ones(np_), (Pv, np.arange(np_))), shape=(m, np_))
    rng = np.random.default_rng(seed)
    if Y0 is not None: Z0 = Y0.copy()
    elif init == 'old': Z0 = C[[col[v] for v in free]] + 0.05*rng.standard_normal((m, d))
    else: Z0 = rng.standard_normal((m, d))
    def f(z):
        Z = z.reshape(m, d); nr = np.linalg.norm(Z, axis=1, keepdims=True); Y = Z/nr
        r1 = np.sum(Y[I]*Y[J], 1) + 1/3; r2 = np.sum(Y[Pv]*Cp, 1) + 1/3
        val = r1@r1 + r2@r2
        gY = SI@(2*r1[:, None]*Y[J]) + SJ@(2*r1[:, None]*Y[I]) + SP@(2*r2[:, None]*Cp)
        gZ = (gY - np.sum(gY*Y, 1, keepdims=True)*Y)/nr
        return val, gZ.ravel()
    res = minimize(f, Z0.ravel(), jac=True, method='L-BFGS-B', options=dict(maxiter=iters, ftol=1e-15, gtol=1e-10, maxcor=10))
    Z = res.x.reshape(m, d); Y = Z/np.linalg.norm(Z, axis=1, keepdims=True)
    return res.fun, Y, C

def bm_X(Y, C):
    """Gram-like block: corner dots (4 x m) in the same format as the SDP X[:4,4:]"""
    W = np.vstack([C, Y]); return W@W.T
