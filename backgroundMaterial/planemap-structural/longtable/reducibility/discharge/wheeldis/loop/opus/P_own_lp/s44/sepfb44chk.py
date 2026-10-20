# s44 control (b2): the fb window terms (fb_win) and the cons2 separation term (cons2_delta) against the row
# coefficients (recv_coef_R2 / cons2_coef) with random fb values; fb-only load, no patterns.
import sys, random, itertools
B = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp'
E = B + '/s44/eng'; M = '/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis'
WK = '/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/wr44_sep'
sys.argv = [E + '/pcheck.py', 'none', 'apexcls', 'hat5', 'fb', 'root=' + M, 'work=' + WK, 'threads=1']
src = open(E + '/pcheck.py').read(); last = src.rstrip().rsplit('\n', 1)
G = {'__file__': E + '/pcheck.py', '__name__': 'pcheck_exec'}; exec(compile(last[0], E + '/pcheck.py', 'exec'), G)
import numpy as np
rng = random.Random(4444); LET = G['LET']
keys = set()
for U in (7, 8, 9):
    for sl in itertools.product(LET, repeat=9):
        a, b, c, e, f, p, q, r, s = sl
        if c < 6: continue
        k = G['fb_key'](U, c, (e, r, f, s if e == 5 else 0), (b, q, a, p if b == 5 else 0))
        if k: keys.add(k)
FBV = G['FBV']; FBV.clear()
for k in keys: FBV[k] = rng.random()
print('fb keys with random values: %d' % len(FBV))
G['CLSFILE'][0] = WK + '/cls.bin'; G['class_table_R2'](False).tofile(G['CLSFILE'][0])
bad = 0; n = 0
for d in (7, 8, 9):
    W = G['window_table_R2'](min(d, 9), np.zeros(len(G['ROOTS'])), {}, lambda sg: None)
    for thr, mode in ((-100.0, 2),):
        res, dt, _ = G['run_sep'](d, W, thr, 300, mode, pats=False)
        for r_ in res:
            if r_[0] != 'V': continue
            cf = G['recv_coef_R2'](d, r_[2], r_[3], False)
            v = sum(c * FBV.get(k[1], 0.0) for k, c in cf.items() if k[0] == 'fb'); n += 1
            if abs(v - float(r_[1])) > 1e-9: bad += 1; print('  MISMATCH d=%d %s %s sep %s rows %.12f' % (d, r_[2], r_[3], r_[1], v))
    # also random rows directly against the window sum
    for _ in range(3000):
        w = [rng.choice(LET) for _ in range(d)]; s = [rng.choice(LET) for _ in range(d)]
        for _f in range(rng.choice((0, 1, 2))):
            i = rng.randrange(d); w[i] = w[(i + 1) % d] = 5; s[i] = 5
        tot = 0.0; ok = True
        for i in range(d):
            ix = tuple(G['LI'][x] for x in (w[(i - 2) % d], w[(i - 1) % d], w[i], w[(i + 1) % d], w[(i + 2) % d], s[(i - 2) % d], s[(i - 1) % d], s[i], s[(i + 1) % d]))
            v = W[ix]
            if not np.isfinite(v): ok = False; break
            tot += v
        if not ok: continue
        cf = G['recv_coef_R2'](d, ''.join(map(str, w)), ''.join(map(str, s)), False)
        v = sum(c * FBV.get(k[1], 0.0) for k, c in cf.items() if k[0] == 'fb'); n += 1
        if abs(v - tot) > 1e-9: bad += 1; print('  MISMATCH random d=%d %s %s window %.12f rows %.12f' % (d, w, s, tot, v))
print('window: %d rows checked, %d mismatches' % (n, bad))
# cons2: cons2_delta (fb part only: g = h = 0) against cons2_coef on every apex word, for 6-words with a 7+
cb = 0; cn = 0
for L in G['all6_words']():
    if max(L) < 7 or 5 not in L: continue
    D = G['cons2_delta'](L, {}, {})
    for idx in rng.sample(range(len(G['SALL'])), 200):
        s = tuple(LET[v] for v in G['SALL'][idx])
        v = sum(c * FBV.get(k[1], 0.0) for k, c in G['cons2_coef'](L, s).items() if k[0] == 'fb'); cn += 1
        if abs(v - D[idx]) > 1e-9: cb += 1
print('cons2: %d (L, s) checked, %d mismatches' % (cn, cb))
print('SEPFB44:', 'PASS' if bad == 0 and cb == 0 and n and cn else 'FAIL')
