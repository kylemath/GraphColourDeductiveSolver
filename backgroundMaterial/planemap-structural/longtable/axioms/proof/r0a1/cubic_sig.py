"""Side check: total Tait sign sum_w sigma(w) mod 4 over all Tait colourings of some plane cubic graphs."""
import networkx as nx, itertools, collections
def tait_signs(G):
    ok, emb = nx.check_planarity(G); assert ok
    E = list(G.edges()); idx = {frozenset(e): i for i, e in enumerate(E)}
    nodes = list(G.nodes()); out = collections.Counter()
    # 3-edge-colourings by backtracking
    col = {}
    def rec(i):
        if i == len(E):
            s = 0
            for w in nodes:
                r = [col[idx[frozenset((w, u))]] for u in emb.neighbors_cw_order(w)]
                # cw order of colours; sigma = +1 if ccw order is (0,1,2) cyclically
                ccw = r[::-1]; k = ccw.index(0)
                s += 1 if ccw[(k + 1) % 3] == 1 else -1
            out[s % 4] += 1; return
        a, b = E[i]
        for c in range(3):
            if any(col.get(idx[frozenset((x, u))]) == c for x in (a, b) for u in G[x] if idx[frozenset((x, u))] < i):
                continue
            col[i] = c; rec(i + 1); del col[i]
    rec(0); return dict(out)
for name, G in [('K4', nx.complete_graph(4)), ('prism', nx.circular_ladder_graph(3)), ('cube', nx.hypercube_graph(3)),
                ('pentprism', nx.circular_ladder_graph(5)), ('dodeca', nx.dodecahedral_graph())]:
    print(name, G.number_of_nodes(), 'sum sigma mod 4 counts:', tait_signs(G))
