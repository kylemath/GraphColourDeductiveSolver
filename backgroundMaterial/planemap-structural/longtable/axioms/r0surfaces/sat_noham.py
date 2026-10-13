"""Variant (a): R0 frame WITHOUT the Hamiltonian pair, WITH planarity (Long Table, r0surfaces).

Question: for which n, L does a simple plane G (v of degree 5, others cubic) carry a closed sequence of
perfect matchings M_0..M_{L-1}, M_t n M_{t+1} = 0 cyclically, v-edge of M_t = f_{k0 - 2t}, with no
Hamiltonian condition on the M's?

Encoding: G is assumed Hamiltonian (any Hamiltonian cycle H of G, unrelated to the M's): H = 0..n-1, v = 0,
G = H + chords.  H passes v through two v-edges at rotation distance 2 (case A: (0,1) = f2, (0,n-1) = f0)
or 1 (case B: (0,1) = f1, (0,n-1) = f0); every other placement is a label shift (absorbed by k0 in 0..4) or a
reflection of H.  Planarity with the rotation f0..f4 (up to mirror) = two-sided non-crossing chord diagram on
the circle 1..n-1 with v blown up between n-1 and 1 (virtual points), as in sat_planar.py:
   case A: points [f4] [f1] [f3], side(f1) != side(f3) = side(f4)      (= PROOF-ATTEMPT-1 rule)
   case B: points [f4] [f3] [f2], side(f2) = side(f3) = side(f4)
(derivation in R0-SCOPE.md section 3).  Pure SAT (CaDiCaL), no CEGAR.
usage: sat_noham.py n L [case A|B|both] [tlimit] [--adv a] [--verify] [--show]   (a = frame advance, default -2)"""
import sys, time, json
from pysat.formula import IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical153

n, L = int(sys.argv[1]), int(sys.argv[2])
cases = sys.argv[3] if len(sys.argv) > 3 else 'both'
tlim = float(sys.argv[4]) if len(sys.argv) > 4 else 550
cases = ['A', 'B'] if cases == 'both' else [cases]
ADV = int(sys.argv[sys.argv.index('--adv') + 1]) if '--adv' in sys.argv else -2


def build(case, k0):
    P = IDPool(); cl = []
    def eq(lits, k):
        for c in CardEnc.equals(lits=lits, bound=k, vpool=P, encoding=EncType.seqcounter).clauses: cl.append(c)
    edges = [(i, (i + 1) % n) for i in range(n)]
    Hs = set(range(n))
    for i in range(n):
        for j in range(i + 2, n):
            if i == 0 and j == n - 1: continue
            edges.append((i, j))
    m = len(edges); inc = [[] for _ in range(n)]
    for e, (a, b) in enumerate(edges): inc[a].append(e); inc[b].append(e)
    X = {e: (None if e in Hs else P.id(('x', e))) for e in range(m)}
    for u in range(n): eq([X[e] for e in inc[u] if X[e] is not None], 3 if u == 0 else 1)
    vE = inc[0]; e01 = 0; e0n = n - 1
    lab = {s: {e: P.id(('lab', s, e)) for e in vE} for s in range(5)}
    fixed = {'A': {2: e01, 0: e0n}, 'B': {1: e01, 0: e0n}}[case]
    free = [s for s in range(5) if s not in fixed]
    for s, e in fixed.items():
        cl.append([lab[s][e]])
        for e2 in vE:
            if e2 != e: cl.append([-lab[s][e2]])
    for s in free:
        cl.append([-lab[s][e01]]); cl.append([-lab[s][e0n]])
        eq([lab[s][e] for e in vE if X[e] is not None], 1)
        for e in vE:
            if X[e] is not None: cl.append([-lab[s][e], X[e]])
    for e in vE:
        if X[e] is None: continue
        ls = [lab[s][e] for s in free]
        cl.append([-X[e]] + ls)
        for i in range(len(ls)):
            for j in range(i + 1, len(ls)): cl.append([-ls[i], -ls[j]])
    Y = {(t, e): P.id(('y', t, e)) for t in range(L) for e in range(m)}
    for t in range(L):
        for u in range(n): eq([Y[t, e] for e in inc[u]], 1)
        for e in range(m):
            if X[e] is not None: cl.append([-Y[t, e], X[e]])
            cl.append([-Y[t, e], -Y[(t + 1) % L, e]])
        k = (k0 + ADV * t) % 5
        for e in vE:
            cl.append([-lab[k][e], Y[t, e]]); cl.append([lab[k][e], -Y[t, e]])
    # planarity
    VPOS = {'A': {4: .25, 1: .5, 3: .75}, 'B': {4: .25, 3: .5, 2: .75}}[case]
    sl = {s: P.id(('vside', s)) for s in VPOS}
    if case == 'A':
        cl += [[sl[1], sl[3]], [-sl[1], -sl[3]], [-sl[3], sl[4]], [sl[3], -sl[4]]]
    else:
        cl += [[-sl[2], sl[3]], [sl[2], -sl[3]], [-sl[3], sl[4]], [sl[3], -sl[4]]]
    items = []
    for e, (a, b) in enumerate(edges):
        if e in Hs or a == 0: continue
        items.append((a, b, [X[e]], P.id(('side', e))))
    for e in vE:
        if X[e] is None: continue
        j = edges[e][1]
        for s in VPOS: items.append((j, n + VPOS[s], [lab[s][e]], sl[s]))
    def cross(a1, b1, a2, b2):
        a1, b1 = sorted((a1, b1)); a2, b2 = sorted((a2, b2))
        return (a1 < a2 < b1) != (a1 < b2 < b1)
    for i in range(len(items)):
        a1, b1, l1, s1 = items[i]
        for j in range(i + 1, len(items)):
            a2, b2, l2, s2 = items[j]
            if len({a1, b1, a2, b2}) < 4 or not cross(a1, b1, a2, b2): continue
            pre = [-x for x in l1 + l2]
            if s1 == s2: cl.append(pre); continue
            cl.append(pre + [s1, s2]); cl.append(pre + [-s1, -s2])
    return cl, edges, X, Y, lab, vE


