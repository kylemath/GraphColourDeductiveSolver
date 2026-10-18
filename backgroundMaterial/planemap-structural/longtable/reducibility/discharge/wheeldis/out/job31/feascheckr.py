"""Relay-mode upper check for a wlp3r6 solution (Job 31): is (y, x, y56, y6b, z9, t) feasible for the whole 6-relay LP?
- receivers d = 7..DMAXP: exhaustive bin/sep3r (SEP_NODELIMIT=0), threshold d - 6 + t + EPS, with the six inflow at
  the current y6b maximum (as wlp3r6);
- six rows: six_sep over every non-R6 link word (max-plus over the 6-cycle, validated against brute force by RSELF);
- every sender row, including the y56 terms; z9 rows (x[tau] <= z9);
- d = DMAXP+1..30: the max-plus DP with z9 and the six inflow (dp9); and the Karp letter-9 cycle-mean tail.
Usage: WLP3X_DEF=1 WLP_SEPF=1 python3 out/job31/feascheckr.py SOL.json [eps=1e-7] <args as for wlp3r6>"""
import sys, os, json
HERE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
SOLF = sys.argv[1]; SOL = json.load(open(SOLF))
EPS = float(next((a[4:] for a in sys.argv[2:] if a.startswith('eps=')), '1e-7'))
ARGS = [a for a in sys.argv[2:] if not a.startswith('eps=')]
os.environ['SEP_NODELIMIT'] = '0'
src = open(os.path.join(HERE, 'wlp3r6.py')).read().replace('os.path.abspath(__file__)', repr(os.path.join(HERE, 'wlp3r6.py')), 1)
sys.argv = ['wlp3r6', 'tag=feasr'] + ARGS
exec(src[:src.index('DS, DSF = list(range(7, 13))')])
yv = np.zeros(NY)
for k, v in SOL['y'].items():
    u, rest = k.split('|'); yv[ix[(int(u),) + tuple(int(c) for c in rest)]] = v
xv = {int(k): v for k, v in SOL['x'].items()}; t = SOL['t']; z9 = SOL['z9']
V56[:] = 0.0; V6B[:] = 0.0
for k, v in SOL.get('y56', {}).items(): V56[I56[tuple(int(c) for c in k)]] = v
for k, v in SOL.get('y6b', {}).items(): V6B[I6B[tuple(int(c) for c in k)]] = v
print('solution t = %.9f: %d y, %d x, %d y56, %d y6b nonzero; z9 = %.4f' % (t, int((yv > 0).sum()), len(xv), int((V56 > 0).sum()), int((V6B > 0).sum()), z9), flush=True)
bad = 0
# bounds
lo = min([yv.min(), V56.min(), V6B.min()] + list(xv.values()) + [0.0]); hi = max([yv.max(), V56.max(), V6B.max(), 0.0])
xh = max(list(xv.values()) + [0.0])
if lo < -EPS or hi > 1 + EPS or xh > XCAP + EPS or z9 > XCAP + EPS: bad += 1; print('VIOLATED bounds: min %g, max y/y56/y6b %g, max x %g, z9 %g' % (lo, hi, xh, z9))
# senders and z9 rows
val = lambda key: (yv[key[1]] if key[0] == 'y' else xv.get(key[1], 0.0) if key[0] == 'x' else V56[key[1]] if key[0] == 'y56'
                   else V6B[key[1]] if key[0] == 'y6b' else z9 if key[0] == 'z9' else t)
ns = nz = 0
for k, inf in enumerate(rinfo):
    if inf[0] not in ('sender', 'z9'): continue
    s = sum(c * val(key) for key, c in rows[k].items())
    if inf[0] == 'sender': ns += 1
    else: nz += 1
    if s > rhs[k] + EPS: bad += 1; print('VIOLATED %s %s lhs %.9f > %.9f' % (inf[0], inf[1], s, rhs[k]))
print('sender rows %d, z9 rows %d checked' % (ns, nz), flush=True)
# six rows
v6 = six_sep(V56, t + EPS, 10 ** 6)
for v_, Lw, sv in v6[:20]: print('VIOLATED six link %s s %s: %.9f > t' % (''.join(map(str, Lw)), ''.join(map(str, sv)), v_))
bad += len(v6); print('six rows: %d link words, %d violated' % (len(W6), len(v6)), flush=True)
# receivers
for d in range(7, DMAXP + 1):
    out = sepx(d, yv, {} if NOTX else xv, d - 6 + t + EPS, 20)
    for o in out: print('VIOLATED d=%d load %.9f link %s s %s' % (d, o[0], o[1], o[2]))
    bad += len(out); print('d=%d: %d violated' % (d, len(out)), flush=True)
for d in range(DMAXP + 1, 31):
    out = dp9(d, yv, 0.0 if NOTX else z9, d - 6 + t + EPS, 5)
    for o in out: print('VIOLATED d=%d DP load %.9f' % (d, o[0]))
    bad += len(out)
print('DP d=%d..30 checked' % (DMAXP + 1), flush=True)
Mk = np.full((NS, NS), -np.inf)
for a, b, rr in TRI[9]:
    (wp, sp, wc), (_, sc, wn) = states[a], states[b]
    v_ = (yv[ix[rr]] if rr is not None else 0.0) + (0.0 if NOTX else z9) * BIGSTATE[a]
    if wc == 6: v_ += best6(9, wn, sc, sp, wp)[0]
    Mk[a, b] = max(Mk[a, b], v_)
n_ = NS; Dk = np.full((n_ + 1, n_), -np.inf); Dk[0, :] = 0.0
for k in range(1, n_ + 1): Dk[k] = (Dk[k - 1][:, None] + Mk).max(axis=0)
with np.errstate(invalid='ignore'):
    q = np.where(np.isfinite(Dk[n_]), np.min(np.where(np.isfinite(Dk[:n_]), (Dk[n_] - Dk[:n_]) / (n_ - np.arange(n_))[:, None], np.inf), axis=0), -np.inf)
lam = q.max(); dstar = (6 - t) / (1 - lam) if lam < 1 else float('inf')
print('Karp letter-9 tail: lambda = %.6f, d*lambda <= d-6+t for all d >= %.2f' % (lam, dstar))
if dstar > 31 + 1e-9: bad += 1; print('VIOLATED Karp tail does not cover d > 30')
SEPX.stdin.close(); SEPX.wait()
print('FEASIBLE' if bad == 0 else 'INFEASIBLE: %d violated' % bad)
