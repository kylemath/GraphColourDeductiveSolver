#!/usr/bin/env python3
"""pd2_runs.py -- [exploratory, these graphs only] do shortest fills follow pure F-runs or pure F'-runs?
F  = swap of the {c(x_j), c(x_{j+3})}-chain of x_{j+2} (astruct_core.F);
F' = mirror: swap of the {c(x_j), c(x_{j+4})}-chain of x_j.  tau_F(s) = least n with F^n s not doubly locked (cap 40).
Test: radius(s) == 1 + min(tau_F, tau_F') on DL states, T4 / A_3 / A_4 (all degree-5 holes)."""
import sys, time
from collections import Counter
sys.path.insert(0, '.')
from pd2_lib import *
t0 = time.process_time()
def Fm(adj, col, L):
    j = repeat_index(col, L); x0, m, x2, a, b = roles(L, j)
    K = comp(adj, col, x0, {col[x0], col[b]}); al, c = col[x0], col[b]
    return {u: ((c if col[u] == al else al) if u in K else col[u]) for u in col}
def tau(g, c, step, cap=40):
    n = 0
    while n < cap and not g.filled(c) and doubly(g.adj, c, g.L): c = step(g.adj, c, g.L); n += 1
    return n if n < cap else None
for grp in ('T4', 'A_3', 'A_4'):
    tab = Counter(); ex = None
    for g in graphs((grp,)):
        st = g.all_states(); dist, byk, nb = dist_to_fill(g, st)
        for k, c in byk.items():
            if g.filled(c) or not doubly(g.adj, c, g.L): continue
            a, b = tau(g, c, F), tau(g, c, Fm)
            pred = 1 + min(x for x in (a, b, 10**6) if x is not None)
            tab[(dist[k], a, b, dist[k] == pred)] += 1
            if dist[k] != pred and ex is None: ex = (g.name, k, dist[k], a, b)
    ok = sum(v for kk, v in tab.items() if kk[3]); tot = sum(tab.values())
    print('[exploratory]', grp, 'DL states', tot, '| radius == 1+min(tau_F,tau_F\') on', ok, '| first failure', ex)
    print('   (radius, tau_F, tau_F\', match) -> count:', dict(sorted(tab.items(), key=str)))
print('cpu %.1f s' % (time.process_time() - t0))
