import sys
p = 'prelay2.py'; s = open(p).read(); n0 = len(s)
def rep(old, new, count=1):
    global s
    c = s.count(old)
    assert c == count, (old[:80], c)
    s = s.replace(old, new)
# (a) flag
rep("CONSALL = 'consall' in FLAGS", "C6LE = 'c6le' in FLAGS             # s83: cons2 as 'the 6 ends <= t' (cf - t <= 0, the receiver row at d = 6) instead of the equation cf = 0\nCONSALL = 'consall' in FLAGS")
# (b) LP row
rep("conset.add(kk); addrow(cf, 0.0, 0.0, ('cons2', list(L), list(s))); return True",
    "conset.add(kk)\n        if C6LE: c6_ = dict(cf); c6_[('t',)] = -1.0; addrow(c6_, -inf, 0.0, ('cons2', list(L), list(s)))   # s83\n        else: addrow(cf, 0.0, 0.0, ('cons2', list(L), list(s)))\n        return True")
# (c) separation
rep("""            for idx in (int(np.argmax(D)), int(np.argmin(D))):
                if abs(D[idx]) > 1e-9:""",
"""            for idx in ((int(np.argmax(D)),) if C6LE else (int(np.argmax(D)), int(np.argmin(D)))):   # s83: under c6le only in - out > t is a violation
                if ((D[idx] - t) > 1e-9) if C6LE else (abs(D[idx]) > 1e-9):""")
# (d) upperR2 check
rep("""        Dl = cons2_delta(L, GV, HV2); m = float(np.abs(Dl).max()); worst = max(worst, m)""",
"""        Dl = cons2_delta(L, GV, HV2); m = max(0.0, float(Dl.max()) - t) if C6LE else float(np.abs(Dl).max()); worst = max(worst, m)
        if C6LE and float(Dl.min()) < -1e-9: NEG6[0] += 1; NEG6[1] = min(NEG6[1], float(Dl.min()))   # s83: a 6 that ends strictly below 0""")
rep("""    nc = 0; worst = 0.0; A6 = all6_words()""", """    nc = 0; worst = 0.0; A6 = all6_words(); NEG6 = [0, 0.0]""")
rep("""    log('conservation: %d canonical non-R6 links x 5^6 apex words; links with |in - out| > 1e-9: %d (worst %.3g)' % (len(A6), nc, worst)); bad += nc""",
"""    if C6LE: log('conservation (c6le: 6 ends <= t): %d canonical non-R6 links x 5^6 apex words; links with in - out > t + 1e-9: %d (worst excess %.3g); links where some 6 ends below 0: %d (lowest in - out %.6g)' % (len(A6), nc, worst, NEG6[0], NEG6[1]))
    else: log('conservation: %d canonical non-R6 links x 5^6 apex words; links with |in - out| > 1e-9: %d (worst %.3g)' % (len(A6), nc, worst))
    bad += nc""")
# (e) lowerR2
rep("""            if isR6(L) or len(L) != 6 or len(s) != 6 or any(v not in LET for v in L + s): log('  BAD CONS2', row); ok = False; continue
            cf = cons2_coef(L, s)
        elif row[0] == 'mrowR2':""",
"""            if isR6(L) or len(L) != 6 or len(s) != 6 or any(v not in LET for v in L + s): log('  BAD CONS2', row); ok = False; continue
            cf = cons2_coef(L, s)
            if C6LE:   # s83: cf - t <= 0, a <= row: weight <= 0, t coefficient -1, constant 0
                if w > 0: log('  WRONG SIGN', row); ok = False; continue
                tc = -1; dc = 0
        elif row[0] == 'mrowR2':""")
# (f) exactbasis bounds
rep("""        elif kd == 'cons2': lb[j], ub[j] = -inf, inf""", """        elif kd == 'cons2': lb[j], ub[j] = (-inf, 0.0) if C6LE else (-inf, inf)   # s83""")
# (g) repair
rep("r[1] == 'cons2' or", "(r[1] == 'cons2' and (not C6LE or r[2] < 0)) or", 2)
# (h) nosep + conssep
rep("""        if 'nosep' in FLAGS: log('nosep: LP over the warm rows only, t = %.12f (a lower bound once lowerR2 checks the cert)' % t); break""",
"""        if 'nosep' in FLAGS:
            if 'conssep' in FLAGS:   # s83: separate cons2 rows only (receivers stay the warm set); repeat until none is violated
                GVc = {k[1]: xv[i] for k, i in cols.items() if k[0] == 'g'}; HVc = {k[1]: xv[i] for k, i in cols.items() if k[0] == 'h'}
                ncs = 0; wcs = 0.0
                for Lc in RW:
                    Dc = cons2_delta(Lc, GVc, HVc)
                    for idx in ((int(np.argmax(Dc)),) if C6LE else (int(np.argmax(Dc)), int(np.argmin(Dc)))):
                        viol = float(Dc[idx] - t) if C6LE else abs(float(Dc[idx]))
                        if viol > 1e-9:
                            wcs = max(wcs, viol)
                            if addcons(Lc, tuple(LET[v] for v in SALL[idx])): ncs += 1
                log('  conssep it %d: t = %.12f, %d cons2 rows added (worst %.3g)' % (it, t, ncs, wcs))
                if ncs: continue
            log('nosep: LP over the warm rows only, t = %.12f (a lower bound once lowerR2 checks the cert)' % t); break""")
open(p, 'w').write(s); print('patched', n0, '->', len(s))
