"""EXPLORE round 42 (Long Table, 11:29Z): defect-style growth of R* by one ring.  R* = d7 link 5675765, s 6.77.75 with
(s1, s4) in {6,7,8,9+}^2; the ring grown is the six privates of the non-5 link vertices (p1 of w1, p2a/p2b of w2,
p4a/p4b of w4, p5 of w5), each 5..9 (9 = degree >= 9, never an exact match).  250,000 closed cases.
Forbidden set: RSST's 633 (unavoidable.conf) + explore's 12 two-engine kills (Job 30 twoeng: 3 D, 9 C).
Containment (own code, as loop/d3/d3_rsst.py): injective map of the configuration's interior into the 2-ball's 21
exact-degree vertices, exact degrees, induced, interior triangles onto faces.  Embeddings are enumerated once on the
2-ball's structure (which does not depend on the letters), giving degree requirements on the 8 variable slots.
Writes k42/hits.txt (config, slot requirements, cut window as a kc line), k42/cases.txt (survivors per filling).
usage: python3 grow.py"""
import sys, os, itertools, collections
H = os.path.dirname(os.path.abspath(__file__)); W = os.path.normpath(os.path.join(H, '..', '..'))
DIS = os.path.dirname(W); sys.path.insert(0, os.path.join(DIS, 'b8b')); sys.path.insert(0, DIS)
from rings import Layered
CONF = os.path.normpath(os.path.join(DIS, '..', '..', '..', 'studiointel', 'routeb', 'rsst', 'unavoidable.conf'))
D, LK, SV = 7, [5, 6, 7, 5, 7, 6, 5], {0: 6, 2: 7, 3: 7, 5: 7, 6: 5}
VAR = [('s', 1), ('s', 4), ('p', 1, 1), ('p', 2, 1), ('p', 2, 2), ('p', 4, 1), ('p', 4, 2), ('p', 5, 1)]
LET = [5, 6, 7, 8, 9]

def build2(r2):
    """gen.build plus faces: u's 2-ball (link LK, ring-2 letters r2 by name, unspecified = 9) with a fresh ring 3."""
    L = Layered(D); L.add_ring(list(LK))
    Wr = L.rings[1]; Z = L.ring(); adj = {}
    for a, b, c in L.tris:
        for x, y in ((a, b), (b, c), (c, a)): adj.setdefault(x, set()).add(y); adj.setdefault(y, set()).add(x)
    name = {0: ('u',)}
    for i, w in enumerate(Wr): name[w] = ('w', i)
    Wi = {w: i for i, w in enumerate(Wr)}; cnt = {}
    for z in Z:
        ws = sorted(Wi[x] for x in adj[z] if x in Wi)
        if len(ws) == 2:
            i, j = ws; name[z] = ('s', j if (i, j) == (0, D - 1) else i)
        else:
            i = ws[0]; cnt[i] = cnt.get(i, 0) + 1; name[z] = ('p', i, cnt[i])
    L.add_ring([r2.get(name[z], 9) for z in Z])
    adj = {}
    for a, b, c in L.tris:
        for x, y in ((a, b), (b, c), (c, a)): adj.setdefault(x, set()).add(y); adj.setdefault(y, set()).add(x)
    return adj, name, {frozenset(t) for t in L.tris}

def letters(a, b, p):
    r2 = {('s', j): v for j, v in SV.items()}; r2[('s', 1)] = a; r2[('s', 4)] = b
    for k, nm in enumerate(VAR[2:]): r2[nm] = p[k]
    return r2

def structure():
    """P = the 21 exact-degree vertices; their induced adjacency and the faces among them, checked letter-independent."""
    ref = None
    for a, b, p in ((6, 6, (6,) * 6), (9, 8, (5, 9, 7, 8, 5, 6)), (7, 9, (9,) * 6)):
        adj, name, faces = build2(letters(a, b, p))
        inv = {v: x for x, v in name.items()}
        assert set(VAR) <= set(inv), sorted(inv)
        P = [x for x in inv]                    # names
        pa = {x: {name[y] for y in adj[inv[x]] if y in name} for x in P}
        pf = {frozenset(name[y] for y in f) for f in faces if all(y in name for y in f)}
        if ref is None: ref = (P, pa, pf)
        else: assert ref[1] == pa and ref[2] == pf
    return ref

