"""Evaluate every sender row of Studio's wlp3x LP at a solution JSON (y, x, t, z9): row . v <= -1 (rows are A v <= b).
feascheck.py checks receivers (exhaustive) and the DP tail but not sender rows; this closes that gap.
Usage: WLP3X_DEF=1 WLP_SEPF=1 python3 sendercheck.py SOL.json <args>"""
import sys, os, json, collections
HERE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
SOL = json.load(open(sys.argv[1]))
src = open(os.path.join(HERE, 'wlp3x.py')).read().replace('os.path.abspath(__file__)', repr(os.path.join(HERE, 'wlp3x.py')), 1)
src = src[:src.index('# warm start: receiver rows')]
sys.argv = ['wlp3x'] + sys.argv[2:]
exec(src)
val = collections.defaultdict(float); val[('t',)] = SOL['t']
keys = collections.Counter(k[0] for k_, inf in enumerate(rinfo) if inf[0] == 'sender' for k in rows[k_])
print('sender-row key types:', dict(keys))
for k, v in SOL['y'].items():
    u, rest = k.split('|'); val[('y', ix[(int(u),) + tuple(int(c) for c in rest)])] = v
for k, v in SOL['x'].items(): val[('x', int(k))] = v
val[('z9',)] = SOL['z9']
n = bad = 0; worst = -1e9
for k_, inf in enumerate(rinfo):
    if inf[0] != 'sender': continue
    n += 1; s = sum(c * val[key] for key, c in rows[k_].items()); worst = max(worst, s)
    if s > -1 + 1e-7: bad += 1; print('VIOLATED sender', inf[1], s) if bad <= 20 else None
print('sender rows %d, violated %d, max lhs %.9f (must be <= -1)' % (n, bad, worst))
SEPX.stdin.close()
