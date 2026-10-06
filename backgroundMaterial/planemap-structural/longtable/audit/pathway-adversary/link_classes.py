#!/usr/bin/env python3
"""P-E adversary for P-A: which degree-5 link classes can a minimum-degree-5 triangulation avoid?
Link class of a degree-5 vertex = cyclic sequence of its neighbours' degrees (7 means >= 7), up to
rotation and reflection. Audit code, plantri ASCII input (spent orders), [exploratory].
usage: link_classes.py FILE..."""
import sys, json
from collections import Counter

def cls(seq):
    seq = [min(d, 7) for d in seq]; c = []
    for s in (seq, seq[::-1]):
        for i in range(5): c.append(tuple(s[i:] + s[:i]))
    return min(c)

out = {}
for path in sys.argv[1:]:
    order = None; per_graph = []; total = Counter()
    for gi, line in enumerate(open(path)):
        if not line.strip(): continue
        n, rest = line.split(); rot = [[ord(ch) - 97 for ch in p] for p in rest.split(',')]
        deg = [len(r) for r in rot]; order = int(n)
        S = {cls([deg[w] for w in rot[x]]) for x in range(order) if deg[x] == 5}
        per_graph.append(sorted(S)); total.update(S)
    n5 = lambda c: sum(1 for d in c if d == 5)
    out[order] = dict(graphs=len(per_graph),
        classes_seen=len(total),
        graphs_without_icosahedral_hole=[i for i, S in enumerate(per_graph) if (5,5,5,5,5) not in S],
        graphs_max_deg5_nbrs={k: sum(1 for S in per_graph if max(n5(c) for c in S) == k) for k in range(6)},
        graphs_without_55_edge=[i for i, S in enumerate(per_graph) if max(n5(c) for c in S) == 0])
print(json.dumps(out, indent=1))
