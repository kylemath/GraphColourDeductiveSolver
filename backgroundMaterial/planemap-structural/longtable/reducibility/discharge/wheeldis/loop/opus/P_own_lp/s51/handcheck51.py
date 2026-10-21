# s51 control (b): the A78 cert q42aA78L carried into the xo LP, and one refined key's reduced cost vs s50.
#   python3 handcheck51.py REG CERT OUTCERT [ENGINE FLAGS...]
# 1. Every cert row is rebuilt by the s51 engine with xo on (receiverR2 rows now carry XQ[q] terms, no old x).
# 2. Each XQ[q] gets mrowX weights lambda_e <= 0 over q's candidates, summing to the receivers' weight on XQ[q] (so XQ's
#    ledger is exactly 0).  The split is chosen (HiGHS) to minimise sum max(0, -rc) over the xo columns, the s50 objective;
#    then rationalised and renormalised exactly.  Written as OUTCERT for lowerR2 (xo).
# 3. Hand part: the top s50 x_out key (8,7,(6,5,5,6,5),(6,7,6,6,5)) comes only from receiver 8 76765656/66565565 at i = 0
#    (out key, candidate (e+, e-) = (5, 5)); with that position's weight on that candidate its rc is w/tco = -24/421 (s50).
import sys, json, collections, itertools
from fractions import Fraction
import numpy as np
REG, CERT, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
B = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp'
E = B + '/s51/eng'
sys.argv = [E + '/pcheck.py', 'lowerR2'] + sys.argv[4:]
src = open(E + '/pcheck.py').read().rstrip().rsplit('\n', 1)[0]
G = {'__file__': E + '/pcheck.py', '__name__': 'pcheck_exec'}; exec(compile(src, E + '/pcheck.py', 'exec'), G)
assert G['XO']
recv_coef_R2 = G['recv_coef_R2']; xo_mrows = G['xo_mrows']; tauo = G['tauo']; sidex = G['sidex']; tauo_dec = G['tauo_dec']
G['load_patterns']()
C = json.load(open(CERT))
def W(c): return Fraction(c['w']) if isinstance(c['w'], str) else Fraction(c['w']).limit_denominator(10 ** 7)
tco = sum(W(c) * (1 if c['row'][0] == 'senderR2' else -1 if c['row'][0] == 'receiverR2' else 0) for c in C)
XQW = collections.defaultdict(Fraction); XQR = collections.defaultdict(list)
for c in C:
    r = c['row']
    if r[0] != 'receiverR2': continue
    for k, v in recv_coef_R2(int(r[1]), r[2], r[3], True).items():
        assert k[0] != 'x', 'old x under xo'
        if k[0] == 'XQ' and v: XQW[k[1]] += W(c) * v; XQR[k[1]].append(('%s %s/%s' % (r[1], r[2], r[3]), W(c), v))
print('tco', tco, '; XQ columns in the cert receivers:', len(XQW))
# split LP: variables lam (>= 0, = -weight) per (q, candidate), z_k >= -tot_k-ish  (min sum_k max(0, -rc_k), rc_k = -tot_k / tco)
cand = []   # (q, ee, coef dict)
for q in XQW:
    for cf, ee in xo_mrows(q): cand.append((q, ee, cf))
keys = sorted({k for _, _, cf in cand for k in cf if k[0] == 'xo'})
kid = {k: i for i, k in enumerate(keys)}
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
nl = len(cand); nk = len(keys)
# tot_k = sum_e w_e coef_e(k) = -sum_e lam_e coef_e(k);  -rc_k = tot_k / tco;  z_k >= tot_k / tco, z >= 0
R, Cc, V = [], [], []
for j, (q, ee, cf) in enumerate(cand):
    for k, v in cf.items():
        if k[0] == 'xo': R.append(kid[k]); Cc.append(j); V.append(-float(v) / float(tco))
