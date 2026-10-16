"""EXPLORE round 19 (H-B0, exploratory): joint (u, v) pairs.  A at u (d = 7), B at a link big v = w_i of u (pairs.py
fits).  One patch: Layered at u with A's link and s; B gives v's other link letters (u's ring 2) and v's s letters
(u's ring 2 or 3).  Unknown letters are 6 fillers and never inside a configuration.  At u and at v, every S (|S| >= 2)
of the centre's fives: B-fixed I = c + S + N(S) and receiver-centred I = c + S + 5/6-neighbours, with defect_check2's
ring repair; each configuration is looked up by la.ckey in bridge.pkl (existing D/C verdicts only).
Kill classes: single (I inside the centre's own arrangement: A's letters for u, B's for v), joint (otherwise).
Usage: python3 b0.py cert WLP3_OUT...   |   python3 b0.py rows HARDROWS FAMILY..."""
import sys, os, re, itertools, collections, pickle
HERE = os.path.dirname(os.path.abspath(__file__)); W = os.path.dirname(os.path.dirname(HERE))
DIS = os.path.dirname(W)
sys.path.insert(0, os.path.join(DIS, 'b8b')); from rings import Layered
sys.path.insert(0, os.path.join(W, 'loop', 'lemmaA')); _a = sys.argv; sys.argv = ['x']; import la; sys.argv = _a
src = open(os.path.join(HERE, 'pairs.py')).read(); exec(src[:src.index('arrs = [')])   # images, view, fits
BR = pickle.load(open(os.path.join(HERE, 'bridge.pkl'), 'rb'))
def graph(L):
    adj = collections.defaultdict(set); nxt = collections.defaultdict(dict)
    for a, b, c in L.tris:
        for x, y in ((a, b), (b, c), (c, a)): adj[x].add(y); adj[y].add(x)
        nxt[a][b] = c; nxt[b][c] = a; nxt[c][a] = b
    return adj, nxt
def rotf(nxt, x):
    s0 = min(nxt[x]); r = [s0]; y = nxt[x][s0]
    while y != s0: r.append(y); y = nxt[x][y]
    return r
def extract_cfg(adj, I):
    Is = set(I); RS = set(y for x in I for y in adj[x]) - Is
    for y in RS:
        if len(adj[y] & RS) != 2: return None
    start = min(RS); order = [start]; prev = None
    while True:
        cur = order[-1]; nb = sorted(adj[cur] & RS); nx = nb[0] if nb[0] != prev else nb[1]
        if nx == start: break
        order.append(nx); prev = cur
    if len(order) != len(RS): return None
    ri = {y: j for j, y in enumerate(order)}; Il = sorted(I); ii = {x: j for j, x in enumerate(Il)}
    f = lambda Ls: ';'.join(','.join(map(str, v)) if v else '-' for v in Ls)
    ia = [sorted(ii[y] for y in adj[x] if y in Is) for x in Il]
    ra = [sorted(ri[y] for y in adj[x] if y in RS) for x in Il]
    return '%d %d %s %s' % (len(order), len(Il), f(ra), f(ia))
def oriented(nxt, c, first, second):
    r = rotf(nxt, c); k = r.index(first); r = r[k:] + r[:k]
    if r[1] != second: r = [r[0]] + r[1:][::-1]
    assert r[1] == second
    return r
