#!/usr/bin/env python3
"""pd_cross.py -- [exploratory] shape of a Tait lock: Z1 = (beta,gamma)-cycle through P pairing e_{j+2},e_{j+1}; Z2 = (beta,delta)-cycle
through P pairing e_{j+4},e_j. Histogram over all doubly locked link-4 states (A_3@v,(0,0); A_4@v; T4@deg-5 holes) of the node counts of
Z1, Z2 and of shared non-P nodes (any shared edge is a beta edge)."""
import collections; from pd_lib import *
def allcols(adj, L):
    order = [L[0]]; seen = {L[0]}
    for u in order:
        for w in sorted(adj[u], key=str):
            if w != 'v' and w not in seen: seen.add(w); order.append(w)
    col = {L[0]: 0}; out = []
    def rec(i):
        if i == len(order): out.append(dict(col)); return
        u = order[i]; used = {col[w] for w in adj[u] if w in col}
        for c in range(4):
            if c not in used: col[u] = c; rec(i + 1); del col[u]
    rec(1); return out
def cyc_nodes(H, tc, pair, e0):
    inc = {}
    for e, (p, q) in H.items(): inc.setdefault(p, []).append((e, q)); inc.setdefault(q, []).append((e, p))
    nodes = []; cur = e0; node = [q for (e, q) in inc['P'] if e == e0][0]; edges = [e0]
    while node != 'P':
        nodes.append(node); w = [e for (e, q) in inc[node] if tc[e] in pair and e != cur][0]
        cur = w; edges.append(w); node = [q for (e, q) in inc[node] if e == w][0]
    return nodes, edges
ndeg = {u: len({w for f in T4_FACES if u in f for w in f if w != u}) for u in range(17)}
gs = [('A_3@v', faces_from_adj(build_A(3)), 'v'), ('A_3@(0,0)', faces_from_adj(build_A(3)), (0, 0)), ('A_4@v', faces_from_adj(build_A(4)), 'v')]
gs += [('T4@%d' % h, T4_FACES, h) for h in range(17) if ndeg[h] == 5]
hist = collections.Counter(); n = 0
for name, fs0, hole in gs:
    adj, fs, L = make_graph(fs0, hole); H = dual(adj, fs)
    pe = {t: frozenset((L[t], L[(t + 1) % 5])) for t in range(5)}
    for col in allcols(adj, L):
        if len({col[x] for x in L}) != 4 or repeat_index(col, L) is None: continue
        if locks(adj, col, L) != (True, True): continue
        j = repeat_index(col, L); tc = tait(col, H); e = hole_edges(col, adj, L)
        b, g, d = e[j], e[(j + 2) % 5], e[(j + 4) % 5]
        n1, e1 = cyc_nodes(H, tc, {b, g}, pe[(j + 2) % 5]); n2, e2 = cyc_nodes(H, tc, {b, d}, pe[(j + 4) % 5])
        sh = len(set(n1) & set(n2)); she = len(set(e1) & set(e2))
        assert all(tc[x] == b for x in set(e1) & set(e2))
        hist[(len(n1) + 1, len(n2) + 1, sh, she)] += 1; n += 1
print('[exploratory] doubly locked states:', n, ' key = (len Z1, len Z2, shared non-P nodes, shared edges)')
for k in sorted(hist): print('  ', k, hist[k])
