# s54 round_sol.py SOL OUT q=Q t=T [scale=S]: round every theta of a parametric sol to a multiple of 1/Q (Q=0: keep), set t,
# re-evaluate the modelled families on their whole universes (engine pmodel), and write a sol for upperR2.
# Free (non-modelled) families are copied unchanged.  Negative evaluated values are reported (upperR2 would refuse them).
import sys, os, json
for _v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'): os.environ[_v] = '1'
from fractions import Fraction
E = os.path.dirname(os.path.abspath(__file__)) + '/eng'
SOLF, OUTF = sys.argv[1], sys.argv[2]; A = dict(a.split('=', 1) for a in sys.argv[3:])
S = json.load(open(SOLF)); PMs = S['pm']
pm = ','.join('%s:%s' % kv for kv in PMs.items())
sys.argv = [E + '/pcheck.py', 'none', 'xon', 'apexcls', 'hat5', 'l3q', 'l3qV=7,8', 'pm=' + pm,
            'root=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis',
            'work=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/s54w/round']
_g = {'__file__': E + '/pcheck.py', '__name__': 'pc'}
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()): exec(open(E + '/pcheck.py').read(), _g)
if 'trees' in S and S['trees']:
    _g['TREES'].update(S['trees']); _g['_phic'].clear()
q = int(A.get('q', '0'))
TH = {}
for fam, f, v in S['theta']:
    if q: v = round(v * q) / q
    if abs(v) > 0: TH[(fam, eval(f))] = v
S2 = dict(S); S2['t'] = float(A['t']) if 't' in A else S['t']; S2['rounded_q'] = q
worst = {}
for fam in PMs:
    V = _g['pm_values'](fam, TH); worst[fam] = min(list(V.values()) + [0.0])
    if fam == 'y': S2['y'] = {_g['rname'](k): float(v) for k, v in V.items() if v > 1e-15}
    elif fam == 'x': S2['x'] = {str(k): float(v) for k, v in V.items() if v > 1e-15}
    else: S2[fam] = [[list(k), float(v)] for k, v in V.items() if v > 1e-15}
S2['theta'] = [[fam, repr(f), v] for (fam, f), v in sorted(TH.items(), key=str)]
json.dump(S2, open(OUTF, 'w'))
print('wrote %s: t = %.12f, q = %d, %d nonzero thetas, most negative value per family %s' % (OUTF, S2['t'], q, len(TH), worst))
