"""Re-check off-sphere rigid->rigid pi-steps found by rv_h0h3.py with a second, networkx-based
computation (absolute colours, no rv_core component code).  Usage: python3 rv_rr_recheck.py OUT.json [max]"""
import sys
import json
import networkx as nx
import rv_core as R
import rv_surf as S


def nx_state(G, h, x, col):
    vals = [col[v] for v in x]
    js = [j for j in range(5) if vals[j] == vals[(j + 2) % 5] and len({vals[j], vals[(j + 1) % 5], vals[(j + 3) % 5], vals[(j + 4) % 5]}) == 4]
    if len(js) != 1:
        return None
    j = js[0]
    X = [x[(j + k) % 5] for k in range(5)]
    al, mu, A, B = col[X[0]], col[X[1]], col[X[3]], col[X[4]]

    def sub(p, q):
        return G.subgraph([v for v in G if v != h and col[v] in (p, q)])

    def same(p, q, u, v):
        H = sub(p, q)
        return nx.has_path(H, u, v)
    L1 = same(mu, A, X[1], X[3]); L2 = same(mu, B, X[1], X[4])
    inA = same(al, A, X[2], X[0]); inB = same(al, B, X[2], X[0])
    counts = tuple(nx.number_connected_components(sub(p, q)) for p, q in
                   [(al, mu), (A, B), (al, A), (mu, B), (al, B), (mu, A)])
    rigid = L1 and L2 and (L1 == (not inB)) and (L2 == (not inA)) and counts == (1, 1, 2, 1, 2, 1)
    K = nx.node_connected_component(sub(al, A), X[2])
    pi = None
    if not inA:
        pi = list(col)
        for v in K:
            pi[v] = A if col[v] == al else al
    return dict(rigid=rigid, pi=pi, counts=counts)


def main():
    d = json.load(open(sys.argv[1]))
    mx = int(sys.argv[2]) if len(sys.argv) > 2 else 10 ** 9
    found = confirmed = 0
    for F in d['faces']:
        F = [tuple(f) for f in F]
        adj = S.adjacency(F)
        G = nx.Graph([(u, v) for u in range(len(adj)) for v in adj[u]])
        for h in range(len(adj)):
            if len(adj[h]) != 5:
                continue
            x = S.link_cycle(F, h)
            for c in R.colourings(adj, h, canonical=True):
                if not R.is_rigid(adj, h, x, c):
                    continue
                p = R.pi_map(adj, h, x, c)
                if p is None or not R.is_rigid(adj, h, x, p):
                    continue
                found += 1
                a = nx_state(G, h, x, c)
                b = nx_state(G, h, x, a['pi']) if a['pi'] else None
                ok = a['rigid'] and b is not None and b['rigid'] and tuple(a['pi']) == p
                confirmed += ok
                if found >= mx:
                    print(json.dumps(dict(found=found, confirmed=confirmed)))
                    return
    print(json.dumps(dict(found=found, confirmed=confirmed)))


if __name__ == '__main__':
    main()
