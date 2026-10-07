#!/usr/bin/env python3
"""Job BE [exploratory]: m's neighbourhood at position 9 in c_9 and d_9 = rho^-1 c_19 (Job BD conventions), every L = 20 (5,5,5,5,6) census Gamma-cycle (jobav records).
Pocket pair = {c9(p), c9(m)} (= the same in d9, hole sync). Far neighbours = neighbours of m outside the 11 named vertices. (i) at the 19 breaks: the non-breaking colouring's far
neighbours of m; (ii) all cycles: #far neighbours with a pair colour in c9 / d9 vs the break; (iii) steps 9..18: which far neighbours of m each swap recolours (pair, component)."""
import json, os
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
NM = ('p', 'xp', 'x2', 'x3', 'xm', 'z', 'wp', 'w2', 'w3', 'y', 'm')
out = []; c1 = Counter(); c2 = Counter(); c3 = Counter()
for l in open(os.path.join(HERE, '../jobav/jobav-cycles.jsonl')):
    r = json.loads(l)
    if r['source'] != 'census' or r['L'] != 20: continue
    n = r['names']; rot = r['rotation']; h = r['hole']; cols = [dict(zip(r['vertices'], c)) for c in r['colourings']]
    rho = {cols[0][n[k]]: cols[10][n[k]] for k in NM}; ri = {b: a for a, b in rho.items()}
    c9 = cols[9]; d9 = {v: ri[c] for v, c in cols[19].items()}; pair = {c9[n['p']], c9[n['m']]}
    inv = {v: k for k, v in n.items()}; m = n['m']; nb = [v for v in rot[m] if v != h]
    far = [v for v in nb if v not in inv]
    pc = [v for v in far if c9[v] in pair]; pd = [v for v in far if d9[v] in pair]
    bc, bd = r['pockets'][0]['reaches_wp'], None
    # d9 break flag = J false at 19 (pulled back) = step8break of period 1
    bc, bd = r['breaks']['step8break'][0], r['breaks']['step8break'][1]
    rec = dict(name=r['name'], hole=h, orientation=r['orientation'], deg_m=len(rot[m]), ring_nbrs=[inv[v] for v in nb if v in inv], far=far,
               c9=[c9[v] for v in far], d9=[d9[v] for v in far], pair=sorted(pair), far_pair_c=pc, far_pair_d=pd, brk_c=bc, brk_d=bd, steps=[])
    for st in r['steps'][9:19]:
        hit = [v for v in far if v in st['K']]
        if hit: rec['steps'].append(dict(pos=st['pos'], pair=st['pair'], far_nbrs_recoloured=hit, K_size=len(st['K'])))
    out.append(rec)
    brk = 'break' if bc or bd else 'no break'
    c2[(brk, 'far pair-coloured nbrs of m: c9 %d, d9 %d' % (len(pc), len(pd)))] += 1
    c2[(brk, 'both colourings have a far pair-coloured nbr of m: %s' % (bool(pc) and bool(pd)))] += 1
    c2[(brk, 'ring nbrs of m: %s' % ','.join(sorted(rec['ring_nbrs'])))] += 1
    if bc or bd:
        nonb = pd if bc else pc; nbcol = d9 if bc else c9
        c1['non-breaking colouring: all far nbrs of m non-pair (P = {m}): %s' % (not nonb)] += 1
        if nonb: c1['  overlap case %s %s h%d: deg(m) %d, far nbrs %s, colours %s, pair %s, pair-coloured %s' % (r['name'], r['orientation'], h, len(rot[m]), far, [nbcol[v] for v in far], sorted(pair), nonb)] += 1
        c1['breaking colouring: far pair-coloured nbrs %d' % len(pc if bc else pd)] += 1
    for s in rec['steps']: c3[(brk, 'step %d pair %s recolours %d far nbr(s) of m' % (s['pos'], ''.join(map(str, s['pair'])), len(s['far_nbrs_recoloured'])))] += 1
    c3[(brk, 'steps 9..18 recolouring a far nbr of m: %s' % ','.join(str(s['pos']) for s in rec['steps']))] += 1
json.dump(out, open(os.path.join(HERE, 'jobbe.json'), 'w'), indent=0)
print('(i) at the 19 breaks:'); [print('   ', v, k) for k, v in sorted(c1.items())]
print('(ii) all 256 L = 20 cycles:'); [print('   ', v, k) for k, v in sorted(c2.items())]
print('(iii) swaps between c9 and c19 that recolour far neighbours of m:'); [print('   ', v, k) for k, v in sorted(c3.items()) if 'steps 9..18' in k[1]]
print('    per-step totals:'); [print('   ', v, k) for k, v in sorted(c3.items()) if 'steps 9..18' not in k[1]]
