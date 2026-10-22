# E5: 6-regular toroidal triangulations T(p,q,r) = triangular lattice / <(p,0),(r,q)>.
# 3-colourable? 4-colourable? For 4-colourable ones: can the height periods (t1,t2) both vanish (a globally level
# colouring)? min |t1|, |t2| over 4-colourings.
import itertools, math, json, sys
from pysat.solvers import Cadical153
DIRS = [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]
SG = {(1, 0): 1, (0, 1): -1, (-1, 1): 1, (-1, 0): -1, (0, -1): 1, (1, -1): -1}
INCL = {1: (1, 0), 2: (0, 1), 3: (-1, -1)}   # full-lattice units
def norm2(p): return p[0]*p[0]+p[1]*p[1]-p[0]*p[1]
def torus(p, q, r):
    idx = lambda i, j: (i % p)*q + j
    def nb(i, j, d):
        i2, j2 = i+d[0], j+d[1]
        if j2 >= q: j2 -= q; i2 -= r
        if j2 < 0: j2 += q; i2 += r
        return (i2 % p, j2)
    n = p*q; adj = [set() for _ in range(n)]
    for i in range(p):
        for j in range(q):
            for d in DIRS:
                w = nb(i, j, d); adj[idx(i, j)].add(idx(*w))
    simple = all(len(a) == 6 for a in adj) and all(v not in adj[v] for v in range(n))
    return n, adj, nb, idx, simple
def solve(p, q, r, ncol=4, target=None, D=None):
    n, adj, nb, idx, simple = torus(p, q, r)
    x = lambda v, c: ncol*v+c+1
    cls = []; top = [ncol*n]
    def new(): top[0] += 1; return top[0]
    for v in range(n):
        cls.append([x(v, c) for c in range(ncol)])
        for a, b in itertools.combinations(range(ncol), 2): cls.append([-x(v, a), -x(v, b)])
        for w in adj[v]:
            if w > v:
                for c in range(ncol): cls.append([-x(v, c), -x(w, c)])
    cls.append([x(0, 0)]); cls.append([x(idx(1, 0), 1)])
    if target is not None:
        # loops: L1 = p steps (1,0) from (0,0); L2 = q steps (0,1) then steps (1,0) back to (0,0)
        L1 = [((i, 0), (1, 0)) for i in range(p)]
        L2 = []; cur = (0, 0)
        for _ in range(q): L2.append((cur, (0, 1))); cur = nb(cur[0], cur[1], (0, 1))
        k = (0 - cur[0]) % p
        for _ in range(k): L2.append((cur, (1, 0))); cur = nb(cur[0], cur[1], (1, 0))
        assert cur == (0, 0)
        for L, t in zip((L1, L2), target):
            if t is None: continue
            Dm = D or len(L)
            dom = [(a, b) for a in range(-Dm, Dm+1) for b in range(-Dm, Dm+1) if norm2((a, b)) <= Dm*Dm]
            ds = set(dom)
            H = [{pt: new() for pt in dom} for _ in range(len(L)+1)]
            cls.append([H[0][(0, 0)]])
            for pt in dom:
                if pt != (0, 0): cls.append([-H[0][pt]])   # exactly one start point (bug fix)
            for s, ((i, j), d) in enumerate(L):
                u = idx(i, j); w = idx(*nb(i, j, d)); sg = SG[d]
                Lv = {l: new() for l in (1, 2, 3)}
                for a in range(4):
                    for b in range(4):
                        if a != b: cls.append([-x(u, a), -x(w, b), Lv[a ^ b]])
                for pt in dom:
                    for l in (1, 2, 3):
                        e = INCL[l]; q2 = (pt[0]+sg*e[0], pt[1]+sg*e[1])
                        if q2 in ds: cls.append([-H[s][pt], -Lv[l], H[s+1][q2]])
                        else: cls.append([-H[s][pt], -Lv[l]])
            # forbid every endpoint outside the target set (the genuine endpoint is forced true by the chain)
            if t == 'zero':
                for pt in dom:
                    if pt != (0, 0): cls.append([-H[len(L)][pt]])
            else:
                for pt in dom:
                    if norm2(pt) > t: cls.append([-H[len(L)][pt]])  # |period|^2 <= t
    s = Cadical153(bootstrap_with=cls); ok = s.solve(); s.delete()
    return ok
if __name__ == '__main__':
    out = open('e5_torus.jsonl', 'w')
    seen = set()
    for n in range(7, 61):
        for q in range(1, n+1):
            if n % q: continue
            p = n//q
            for r in range(p):
                N, adj, nb, idx, simple = torus(p, q, r)
                if not simple: continue
                key = tuple(sorted(len(a) for a in adj))
                rec = dict(p=p, q=q, r=r, n=n)
                rec['col3'] = solve(p, q, r, ncol=3)
                rec['col4'] = solve(p, q, r, ncol=4)
                if False and rec["col4"] and not rec["col3"] and n <= 48:  # superseded by e5b_periods.py (earlier encoding was buggy)
                    rec['zero_periods'] = solve(p, q, r, target=('zero', 'zero'))
                    if not rec['zero_periods']:
                        m1 = next(t for t in [1, 3, 4, 7, 9, 12, 13, 16, 19, 21, 25, 27, 28, 31, 36, 100] if solve(p, q, r, target=(t, None)))
                        m2 = next(t for t in [1, 3, 4, 7, 9, 12, 13, 16, 19, 21, 25, 27, 28, 31, 36, 100] if solve(p, q, r, target=(None, t)))
                        rec['min_t1sq'], rec['min_t2sq'] = m1, m2
                if rec['col3'] and n <= 30:
                    rec['zero_periods'] = solve(p, q, r, target=('zero', 'zero'))
                out.write(json.dumps(rec)+'\n'); out.flush()
                if not rec['col4'] or 'min_t1sq' in rec: print(rec, flush=True)