def ncomp(S, edges):
    par = list(range(n))
    def f(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    c = n
    for e in S:
        a, b = edges[e]; ra, rb = f(a), f(b)
        if ra != rb: par[ra] = rb; c -= 1
    return c


t0 = time.time(); found = None
for case in cases:
    for k0 in range(5):
        cl, edges, X, Y, lab, vE = build(case, k0)
        s = Cadical153(bootstrap_with=cl)
        r = s.solve()
        if r:
            S = set(x for x in s.get_model() if x > 0)
            E = [e for e in range(len(edges)) if X[e] is None or X[e] in S]
            M = [[e for e in E if Y[t, e] in S] for t in range(L)]
            fv = [next(e for e in vE if lab[sx][e] in S) for sx in range(5)]
            comps = [ncomp(set(M[t]) | set(M[(t + 1) % L]), edges) for t in range(L)]
            per = next(p for p in range(1, L + 1) if all(set(M[t]) == set(M[(t + p) % L]) for t in range(L)))
            found = dict(case=case, k0=k0, comps=comps, period=per,
                         line=' '.join(map(str, [n, len(E)] + [x for e in E for x in edges[e]] + [E.index(f) for f in fv])),
                         M=[[edges[e] for e in Mt] for Mt in M])
            break
        if time.time() - t0 > tlim: break
    if found: break
print(json.dumps(dict(n=n, L=L, cases=cases, status='SAT' if found else 'UNSAT', sec=round(time.time() - t0, 1),
                      **({k: found[k] for k in ('case', 'k0', 'comps', 'period', 'line')} if found else {}))), flush=True)
if found and '--verify' in sys.argv:
    sys.path.insert(0, '..')
    from ax_lib import G5, parse_line, planar_rot
    g = G5(*parse_line(found['line'])); Eg = g.E; idx = {tuple(sorted(e)): i for i, e in enumerate(Eg)}
    Ms = [frozenset(idx[tuple(sorted(e))] for e in Mt) for Mt in found['M']]
    pm = all(sorted(x for e in Mt for x in Eg[e]) == list(range(n)) for Mt in Ms)
    dis = all(not (Ms[t] & Ms[(t + 1) % L]) for t in range(L))
    fr = [g.kidx(Mt) for Mt in Ms]
    print('verify: PM', pm, 'disjoint', dis, 'frames', fr, 'adv ok', all((fr[(t + 1) % L] - fr[t]) % 5 == ADV % 5 for t in range(L)),
          'planar_rot', planar_rot(g), 'components', [g.ncomp(Ms[t] | Ms[(t + 1) % L]) for t in range(L)])
if found and '--show' in sys.argv: print(json.dumps(found['M']))
