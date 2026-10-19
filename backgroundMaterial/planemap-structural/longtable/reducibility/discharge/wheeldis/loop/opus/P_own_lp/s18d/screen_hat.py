"""Stage 18 pre-build screen (b): a big b that is a hat of a five v (b adjacent to v's consecutive spokes w_k, w_{k+1}) sends
r[K] to v. Coarse key K = {w_k, w_{k+1}} (both ends see both letters exactly). Sender rows: +r where the row fixes hat k big.
Receiver rows: +r (outflow) at every apex position S(i) = 5 (the apex five has the centre as a hat). Profitable iff tot > 0."""
import json, sys, collections
from fractions import Fraction as F
C = json.load(open(sys.argv[1]))
tot = collections.defaultdict(F); ex = collections.defaultdict(list)
for c in C:
    r = c['row']; w = F(c['w']).limit_denominator(10 ** 7)
    if r[0] == 'senderR2':
        wd = [int(x) for x in r[1]]; n = 5; sixes = [k for k in range(n) if wd[k] == 6]
        hats = sorted({h for k in sixes for h in (k, (k - 1) % n)}); bits = r[2]; hb = bits[:bits.index('|')]
        H = dict(zip(hats, hb))
        for k, v in H.items():
            if v == 1:
                K = tuple(sorted((wd[k], wd[(k + 1) % n]))); tot[K] += w; ex[K].append(('in', float(w), r[1], bits, k))
    elif r[0] == 'receiverR2':
        d = int(r[1]); lk = [int(x) for x in r[2]]; sv = [int(x) for x in r[3]]
        for i in range(d):
            if sv[i] == 5:
                K = tuple(sorted((lk[i], lk[(i + 1) % d]))); tot[K] += w; ex[K].append(('out', float(w), d, r[2], r[3], i))
for K in sorted(tot, key=lambda k: -tot[k]): print(K, float(tot[K]), 'PROFITABLE' if tot[K] > 0 else '', ex[K][:4])
