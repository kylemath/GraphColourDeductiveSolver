# s37c (route b, Long Table): cluster rows for the d7 binder 7 8666655/5677657, fed with explore's census kills
# (cyl37.json = cen54's registry + two-engine window cylinders, part by part).  exec'd by pcheck.py:
#   python3 pcheck.py price37 pfile=pricer37.py <cert flags> cert=FILE [sol=FILE] cyl=cyl37.json [tag=..]
# Cell = exact letters of the binder's 14 census slots (privates of w0 (8), w1..w4 (6) and the ring-3 vertices of s3, s4,
# s5, s6).  Only the 6-spoke privates p11 p21 p31 p41 enter terms (M -> exact h); a (p11,p21,p31,p41) group is alive iff
# some filling of the other slots is uncovered in its structural part and each p is amask-allowed (filt16) and non-R6.
# 1. lifting: spread the binder's cert weight over the alive groups and re-weight the mrowR2 rows of the binder's four
#    M signatures, so that every column keeps rc >= 0 (x, D, lq priced at their caps as lowerR2).  Infeasible = the
#    cluster rows break the cert.  2. primal: binder load at sol with M (as solved) vs max over alive groups of exact h.
import json, itertools, collections
import numpy as np
from fractions import Fraction
from scipy.optimize import linprog
TAG = OPT.get('tag', 'run'); OUTF = open(os.path.join(OPT.get('outdir', '.'), 'price37_%s.log' % TAG), 'w')
def P(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); OUTF.write(s + '\n'); OUTF.flush()
LKs, SVs = OPT.get('lk', '8666655'), OPT.get('sv', '5677657'); d = 7; U = 7
wl = [int(c) for c in LKs]; sl = [int(c) for c in SVs]
CY = json.load(open(OPT['cyl'])); assert CY['row'] == '7 %s/%s' % (LKs, SVs)
def count(cyl, slots, lets):
    """fillings of slots (letters lets) inside the union of cylinders (cen51/cen54 count)"""
    cyl = [c for c in cyl if all(v in lets[k] for k, v in c.items())]
    if not cyl: return 0
    if any(not c for c in cyl):
        n = 1
        for x in slots: n *= len(lets[x])
        return n
    fr = collections.Counter(x for c in cyl for x in c); x = max(slots, key=lambda s: fr[s])
    rest = [s for s in slots if s != x]; tot = 0
    for l in lets[x]:
        sub = [{k: v for k, v in c.items() if k != x} for c in cyl if c.get(x, l) == l]
        tot += count(sub, rest, lets)
    return tot
PARTS = []
for p in CY['parts']:
    cyl = [c['req'] for c in p['registry']] + [w['req'] for w in p['windows']]
    PARTS.append((p['part'], p['fixed'], p['free'], {k: tuple(v) for k, v in p['letters'].items()}, cyl))
    P('part %s: %d registry + %d window cylinders; covered %.4f%%' % (p['part'], len(p['registry']), len(p['windows']), 100.0 * p['covered'] / p['fillings']))
PRIV = ['p11', 'p21', 'p31', 'p41']; sixes = [1, 2, 3, 4]
def uncovered(pv, extra=None):
    """number of uncovered fillings of the other slots with the 6-privates fixed to pv (extra: more fixed slots)"""
    tot = 0; fx = dict(zip(PRIV, pv)); fx.update(extra or {})
    for lab, fixed, free, lets, cyl in PARTS:
        if any(k in fixed and fixed[k] != v for k, v in fx.items()): continue
        if any(k in free and v not in lets[k] for k, v in fx.items()): continue
        sub = {x: ((fx[x],) if x in fx else lets[x]) for x in free}
        n = 1
        for x in free: n *= len(sub[x])
        tot += n - count(cyl, free, sub)
    return tot
def amask_j(j): return amask(U, wl[(j - 2) % d], wl[(j - 1) % d], wl[(j + 1) % d], wl[(j + 2) % d], sl[(j - 2) % d], sl[(j - 1) % d], sl[j], sl[(j + 1) % d])
def msig(j): return sig2_of(U, wl[(j + 1) % d], sl[j], sl[(j - 1) % d], wl[(j - 1) % d], wl[(j + 2) % d], wl[(j - 2) % d]) + ((amask_j(j),) if F16 else ())
def hkey(j, p): return h2_of((U, wl[(j + 1) % d], sl[j], p, sl[(j - 1) % d], wl[(j - 1) % d]), wl[(j + 2) % d], wl[(j - 2) % d])
allowed = {j: [p for p in LET if (not F16 or (amask_j(j) >> (p - 5)) & 1) and not isR6((U, wl[(j + 1) % d], sl[j], p, sl[(j - 1) % d], wl[(j - 1) % d]))] for j in sixes}
P('binder %s/%s: amask/R6-allowed privates %s' % (LKs, SVs, {'p%d1' % j: allowed[j] for j in sixes}))
ALIVE = {}
for pv in itertools.product(*[allowed[j] for j in sixes]):
    n = uncovered(pv)
    if n: ALIVE[pv] = n
