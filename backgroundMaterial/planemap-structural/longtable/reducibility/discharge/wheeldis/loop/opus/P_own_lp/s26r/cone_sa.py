"""Simulated-annealing search for a registry-free positive cone containing a receiver row (u, link, apexes fixed = the row).
Free: ring-2 privates, ring 3, ring 4 (letters 5..8, deg >= in+3); rings >= 5 all 6. Cost = number of forbidden
embeddings in the whole exact region + charge-window (1 <= sum(6-d) <= 5) and geometry penalties.
A zero-cost state is a registry-free plane triangulation with finitely many non-6 vertices and positive total charge."""
import sys, random, math, json, time
from ball import *
import cone, cone_search as cs
C = registry()
lk, sv, seed, iters = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
LK = [int(c) for c in lk]; SV = [int(c) for c in sv]; D = len(LK)
_, _, _, order2, _, _ = frame(D, LK); free2 = [x for x in order2 if x[0] == 'p']
rnd = random.Random(seed)
def rings_of(st):
    p, r3, r4 = st
    R2 = {('s', i): SV[i] for i in range(D)}; R2.update(dict(zip(free2, p)))
    return [LK, [R2[x] for x in order2], r3, r4]
def fix(st):
    p, r3, r4 = st
    r2 = rings_of((p, [], []))[1]
    M = Layered(D); M.add_ring(LK); M.add_ring(r2); n3 = len(M.ring())
    r3 = (r3 + [6] * n3)[:n3]
    r3 = [max(l, M.inn[x] + 3) for l, x in zip(r3, M.ring())]
    M.add_ring(r3); n4 = len(M.ring())
    r4 = (r4 + [6] * n4)[:n4]
    r4 = [max(l, M.inn[x] + 3) for l, x in zip(r4, M.ring())]
    return (p, r3, r4)
def cost(st):
    rings = rings_of(st); tot = 6 - D + sum(6 - l for r in rings for l in r)
    pen = 4 * max(0, 1 - tot) + 4 * max(0, tot - 5)
    try:
        ok, lens = cs.stable(None, D, rings, 9)
        if not ok: return 60 + pen, tot, None
        L, P, pa, pf, fd = cone.build(D, rings, 6)
    except AssertionError: return 80 + pen, tot, None
    h = cone.contains(C, P, pa, pf, fd, stop=False)
    return len(h) + pen, tot, h
if __name__ == '__main__':
    st = fix(([6] * len(free2), [], []))
    c, tot, h = cost(st); best = (c, st, tot); T = 2.0; t0 = time.time()
    for it in range(iters):
        p, r3, r4 = [list(x) for x in st]
        for _ in range(1 + (rnd.random() < 0.3)):
            k = rnd.random()
            tgt = p if k < 0.15 else (r3 if k < 0.65 else r4)
            j = rnd.randrange(len(tgt)); tgt[j] = rnd.choice([5, 5, 6, 6, 7, 8])
        ns = fix((p, r3, r4)); nc, ntot, nh = cost(ns)
        if nc <= c or rnd.random() < math.exp((c - nc) / T):
            st, c, tot, h = ns, nc, ntot, nh
            if c < best[0]:
                best = (c, st, tot)
                print('it', it, 'cost', c, 'tot', tot, ''.join(map(str, st[0])), ''.join(map(str, st[1])), ''.join(map(str, st[2])),
                      sorted({x[0] for x in (h or [])})[:6], round(time.time() - t0), flush=True)
            if c == 0: print('FOUND', json.dumps(dict(p=st[0], r3=st[1], r4=st[2], tot=tot)), flush=True); break
        T = max(0.15, T * 0.999)
    print('best', best[0], best[2], json.dumps([list(x) for x in best[1]]))
