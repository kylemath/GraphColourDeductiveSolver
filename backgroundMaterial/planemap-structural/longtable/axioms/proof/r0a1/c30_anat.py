"""Anatomy of the C30#0 closed walk: edge usage over the orbit, never-used edges, Q_t connectivity (DL),
loop sizes, and Hamiltonian cycles of G vs the orbit."""
import collections, networkx as nx
from c30 import from_line, TU
from r0lib import analyse
line = open(TU).readline(); g = from_line(line); A = analyse(g)
C = A['cyc'][0]; D = A['D'].subgraph(C); cyc = [min(C)]
while True:
    nx_ = next(iter(D.successors(cyc[-1])))
    if nx_ == cyc[0]: break
    cyc.append(nx_)
P = A['P']; L = len(cyc)
use = collections.Counter()
for x in cyc:
    for e in range(g.m):
        if P[x] >> e & 1: use[e] += 1
print('n', g.n, 'm', g.m, 'L', L, 'edge-use histogram', collections.Counter(use[e] for e in range(g.m)))
never = [g.E[e] for e in range(g.m) if use[e] == 0]
print('never-matched edges:', never)
Gn = nx.Graph(); Gn.add_edges_from(never); print('  they form components:', [sorted(c) for c in nx.connected_components(Gn)])
# Q_t connectivity and out-degrees along the orbit
print('out-degree along orbit:', [A['D'].out_degree(x) for x in cyc])
print('#PM', len(P), '#type-A-with-arcs', sum(1 for x in A['D'].nodes if A['D'].in_degree(x) and A['D'].out_degree(x)))
# usage per v-edge and the five far ends
print('v-edge use:', [use[g.fv[s]] for s in range(5)])