NALL = 1
for j in sixes: NALL *= len(allowed[j])
P('6-private groups: %d allowed, %d alive (have an uncovered filling of the other 10 slots)' % (NALL, len(ALIVE)))
for k, j in enumerate(sixes):
    P('  p%d1 letters alive: %s' % (j, sorted({pv[k] for pv in ALIVE})))
# ---------------- cert ----------------
load_patterns(); xon = 'xon' in FLAGS
C = json.load(open(OPT['cert'])); SR = {(wd, tuple(map(str, b))): cf for wd, cf, b in R2_sender_rows()}
row0 = recv_coef_R2(d, LKs, SVs, xon)
BS = {msig(j) for j in sixes if ('M', msig(j)) in row0}
P('binder M signatures: %s' % sorted(BS))
base = collections.defaultdict(Fraction); tco = Fraction(0); BW = None; D0 = Fraction(0); freed = []
for c in C:
    w = Fraction(c['w']).limit_denominator(10 ** 7); row = c['row']
    if row[0] == 'senderR2':
        tco += w; D0 += w
        for k, v in SR[(row[1], tuple(map(str, row[2])))].items(): base[k] += w * v
    elif row[0] == 'cons2':
        for k, v in cons2_coef(tuple(row[1]), tuple(row[2])).items(): base[k] += w * v
    elif row[0] == 'mrowR2':
        if tuple(row[1]) in BS: freed.append((tuple(row[1]), tuple(row[2]), w)); continue
        base[('h', tuple(row[2]))] += w; base[('M', tuple(row[1]))] -= w
    elif row[0] == 'mrowL':
        sg = tuple(row[1]); k = tuple(row[2]); base[('lq', k)] += w; base[('lQ', sg)] -= w
    elif row[0] == 'receiverR2':
        tco -= w; dd, lk, sv = int(row[1]), row[2], row[3]; D0 += w * (dd - 6)
        if (dd, lk, sv) == (d, LKs, SVs): BW = w; continue
        for k, v in recv_coef_R2(dd, lk, sv, xon).items(): base[k] += w * v
    else: raise SystemExit('row type %s not handled' % row[0])
assert BW is not None
P('cert %s: %d rows, tco %s, binder weight %s, freed mrowR2 rows of the binder signatures: %d %s' % (OPT['cert'], len(C), tco, BW, len(freed), [(a, b, str(w)) for a, b, w in freed]))
CAPS = {'x': Fraction(OPT.get('xcap', '3')), 'D': Fraction(OPT.get('dcap', '3')), 'lq': Fraction(OPT.get('lqcap', '3'))}
def cell_coef(pv):
    cf = collections.Counter(row0)
    for j, p in zip(sixes, pv):
        if ('M', msig(j)) in row0: cf[('M', msig(j))] -= 1
        cf[('h', hkey(j, p))] += 1
    return {k: v for k, v in cf.items() if v}
