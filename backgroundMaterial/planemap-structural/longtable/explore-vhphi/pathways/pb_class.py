"""[exploratory] link degree multisets of deg-5 vertices; D5-reach of (6^5)/(5^5) holes."""
from collections import Counter
from pb_lib import *
from pb_struct import hexanti, gc20
for name, adj in [('T4', from_faces(T4F)), ('A_3', a3()[0]), ('order14', hexanti()), ('GC20 (42)', gc20())]:
    deg = {u: len(adj[u]) for u in adj}
    cl = Counter(tuple(sorted(deg[w] for w in adj[u])) for u in adj if deg[u] == 5)
    print(f"[exploratory] {name}: link multiset classes of deg-5 holes: {dict(cl)}")
    print("   (6^5) holes with a deg-5 neighbour:", sum(1 for u in adj if deg[u]==5 and set(deg[w] for w in adj[u])=={6} and any(deg[w]==5 for w in adj[u])))
