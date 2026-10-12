#!/usr/bin/env python3
"""[Track B] Hole-type (link-degree word) analysis of frame-class graphs.
Input: frame.c output files (lines "name n r0;r1;... flags").  For each degree-5 vertex v, its word is the cyclic
sequence of neighbour degrees in rotation order, capped at CAP (CAP means "CAP or more"), canonicalised as the
lexicographically least of the 10 rotations/reflections.  Reports word frequencies, per-graph word sets, which words
are forced (some graph has only that word), and greedy + exact (scipy MILP) minimum hitting sets.
Usage: python3 words.py CAP file [file ...]"""
import sys, collections, itertools
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

def canon(w):
    c = []
    for s in (w, w[::-1]):
        for i in range(len(s)): c.append(tuple(s[i:] + s[:i]))
    return min(c)

def fmt(w, cap):
    return ''.join(str(d) if d < cap else str(cap) + '+' for d in w) if cap < 10 else ','.join(map(str, w))

def load(files):
    G = []
    for f in files:
        for line in open(f):
            p = line.split()
            if len(p) < 3: continue
            rot = [list(map(int, r.split(','))) for r in p[2].split(';')]
            G.append((p[0], int(p[1]), rot))
    return G

def graph_words(rot, cap):
    deg = [len(r) for r in rot]
    ws = []
    for v, r in enumerate(rot):
        if deg[v] == 5: ws.append(canon([min(deg[u], cap) for u in r]))
    return ws

def hitting(sets, universe):
    U = sorted(universe); idx = {w: i for i, w in enumerate(U)}
    # greedy
    rem = list(range(len(sets))); S = []
    while rem:
        best = max(U, key=lambda w: sum(1 for i in rem if w in sets[i]))
        S.append(best); rem = [i for i in rem if best not in sets[i]]
    # exact MILP
    Amat = np.zeros((len(sets), len(U)))
    for i, s in enumerate(sets):
        for w in s: Amat[i, idx[w]] = 1
    res = milp(c=np.ones(len(U)), constraints=LinearConstraint(Amat, lb=1, ub=np.inf), integrality=np.ones(len(U)), bounds=Bounds(0, 1))
    E = [U[i] for i in range(len(U)) if res.x[i] > 0.5]
    return S, E

def main():
    cap = int(sys.argv[1]); G = load(sys.argv[2:])
    byorder = collections.Counter(n for _, n, _ in G)
    print('graphs:', len(G), 'per order:', dict(sorted(byorder.items())))
    freq = collections.Counter(); gfreq = collections.Counter(); sets = []
    for name, n, rot in G:
        ws = graph_words(rot, cap); freq.update(ws); s = frozenset(ws); gfreq.update(s); sets.append(s)
    print('\nword (cap %d+) | #deg-5 vertices | #graphs containing' % cap)
    for w, c in sorted(freq.items(), key=lambda x: -gfreq[x[0]]): print('  %-12s %8d %6d' % (fmt(w, cap), c, gfreq[w]))
    forced = collections.Counter()
    for s in sets:
        if len(s) == 1: forced[next(iter(s))] += 1
    print('\nforced words (graphs whose deg-5 vertices all have one word):', {fmt(w, cap): c for w, c in forced.items()})
    # words whose removal still allows a hitting set: a word is "necessary" iff some graph's set is {w}
    S, E = hitting(sets, set(freq))
    print('greedy hitting set (%d):' % len(S), [fmt(w, cap) for w in S])
    print('exact minimum hitting set (%d):' % len(E), [fmt(w, cap) for w in E])
    # all minimum hitting sets if small
    U = sorted(freq); k = len(E); allmin = []
    if len(U) <= 40 and k <= 4:
        for comb in itertools.combinations(U, k):
            cs = set(comb)
            if all(s & cs for s in sets): allmin.append([fmt(w, cap) for w in comb])
        print('all minimum hitting sets (%d):' % len(allmin)); [print('  ', a) for a in allmin[:50]]
    return G, sets

if __name__ == '__main__':
    main()
