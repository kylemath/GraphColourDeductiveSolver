"""B1 window generator. 2-ball of a receiver row (d, LK, SV) at exact degrees, plus optional extra vertices:
  privates p (ring-2 vertex adjacent to one link vertex) and ring-3 vertices t, each at a given degree.
windows(...) enumerates connected subsets S of the fixed-degree vertices (u, w_i, s_i, extras) that contain every vertex of `must`,
with ring (N(S)-S a simple induced cycle) <= RMAX; returns kc lines plus a rotation-canonical code (dedupe up to reflection)."""
import sys, os, hashlib
W = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge'
sys.path.insert(0, os.path.join(W, 'b8b')); sys.path.insert(0, W)
from rings import Layered
def adjof(L):
    adj = {}
    for a, b, c in L.tris:
        for x, y in ((a, b), (b, c), (c, a)): adj.setdefault(x, set()).add(y); adj.setdefault(y, set()).add(x)
    return adj
def build(LK, SV, pdeg=None, tdeg=None):
    """pdeg: {('p',i,c): deg}; tdeg: {k: deg} with k an index into the ring-3 list (as built with the given pdeg).
    returns adj, rot, name(dict vertex->name), deg(dict name->degree for fixed vertices), Z3, nameinv"""
    pdeg = pdeg or {}; tdeg = tdeg or {}
    D = len(LK); L = Layered(D); L.add_ring([int(c) for c in LK])
    Wr = L.rings[1]; Z = L.ring(); adj = adjof(L)
    name = {0: ('u',)}
    for i, w in enumerate(Wr): name[w] = ('w', i)
    Wi = {w: i for i, w in enumerate(Wr)}; cnt = {}
    for z in Z:
        ws = sorted(Wi[x] for x in adj[z] if x in Wi)
        if len(ws) == 2:
            i, j = ws; name[z] = ('s', j if (i, j) == (0, D - 1) else i)
        else:
            i = ws[0]; cnt[i] = cnt.get(i, 0) + 1; name[z] = ('p', i, cnt[i])
    deg = {('u',): D}
    for i in range(D): deg[('w', i)] = int(LK[i]); deg[('s', i)] = int(SV[i])
    for k, v in pdeg.items(): deg[k] = v
    L.add_ring([deg.get(name[z], 9) for z in Z]); Z3 = list(L.ring())
    if not tdeg:
        L.add_ring([9 for z in Z3])
    else:
        assert len(tdeg) == 1
        (k, td), = tdeg.items(); t = Z3[k]; name[t] = ('t', k)
        o = td - L.inn[t] - 2
        if o < 0: raise ValueError('impossible: t has %d inner nbrs' % L.inn[t])
        deg[('t', k)] = td
        if o == 0:
            R = L.rings[-1]; j = R.index(t); a = R[(j - 1) % len(R)]; b = R[(j + 1) % len(R)]
            L.tris.append((a, t, b)); L.inn[a] += 1; L.inn[b] += 1; L.deg[t] = td; R.remove(t)
            L.add_ring([9 for z in R])
        else:
            L.add_ring([td if z == t else 9 for z in Z3])
    adj = adjof(L); rot = rotof(L)
    inv = {v: x for x, v in name.items()}
    for nm, dg in deg.items():
        assert len(adj[inv[nm]]) == dg, (nm, len(adj[inv[nm]]), dg)
    return adj, rot, name, deg, Z3, inv
def rotof(L):
    nxt = {}
    for a, b, c in L.tris:
        for x, y, z in ((a, b, c), (b, c, a), (c, a, b)): nxt.setdefault(x, {})[y] = z
    rot = {}
    for x, mp in nxt.items():
        preds = set(mp.values()); starts = [y for y in mp if y not in preds]
        s = starts[0] if starts else next(iter(mp)); r = [s]; y = mp.get(s)
        while y is not None and y != s: r.append(y); y = mp.get(y)
        rot[x] = r
    return rot
def ring3_candidates(LK, SV, pdeg=None):
    adj, rot, name, deg, Z3, inv = build(LK, SV, pdeg)
    return [(k, sorted((name[y] for y in adj[t] if y in name), key=str)) for k, t in enumerate(Z3)]
def ringcycle(adj, Is):
    RS = set(y for x in Is for y in adj[x]) - Is
    for y in RS:
        if len(adj[y] & RS) != 2: return None
    start = min(RS); order = [start]; prev = None
    while True:
        cur = order[-1]; nb = sorted(adj[cur] & RS); nxt = nb[0] if nb[0] != prev else nb[1]
        if nxt == start: break
        order.append(nxt); prev = cur
    if len(order) != len(RS): return None
    return order
