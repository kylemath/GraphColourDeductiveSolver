# Team C trust-region LP at the in-point: the solveR2 nosep LP over the warm rows (engine builder, 'structonly'), every column boxed to
# [x_in - delta, x_in + delta] (intersected with its own bounds; t free). Row duals = which rows block local descent from the in-point.
# If every row left out of the warm set has slack >= s0 at x_in and every receiver row has ||coef||_1 <= c1, then delta <= s0 / (c1 + 1) makes the
# box LP over the warm rows equal to the box LP over all rows (d = 7..17; the Karp tail is far from tight). All t values [M].
# usage: python3 trC.py <solveR2 flags incl. warm= consbasis= K= xcap= work=> sol=INPOINT tag=T outdir=DIR deltas=1e-4,3e-4 [ntop=25] [s0=0.01]
import sys, os, json, collections, time
ENG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'eng', 'pcheck.py')
_argv = sys.argv[1:]
sys.argv = [ENG, 'help', 'structonly', 'nosep'] + _argv
ns = {'__file__': ENG, '__name__': 'pcheck_sC'}
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()): exec(compile(open(ENG).read(), ENG, 'exec'), ns)
OPT, FLAGS = ns['OPT'], ns['FLAGS']; log = ns['log']
import highspy, numpy as np
T0 = time.time()
h, cols, info, conset, RW, SR = ns['cmd_solveR2']()
h.setOptionValue('output_flag', False)
log('built: %d rows, %d cols, %.0fs' % (h.getNumRow(), h.getNumCol(), time.time() - T0))
OUT = OPT['outdir']; TAG = OPT['tag']; os.makedirs(OUT, exist_ok=True)
# ---- in-point values for every LP column
Sj = json.load(open(OPT['sol'])); tin = Sj['t']
Y = {}
for k, v in Sj['y'].items():
    u, rest = k.split('|'); Y[ns['root'](list((int(u),) + tuple(int(c) for c in rest)), 0)] = v
FAM = {f: {tuple(k): v for k, v in Sj.get(f, [])} for f in ('g', 'h', 'z', 'zr', 'r', 'rr', 'lq', 'lQ', 'q')}
X = {int(k): v for k, v in Sj.get('x', {}).items()}
ns['LQV'].clear(); ns['LQV'].update(FAM['lq']); ns['LQQ'].clear(); ns['LQQ'].update(FAM['lQ'])
def val(k):
    f = k[0]
    if f == 't': return tin
    if f == 'y': return Y.get(k[1], 0.0)
    if f == 'x': return X.get(k[1], 0.0)
    if f == 'M': return max([FAM['h'].get(tuple(kk), 0.0) for kk in ns['sig2_keys'](k[1])] or [0.0])
    if f == 'lQ': return ns['l3q_QeffV'](k[1][0], *k[1][1:]) if len(k[1]) == 4 else ns['l3q_Qeff'](*k[1])
    if f == 'Q': return max([FAM['q'].get(tuple(kk), 0.0) for kk in ns['q7keys'](k[1])] or [0.0])
    if f in FAM: return FAM[f].get(k[1], 0.0)
    raise KeyError(k)
n = h.getNumCol(); xin = np.zeros(n)
for k, i in cols.items(): xin[i] = val(k)
lp = h.getLp(); lo0 = np.array(lp.col_lower_); hi0 = np.array(lp.col_upper_); rlo = np.array(lp.row_lower_); rhi = np.array(lp.row_upper_)
A = lp.a_matrix_
import scipy.sparse as sp
_st = np.array(A.start_)
if len(_st) == h.getNumRow() + 1: M_ = sp.csr_matrix((np.array(A.value_), np.array(A.index_), _st), shape=(h.getNumRow(), n))
else: M_ = sp.csc_matrix((np.array(A.value_), np.array(A.index_), _st), shape=(h.getNumRow(), n)).tocsr()
act = M_ @ xin
viol = np.maximum(rlo - act, act - rhi); viol[~np.isfinite(viol)] = 0
cb = np.maximum(lo0 - xin, xin - hi0)
log('in-point in this LP: t_in %.12f; max row violation %.3g (row %s); max column-bound violation %.3g' % (tin, viol.max(), info[int(viol.argmax())], cb.max()))
rowslack = np.minimum(act - rlo, rhi - act)
_l1 = np.asarray(abs(M_).sum(axis=1)).ravel(); c1 = max(float(_l1[i]) for i, r in enumerate(info) if r[0] == 'receiverR2')
s0 = float(OPT.get('s0', '0.01'))
log('max ||coef||_1 over receiver rows (incl. t) %.1f -> exact-delta s0/c1 = %.3g' % (c1, s0 / c1))
jt = cols[('t',)]
canon_row = ns['_canon_row']
rec = [i for i, r in enumerate(info) if r[0] == 'receiverR2']
bylink = collections.defaultdict(list)
for i in rec: r = info[i]; bylink[(r[1], canon_row(r[1], r[2], '5' * r[1])[0])].append(i)
inf = highspy.kHighsInf
def solve():
    h.run(); st = h.getModelStatus()
    return (h.getSolution().col_value[jt] if st == highspy.HighsModelStatus.kOptimal else None), h.modelStatusToString(st)
