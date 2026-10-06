#!/usr/bin/env python3
"""pd_orbit.py -- [exploratory] A_3 witness F-orbit (raw period 60) in Tait terms. Prints per step: link colours, hole steps e_t,
repeat index j, P-path pairing of the gamma-end / delta-end, cycle counts k_s (cycles of the 2-factor avoiding P, per excluded colour s),
swap size and number of Kempe cycles in the cut of the swapped chain."""
import sys; from pd_lib import *
sys.path.insert(0, '..')
import lattack_witness as W
r = 3; adj = build_A(r); fs = faces_from_adj(adj)
adj, fs, L = make_graph(fs, 'v'); H = dual(adj, fs)
col = {}
for i in range(r):
    for t in range(5): col[(i, t)] = W.A3_COL[1 + 5 * i + t]
col['c'] = W.A3_COL[16]
order = [u for u in adj if u != 'v']
def kvec(col):
    tc = tait(col, H); out = []
    for s in (1, 2, 3):
        cs = components(H, tc, {1, 2, 3} - {s})
        out.append(sum(1 for c in cs if 'P' not in c))   # closed Kempe cycles not through P
    return tuple(out)
def ncyc(edges, H):
    # number of connected components of the edge set 'edges' in H
    nb = {}
    for e in edges:
        p, q = H[e]; nb.setdefault(p, set()).add(q); nb.setdefault(q, set()).add(p)
    seen = set(); k = 0
    for n in nb:
        if n in seen: continue
        k += 1; st = [n]; seen.add(n)
        while st:
            u = st.pop()
            for w in nb[u]:
                if w not in seen: seen.add(w); st.append(w)
    return k
seenstate = {}; s = dict(col); rows = []
for step in range(62):
    k = tuple(s[u] for u in order)
    if k in seenstate: print('[exploratory] raw state repeats: step', step, '== step', seenstate[k], '(period', step - seenstate[k], ')'); break
    seenstate[k] = step
    check_tait(s, H); j = repeat_index(s, L); x0, m, x2, a, b = roles(L, j)
    e = hole_edges(s, adj, L); tc = tait(s, H)
    beta = e[j]; gam = e[(j + 2) % 5]; dl = e[(j + 4) % 5]
    pg = p_paths(H, tc, L, adj, {beta, gam}); pd = p_paths(H, tc, L, adj, {beta, dl})
    lk = locks(adj, s, L)
    # F swap: chain of x2 in colours {c(x0), c(a)}; translation t = c(x0)^c(a) = gamma
    K = comp(adj, s, x2, {s[x0], s[a]}); cut = {ed for ed in H if len(ed & K) == 1}
    # relative colours: rename Tait colours so beta->A, gam->B, dl->C
    rn = {beta: 'A', gam: 'B', dl: 'C'}
    erel = ''.join(rn[x] for x in e)
    print('[exploratory] step %2d j=%d e(rel to beta,gamma,delta)=%s gamma-path e%d->e%d delta-path e%d->e%d locks=%s k=(%s) |K|=%d cut=%d edges in %d Kempe cycle(s)'
          % (step, j, erel, (j + 2) % 5 - j, (pg[(j + 2) % 5] - j) % 5, (j + 4) % 5 - j, (pd[(j + 4) % 5] - j) % 5, lk, ','.join(map(str, kvec(s))), len(K), len(cut), ncyc(cut, H)))
    s = F(adj, s, L)
