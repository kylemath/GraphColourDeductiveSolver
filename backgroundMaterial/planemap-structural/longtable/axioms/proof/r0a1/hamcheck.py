"""Hamiltonian cycles of a G5 graph through v: count by v-edge pair (adjacent / non-adjacent).
usage: hamcheck.py [graph line file]  (default: C30#0 seeds)"""
import sys
from c30 import from_line, TU

def ham_pairs(g, limit=10**6):
    """count Hamiltonian cycles by the unordered pair of v-edges they use"""
    n = g.n; cnt = {}
    for a in range(5):
        for b in range(a + 1, 5):
            ea, eb = g.fv[a], g.fv[b]
            start, end = g.other(ea, 0), g.other(eb, 0)
            # paths start -> end through all vertices 1..n-1
            vis = [False] * n; vis[0] = True; vis[start] = True; c = 0
            def dfs(x, depth):
                nonlocal c
                if x == end:
                    if depth == n - 1: c += 1
                    return
                for e in g.inc[x]:
                    y = g.other(e, x)
                    if not vis[y]:
                        vis[y] = True; dfs(y, depth + 1); vis[y] = False
            dfs(start, 1)
            cnt[(a, b)] = c
    return cnt

if __name__ == '__main__':
    for i, line in enumerate(open(sys.argv[1] if len(sys.argv) > 1 else TU)):
        if not line.strip(): continue
        g = from_line(line)
        print('line', i, ham_pairs(g))
