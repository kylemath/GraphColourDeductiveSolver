#!/usr/bin/env python3
"""Track Q: per-state role-ordered pair-graph data (#components, cycle rank) for a graph line and its law R-cycle.
usage: tq_roles.py GRAPHFILE   (prints per state: N, frame j, (#comp/rank) for alpha-mu, AB, alpha-A, mu-B, alpha-B, mu-A)"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from tn_lib import Engine
from tn_forest import parse_dump, cycles_in_R_law, components

def roles(c):
    x = [c[t] for t in range(1, 6)]
    for j in range(5):
        if x[j] == x[(j + 2) % 5]:
            return j, (x[j], x[(j + 1) % 5], x[(j + 3) % 5], x[(j + 4) % 5])

def profile(n, E, c):
    j, (a, m, A, B) = roles(c); out = []
    for (p, q) in ((a, m), (A, B), (a, A), (m, B), (a, B), (m, A)):
        V = [v for v in range(1, n) if c[v] in (p, q)]; Es = [e for e in E if c[e[0]] in (p, q) and c[e[1]] in (p, q)]
        k = len(components(V, Es)); out.append((k, len(Es) - len(V) + k))
    return j, out

if __name__ == '__main__':
    ed = Engine(dump=True, maxstates=400000)
    for l in open(sys.argv[1]):
        p = l.split(); rot = [list(map(int, r.split(','))) for r in p[2].split(';')]
        n = len(rot); E = sorted({tuple(sorted((u, v))) for u in range(1, n) for v in rot[u] if v != 0})
        js, tn, dump = ed.run(l); S = parse_dump(dump)
        for C in cycles_in_R_law(S):
            print(p[0], 'n', n, '|E|', len(E), 'e', len(E) - 3 * (n - 1) + 8)
            for x in C:
                c = [-1 if ch == '-' else int(ch) for ch in S[x]['col']]
                j, pr = profile(n, E, c)
                print('  N', S[x]['N'], 'j', j, ' '.join('%s:%d/%d' % (nm, k, r) for nm, (k, r) in zip(('am', 'AB', 'aA', 'mB', 'aB', 'mA'), pr)))
