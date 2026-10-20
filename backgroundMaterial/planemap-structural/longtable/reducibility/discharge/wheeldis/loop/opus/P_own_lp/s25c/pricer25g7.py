# Stage 25, section s25c-g (RELAY_SPEC_s20.md): explore's 10 g7_ kills (Studio dc1ff9f9) as forbidden cells.
#   python3 pcheck.py price25 pfile=pricer25g7.py <flags> cert=FILE [fy]
# Cluster cell of the cert binder 7 7665566/6675676 = exact letters of the privates of its 6-spokes w1, w2, w5, w6 and of
# its 7-spoke w0 (two), plus the four ring-3 letters of the g7 header.  In a cell the binder's M terms become the exact h2
# of the cell's privates (the cluster row reads them).  Lifting test: spread the binder's cert weight over the surviving
# cells so that every column keeps rc >= 0.  Done without and with the g7 kills (and with fy if the flag is on).
import json, collections, re
import numpy as np
from fractions import Fraction
from scipy.optimize import linprog
OUTF = open('pricer25_g7%s.log' % ('_fy' if FY else ''), 'w')
def P(*a):
    s = ' '.join(str(x) for x in a); print(s); OUTF.write(s + '\n'); OUTF.flush()
G7SLOTS = ['p01', 'p02', 'p11', 'p21', 'p51', 'p61', 'tp21/s2', 'ts2/s3/s4', 'ts4', 'tp51/s4']
def g7_parse(nm):
    """name -> {vertex: letter} in the coordinates of the name's own row 7 7665566/6765766"""
    f = nm.split('_'); lk, sw, sl = f[1], f[2], f[3]; req = {}
    assert len(lk) == 8 and len(sw) == 7 and len(sl) == 10, nm
    if lk[0] == 'u': req['v'] = 7
    for i, ch in enumerate(lk[1:]):
        if ch != '.': req['w%d' % i] = int(ch)
    for i, ch in enumerate(sw):
        if ch != '.': req['s%d' % i] = int(ch)
    for k, ch in enumerate(sl):
        if ch != '.': req[G7SLOTS[k]] = int(ch)
    return req
def mirror_vertex(x, d=7):
    """reflection w_i -> w_{-i}, s_i -> s_{-i-1}; privates p_{I,K} -> p_{-I, deg-5+1-K}; t(a/b/..) -> t(images)"""
    if x == 'v': return 'v'
    if x[0] == 'w': return 'w%d' % ((-int(x[1:])) % d)
    if x[0] == 's': return 's%d' % ((-int(x[1:]) - 1) % d)
    if x[0] == 'p':
        I, K = int(x[1]), int(x[2]); n = THEIRS_W[I] - 5
        return 'p%d%d' % ((-I) % d, n + 1 - K)
    if x[0] == 't': return 't' + '/'.join(sorted(mirror_vertex(y) for y in x[1:].split('/')))
THEIRS_W = [7, 6, 6, 5, 5, 6, 6]; THEIRS_S = [6, 7, 6, 5, 7, 6, 6]
OURS_W = [7, 6, 6, 5, 5, 6, 6]; OURS_S = [6, 6, 7, 5, 6, 7, 6]
assert all(OURS_W[(-i) % 7] == THEIRS_W[i] and OURS_S[(-i - 1) % 7] == THEIRS_S[i] for i in range(7))
names = [l.split()[0] for l in open(OPT.get('g7', 'g7_names.txt')) if l.startswith('g7_')]
P('g7 names read: %d' % len(names))
ROWV = {'v': 7}; ROWV.update({'w%d' % i: OURS_W[i] for i in range(7)}); ROWV.update({'s%d' % i: OURS_S[i] for i in range(7)})
def tnorm(x): return 't' + '/'.join(sorted(x[1:].split('/'))) if x[0] == 't' else x
kills = []
for nm in names:
    req = {tnorm(mirror_vertex(tnorm(x))): v for x, v in g7_parse(nm).items()}
    fixed = {x: v for x, v in req.items() if x in ROWV}
    if any(ROWV[x] != v for x, v in fixed.items()): P('  %s: does not apply to this row (%s)' % (nm, fixed)); continue
    cell = {x: v for x, v in req.items() if x not in ROWV}
    kills.append((nm, cell)); P('  %s -> our cell constraints %s' % (nm, cell))
# private cells: p11 (w1), p21 (w2), p51 (w5), p61 (w6), p01, p02 (w0); ring-3 letters free (5..9)
load_patterns(); xon = 'xon' in FLAGS
C = json.load(open(OPT['cert'])); SR = {(wd, tuple(map(str, b))): cf for wd, cf, b in R2_sender_rows()}
MDROP = []; base = collections.defaultdict(Fraction); tco = Fraction(0); BW = None
for c in C:
    w = Fraction(c['w']).limit_denominator(10 ** 7); row = c['row']
    if row[0] == 'senderR2':
        tco += w
        for k, v in SR[(row[1], tuple(map(str, row[2])))].items(): base[k] += w * v
    elif row[0] == 'cons2':
        for k, v in cons2_coef(tuple(row[1]), tuple(row[2])).items(): base[k] += w * v
    elif row[0] == 'mrowR2':
        if tuple(row[1])[0] == 7: MDROP.append(row); continue   # U = 7 signatures are the binder's only: in a cell its M is exact h, so these rows get weight 0
        base[('h', tuple(row[2]))] += w; base[('M', tuple(row[1]))] -= w
    elif row[0] == 'receiverR2':
        tco -= w; d, lk, sv = int(row[1]), row[2], row[3]
        if (d, lk, sv) == (7, '7665566', '6675676'): BW = w; continue
        for k, v in recv_coef_R2(d, lk, sv, xon).items(): base[k] += w * v
