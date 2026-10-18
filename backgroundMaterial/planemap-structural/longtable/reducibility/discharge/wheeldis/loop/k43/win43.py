"""EXPLORE round 43 (Long Table, 19:33Z): windows of the K = 2 binder at 1/4, receiver d = 8 link 85556565, s 65866655
(s_i between w_i and w_i+1; every letter exact).  Part A: every connected induced subset X of the 17 fixed vertices
(u, w0..w7, s0..s7) at exact degrees, the rest of the map free ring; ring <= RMAX, simple ring.  Built on
gen.build's layered 2-ball (fresh third ring, privates of w0/w4/w6 free).  Names a8_<u|-><w letters>_<s letters>.
Writes win43_A.txt (kc/dfast lines, ring order).  usage: python3 win43.py RMAX"""
import sys, os, collections
H = os.path.dirname(os.path.abspath(__file__)); W = os.path.normpath(os.path.join(H, '..', '..'))
DIS = os.path.dirname(W); sys.path.insert(0, os.path.join(DIS, 'b8b')); sys.path.insert(0, DIS)
from rings import Layered
D, LK, SV = 8, '85556565', '65866655'
RMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 16

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
    return adj, name, {frozenset(t) for t in L.tris}

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

def ringsize(X, adj):
    Is = set(X); return len(set(y for x in X for y in adj[x]) - Is)

if __name__ == '__main__':
    r2 = {('s', j): int(SV[j]) for j in range(D)}
    adj, name, faces = build(r2); inv = {v: x for x, v in name.items()}
    V = [('u',)] + [('w', j) for j in range(D)] + [('s', j) for j in range(D)]
    deg = {('u',): D}; deg.update({('w', j): int(LK[j]) for j in range(D)}); deg.update({('s', j): int(SV[j]) for j in range(D)})
    for x in V: assert len(adj[inv[x]]) == deg[x], x
    nb = {x: {name[y] for y in adj[inv[x]] if name.get(y) in deg} for x in V}
    # connected subsets by canonical growth (each found once: grow from its least vertex, extensions above it)
    idx = {x: k for k, x in enumerate(V)}; out = {}; seen = set()
    def grow(S, ext, lo):
        key = frozenset(S)
        if key in seen: return
        seen.add(key)
        if len(S) >= 2:
            r = ringsize([inv[x] for x in S], adj)
            if r <= RMAX:
                c = extract(adj, [inv[x] for x in S], {inv[x]: deg[x] for x in S})
                if c is not None:
                    nm = 'a8_%s%s_%s' % ('u' if ('u',) in S else '-', ''.join(LK[j] if ('w', j) in S else '.' for j in range(D)),
                                         ''.join(SV[j] if ('s', j) in S else '.' for j in range(D)))
                    out[nm] = (c[0], '%s %d %d %s %s' % ((nm,) + c), sum(1 for x in S if deg[x] == 5))
        for y in sorted(ext, key=lambda z: idx[z]):
            if idx[y] <= lo: continue
            grow(S | {y}, (ext | nb[y]) - S - {y}, lo)
    for x in V:
        grow({x}, set(nb[x]), idx[x])
    L = sorted(out.values(), key=lambda t: (t[0], -t[2], t[1]))
    open(os.path.join(H, 'win43_A.txt'), 'w').write(''.join(t[1] + '\n' for t in L))
    print('connected subsets', len(seen), 'windows ring <= %d' % RMAX, len(L), sorted(collections.Counter(t[0] for t in L).items()))
    print('with >= 2 fives', sorted(collections.Counter(t[0] for t in L if t[2] >= 2).items()))
