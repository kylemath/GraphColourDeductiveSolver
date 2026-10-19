"""Randomised search for a registry-free cone around a receiver row: rings 1..3 (+ optional ring 4) chosen, all-6 beyond.
A hit is verified by full containment over the whole exact region (core + 6 all-6 rings, diameter of configs <= 4)."""
import sys, random, time, json
from ball import *
import cone
C = registry()
def ch(l): return 6 - l
def mkcone(D, rings, extra=7):
    try: L, P, pa, pf, fd = cone.build(D, rings, extra)
    except AssertionError: return None
    return L, P, pa, pf, fd
def stable(L, D, rings, extra):
    # in-counts of the last exact all-6 rings must be <= 2 (corner/edge pattern of a hex cone)
    # recompute: rebuild without the closing rings
    M = Layered(D)
    for r in rings: M.add_ring(r)
    lens = []; sig = []
    for _ in range(extra):
        M.add_ring([6] * len(M.ring())); lens.append(len(M.ring()))
        sig.append((sorted(M.inn[x] for x in M.ring()).count(1), sorted(M.inn[x] for x in M.ring()).count(3), max(M.inn[x] for x in M.ring())))
    # all-6 continuation reproduces itself: same numbers of in=1 / in=3 vertices, max in <= 3, constant growth
    return len(set(sig[-4:])) == 1 and sig[-1][2] <= 3 and len(set(b - a for a, b in zip(lens[-5:], lens[-4:]))) == 1, lens
def run(lk, sv, r2line, tries, seed, ring4=False):
    rnd = random.Random(seed)
    LK = [int(c) for c in lk]; SV = [int(c) for c in sv]; D = len(LK)
    P2, pa2, pf2, order2, _, _ = frame(D, LK)
    free2 = [x for x in order2 if x[0] == 'p']
    p = [int(c) for c in r2line]
    R2 = {('s', i): SV[i] for i in range(D)}; R2.update(dict(zip(free2, p)))
    P, pa, pf, order2, inn3, touch = frame(D, LK, R2)
    fd = {('u',): D}
    for i in range(D): fd[('w', i)] = LK[i]
    for x in order2: fd[x] = R2[x]
    ring3 = [('r', k) for k in range(len(inn3))]
    pats = list(reqsets(C, P, pa, pf, fd, set(ring3)))
    base = 6 - D + sum(6 - l for l in LK) + sum(6 - R2[x] for x in order2)
    found = []; import collections; cnt = collections.Counter()
    for t in range(tries):
        # random DFS assignment of ring 3 avoiding pats; letters weighted towards 6
        a = {}
        ok = True
        for x in ring3:
            opts = [l for l in (5, 6, 7, 8) if l >= inn3[x] + 3]
            rnd.shuffle(opts); opts.sort(key=lambda l: rnd.random() * (0.3 if l == 6 else 1.0))
            for l in opts:
                a[x] = l
                if not any(all(a.get(y) == ll for y, ll in q) for q in pats if any(y == x for y, _ in q)): break
            else: ok = False; break
        if not ok: cnt['dfsfail'] += 1; continue
        tot = base + sum(6 - a[x] for x in ring3)
        cnt['tot%d' % tot] += 1
        if not 1 <= tot <= 5: continue
        rings = [LK, [R2[x] for x in order2], [a[x] for x in ring3]]
        st = None
        try: st, lens = stable(None, D, rings, 8)
        except AssertionError: cnt['geom'] += 1; continue
        if not st: cnt['unstable'] += 1; continue
        B = mkcone(D, rings, 7)
        if B is None: continue
        L, Pc, pac, pfc, fdc = B
        h = cone.contains(C, Pc, pac, pfc, fdc); cnt['tested'] += 1
        if h: cnt[h[0][0]] += 1
        if not h:
            found.append(dict(r2=r2line, r3=''.join(map(str, rings[2])), total=tot, lens=lens)); print('FOUND', found[-1], flush=True)
            return found
    run.cnt = cnt
    return found
if __name__ == '__main__':
    lk, sv, src, tries = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
    lines = [l.strip() for l in open(src) if l.strip() and '9' not in l]
    t0 = time.time()
    for k, l in enumerate(lines):
        f = run(lk, sv, l, tries, k)
        if k % 50 == 0: print(k, l, round(time.time() - t0), flush=True)
