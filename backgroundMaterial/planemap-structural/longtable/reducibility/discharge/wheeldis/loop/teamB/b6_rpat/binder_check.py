"""B6 probe: for a receiver arrangement (degree d, link word w, s-word s; 9 = 9+), does a published RSST configuration
(all 633 two-engine verified by Team B in B2) appear for every assignment of the privates?  Own containment test from
b5_lt7/contain.py on explicit discs (third ring free)."""
import sys, os, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
DIS = os.path.abspath(os.path.join(HERE, '../../../..'))
sys.path.insert(0, os.path.join(DIS, 'b8b')); sys.path.insert(0, DIS)
sys.path.insert(0, os.path.join(HERE, '..', 'b1_rsst')); sys.path.insert(0, os.path.join(HERE, '..', 'b5_lt7'))
from rings import Layered
from rstar import disc_rot
import contain

def layout(d, link, sword):
    L = Layered(d); w = L.rings[1]; L.add_ring(list(link)); R2 = L.rings[2]
    adj = {}
    for a, b, c in L.tris:
        for x, y in ((a, b), (b, c), (c, a)):
            adj.setdefault(x, set()).add(y); adj.setdefault(y, set()).add(x)
    S = []
    for i in range(d):
        c = [z for z in R2 if w[i] in adj[z] and w[(i + 1) % d] in adj[z]]
        assert len(c) == 1; S.append(c[0])
    P = [z for z in R2 if z not in S]
    return L, w, S, P

def check(d, link, sword, mode='strict'):
    L0, w, S, P = layout(d, link, sword)
    nkill = 0; n = 0; hits = {}
    for priv in itertools.product([5, 6, 7, 8, 9], repeat=len(P)):
        L, w, S, P = layout(d, link, sword)
        deg = {0: d}
        for i in range(d):
            deg[w[i]] = link[i]; deg[S[i]] = sword[i]
        for z, p in zip(P, priv): deg[z] = p
        L.add_ring([deg[z] for z in L.rings[2]])
        rot = disc_rot(L)
        known = {x for x in deg if deg[x] is not None and len(rot[x]) == deg[x]}
        n += 1
        h = None
        for c in contain.CONFS:
            if contain.embed(c, rot, deg, known, mode):
                h = c[0]; break
        if h:
            nkill += 1; hits[h] = hits.get(h, 0) + 1
        else:
            return False, n, nkill, priv, hits
    return True, n, nkill, None, hits

if __name__ == '__main__':
    for a in sys.argv[1:]:
        ww, ss = a.split('/')
        link = [int(c) for c in ww]; sw = [int(c) for c in ss]
        print(a, check(len(link), link, sw), flush=True)
