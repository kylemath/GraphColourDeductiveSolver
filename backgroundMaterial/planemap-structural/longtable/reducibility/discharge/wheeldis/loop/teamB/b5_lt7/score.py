"""Team B round B5 (Long Table request): RSST score of a degree-7 receiver u with link 7665566 and s-word 6675666,
over all private-degree assignments in {5..9+}, third ring free (same method as round B1's R* sweep).
Privates are listed in ring-2 order starting after s_6 (around w_0 first). Output: privates, min score, max score."""
import sys, os, itertools
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__))
B1 = os.path.join(HERE, '..', 'b1_rsst')
DIS = os.path.abspath(os.path.join(HERE, '../../../..'))
sys.path.insert(0, os.path.join(DIS, 'b8b'))
sys.path.insert(0, DIS)
sys.path.insert(0, B1)
from rings import Layered
import rsst
from rstar import disc_rot

LINK = [7, 6, 6, 5, 5, 6, 6]
SWORD = [6, 6, 7, 5, 6, 6, 6]


def layout():
    L = Layered(7)
    w = L.rings[1]
    L.add_ring(LINK)
    R2 = L.rings[2]
    adj = {}
    for a, b, c in L.tris:
        for x, y in ((a, b), (b, c), (c, a)):
            adj.setdefault(x, set()).add(y)
            adj.setdefault(y, set()).add(x)
    S = []
    for i in range(7):
        c = [z for z in R2 if w[i] in adj[z] and w[(i + 1) % 7] in adj[z]]
        assert len(c) == 1
        S.append(c[0])
    # ring-2 order starting just after s_6
    k = R2.index(S[6])
    order = R2[k + 1:] + R2[:k + 1]
    P = [z for z in order if z not in S]
    owner = {z: [i for i in range(7) if w[i] in adj[z]] for z in P}
    return L, w, S, P, owner


def score(priv):
    L, w, S, P, owner = layout()
    deg = {0: 7}
    for i in range(7):
        deg[w[i]] = LINK[i]
        deg[S[i]] = SWORD[i]
    for z, p in zip(P, priv):
        deg[z] = p
    L.add_ring([deg[z] for z in L.rings[2]])
    R3 = L.rings[3]
    for z in R3:
        deg[z] = None
    rot = disc_rot(L)
    M = rsst.Map(rot, dict(deg))
    out_u = M.sends(0)
    hi = lo = -10 - len(out_u)
    for x in w:
        a, b, _ = rsst.inflow_range(M, x, 0, set(R3))
        hi += b
        lo += a
    return lo, hi


def job(first):
    out = []
    for rest in itertools.product([5, 6, 7, 8, 9], repeat=NP - 1):
        priv = (first,) + rest
        try:
            lo, hi = score(priv)
            out.append('%s %d %d' % (''.join(map(str, priv)), lo, hi))
        except AssertionError:
            out.append('%s ERR' % ''.join(map(str, priv)))
    return out


_, _, _, P0, OWN = layout()
NP = len(P0)

if __name__ == '__main__':
    print('privates (ring-2 order after s6), owners (link index):', [OWN[z] for z in P0], file=sys.stderr)
    with Pool(2) as pool, open(os.path.join(HERE, 'sweep.out'), 'w') as fo:
        for res in pool.imap_unordered(job, [5, 6, 7, 8, 9]):
            fo.write('\n'.join(res) + '\n')
            fo.flush()
