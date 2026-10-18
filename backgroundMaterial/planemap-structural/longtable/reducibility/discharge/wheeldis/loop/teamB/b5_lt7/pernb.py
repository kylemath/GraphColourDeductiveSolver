"""Per-neighbour comparison with Studio's case file: inflow range to u from each w_i and u's out-sends to it."""
import sys, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import score, rsst
def mine(priv):
    L, w, S, P, owner = score.layout()
    deg = {0: 7}
    for i in range(7):
        deg[w[i]] = score.LINK[i]; deg[S[i]] = score.SWORD[i]
    for z, p in zip(P, priv): deg[z] = p
    L.add_ring([deg[z] for z in L.rings[2]])
    R3 = L.rings[3]
    for z in R3: deg[z] = None
    M = rsst.Map(score.disc_rot(L), dict(deg))
    outs = M.sends(0)
    res = []
    for i, x in enumerate(w):
        a, b, _ = rsst.inflow_range(M, x, 0, set(R3))
        res.append((sum(1 for y, _ in outs if y == x), a, b))
    return res
mm = 0; n = 0; ex = []
for l in open(os.path.join(HERE, 'studio_lt7_cases_31dc6d2e.txt')):
    if l.startswith('#'): continue
    f = l.split(); n += 1
    st = [tuple(map(int, re.match(r'w\d:out(\d+)/in(\d+)\.\.(\d+)', t).groups())) for t in f[6:13]]
    me = mine(tuple(int(c) for c in f[0]))
    if st != me:
        mm += 1
        if len(ex) < 3: ex.append((f[0], st, me))
print('cases', n, 'per-neighbour mismatches', mm, ex)
