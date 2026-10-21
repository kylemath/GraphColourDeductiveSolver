# s54 fit_ls.py: step 1, least-squares fits of each family of sol_q53A97.json by the generic models of feats.py,
# over the family's whole key universe (absent key = weight 0).  Writes fits_ls.txt and, with out=, a sol JSON in which
# the chosen families are replaced by their (clipped >= 0) fitted values, for an upperR2 regress-and-round check.
# run: cd s54/eng && python3 ../fit_ls.py SOL [fam:model,...] [out=FILE]   (exec's the engine for keys / universes)
import sys, os, json
for _v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'): os.environ[_v] = '1'
E = os.path.dirname(os.path.abspath(__file__)) + '/eng'
SOLF = sys.argv[1]; REPL = sys.argv[2] if len(sys.argv) > 2 and '=' not in sys.argv[2] else ''
OUT = [a.split('=', 1)[1] for a in sys.argv[2:] if a.startswith('out=')]
sys.argv = [E + '/pcheck.py', 'none', 'xon', 'apexcls', 'hat5', 'l3q', 'l3qV=7,8', 'pm=', 'root=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis', 'work=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/s54w/fit']
_g = {'__file__': E + '/pcheck.py', '__name__': 'pc'}
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()): exec(open(E + '/pcheck.py').read(), _g)
np = _g['np']; pm_universe = _g['pm_universe']; model = _g['_fg']['model']; FEATS = _g['_fg']['FEATS']; rname = _g['rname']
S = json.load(open(SOLF))
def solvals(fam):
    if fam == 'y':
        V = {}
        for k, v in S['y'].items():
            u, rest = k.split('|'); V[_g['root'](list((int(u),) + tuple(int(c) for c in rest)), 0)] = v
        return V
    if fam == 'x': return {int(k): v for k, v in S['x'].items()}
    return {tuple(k): v for k, v in S[fam]}
def fit(fam, name):
    U = pm_universe(fam); V = solvals(fam); f = model(fam, name)
    ph = [f(k) for k in U]; F = sorted({q for p in ph for q in p}, key=str); ix = {q: i for i, q in enumerate(F)}
    A = np.zeros((len(U), len(F)))
    for r, p in enumerate(ph):
        for q, c in p.items(): A[r, ix[q]] = c
    b = np.array([V.get(k, 0.0) for k in U])
    if F: th, *_ = np.linalg.lstsq(A, b, rcond=None); pred = A @ th; rk = np.linalg.matrix_rank(A)
    else: pred = np.zeros(len(U)); rk = 0; th = []
    # error on the keys the LP actually uses (positive) and overall
    pos = b > 0
    ss = ((b - b.mean()) ** 2).sum()
    return dict(fam=fam, model=name, n=len(U), npos=int(pos.sum()), rank=int(rk), r2=1 - ((b - pred) ** 2).sum() / ss if ss else 0,
                rmse=float(np.sqrt(((b - pred) ** 2).mean())), maxerr=float(np.abs(b - pred).max()), nneg=int((pred < -1e-12).sum())), dict(zip(U, pred))
lines = ['family model universe positive rank R2 rmse maxerr npred<0']
FITS = {}
for fam in ('y', 'g', 'h', 'x', 'r', 'lq'):
    for name in FEATS[fam]:
        if name in ('zero', 'full'): continue
        st, pr = fit(fam, name); FITS[(fam, name)] = pr
        lines.append('%s %s %d %d %d %.4f %.4f %.4f %d' % (fam, name, st['n'], st['npos'], st['rank'], st['r2'], st['rmse'], st['maxerr'], st['nneg']))
        print(lines[-1], flush=True)
open(os.path.join(os.path.dirname(E), 'fits_ls.txt'), 'w').write('\n'.join(lines) + '\n')
if OUT and REPL:
    S2 = dict(S)
    for it in REPL.split(','):
        fam, name = it.split(':'); pr = FITS[(fam, name)]
        if fam == 'y': S2['y'] = {rname(k): float(v) for k, v in pr.items() if v > 0}
        elif fam == 'x': S2['x'] = {str(k): float(min(v, 3.0)) for k, v in pr.items() if v > 0}
        else: S2[fam] = [[list(k), float(v)] for k, v in pr.items() if v > 0]
    S2['ls_replaced'] = REPL; json.dump(S2, open(OUT[0], 'w')); print('wrote', OUT[0])
