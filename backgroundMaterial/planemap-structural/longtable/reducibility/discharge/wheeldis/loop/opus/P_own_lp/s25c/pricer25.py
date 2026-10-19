# Stage 25 pricer (cluster rows, RELAY_SPEC_s20.md).  exec'd inside the pcheck namespace (after prelay2.py):
#   python3 pcheck.py price25 <flags> cert=FILE lev=L [ptag=T]
# New column family phi (five -> big spoke, in addition to y): key = (the five's link read from the big, n = (U,n1..n4))
# + the small/big classes of the five's five hats h0..h4, each MASKED (code 2) unless the big's row can read it.
#   h0 = hat(U,n1) = w_{i+2},  h4 = hat(n4,U) = w_{i-2}                                  always visible (zh, stage 13)
#   h1 = hat(n1,n2) = s_{i+1} if n1 = 5;  h3 = hat(n3,n4) = s_{i-2} if n4 = 5            lev >= 1 (standard row)
#   h2 = hat(n2,n3) = private of the face apex five if (n1,n2) = (5,5) or (n4,n3) = (5,5)  lev >= 2 (cluster row, e-vertex)
#   h2 = e_bc of the face (v, n2, n3) if (n2,n3) = (5,5)                                  lev >= 3 (cluster row, k-vertex)
# Pricing = exact lifting test: every cert sender row may be replaced by any convex mix of the sender contexts that give
# the same old coefficient row; every cert receiver row by any mix of its completions on the hidden hats (lev >= 2).
# The old cert is valid in the new class iff the lifting LP is feasible (all phi reduced costs >= 0).
import json, collections, random
from fractions import Fraction
from scipy.optimize import linprog
LEV = int(OPT.get('lev', '1')); TAG = OPT.get('ptag', 'L%d' % LEV)
OUT = open('pricer25_%s.log' % TAG, 'w')
def P(*a):
    s = ' '.join(str(x) for x in a); print(s); OUT.write(s + '\n'); OUT.flush()
MASK = 2
def vis(n, lev):
    """which of h0..h4 the big's row reads, as a function of the five's link n = (U, n1, n2, n3, n4) only"""
    U, n1, n2, n3, n4 = n
    v = [True, lev >= 1 and n1 == 5, False, lev >= 1 and n4 == 5, True]
    if lev >= 2 and ((n1 == 5 and n2 == 5) or (n4 == 5 and n3 == 5)): v[2] = True
    if lev >= 3 and n2 == 5 and n3 == 5: v[2] = True
    return v
def phikey(n, h, lev):
    v = vis(n, lev); hm = tuple(h[k] if v[k] else MASK for k in range(5))
    a = tuple(n) + hm; b = (n[0], n[4], n[3], n[2], n[1]) + tuple(reversed(hm))
    return min(a, b)
def phi_sender(w, H, lev):
    """phi terms of a five with canonical word w and hat classes H[0..4] (H[k] between w_k and w_{k+1})"""
    cf = collections.Counter()
    for j in range(5):
        if w[j] >= 7:
            n = tuple(w[(j + i) % 5] for i in range(5)); h = tuple(H[(j + i) % 5] for i in range(5))
            cf[('phi', phikey(n, h, lev))] += 1
    return cf
def phi_recv(d, w, s, q=None, lev=1):
    """phi terms (+1 load) of a receiver (link w, apexes s); q = {i: class of the hidden hat h2 of link five w_i}"""
    cf = collections.Counter(); U = min(d, 9)
    for i in range(d):
        if w[i] != 5: continue
        n = (U, w[(i + 1) % d], s[i], s[(i - 1) % d], w[(i - 1) % d])
        h = [c2(w[(i + 2) % d]), c2(s[(i + 1) % d]) if w[(i + 1) % d] == 5 else MASK, MASK,
             c2(s[(i - 2) % d]) if w[(i - 1) % d] == 5 else MASK, c2(w[(i - 2) % d])]
        if vis(n, lev)[2]: h[2] = q[i]
        cf[('phi', phikey(n, tuple(h), lev))] += 1
    return cf
