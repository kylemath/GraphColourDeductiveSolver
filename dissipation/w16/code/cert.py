# W16: exact lower certificate from the LP dual of a label set (my row algebra on st21_w10 rows), Fractions; exports the
# certificate in the st21 / pcheck label format (string weights).  usage: python3 -I cert.py LABELS.pkl FAM OUTPREFIX [den]
import sys, os, pickle, json, collections, time
sys.path.insert(0, '/tmp/swarm-W16/code')
from fractions import Fraction as Fr
import numpy as np
import w16lib as W
from lp_patterns import lab_str
T0 = time.time()
def log(*a): print(*a, '[%.0fs]' % (time.time() - T0), flush=True)

def exact_bound(rows, mult, caps):
    """mult[i] = Fraction multiplier (>= 0 for ge/le/mrow, free for eq). Returns (D, violations, G)."""
    G = collections.defaultdict(Fr); tco = Fr(0); rhs = Fr(0)
    for (lab, cf, kind, b), m in zip(rows, mult):
        if m == 0: continue
        if kind == 'ge':
            tco += m; rhs += m
            for k, v in cf.items(): G[k] += m * v
        elif kind == 'le':
            tco += m; rhs -= m * Fr(lab[1] - 6)
            for k, v in cf.items(): G[k] -= m * v
        elif kind == 'eq':
            for k, v in cf.items(): G[k] += m * v
        else:   # mrow: m * (M - h) >= 0
            for k, v in cf.items(): G[k] -= m * v
    viol = {k: g for k, g in G.items() if g > 0 and caps.get(k[0]) is None}   # an uncapped column with positive combined coefficient
    D = rhs - sum(Fr(caps[k[0]]).limit_denominator(1000) * g for k, g in G.items() if g > 0 and caps.get(k[0]) is not None)
    return D / tco if tco else None, viol, G, tco

def lp_mults(rows, res, rmap):
    lam = -np.asarray(res.ineqlin.marginals); mu = np.asarray(res.eqlin.marginals) if res.eqlin is not None else np.zeros(0)
    out = []
    for (lab, cf, kind, b), (typ, r) in zip(rows, rmap): out.append(lam[r] if typ == 'ub' else mu[r])
    return out

def to_label(lab, cf, kind):
    if kind in ('ge', 'le', 'eq'): return W.label_json(lab)
    if lab[0] == 'mrowR2': return ['mrowR2', list(lab[1]), list(lab[2])]
    if lab[0] == 'mrowL': return ['mrowL', list(lab[1]), list(lab[2])]
    if lab[0] == 'mrowQ':
        sg = list(lab[1])
        if os.environ.get('OPUSQ') == '1' and sg[5] == 31 and sg[6] == 31: sg = sg[:5]   # Opus q7sig: unmasked = the 5-tuple
        return ['mrowQ', sg, list(lab[2])]
    raise ValueError(lab)

if __name__ == '__main__':
    ARGV = list(sys.argv); W.init()
    labs = pickle.load(open(ARGV[1], 'rb')); fam = ARGV[2]; pre = ARGV[3]; den = int(ARGV[4]) if len(ARGV) > 4 else 10 ** 6
    rows = labs['rows'] if isinstance(labs, dict) else W.build_lp(labs, fam); res, keys, rmap = W.solve_lp(rows); log('LP t = %.12f (%s)' % (res.fun, res.status))
    mf = lp_mults(rows, res, rmap)
    best = None
    for sgn in (1, -1):
        mult = [Fr(float(m)).limit_denominator(den) * (sgn if kind == 'eq' else 1) if abs(m) > 1e-12 else Fr(0) for m, (lab, cf, kind, b) in zip(mf, rows)]
        mult = [max(m, Fr(0)) if kind != 'eq' else m for m, (lab, cf, kind, b) in zip(mult, rows)]
        D, viol, G, tco = exact_bound(rows, mult, W.CAP)
        log('eq sign %+d: D = %s = %.12f, uncapped negative columns %d %s' % (sgn, D, float(D), len(viol), list(viol.items())[:4]))
        if best is None or len(viol) < len(best[1]): best = (D, viol, mult)
    D, viol, mult = best
    cert = [dict(w=('%s' % (m if kind in ('ge', 'eq') else -m)), row=to_label(lab, cf, kind)) for m, (lab, cf, kind, b) in zip(mult, rows) if m != 0]
    json.dump(cert, open(pre + '_cert.json', 'w'), indent=0)
    supp = sorted(((float(m), lab_str(lab) if lab[0] in 'SRC' else str(lab)) for m, (lab, cf, kind, b) in zip(mult, rows) if m != 0 and kind in ('ge', 'le')), key=lambda x: -x[0])
    json.dump(dict(fam=fam, D=str(D), Dfloat=float(D), uncapped_negative=len(viol), rows=len(cert), support=supp), open(pre + '_summary.json', 'w'), indent=1)
    log('VERDICT: %s t >= %s (%.12f), %d certificate rows, uncapped negative rc %d' % ('VALID' if not viol else 'NOT ESTABLISHED', D, float(D), len(cert), len(viol)))
