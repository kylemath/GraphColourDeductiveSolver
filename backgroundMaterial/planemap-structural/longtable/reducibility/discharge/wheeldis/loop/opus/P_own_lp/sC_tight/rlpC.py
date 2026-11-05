# Team C restricted LP with drop-one ranking. Builds exactly the solveR2 nosep LP (engine's own builder via 'structonly'), solves it,
# writes sol-free cert JSON (solveR2 format) for lowerR2, then for the top receiver classes by |dual| re-solves with (a) that row dropped,
# (b) every LP row with the same canonical link dropped. All t values are [M] pointers (restricted LP), never bounds.
# usage: python3 rlpC.py <solveR2 flags incl. warm= consbasis= K= xcap= work=> tag=T outdir=DIR [ntop=20] [nodrop]
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
log('built: %d rows (info %d), %d cols, %.0fs' % (h.getNumRow(), len(info), h.getNumCol(), time.time() - T0))
assert h.getNumRow() == len(info)
OUT = OPT['outdir']; TAG = OPT['tag']; os.makedirs(OUT, exist_ok=True)
jt = cols[('t',)]
def solve():
    h.run(); st = h.getModelStatus()
    return (h.getSolution().col_value[jt] if st == highspy.HighsModelStatus.kOptimal else None), h.modelStatusToString(st)
t1 = time.time(); t, st = solve()
log('restricted nosep LP: status %s t = %s  (%.0fs)  [M pointer]' % (st, t, time.time() - t1))
sol = h.getSolution(); du = np.array(sol.row_dual); xv = np.array(sol.col_value)
cert = [{'w': float(dv), 'row': info[i]} for i, dv in enumerate(du) if abs(dv) > 1e-11]
json.dump(cert, open(os.path.join(OUT, 'cert_%s.json' % TAG), 'w'), indent=0)
# compact solution summary (family totals)
fam = collections.defaultdict(float); famn = collections.Counter()
for k, i in cols.items():
    if xv[i] > 1e-12: fam[k[0]] += xv[i]; famn[k[0]] += 1
log('positive columns by family: ' + ', '.join('%s %d (sum %.4f)' % (f, famn[f], fam[f]) for f in sorted(fam)))
json.dump({'t': t, 'fam': {f: [famn[f], fam[f]] for f in fam}, 'nrows': h.getNumRow()}, open(os.path.join(OUT, 'lp_%s.json' % TAG), 'w'))
log('cert rows %d -> %s' % (len(cert), os.path.join(OUT, 'cert_%s.json' % TAG)))
if 'nodrop' in FLAGS: sys.exit(0)
canon_row = ns['_canon_row']
def clink(lk):
    d = len(lk); return min(canon_row(d, lk, '5' * d)[0] for _ in [0])
rec = [(i, r) for i, r in enumerate(info) if r[0] == 'receiverR2']
R = sum(-du[i] for i, r in rec) or 1.0
bylink = collections.defaultdict(list)
for i, r in rec: bylink[(r[1], ns['_canon_row'](r[1], r[2], '5' * r[1])[0])].append(i)
top = sorted(rec, key=lambda x: du[x[0]])[:int(OPT.get('ntop', '20'))]
inf = highspy.kHighsInf
res = []
for i, r in top:
    d = r[1]; share = -du[i] / R
    h.changeRowBounds(i, -inf, inf); ta, sa = solve(); h.changeRowBounds(i, -inf, d - 6.0)
    key = (d, ns['_canon_row'](d, r[2], '5' * d)[0]); grp = bylink[key]
    for j in grp: h.changeRowBounds(j, -inf, inf)
    tb, sb = solve()
    for j in grp: h.changeRowBounds(j, -inf, info[j][1] - 6.0)
    res.append({'row': r, 'share': share, 'dual': float(du[i]), 't_drop_row': ta, 't_drop_link': tb, 'link_rows': len(grp), 'link_share': float(sum(-du[j] for j in grp) / R)})
    log('drop %s: share %.4f; drop row -> t %s (%s, dt %s); drop link %s (%d LP rows, share %.4f) -> t %s (%s)' % ('/'.join(map(str, r[1:4])), share, ta, sa, None if ta is None else '%.6f' % (ta - t), key[1], len(grp), res[-1]['link_share'], tb, sb))
solve()
json.dump({'t': t, 'drops': res}, open(os.path.join(OUT, 'drops_%s.json' % TAG), 'w'), indent=1)
log('done %.0fs' % (time.time() - T0))
