#!/usr/bin/env python3
"""Track N: exact edge-set surgery (ILP) for Q-e.

Idea [hand, elementary]: let C be a pi-cycle of DL states with N <= 9 and the chain-parity law (any graph G, hole h).
If we delete edges of G - h (or add properly coloured edges) so that, at EVERY state s of C, every pair graph
G_s[p,q] keeps the same vertex partition into components, then every s stays a proper colouring, the locks, inA/inB,
the swap set K_{alpha A}(x_{j+2}) and hence pi, N(s) and the law are unchanged: C is still such a pi-cycle in G'.
So Q-e (cycle-state version) for G reduces to choosing an edge set K (link 5-cycle kept) with
  (conn) for every s in C and pair {p,q}: K contains a spanning tree of each component of G_s[p,q]
  (233)  for every s in C and perfect matching m of K4: |K cap E_m(s)| = nv - 1 - (5 - l_m(s))/2   (Lemma E constants)
Ground set: edges of G - h, plus (option --add) every non-edge xy (not link-link) that is properly coloured at all s in C
and joins two vertices of the same {c_s(x), c_s(y)}-component at all s (adding it never merges components).
Solved with scipy milp (HiGHS) and lazy cut generation for (conn).  If infeasible, we minimise the total |deviation|
sum_s sum_m |...| (closeness).  Each feasible K is re-checked with tn_eng (cyc[3] > 0) and written out.
usage: tn_forest.py OUT.jsonl [--add] [--nolaw] [--flow [--flowt SEC]] [--max K]   (--flow: single-MILP flow model of tn_flow.py) FILE [FILE ...]   (FILE: graph lines or jsonl with 'graph')
"""
import sys, json, time
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix
from tn_lib import Engine, adjof, to_line, notri

FLOW = False; FLOWT = 120
MT = [[-1, 0, 1, 2], [0, -1, 2, 1], [1, 2, -1, 0], [2, 1, 0, -1]]
PAIRS = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]


def parse_dump(lines):
    S = []
    for l in lines:
        a, b = l.split('|')
        p = a.split()
        S.append(dict(i=int(p[1]), cls=int(p[2]), kind=int(p[3]), pi=int(p[9]), N=int(p[10]), oncyc=int(p[12]), dev=int(p[14]), col=p[15]))
    return S


def law_ok(S, x):
    y = S[x]['pi']
    return ((S[y]['N'] - S[x]['N']) & 1) == (1 if S[y]['kind'] == 1 else 0)


def cycles_in_R_law(S, uselaw=True):
    good = lambda x: x >= 0 and S[x]['kind'] == 1 and S[x]['N'] <= 9
    seen = set(); out = []
    for i in range(len(S)):
        if i in seen or not good(i): continue
        path = []; x = i; pos = {}
        while good(x) and x not in pos and x not in seen:
            pos[x] = len(path); path.append(x)
            if uselaw and not law_ok(S, x): x = -1; break
            x = S[x]['pi']
        if x >= 0 and x in pos: out.append(path[pos[x]:])
        seen.update(path)
    return out


def components(V, edges):
    par = {v: v for v in V}
    def f(a):
        while par[a] != a: par[a] = par[par[a]]; a = par[a]
        return a
    for u, v in edges:
        a, b = f(u), f(v)
        if a != b: par[a] = b
    comp = {}
    for v in V: comp.setdefault(f(v), set()).add(v)
    return list(comp.values())


