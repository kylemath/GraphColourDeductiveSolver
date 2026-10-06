"""nprove_members.py: per-member data of the D'-free class (order <= 17 lines or the given res_23 lines).
Per member: distance, good?, comps and cyclomatic numbers of all six pairs, m_pq (ring-containing comps)."""
import sys
from nprove_lib import *
fn = sys.argv[1]; which = int(sys.argv[2]); nm = sys.argv[3]
line = [l for l in open(fn) if 'DISC' in l][which]
col, E = parse(line); x, adj = build(col, E)
cp, cpp, K2, K0 = neighbours_cprime(adj, x, col + [0])
c0, apex = (cp, 0) if nm == "c'" else (cpp, 2)
dist, rep, g = dfree_class(adj, x, c0, apex)
P6 = [(D,AL),(D,BE),(D,GA),(AL,BE),(AL,GA),(BE,GA)]
ids = {k: i for i, k in enumerate(sorted(dist, key=lambda k: (dist[k], k)))}
for k in sorted(dist, key=lambda k: ids[k]):
    c = rep[k]; row = []
    for p in P6:
        cs, ix = comps(adj, c, p, x)
        V = sum(1 for v in range(x) if c[v] in p)
        Ee = sum(1 for u in range(x) for w in adj[u] if w != x and u < w and c[u] in p and c[w] in p)
        cyc = Ee - V + len(cs)
        m = len({ix[r] for r in range(5) if c[r] in p})
        row.append((len(cs), cyc, m))
    ring = ''.join(str(c[r]) for r in range(5))
    print(ids[k], "d", dist[k], "ring", ring, "good" if chain_broken(adj, x, c, apex) else "    ", "comps/cyc/m for", [ (a,b) for a,b in P6], row, "nbrs", sorted(ids[h] for h in g[k]))
