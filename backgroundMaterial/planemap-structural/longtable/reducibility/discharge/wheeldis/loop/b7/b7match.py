"""EXPLORE round 10 (exploratory): do LP binder arrangements (u = 7, link w, s word) occur inside isolated positive
defects centred at u?  Reads defect leaves ("c=.. sig=7|ring1|ring2|..."), names ring-2 vertices with b8b/rings.py's
Layered and gen.py's convention (s_i = common neighbour of w_i, w_i+1; p = the other second-ring neighbours), and
reports every leaf whose (link, s) is a dihedral image of a binder (p letters free).
Usage: python3 b7match.py BINDERS LEAVES...   (BINDERS: lines 'link s')"""
import sys, os, collections
DIS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(DIS, 'b8b')); from rings import Layered
def names(link):
    d = len(link); L = Layered(d); L.add_ring([int(c) for c in link]); W = L.rings[1]; Z = L.ring(); adj = {}
    for a, b, c in L.tris:
        for x, y in ((a, b), (b, c), (c, a)): adj.setdefault(x, set()).add(y); adj.setdefault(y, set()).add(x)
    Wi = {w: i for i, w in enumerate(W)}; out = []; cnt = {}
    for z in Z:
        ws = sorted(Wi[x] for x in adj[z] if x in Wi)
        if len(ws) == 2: i, j = ws; out.append(('s', j if (i, j) == (0, d - 1) else i))
        else: i = ws[0]; cnt[i] = cnt.get(i, 0) + 1; out.append(('p', i, cnt[i]))
    return out
def images(lk, sv):
    d = len(lk)
    for r in range(d):
        yield lk[r:] + lk[:r], sv[r:] + sv[:r]
        yield ''.join(lk[(r - i) % d] for i in range(d)), ''.join(sv[(r - i - 1) % d] for i in range(d))
B = {}
for line in open(sys.argv[1]):
    f = line.split()
    if len(f) >= 2:
        for im in images(f[0], f[1]): B.setdefault(im, '%s/%s' % (f[0], f[1]))
NM = {}; hits = collections.Counter(); seen = collections.Counter()
for fn in sys.argv[2:]:
    for line in open(fn):
        if 'sig=' not in line: continue
        c = line.split()[0]; rg = line.split('sig=')[1].split()[0].split('|')
        if rg[0] != '7' or len(rg) < 3: continue
        lk, r2 = rg[1], rg[2]
        if lk not in NM: NM[lk] = names(lk)
        nm = NM[lk]
        if len(nm) != len(r2): print('length mismatch', line.strip()); continue
        sv = ['?'] * len(lk)
        for (x, l) in zip(nm, r2):
            if x[0] == 's': sv[x[1]] = l
        key = (lk, ''.join(sv)); seen[os.path.basename(fn)] += 1
        if key in B:
            hits[(B[key], os.path.basename(fn))] += 1
            print('HIT %s in %s: %s %s' % (B[key], os.path.basename(fn), c, '|'.join(rg)))
print('leaves read:', dict(seen)); print('hits:', dict(hits) if hits else 'none')
