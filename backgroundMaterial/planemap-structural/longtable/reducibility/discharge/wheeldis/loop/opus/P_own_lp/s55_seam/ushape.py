# Seam-lemma counterexample test: U-shaped rigid strip P_N^3 (uniquely 4-colourable), legs in A, bottom in B,
# A's legs joined at the top by a flexible P^2 band. For each R and each of 24 renamings of B, ask whether a proper
# colouring of the union exists agreeing with A and pi(B) outside the R-neighbourhood of the seam.
import itertools, sys
from collections import deque
def build(R):
    L = 3*R + 12; M = 8; N = 2*L + M
    E = set(); side = {}
    for i in range(N):
        side[i] = 'B' if L <= i < L+M else 'A'
        for j in range(i+1, min(N, i+4)): E.add((i, j))
    K = 6; c = [N + k for k in range(K)]
    seq = [1, 0] + c + [N-1, N-2]          # P^2 band 1,0,c0..c5,N-1,N-2 (A only)
    for v in c: side[v] = 'A'
    for a in range(len(seq)):
        for b in range(a+1, min(len(seq), a+3)):
            u, v = sorted((seq[a], seq[b]))
            E.add((u, v))
    V = list(range(N + K))
    adj = {v: set() for v in V}
    for u, v in E: adj[u].add(v); adj[v].add(u)
    return V, adj, side, N
def colour(V, adj, fixed, order=None):
    col = dict(fixed); free = [v for v in (order or V) if v not in col]
    for v in V:
        if v in col and any(col.get(w) == col[v] for w in adj[v] if w in col): return None
    def bt(k):
        if k == len(free): return True
        v = free[k]
        for x in range(4):
            if all(col.get(w) != x for w in adj[v]):
                col[v] = x
                if bt(k+1): return True
                del col[v]
        return False
    return dict(col) if bt(0) else None
for R in map(int, sys.argv[1:] or ['2','4','6']):
    V, adj, side, N = build(R)
    A = [v for v in V if side[v] == 'A']; B = [v for v in V if side[v] == 'B']
    L = 3*R + 12
    # A colouring: leg1 = i mod 4; leg2 must be a different twist than the union's forced i mod 4
    Aadj = {v: {w for w in adj[v] if side[w] == 'A'} for v in A}
    fixA = {i: i % 4 for i in range(L)}
    cA = None
    for perm in itertools.permutations(range(4)):
        if perm == (0, 1, 2, 3): continue
        fx = dict(fixA); fx.update({i: perm[i % 4] for i in range(L+8, N)})
        cA = colour(A, Aadj, fx)
        if cA: break
    assert cA, 'no wrong-twist colouring of A'
    Badj = {v: {w for w in adj[v] if side[w] == 'B'} for v in B}
    cB = colour(B, Badj, {})
    seamv = {v for v in V for w in adj[v] if side[v] != side[w]}
    dist = {v: 0 for v in seamv}; q = deque(seamv)
    while q:
        v = q.popleft()
        for w in adj[v]:
            if w not in dist: dist[w] = dist[v] + 1; q.append(w)
    far = [v for v in V if dist[v] > R]
    ok = 0
    for pi in itertools.permutations(range(4)):
        fx = {v: (cA[v] if side[v] == 'A' else pi[cB[v]]) for v in far}
        if colour(V, adj, fx): ok += 1
    print(f'R={R}: |V|={len(V)} seam vertices={len(seamv)} far(fixed)={len(far)} wrong twist used={perm}; renamings that work: {ok}/24; union 4-colourable: {colour(V, adj, {}) is not None}')