summary = []
for dl in [float(x) for x in OPT.get('deltas', '1e-4').split(',')]:
    lo = np.maximum(lo0, xin - dl); hi = np.minimum(hi0, xin + dl); lo[jt] = -inf; hi[jt] = inf
    lo = np.minimum(lo, xin); hi = np.maximum(hi, xin)   # keep x_in inside the box even where it sits a hair outside its own bound
    h.changeColsBounds(n, np.arange(n, dtype=np.int32), lo, hi)
    t1 = time.time(); t, st = solve()
    sol = h.getSolution(); du = np.array(sol.row_dual); xv = np.array(sol.col_value)
    nbox = int(np.sum((np.abs(xv - lo) < 1e-12) & (lo > lo0 + 1e-15)) + np.sum((np.abs(xv - hi) < 1e-12) & (hi < hi0 - 1e-15)))
    log('delta %.3g: status %s t = %.12f (dt %.3e) %.0fs; columns at a box face %d [M]' % (dl, st, t, t - tin, time.time() - t1, nbox))
    cert = [{'w': float(dv), 'row': info[i], 'slack_in': float(rowslack[i])} for i, dv in enumerate(du) if abs(dv) > 1e-11]
    json.dump(cert, open(os.path.join(OUT, 'tr_%s_d%g.json' % (TAG, dl)), 'w'), indent=0)
    tot = collections.defaultdict(float)
    for c in cert: tot[c['row'][0]] += abs(c['w'])
    log('   row-dual mass by type: ' + ', '.join('%s %.4g (%d rows)' % (k, v, sum(1 for c in cert if c['row'][0] == k)) for k, v in sorted(tot.items(), key=lambda x: -x[1])))
    # drop tests on the heaviest receiver rows: (a) the row, (b) its whole link group
    R = sum(-du[i] for i in rec) or 1.0; res = []
    top = sorted(rec, key=lambda i: du[i])[:int(OPT.get('ntop', '25'))]
    for i in top:
        r = info[i]; d = r[1]
        if du[i] > -1e-11: break
        h.changeRowBounds(i, -inf, inf); ta, sa = solve(); h.changeRowBounds(i, -inf, d - 6.0)
        key = (d, canon_row(d, r[2], '5' * d)[0]); grp = bylink[key]
        for j in grp: h.changeRowBounds(j, -inf, inf)
        tb, sb = solve()
        for j in grp: h.changeRowBounds(j, -inf, info[j][1] - 6.0)
        res.append({'row': r, 'share': float(-du[i] / R), 'slack_in': float(rowslack[i]), 'dt_row': None if ta is None else ta - t, 'dt_link': None if tb is None else tb - t, 'link': key[1], 'link_rows': len(grp), 'link_share': float(sum(-du[j] for j in grp) / R)})
        log('   drop %s (share %.4f, slack_in %.2g): row -> dt %s; link %s (%d rows, share %.4f) -> dt %s' % ('/'.join(map(str, r[1:4])), res[-1]['share'], rowslack[i], 'n/a' if ta is None else '%.3e' % (ta - t), key[1], len(grp), res[-1]['link_share'], 'n/a' if tb is None else '%.3e' % (tb - t)))
    solve()
    summary.append({'delta': dl, 't': t, 'dt': t - tin, 'drops': res})
    if 'savex' in FLAGS:
        np.save(os.path.join(OUT, 'xtr_%s_d%g.npy' % (TAG, dl)), xv)
json.dump({'t_in': tin, 'c1': c1, 'runs': summary}, open(os.path.join(OUT, 'trsum_%s.json' % TAG), 'w'), indent=1)
log('done %.0fs' % (time.time() - T0))