for i in range(nk): R.append(i); Cc.append(nl + i); V.append(-1.0)
Aub = coo_matrix((V, (R, Cc)), shape=(nk, nl + nk)).tocsr(); bub = np.zeros(nk)
qs = list(XQW); qi = {q: i for i, q in enumerate(qs)}
Aeq = coo_matrix(([1.0] * nl, ([qi[q] for q, _, _ in cand], list(range(nl)))), shape=(len(qs), nl + nk)).tocsr()
beq = np.array([-float(XQW[q]) for q in qs])
cvec = np.r_[np.zeros(nl), np.ones(nk)]
res = linprog(cvec, A_ub=Aub, b_ub=bub, A_eq=Aeq, b_eq=beq, bounds=[(0, None)] * (nl + nk), method='highs-ds'); assert res.status == 0
lam = [Fraction(max(v, 0.0)).limit_denominator(10 ** 9) for v in res.x[:nl]]
# exact renormalisation per q
out = list(C)
byq = collections.defaultdict(list)
for j, (q, ee, cf) in enumerate(cand): byq[q].append(j)
wts = {}
for q, js in byq.items():
    s = sum(lam[j] for j in js)
    if s == 0: lam[js[0]] = Fraction(1); s = Fraction(1)
    for j in js: wts[j] = -(-XQW[q]) * lam[j] / s   # = XQW[q] * share (<= 0)
tot = collections.defaultdict(Fraction)
for j, (q, ee, cf) in enumerate(cand):
    if wts[j] == 0: continue
    out.append({'w': str(wts[j]), 'row': ['mrowX', [q[0], q[1], list(q[2]), list(q[3])], ee]})
    for k, v in cf.items(): tot[k] += wts[j] * v
for q, w in XQW.items(): tot[('XQ', q)] += w
assert all(v == 0 for k, v in tot.items() if k[0] == 'XQ'), 'XQ ledger not 0'
rc = {k: -v / tco for k, v in tot.items() if k[0] == 'xo' and v}
neg = sorted((v, k) for k, v in rc.items() if v < 0)
S = -sum((v for v, _ in neg), Fraction(0))
print('split LP: %d candidates over %d XQ; xo keys with rc < 0: %d, sum max(0, -rc) = %s = %.6f' % (nl, len(qs), len(neg), S, float(S)))
for v, k in neg[:8]: print('   rc %s  key %s' % (v, tauo_dec(k[1])))
json.dump(out, open(OUT, 'w'))
print('wrote', OUT, len(out), 'rows (+%d mrowX)' % (len(out) - len(C)))
# hand part
kstar = tauo(8, 7, sidex(6, 5, 5, 6, 5), sidex(6, 7, 6, 6, 5))
d, lk, sv = 8, '76765656', '66565565'; w_ = [int(ch) for ch in lk]; s_ = [int(ch) for ch in sv]
q0 = G['xo_vis'](8, 7, lambda k: w_[k % 8], lambda k: s_[k % 8])
cs = [(ee, cf) for cf, ee in xo_mrows(q0)]
hit = [(ee, cf[('xo', kstar)]) for ee, cf in cs if ('xo', kstar) in cf]
wr = [W(c) for c in C if c['row'][0] == 'receiverR2' and c['row'][2] == lk and c['row'][3] == sv][0]
others = [x for x in XQR[q0]]
print('hand: q0 = %s; candidates %d; k* is the out key of candidate(s) %s; receivers on q0: %s' % (q0, len(cs), hit, others))
print('hand: receiver weight %s x XQ coefficient %s (positions 0 and 2 are mirror images, same q0) = %s on XQ[q0]; tco %s; k* in no other cert row -> with q0\'s weight on candidate %s: tot(k*) = %s * (%s) => rc(k*) = %s (s50: -24/421)' % (
    wr, sum(v for _, _, v in XQR[q0]), XQW[q0], tco, hit[0][0], XQW[q0], hit[0][1], -(XQW[q0] * hit[0][1]) / tco))
print('split LP rc(k*) = %s' % rc.get(('xo', kstar), 0))
