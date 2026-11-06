"""s84_sepaudit check (c)/(b): sign invariants and the nc slack recomputed from the d = 7 query files the driver wrote (work/<tag>/).
usage: python3 check_c.py <work dir>   (layouts as in jsepf.cpp main())"""
import sys, os, numpy as np
W = sys.argv[1]
def rd(fn): return open(os.path.join(W, fn), 'rb').read()
out = []
# l3q (argv[7]) and l3qV=8 (argv[9]): QX[2*5^6] <= 0, PQ[125] >= 0, MK[2*5^6]
for fn in ('l3q.bin', 'l3q8.bin'):
    a = np.frombuffer(rd(fn), dtype='<f8'); assert a.size == 31250 + 125 + 31250, (fn, a.size)
    QX, PQ, MK = a[:31250], a[31250:31375], a[31375:]
    out.append('%s: QX max %.3g (min %.6g), #QX>0 %d; PQ min %.3g (max %.6g), #PQ<0 %d; MK in [%g, %g]' % (fn, QX.max(), QX.min(), int((QX > 0).sum()), PQ.min(), PQ.max(), int((PQ < 0).sum()), MK.min(), MK.max()))
# bonus (argv[6]): canonical d = 7 link -> value subtracted at the leaf
v = [float(l.split()[1]) for l in open(os.path.join(W, 'bonus7.txt')) if l.strip()]
out.append('bonus7.txt: %d links, min %.6g, max %.6g, #<=0 %d' % (len(v), min(v), max(v), sum(1 for x in v if x <= 0)))
# K* (argv[13])
b = rd('kstar_d7.bin'); mg, dd = np.frombuffer(b[:8], dtype='<i4'); aK = np.frombuffer(b[8:16], dtype='<f8')[0]; KUB = np.frombuffer(b[16:], dtype=np.uint8)
out.append('kstar_d7.bin: magic %d d %d aK %.12g (>= 0: %s); KUB size %d values %s, ones %d / %d' % (mg, dd, aK, aK >= 0, KUB.size, sorted(set(KUB.tolist())), int(KUB[:1953125].sum()), int(KUB[1953125:].sum())))
# EDGE (argv[14])
b = rd('edge_d7.bin'); mg, nk = np.frombuffer(b[:8], dtype='<i4'); p = 8; am = []
for k in range(nk):
    amt = np.frombuffer(b[p:p + 8], dtype='<f8')[0]; vm, nc = np.frombuffer(b[p + 8:p + 16], dtype='<i4'); p += 16 + 12 * nc; am.append((amt, int(vm), int(nc)))
out.append('edge_d7.bin: magic %d, %d keys, (amount, payee mask, ncond) %s; all amounts >= 0: %s; bytes used %d of %d' % (mg, nk, am, all(a[0] >= 0 for a in am), p, len(b)))
# f2b (argv[10]): int32 d, uint8 KM[5^8], double V6M[625*4*32], double QMT[25*32], buckets
b = rd('f2b_d7.bin'); d = np.frombuffer(b[:4], dtype='<i4')[0]; p = 4 + 390625
V6M = np.frombuffer(b[p:p + 8 * 80000], dtype='<f8').reshape(2500, 32); p += 8 * 80000
QMT = np.frombuffer(b[p:p + 8 * 800], dtype='<f8').reshape(25, 32)
sub = [(m, sb) for m in range(32) for sb in range(32) if sb & ~m == 0]
dV = max(0.0, max(float((V6M[:, sb] - V6M[:, m]).max()) for m, sb in sub))
dQ = max(0.0, max(float((QMT[:, sb] - QMT[:, m]).max()) for m, sb in sub))
# which QMT entries give the positive delta
pos = [(ix, m, sb, float(QMT[ix, sb] - QMT[ix, m])) for ix in range(25) for m, sb in sub if QMT[ix, sb] - QMT[ix, m] > 1e-15]
pos.sort(key=lambda r: -r[3])
out.append('f2b_d7.bin: d %d; V6M finite %s, min %.6g max %.6g; QMT min %.6g max %.6g; max positive subset delta dV %.9g dQ %.9g; #(ix,m,sb) with QMT delta > 0: %d, top %s' % (
    d, bool(np.isfinite(V6M).all()), V6M.min(), V6M.max(), QMT.min(), QMT.max(), dV, dQ, len(pos), [(divmod(r[0], 5), r[1], r[2], round(r[3], 12)) for r in pos[:4]]))
# q7m (argv[12]): QT[625][1024]
QT = np.frombuffer(rd('q7m_d7.bin'), dtype='<f8').reshape(625, 1024)
dT = max(0.0, float((QT - QT[:, 1023:1024]).max()))
# monotonicity in each mask (max over a subset <= max over the superset)
mono = all(bool((QT.reshape(625, 32, 32)[:, sb, :] <= QT.reshape(625, 32, 32)[:, m, :] + 1e-15).all()) for m, sb in sub[:])
out.append('q7m_d7.bin: QT min %.6g max %.6g; dT = max(QT[m] - QT[1023]) = %.9g; QT monotone in mask 1: %s' % (QT.min(), QT.max(), dT, mono))
SLACKT = 7 * dT + (1e-12 if dT > 0 else 0); SLACK = 7 * dV + 2 * 7 * dQ + SLACKT + (1e-12 if (dV > 0 or dQ > 0) else 0)
out.append('recomputed nc slack at d = 7: SLACK = 7 dV + 14 dQ + SLACKT (+1e-12) = %.9g, SLACKT = %.9g' % (SLACK, SLACKT))
WIN = np.fromfile(os.path.join(W, 'win_d7.bin'), dtype='<f8')
out.append('win_d7.bin: %d entries, NaN %d, +inf %d, entries <= -1e299 (inadmissible) %d, finite max %.6g min %.6g' % (WIN.size, int(np.isnan(WIN).sum()), int(np.isposinf(WIN).sum()), int((WIN <= -1e299).sum()), WIN[WIN > -1e299].max(), WIN[WIN > -1e299].min()))
print('\n'.join(out))
