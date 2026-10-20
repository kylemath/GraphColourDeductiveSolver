exec(open('/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s43/pricer43.py').read().split("T = float(tco)")[0])
T = float(tco)
e2, lam = worst(FK)
tv = A @ lam
print('\nface keys: tot (sender - receiver weight, x183) at the (P2) lifting and who pays them')
for K in FK:
    i = kix[K]; print(' key', K[1], 'rc*183 = %+.3f' % (-tv[i] / T * 183))
    for vi, (ri, ci) in enumerate(var):
        if A[i, vi] and lam[vi] > 1e-12:
            r = rows[ri]; print('    %s %-26s ctx %-12s lam*183=%.3f coef %+d' % (r[0], r[1], r[3][ci][0], lam[vi] * 183, int(A[i, vi])))
# full hats of the paying sender contexts at the big spoke
print('\nsender contexts paying a face key: unmasked hat vector (h0..h4) read at the big spoke (H classes)')
for ri, r in enumerate(rows):
    if r[0] != 'S': continue
    wd = r[1].split()[0]; w = [int(c) for c in wd]
    for ci, (cl, z) in enumerate(r[3]):
        hit = [k for k in z if k in FK]
        if not hit: continue
        Hb = [int(c) for c in cl.split('|')[0]]
        for j in range(5):
            if w[j] >= 7:
                n = tuple(w[(j + m) % 5] for m in range(5)); h = tuple(Hb[(j + m) % 5] for m in range(5))
                k2 = G['fy_sender_key'](w, Hb, j)
                if ('z', k2) in FK:
                    a = n + h; b = (n[0], n[4], n[3], n[2], n[1]) + tuple(reversed(h))
                    print('   %s ctx %s spoke %d: n,h (canonical orientation) = %s  key %s' % (wd, cl, j, min(a, b), k2))
