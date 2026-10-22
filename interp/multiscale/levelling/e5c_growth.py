# E5c: does the forced height period of non-3-colourable 6-regular tori grow with size?  Square-ish tori T(p,p,r)
# and T(p,q,r) with large edge-width.  Reports min over 4-colourings of |t1|^2, |t2|^2 and max(|t1|^2,|t2|^2).
import json, sys, itertools
import e5_torus as E
from torus_summ import ew
L2 = sorted(set(4*(a*a+b*b-a*b) for a in range(-12, 13) for b in range(-12, 13)))
def minsq(p, q, r, which):
    for t in L2:
        tgt = (t, None) if which == 1 else ((None, t) if which == 2 else (t, t))
        if E.solve(p, q, r, target=tgt): return t
out = open('e5c_growth.jsonl', 'w')
cases = []
for p in range(4, 13):
    for r in range(p):
        cases.append((p, p, r))
for (p, q) in [(6, 9), (9, 6), (8, 10), (10, 8), (12, 6), (6, 12), (15, 5), (5, 15), (20, 4), (24, 3)]:
    for r in range(p): cases.append((p, q, r))
seen = set()
for (p, q, r) in cases:
    n, adj, nb, idx, simple = E.torus(p, q, r)
    if not simple or n > 150: continue
    if E.solve(p, q, r, ncol=3): continue
    if not E.solve(p, q, r, ncol=4):
        rec = dict(p=p, q=q, r=r, n=n, ew=ew(p, q, r), col4=False); out.write(json.dumps(rec)+'\n'); out.flush(); continue
    rec = dict(p=p, q=q, r=r, n=n, ew=ew(p, q, r), col4=True, zero=E.solve(p, q, r, target=('zero', 'zero')))
    rec['t1sq'] = minsq(p, q, r, 1); rec['t2sq'] = minsq(p, q, r, 2); rec['maxsq'] = minsq(p, q, r, 3)
    out.write(json.dumps(rec)+'\n'); out.flush(); print(rec, flush=True)
