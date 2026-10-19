# Stage 25 variant F6 (coordinator steer): the cluster row also reads the far-side 6s of the binder (w1, w6: the 6s next
# to the big spoke w0, opposite the face) exactly, including their privates p1, p6; their M terms become exact h2 terms.
# Lifting test against cert_st24bL: the binder's weight is spread over (p1, p6) in the filt16 allowed sets; every other
# cert row is unchanged.  Old cert valid iff some lifting keeps every h2 reduced cost >= 0.
import json, collections
from fractions import Fraction
load_patterns(); xon = 'xon' in FLAGS
C = json.load(open(OPT['cert'])); SR = {(wd, tuple(map(str, b))): cf for wd, cf, b in R2_sender_rows()}
tot = collections.defaultdict(Fraction); tco = Fraction(0)
for c in C:
    w = Fraction(c['w']).limit_denominator(10 ** 7); row = c['row']
    if row[0] == 'senderR2':
        tco += w
        for k, v in SR[(row[1], tuple(map(str, row[2])))].items(): tot[k] += w * v
    elif row[0] == 'cons2':
        for k, v in cons2_coef(tuple(row[1]), tuple(row[2])).items(): tot[k] += w * v
    elif row[0] == 'mrowR2': tot[('h', tuple(row[2]))] += w; tot[('M', tuple(row[1]))] -= w
    elif row[0] == 'receiverR2':
        tco -= w; d, lk, sv = int(row[1]), row[2], row[3]
        if (lk, sv) == ('7665566', '6675676'): BW = w; continue
        for k, v in recv_coef_R2(d, lk, sv, xon).items(): tot[k] += w * v
d, lk, sv = 7, '7665566', '6675676'; U = 7; wl = [int(x) for x in lk]; sl = [int(x) for x in sv]
base = recv_coef_R2(d, lk, sv, xon)
far = (1, 6)
opts = {}
for j in far:
    am = amask(U, wl[(j - 2) % d], wl[(j - 1) % d], wl[(j + 1) % d], wl[(j + 2) % d], sl[(j - 2) % d], sl[(j - 1) % d], sl[j], sl[(j + 1) % d])
    sg = sig2_of(U, wl[(j + 1) % d], sl[j], sl[(j - 1) % d], wl[(j - 1) % d], wl[(j + 2) % d], wl[(j - 2) % d]) + (am,)
    opts[j] = (sg, [(p, h2_of((U, wl[(j + 1) % d], sl[j], p, sl[(j - 1) % d], wl[(j - 1) % d]), wl[(j + 2) % d], wl[(j - 2) % d])) for p in LET if (am >> (p - 5)) & 1 and not isR6((U, wl[(j + 1) % d], sl[j], p, sl[(j - 1) % d], wl[(j - 1) % d]))])
log('far-side 6s of the binder:', {j: (opts[j][0], [p for p, _ in opts[j][1]]) for j in far})
best = None
for p1, k1 in opts[1][1]:
    for p6, k6 in opts[6][1]:
        t2 = collections.defaultdict(Fraction, tot); cf = collections.Counter(base)
        for j, k in ((1, k1), (6, k6)): cf[('M', opts[j][0])] -= 1; cf[('h', k)] += 1
        for k, v in cf.items(): t2[k] += BW * v
        neg = sorted((-v / tco, k) for k, v in t2.items() if v > 0 and k[0] not in ('x', 'D'))
        log('  p1=%d p6=%d: columns with rc < 0: %d %s' % (p1, p6, len(neg), neg[:3]))
        if not neg and best is None: best = (p1, p6)
log('F6 lifting: %s' % ('FEASIBLE at p1=%d p6=%d: old cert valid, F6 null' % best if best else 'no single (p1, p6) lifting works'))
