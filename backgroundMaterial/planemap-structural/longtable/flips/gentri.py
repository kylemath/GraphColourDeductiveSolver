"""gentri.py -- all sphere triangulations on n vertices (up to isomorphism), by BFS over edge flips
from a double wheel (Wagner: flips connect all triangulations on n vertices).
Output: one line per triangulation: n then for each vertex its clockwise neighbour list (from networkx planar embedding).
Usage: python3 gentri.py n > tri-n.txt   (n <= 10 is quick)"""
import sys, networkx as nx
from networkx.algorithms.graph_hashing import weisfeiler_lehman_graph_hash as wl

def double_wheel(n):
    G = nx.cycle_graph(n - 2)
    for v in range(n - 2):
        G.add_edge(v, n - 2); G.add_edge(v, n - 1)
    return G

def flips(G):
    for u, v in list(G.edges()):
        com = [w for w in G[u] if w in G[v]]
        # in a triangulation (n>=5), the edge uv lies in exactly 2 facial triangles; with separating
        # triangles there can be more common nbrs, so use the embedding
        yield u, v

def main():
    n = int(sys.argv[1])
    if n == 4:
        reps = [nx.complete_graph(4)]
    else:
        start = double_wheel(n)
        reps, buckets, todo = [], {}, [start]
        def add(G):
            h = wl(G, iterations=3)
            for H in buckets.get(h, []):
                if nx.is_isomorphic(G, H): return False
            buckets.setdefault(h, []).append(G); reps.append(G); return True
        add(start)
        while todo:
            G = todo.pop()
            ok, emb = nx.check_planarity(G)
            for u, v in list(G.edges()):
                # faces on both sides of u->v
                a = emb[u][v]['cw']   # neighbour of u clockwise after v
                b = emb[u][v]['ccw']
                if G.degree(u) <= 3 or G.degree(v) <= 3 or G.has_edge(a, b): continue
                H = G.copy(); H.remove_edge(u, v); H.add_edge(a, b)
                if nx.check_planarity(H)[0] and H.number_of_edges() == 3 * n - 6 and add(H):
                    todo.append(H)
    for G in reps:
        ok, emb = nx.check_planarity(G)
        nb = [list(emb.neighbors_cw_order(v)) for v in range(n)]
        print(n, ' '.join(','.join(map(str, l)) for l in nb))
    print(f"# n={n} triangulations={len(reps)}", file=sys.stderr)
main()
