"""radius-3 census for one receiver row: for each radius-2 survivor (ring-2 completion), build the 3-ball frame and solve
ring 3 exactly (dp.py). Ring-3 letters: {5..8 with deg >= inn+3 (layered: out >= 1), >=9 (99)}; ring-3 vertices touching a
>=9 ring-2 vertex are unknown (99, never matched; charge counted as +1 in the max, i.e. as if a five)."""
import sys, json, time, collections, multiprocessing as mp
from ball import *
import dp2
D = None
def ch(l): return 6 - (9 if l >= 99 else l)
def init(lk, sv):
    global C, D, LK, SV, FREE2, BASE
    C = registry(); LK = [int(c) for c in lk]; SV = [int(c) for c in sv]; D = len(LK)
    P, pa, pf, order2, _, _ = frame(D, LK)
    FREE2 = [x for x in order2 if x[0] == 'p' and LK[x[1]] < 9]
def one(line):
    p = [99 if c == '9' else int(c) for c in line.strip()]
    R2 = {('s', i): (SV[i] if SV[i] < 9 else 99) for i in range(D)}; R2.update(dict(zip(FREE2, p)))
    P, pa, pf, order2, inn3, touch = frame(D, LK, R2)
    for x in order2: R2.setdefault(x, 99)        # privates of >=9 link vertices: unknown
    fd = {('u',): D}
    for i in range(D): fd[('w', i)] = LK[i] if LK[i] < 9 else 99
    for x in order2: fd[x] = R2[x]
    ring3 = [('r', k) for k in range(len(inn3))]
    unk = [x for x in ring3 if any(R2[y] >= 99 for y in touch[x])]
    for x in unk: fd[x] = 99
    free = [x for x in ring3 if x not in fd]
    R = reqsets(C, P, pa, pf, fd, set(free))
    dom = {x: [l for l in (5, 6, 7, 8) if l >= inn3[x] + 3] + [99] for x in free}
    excl = sum(1 for x in free for l in (5, 6, 7, 8) if l < inn3[x] + 3)
    pats = list(R)
    nine_free = all(v < 99 for v in R2.values()) and all(l < 9 for l in LK)
    base = sum(ch(fd[x]) for x in fd if x[0] != 'r')            # rings 0..2 (>=9 as 9)
    r = dict(r2=line.strip(), n3=len(ring3), nfree=len(free), nunk=len(unk), nreq=len(R), excl=excl, base2=base)
    dsz = 1
    for x in free: dsz *= len(dom[x])
    r['domain'] = dsz
    cnt, mx, wmx, mn, wmn = dp2.solve(free, dom, pats)
    r['surv'] = cnt
    r['exact2'] = all(v < 99 for v in p) and nine_free
    if cnt and r['exact2']:
        domE = {x: [l for l in dom[x] if l < 99] for x in free}
        cE, mE, wE, nE, wnE = dp2.solve(free, domE, pats); r['surv_exact'] = cE
        if cE:
            r['max_exact'] = base + mE; r['wit_max'] = ''.join(str(wE[x]) for x in free)
            r['min_exact'] = base + nE; r['wit_min'] = ''.join(str(wnE[x]) for x in free)
        if all(v in (5, 6) for v in p):
            domS = {x: [l for l in dom[x] if l in (5, 6)] for x in free}
            cS, mS, wS, nS, wnS = dp2.solve(free, domS, pats); r['surv_small'] = cS
            if cS: r['max_small'] = base + mS; r['wit_small'] = ''.join(str(wS[x]) for x in free); r['min_small'] = base + nS; r['wit_small_min'] = ''.join(str(wnS[x]) for x in free)
    return r
if __name__ == '__main__':
    lk, sv, src, out = sys.argv[1:5]
    lines = [l for l in open(src) if l.strip()]
    if len(sys.argv) > 5: lines = lines[:int(sys.argv[5])]
    t0 = time.time(); n = 0
    with mp.Pool(int(dict(a.split('=') for a in sys.argv[6:]).get('np', 4)) if len(sys.argv) > 6 else 4, initializer=init, initargs=(lk, sv)) as pool, open(out, 'w') as o:
        for r in pool.imap(one, lines, chunksize=8):
            o.write(json.dumps(r) + '\n'); n += 1
            if n % 200 == 0: print(n, round(time.time() - t0), flush=True)
    print('done', n, round(time.time() - t0))
