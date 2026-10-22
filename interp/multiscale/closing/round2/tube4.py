# [P]-check: tube sphere with seam a chordless 4-cycle; level sides that cannot be closed by any bounded band.
import sys, itertools
sys.path.insert(0,'/mnt/project-files/multiscale/closing/round2')
from band import *
def tube(K):
    V = {}; adj = []
    def v(k, i):
        key = (k, i % 4)
        if key not in V: V[key] = len(adj); adj.append(set())
        return V[key]
    def e(a, b): adj[a].add(b); adj[b].add(a)
    for k in range(K+1):
        for i in range(4):
            e(v(k, i), v(k, i+1))
            if k < K: e(v(k, i), v(k+1, i)); e(v(k, i), v(k+1, i-1))
    x = len(adj); adj.append(set()); y = len(adj); adj.append(set()); z = len(adj); adj.append(set())
    for i in (0, 1, 2): e(x, v(0, i))
    for i in (2, 3, 0): e(y, v(0, i))
    e(x, y)
    for i in range(4): e(z, v(K, i))
    return adj, V, x, y, z
def succ(r):
    L = len(r)
    return [r2 for r2 in itertools.product(*[[c for c in range(4) if c != r[k] and c != r[(k+1) % L]] for k in range(L)]) if all(r2[k] != r2[(k+1) % L] for k in range(L))]
for K in (7, 11, 15, 19):
    adj, V, x, y, z = tube(K); T = Tri(adj); l = K//2
    A = set(V[(k, i)] for k in range(l+1) for i in range(4)) | {x, y}; B = set(range(len(adj))) - A
    cA, cB = valid_split(T, A)
    col = {x: 3, y: 1}; r = (0, 1, 2, 3)
    for k in range(l+1):
        for i in range(4): col[V[(k, i)]] = r[i]
        r = succ(r)[0]
    colA = dict(col); col = {}; r = (0, 1, 2, 1)
    for k in range(l+1, K+1):
        for i in range(4): col[V[(k, i)]] = r[i]
        r = succ(r)[-1]
    used = set(col[V[(K, i)]] for i in range(4)); col[z] = min(set(range(4)) - used); colB = col
    assert all(colA[u] != colA[w] for u in A for w in adj[u] if w in A) and all(colB[u] != colB[w] for u in B for w in adj[u] if w in B)
    print('K', K, 'n', len(adj), 'seam m', cA.m, cB.m, 'chords', chords(cA), chords(cB), 'tauA', cA.tau(colA), 'tauB', cB.tau(colB),
          'odd', cA.parity_odd, cB.parity_odd, closing_full(T, A, B, colA, colB, Rmax=K+2), flush=True)
