# W6 rule grammar: pictures (local patches), firing slots, rules = path x context, conservative per-slot pricing.
# A rule is (PATH, u-letter, v-letter, CONTEXT); CONTEXT = {position: allowed-letter bitmask}; unspecified = wildcard.
# A picture is a planar patch around a centre (a row of the LP): rotations of interior vertices + a letter set per vertex.
# A slot is one oriented firing of a path with the centre as an endpoint; it carries the letter sets of every position.
# Pricing (credit semantics, = engine's mrow design): each slot's 0/1 firing is chosen cert-favourably, i.e. the row's
# coefficient is the conservative one: an outflow is counted only if the context SURELY matches, an inflow if it POSSIBLY
# matches.  Each new rule carries its own receiver credit.  See PRIMITIVES.md.
import itertools, collections
import numpy as np
LET = (5, 6, 7, 8, 9)
BIT = {l: 1 << i for i, l in enumerate(LET)}
ALL = 31
CLS = {0: BIT[5] | BIT[6], 1: BIT[7] | BIT[8] | BIT[9]}
SYM = {'5': 1, '6': 2, '7': 4, '8': 8, '9': 16, 'S': 3, 'B': 28}       # context symbols (bitmasks); '*' = 31 = wildcard
SYMNAME = {v: k for k, v in SYM.items()}
def lb(x): return BIT[x]
def letters_of(m): return [l for l in LET if m & BIT[l]]
def msym(m): return SYMNAME.get(m, '{' + ''.join(str(l) for l in letters_of(m)) + '}') if m != ALL else '*'

class Pic:
    """planar patch: vertex 0 = centre; rot[v] = ccw neighbour list for interior v; let[v] = letter bitmask"""
    def __init__(self, kind, label):
        self.kind = kind; self.label = label; self.rot = {}; self.let = {}; self.n = 0
    def add(self, m):
        v = self.n; self.n += 1; self.let[v] = m; return v
def build(kind, label, d, link, apex, priv):
    """link: list of exact letters (len d); apex: list of bitmasks (len d), apex[i] between link i, i+1;
    priv: priv[i] = list of bitmasks for the privates of link i ordered from apex i-1 side to apex i side (len = letter-5)"""
    P = Pic(kind, label); c = P.add(BIT[min(d, 9)])
    L = [P.add(BIT[x]) for x in link]; A = [P.add(m) for m in apex]
    PV = [[P.add(m) for m in priv[i]] for i in range(d)]
    P.rot[c] = list(L)
    for i in range(d):
        P.rot[L[i]] = [c, L[(i - 1) % d], A[(i - 1) % d]] + PV[i] + [A[i], L[(i + 1) % d]]
    P.L, P.A, P.P, P.d = L, A, PV, d
    return P
def apex_of(P, a, b, x):
    """third vertex of the triangle on edge (a, b) not containing x; None if unknown"""
    for p, q in ((a, b), (b, a)):
        if p in P.rot:
            r = P.rot[p]; n = len(r)
            if q not in r: return None
            j = r.index(q); nb = (r[(j + 1) % n], r[(j - 1) % n])
            if nb[0] == x: return nb[1]
            if nb[1] == x: return nb[0]
            return None
    return None
def frame(P, x, y, sg):
    """link of interior x rooted at y in direction sg: (L, A) vertex lists (A[k] = apex of L[k], L[k+1] away from x)"""
    r = P.rot[x]; n = len(r); j = r.index(y)
    L = [r[(j + sg * k) % n] for k in range(n)]
    A = [apex_of(P, L[k], L[(k + 1) % n], x) for k in range(n)]
    return L, A
def lt(P, v): return ALL if v is None else P.let[v]
# ---------------- EDGE slots ----------------
EPOS = ['S.L+1', 'S.L+2', 'S.L+3', 'S.L-1', 'S.L-2', 'S.L-3', 'S.A+1', 'S.A-1', 'R.L+2', 'R.L+3', 'R.L-2', 'R.L-3', 'R.A+1', 'R.A-1']
EMIRROR = [3, 4, 5, 0, 1, 2, 7, 6, 10, 11, 8, 9, 13, 12]
def edge_vec(P, u, v, sg):
    """position letter masks for the oriented edge u -> v (u, v both interior or known); orientation sg at u"""
    if u not in P.rot or v not in P.rot: return None
    SL, SA = frame(P, u, v, sg)
    for sv in (1, -1):
        RL, RA = frame(P, v, u, sv)
        if RL[1] == SL[1]: break
    else: raise AssertionError('frame orientation')
    du, dv = len(SL), len(RL)
    g = lambda arr, k, d: arr[k % d]
    vec = [g(SL, 1, du), g(SL, 2, du), g(SL, 3, du), g(SL, -1, du), g(SL, -2, du), g(SL, -3, du), g(SA, 1, du), g(SA, -2, du),
           g(RL, 2, dv), g(RL, 3, dv), g(RL, -2, dv), g(RL, -3, dv), g(RA, 1, dv), g(RA, -2, dv)]
    return [lt(P, z) for z in vec]
# ---------------- HAT slots (u -> b across the edge x y; b = the other apex of xy) ----------------
HPOS = ['X', 'Y', 'U-1', 'U+1', 'XA', 'YA', 'V-1', 'V+1']
HMIRROR = [1, 0, 3, 2, 5, 4, 7, 6]
def hat_vec(P, u, x, y, b):
    """X, Y spokes; U-1 = apex(u,x) away from y; U+1 = apex(u,y) away from x; XA = x's next link vertex after U-1 (away from u);
    YA likewise; V-1 = apex(b,x) away from y; V+1 = apex(b,y) away from x"""
    um = apex_of(P, u, x, y); up = apex_of(P, u, y, x)
    vm = apex_of(P, b, x, y); vp = apex_of(P, b, y, x)
    xa = apex_of(P, x, um, u) if um is not None else None
    ya = apex_of(P, y, up, u) if up is not None else None
    return [lt(P, z) for z in (x, y, um, up, xa, ya, vm, vp)]
