#!/usr/bin/env python3
"""pd_finv.py -- [exploratory] Is a Tait feature invariant under F (also F^2, F^4 mod renaming)? Every 4-colour-link state with unique
repeat index of A_3@v, A_3@(0,0), A_4@v, T4@all deg-5 holes. Features: closed-cycle counts (k_1,k_2,k_3) sorted, ksum, ksum mod 2,
vertex-chain counts, the pairing of P-ends. Also the identity chains - ksum per status."""
import sys, collections; from pd_lib import *
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
    rec(1); return out, order
def graphs():
    for r, holes in ((3, ['v', (0, 0)]), (4, ['v'])):
        adj = build_A(r); fs = faces_from_adj(adj)
        for h in holes: yield 'A_%d@%s' % (r, h), fs, h
    ndeg = {u: len({w for f in T4_FACES if u in f for w in f if w != u}) for u in range(17)}
    for h in [u for u in range(17) if ndeg[u] == 5]: yield 'T4@%d' % h, T4_FACES, h
tot = collections.Counter(); chg = collections.Counter(); idv = collections.defaultdict(collections.Counter)
for name, fs0, hole in graphs():
    adj, fs, L = make_graph(fs0, hole); H = dual(adj, fs); cols, order = allcols(adj, L)
    def feats(col):
        tc = tait(col, H); k = []
        for s in (1, 2, 3):
            cs = components(H, tc, {1, 2, 3} - {s}); k.append(sum(1 for c in cs if 'P' not in c))
        ch = 0
        for s in (1, 2, 3):
            seen = set()
            for u in order:
                if u in seen: continue
                seen |= comp(adj, col, u, {col[u], col[u] ^ s}); ch += 1
        return {'ksort': tuple(sorted(k)), 'ksum': sum(k), 'ksum%2': sum(k) % 2, 'chains': ch, 'chains%2': ch % 2}
    for col in cols:
        link = [col[x] for x in L]
        if len(set(link)) != 4 or repeat_index(col, L) is None: continue
        l = locks(adj, col, L); st = 'DL' if l == (True, True) else 'notDL'
        f0 = feats(col); idv[st][f0['chains'] - f0['ksum']] += 1
        for steps in (1, 2):
            s = col
            for _ in range(steps):
                if len({s[x] for x in L}) != 4 or repeat_index(s, L) is None: s = None; break
                s = F(adj, s, L)
            if s is None: continue
            f1 = feats(s)
            for fn in f0:
                tot[(steps, st, fn)] += 1; chg[(steps, st, fn)] += (f0[fn] != f1[fn])
print('[exploratory] fraction of states where the feature CHANGES under F^steps (DL = state is doubly locked):')
for steps in (1, 2):
    for st in ('DL', 'notDL'):
        print('  F^%d %-5s' % (steps, st), {fn: '%d/%d' % (chg[(steps, st, fn)], tot[(steps, st, fn)]) for fn in ('ksort', 'ksum', 'ksum%2', 'chains', 'chains%2')})
print('[exploratory] identity test: chains - ksum by status:', {k: dict(v) for k, v in idv.items()})