def solve(n, E, cols, add=False, seed=0, tlim=60, phases=('exact', 'relax'), verbose=False):
    """cols: list of colourings (lists, index = vertex, h = 0 -> -1). Returns (status, K, dev)."""
    nv = n - 1
    link = {frozenset((t, t % 5 + 1)) for t in range(1, 6)}
    ground = sorted(tuple(sorted(e)) for e in E)
    if add:
        Es = set(E)
        # components at each state and pair
        compid = []
        for c in cols:
            d = {}
            for (p, q) in PAIRS:
                V = [v for v in range(1, n) if c[v] in (p, q)]
                for k, C in enumerate(components(V, [tuple(e) for e in E if all(c[x] in (p, q) for x in e)])):
                    for v in C: d[(p, q, v)] = k
            compid.append(d)
        for x in range(1, n):
            for y in range(x + 1, n):
                if frozenset((x, y)) in Es or (x <= 5 and y <= 5): continue
                ok = True
                for c, d in zip(cols, compid):
                    if c[x] == c[y]: ok = False; break
                    pq = tuple(sorted((c[x], c[y])))
                    if d[pq + (x,)] != d[pq + (y,)]: ok = False; break
                if ok: ground.append((x, y))
    m = len(ground); idx = {e: k for k, e in enumerate(ground)}
    # equality rows (233)
    rows = []; tg = []
    for c in cols:
        lm = [0, 0, 0]
        for t in range(1, 6): lm[MT[c[t]][c[t % 5 + 1]]] += 1
        for mm in range(3):
            rows.append([k for k, (u, v) in enumerate(ground) if MT[c[u]][c[v]] == mm]); tg.append(nv - 1 - (5 - lm[mm]) // 2)
    # pair-graph components (target partition) from the ORIGINAL edges
    comps = []
    for si, c in enumerate(cols):
        for (p, q) in PAIRS:
            V = [v for v in range(1, n) if c[v] in (p, q)]
            for C in components(V, [tuple(sorted(e)) for e in E if all(c[x] in (p, q) for x in e)]):
                if len(C) > 1: comps.append((si, p, q, frozenset(C)))
    cuts = []
    # seed cuts: every non-isolated vertex of each component needs an incident pq-edge in K
    for (si, p, q, C) in comps:
        c = cols[si]
        for v in C:
            cuts.append([k for k, (a, b) in enumerate(ground) if (a == v and b in C) or (b == v and a in C)])
    rng = np.random.default_rng(seed)
    nrow = len(rows)
    lb = np.zeros(m); ub = np.ones(m)
    for k, e in enumerate(ground):
        if frozenset(e) in link: lb[k] = 1
    for phase in phases:
        it = 0
        while True:
            it += 1
            if phase == 'exact':
                nx = m; cobj = rng.random(m) * 0.01
            else:
                nx = m + 2 * nrow; cobj = np.concatenate([np.zeros(m), np.ones(2 * nrow)])
            A = lil_matrix((nrow + len(cuts), nx)); lo = []; hi = []
            for r, (row, t) in enumerate(zip(rows, tg)):
                for k in row: A[r, k] = 1
                if phase == 'relax': A[r, m + 2 * r] = 1; A[r, m + 2 * r + 1] = -1
                lo.append(t); hi.append(t)
            for r, cut in enumerate(cuts):
                for k in cut: A[nrow + r, k] = 1
                lo.append(1); hi.append(np.inf)
            bl = np.concatenate([lb, np.zeros(nx - m)]); bu = np.concatenate([ub, np.full(nx - m, np.inf)])
            res = milp(cobj, constraints=LinearConstraint(A.tocsr(), lo, hi), integrality=np.concatenate([np.ones(m), np.zeros(nx - m)]),
                       bounds=Bounds(bl, bu), options=dict(time_limit=tlim, disp=False))
            if res.x is None:
                if phase == 'exact': break
                return ('fail', None, None, len(ground) - len(E))
            x = np.round(res.x[:m]).astype(int)
            K = [ground[k] for k in range(m) if x[k]]
            new = 0
            for (si, p, q, C) in comps:
                c = cols[si]
                pieces = components(list(C), [e for e in K if e[0] in C and e[1] in C])
                if len(pieces) > 1:
                    for P in pieces:
                        cuts.append([k for k, (a, b) in enumerate(ground) if (a in P) != (b in P) and a in C and b in C]); new += 1
            if verbose: print('  it', it, phase, 'dev', round(res.fun, 2) if phase == 'relax' else '-', 'newcuts', new, 'status', res.status, flush=True)
            if new == 0:
                dev = 0 if phase == 'exact' else int(round(res.fun))
                return (phase, K, dev, len(ground) - len(E))
            if it > 400: return ('iter', None, None, len(ground) - len(E))
    return ('fail', None, None, 0)


def main():
    args = sys.argv[1:]; out = open(args.pop(0), 'a'); add = False; mx = 10 ** 9
    if '--add' in args: args.remove('--add'); add = True
    global FLOW, FLOWT
    FLOW = '--flow' in args
    if FLOW: args.remove('--flow')
    FLOWT = 120
    if '--flowt' in args: k = args.index('--flowt'); FLOWT = float(args[k + 1]); del args[k:k + 2]
    uselaw = '--nolaw' not in args
    if not uselaw: args.remove('--nolaw')
    if '--max' in args: k = args.index('--max'); mx = int(args[k + 1]); del args[k:k + 2]
    ed = Engine(dump=True, maxstates=200000); ec = Engine(maxstates=400000)
    cnt = 0
    for f in args:
        for l in open(f):
            if cnt >= mx: break
            if l.startswith('{'):
                d = json.loads(l)
                if d.get('ev', 'example') != 'example' or 'graph' not in d: continue
                l = d['graph']
            p = l.split()
            if len(p) < 3: continue
            rot = [list(map(int, r.split(','))) for r in p[2].split(';')]
            n = len(rot); nv0 = n - 1; E = {frozenset((u, v)) for u in range(1, n) for v in rot[u] if v != 0}
            js, tn, dump = ed.run(l)
            if tn is None: continue
            S = parse_dump(dump)
            cyc = cycles_in_R_law(S, uselaw)
            if not cyc: continue
            cnt += 1
            for ci, C in enumerate(cyc[:2]):
                cols = [[-1 if ch == '-' else int(ch) for ch in S[x]['col']] for x in C]
                t0 = time.time()
                if FLOW:
                    from tn_flow import solve_flow, addable
                    ground = sorted(tuple(sorted(e)) for e in E); ad = addable(n, E, cols) if add else []
                    dev, K, msg = solve_flow(n, E, cols, ground + ad, tlim=FLOWT)
                    st = ('exact' if dev == 0 else 'relax') + ('' if 'Optimal' in str(msg) else '_timelimit'); nadd = len(ad)
                else:
                    st, K, dev, nadd = solve(n, E, cols, add=add)
                lawf = sum(1 for x in C if not law_ok(S, x))
                rec = dict(src=p[0], lawfails=lawf, n=n, nedge=len(E), target=3 * n - 11, cyclen=len(C), Nprof=''.join(str(S[x]['N']) for x in C),
                           add=add, nadd=nadd, status=st, mindev=dev, secs=round(time.time() - t0, 1))
                if K is not None:
                    Ks = {frozenset(e) for e in K}
                    exv = {}
                    for c, x in zip(cols, C):
                        Em = [0, 0, 0]; lm = [0, 0, 0]
                        for (u, v) in K: Em[MT[c[u]][c[v]]] += 1
                        for t in range(1, 6): lm[MT[c[t]][c[t % 5 + 1]]] += 1
                        k3 = lm.index(3); order = [k3] + [m for m in range(3) if m != k3]   # P1 first (the matching with 3 link edges)
                        key = '%d:' % S[x]['N'] + ','.join(str(Em[m] - (nv0 - 1 - (5 - lm[m]) // 2)) for m in order)
                        exv[key] = exv.get(key, 0) + 1
                    rec['excess_P1P2P3'] = exv
                    adj = adjof(Ks, n); line = to_line(p[0] + '_K', adj)
                    js2, tn2, _ = ec.run(line)
                    rec.update(kedges=len(K), deleted=len(E - Ks), added=len(Ks - E), check_cyc=tn2['cyc'] if tn2 else None, check_run=tn2['run'] if tn2 else None,
                               cls3=tn2.get('cls3') if tn2 else None, states=js2.get('states'), filled=js2.get('filled'), notri=notri(adj),
                               mindeg=min(len(a) for a in adj[1:]), graph=line)
                out.write(json.dumps(rec) + '\n'); out.flush()
                print(json.dumps({k: v for k, v in rec.items() if k != 'graph'}), flush=True)


if __name__ == '__main__':
    main()
