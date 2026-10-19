"""Stage 18 screen (b), finest shared key. Diamond (v five, x, b big hat, y): side tuple for a shared spoke x:
 x=5: (5, c2 X1, X2)   X1 = x's nbr adjacent to b (v: hat H[k-1] class; b: link nbr exact), X2 = x's nbr adjacent to v (v: link w_{k-1}; b: apex)
 x=6: (6, c2 X1, c2 Fo) X1 = x's nbr adjacent to b (v: fan of x; b: link nbr), Fo = x's nbr opposite y (v: hat H[k-1]; b: apex)
 x>=7: (x,)
K = min over the side swap. Sender rows whose needed bit is not enumerated are reported as ambiguous (no inflow counted)."""
import json, sys, collections
from fractions import Fraction as F
def c2(l): return 1 if l >= 7 else 0
C = json.load(open(sys.argv[1]))
tot = collections.defaultdict(F); ex = collections.defaultdict(list); amb = 0
for c in C:
    r = c['row']; w = F(c['w']).limit_denominator(10 ** 7)
    if r[0] == 'senderR2':
        wd = [int(x) for x in r[1]]; n = 5; sixes = [k for k in range(n) if wd[k] == 6]
        hats = sorted({h for k in sixes for h in (k, (k - 1) % n)}); bits = r[2]; j = bits.index('|')
        H = dict(zip(hats, bits[:j])); Fn = dict(zip(sixes, bits[j + 1:]))
        for k, v in H.items():
            if v != 1: continue
            def sd(p, q, hp, fp):   # spoke p (x), its other link nbr q, hat between q and p index hp
                x = wd[p]
                if x == 5: return None if hp not in H else (5, H[hp], wd[q])
                if x == 6: return (6, Fn[p], H[hp]) if hp in H else None
                return (x,)
            a = sd(k, (k - 1) % n, (k - 1) % n, None); b = sd((k + 1) % n, (k + 2) % n, (k + 1) % n, None)
            if a is None or b is None: amb += 1; continue
            K = min(a + b, b + a); tot[K] += w; ex[K].append(('in', float(w), r[1], bits, k))
    elif r[0] == 'receiverR2':
        d = int(r[1]); lk = [int(x) for x in r[2]]; sv = [int(x) for x in r[3]]
        for i in range(d):
            if sv[i] != 5: continue
            def sd(p, q, sq):   # spoke p, b's link nbr q next to p (other side), apex sq between q and p
                x = lk[p % d]
                if x == 5: return (5, c2(lk[q % d]), sv[sq % d])
                if x == 6: return (6, c2(lk[q % d]), c2(sv[sq % d]))
                return (x,)
            a = sd(i, i - 1, i - 1); b = sd(i + 1, i + 2, i + 1)
            K = min(a + b, b + a); tot[K] += w; ex[K].append(('out', float(w), d, r[2], r[3], i))
print('ambiguous sender inflows (not counted):', amb)
for K in sorted(tot, key=lambda k: -tot[k]): print(K, float(tot[K]), 'PROFITABLE' if tot[K] > 0 else '', ex[K][:3])
