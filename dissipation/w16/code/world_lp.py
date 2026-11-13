# W16: solve min t over a saved label set for the families base / rrz / all / allK; write duals of the positive ones.
# usage: python3 -I world_lp.py LABELS.pkl OUT.json [fams]
import sys, os, time, pickle, json, collections
sys.path.insert(0, '/tmp/swarm-W16/code')
import numpy as np
import w16lib as W
from lp_patterns import lab_str
T0 = time.time()
def log(*a): print(*a, '[%.0fs]' % (time.time() - T0), flush=True)
def lab_key(lab):
    if lab[0] in ('S', 'C', 'R'): return lab_str(lab)
    return str(lab)
def dual_support(rows, res, rmap, top=40):
    lam = -np.asarray(res.ineqlin.marginals) if res.ineqlin is not None else np.zeros(0)
    mu = np.asarray(res.eqlin.marginals) if res.eqlin is not None else np.zeros(0)
    sup = []
    for (lab, cf, kind, rhs), (typ, r) in zip(rows, rmap):
        v = lam[r] if typ == 'ub' else mu[r]
        if abs(v) > 1e-9 and lab[0] in ('S', 'R'): sup.append((float(v), lab_key(lab)))
    sup.sort(key=lambda x: -abs(x[0]))
    tot = sum(abs(v) for v, _ in sup)
    return dict(n=len(sup), total=tot, top=[(round(v / tot, 4), k) for v, k in sup[:top]])
if __name__ == '__main__':
    ARGV = list(sys.argv); W.init()
    labs = pickle.load(open(ARGV[1], 'rb')); fams = ARGV[3].split(',') if len(ARGV) > 3 else ['base', 'rrz', 'all', 'allK']
    log('labels %d: %s' % (len(labs), dict(collections.Counter(l[0] for l in labs))))
    out = {}
    for fam in fams:
        rows = W.build_lp(labs, fam); res, keys, rmap = W.solve_lp(rows)
        ent = dict(status=int(res.status), t=float(res.fun) if res.status == 0 else None, nrows=len(rows), nvars=len(keys))
        if res.status == 0: ent['dual'] = dual_support(rows, res, rmap)
        if res.status == 0 and fam in ('all', 'allK'):
            x = res.x; kk = {k: x[i + 1] for i, k in enumerate(keys) if abs(x[i + 1]) > 1e-9}
            ent['fam_mass'] = {f: round(sum(v for k, v in kk.items() if k[0] == f), 6) for f in sorted({k[0] for k in kk})}
        out[fam] = ent; log(fam, {k: v for k, v in ent.items() if k != 'dual'}, 'dual support', ent.get('dual', {}).get('n'))
        if ent.get('dual'): log('   top dual rows:', ent['dual']['top'][:12])
    json.dump(out, open(ARGV[2], 'w'), indent=1)