def canon_code(adj, rot, Is, order):
    Vp = Is | set(order); r = len(order); best = None
    for i in range(r):
        a = order[i]
        for b in (order[(i + 1) % r], order[(i - 1) % r]):
            for mir in (0, 1):
                lab = {a: 0, b: 1}; seq = [a, b]; ref = {a: b, b: a}; out = []; k = 0
                while k < len(seq):
                    x = seq[k]; nb = [y for y in rot[x] if y in Vp]
                    if mir: nb = nb[::-1]
                    j = nb.index(ref[x]); nb = nb[j:] + nb[:j]
                    for y in nb:
                        if y not in lab: lab[y] = len(seq); seq.append(y); ref[y] = x
                    out.append((1 if x in Is else 0,) + tuple(lab[y] for y in nb)); k += 1
                c = tuple(out)
                if best is None or c < best: best = c
    return hashlib.md5(repr(best).encode()).hexdigest()[:20]
def kcline(nm, adj, Is, order):
    ri = {y: j for j, y in enumerate(order)}; Il = sorted(Is); ii = {x: j for j, x in enumerate(Il)}
    f = lambda Ls: ';'.join(','.join(map(str, v)) if v else '-' for v in Ls)
    ia = [sorted(ii[y] for y in adj[x] if y in Is) for x in Il]
    ra = [sorted(ri[y] for y in adj[x] if y in ri) for x in Il]
    return '%s %d %d %s %s' % (nm, len(order), len(Il), f(ra), f(ia))
def wname(LK, SV, Snames, extras):
    D = len(LK); u = 'u' if ('u',) in Snames else '-'
    lw = ''.join(LK[j] if ('w', j) in Snames else '.' for j in range(D)); ls = ''.join(SV[j] if ('s', j) in Snames else '.' for j in range(D))
    ex = '_'.join('%s%s%d' % (x[0], ''.join(map(str, x[1:])), dg) for x, dg in extras if x in Snames)
    return 'b%d_%s%s_%s%s' % (D, u, lw, ls, ('_' + ex) if ex else '')
def windows(LK, SV, pdeg=None, tdeg=None, RMAX=14, must=(), MMAX=16, allowed=None, minscore=None):
    """all connected subsets of fixed-degree vertices containing `must` (names), ring <= RMAX. allowed: optional set of names."""
    adj, rot, name, deg, Z3, inv = build(LK, SV, pdeg, tdeg)
    D = len(LK)
    V = [nm for nm in deg if (allowed is None or nm in allowed)]
    Vs = set(V); nb = {x: {name[y] for y in adj[inv[x]] if name.get(y) in Vs} for x in V}
    extras = [(k, v) for k, v in deg.items() if k[0] in 'pt']
    out = {}
    must = list(must)
    def emit(S):
        if len(S) < 2: return
        Is = set(inv[x] for x in S)
        order = ringcycle(adj, Is)
        if order is None or len(order) > RMAX: return
        if minscore is not None:
            sc = sum(1 for x in S if deg[x] == 5) - sum(1 for x in S if deg[x] >= 7)
            if sc < minscore.get(len(order), -99): return
        code = canon_code(adj, rot, Is, order)
        if code in out: return
        nm = wname(LK, SV, S, extras)
        out[code] = (len(order), len(S), nm, kcline(nm, adj, Is, order), sum(1 for x in S if deg[x] == 5))
    # enumerate connected sets containing root = must[0] (or every vertex if no must), each exactly once
    roots = [must[0]] if must else V
    idx = {x: i for i, x in enumerate(V)}
    for r0 in roots:
        forb0 = set() if must else {x for x in V if idx[x] < idx[r0]}
        def rec(S, front, forb):
            if all(m in S for m in must): emit(S)
            if len(S) >= MMAX: return
            front = list(front); forb = set(forb)
            for y in sorted(front, key=lambda z: idx[z]):
                forb.add(y)
                nf = (set(front) | nb[y]) - S - {y} - forb
                rec(S | {y}, nf - forb, forb)
        rec(frozenset([r0]), nb[r0] - forb0, forb0 | {r0})
    return sorted(out.items(), key=lambda kv: (kv[1][0], -kv[1][1]))
if __name__ == '__main__':
    import time
    LK, SV, R = sys.argv[1], sys.argv[2], int(sys.argv[3])
    t = time.time(); ws = windows(LK, SV, RMAX=R)
    import collections
    print(len(ws), sorted(collections.Counter(v[0] for k, v in ws).items()), '%.1fs' % (time.time() - t))
