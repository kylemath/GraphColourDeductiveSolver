"""Idea C, sharpened: the 'overflow law'.
  law: a hub of degree 7/8 whose charge after the RSST rules is c > 0 pushes exactly c out through SP parts.
Measured on concrete hub balls drawn inside every SP part (2 draws each)."""
import random, numpy as np, collections as C, sys, pickle
from common import *
from ball import *
P = load(); R = Rules(P)
A = np.load('../real58.npz')
pre = np.array([p['pre'] for p in P]); dr = pre == 'drule'
E0 = {}
for d in (5, 6, 7, 8):
    M = A[f'M{d}'].astype(float); e = 60 * (6 - d) + M[:, dr].sum(1)
    for w, x in zip(A[f'W{d}'], e): E0[tuple(int(v) for v in w)] = x
rng = random.Random(11)
def full(d, link, asg):
    Wu = Ball(d, link, asg); Wl = Ball(d, link, asg, True)
    o = R.out(Wu); iu = R.inn(Wu); il = R.inn(Wl)
    g = lambda L, k: sum(x.get(k, 0) for x in L)
    c_lo = 60 * (6 - d) - g(o, 'dr') + g(il, 'dr'); c_hi = 60 * (6 - d) - g(o, 'dr') + g(iu, 'dr')
    spo = [x.get('SP', 0) for x in o]
    et = []
    for i in range(d):
        tw = target_word(Wu, i); et.append(E0[canon(tw)] if tw else None)
    return dict(d=d, link=link, c_lo=c_lo, c_hi=c_hi, spo=spo, sp_in_hi=g(iu, 'SP'), sp_in_lo=g(il, 'SP'),
                st_out=g(o, 'ST'), st_in_hi=g(iu, 'ST'), et=et)
if __name__ == '__main__':
    rows = []
    for p in P:
        if p['pre'] != 'SP_': continue
        for rep in range(2):
            r = full(*ball_from_part(p, 0, rng)); r['w'] = p['w']; r['tag'] = p['tag']; rows.append(r)
    pickle.dump(rows, open('overflow_rows.pkl', 'wb'))
    n = len(rows)
    print('balls', n, ' bounds differ (third ring matters):', sum(r['c_lo'] != r['c_hi'] for r in rows))
    print('hub RSST charge c (upper):', sorted(C.Counter(r['c_hi'] for r in rows).items()))
    print('total SP out:', sorted(C.Counter(sum(r['spo']) for r in rows).items()))
    print('c - SPout:', sorted(C.Counter(r['c_hi'] - sum(r['spo']) for r in rows).items()))
    print('c - SPout + SPin(upper) - STout + STin:', sorted(C.Counter(r['c_hi'] - sum(r['spo']) + r['sp_in_hi'] - r['st_out'] + r['st_in_hi'] for r in rows).items()))
    print('hub also receives SP (upper reading):', sum(r['sp_in_hi'] > 0 for r in rows), ' ST involved:', sum(r['st_out'] != 0 or r['st_in_hi'] != 0 for r in rows))
    print('law A  c > 0 on SP balls:', np.mean([r['c_hi'] > 0 for r in rows]).round(3))
    print('law B  SP out == c exactly:', np.mean([r['c_hi'] == sum(r['spo']) for r in rows]).round(3),
          '   SP out == max(c,0)+k? diff table above')
    print('number of distinct SP targets per ball:', sorted(C.Counter(sum(1 for x in r['spo'] if x) for r in rows).items()))
    print('per-target amounts:', sorted(C.Counter(tuple(sorted(x for x in r['spo'] if x)) for r in rows).items()))
    # target choice: is each SP target a spoke of degree>=7 ? is it the one with most slack?
    tdeg = C.Counter(); rank = C.Counter(); elig = C.Counter()
    for r in rows:
        d = r['d']
        cand = [i for i in range(d) if r['link'][i] >= 7]
        elig[len(cand)] += 1
        sl = {i: (r['et'][i] if r['et'][i] is not None else -60 * (r['link'][i] - 6) - 1e-3) for i in cand}  # 9+: unknown, assume very slack
        order = sorted(cand, key=lambda i: sl[i])
        for i in range(d):
            if r['spo'][i]:
                tdeg[r['link'][i]] += 1
                rank[order.index(i) if i in order else -1] += 1
    print('target degree:', sorted(tdeg.items()), ' eligible (>=7) spokes per ball:', sorted(elig.items()))
    print('rank of target among >=7 spokes by expected RSST charge (0 = most slack):', sorted(rank.items()))
    e = [r['et'][i] for r in rows for i in range(r['d']) if r['spo'][i] and r['et'][i] is not None]
    print('target expected RSST charge: share < 0:', np.mean(np.array(e) < 0).round(3), ' share <= -w... median', np.median(e).round(1))