assert BW is not None and tco == 1
P('mrowR2 rows dropped (U = 7, binder-only signatures): %s' % [(r[1], r[2]) for r in MDROP])
d = 7; U = 7; wl, sl = OURS_W, OURS_S
row0 = recv_coef_R2(d, '7665566', '6675676', xon)
sixes = [j for j in range(7) if wl[j] == 6]
def amask_j(j): return amask(U, wl[(j - 2) % d], wl[(j - 1) % d], wl[(j + 1) % d], wl[(j + 2) % d], sl[(j - 2) % d], sl[(j - 1) % d], sl[j], sl[(j + 1) % d])
def msig(j): return sig2_of(U, wl[(j + 1) % d], sl[j], sl[(j - 1) % d], wl[(j - 1) % d], wl[(j + 2) % d], wl[(j - 2) % d]) + (amask_j(j),)
def hkey(j, p): return h2_of((U, wl[(j + 1) % d], sl[j], p, sl[(j - 1) % d], wl[(j - 1) % d]), wl[(j + 2) % d], wl[(j - 2) % d])
allowed = {j: [p for p in LET if (amask_j(j) >> (p - 5)) & 1 and not isR6((U, wl[(j + 1) % d], sl[j], p, sl[(j - 1) % d], wl[(j - 1) % d]))] for j in sixes}
P('binder 7665566/6675676 weight %s; amask-allowed privates %s' % (BW, {('p%d1' % j): allowed[j] for j in sixes}))
TS = ['tp51/s4', 'ts2/s3/s4', 'ts3', 'tp21/s3']   # placeholders, replaced below by the mirrored header t-slots
TS = sorted({x for _, cl in kills for x in cl if x.startswith('t')} | {tnorm(mirror_vertex(tnorm(s))) for s in G7SLOTS if s.startswith('t')})
P('ring-3 slots in our coordinates: %s' % TS)
def cell_dead(cell):
    """a private cell (dict) is dead iff EVERY completion of the ring-3 slots is matched by some g7 name"""
    live = []
    for nm, cl in kills:
        if all(cell.get(x, v) == v for x, v in cl.items() if not x.startswith('t')): live.append(cl)
    if not live: return False
    for tv in itertools.product(LET, repeat=len(TS)):
        tt = dict(zip(TS, tv))
        if not any(all((tt[x] if x.startswith('t') else cell[x]) == v for x, v in cl.items()) for cl in live): return False
    return True
PRIV = ['p01', 'p02'] + ['p%d1' % j for j in sixes]
def run(use_g7, region6=False, tag=''):
    cells = []
    for pv in itertools.product(LET, LET, *[allowed[j] for j in sixes]):
        cell = dict(zip(PRIV, pv))
        if region6 and min(pv) < 6: continue
        if use_g7 and cell_dead(cell): continue
        cells.append(cell)
    # distinct coefficient rows over the 6-spoke privates only (w0's privates enter no term)
    rowsC = {}
    for cell in cells:
        cf = collections.Counter(row0)
        for j in sixes: cf[('M', msig(j))] -= 1; cf[('h', hkey(j, cell['p%d1' % j]))] += 1
        rowsC.setdefault(tuple(cell['p%d1' % j] for j in sixes), {k: v for k, v in cf.items() if v})
    keys = sorted({k for cf in rowsC.values() for k in cf} | {k for k in base}, key=str)
    keys = [k for k in keys if k[0] not in ('x', 'D', 't')]
    kix = {k: i for i, k in enumerate(keys)}; cl = list(rowsC)
    A = np.zeros((len(keys), len(cl))); b0 = np.array([float(base[k]) for k in keys])
    for c_, kk in enumerate(cl):
        for k, v in rowsC[kk].items():
            if k in kix: A[kix[k], c_] += float(BW) * v
    # tot = b0 + A lam <= e, sum lam = 1, lam >= 0; minimise e
    nv = len(cl); cobj = np.zeros(nv + 1); cobj[-1] = 1
    res = linprog(cobj, A_ub=np.hstack([A, -np.ones((len(keys), 1))]), b_ub=-b0, A_eq=np.hstack([np.ones((1, nv)), np.zeros((1, 1))]),
                  b_eq=[1.0], bounds=[(0, None)] * nv + [(None, None)], method='highs')
    e = res.x[-1]; lam = res.x[:-1]; tv = b0 + A @ lam
    P('\n[%s] cells %d (6-spoke private combos %d); lifting worst tot = %.9f -> %s' % (tag, len(cells), len(cl), e,
      'FEASIBLE: cert_st24bL valid, null' if e <= 1e-10 else 'INFEASIBLE: no lifting keeps all rc >= 0'))
    if e > 1e-10:
        neg = np.argsort(-tv)[:8]
        for i in neg:
            if tv[i] > 1e-10: P('   rc %.6f  %s' % (-tv[i], keys[i]))
    else:
        for c_ in np.argsort(-lam)[:4]:
            if lam[c_] > 1e-9: P('   lifting cell (p11,p21,p51,p61) = %s  lam %.4f' % (cl[c_], lam[c_]))
    return e
e0 = run(False, tag='without g7 (filt16 amask only)')
e1 = run(True, tag='with g7 kills')
e2 = run(False, region6=True, tag="Explore's round-53 region: every private >= 6")
P('\nsummary: worst rc without g7 %.6f, with g7 %.6f, region>=6 %.6f (0 = null)' % (-e0 if e0 > 1e-10 else 0, -e1 if e1 > 1e-10 else 0, -e2 if e2 > 1e-10 else 0))
OUTF.close()
