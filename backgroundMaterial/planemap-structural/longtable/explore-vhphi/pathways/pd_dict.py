#!/usr/bin/env python3
"""pd_dict.py -- [exploratory] verifies the dictionary on A_2,A_3,A_4,T4 states: proper Tait colouring, lock criterion by P-paths,
Kempe chain swap == swap on all cycles of its cut. Prints counts."""
import sys; from pd_lib import *
def graphs():
    for r in (2, 3, 4):
        adj = build_A(r); fs = faces_from_adj(adj); assert len(fs) == 2 * len(adj) - 4
        yield 'A_%d' % r, adj, fs, 'v'
    yield 'T4', None, T4_FACES, 4
for name, adj0, fs0, hole in graphs():
    adj, fs, L = make_graph(fs0, hole); H = dual(adj, fs)
    cols, order = colourings(adj, L)
    n_ok = n_lock = n_pairmatch = 0; swapok = 0; swaptot = 0
    for col in cols:
        check_tait(col, H); n_ok += 1
        j = repeat_index(col, L)
        if j is None: continue
        x0, m, x2, a, b = roles(L, j)
        e = hole_edges(col, adj, L)
        # lock criterion via paths: gamma path from e_{j+2} must end at e_{j+1}; delta path from e_{j+4} at e_j
        tc = tait(col, H)
        beta = e[j]; gam = e[(j + 2) % 5]; dl = e[(j + 4) % 5]
        assert e[(j + 1) % 5] == beta and e[(j + 3) % 5] == beta
        pg = p_paths(H, tc, L, adj, {beta, gam}); pdl = p_paths(H, tc, L, adj, {beta, dl})
        lk1 = pg[(j + 2) % 5] == (j + 1) % 5; lk2 = pdl[(j + 4) % 5] == j
        l = locks(adj, col, L)
        n_pairmatch += (l == (lk1, lk2))
        # chain swap vs cycle-swap: translate chain by s; edge colours change exactly on cut edges (colours != s)
        for s in (1, 2, 3):
            seen = set()
            for u in order:
                if u in seen: continue
                pair = {col[u], col[u] ^ s}
                C = comp(adj, col, u, pair); seen |= C
                new = dict(col)
                for w in C: new[w] = col[w] ^ s
                tn = tait(new, H)
                diff = {ed for ed in H if tn[ed] != tc[ed]}
                cut = {ed for ed in H if len(ed & C) == 1}
                swaptot += 1
                swapok += (diff == cut and all(tc[ed] != s and tn[ed] == tc[ed] ^ s for ed in cut))
    print('[exploratory]', name, 'states', len(cols), 'tait-proper', n_ok, 'lock-by-P-paths == locks()', n_pairmatch,
          '| chain swaps checked', swaptot, 'cut-edge identity ok', swapok)