def slots(P):
    """all firing slots of picture P (centre 0).  Each slot: (path, role, uL, vL, vec, sign); role 'out': the centre pays,
    'in': the centre is paid.  sign = the slot's coefficient sign in the centre's row: a sender row (kind S) reads
    outflow - inflow (>= 1 - t), every other row reads inflow - outflow (receiver <= d - 6 + t; a 6: = 0)."""
    out = []; c = 0
    so = 1 if P.kind == 'S' else -1; si = -so
    for v in P.rot[c]:
        for sg in (1, -1):
            out.append(('EDGE', 'out', P.let[c], P.let[v], edge_vec(P, c, v, sg), so))
            out.append(('EDGE', 'in', P.let[v], P.let[c], edge_vec(P, v, c, sg), si))
    L = P.rot[c]; d = len(L)
    for k in range(d):
        x, y = L[k], L[(k + 1) % d]; b = apex_of(P, x, y, c)
        if b is None: continue
        for (xx, yy) in ((x, y), (y, x)):
            out.append(('HAT', 'out', P.let[c], P.let[b], hat_vec(P, c, xx, yy, b), so))
            out.append(('HAT', 'in', P.let[b], P.let[c], hat_vec(P, b, xx, yy, c), si))   # payer = the apex b
    return out
class SlotTable:
    """numpy arrays of all slots per path; with_dual(y) gives the pricing view (a = sign * y[row], zero-dual rows dropped).
    items: iterable of (rowid, slot); converted in chunks to keep memory low."""
    KEYS = ('rid', 'out', 'uL', 'vL', 'V', 's')
    def __init__(self, items, chunk=200000):
        buf = collections.defaultdict(list); parts = collections.defaultdict(list)
        def flush(path):
            lst = buf[path]
            if not lst: return
            parts[path].append(dict(rid=np.array([x[0] for x in lst], dtype=np.int64), out=np.array([x[1] == 'out' for x in lst]),
                                    uL=np.array([x[2] for x in lst], dtype=np.uint8), vL=np.array([x[3] for x in lst], dtype=np.uint8),
                                    V=np.array([x[4] for x in lst], dtype=np.uint8), s=np.array([x[5] for x in lst], dtype=np.int8)))
            buf[path] = []
        for rid, (path, role, uL, vL, vec, sgn) in items:
            if vec is None: continue
            buf[path].append((rid, role, uL, vL, vec, sgn))
            if len(buf[path]) >= chunk: flush(path)
        for path in list(buf): flush(path)
        self.G = {}
        for path, ps in parts.items():
            self.G[path] = {k: np.concatenate([p[k] for p in ps]) for k in self.KEYS}
            self.G[path]['s'] = self.G[path]['s'].astype(float)
    def with_dual(self, y, tol=1e-13):
        y = np.asarray(y, dtype=float); out = SlotTable([])
        for path, g in self.G.items():
            a = g['s'] * y[g['rid']]; keep = np.abs(a) > tol
            out.G[path] = {k: v[keep] for k, v in g.items()}; out.G[path]['a'] = a[keep]
        return out
def match(G, um, vm, ctx):
    """sure / possible boolean arrays for rule (um, vm endpoint masks, ctx = {pos index: mask})"""
    um, vm = np.uint8(um), np.uint8(vm); nu, nv = np.uint8(31 & ~int(um)), np.uint8(31 & ~int(vm))
    sure = ((G['uL'] & nu) == 0) & ((G['vL'] & nv) == 0)
    poss = ((G['uL'] & um) != 0) & ((G['vL'] & vm) != 0)
    for p, m in ctx.items():
        col = G['V'][:, p]; m8 = np.uint8(m); n8 = np.uint8(31 & ~m)
        sure &= (col & n8) == 0; poss &= (col & m8) != 0
    return sure, poss
def price(G, um, vm, ctx):
    """tot = A^T y of the rule's column (> 0 = improving) with the LP's conservative coefficients (an outflow slot counts
    only if the context SURELY matches, an inflow slot if it POSSIBLY matches), and the branch-and-bound upper bound over
    every refinement of ctx (refining can only switch slots off)."""
    sure, poss = match(G, um, vm, ctx)
    on = np.where(G['out'], sure, poss)
    a = G['a']
    return float(a[on].sum()), float(np.maximum(a[on], 0.0).sum()), sure, poss
def coef_rows(G, um, vm, ctx, nrows):
    """the rule's LP column: per-row coefficient (row ids in G['rid']); G['s'] = +1/-1 sign of the slot in its row"""
    sure, poss = match(G, um, vm, ctx)
    on = np.where(G['out'], sure, poss)
    return np.bincount(G['rid'][on], weights=G['s'][on], minlength=nrows)
def rule_str(path, um, vm, ctx):
    names = EPOS if path == 'EDGE' else HPOS
    s = '%s(%s->%s)' % (path, msym(um), msym(vm))
    if ctx: s += '[' + ' '.join('%s=%s' % (names[p], msym(m)) for p, m in sorted(ctx.items())) + ']'
    return s
def canon_ctx(path, ctx):
    mir = EMIRROR if path == 'EDGE' else HMIRROR
    a = tuple(sorted(ctx.items())); b = tuple(sorted((mir[p], m) for p, m in ctx.items()))
    return min(a, b)
