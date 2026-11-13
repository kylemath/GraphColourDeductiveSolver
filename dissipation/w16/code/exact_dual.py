# W16: exact vertex dual of an LP over a row set (rowgen pickle): take HiGHS's dual support, require every column whose float
# combined coefficient is ~0 to be exactly 0 (plus the t normalisation), solve that sparse rational system exactly (Fractions,
# free unknowns fixed at their rounded float values), check signs, compute the exact bound and export as cert.py does.
# usage: python3 -I exact_dual.py ROWS.pkl FAM OUTPREFIX
import sys, os, pickle, json, collections, time
sys.path.insert(0, '/tmp/swarm-W16/code')
from fractions import Fraction as Fr
import numpy as np
import w16lib as W
from lp_patterns import lab_str
import cert as CE
T0 = time.time()
def log(*a): print(*a, '[%.0fs]' % (time.time() - T0), flush=True)
SG = {'ge': 1, 'eq': 1, 'le': -1, 'mrow': -1}
def solve_exact(eqs, guess):
    """eqs: list of ({var: Fr}, Fr rhs). Gaussian elimination; free vars := guess. Returns {var: Fr} or None (inconsistent)."""
    piv = {}   # var -> (dict without var, rhs): var = rhs - sum(c * v)
    order = []
    for cf, r in eqs:
        cf = dict(cf); r = Fr(r)
        changed = True
        while changed:   # substitute existing pivots
            changed = False
            for v in [v for v in cf if v in piv]:
                c = cf.pop(v); pc, pr = piv[v]; r -= c * pr
                for u, a in pc.items():
                    nv = cf.get(u, 0) - c * a
                    if nv: cf[u] = nv
                    else: cf.pop(u, None)
                changed = True
        if not cf:
            if r != 0: return None, 'inconsistent (residual %s)' % float(r)
            continue
        v = min(cf, key=lambda u: (abs(float(guess.get(u, 0))) < 1e-15, -abs(float(cf[u]))))   # pivot on a variable with a nonzero float value
        c = cf.pop(v); pc = {u: a / c for u, a in cf.items()}; pr = r / c
        for w_, (qc, qr) in list(piv.items()):   # keep pivots fully reduced (back-substitution as we go)
            if v in qc:
                a = qc.pop(v); qr2 = qr - a * pr
                for u, b in pc.items():
                    nv = qc.get(u, 0) - a * b
                    if nv: qc[u] = nv
                    else: qc.pop(u, None)
                piv[w_] = (qc, qr2)
        piv[v] = (pc, pr); order.append(v)
    free = {}
    sol = {}
    for v, (pc, pr) in piv.items():
        val = pr
        for u, a in pc.items():
            if u not in free: free[u] = Fr(float(guess.get(u, 0))).limit_denominator(10 ** 9)
            val -= a * free[u]
        sol[v] = val
    sol.update(free)
    return sol, 'ok: %d pivots, %d free' % (len(piv), len(free))
if __name__ == '__main__':
    ARGV = list(sys.argv); W.init()
    obj = pickle.load(open(ARGV[1], 'rb')); fam = ARGV[2]; pre = ARGV[3]
    rows = obj['rows'] if isinstance(obj, dict) else W.build_lp(obj, fam)
    res, keys, rmap = W.solve_lp(rows); log('LP t = %.12f (%s)' % (res.fun, res.status))
    mf = CE.lp_mults(rows, res, rmap)
    supp = [i for i, m in enumerate(mf) if abs(m) > 1e-12]
    G = collections.defaultdict(float)
    for i in supp:
        lab, cf, kind, b = rows[i]
        for k, v in cf.items(): G[k] += SG[kind] * mf[i] * float(v)
    tol = float(os.environ.get('ZTOL', '1e-9'))
    zero = [k for k, g in G.items() if abs(g) <= tol]
    log('support rows %d (%s); columns %d, of which ~0: %d; uncapped with G > tol: %d' % (len(supp), dict(collections.Counter(rows[i][2] for i in supp)), len(G), len(zero),
        sum(1 for k, g in G.items() if g > tol and W.CAP.get(k[0]) is None)))
    for rnd in range(10):
        colrows = collections.defaultdict(dict)
        for i in supp:
            lab, cf, kind, b = rows[i]
            for k, v in cf.items():
                if v: colrows[k][i] = Fr(v).limit_denominator(10 ** 6) * SG[kind] if not isinstance(v, (int, Fr)) else Fr(v) * SG[kind]
        eqs = [(colrows[k], Fr(0)) for k in zero]
        eqs.append(({i: Fr(1) for i in supp if rows[i][2] in ('ge', 'le')}, Fr(1)))
        sol, msg = solve_exact(eqs, {i: mf[i] for i in supp}); log('round %d: exact solve %s' % (rnd, msg))
        if sol is None: break
        bad = [i for i in supp if rows[i][2] != 'eq' and sol.get(i, 0) < 0]
        if not bad: break
        log('   %d multipliers of the wrong sign (largest %.3g): dropping them and re-solving' % (len(bad), max(-float(sol[i]) for i in bad)))
        supp = [i for i in supp if i not in set(bad)]
    mult = [Fr(0)] * len(rows)
    for i in supp: mult[i] = sol.get(i, Fr(0))
    D, viol, Gx, tco = CE.exact_bound(rows, mult, W.CAP)
    log('exact: D = %s = %.12f, tco = %s, uncapped positive columns %d %s' % (D, float(D), tco, len(viol), list(viol.items())[:3]))
    cert = [dict(w=('%s' % (m if kind in ('ge', 'eq') else -m)), row=CE.to_label(lab, cf, kind)) for m, (lab, cf, kind, b) in zip(mult, rows) if m != 0]
    json.dump(cert, open(pre + '_cert.json', 'w'), indent=0)
    sup = sorted(((float(m), lab_str(lab) if lab[0] in 'SRC' else str(lab)) for m, (lab, cf, kind, b) in zip(mult, rows) if m != 0 and kind in ('ge', 'le')), key=lambda x: -x[0])
    json.dump(dict(fam=fam, D=str(D), Dfloat=float(D), uncapped_negative=len(viol), rows=len(cert), support=sup), open(pre + '_summary.json', 'w'), indent=1)
    log('VERDICT: %s t >= %s (%.12f), %d certificate rows, uncapped positive G %d' % ('VALID' if not viol else 'NOT ESTABLISHED', D, float(D), len(cert), len(viol)))
