"""State test: does (height, dual Kempe trace per Tait pair, chain parity) on every collar row determine
whether the window-k0 collar target is UNSAT (obstructing)?"""
import sys, json, random, time, itertools, math, os
KT = '/mnt/project-files/multiscale/kempe_trace'
sys.path.insert(0, KT); sys.path.insert(0, '/mnt/project-files/multiscale/opus_attack/bandfill'); sys.path.insert(0, '/mnt/project-files/multiscale/hodge')
from kt import traces, PAIRS
from collar import Collar, depth_in
from t2_tubes import annulus, sat_colour
from minbad import extend_below
from pairrow import pair as height_pair

def unsat(adj, S, col, bd, w, k0):
    C = Collar(adj, S, col, bd, w); C.target_window(k0); return C.solve() is None

# ---------- dual Kempe trace -----------------------------------------------------------
def tri_list(adj, S):
    S = set(S); out = []
    for u in S:
        for v in adj[u]:
            if v > u and v in S:
                for x in adj[u] & adj[v]:
                    if x > v and x in S: out.append((u, v, x))
    return out

def dual_trace(adj, R, col, row, tris):
    """R: region (set), row: ordered list of the row's vertices (outer boundary of R, cyclic).
    Returns per gamma in (1,2,3): (pairing tuple, parity tuple, n_closed) where pairing[i] = partner port index of port i
    (port i = edge row[i]-row[i+1]), -1 if port i is not a gamma-pair port, 'I' (=-2) if path ends on another boundary.
    parity[i] = number of triangles on the path mod 2 (-1 if not a port)."""
    R = set(R); T = [t for t in tris if t[0] in R and t[1] in R and t[2] in R]
    e2t = {}
    for k, (a, b, c) in enumerate(T):
        for e in ((a, b), (a, c), (b, c)): e2t.setdefault(frozenset(e), []).append(k)
    L = len(row); pidx = {frozenset((row[i], row[(i+1) % L])): i for i in range(L)}
    lab = lambda e: col[min(e)] ^ col[max(e)]
    out = {}
    for g in (1, 2, 3):
        partner = [-1]*L; par = [-1]*L; seen_t = set()
        for i in range(L):
            e = frozenset((row[i], row[(i+1) % L]))
            if lab(tuple(e)) == g or partner[i] != -1: continue
            ts = e2t.get(e, [])
            assert len(ts) == 1, ('port not on exactly one triangle', len(ts))
            cur_e, t, n = e, ts[0], 0
            while True:
                seen_t.add(t); n += 1
                a, b, c = T[t]
                nxt = [f for f in (frozenset((a, b)), frozenset((a, c)), frozenset((b, c))) if f != cur_e and lab(tuple(f)) != g]
                assert len(nxt) == 1
                f = nxt[0]; ts2 = [s for s in e2t[f] if s != t]
                if not ts2:
                    j = pidx.get(f, -2)
                    partner[i] = j; par[i] = n % 2
                    if j >= 0: partner[j] = i; par[j] = n % 2
                    break
                cur_e, t = f, ts2[0]
        # closed cycles
        ncl = 0
        for t0 in range(len(T)):
            if t0 in seen_t: continue
            # walk the cycle through t0 if it is closed
            a, b, c = T[t0]; es = [f for f in (frozenset((a, b)), frozenset((a, c)), frozenset((b, c))) if lab(tuple(f)) != g]
            cur_e, t, path = es[0], t0, []
            ok = True
            while True:
                seen_t.add(t); path.append(t)
                a, b, c = T[t]
                f = [h for h in (frozenset((a, b)), frozenset((a, c)), frozenset((b, c))) if h != cur_e and lab(tuple(h)) != g][0]
                ts2 = [s for s in e2t[f] if s != t]
                if not ts2: ok = False; break
                if ts2[0] == t0: break
                cur_e, t = f, ts2[0]
            if ok: ncl += 1
        out[g] = (tuple(partner), tuple(par), ncl)
    return out

# ---------- canonicalisation -----------------------------------------------------------
LABPERM = list(itertools.permutations((1, 2, 3)))
def transform_row(dt, L, rot, refl, lp):
    """apply port map i -> refl*i(+shift) and label permutation lp (g -> lp[g-1])."""
    # port i = edge (i, i+1); reflection c -> -c maps it to edge (-i-1, -i) = port (-i-1)
    pm = (lambda i: (i + rot) % L) if refl == 1 else (lambda i: (-i - 1 + rot) % L)
    new = {}
    for g, (partner, par, ncl) in dt.items():
        P = [-1]*L; Q = [-1]*L
        for i in range(L):
            j = partner[i]; P[pm(i)] = pm(j) if j >= 0 else j; Q[pm(i)] = par[i]
        new[lp[g-1]] = (tuple(P), tuple(Q), ncl)
    return tuple(new[g] for g in (1, 2, 3))

def canon(rows_dt, L, keep=lambda x: x):
    """rows_dt: list over rows of dual traces. Joint canonical form under one global symmetry."""
    best = None
    for rot in range(L):
        for refl in (1, -1):
            for lp in LABPERM:
                key = tuple(keep(transform_row(dt, L, rot, refl, lp)) for dt in rows_dt)
                if best is None or key < best: best = key
    return best

