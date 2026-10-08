"""Edge-balance (H3 form) at the 10 class states of the counterexample: E1-E2-1, E2-E3 per state."""
import sys
import rv_core as R
name, adj = R.parse_line(open(sys.argv[1]).readline())
h = 0; x = adj[0]; n = len(adj)
edges = [(u, v) for u in range(n) for v in adj[u] if u < v and h not in (u, v)]
print(name, '|E(G-h)| =', len(edges), ' mod 3 =', len(edges) % 3, '(a triangulated surface needs 1)')
for c in R.colourings(adj, h, canonical=True):
    inf = R.state_info(adj, h, x, c)
    if inf is None or not inf['DL'] or inf['inA']:
        continue
    al, mu, A, B = inf['roles']
    P = [({al, mu}, {A, B}), ({al, A}, {mu, B}), ({al, B}, {mu, A})]
    E = [sum(1 for u, v in edges if {c[u], c[v]} <= p or {c[u], c[v]} <= q) for p, q in P]
    print('  E1,E2,E3 =', E, ' E1-E2-1 =', E[0] - E[1] - 1, ' E2-E3 =', E[1] - E[2])
