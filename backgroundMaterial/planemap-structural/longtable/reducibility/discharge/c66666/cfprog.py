"""Job 20 (Studio, exploratory): a Python transcription of fourcolor's configuration construction programs
(cfmap.v: cpmap0, ecpU, ecpN, ecpR, ecpR', ecpK, ecpY = N.U, ecpH = N.Y; cfcontract.v: ctrenum), used only to
find and describe a cprog for the 66666 wheel.  The Coq build is the authority; this file is a search aid.
A map is (edge, node, face) dicts on integer darts plus a pointer; old darts keep their ids (icp* = identity)."""
import itertools


class Map:
    def __init__(self, e, n, f, x0):
        self.e, self.n, self.f, self.x0 = e, n, f, x0

    def order_node(self, x):
        k, y = 1, self.n[x]
        while y != x: k, y = k + 1, self.n[y]
        return k

    def cpring(self):          # rev (orbit node (node (node x0)))
        z = self.n[self.n[self.x0]]; orb = [z]; y = self.n[z]
        while y != z: orb.append(y); y = self.n[y]
        return orb[::-1]

    def faces(self):
        seen, out = set(), []
        for x in self.f:
            if x in seen: continue
            orb = [x]; y = self.f[x]
            while y != x: orb.append(y); y = self.f[y]
            seen.update(orb); out.append(orb)
        return out


def base():
    return Map({0: 1, 1: 0}, {0: 1, 1: 0}, {0: 0, 1: 1}, 1)   # darts true=1, false=0


def _fresh(G):
    m = max(G.e) + 1
    return m, m + 1


def U(G):
    X, Xe = _fresh(G); x0 = G.x0; nx0 = G.n[x0]
    e = dict(G.e); e[X] = Xe; e[Xe] = X
    n = {X: Xe, Xe: G.n[nx0]}
    for y in G.n: n[y] = X if y == nx0 else G.n[y]
    f = {X: X, Xe: nx0}
    for y in G.f: f[y] = Xe if G.f[y] == nx0 else G.f[y]
    return Map(e, n, f, X)


def N(G):
    X, Xe = _fresh(G); x0 = G.x0; ex0 = G.e[x0]; nx0 = G.n[x0]
    long = G.f[ex0] != nx0
    e = dict(G.e); e[X] = Xe; e[Xe] = X
    n = {X: (nx0 if long else X), Xe: G.f[ex0]}
    for y in G.n:
        n[y] = Xe if y == x0 else (X if G.n[G.n[y]] == x0 else G.n[y])
    f = {X: x0, Xe: (G.f[G.e[G.f[ex0]]] if long else X)}
    for y in G.f:
        f[y] = Xe if y == G.e[G.f[ex0]] else (X if y == G.e[nx0] else G.f[y])
    return Map(e, n, f, X)


def R(G, k):
    o = G.order_node(G.x0); x = G.x0
    for _ in range(max(o - k, 0)): x = G.n[x]
    return Map(G.e, G.n, G.f, x)


def Rp(G): return R(G, G.order_node(G.x0) - 1)
def Y(G): return N(U(G))
def H(G): return N(Y(G))
def K(G): return R(N(Rp(G)), 1)


def parse(s):
    """'Config* 1 2 H 2 H Y' or a bare program 'H 2 H Y' -> (sym, contract list, steps)."""
    t = s.split(); sym = False
    if t and t[0].startswith('Config'):
        sym = t[0].endswith('*') or (len(t) > 1 and t[1] == '*'); t = t[1:] if t[0] != 'Config' or t[1] != '*' else t[2:]
        if t and t[0] == '*': t = t[1:]
    cc = []
    while t and t[0].isdigit(): cc.append(int(t.pop(0)))
    steps = [int(x) if x.isdigit() else x for x in t]
    return sym, cc[::-1], steps            # Config stores rev cc


def run(steps):
    """Interpret right-to-left; return the map and ctrenum (kernel-edge transversal, cfcontract.v order)."""
    G = base(); enum = []
    rest = []
    for s in reversed(steps):
        if isinstance(s, int): G = R(G, s)
        elif s == "R'": G = Rp(G)
        elif s == 'Y':
            nG = Y(G)
            enum = [] if not rest else [G.n[G.x0]] + enum
            G = nG
        elif s == 'H':
            nG = H(G)
            enum = [nG.f[nG.x0], G.n[G.x0], G.x0] + enum
            G = nG
        elif s == 'U': G = U(G)
        elif s == 'K': G = K(G)
        else: raise ValueError(s)
        rest.append(s)
    return G, enum


def describe(G):
    ring = G.cpring(); rs = set(ring)
    F = G.faces(); fid = {x: i for i, fc in enumerate(F) for x in fc}
    ringf = sorted({fid[x] for x in ring})
    kern = [i for i in range(len(F)) if i not in ringf]
    adj = {i: set() for i in range(len(F))}
    for x in G.e: adj[fid[x]].add(fid[G.e[x]])
    return F, fid, ring, ringf, kern, adj