# ---- physical test: random 2-balls around a five v with a big spoke u; v reads its hats, u reads from its own rotation
def selftest(N=100000, lev=3, broken=False):
    rng = random.Random(25); bad = 0
    for _ in range(N):
        # v's spokes x0..x4 (x0 = u, big), hats t_k between x_k and x_{k+1}; each five spoke's rotation is explicit
        L = lambda: rng.choice(LET)
        x = [rng.choice((7, 8, 9))] + [rng.choice((5, 5, 6, 7)) for _ in range(4)]; t = [L() for _ in range(5)]
        H = [c2(z) for z in t]
        ks = phikey(tuple(x), tuple(H), lev)
        # u's view: u's link around v (= w_i): w_{i+1} = x1, w_{i-1} = x4, apex s_i = x2 (other common nbr of v, x1),
        # s_{i-1} = x3; w_{i+2} = t0 (common nbr of u, x1 other than v), w_{i-2} = t4.
        # s_{i+1} = apex of (x1, w_{i+2}) = the nbr of x1 adjacent to t0 other than u: from x1's rotation if x1 = 5:
        rot1 = ['v', 'u', 't0', 'X1', 'x2'] if x[1] == 5 else None    # x1's 5 nbrs in order: v, u, t0, ?, x2 -> ? = t1
        s_ip1 = t[1] if rot1 else None                                  # hat(x1, x2) is x1's nbr between t0 and x2
        rot4 = ['v', 'x3', 'Y', 't4', 'u'] if x[4] == 5 else None
        s_im2 = t[3] if rot4 else None
        hu = [c2(t[0]), c2(s_ip1) if x[1] == 5 else MASK, MASK, c2(s_im2) if x[4] == 5 else MASK, c2(t[4])]
        n = (x[0], x[1], x[2], x[3], x[4])
        if vis(n, lev)[2]:
            # face (v, x1, x2): x2 = 5 is the face apex for u; its link (v, x1, s_{i+1}, q, x3): q = hat(x2, x3) = t2
            # face (v, x4, x3): q = s_{i-1}'s private = hat(x2, x3) = t2 ; k-vertex face (v, x2, x3): e = hat(x2,x3) = t2
            hu[2] = c2(t[1] if broken else t[2])
        if broken and not vis(n, lev)[2]: hu[0], hu[4] = hu[4], hu[0]
        ku = phikey(n, tuple(hu), lev)
        # u's own orientation is arbitrary: also read reflected
        ku2 = phikey((n[0], n[4], n[3], n[2], n[1]), tuple(reversed(hu)), lev)
        if ku != ks or ku2 != ks: bad += 1
    return N, bad
if 'selftest' in FLAGS:
    for lv in (1, 2, 3):
        n_, b_ = selftest(lev=lv); n2_, bb_ = selftest(lev=lv, broken=True)
        P('physical test lev %d: %d fives, %d key mismatches; broken-key control: %d mismatches' % (lv, n_, b_, bb_))
# ---- lifting LP ----------------------------------------------------------------------------------------------------
load_patterns(); xon = 'xon' in FLAGS
C = json.load(open(OPT['cert']))
def sender_contexts(wd):
    """all (H, F) class contexts of word wd that pass R2_sender_rows' filters (hat5: all hats), with their old coef rows"""
    w = tuple(int(ch) for ch in wd); n = 5; sixes = [k for k in range(n) if w[k] == 6]
    allow = {k: {(a_, q, b_) for a_ in LET for q in LET for b_ in LET if not isR6((5, w[(k + 1) % n], a_, q, b_, w[(k - 1) % n]))} for k in sixes}
    base = collections.Counter()
    for j in range(n):
        if w[j] >= 7: base[('y', root(list(w), j))] += 1
    out = []
    for hb in itertools.product((0, 1), repeat=5):
        H = dict(enumerate(hb))
        for fb in itertools.product((0, 1), repeat=len(sixes)):
            Fn = dict(zip(sixes, fb))
            if any(not any((a_, q, b_) in allow[k] for a_ in CLS2[H[k]] for q in CLS2[Fn[k]] for b_ in CLS2[H[(k - 1) % n]]) for k in sixes): continue
            if HX and not hx_ok(w, H, Fn): continue
            cf = collections.Counter(base)
            for k in range(n):
                if H[k]:
                    for k2, c2v in hat_sender_terms(w, H, Fn, k).items(): cf[k2] += c2v
            for k in sixes:
                L5 = lambda c: 7 if c else 5
                cf[('g', g2_of(w[(k + 1) % n], L5(H[k]), L5(Fn[k]), L5(H[(k - 1) % n]), w[(k - 1) % n], w[(k + 2) % n], w[(k - 2) % n]))] += 1
            out.append((list(hb) + ['|'] + list(fb), H, {k: v for k, v in cf.items() if v}))
    return w, out
