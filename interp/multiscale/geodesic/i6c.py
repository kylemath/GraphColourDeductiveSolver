# internally 6-connected check: no separating triangles, no induced 4-cycles, every induced 5-cycle is a vertex link.
import sys, itertools
sys.path.insert(0, '/mnt/project-files/multiscale/geodesic'); sys.path.insert(0, '/mnt/project-files/multiscale/hierarchy')
from geo import *
from e1_hier import make
def i6c(g):
    sc = hier.sep_short_cycles(g); adj = g.adj; bad5 = set()
    for u in range(g.n):
        for a, d in itertools.combinations(adj[u], 2):
            if d in adj[a]: continue
            for b in adj[a]:
                if b == u or b in adj[u] or b == d or b in adj[d]: continue
                for c in adj[b] & adj[d]:
                    if c == a or c == u or c in adj[u] or c in adj[a]: continue
                    C = frozenset((u, a, b, c, d))
                    if min(C) != u: continue
                    common = set.intersection(*[adj[x] for x in C])
                    if not any(len(adj[v]) == 5 for v in common): bad5.add(C)
    return dict(n=g.n, sep3=sc['sep3'], ind4=sc['ind4'], nonlink5=len(bad5), maxdeg=max(g.deg))
if __name__ == '__main__':
    for nm in sys.argv[1].split(','):
        print(nm, i6c(G(make(nm))), flush=True)
