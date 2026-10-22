# s54 fails.py SOL T [VIOL]: the sender rows (five link words, worst hat/fan context) that end above T under SOL's rule,
# with their excess (charge left - T), and a digest of the receiver rows in VIOL (an upperR2 vfile: d load excess link sv).
import sys, os, json, collections
for _v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'): os.environ[_v] = '1'
E = os.path.dirname(os.path.abspath(__file__)) + '/eng'
SOLF, T = sys.argv[1], float(sys.argv[2]); VIOL = sys.argv[3] if len(sys.argv) > 3 else None
sys.argv = [E + '/pcheck.py', 'none', 'xon', 'apexcls', 'hat5', 'l3q', 'l3qV=7,8', 'pm=',
            'root=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis',
            'work=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/s54w/fails']
_g = {'__file__': E + '/pcheck.py', '__name__': 'pc'}
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()): exec(open(E + '/pcheck.py').read(), _g)
S = json.load(open(SOLF)); root = _g['root']
Y = {}
for k, v in S['y'].items():
    u, rest = k.split('|'); Y[root(list((int(u),) + tuple(int(c) for c in rest)), 0)] = v
G = {tuple(k): v for k, v in S.get('g', [])}; R = {tuple(k): v for k, v in S.get('r', [])}
worst = {}
for wd, cf, bits in _g['R2_sender_rows']():
    v = sum(c * (Y.get(k[1], 0.0) if k[0] == 'y' else G.get(k[1], 0.0) if k[0] == 'g' else R.get(k[1], 0.0) if k[0] == 'r' else 0.0) for k, c in cf.items())
    left = 1 - v
    if wd not in worst or left > worst[wd][0]: worst[wd] = (left, bits)
bad = sorted(((l - T, wd, b) for wd, (l, b) in worst.items() if l > T + 1e-9), reverse=True)
print('senders: %d of %d five words end above t = %.6f' % (len(bad), len(worst), T))
for ex, wd, b in bad[:15]: print('  five link %s (hats|fans %s): ends at %.6f, excess %.6f' % (wd, ''.join(map(str, b)), T + ex, ex))
if VIOL and os.path.exists(VIOL):
    rows = [l.split() for l in open(VIOL) if l.strip()]
    byl = collections.defaultdict(list)
    for d, load, ex, lk, sv in rows: byl[(int(d), lk)].append((float(ex), sv))
    print('receivers: %d violated rows reported (vK per d), %d distinct (d, link)' % (len(rows), len(byl)))
    for (d, lk), l in sorted(byl.items(), key=lambda kv: -max(e for e, _ in kv[1]))[:15]:
        print('  d=%d link %s: excess %.6f (%d apex words, e.g. %s)' % (d, lk, max(e for e, _ in l), len(l), l[0][1]))
