"""B8 (exploratory): empirical discharging LP over R-free local types.

Charges ch(x) = 6 - deg x (sum 12).  Every degree-5 vertex v sends to every vertex u of degree >= 7 within distance 2
an amount sigma[f] that depends on a feature f of the pair (v, u):
  model 'simple': f = (dist, min(deg u, 10))
  model 'face'  : dist 1: f = (1, Dcap, sorted caps of the two face apices of vu);  dist 2: f = (2, Dcap, #common nbrs)
  (caps at 8 for apices).
  model 'd3'    : f = (dist, min(deg u, 10)) for dist <= 3 (added 14 Oct, resumed run: does a larger radius help?)
Constraints, sampled from graphs (one row per distinct local type):
  sender  : every degree-5 v whose 2-ball is NOT in R:          1 - sum_f sigma[f] * n_f(v)  <= t
  receiver: every u of degree >= 7 all of whose degree-5 vertices within distance 2 are not in R:
                                                                 (6 - deg u) + sum_f sigma[f] * n_f(u) <= t
Minimise t over sigma >= 0 (sigma <= 1).  t <= 0 (strictly < 0 is not needed) means rules exist that leave every
observed R-free local type with charge <= 0; on a graph with no R anywhere this contradicts sum = 12.  t > 0: the dual
weights on rows are the infeasibility certificate (which local types keep positive charge).
Usage: lp.py MODEL FAMILIES OUTPREFIX GRAPHFILE... (census 'name n rot' lines; .gz ok)  [--sample K: every K-th graph]"""
import sys, os, gzip, collections, json
import numpy as np
from scipy.optimize import linprog
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ball, h0, construct


def features(rot, model):
    n = len(rot); deg = [len(r) for r in rot]; adj = [set(r) for r in rot]
    send = {}; recv = collections.defaultdict(collections.Counter)
    for v in range(n):
        if deg[v] != 5: continue
        c = collections.Counter(); N1 = adj[v]
        N2 = set(z for x in N1 for z in adj[x]) - N1 - {v}
        N3 = (set(z for x in N2 for z in adj[x]) - N2 - N1 - {v}) if model == 'd3' else set()
        for u in N1 | N2 | N3:
            if deg[u] < 7: continue
            D = min(deg[u], 10)
            if model == 'simple': f = (1 if u in N1 else 2, D)
            elif model == 'd3': f = (1 if u in N1 else 2 if u in N2 else 3, D)
            elif u in N1:
                R = rot[v]; i = R.index(u); p, q = deg[R[(i + 1) % 5]], deg[R[(i - 1) % 5]]
                f = (1, D, min(p, 8), min(q, 8)) if p <= q else (1, D, min(q, 8), min(p, 8))
            else: f = (2, D, len(adj[v] & adj[u]))
            c[f] += 1; recv[u][f] += 1
        send[v] = c
    return deg, send, recv


def near5(rot, u, r=2):
    seen = {u}; fr = {u}
    for _ in range(r):
        fr = set(z for x in fr for z in rot[x]) - seen; seen |= fr
    return [v for v in seen - {u} if len(rot[v]) == 5]


if __name__ == '__main__':
    model, fams, outp = sys.argv[1], set(sys.argv[2].split(',')), sys.argv[3]
    args = sys.argv[4:]; K = 1
    if '--sample' in args: i = args.index('--sample'); K = int(args[i + 1]); args = args[:i] + args[i + 2:]
    red = h0.make_pred(fams)
    rows = collections.Counter(); example = {}; ng = 0; rfree_graphs = 0
    for fn in args:
        op = gzip.open if fn.endswith('.gz') else open
        for li, line in enumerate(op(fn, 'rt')):
            if li % K: continue
            name, rot = ball.parse_line(line); ng += 1
            dia = construct.has_diamond_or_2122(rot)
            isR = {}
            for v in range(len(rot)):
                if len(rot[v]) == 5:
                    w, key, st = ball.ball_at(rot, v)
                    isR[v] = dia or bool(red(''.join(map(str, ball.wheel_canon(w))), ball.key_str(key) if key else None))
            if not any(isR.values()): rfree_graphs += 1
            deg, send, recv = features(rot, model)
            for v, c in send.items():
                if isR[v]: continue
                w = ''.join(map(str, ball.wheel_canon([deg[x] for x in rot[v]])))
                r = ('S', 1, tuple(sorted(c.items())))
                rows[r] += 1; example.setdefault(r, '%s:%d word %s' % (name, v, w))
            for u, c in recv.items():
                if any(isR[v] for v in near5(rot, u, 3 if model == 'd3' else 2)): continue
                r = ('R', 6 - deg[u], tuple(sorted(c.items())))
                rows[r] += 1; example.setdefault(r, '%s:%d deg %d' % (name, u, deg[u]))
    F = sorted({f for r in rows for f, _ in r[2]})
    FI = {f: i for i, f in enumerate(F)}; nv = len(F) + 1        # last = t
    A = []; b = []; R = list(rows)
    for r in R:
        a = np.zeros(nv); a[-1] = -1
        sign = -1 if r[0] == 'S' else 1
        for f, m in r[2]: a[FI[f]] = sign * m
        A.append(a); b.append(-r[1])        # sign*sum - t <= -const   (S: 1 - sum <= t ; R: c + sum <= t)
    c = np.zeros(nv); c[-1] = 1
    bounds = [(0, 1)] * len(F) + [(None, None)]
    res = linprog(c, A_ub=np.array(A), b_ub=np.array(b), bounds=bounds, method='highs')
    t = res.x[-1]; y = -res.ineqlin.marginals
    out = {'model': model, 'families': sorted(fams), 'graphs': ng, 'R_free_graphs': rfree_graphs,
           'rows': len(R), 'features': len(F), 't': t,
           'sigma': {str(f): round(res.x[i], 6) for i, f in enumerate(F) if res.x[i] > 1e-9}}
    cert = sorted(((y[i], R[i]) for i in range(len(R)) if y[i] > 1e-9), key=lambda z: -z[0])
    out['certificate'] = [{'weight': round(w, 6), 'kind': 'sender-5' if r[0] == 'S' else 'receiver deg %d' % (6 - r[1]),
                           'features': [[list(f), m] for f, m in r[2]], 'count': rows[r], 'example': example[r]}
                          for w, r in cert]
    json.dump(out, open(outp + '.json', 'w'), indent=1)
    print('model', model, 'graphs', ng, 'R-free graphs', rfree_graphs, 'rows', len(R), 'features', len(F), 't = %.6f' % t)
    print('certificate rows (dual > 0):', len(cert))
    for w, r in cert[:25]:
        print('  %.4f  %-14s %s  n=%d  e.g. %s' % (w, 'sender-5' if r[0] == 'S' else 'recv deg %d' % (6 - r[1]),
                                                  list(r[2]), rows[r], example[r]))