def recv_hidden(d, w, s, lev):
    """hidden-hat positions of the receiver at this level: {i: candidate classes}; a face apex five's private q must
    leave that five's link non-R5 (q = 5 or 6 for class 0 (some letter), q in 7..9 for class 1)"""
    U = min(d, 9); hid = {}
    for i in range(d):
        if w[i] != 5: continue
        n = (U, w[(i + 1) % d], s[i], s[(i - 1) % d], w[(i - 1) % d])
        if not vis(n, lev)[2]: continue
        cls = []
        for c in (0, 1):
            ok = False
            for qq in CLS2[c]:
                if n[1] == 5 and n[2] == 5:    # apex five s_i: link (w_i, w_{i+1}, s_{i+1}, q, s_{i-1})
                    lk5 = (w[i], w[(i + 1) % d], s[(i + 1) % d], qq, s[(i - 1) % d])
                elif n[4] == 5 and n[3] == 5:  # apex five s_{i-1}: link (w_{i-1}, w_i, s_i, q, s_{i-2})
                    lk5 = (w[(i - 1) % d], w[i], s[i], qq, s[(i - 2) % d])
                else: lk5 = None               # k-vertex face: e_bc adjacent to s_i, s_{i-1}; their links are not all known
                if lk5 is None or not isR5(lk5): ok = True; break
            if ok: cls.append(c)
        vid = ('apexpriv', i % d) if (n[1] == 5 and n[2] == 5) else ('apexpriv', (i - 1) % d) if (n[4] == 5 and n[3] == 5) else ('e', i)
        hid[vid] = sorted(set(hid.get(vid, cls)) & set(cls)); POS.setdefault(vid, []).append(i)
    return hid
POS = {}
rows = []   # (kind, label, weight, [ (ctxlabel, phi Counter) ])
tco = Fraction(0); Dv = Fraction(0)
for c in C:
    wgt = Fraction(c['w']).limit_denominator(10 ** 7); row = c['row']
    if row[0] == 'senderR2':
        tco += wgt; Dv += wgt
        w, ctxs = sender_contexts(row[1])
        lab = [x if x == '|' else int(x) for x in row[2]]
        mine = [cx for cx in ctxs if cx[0] == lab]
        assert len(mine) == 1, (row, len(mine))
        same = [cx for cx in ctxs if cx[2] == mine[0][2]]
        rows.append(('S', '%s %s' % (row[1], ''.join(map(str, row[2]))), wgt, [(''.join(map(str, cx[0])), phi_sender(w, cx[1], LEV)) for cx in same]))
    elif row[0] == 'receiverR2':
        d, lk, sv = int(row[1]), row[2], row[3]; tco -= wgt; Dv += wgt * (d - 6)
        w = [int(ch) for ch in lk]; s = [int(ch) for ch in sv]
        POS.clear(); hid = recv_hidden(d, w, s, LEV); opts = []; vids = sorted(hid, key=str)
        for combo in itertools.product(*[hid[v] for v in vids]):
            q = {i: cc for v, cc in zip(vids, combo) for i in POS[v]}; opts.append((str(dict(zip(map(str, vids), combo))), phi_recv(d, w, s, q, LEV)))
        rows.append(('R', '%d %s %s' % (d, lk, sv), wgt, opts))
