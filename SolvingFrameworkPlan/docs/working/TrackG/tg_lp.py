#!/usr/bin/env python3
"""Track G [exploratory]: LP feasibility of a linear stream function psi = theta . phi(s) with
psi(pi s) >= psi(s) + 1 on every DL->DL pi-step that is NOT on an all-DL pi-cycle.

usage: tg_lp.py PREFIX[,PREFIX...] [--test PREFIX,...] [--sets ring,comp,...] [--hom]
  per-hole / per-graph / pooled feasibility for each feature set; with --test, theta fitted on the training
  pool is evaluated on the test pool (fraction of non-cycle DL->DL steps with dpsi >= 1 and with dpsi > 0) and on the
  all-DL cycle steps. --hom adds the Z/2 homology bits of the four chain cycles (off-sphere data only).
"""
import sys, json, argparse, gzip, os
def _open(f):
    return open(f) if os.path.exists(f) else gzip.open(f + '.gz', 'rt')
import numpy as np, random, warnings
warnings.filterwarnings('ignore')
from scipy.optimize import linprog
import scipy.sparse as sp
from tg_engine import FEATS, FEATSETS

HOMF = ['C_MA', 'C_MB', 'C_AA', 'C_AB']


def load(prefixes, hom=False):
    rows = []   # (graph, hole, cyc, delta(all feats [+hom]))
    for p in prefixes:
        for l in _open(p + '.steps.jsonl'):
            d = json.loads(l)
            for s in d['steps']:
                dv = [b - a for a, b in zip(s['fs'], s['ft'])]
                if hom:
                    hs, ht = s['H'] if s['H'] else ({}, {})
                    dv += [(ht.get(k) or 0) - (hs.get(k) or 0) for k in HOMF]
                rows.append((d['graph'], d['h'], s['cyc'], dv))
    return rows


def cols(fs, hom):
    names = list(FEATS) + (HOMF if hom else [])
    return [names.index(f) for f in fs]


def fit(D):
    """min sum u s.t. D theta + u >= 1, u >= 0. Returns (opt, theta, satisfied fraction). D: unique rows."""
    if len(D) == 0: return 0.0, None, 1.0
    D = np.unique(np.asarray(D, float), axis=0)
    m, d = D.shape
    c = np.concatenate([np.zeros(d), np.ones(m)])
    A = -sp.hstack([sp.csr_matrix(D), sp.identity(m, format='csr')], format='csr'); b = -np.ones(m)
    bounds = [(-100, 100)] * d + [(0, None)] * m
    r = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')
    th = r.x[:d]; sat = float(np.mean(D @ th >= 1 - 1e-7))
    return r.fun, th, sat


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('train'); ap.add_argument('--test'); ap.add_argument('--sets', default='ring,lockpar,comp,global,chains,dist,local,all')
    ap.add_argument('--hom', action='store_true'); ap.add_argument('--perhole', action='store_true')
    ap.add_argument('--null', action='store_true', help='also run per-hole fits with each step reversed with prob 1/2')
    a = ap.parse_args()
    tr = load(a.train.split(','), a.hom); te = load(a.test.split(','), a.hom) if a.test else []
    sets = {k: FEATSETS[k] for k in a.sets.split(',')}
    if a.hom:
        sets = {k + '+hom': v + HOMF for k, v in sets.items()}; sets['hom'] = HOMF
    ntr = [r for r in tr if not r[2]]; cyc_tr = [r for r in tr if r[2]]
    print('train steps (non-cycle DL->DL): %d in %d holes, %d graphs; cycle steps %d' % (
        len(ntr), len({(r[0], r[1]) for r in ntr}), len({r[0] for r in ntr}), len(cyc_tr)))
    # single-feature monotonicity
    D = np.array([r[3] for r in ntr], float)
    names = list(FEATS) + (HOMF if a.hom else [])
    print('single-feature sign of delta on non-cycle DL->DL steps: name +/0/-')
    print('  ' + '  '.join('%s %d/%d/%d' % (n, (D[:, i] > 0).sum(), (D[:, i] == 0).sum(), (D[:, i] < 0).sum()) for i, n in enumerate(names)))
    res = {}
    for sname, fs in sets.items():
        ci = cols(fs, a.hom)
        out = {}
        if a.perhole:
            for key, kf in (('hole', lambda r: (r[0], r[1])), ('graph', lambda r: r[0])):
                grp = {}
                for r in ntr: grp.setdefault(kf(r), []).append([r[3][i] for i in ci])
                feas = sum(1 for g in grp.values() if fit(g)[0] < 1e-7)
                out[key] = '%d/%d' % (feas, len(grp))
                if a.null:
                    rng = random.Random(1)
                    feas0 = sum(1 for g in grp.values() if fit([[x * rng.choice((1, -1)) for x in row] for row in g])[0] < 1e-7)
                    out[key + '_null'] = '%d/%d' % (feas0, len(grp))
        opt, th, sat = fit([[r[3][i] for i in ci] for r in ntr])
        out['pooled_opt'] = round(opt, 4); out['pooled_sat_unique'] = round(sat, 4)
        if th is not None:
            Dtr = np.array([[r[3][i] for i in ci] for r in ntr], float); out['pooled_sat_all'] = round(float(np.mean(Dtr @ th >= 1 - 1e-7)), 4)
            out['theta'] = {f: round(float(t), 3) for f, t in zip(fs, th) if abs(t) > 1e-6}
            if te:
                nte = [r for r in te if not r[2]]; cte = [r for r in te if r[2]]
                Dte = np.array([[r[3][i] for i in ci] for r in nte], float); v = Dte @ th
                out['test_noncyc'] = dict(n=len(nte), ge1=round(float(np.mean(v >= 1 - 1e-7)), 4), gt0=round(float(np.mean(v > 1e-7)), 4))
                if cte:
                    Dc = np.array([[r[3][i] for i in ci] for r in cte], float); vc = Dc @ th
                    out['test_cycle_steps'] = dict(n=len(cte), ge1=round(float(np.mean(vc >= 1 - 1e-7)), 4), gt0=round(float(np.mean(vc > 1e-7)), 4))
        res[sname] = out
        print(sname, json.dumps(out), flush=True)
    return res


if __name__ == '__main__':
    main()
