"""[exploratory] NightPotential: check sum over six pairs of cycle rank = (sum of component counts) - 8 on every 4-colouring of T - h,
h of degree 5, gentri orders 12-17 (all graphs, all degree-5 holes); and the DL duality rank_ab = C_cd - 1 - [ab is a lock pair]."""
import sys, os, itertools
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../30-nighta34'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../common'))
from eng import graphs
from kempe_py import Space, adj_from_rot
from collections import Counter
PAIRS = list(itertools.combinations(range(4), 2)); T = Counter()
for n in (12, 14, 16, 17):
    for gi, rot in graphs(n):
        for h in range(len(rot)):
            if len(rot[h]) != 5: continue
            sp = Space(adj_from_rot(rot), h, link=rot[h]); N = sp.N
            nb = [[sp.idx[u] for u in rot[sp.order[i]] if u != h] for i in range(N)]
            E = [(u, v) for u in range(N) for v in nb[u] if u < v]; X = [sp.idx[x] for x in rot[h]]
            for c in sp.states:
                rk = {}; nc = {}
                for a, b in PAIRS:
                    seen = set(); k = 0
                    for v in range(N):
                        if c[v] in (a, b) and v not in seen:
                            st = [v]; seen.add(v); k += 1
                            while st:
                                u = st.pop()
                                for t in nb[u]:
                                    if t not in seen and c[t] in (a, b): seen.add(t); st.append(t)
                    nc[(a, b)] = k
                    rk[(a, b)] = sum(1 for u, v in E if c[u] in (a, b) and c[v] in (a, b)) - sum(1 for v in range(N) if c[v] in (a, b)) + k
                T[('sum rank - sum comp', sum(rk.values()) - sum(nc.values()))] += 1
                T['states'] += 1
    print(n, dict(T), flush=True)
