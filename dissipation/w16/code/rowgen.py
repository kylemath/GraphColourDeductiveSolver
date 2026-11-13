# W16: row generation for a big world LP: start from senders + cons2 + mrows + the pure 5/7 receivers, solve, add the receivers
# the solution violates (all mrows are always in), repeat; the final active set has the same optimum as the full world LP
# (its solution, extended by 0 on absent columns, satisfies every world row).  Saves {'rows': active rows, 't': ...} for cert.py.
# usage: python3 -I rowgen.py WORLD.pkl FAM OUT.pkl
import sys, os, pickle, json, time, collections
sys.path.insert(0, '/tmp/swarm-W16/code')
import numpy as np
from scipy.sparse import coo_matrix
import w16lib as W
from lp_patterns import lab_str
T0 = time.time()
def log(*a): print(*a, '[%.0fs]' % (time.time() - T0), flush=True)
if __name__ == '__main__':
    ARGV = list(sys.argv); W.init()
    OPUSF = os.environ.get('OPUSF') == '1'; OK = {}
    if OPUSF:   # lazy Opus (A97 stack) admissibility: only rows that enter the active set are checked; rejected rows stay out
        import opus_ns; ONS = opus_ns.load()
        def oadm(lab):
            if lab not in OK: OK[lab] = ONS['admissible'](lab[1], ''.join(map(str, lab[2])), ''.join(map(str, lab[3]))) is None
            return OK[lab]
    else: oadm = lambda lab: True
    labs = pickle.load(open(ARGV[1], 'rb')); fam = ARGV[2]; out = ARGV[3]
    rows = W.build_lp(labs, fam); log('built %d rows (%s)' % (len(rows), dict(collections.Counter(r[2] for r in rows))))
    DROP = set(x for x in os.environ.get('DROPLINK', '').split(',') if x)
    R = [i for i, r in enumerate(rows) if r[2] == 'le' and ''.join(map(str, r[0][2])) not in DROP]
    if DROP: log('DROPLINK %s: %d receivers left' % (sorted(DROP), len(R)))
    fixed = [i for i, r in enumerate(rows) if r[2] != 'le']
    keys = sorted({k for _, cf, _, _ in rows for k in cf}, key=str); idx = {k: i for i, k in enumerate(keys)}
    Ai, Aj, Av = [], [], []
    for j, i in enumerate(R):
        for k, v in rows[i][1].items(): Ai.append(j); Aj.append(idx[k]); Av.append(float(v))
    MR = coo_matrix((Av, (Ai, Aj)), shape=(len(R), len(keys))).tocsr(); rhs = np.array([rows[i][3] for i in R])
    active = {j for j, i in enumerate(R) if set(rows[i][0][2]) | set(rows[i][0][3]) <= {5, 7} and oadm(rows[i][0])}
    extra = os.environ.get('SEED')
    if extra: want = set(open(extra).read().split('\n')); active |= {j for j, i in enumerate(R) if lab_str(rows[i][0]) in want}
    log('receivers %d, initial active %d, fixed rows %d' % (len(R), len(active), len(fixed)))
    for it in range(int(os.environ.get('ITERS', '60'))):
        sub = [rows[i] for i in fixed] + [rows[R[j]] for j in sorted(active)]
        res, k2, rmap = W.solve_lp(sub)
        if res.status != 0: log('LP status', res.status, res.message); break
        t = res.x[0]; xv = np.zeros(len(keys))
        for jj, k in enumerate(k2): xv[idx[k]] = res.x[jj + 1]
        viol = MR @ xv - t - rhs
        order = np.argsort(-viol); new = []; nrej = 0
        for j in order:
            j = int(j)
            if viol[j] <= 1e-9 or len(new) >= int(os.environ.get('ADD', '400')): break
            if j in active: continue
            if oadm(rows[R[j]][0]): new.append(j)
            else: nrej += 1; viol[j] = -1; MR.data[MR.indptr[j]:MR.indptr[j + 1]] = 0.0; rhs[j] = 1e9   # never again
        log('iter %d: t = %.12f, active %d, violated %d (max %.3g), adding %d, Opus-rejected %d (total %d)' % (it, t, len(active), int((viol > 1e-9).sum()), viol.max(), len(new), nrej, sum(1 for v in OK.values() if not v)))
        if not new: break
        active |= set(new)
    sub = [rows[i] for i in fixed] + [rows[R[j]] for j in sorted(active)]
    pickle.dump(dict(rows=sub, t=float(t), fam=fam, world=ARGV[1], converged=not new, opus_rejected=[l for l, v in OK.items() if not v]), open(out, 'wb'))
    log('saved %d rows, t = %.12f, converged %s' % (len(sub), t, not new))
