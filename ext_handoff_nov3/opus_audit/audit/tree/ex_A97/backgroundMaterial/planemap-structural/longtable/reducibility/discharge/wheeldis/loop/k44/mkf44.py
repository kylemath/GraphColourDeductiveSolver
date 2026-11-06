"""EXPLORE round 44 part B: twoeng-ready f-names for the eligible RSST containment patterns (pats44.txt).
Each pattern becomes f<d>_<link>_<s> names (letters 5..8 exact, B = {7,8,9}, '.' free); a w_i that must be not-5 is
written twice, as 6 and as B.  Each name gets a kc line: the window cut at the embedding's image from a representative
2-ball (free link letters 9, free s letters 9, layered with a fresh third ring, as win43/win45), checked to have the
source configuration's ring size and interior size.  The kc lines then go through drive44.py (kc -C, dfast, cfast
--fixed with kc's X), so the f-names are verified on two engines as windows, as round 43's were.
usage: python3 mkf44.py   -> pats44_f.txt (kc lines, ring order), pats44_f.map (f-name, NF pattern, source config)"""
import sys, os, itertools
H = os.path.dirname(os.path.abspath(__file__)); W = os.path.normpath(os.path.join(H, '..', '..'))
DIS = os.path.dirname(W); sys.path.insert(0, os.path.join(DIS, 'b8b')); sys.path.insert(0, DIS); sys.path.insert(0, H)
from rings import Layered
import gen44 as G

def build(d, lk, sv):
    L = Layered(d); L.add_ring(list(lk))
    Wr = L.rings[1]; Z = L.ring(); adj = {}
    for a, b, c in L.tris:
        for x, y in ((a, b), (b, c), (c, a)): adj.setdefault(x, set()).add(y); adj.setdefault(y, set()).add(x)
    name = {0: ('u',)}
    for i, w in enumerate(Wr): name[w] = ('w', i)
    Wi = {w: i for i, w in enumerate(Wr)}; cnt = {}
    for z in Z:
        ws = sorted(Wi[x] for x in adj[z] if x in Wi)
        if len(ws) == 2:
            i, j = ws; name[z] = ('s', j if (i, j) == (0, d - 1) else i)
        else:
            i = ws[0]; cnt[i] = cnt.get(i, 0) + 1; name[z] = ('p', i, cnt[i])
    L.add_ring([sv[name[z][1]] if name[z][0] == 's' else 9 for z in Z])
    adj = {}
    for a, b, c in L.tris:
        for x, y in ((a, b), (b, c), (c, a)): adj.setdefault(x, set()).add(y); adj.setdefault(y, set()).add(x)
    return adj, name

def extract(adj, I):
    Is = set(I); RS = set(y for x in I for y in adj[x]) - Is
    for y in RS:
        if len(adj[y] & RS) != 2: return None
    start = min(RS); order = [start]; prev = None
    while True:
        cur = order[-1]; nb = sorted(adj[cur] & RS); nxt = nb[0] if nb[0] != prev else nb[1]
        if nxt == start: break
        order.append(nxt); prev = cur
    if len(order) != len(RS): return None
    ri = {y: j for j, y in enumerate(order)}; Il = sorted(I); ii = {x: j for j, x in enumerate(Il)}
    f = lambda Ls: ';'.join(','.join(map(str, v)) if v else '-' for v in Ls)
    ia = [sorted(ii[y] for y in adj[x] if y in Is) for x in Il]
    ra = [sorted(ri[y] for y in adj[x] if y in RS) for x in Il]
    return len(order), len(Il), f(ra), f(ia)

def canon_key(d, lk, sv):     # gen.canon_key (s_i between w_i and w_i+1), as k43/fname.py
    best = None
    for refl in (0, 1):
        if refl: l2 = lk[::-1]; s2 = ''.join(sv[(-i - 2) % d] for i in range(d))
        else: l2, s2 = lk, sv
        for k in range(d):
            c = (l2[k:] + l2[:k], s2[k:] + s2[:k])
            if best is None or c < best: best = c
    return best

if __name__ == '__main__':
    C = {c[0]: c for c in G.grow.rsst()}
    kcn = {l.split()[0]: l.split() for l in open(os.path.join(H, 'rsst.txt')) if l.strip()}
    out = {}; mp = []; bad = 0
    for l in open(os.path.join(H, 'pats44.txt')):
        if l.startswith('#'): continue
        a, word, srcs = l.rstrip('\n').split(' | '); f = list(map(int, a.split())); d = f[0]
        F = tuple((f[2 + 2 * j], f[3 + 2 * j]) for j in range(f[1]))
        # find an embedding of a source config that gives exactly this pattern (some dihedral image of it)
        target = G.canon(d, F); got = None
        for src in srcs.split():
            c = C[src.split('_')[0]]; c = (src,) + tuple(c[1:])
            for phi, r in G.embeddings(c, d, G.host(d)):
                if G.canon(d, G.pattern(d, c, phi, r)) == target: got = (c, phi, r); break
            if got: break
        assert got, l
        c, phi, r = got; Fd = dict(G.pattern(d, c, phi, r))
        cols = []
        for sl in range(2 * d):
            m = Fd.get(sl)
            if m is None: cols.append(['.'])
            elif m == 30: cols.append(['6', 'B'])
            else: cols.append([str(5 + m.bit_length() - 1)])
        img = set(phi.values())
        for pick in itertools.product(*cols):
            lk = [int(ch) if ch in '5678' else (7 if ch == 'B' else 9) for ch in pick[:d]]
            sv = [int(ch) if ch in '5678' else 9 for ch in pick[d:]]
            adj, name = build(d, lk, sv); inv = {v: x for x, v in name.items()}
            cut = extract(adj, [inv[v] for v in img])
            r0, m0 = int(kcn[c[0]][1]), int(kcn[c[0]][2])
            if cut is None or cut[0] != r0 or cut[1] != m0:
                bad += 1; print('# cut mismatch', c[0], d, ''.join(pick), cut[:2] if cut else None); continue
            ck = canon_key(d, ''.join(pick[:d]), ''.join(pick[d:])); fn = 'f%d_%s_%s' % (d, ck[0], ck[1])
            if fn in out: continue
            out[fn] = (cut[0], '%s %d %d %s %s' % ((fn,) + cut)); mp.append('%s | %s | %s' % (fn, a, c[0]))
    L = sorted(out.values(), key=lambda t: (t[0], t[1]))
    open(os.path.join(H, 'pats44_f.txt'), 'w').write(''.join(t[1] + '\n' for t in L))
    open(os.path.join(H, 'pats44_f.map'), 'w').write('# f-name | NF pattern | source configuration (cut window has its ring and interior size)\n' + '\n'.join(mp) + '\n')
    print('f-names %d (cut mismatches %d)' % (len(out), bad))
