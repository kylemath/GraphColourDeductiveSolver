# s43 control (b2): jsep6's fy2 face coupling vs an independent Python max over cells.  z-only load: random z2 values,
# y = x = h = 0, no patterns.  For every row jsep6 (mode 2, K rows, d = 7, 8) returns, its load must equal
#   max over cells tau of sum_{link fives} z[K2(tau)]   (computed here from the row, own loop over cells).
# Control: the same table with the face file 'none' (decoupled UB) must differ on some face rows.
import sys, random, itertools, collections, subprocess
B = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp'
E = B + '/s43/eng'; M = '/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis'
WK = '/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/wr43_sep'
sys.argv = [E + '/pcheck.py', 'none', 'apexcls', 'hat5', 'fy', 'fy2', 'root=' + M, 'work=' + WK, 'threads=1']
src = open(E + '/pcheck.py').read(); last = src.rstrip().rsplit('\n', 1)
G = {'__file__': E + '/pcheck.py', '__name__': 'pcheck_exec'}; exec(compile(last[0], E + '/pcheck.py', 'exec'), G)
import numpy as np
rng = random.Random(4343); LET = G['LET']; isR5 = G['isR5']; c2 = G['c2']
# random z on every level-2 receiver key (faces get large values so face rows dominate)
keys = set()
for U in (7, 8):
    for a, b, e, f, p, q, r, s in itertools.product(LET, repeat=8):
        n = (U, e, r, q, b)
        if isR5(n): continue
        for tc in ((0, 1) if G['fy_vis'](n)[2] else (None,)): keys.add(G['fy_recv_key'](U, a, b, e, f, p, q, r, s, tc))
ZV = G['ZV']; ZV.clear()
for k in keys: ZV[k] = rng.random() * (3.0 if k[7] in (0, 1) else 0.2)
print('z2 keys with random values: %d (face keys %d)' % (len(ZV), sum(1 for k in ZV if k[7] in (0, 1))))
G['CLSFILE'][0] = WK + '/cls.bin'; G['class_table_R2'](False).tofile(G['CLSFILE'][0])
def indep(d, wl, sl):
    """own implementation: faces, allowed classes, max over cells of the z load"""
    U = min(d, 9); F = [i for i in range(d) if wl[i] == 5 and wl[(i + 1) % d] == 5 and sl[i] == 5]
    def allowed(i):
        A = [c for c in (0, 1) if any(not isR5((5, 5, sl[(i + 1) % d], x, sl[(i - 1) % d])) for x in ((5, 6) if c == 0 else (7, 8, 9)))]
        return A or [0, 1]
    best = None
    for cb in itertools.product(*[allowed(i) for i in F]):
        tau = dict(zip(F, cb)); tot = 0.0
        for i in range(d):
            if wl[i] != 5: continue
            n = [U, wl[(i + 1) % d], sl[i], sl[(i - 1) % d], wl[(i - 1) % d]]
            h = [c2(wl[(i + 2) % d]), c2(sl[(i + 1) % d]) if n[1] == 5 else 2, 2, c2(sl[(i - 2) % d]) if n[4] == 5 else 2, c2(wl[(i - 2) % d])]
            if n[1] == 5 and n[2] == 5: h[2] = tau[i]
            elif n[4] == 5 and n[3] == 5: h[2] = tau[(i - 1) % d]
            k = min(tuple(n) + tuple(h), (n[0], n[4], n[3], n[2], n[1]) + tuple(h[::-1]))
            tot += ZV.get(k, 0.0)
        best = tot if best is None else max(best, tot)
    return best, len(F)
bad = 0; nrow = 0; nface = 0; diff_unc = 0
for d in (7, 8):
    W = G['window_table_R2'](min(d, 9), np.zeros(len(G['ROOTS'])), {}, lambda sg: None)
    res, dt, _ = G['run_sep'](d, W, -1.0, 400, 2, pats=False)
    # decoupled control: same table, face file 'none'
    hdr = WK + '/hdr_%d_m2.txt' % d; wp = WK + '/win_d%d.bin' % d
    out = subprocess.run([G['BIN6'], hdr, wp, '1', '1', G['CLSFILE'][0], 'none', 'none', 'none'], capture_output=True, text=True, check=True).stdout.split('\n')
    unc = {(l.split()[2], l.split()[3]): float(l.split()[1]) for l in out if l.startswith('V')}
    for r in res:
        if r[0] != 'V': continue
        wl = [int(c) for c in r[2]]; sl = [int(c) for c in r[3]]; v, nf = indep(d, wl, sl); nrow += 1; nface += nf > 0
        if abs(v - float(r[1])) > 1e-9: bad += 1; print('  MISMATCH d=%d %s %s jsep6 %s indep %.12f' % (d, r[2], r[3], r[1], v))
        if (r[2], r[3]) in unc and unc[(r[2], r[3])] > float(r[1]) + 1e-9: diff_unc += 1
    print('d=%d: %d rows returned (%.1fs), decoupled run returned %d' % (d, sum(1 for r in res if r[0] == 'V'), dt, len(unc)))
print('SEP43: %s  (%d rows checked, %d with a face, %d mismatches; rows where the decoupled UB is strictly larger: %d)' % ('PASS' if bad == 0 and nrow else 'FAIL', nrow, nface, bad, diff_unc))
