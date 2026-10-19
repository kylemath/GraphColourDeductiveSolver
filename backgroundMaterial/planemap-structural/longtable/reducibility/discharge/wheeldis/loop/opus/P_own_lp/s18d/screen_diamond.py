"""Stage 18 pre-build screen. Diamond channel: a big centre c and its big apex b = S(i) (they share the edge w_i w_{i+1})
exchange q[K]. K is the finest key both ends read: (from-letter, to-letter, w_i, w_{i+1}, plus at each shared side vertex x:
x=5 -> (nbr adjacent to sender, nbr adjacent to receiver); x=6 -> (opposite vertex); x>=7 -> ()), canonical over the side swap.
q appears only in receiver rows (+out, -in). Under a dual cert, column q[K] has tot = sum_rows w*coef. If tot <= 0 for every K
(rc = -tot/tco >= 0), the cert stays valid for the extended class: the channel is null at this key and at any coarser key."""
import json, sys, collections
from fractions import Fraction as F
C = json.load(open(sys.argv[1]))
def side(x, a_nbr, b_nbr, opp): return (x,) + ((a_nbr, b_nbr) if x == 5 else (opp,) if x == 6 else ())
def key(A, B, sa, sb): return (A, B) + min(sa + sb, sb + sa)
tot = collections.defaultdict(F); occ = collections.defaultdict(list)
for c in C:
    r = c['row']
    if r[0] != 'receiverR2': continue
    w = F(c['w']).limit_denominator(10 ** 7); d = int(r[1]); lk = [int(x) for x in r[2]]; sv = [int(x) for x in r[3]]; U = min(d, 9)
    W = lambda k: lk[k % d]; S = lambda k: sv[k % d]
    for i in range(d):
        B = S(i)
        if B < 7 or W(i) < 7 and False: pass
        if B < 7: continue
        x, y = W(i), W(i + 1)
        # out c -> b : sides (adjacent to c = link nbr, adjacent to b = apex)
        so_x = side(x, W(i - 1), S(i - 1), S(i - 1)); so_y = side(y, W(i + 2), S(i + 1), S(i + 1))
        si_x = side(x, S(i - 1), W(i - 1), S(i - 1)); si_y = side(y, S(i + 1), W(i + 2), S(i + 1))
        ko = key(U, B, so_x, so_y); ki = key(B, U, si_x, si_y)
        tot[ko] += w * 1; tot[ki] += w * -1
        occ[ki].append(('in', float(w), d, r[2], r[3], i)); occ[ko].append(('out', float(w), d, r[2], r[3], i))
neg = sorted((k for k in tot if tot[k] > 0), key=lambda k: -tot[k])
print('receiver rows with weight:', sum(1 for c in C if c['row'][0] == 'receiverR2'), '; diamond keys touched:', len(tot))
print('keys with tot > 0 (negative reduced cost, the LP would use them):', len(neg))
for k in neg[:20]: print('  ', k, float(tot[k]), occ[k][:3])
