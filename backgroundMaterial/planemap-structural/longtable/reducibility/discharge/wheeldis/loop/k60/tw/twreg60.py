"""Round 60: which registry configurations sit inside the triple wheel's closed vertices (tw60.py's patch), and which of
them inside the two-hub window P11 = {u0, u1} + both links (u2 left out)?
usage: python3 twreg60.py TD TC"""
import sys, os
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, '..')); sys.path.insert(0, os.path.join(H, '..', '..', 'k59'))
TD, TC = sys.argv[1:3]; sys.argv = sys.argv[:1]
import tw60, chain59 as C, grow
REG, miss = C.F.registry(TD, TC)
D, U, req = tw60.build()
P = list(range(D.n)); pa = {v: set(D.adj[v]) for v in P}; pf = {frozenset(t) for t in D.tris}; fd = dict(D.deg)
P11 = ({U[0]} | D.adj[U[0]] | {U[1]} | D.adj[U[1]]) - {U[2]}
print('# patch: %d vertices, %d closed; P11 interior %d: %s' % (D.n, len(fd), len(P11), ' '.join(sorted(D.lab[v] for v in P11))))
seen = {}
for c in REG:
    if len(c[2]) > len(P): continue
    for e in grow.embeddings(c, P, pa, pf, fd):
        if any(v not in fd for x, v in e): continue
        img = frozenset(v for x, v in e)
        key = (c[0], img)
        if key in seen: continue
        seen[key] = 1
        print(c[0], 'inside P11' if img <= P11 else 'not inside P11', ' '.join(sorted(D.lab[v] for v in img)))