def fixed_deg():
    fd = {('u',): D}
    for i in range(D): fd[('w', i)] = LK[i]
    for j, v in SV.items(): fd[('s', j)] = v
    return fd

def rsst():
    C = []; lines = open(CONF).read().split('\n'); i = 0
    while i < len(lines):
        if not lines[i].strip(): i += 1; continue
        nm = lines[i].strip(); f = lines[i + 1].split(); n, r = int(f[0]), int(f[1]); i += 3
        nb = {}
        for _ in range(n):
            f = lines[i].split(); nb[int(f[0])] = [int(x) for x in f[2:]]; i += 1
        while i < len(lines) and lines[i].strip(): i += 1
        U = list(range(r + 1, n + 1)); g = {u: len(nb[u]) for u in U}
        E = {u: {w for w in nb[u] if w > r} for u in U}; tri = set()
        for u in U:
            L_ = nb[u]
            for k in range(len(L_)):
                x, y = L_[k], L_[(k + 1) % len(L_)]
                if x > r and y > r: tri.add(frozenset((u, x, y)))
        C.append(('rsst%03d' % len(C), 'RSST ' + nm, U, g, E, tri))
    return C

def kcline(line, tag):
    f = line.split(); m = int(f[2]); rp = f[3].split(';'); ip = f[4].split(';')
    U = list(range(m)); E = {u: set() if ip[u] == '-' else {int(x) for x in ip[u].split(',')} for u in U}
    g = {u: len(E[u]) + (0 if rp[u] == '-' else len(rp[u].split(','))) for u in U}
    tri = {frozenset((x, y, z)) for x in U for y in E[x] for z in E[x] & E[y] if x < y < z}
    return (f[0], tag, U, g, E, tri)

def explore_kills():
    want = {'f7_5567576_5....5.': 'D', 'f7_5567576_5....56': 'D', 'f7_5567576_5.5...6': 'D',
            'f7_..56757_...5...': 'C', 'f7_..57556_...65..': 'C', 'f7_..57556_...66..': 'C', 'f7_..65757_..55...': 'C',
            'f7_..65757_..65...': 'C', 'f7_5566757_...5...': 'C', 'f7_5567576_.....5.': 'C', 'f7_5667576_..5....': 'C',
            'f7_5675767_.5.....': 'C'}
    got = {}
    for fn in ('k34/fill.txt', 'k38/kills.txt', 'k37/cwin.txt', 'k34/b14.txt'):
        for l in open(os.path.join(H, '..', fn)):
            nm = l.split()[0]
            if nm in want and nm not in got: got[nm] = kcline(l, 'explore ' + want[nm])
    assert len(got) == len(want), set(want) - set(got)
    return list(got.values())

def embeddings(c, P, pa, pf, fd):
    nm, tag, U, g, E, tri = c
    order = [max(U, key=lambda u: (len(E[u]), g[u]))]
    while len(order) < len(U):
        order.append(max((u for u in U if u not in order), key=lambda u: (len(E[u] & set(order)), g[u])))
    out = set(); phi = {}
    def ok(u, v):
        return fd[v] == g[u] if v in fd else 5 <= g[u] <= 8
    def rec(i):
        if i == len(order):
            if all(frozenset(phi[x] for x in t) in pf for t in tri):
                out.add(tuple(sorted(phi.items())))
            return
        u = order[i]; pl = [w for w in order[:i] if w in E[u]]
        cand = set.intersection(*[pa[phi[w]] for w in pl]) if pl else set(P)
        for v in cand:
            if v in phi.values() or not ok(u, v): continue
            if any((phi[w] in pa[v]) != (w in E[u]) for w in order[:i]): continue
            phi[u] = v; rec(i + 1); del phi[u]
    if all(any(ok(u, v) for v in P) for u in U): rec(0)
    return out

