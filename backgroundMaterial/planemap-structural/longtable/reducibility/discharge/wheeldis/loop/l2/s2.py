"""EXPLORE round 22 (H-S, exploratory): Schnyder-orientation transfers in round 20's restricted LP (start set only).
Every interior vertex of a planar triangulation has a 3-orientation (out-degree exactly 3).  A row is an arrangement
plus an orientation of u's edges to its big link vertices; the small (5/6) neighbours take the remaining out-edges,
so O (u's out-edges among the bigs) ranges over 3 - #small <= |O| <= 3.  The orientation is adversarial: every
feasible O is a row.  Variables per oriented edge type kappa = tkey(tail, head, sides): a[kappa] (tail sends to
head) and b[kappa] (head sends to tail).  Big link k of u: k in O (u tail): -a[out_k] + b[out_k];
k not in O (u head): +a[in_k] - b[in_k].  Round 20's symmetric rules are a = x, b[kappa] = x[reverse kappa].
No separation: rows only raise t*, so a start-set t* that stays at 7/27 is a kill.
Usage: python3 s2.py [sym]   (sym = round 20's model on the same start set, as a check)"""
import sys, os, itertools, collections
import numpy as np, scipy.sparse as sps
from scipy.optimize import linprog
S2D = os.path.dirname(os.path.abspath(__file__)); SYM = 'sym' in sys.argv[1:]
src = open(os.path.join(S2D, 'l2.py')).read().replace('os.path.abspath(__file__)', repr(os.path.join(S2D, 'l2.py')), 1)
sys.argv = ['l2.py']; exec(src[:src.index('# ---- LP')])
def bigs(d, lk, sv):
    U = min(d, 9); Ui = U - 5; w = [li(c) for c in lk]; s = [li(c) for c in sv]; out = []
    for i in range(d):
        if w[i] >= 2:
            lm1, lm2, lp1, lp2 = w[(i - 1) % d], w[(i - 2) % d], w[(i + 1) % d], w[(i + 2) % d]
            sm, sp_ = s[(i - 1) % d], s[i]
            out.append((i, tkey(Ui, w[i], (lm1, lm2, sm), (lp1, lp2, sp_)), tkey(w[i], Ui, (lm1, sm, lm2), (lp1, sp_, lp2))))
    return out
COL = {}
def col(k):
    if k not in COL: COL[k] = NY + 1 + len(COL)
    return COL[k]
ri, ci, vv, b, RINFO = [], [], [], [], []; r = 0
for w in senders:
    for j in range(5):
        if w[j] >= 7: ri.append(r); ci.append(ix[root(list(w), j)]); vv.append(-1.0)
    ri.append(r); ci.append(NY); vv.append(-1.0); b.append(-1.0); r += 1
ns = r; nrow_by = collections.Counter()
for q, (d, lk, sv, ys, xs) in enumerate(ROWS):
    if SYM: orients = [None]
    else:
        B = bigs(d, lk, sv); nsmall = d - len(B)
        orients = [set(O) for m in range(max(0, 3 - nsmall), min(3, len(B)) + 1) for O in itertools.combinations(range(len(B)), m)]
    for O in orients:
        terms = collections.Counter()
        if SYM:
            for k, c in xs.items(): terms[('x', k)] += c
        else:
            for j, (i, ko, kin) in enumerate(B):
                if j in O: terms[('a', ko)] -= 1; terms[('b', ko)] += 1
                else: terms[('a', kin)] += 1; terms[('b', kin)] -= 1
        for z in ys: ri.append(r); ci.append(z); vv.append(1.0)
        ri.append(r); ci.append(NY); vv.append(-1.0)
        for k, c in terms.items():
            if c: ri.append(r); ci.append(col(k)); vv.append(float(c))
        b.append(d - 6.0); RINFO.append((q, None if O is None else tuple(sorted(O)))); r += 1; nrow_by[d] += 1
ncol = NY + 1 + len(COL)
A = sps.csr_matrix((vv, (ri, ci)), shape=(r, ncol)); cvec = np.zeros(ncol); cvec[NY] = 1.0
res = linprog(cvec, A_ub=A, b_ub=np.array(b), bounds=[(0, 1)] * NY + [(None, None)] + [(0, 3)] * len(COL), method='highs')
assert res.status == 0, res.message
t = res.x[NY]; duals = -res.ineqlin.marginals[ns:]; slack = (np.array(b) - A @ res.x)[ns:]
out = ['# s2.py %s: t* = %.6f (7/27 = %.6f, 13/49 = %.6f); %d arrangements, %d oriented rows %s, %d transfer columns' % (
    'sym' if SYM else 'orient', t, 7 / 27, 13 / 49, len(ROWS), len(RINFO), dict(sorted(nrow_by.items())), len(COL))]
out.append('binding rows (largest dual first): dual, source, arrangement, out-edges among bigs (link positions)')
for z in np.argsort(-duals)[:20]:
    if duals[z] <= 1e-9: break
    q, O = RINFO[z]; d, lk, sv, ys, xs = ROWS[q]
    Bp = [i for i, _, _ in bigs(d, lk, sv)]
    out.append('  %.4f  %s d=%d link %s s %s  bigs at %s, out %s' % (duals[z], RSRC[q], d, lk, sv, Bp,
                                                             None if O is None else [Bp[j] for j in O]))
nz = sorted(((res.x[c], k) for k, c in COL.items() if res.x[c] > 1e-9), reverse=True)
out.append('nonzero transfers: %d; largest: %s' % (len(nz), ', '.join('%s %s %.3f' % (k[0], tname(k[1]), v) for v, k in nz[:8])))
# HARD28-like rows: worst orientation slack
worst = {}
for z, (q, O) in enumerate(RINFO): worst[q] = min(worst.get(q, 9), slack[z])
nsl = sum(1 for d, ck, lab in HARD if ck_in(ck) ) if False else None
hs = [(lab, worst.get(RKEY.get((d, ck)), None)) for d, ck, lab in HARD]
out.append('HARD28-like rows slack (worst orientation): %d of %d slack' % (sum(1 for lab, v in hs if v is not None and v > 1e-7), len(hs)))
open(os.path.join(S2D, 's2_%s.txt' % ('sym' if SYM else 'orient')), 'w').write('\n'.join(out) + '\n')
print('\n'.join(out))
