"""Coordinator's check (09:22Z): does H7's defect D3 contain RSST configuration #110?  Own containment search (not
studiointel/rsst_contain.py or Opus's rsst_in_defect.py).  D3 is built from its signature with b8b/rings.py Layered (as
defect_verify.py does) plus all-6 sea rings; the outer ring's vertices have no exact degree and are never images.
Containment (RSST): injective map of the configuration's interior vertices, exact degrees, induced, and every
interior triangle of the configuration onto a face of the patch.  Each hit is then cut out of the patch (interior =
image, ring = its outside neighbours) and written as a kc input line, so kc (not dfast) can test it for D.
usage: python3 d3_rsst.py [index ...]  (default 110; 0-based and 1-based readings are both reported)"""
import sys, os
H = os.path.dirname(os.path.abspath(__file__)); DIS = os.path.normpath(os.path.join(H, '..', '..', '..'))
sys.path.insert(0, os.path.join(DIS, 'b8b')); sys.path.insert(0, DIS)
from rings import Layered
SIG, SEA = '5|55667|776675755|75576667557657', 4
CONF = os.path.normpath(os.path.join(DIS, '..', '..', '..', 'studiointel', 'routeb', 'rsst', 'unavoidable.conf'))

def patch():
    r = SIG.split('|'); L = Layered(int(r[0]))
    for k in range(1, len(r)): L.add_ring([int(c) for c in r[k]])
    for _ in range(SEA): L.add_ring([6] * len(L.ring()))
    adj = {}
    for a, b, c in L.tris:
        for x, y in ((a, b), (b, c), (c, a)): adj.setdefault(x, set()).add(y); adj.setdefault(y, set()).add(x)
    outer = set(L.ring()); deg = {v: len(adj[v]) for v in adj if v not in outer}
    for v, d in deg.items(): assert d == L.deg[v], (v, d, L.deg[v])
    faces = {frozenset(t) for t in L.tris}
    Y = [v for v in deg if deg[v] != 6]
    return adj, deg, faces, Y, L

def confs():
    C = []; lines = open(CONF).read().split('\n'); i = 0
    while i < len(lines):
        if not lines[i].strip(): i += 1; continue
        name = lines[i].strip(); f = lines[i + 1].split(); n, r = int(f[0]), int(f[1]); i += 3
        nb = {}
        for _ in range(n):
            f = lines[i].split(); nb[int(f[0])] = [int(x) for x in f[2:]]; assert len(nb[int(f[0])]) == int(f[1]); i += 1
        while i < len(lines) and lines[i].strip(): i += 1
        C.append({'name': name, 'n': n, 'r': r, 'nb': nb})
    return C

def embeddings(c, adj, deg, faces):
    r, n = c['r'], c['n']; U = list(range(r + 1, n + 1)); g = {u: len(c['nb'][u]) for u in U}
    E = {u: {w for w in c['nb'][u] if w > r} for u in U}
    tri = set()
    for u in U:
        L = c['nb'][u]
        for k in range(len(L)):
            a, b = L[k], L[(k + 1) % len(L)]
            if a > r and b > r: tri.add(frozenset((u, a, b)))
    order = [max(U, key=lambda u: len(E[u]))]
    while len(order) < len(U):
        order.append(max((u for u in U if u not in order), key=lambda u: (len(E[u] & set(order)), g[u])))
    out = set(); phi = {}
    def rec(i):
        if i == len(order):
            if all(frozenset(phi[x] for x in t) in faces for t in tri): out.add(tuple(sorted(phi.items())))
            return
        u = order[i]; pl = [w for w in order[:i] if w in E[u]]
        cand = (set.intersection(*[adj[phi[w]] for w in pl]) if pl else set(deg))
        for v in cand:
            if deg.get(v) != g[u] or v in phi.values(): continue
            if any((phi[w] in adj[v]) != (w in E[u]) for w in order[:i]): continue
            phi[u] = v; rec(i + 1); del phi[u]
    rec(0)
    return out

def cut(img, adj, deg, faces, name):
    """kc line for the configuration with interior img (cut from the patch); None unless its ring is a simple cycle."""
    I = sorted(img); Is = set(I); Rn = sorted({w for v in I for w in adj[v]} - Is)
    rg = {x: [y for y in adj[x] if y in Rn] for x in Rn}
    # ring order: walk the boundary through faces with exactly one... use: each ring vertex must have 2 ring neighbours
    # adjacent across a face that touches the interior
    nbr = {x: set() for x in Rn}
    for f in faces:
        if len(f & Is) >= 1 and len(f - Is) == 2:
            a, b = sorted(f - Is); nbr[a].add(b); nbr[b].add(a)
    if any(len(nbr[x]) != 2 for x in Rn): return None, 'ring not simple'
    cyc = [Rn[0]]; prev = None
    while True:
        nx = [y for y in nbr[cyc[-1]] if y != prev][0] if prev is not None else sorted(nbr[cyc[-1]])[0]
        if nx == cyc[0]: break
        prev = cyc[-1]; cyc.append(nx)
    if len(cyc) != len(Rn): return None, 'ring has %d of %d' % (len(cyc), len(Rn))
    chords = sum(1 for x in Rn for y in adj[x] if y in Rn and y not in nbr[x]) // 2
    ri = {x: k for k, x in enumerate(cyc)}; ii = {v: k for k, v in enumerate(I)}
    rp = ';'.join(','.join(str(k) for k in sorted(ri[w] for w in adj[v] if w in ri)) or '-' for v in I)
    ip = ';'.join(','.join(str(k) for k in sorted(ii[w] for w in adj[v] if w in ii)) or '-' for v in I)
    return '%s %d %d %s %s' % (name, len(cyc), len(I), rp, ip), 'ring %d, chords %d' % (len(cyc), chords)

if __name__ == '__main__':
    adj, deg, faces, Y, L = patch()
    dist = {0: 0}; fr = [0]
    while fr:
        nf = []
        for v in fr:
            for w in adj[v]:
                if w not in dist: dist[w] = dist[v] + 1; nf.append(w)
        fr = nf
    print('# D3 patch: %d vertices with exact degree, Y = %d fives + %d sevens, ring lengths %s' %
          (len(deg), sum(1 for v in Y if deg[v] == 5), sum(1 for v in Y if deg[v] == 7), [len(x) for x in L.rings]))
    C = confs(); print('# RSST file: %d configurations' % len(C))
    want = [int(a) for a in sys.argv[1:]] or [110]
    for k in want:
        for base, idx in (('0-based', k), ('1-based', k - 1)):
            c = C[idx]; r, n = c['r'], c['n']
            dg = sorted(len(c['nb'][u]) for u in range(r + 1, n + 1))
            emb = embeddings(c, adj, deg, faces)
            imgs = {frozenset(v for _, v in e) for e in emb}
            print('#%d (%s): name %s, ring %d, interior degrees %s: %d embeddings, %d images' % (k, base, c['name'], r, dg, len(emb), len(imgs)))
            for j, img in enumerate(sorted(imgs, key=sorted)):
                inY = all(v in Y for v in img); dY = max(min(abs(dist[v] - dist[y]) for y in Y) for v in img)
                line, info = cut(img, adj, deg, faces, 'd3_rsst%d_%s_%d' % (k, base[0], j))
                print('  image %s (all in Y: %s), %s' % (sorted(img), inY, info))
                if line: print('KC ' + line)
