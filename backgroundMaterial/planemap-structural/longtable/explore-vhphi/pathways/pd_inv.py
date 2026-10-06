#!/usr/bin/env python3
"""pd_inv.py -- [exploratory] candidate invariants on ALL x0=0 colourings (link 3 or 4 colours) of G-v for A_2,A_3,A_4,T4 at several
degree-5 holes. status: FILLED (link<=3 colours) / DL (doubly locked) / UNL1 (4-link, exactly one lock fails) / UNL2 (both fail).
Features are in colour-renaming-invariant form. Prints for each feature the value sets per status and whether DL is separated from FILLED."""
import sys, time, collections; from pd_lib import *
t0 = time.time()
def graphs():
    for r, holes in ((2, ['v']), (3, ['v', (0, 0)]), (4, ['v', (0, 0)])):
        adj = build_A(r); fs = faces_from_adj(adj)
        for h in holes: yield 'A_%d@%s' % (r, h), fs, h
    deg = collections.Counter(u for f in T4_FACES for u in f); ndeg = {u: len({w for f in T4_FACES if u in f for w in f if w != u}) for u in range(17)}
    for h in [u for u in range(17) if ndeg[u] == 5]: yield 'T4@%d' % h, T4_FACES, h
def allcols(adj, L):
    V = [u for u in adj if u != 'v']; order = [L[0]]; seen = {L[0]}
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
feat_names = ['ksort', 'ksum', 'ksum%2', 'krel(b;gd,bd,bg)', 'krel%2', 'chains', 'chains%2', 'dist', 'ksum-chains', 'P-cycle len/2 %2']
table = {n: collections.defaultdict(collections.Counter) for n in feat_names}
cnt = collections.Counter()
for name, fs0, hole in graphs():
    adj, fs, L = make_graph(fs0, hole); H = dual(adj, fs); cols, order = allcols(adj, L)
    for col in cols:
        link = [col[x] for x in L]
        e = hole_edges(col, adj, L); tc = tait(col, H)
        cnt_e = collections.Counter(e); beta = [c for c in cnt_e if cnt_e[c] == 3][0]
        singles = [t for t in range(5) if e[t] != beta]; d = (singles[1] - singles[0]) % 5; d = min(d, 5 - d)
        filled = len(set(link)) <= 3
        assert filled == (d == 1)                      # Tait criterion for a filled link
        if filled: st = 'FILLED'
        else:
            l = locks(adj, col, L); st = 'DL' if l == (True, True) else ('UNL1' if True in l else 'UNL2')
        gam, dl = [e[t] for t in singles]
        k = {}
        for s in (1, 2, 3):
            cs = components(H, tc, {1, 2, 3} - {s}); k[s] = sum(1 for c in cs if 'P' not in c)
        kk = tuple(sorted(k.values())); ksum = sum(k.values())
        krel = (k[beta], k[gam ^ beta ^ dl ^ gam] if False else 0)
        # relative: kb = cycles avoiding P in pair excluding beta; kg: excluding gamma; kd: excluding delta
        kr = (k[beta], k[gam], k[dl])
        ch = 0
        for s in (1, 2, 3):
            seen = set()
            for u in order:
                if u in seen: continue
                seen |= comp(adj, col, u, {col[u], col[u] ^ s}); ch += 1
        pc = components(H, tc, {gam, dl})
        pcyc = [c for c in pc if 'P' in c][0]
        vals = {'ksort': kk, 'ksum': ksum, 'ksum%2': ksum % 2, 'krel(b;gd,bd,bg)': kr, 'krel%2': tuple(x % 2 for x in kr),
                'chains': ch, 'chains%2': ch % 2, 'dist': d, 'ksum-chains': ksum - ch, 'P-cycle len/2 %2': (len(pcyc) // 2) % 2}
        # key by graph too so that 'order' dependence is visible for raw counts
        for fn in feat_names: table[fn][st][(name.split('@')[0], vals[fn]) if fn in ('ksum', 'chains', 'ksum-chains') else vals[fn]] += 1
        cnt[(name, st)] += 1
print('[exploratory] state counts by (graph@hole, status):')
agg = collections.Counter()
for (n, s), c in cnt.items(): agg[(n.split('@')[0], s)] += c
for k in sorted(agg): print('  ', k, agg[k])
for fn in feat_names:
    T = table[fn]; vs = {s: set(T[s]) for s in T}
    dl = vs.get('DL', set()); fi = vs.get('FILLED', set()); un = vs.get('UNL1', set()) | vs.get('UNL2', set())
    print('[exploratory] feature %-18s DL values %d, FILLED values %d, UNL values %d; DL∩FILLED=%d, DL∩UNL=%d' % (fn, len(dl), len(fi), len(un), len(dl & fi), len(dl & un)))
    if len(dl) <= 8: print('     DL values:', {v: T['DL'][v] for v in sorted(dl, key=str)})
    if len(dl & fi) <= 6 and dl & fi: print('     shared with FILLED:', {v: (T['DL'][v], T['FILLED'][v]) for v in sorted(dl & fi, key=str)})
print('[exploratory] cpu seconds %.1f' % (time.time() - t0))