def build(A, i, Bimg, SEA=4):
    """patch for A (link, s) at u with B's image (aligned with view(A, i)) at v = w_i; None if inconsistent"""
    lk, sv = A; d = len(lk); bl, bs = Bimg
    def mk(r2deg, r3deg):
        L = Layered(d); L.add_ring([int(c) for c in lk])
        if r2deg is None: return L
        L.add_ring(r2deg)
        if r3deg is None: return L
        L.add_ring(r3deg)
        for _ in range(SEA):   # filler sea, only to close rings around configurations; stop where 6s cannot continue
            try: L.add_ring([6] * len(L.ring()))
            except AssertionError: break
        return L
    L = mk(None, None); adj, nxt = graph(L); Wv = L.rings[1]; R2 = L.ring(); u = 0
    deg2 = {}
    for z in R2:
        ws = sorted(Wv.index(x) for x in adj[z] if x in Wv)
        if len(ws) == 2:
            a, b = ws; j = b if (a, b) == (0, d - 1) else a; deg2[z] = int(sv[j])
        else: deg2[z] = 6
    known = {u} | set(Wv) | {z for z in R2 if deg2[z] != 6 or len([x for x in adj[z] if x in Wv]) == 2}
    known = {u} | set(Wv) | {z for z in R2 if len([x for x in adj[z] if x in Wv]) == 2}
    Aset = set(known)
    v = Wv[i]
    # v's link: after adding ring 2 (ring-2 degrees not needed for v's own neighbours)
    adj2, nxt2 = adj, nxt   # ring 1 added: v's neighbourhood and ring 2 (with its adjacencies) exist, ring 3 not yet
    vl = oriented(nxt2, v, u, Wv[(i + 1) % d])
    if len(vl) != len(bl): return None
    for x, c in zip(vl, bl):
        if x in deg2:
            if x in Aset and deg2[x] != int(c): return None
            deg2[x] = int(c); known.add(x)
        elif x != u and x in Wv and int(lk[Wv.index(x)]) != int(c): return None
    # v's s letters: common neighbour of consecutive link vertices other than v; ring-2 ones first (they change ring 3)
    for t in range(len(vl)):
        a, b = vl[t], vl[(t + 1) % len(vl)]
        com = [z for z in adj2[a] & adj2[b] if z != v]
        if len(com) > 1: return None
        if not com: continue
        z = com[0]; c = int(bs[t])
        if z in deg2:
            if (z in Aset or z in known) and deg2[z] != c: return None
            deg2[z] = c; known.add(z)
        elif z in Wv:
            if int(lk[Wv.index(z)]) != c: return None
        else: return None
    try:
        L3 = mk([deg2[z] for z in R2], None)
    except AssertionError:
        return None
    adj3, nxt3 = graph(L3); R3 = L3.ring(); deg3 = {z: 6 for z in R3}
    vl = oriented(nxt3, v, u, Wv[(i + 1) % d]); sset = []
    for t in range(len(vl)):
        a, b = vl[t], vl[(t + 1) % len(vl)]
        com = [z for z in adj3[a] & adj3[b] if z != v]
        if len(com) != 1: return None
        z = com[0]; c = int(bs[t]); sset.append(z)
        if z in deg3: deg3[z] = c; known.add(z)
        elif z in deg2:
            if deg2[z] != c: return None
        elif z in Wv:
            if int(lk[Wv.index(z)]) != c: return None
        else: return None
    try:
        L4 = mk([deg2[z] for z in R2], [deg3[z] for z in R3])
    except AssertionError:
        return None
    adj4, nxt4 = graph(L4); deg = dict(L4.deg)
    Bset = {v} | set(vl) | set(sset)
    return adj4, nxt4, deg, known, Aset, Bset, u, v
def configs(adj, nxt, deg, known, c):
    """yield (kind, S, I) for the centre c: B-fixed and receiver-centred, with ring repair; I must be inside known"""
    lk = rotf(nxt, c); snd = [x for x in lk if deg[x] == 5]
    for k in range(2, len(snd) + 1):
        for S in itertools.combinations(snd, k):
            for kind in ('bf', 'rc'):
                I = {c} | set(S)
                for x in S: I |= (adj[x] if kind == 'bf' else {y for y in adj[x] if deg[y] <= 6})
                cfg = extract_cfg(adj, I)
                if cfg is None:
                    RS = set(y for x in I for y in adj[x]) - I
                    I2 = I | {y for y in RS if adj[y] <= (I | RS)}
                    if I2 == I: continue
                    I = I2; cfg = extract_cfg(adj, I)
                    if cfg is None: continue
                if not I <= known: continue
                yield kind, S, I, cfg
def pair_kills(A, i, Bimg):
    P = build(A, i, Bimg)
    if P is None: return None
    adj, nxt, deg, known, Aset, Bset, u, v = P; out = []
    for c, own in ((u, Aset), (v, Bset)):
        for kind, S, I, cfg in configs(adj, nxt, deg, known, c):
            hit = BR.get(la.ckey(cfg))
            if hit: out.append(('u' if c == u else 'v', kind, 'single' if I <= own else 'joint', hit[0], hit[1], int(cfg.split()[0])))
    return out
def fitting(A, B):
    """(i, image) for every link big w_i of A at which B fits"""
    res = []
    for i, ch in enumerate(A[0]):
        if ch not in '789' or int(ch) != len(B[0]): continue
        for im in sorted(set(fits(view(A[0], A[1], i), B))): res.append((i, im))
    return res
def arrs(fn):
    out = []
    for line in open(fn):
        m = re.search(r'd=7 link (\d{7}) s (\d{7})', line)
        if m: out.append((m.group(1), m.group(2)))
    return list(dict.fromkeys(out))
if __name__ == '__main__' and sys.argv[1] == 'cert':
    for fn in sys.argv[2:]:
        R = []
        for line in open(fn):
            m = re.match(r'\s+([\d.]+)\s+receiver d=7 link (\S+) s (\S+),', line)
            if m: R.append((float(m.group(1)), (m.group(2), m.group(3))))
        print('==', os.path.basename(fn), len(R), 'receivers')
        for (wa, A), (wb, B) in itertools.product(R, R):
            for i, im in fitting(A, B):
                k = pair_kills(A, i, im)
                if k is None: print('  %s/%s at w%d <- %s/%s: patch inconsistent' % (A[0], A[1], i, B[0], B[1])); continue
                cls = collections.Counter((x[0], x[2]) for x in k)
                print('  %s/%s at w%d <- %s/%s as %s/%s: %s %s' % (A[0], A[1], i, B[0], B[1], im[0], im[1], dict(cls) or 'FEASIBLE', ' '.join(sorted(set('%s:%s:%s:%s:r%d' % (x[0], x[2], x[3], x[4][:24], x[5]) for x in k)))[:300]))
