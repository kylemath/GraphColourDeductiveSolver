"""B8b (exploratory): dfast configurations of u-centred 2-balls (free completion; ring = third ring of u) from the
block model.  Usage: centred_cfg.py D MINP RMIN RMAX  > configs   (u-centred 2-balls of degree D with at least MINP
relaxed private 66666 senders, rings RMIN..RMAX; names c<D>_<blocks>, blocks as dw.p.s with p '-' if none)."""
import sys, os, itertools
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import ball
from maxsend import BLOCKS, count
from centred import canon, ring
from rings import Layered


def cfg_of(S, name):
    d = len(S); L = Layered(d); L.add_ring([b[0] for b in S])
    R2 = L.ring(); degs = []; i = 0; k = 0
    # ring-2 order produced by Layered: for each link vertex its O-triangles' outer vertices; map to blocks
    flat = []; priv = []
    for dw, p, s in S:
        if p is not None: flat.append(p); priv.append(True)
        flat.append(s); priv.append(False)
    # Layered's ring 2 starts with z_0 = vertex shared by w_{d-1} and w_0, i.e. s_{d-1}
    flat = [flat[-1]] + flat[:-1]; priv = [priv[-1]] + priv[:-1]
    assert len(flat) == len(R2) and all((L.inn[z] == 1) == pv for z, pv in zip(R2, priv)), name
    L.add_ring(flat)
    I = set(L.rings[0] + L.rings[1] + L.rings[2]); R3 = L.rings[3]
    adj = {}
    for a, b, c in L.tris:
        for x, y in ((a, b), (b, c), (c, a)): adj.setdefault(x, set()).add(y); adj.setdefault(y, set()).add(x)
    Il = sorted(I); ii = {x: j for j, x in enumerate(Il)}; ri = {y: j for j, y in enumerate(R3)}
    # check private/shared pattern matches: in-count 1 exactly at private positions
    for z, dz in zip(R2, flat): assert len(adj[z]) == dz, (name, z, dz, len(adj[z]))
    ia = [sorted(ii[y] for y in adj[x] if y in I) for x in Il]
    ra = [sorted(ri[y] for y in adj[x] if y in ri) for x in Il]
    D = [len(adj[x]) for x in Il]
    return ball.fmt_config(name, (len(R3), len(Il), D, ia, ra))


if __name__ == '__main__':
    d, minp, lo, hi = map(int, sys.argv[1:5]); seen = set()
    for seq in itertools.product(range(6), repeat=d):
        c = canon([BLOCKS[b] for b in seq])
        if c in seen: continue
        seen.add(c); k, who = count(list(c), d)
        if sum(1 for w in who if w[0] == 'p') < minp: continue
        r = ring(c)
        if not lo <= r <= hi: continue
        name = 'c%d_' % d + '_'.join('%d.%s.%d' % (dw, '-' if p is None else p, s) for dw, p, s in c)
        print(cfg_of(list(c), name))
