"""Side check: relation between the Tait sign sum and the Kempe cycle counts c12+c13+c23 on plane cubic graphs."""
import networkx as nx, collections
def data(G):
    ok, emb = nx.check_planarity(G)
    E = list(G.edges()); idx = {frozenset(e): i for i, e in enumerate(E)}
    nodes = list(G.nodes()); rows = collections.Counter(); col = {}
    def rec(i):
        if i == len(E):
            s = 0
            for w in nodes:
                ccw = [col[idx[frozenset((w, u))]] for u in emb.neighbors_cw_order(w)][::-1]
                k = ccw.index(0); s += 1 if ccw[(k + 1) % 3] == 1 else -1
            cs = []
            for a, b in ((0, 1), (0, 2), (1, 2)):
                H = nx.Graph(); H.add_edges_from(E[j] for j in range(len(E)) if col[j] in (a, b))
                cs.append(nx.number_connected_components(H))
            rows[(s, sum(cs))] += 1; return
        a, b = E[i]
        for c in range(3):
            if any(col.get(idx[frozenset((x, u))]) == c for x in (a, b) for u in G[x] if idx[frozenset((x, u))] < i): continue
            col[i] = c; rec(i + 1); del col[i]
    rec(0); return dict(rows)
for name, G in [('K4', nx.complete_graph(4)), ('prism', nx.circular_ladder_graph(3)), ('cube', nx.hypercube_graph(3)),
                ('pentprism', nx.circular_ladder_graph(5)), ('dodeca', nx.dodecahedral_graph())]:
    print(name, G.number_of_nodes(), '(sum sigma, c12+c13+c23): count', data(G))
