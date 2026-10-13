"""Does axiom A5v predict the chain-parity law step-by-step in abstract graphs?
For random abstract G5 graphs (config model, v=0 degree 5, rest cubic), every step M -> succ(M) with
pred(M), M, succ(M) all DL-good: record (A5v(M), A5v(succ), law step ok?)."""
import random, sys
from collections import Counter
from ax_lib import *
def rand_graph(n, rng):
    while True:
        stubs = [0] * 5 + [x for x in range(1, n) for _ in range(3)]
        rng.shuffle(stubs)
        E = [(stubs[2 * i], stubs[2 * i + 1]) for i in range(len(stubs) // 2)]
        if any(a == b for a, b in E): continue
        if len({tuple(sorted(e)) for e in E}) < len(E): continue
        g = nx.Graph(); g.add_edges_from(E)
        if not nx.is_connected(g): continue
        fv = [i for i, (a, b) in enumerate(E) if 0 in (a, b)]
        rng.shuffle(fv)
        return n, E, fv
rng = random.Random(int(sys.argv[2])); C = Counter(); N = int(sys.argv[1]); cnt = int(sys.argv[3])
for it in range(cnt):
    g = G5(*rand_graph(N, rng))
    P = g.pms()
    good = {}
    for M in P:
        d = g.dl(M)
        if d: good[M] = d
    def succ(M, k):
        f = g.fv[(k - 2) % 5]; c = [x for x in P if f in x and not (x & M)]; return c[0] if len(c) == 1 else None
    def pred(M, k):
        f = g.fv[(k + 2) % 5]; c = [x for x in P if f in x and not (x & M)]; return c[0] if len(c) == 1 else None
    for M, d in good.items():
        k = d[0]; S = succ(M, k); Pr = pred(M, k)
        if S not in good or Pr not in good: continue
        a = fig8_axioms(g, M, d)['v_into_X']; b = fig8_axioms(g, S, good[S])['v_into_X']
        k1 = g.ncomp(Pr | M); k2 = g.ncomp(M | S)
        C[(a, b, (k1 - k2) % 2 == 1)] += 1
for key in sorted(C): print(key, C[key])
