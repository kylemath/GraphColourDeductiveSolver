# W16: per-pattern and joint LPs over admissible (kill-free, leak-free) periodic patterns; optional all-sender rows.
# usage: python3 -I joint.py OUT.json found1.pkl [found2.pkl ...]   env ALLSEND=1 adds every senderR2 row
import sys, os, pickle, json, time, itertools, collections
sys.path.insert(0, '/tmp/swarm-W16/code')
import numpy as np
import w16lib as W, torus as TT
from lp_patterns import lab_str, describe
from uniform import uniform
T0 = time.time()
def log(*a): print(*a, '[%.0fs]' % (time.time() - T0), flush=True)

def all_sender_labels():
    ns = W.NS; out = []; seen = set()
    for w in ns['SENDERS']:
        sixes = [k for k in range(5) if w[k] == 6]
        for hb in itertools.product((0, 1), repeat=5):
            for fb in itertools.product((0, 1), repeat=len(sixes)):
                F = [-1] * 5
                for k, b in zip(sixes, fb): F[k] = b
                lab = ('S', tuple(w), tuple(hb), tuple(F))
                cf = W.sender_coef(lab)
                if cf is None: continue
                key = tuple(sorted(cf.items()))
                if key in seen: continue
                seen.add(key); out.append(lab)
    return out

def pattern_ok(P):
    """kill-free and leak-free: every row admissible, no payee kill, uniform residual 0 for all families."""
    T = TT.Torus(P['n'], P['faces'])
    for v in range(T.n):
        lab = W.vertex_row(T, v)
        if W.row_status(lab) is not None: return False, 'row %s %s' % (lab_str(lab), W.row_status(lab))
        if T.deg[v] >= 7:
            w, s, r, ap = TT.words(T, v); k = W.payee_kills(T.deg[v], w, s, W.privates(T, v))
            if k: return False, 'kill %s %s' % (lab_str(lab), k)
    D, res = uniform(P['cnt'], 'all')
    # residual must be absorbable by mrows: every positive h / lq / q residual matched by a negative credit of a sig containing it
    return True, (D, len(res))

if __name__ == '__main__':
    ARGV = list(sys.argv); W.init()
    found = {}
    for f in ARGV[2:]: found.update(pickle.load(open(f, 'rb')))
    pats = []
    for key, P in found.items():
        ok, why = pattern_ok(P)
        if not ok: log('skip pattern n=%d %s: %s' % (P['n'], dict(P['degs']), why)); continue
        pats.append(P)
    log('%d admissible patterns of %d' % (len(pats), len(found)))
    out = dict(patterns=[], joint={})
    for P in sorted(pats, key=lambda P: (P['n'], str(describe(P['cnt'])))):
        ent = dict(n=P['n'], degs=describe(P['cnt']), tag=P['tag'], rows=[(lab_str(l), m) for l, m in sorted(P['cnt'].items(), key=str)], t={})
        for fam in ('base', 'rrz', 'all'):
            res, keys, rmap = W.solve_lp(W.build_lp(list(P['cnt']), fam))
            ent['t'][fam] = float(res.fun) if res.status == 0 else 'status%d' % res.status
        out['patterns'].append(ent); log(ent['n'], ent['degs'], ent['t'])
    U = sorted({l for P in pats for l in P['cnt']}, key=str)
    variants = [('joint', U)]
    if os.environ.get('ALLSEND'):
        S = all_sender_labels(); log('all sender rows: %d' % len(S)); variants.append(('joint+allsend', sorted(set(U) | set(S), key=str)))
    for name, labs in variants:
        out['joint'][name] = {}
        for fam in ('base', 'rrz', 'all'):
            rows = W.build_lp(labs, fam); res, keys, rmap = W.solve_lp(rows)
            out['joint'][name][fam] = dict(t=float(res.fun) if res.status == 0 else None, status=res.status, nrows=len(rows), nvars=len(keys))
            log(name, fam, out['joint'][name][fam])
    json.dump(out, open(ARGV[1], 'w'), indent=1)