def lift(groups, label):
    """LP over lam (binder weight split, sum 1) and mu (freed mrowR2 weights, <= 0): minimise the worst tot over the
    uncapped columns (e); then, if e <= 0, the capped columns' cost.  Returns (e, bound or None, worst list)"""
    cols = list(groups); rows = {pv: cell_coef(pv) for pv in cols}
    mus = sorted({(sg, k) for sg in BS for k in sig2_keys(sg)})
    keys = sorted({k for cf in rows.values() for k in cf} | set(base) | {('h', k) for _, k in mus} | {('M', sg) for sg, _ in mus}, key=str)
    keys = [k for k in keys if k[0] != 't']; kix = {k: i for i, k in enumerate(keys)}
    nl, nm = len(cols), len(mus); A = np.zeros((len(keys), nl + nm)); b0 = np.array([float(base[k]) for k in keys])
    for c_, pv in enumerate(cols):
        for k, v in rows[pv].items():
            if k in kix: A[kix[k], c_] += float(BW) * v
    for m_, (sg, k) in enumerate(mus):
        A[kix[('h', k)], nl + m_] += 1.0; A[kix[('M', sg)], nl + m_] -= 1.0
    capd = np.array([k[0] in CAPS for k in keys]); unc = ~capd
    bnd = [(0, None)] * nl + [(None, 0)] * nm
    Aeq = np.hstack([np.ones((1, nl)), np.zeros((1, nm))])
    # LP1: min e, A_unc x - e <= -b0_unc
    nv = nl + nm
    r1 = linprog(np.r_[np.zeros(nv), 1.0], A_ub=np.hstack([A[unc], -np.ones((unc.sum(), 1))]), b_ub=-b0[unc],
                 A_eq=np.hstack([Aeq, np.zeros((1, 1))]), b_eq=[1.0], bounds=bnd + [(None, None)], method='highs')
    e = r1.x[-1]; tv = b0 + A @ r1.x[:-1]
    worst = sorted(((tv[i], keys[i]) for i in range(len(keys)) if unc[i] and tv[i] > 1e-9), reverse=True)[:10]
    bound = None
    if e <= 1e-9:
        # LP2: min sum cap*s over capped keys, s >= tot, s >= 0, uncapped tot <= 0
        ci = np.where(capd)[0]; ns = len(ci); cap = np.array([float(CAPS[keys[i][0]]) for i in ci])
        Aub = np.vstack([np.hstack([A[unc], np.zeros((unc.sum(), ns))]), np.hstack([A[ci], -np.eye(ns)])])
        bub = np.r_[-b0[unc] + 1e-12, -b0[ci]]
        r2 = linprog(np.r_[np.zeros(nv), cap], A_ub=Aub, b_ub=bub, A_eq=np.hstack([Aeq, np.zeros((1, ns))]), b_eq=[1.0],
                     bounds=bnd + [(0, None)] * ns, method='highs')
        bound = float(D0 / tco) - r2.fun / float(tco) if r2.status == 0 else None
        lam = r1.x[:nl]
    P('\n[%s] groups %d; lifting worst uncapped tot e = %.9f -> %s%s' % (label, nl, e,
      'cert VALID in the cluster class' if e <= 1e-9 else 'cert INVALID: no lifting keeps every rc >= 0',
      '; lifted bound t >= %.9f (cert %s)' % (bound, float(D0 / tco)) if bound is not None else ''))
    for tvv, k in worst: P('   column %s rc %.6f' % (k, -tvv / float(tco)))
    if e <= 1e-9:
        for c_ in np.argsort(-r1.x[:nl])[:4]:
            if r1.x[c_] > 1e-9: P('   lifting group (p11,p21,p31,p41) = %s lam %.4f' % (cols[c_], r1.x[c_]))
    return e, bound, worst
# ---------------- primal load ----------------
def primal(sol):
    Sj = json.load(open(sol)); t = Sj['t']
    YV = Sj['y']; HV = {tuple(k): v for k, v in Sj['h']}
    tab = {}
    for nm in ('z', 'q', 'v', 'r', 'rr', 'g', 'f', 'lq', 'lQ'): tab[nm] = {tuple(k): v for k, v in Sj.get(nm, [])}
    tab['D'] = {eval(k): v for k, v in Sj.get('D', [])}; XV = {int(k): v for k, v in Sj.get('x', {}).items()}
    LQV.clear(); LQV.update(tab['lq']); LQQ.clear(); LQQ.update(tab['lQ'])
    def val(k):
        t_, a = k
        if t_ == 'y': return YV.get(rname(a), 0.0)
        if t_ == 'x': return XV.get(a, 0.0)
        if t_ == 'h': return HV.get(a, 0.0)
        if t_ == 'M': ks = sig2_keys(a); return max(HV.get(kk, 0.0) for kk in ks) if ks else 0.0
        if t_ == 'lQ': return l3q_Qeff(*a)
        if t_ in tab: return tab[t_].get(a, 0.0)
        raise SystemExit('primal: term type %s not handled' % t_)
    L0 = sum(c * val(k) for k, c in row0.items())
    loads = {pv: sum(c * val(k) for k, c in cell_coef(pv).items()) for pv in ALIVE}
    L1 = max(loads.values()); arg = max(loads, key=loads.get)
    Mv = {j: val(('M', msig(j))) for j in sixes}
    P('\nprimal %s (t = %.9f): binder load %.9f, cap %.9f (slack %.3g)' % (sol, t, L0, d - 6 + t, d - 6 + t - L0))
    P('  M values %s; h by letter %s' % ({'p%d1' % j: round(Mv[j], 6) for j in sixes},
      {'p%d1' % j: {p: round(HV.get(hkey(j, p), 0.0), 6) for p in allowed[j]} for j in sixes}))
    P('  cluster rows: max load over the %d alive groups %.9f at %s; load drop %.9f; projected gain |dual| x drop = %.6f' % (
      len(ALIVE), L1, arg, L0 - L1, float(-BW / tco) * (L0 - L1)))
    return L0, L1
e, bound, worst = lift(ALIVE, 'census kills (registry + two-engine windows) + filt16 amask')
eA, bA, _ = lift({pv: 1 for pv in itertools.product(*[allowed[j] for j in sixes])}, 'control: amask only, no census kills')
if 'sol' in OPT: primal(OPT['sol'])
OUTF.close()