P('cert', OPT['cert'], 'rows', len(C), 'tco', tco, 'objective', Dv / tco, 'level', LEV)
for k, lab, wgt, opts in rows:
    P('  %s %-40s w=%-8s contexts=%d' % (k, lab, wgt, len(opts)))
# fixed pricing (cert labels only, receivers at their first hidden completion) and the lifting LP
keys = sorted({kk for _, _, _, opts in rows for _, cf in opts for kk in cf})
kix = {kk: i for i, kk in enumerate(keys)}
var = []   # (row index, ctx index)
for r_, (_, _, _, opts) in enumerate(rows):
    for c_ in range(len(opts)): var.append((r_, c_))
# tot[key] = sum_vars lam * sign * coef, sign = +1 (sender, w>0, phi coef +1) ; receivers: w<0, coef +1 -> -|w|
import numpy as np
A = np.zeros((len(keys), len(var)))
for v_, (r_, c_) in enumerate(var):
    kind = rows[r_][0]; cf = rows[r_][3][c_][1]
    for kk, val in cf.items(): A[kix[kk], v_] += val * (1 if kind == 'S' else -1)
Aeq = np.zeros((len(rows), len(var))); beq = np.zeros(len(rows))
for v_, (r_, c_) in enumerate(var): Aeq[r_, v_] = 1
for r_, (_, _, wgt, _) in enumerate(rows): beq[r_] = float(abs(wgt))
# minimise the worst violation e: A lam <= e  (rc = -tot >= -e)
nv = len(var)
cobj = np.zeros(nv + 1); cobj[-1] = 1
Aub = np.hstack([A, -np.ones((len(keys), 1))]); bub = np.zeros(len(keys))
res = linprog(cobj, A_ub=Aub, b_ub=bub, A_eq=np.hstack([Aeq, np.zeros((len(rows), 1))]), b_eq=beq,
              bounds=[(0, None)] * nv + [(None, None)], method='highs')
e = res.x[-1]; lam = res.x[:-1]
P('\nphi keys touched: %d.  lifting LP: best worst-case tot = %.9f  (%s)' % (len(keys), e, 'FEASIBLE: old cert valid, null' if e <= 1e-12 else 'INFEASIBLE: some phi column has rc < 0 under every lifting'))
# total negative mass under the best lifting: sum of positive tot (the rc < 0 columns)
tv = A @ lam
P('columns with rc < 0 at the best lifting: %d, sum of -rc = %.9f' % (int((tv > 1e-12).sum()), float(tv[tv > 1e-12].sum())))
for i in np.argsort(-tv)[:12]:
    if tv[i] <= 1e-12: break
    who = [(rows[r_][1], rows[r_][3][c_][0], round(lam[v_], 6), int(A[i, v_])) for v_, (r_, c_) in enumerate(var) if A[i, v_] and lam[v_] > 1e-12]
    P('  NEG phi', keys[i][1], 'rc = %.6f' % -tv[i], who)
P('\nlifting used (contexts with weight):')
for v_, (r_, c_) in enumerate(var):
    if lam[v_] > 1e-12: P('  %s %s ctx %s lam %.6f' % (rows[r_][0], rows[r_][1], rows[r_][3][c_][0], lam[v_]))
# exact fixed-label pricing (no lifting): each cert row at its own label, receivers at every hidden completion's min
tot = collections.defaultdict(Fraction)
for kind, lab, wgt, opts in rows:
    for kk, val in opts[0][1].items(): tot[kk] += wgt * val
neg = sorted((kk for kk in tot if tot[kk] > 0), key=lambda kk: -tot[kk])
P('\nlabel-only pricing (exact, no lifting): %d phi columns with rc < 0' % len(neg))
for kk in neg: P('  rc = %s = %.6f  %s' % (-tot[kk] / tco, float(-tot[kk] / tco), kk[1]))
OUT.close()
