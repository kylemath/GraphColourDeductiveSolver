"""DP vs literal enumeration on restricted ring-3 domains (control). Also 'shift' control: degree+1 registry gives other answers."""
import random, sys
import r3, dp2 as dp
r3.init('7665566', '6675676')
from ball import *
random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
lines = [l.strip() for l in open('surv2_7665566_6675676.txt')]
bad = 0; nt = 0
for line in random.sample(lines, 8) + ['666666', '666655', '666656']:
    p = [99 if c == '9' else int(c) for c in line]
    R2 = {('s', i): r3.SV[i] for i in range(7)}; R2.update(dict(zip(r3.FREE2, p)))
    P, pa, pf, order2, inn3, touch = frame(7, r3.LK, R2)
    fd = {('u',): 7}
    for i in range(7): fd[('w', i)] = r3.LK[i]
    for x in order2: fd[x] = R2[x]
    ring3 = [('r', k) for k in range(len(inn3))]
    for x in ring3:
        if any(R2[y] >= 99 for y in touch[x]): fd[x] = 99
    free = [x for x in ring3 if x not in fd]
    pats = list(reqsets(r3.C, P, pa, pf, fd, set(free)))
    for trial in range(4):
        full = {x: [l for l in (5, 6, 7, 8) if l >= inn3[x] + 3] + [99] for x in free}
        dom = {}
        for k, x in enumerate(free):
            m = 3 if k < 4 else (2 if k < 12 else 1)
            dom[x] = sorted(random.sample(full[x], min(m, len(full[x]))))
        c, mx, w1, mn, w2 = dp.solve(free, dom, pats); c2, mx2, mn2 = dp.brute(free, dom, pats); nt += 1
        if (c, mx, mn) != (c2, mx2, mn2): bad += 1; print('MISMATCH', line, c, mx, mn, c2, mx2, mn2)
        elif c:
            # witnesses must be survivors with the stated charge
            for w, v in ((w1, mx), (w2, mn)):
                assert not any(all(w[y] == l for y, l in p) for p in pats) and sum(dp.ch(w[x]) for x in free) == v
print('tests', nt, 'mismatches', bad)