def cut(img, a, b, p, tag):
    """kc line of the window with interior img (names) cut from the case's 2-ball, or None."""
    adj, name, faces = build2(letters(a, b, p)); inv = {v: x for x, v in name.items()}
    I = sorted(inv[x] for x in img); Is = set(I); RS = sorted({w for v in I for w in adj[v]} - Is)
    nbr = {x: set() for x in RS}
    for f in faces:
        if f & Is and len(f - Is) == 2:
            x, y = sorted(f - Is); nbr[x].add(y); nbr[y].add(x)
    if any(len(nbr[x]) != 2 for x in RS): return None
    cyc = [RS[0]]; prev = None
    while True:
        nx = sorted(nbr[cyc[-1]] - ({prev} if prev is not None else set()))[0]
        if nx == cyc[0]: break
        prev = cyc[-1]; cyc.append(nx)
    if len(cyc) != len(RS): return None
    ri = {x: k for k, x in enumerate(cyc)}; ii = {v: k for k, v in enumerate(I)}
    rp = ';'.join(','.join(str(k) for k in sorted(ri[w] for w in adj[v] if w in ri)) or '-' for v in I)
    ip = ';'.join(','.join(str(k) for k in sorted(ii[w] for w in adj[v] if w in ii)) or '-' for v in I)
    return '%s %d %d %s %s' % (tag, len(cyc), len(I), rp, ip)

if __name__ == '__main__':
    P, pa, pf = structure(); fd = fixed_deg()
    print('# 2-ball: %d exact-degree vertices, %d edges, %d faces among them' % (len(P), sum(len(v) for v in pa.values()) // 2, len(pf)))
    C = rsst() + explore_kills()
    pats = collections.defaultdict(set)      # requirement (tuple over VAR, 0 = free) -> {(config, image)}
    for c in C:
        for e in embeddings(c, P, pa, pf, fd):
            req = dict((v, c[3][u]) for u, v in e if v not in fd)
            key = tuple(req.get(x, 0) for x in VAR)
            if key[0] == 5 or key[1] == 5: continue          # fillings with a five at s1/s4: already dead
            pats[key].add((c[0], frozenset(v for _, v in e)))
    print('# configs %d; requirement patterns %d (from %d configs)' % (len(C), len(pats), len({x[0] for s in pats.values() for x in s})))
    # union over the 250,000 cases
    dead = {}; idx = lambda t: t
    for key, src in pats.items():
        rng = [[k] if k else ([6, 7, 8, 9] if j < 2 else LET) for j, k in enumerate(key)]
        for case in itertools.product(*rng):
            if case not in dead: dead[case] = (key, min(src, key=lambda x: (x[0], sorted(x[1]))))
    tot = collections.Counter(); surv = collections.defaultdict(list)
    for a in (6, 7, 8, 9):
        for b in (6, 7, 8, 9):
            for p in itertools.product(LET, repeat=6):
                case = (a, b) + p; tot[(a, b)] += 1
                if case not in dead: surv[(a, b)].append(p)
    with open(os.path.join(H, 'hits.txt'), 'w') as o:
        o.write('# requirement over %s (0 = free) | killing configs (name, image)\n' % ' '.join(map(str, VAR)))
        for key in sorted(pats):
            o.write('%s | %s\n' % (''.join(str(k) if k else '.' for k in key),
                                   ' '.join('%s:%s' % (n, '+'.join('%s%s' % (x[0], ''.join(map(str, x[1:]))) for x in sorted(img))) for n, img in sorted(pats[key])[:4])))
    with open(os.path.join(H, 'cases.txt'), 'w') as o:
        o.write('# survivors per filling (s1 s4), privates in order p1 p2a p2b p4a p4b p5 as build names %s\n' % VAR[2:])
        for f in sorted(tot):
            sv = surv[f]; m5 = sum(1 for p in sv if 5 in p); m6 = sum(1 for p in sv if 6 in p and 5 not in p)
            o.write('%d%d survivors %d of %d (with a private 5: %d; a 6 but no 5: %d; all >= 7: %d)\n' % (
                f + (len(sv), tot[f], m5, m6, sum(1 for p in sv if min(p) >= 7))))
        for f in sorted(tot):
            o.write('## %d%d\n' % f)
            for p in surv[f]: o.write(''.join(map(str, p)) + '\n')
    for f in sorted(tot): print('%d%d survivors %d of %d' % (f + (len(surv[f]), tot[f])))
