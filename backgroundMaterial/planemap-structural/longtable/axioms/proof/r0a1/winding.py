"""Per-vertex windings along the closed walk(s) of D on the planar C30#0 graphs (rotation from a planar
embedding of the 5-wheel gadget).  rho(w) = (sum over steps of the notch rotation M_t(w) -> M_{t+1}(w),
+1 = ccw) / 3.  Also the Tait signs.  usage: winding.py"""
import networkx as nx
from c30 import from_line, TU
from r0lib import analyse

for li, line in enumerate(open(TU)):
    if not line.strip(): continue
    g = from_line(line); A = analyse(g)
    gg = g.gadget(); ok, emb = nx.check_planarity(gg)
    # rotation at cubic vertex w: neighbours in emb order; map to edge ids
    base = g.n
    def edge_to(w, u):
        if u >= base:   # rim vertex = f_{u-base}
            return g.fv[u - base]
        return next(e for e in g.inc[w] if g.other(e, w) == u)
    rot = {w: [edge_to(w, u) for u in emb.neighbors_cw_order(w)] for w in range(1, g.n)}
    # v rotation direction relative to the embedding: rim order
    rim = [u - base for u in emb.neighbors_cw_order(base + 5)]
    for C in A['cyc']:
        # extract the cycle order
        D = A['D'].subgraph(C); start = min(C); cyc = [start]
        while True:
            nx_ = list(D.successors(cyc[-1]))
            assert len(nx_) == 1, nx_
            if nx_[0] == start: break
            cyc.append(nx_[0])
        L = len(cyc); P = A['P']
        rho = {}; sig_tot = 0
        for w in range(1, g.n):
            r = rot[w]; tot = 0
            for t in range(L):
                a = next(e for e in g.inc[w] if P[cyc[t]] >> e & 1)
                b = next(e for e in g.inc[w] if P[cyc[(t + 1) % L]] >> e & 1)
                d = (r.index(b) - r.index(a)) % 3   # cw steps in cw order
                tot += 1 if d == 1 else -1
            rho[w] = -tot / 3   # ccw positive
        print(f'line {li}: L={L}, v-frames {[A["ks"][x] for x in cyc[:10]]}..., hub cw rim order {rim}')
        print('   windings rho(w), w = 1..n-1:', [rho[w] for w in range(1, g.n)], ' sum', sum(rho.values()))
