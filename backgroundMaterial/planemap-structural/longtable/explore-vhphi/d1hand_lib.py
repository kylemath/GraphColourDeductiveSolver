"""EXPLORATORY (D1-Hand). Census of ALL locked members on 17:0 and 17:1 (192). For each member c (a
colouring of T-x, class member of a locked G=T-xy class): word, apex role (M = middle singleton u1,
L = u3, R = u4), whether every chain {c(y),k} is the full colour pair (rigid), per-pair component
count and cyclomatic number in T-x (identity: sum comps - sum cyc = 8), number of legal admitting fans
that are locked for the state.  library: pair_stats"""
import sys, itertools, json
from collections import Counter, deque
import tilley_apex as TA, vhphi_explore as E, sep_any as SA, lock_anatomy as LA, d1hand_swaps as H

def pair_stats(adj, c, x, N):
    out = {}
    for a, b in itertools.combinations(range(4), 2):
        cs, idx = H.comps(adj, c, {a, b}, x)
        V = [w for w in range(N) if w != x and c[w] in (a, b)]
        e = sum(1 for u in V for w in adj[u] if w > u and w != x and c[w] in (a, b))
        out[(a, b)] = (len(cs), e - len(V) + len(cs))   # comps, cyclomatic
    return out


