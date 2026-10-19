"""For the all-{5,6} radius-2 survivors of the binder: radius-3 survivors whose ring 3 has exactly ONE vertex >= 7
(all others in {5,6}); exact (DP over the rest)."""
import r3, dp2, json, sys
from ball import *
lk, sv = sys.argv[1], sys.argv[2]
r3.init(lk, sv)
D = r3.D
def frame3(line):
    p = [int(c) for c in line]
    R2 = {('s', i): r3.SV[i] for i in range(D)}; R2.update(dict(zip(r3.FREE2, p)))
    P, pa, pf, order2, inn3, touch = frame(D, r3.LK, R2)
    fd = {('u',): D}
    for i in range(D): fd[('w', i)] = r3.LK[i]
    for x in order2: fd[x] = R2[x]
    ring3 = [('r', k) for k in range(len(inn3))]
    pats = list(reqsets(r3.C, P, pa, pf, fd, set(ring3)))
    base = sum(6 - fd[x] for x in fd)
    return ring3, inn3, touch, pats, base, order2
def nm(x): return x[0] + ''.join(map(str, x[1:]))
for line in sys.argv[3:]:
    ring3, inn3, touch, pats, base, order2 = frame3(line)
    print('r2', line, 'ring2 order', ' '.join(nm(x) for x in order2))
    tot = 0
    for j, x in enumerate(ring3):
        for b in (7, 8, 99):
            if b < 99 and b < inn3[x] + 3: continue
            dom = {y: ([b] if y == x else [l for l in (5, 6) if l >= inn3[y] + 3]) for y in ring3}
            c, mx, wmx, mn, wmn = dp2.solve(ring3, dom, pats)
            if c:
                tot += c
                print('  big at %s (touches %s) = %s: %d survivors, max sum(6-d) %d, witness %s' % (nm(x), ','.join(nm(y) for y in touch[x]), '>=9' if b == 99 else b, c, base + mx - (0 if b < 99 else 0), ''.join('9' if wmx[y] == 99 else str(wmx[y]) for y in ring3)))
    print('  total one-big survivors', tot)