def strip_parity(t): return tuple((P, ncl) for P, Q, ncl in t)

# ---------- experiments ----------------------------------------------------------------
def tube_setup(c, side):
    L = c['L']
    rows = c['A_rows_depth_w_to_seam'] if side == 'A' else [r[::-1] for r in reversed(c['B_rows_seam_to_depth_w'])]
    rows = extend_below(rows[0], 2) + rows
    adj, col = annulus(rows); n = len(col); seam = len(rows) - 1
    rowv = lambda r: [(seam - r)*L + i for i in range(L)]
    region = lambda r: {v for v in range(n) if v // L <= seam - r}
    depth = {v: seam - v // L for v in range(n)}
    return dict(L=L, adj=adj, col={v: col[v] for v in range(n)}, S=set(range(n)), bd=rowv(0), rowv=rowv, region=region,
                depth=depth, coord={v: (seam - v // L, v % L) for v in range(n)}, maxrow=seam)

def opus_setup(side):
    d = json.load(open('/mnt/project-files/multiscale/opus_attack/bandfill/sphere_L18_w4.json'))
    adj = [set(a) for a in d['adj']]; L = 18; n = len(adj); A = set(d['A']); B = set(range(n)) - A; m = d['seam_row_A']
    ntube = 26*L
    if side == 'A':
        S = A; col = {int(k): v for k, v in d['colA'].items()}
        rowv = lambda r: [(m - r)*L + i for i in range(L)]
        region = lambda r: {v for v in S if v >= ntube or v // L <= m - r}
        coord = {v: ((m - v // L, v % L) if v < ntube else (99, v)) for v in S}
    else:
        S = B; col = {int(k): v for k, v in d['colB'].items()}
        rowv = lambda r: [(m + 1 + r)*L + i for i in range(L)]
        region = lambda r: {v for v in S if v >= ntube or v // L >= m + 1 + r}
        coord = {v: ((v // L - (m+1), v % L) if v < ntube else (99, v)) for v in S}
    depth = {v: coord[v][0] for v in S}
    return dict(L=L, adj=adj, col=col, S=S, bd=rowv(0), rowv=rowv, region=region, depth=depth, coord=coord, maxrow=99)

def state(E, col, w, tris):
    L = E['L']; rows = []; H = []
    for r in range(w + 1):
        rv = E['rowv'](r); R = E['region'](r)
        rows.append(dual_trace(E['adj'], R, col, rv, tris))
        tt, th = height_pair([col[v] for v in rv]); H.append((round(tt, 4), round(th, 4)))
    return rows, H

def parity_check(rows, E, col):
    """[P] check: parity of a dual chain = [end-port labels differ]."""
    L = E['L']; bad = 0; tot = 0
    for r, dt in enumerate(rows):
        rv = E['rowv'](r); lab = [col[rv[i]] ^ col[rv[(i+1) % L]] for i in range(L)]
        for g, (P, Q, ncl) in dt.items():
            for i in range(L):
                if P[i] >= 0:
                    tot += 1; bad += (Q[i] != (lab[i] != lab[P[i]]))
    return bad, tot

def keys(rows, H, L, w):
    K = {}
    K['height_row0'] = H[0]
    K['height_all'] = tuple(H)
    K['trace_row0'] = canon(rows[:1], L)
    K['trace_row0+h'] = (K['trace_row0'], H[0])
    K['trace_roww'] = canon(rows[w:w+1], L)
    K['trace_rows0,w'] = canon([rows[0], rows[w]], L)
    K['trace_deep_1..w'] = canon(rows[1:], L)
    K['trace_all_indep'] = tuple(canon([dt], L) for dt in rows)
    for r in range(1, w):
        K[f'prefix_0..{r}'] = (canon(rows[:r+1], L), tuple(H[:r+1]))
    K['FULL'] = (canon(rows, L), tuple(H))
    K['FULL_noparity'] = (canon(rows, L, strip_parity), tuple(H))
    return K

from pysat.solvers import Cadical153
def sampler(adj, S, fixed, rng):
    vs = sorted(S); ix = {v: k for k, v in enumerate(vs)}; x = lambda v, c: 4*ix[v] + c + 1; cls = []
    for v in vs:
        cls.append([x(v, c) for c in range(4)])
        for c in range(4):
            for c2 in range(c+1, 4): cls.append([-x(v, c), -x(v, c2)])
        for u in adj[v]:
            if u in ix and u > v:
                for c in range(4): cls.append([-x(v, c), -x(u, c)])
    s = Cadical153(bootstrap_with=cls); ass = [x(v, c) for v, c in fixed.items()]
    if not s.solve(assumptions=ass): s.delete(); return None
    free = [v for v in vs if v not in fixed]; rng.shuffle(free)
    for v in free:
        cs = list(range(4)); rng.shuffle(cs)
        for c in cs:
            if s.solve(assumptions=ass + [x(v, c)]): ass.append(x(v, c)); break
    s.solve(assumptions=ass); mod = set(l for l in s.get_model() if l > 0); s.delete()
    return {v: next(c for c in range(4) if x(v, c) in mod) for v in vs}

