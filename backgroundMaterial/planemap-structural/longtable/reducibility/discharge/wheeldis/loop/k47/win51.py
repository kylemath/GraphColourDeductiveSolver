"""EXPLORE round 51 part 2 (Long Table, 01:52Z): windows of the binder 7665566/6675666 that use its one-ring-out
census survivors (loop/k50/census50_7_7665566_6675666.txt: every private >= 6 and p51 >= 7).
The 2-ball is win45's (gen-style layered build, fresh third ring).  Windows are connected induced subsets X of u, w_i,
s_i and the six privates, with at least one private, at exact degrees, simple ring, RMIN <= ring <= RMAX.  Each private
in X takes each exact letter its survivor set allows (6..8; p51 7..8; a 9 is >= 9 and never exact), which sets its
ring-3 degree; privates outside X keep win45's free letter.  Names b7_<u|-><w>_<s>_<privates p01 p02 p11 p21 p51 p61,
letter or .>, with win45's F/N for w_i when s_(i-1) and s_i are both in X.  Order: ring, then more fives, more sixes.
usage: python3 win51.py RMAX [RMIN]   -> win51_A<RMAX>.txt (kc/dfast lines)"""
import sys, os, collections, itertools
H = os.path.dirname(os.path.abspath(__file__)); W = os.path.normpath(os.path.join(H, '..', '..'))
DIS = os.path.dirname(W); sys.path.insert(0, os.path.join(DIS, 'b8b')); sys.path.insert(0, DIS)
from rings import Layered
D, LK, SV = 7, '7665566', '6675666'
RMAX = int(sys.argv[1]); RMIN = int(sys.argv[2]) if len(sys.argv) > 2 else 0

def build(r2):
    L = Layered(D); L.add_ring([int(c) for c in LK])
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
    return adj, name

def extract(adj, I, deg):
    Is = set(I); RS = set(y for x in I for y in adj[x]) - Is
    for y in RS:
        if len(adj[y] & RS) != 2: return None
    start = min(RS); order = [start]; prev = None
    while True:
        cur = order[-1]; nb = sorted(adj[cur] & RS); nxt = nb[0] if nb[0] != prev else nb[1]
        if nxt == start: break
        order.append(nxt); prev = cur
    if len(order) != len(RS): return None
    for x in I: assert len(adj[x]) == deg[x], (x, len(adj[x]), deg[x])
    ri = {y: j for j, y in enumerate(order)}; Il = sorted(I); ii = {x: j for j, x in enumerate(Il)}
    f = lambda Ls: ';'.join(','.join(map(str, v)) if v else '-' for v in Ls)
    ia = [sorted(ii[y] for y in adj[x] if y in Is) for x in Il]
    ra = [sorted(ri[y] for y in adj[x] if y in RS) for x in Il]
    return len(order), len(Il), f(ra), f(ia)

if __name__ == '__main__':
    S0 = {('s', j): int(SV[j]) for j in range(D)}
    adj0, name0 = build(S0)
    PRIV = sorted(v for v in name0.values() if v[0] == 'p')
    assert PRIV == [('p', 0, 1), ('p', 0, 2), ('p', 1, 1), ('p', 2, 1), ('p', 5, 1), ('p', 6, 1)], PRIV
    ALLOW = {p: ((7, 8) if p == ('p', 5, 1) else (6, 7, 8)) for p in PRIV}
    V = [('u',)] + [('w', j) for j in range(D)] + [('s', j) for j in range(D)] + PRIV
    inv0 = {v: x for x, v in name0.items()}
    fixed = {('u',): D}; fixed.update({('w', j): int(LK[j]) for j in range(D)}); fixed.update(S0)
    nb = {x: {name0[y] for y in adj0[inv0[x]] if name0.get(y) in set(V)} for x in V}
    cache = {}
    def ball(key):
        if key not in cache:
            adj, name = build(dict(S0) | dict(key)); cache[key] = (adj, {v: x for x, v in name.items()})
        return cache[key]
    idx = {x: k for k, x in enumerate(V)}; out = {}; seen = set(); nsub = [0, 0, 0]
    def visit(S):
        pr = [p for p in PRIV if p in S]
        if not pr or len(S) < 2: return
        nsub[0] += 1
        lo_ = tuple((p, ALLOW[p][0]) for p in pr); adj, inv = ball(lo_); X = [inv[x] for x in S]
        rmin = len(set(y for x in X for y in adj[x]) - set(X))    # a private one degree higher adds one ring vertex
        if rmin > RMAX: return
        for lets in itertools.product(*[ALLOW[p] for p in pr]):
            if not RMIN <= rmin + sum(l - ALLOW[p][0] for p, l in zip(pr, lets)) <= RMAX: continue
            key = tuple(zip(pr, lets)); adj, inv = ball(key); deg = dict(fixed); deg.update(key)
            X = [inv[x] for x in S]
            r = len(set(y for x in X for y in adj[x]) - set(X))
            if r != rmin + sum(l - ALLOW[p][0] for p, l in zip(pr, lets)): nsub[2] += 1
            if not RMIN <= r <= RMAX: continue
            c = extract(adj, X, {inv[x]: deg[x] for x in S})
            if c is None: continue
            pl = dict(key)
            nm = 'b7_%s%s_%s_%s' % ('u' if ('u',) in S else '-',
                                    ''.join(LK[j] if ('w', j) in S else (('F' if LK[j] == '5' else 'N') if (('s', (j - 1) % D) in S and ('s', j) in S) else '.') for j in range(D)),
                                    ''.join(SV[j] if ('s', j) in S else '.' for j in range(D)),
                                    ''.join(str(pl[p]) if p in pl else '.' for p in PRIV))
            out[nm] = (c[0], -sum(1 for x in S if deg[x] == 5), -sum(1 for x in S if deg[x] == 6), '%s %d %d %s %s' % ((nm,) + c))
            nsub[1] += 1
    def grow(S, ext, lo):
        key = frozenset(S)
        if key in seen: return
        seen.add(key); visit(S)
        for y in sorted(ext, key=lambda z: idx[z]):
            if idx[y] <= lo: continue
            grow(S | {y}, (ext | nb[y]) - S - {y}, lo)
    for x in V:
        grow({x}, set(nb[x]), idx[x])
    L = sorted(out.values())
    open(os.path.join(H, 'win51_A%d.txt' % RMAX), 'w').write(''.join(t[3] + '\n' for t in L))
    print('connected subsets', len(seen), 'with a private', nsub[0], 'ring not additive', nsub[2], 'windows %d <= ring <= %d' % (RMIN, RMAX), len(L),
          sorted(collections.Counter(t[0] for t in L).items()))
