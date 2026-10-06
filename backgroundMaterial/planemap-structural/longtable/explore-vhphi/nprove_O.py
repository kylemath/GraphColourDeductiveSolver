"""nprove_O.py: test hypothesis (O) (P13, P14 meet their common vertices in the same order) on every rigid disc of the given files.
P13 = tree path u1 -> u3 in [alpha,beta], P14 = tree path u1 -> u4 in [alpha,gamma] (both pairs are spanning trees for rigid c)."""
import sys
from nprove_lib import *
def path(adj, c, a, b, pair, x):
    prev = {a: None}; st = [a]
    while st:
        u = st.pop()
        for w in adj[u]:
            if w != x and w not in prev and c[w] in pair: prev[w] = u; st.append(w)
    p = []; u = b
    while u is not None: p.append(u); u = prev[u]
    return p[::-1]
for fn in sys.argv[1:]:
    tot = ok = 0; hit = 0
    for line in open(fn):
        if 'DISC' not in line: continue
        col, E = parse(line); x, adj = build(col, E); c = col + [0]
        P13 = path(adj, c, 1, 3, (AL, BE), x); P14 = path(adj, c, 1, 4, (AL, GA), x)
        S = [v for v in P13 if v in set(P14)]
        order14 = [v for v in P14 if v in set(P13)]
        tot += 1; ok += (S == order14)
    print(fn.split('/')[-1], "discs", tot, "(O) holds", ok)
