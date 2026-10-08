#!/usr/bin/env python3
"""Track Q, Part 1: exact minimum excess of a law R-cycle under partition-preserving add+delete surgery.

Problem (exact, any graph).  Fix the hole h (vertex 0, link 1..5 in cyclic order) and the L colourings c_0..c_{L-1}
of a law R-cycle C of G - h (from tn_eng --dump).  For every state t and colour pair {p,q} let Part(t,p,q) be the
vertex partition of G_t[p,q] into components.  A graph G' on the same vertices (h and its 5 edges unchanged, link
5-cycle present, no link chord) carries C as the *same* law R-cycle with the same partitions iff
  (a) every edge xy of G' - h is properly coloured at every state and joins two vertices of the same part of
      Part(t, c_t(x), c_t(y)) for every t        [ground set U = all such pairs]
  (b) for every t and every part P (|P| >= 2) of every Part(t,p,q), the edges of G' inside P connect P.
(Then pair-graph partitions, locks, K_t, pi, N and the law are unchanged; see TrackN tn_forest.py header.)
Minimise |E(G' - h)|; excess e = min - (3 nv - 8), nv = n - 1.  Note: every graph G' with these colourings and these
partitions is of this form, so the optimum is the minimum over ALL graphs carrying a law R-cycle with the same
10-state colouring data and vertex partitions (not only modifications of one skeleton).

Engines.
  H: HiGHS (scipy.optimize.milp, mip_rel_gap = 0) with lazy cut generation: start with vertex-star cuts, solve to
     optimality, add the cut delta(S) cap E(P) >= 1 for every component S of every disconnected part, repeat.  The
     final MILP is a relaxation of (b) whose optimum is feasible for (b), hence optimal: certificate = (cut family,
     relaxation optimum = incumbent value, solver status Optimal, gap 0).
  C: OR-tools CP-SAT, same scheme, independent solver; the proven optimum is compared.
  Also: LP bound of the full cut formulation (separation by max-flow/min-cut on fractional points), for information.
usage: tq_exact.py OUT.jsonl FILE [--engines HC] [--nolinkforce] [--max K]
"""
import sys, os, json, time
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import coo_matrix
import networkx as nx
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from tn_lib import Engine, adjof, to_line
from tn_forest import parse_dump, cycles_in_R_law, components, PAIRS, law_ok


def build(n, E, cols, linkforce=True):
    """ground set U, list of parts (t,p,q,P), forced edge indices."""
    Eo = [tuple(sorted(e)) for e in E]
    parts = []; compid = []
    for t, c in enumerate(cols):
        d = {}
        for (p, q) in PAIRS:
            V = [v for v in range(1, n) if c[v] in (p, q)]
            for k, P in enumerate(components(V, [e for e in Eo if c[e[0]] in (p, q) and c[e[1]] in (p, q)])):
                for v in P: d[(p, q, v)] = (t, p, q, k)
                if len(P) > 1: parts.append((t, p, q, frozenset(P)))
        compid.append(d)
    link = {(t, t % 5 + 1) if t < 5 else (1, 5) for t in range(1, 6)}
    U = []
    for x in range(1, n):
        for y in range(x + 1, n):
            if x <= 5 and y <= 5 and (x, y) not in link: continue
            ok = True
            for c, d in zip(cols, compid):
                if c[x] == c[y]: ok = False; break
                pq = tuple(sorted((c[x], c[y])))
                if d[pq + (x,)] != d[pq + (y,)]: ok = False; break
            if ok: U.append((x, y))
    forced = [k for k, e in enumerate(U) if e in link] if linkforce else []
    assert all(e in U for e in Eo), 'original edge outside ground set?'
    return U, parts, forced


def inside(U, P):
    return [k for k, (a, b) in enumerate(U) if a in P and b in P]


def cut_of(U, P, S):
    return [k for k, (a, b) in enumerate(U) if a in P and b in P and ((a in S) != (b in S))]


def separate_int(U, parts, x):
    K = [U[k] for k in range(len(U)) if x[k] > 0.5]
    new = []
    for (t, p, q, P) in parts:
        pieces = components(list(P), [e for e in K if e[0] in P and e[1] in P])
        if len(pieces) > 1:
            for S in pieces: new.append(cut_of(U, P, S))
    return new


def seed_cuts(U, parts):
    cuts = []
    for (t, p, q, P) in parts:
        for v in P: cuts.append(cut_of(U, P, {v}))
    return cuts


def key(cut): return tuple(sorted(cut))


def solve_highs(U, parts, forced, cuts, tlim=3000):
    m = len(U); cuts = list(cuts); seen = {key(c) for c in cuts}; it = 0; t0 = time.time()
    while True:
        it += 1
        ri, rj = [], []
        for r, cu in enumerate(cuts):
            for k in cu: ri.append(r); rj.append(k)
        A = coo_matrix((np.ones(len(ri)), (ri, rj)), shape=(len(cuts), m)).tocsr()
        lb = np.zeros(m); lb[forced] = 1
        res = milp(np.ones(m), constraints=LinearConstraint(A, 1, np.inf), integrality=np.ones(m), bounds=Bounds(lb, np.ones(m)),
                   options=dict(time_limit=tlim, disp=False, mip_rel_gap=0.0))
        if res.status != 0: return dict(status='notoptimal:' + str(res.message), it=it)
        x = res.x; new = [c for c in separate_int(U, parts, x) if key(c) not in seen]
        for c in new: seen.add(key(c)); cuts.append(c)
        if not new:
            K = [U[k] for k in range(m) if x[k] > 0.5]
            return dict(status='optimal', opt=int(round(res.fun)), dual_bound=float(getattr(res, 'mip_dual_bound', res.fun)), gap=float(getattr(res, 'mip_gap', 0.0)),
                        it=it, ncuts=len(cuts), K=K, secs=round(time.time() - t0, 1), cuts=cuts)


def solve_cpsat(U, parts, forced, cuts, hint=None, tlim=3000, workers=1):
    from ortools.sat.python import cp_model
    m = len(U); cuts = list(cuts); seen = {key(c) for c in cuts}; it = 0; t0 = time.time()
    while True:
        it += 1
        md = cp_model.CpModel(); x = [md.NewBoolVar('x%d' % k) for k in range(m)]
        for k in forced: md.Add(x[k] == 1)
        for cu in cuts: md.AddBoolOr([x[k] for k in cu])
        md.Minimize(sum(x))
        if hint is not None:
            for k in range(m): md.AddHint(x[k], int(hint[k]))
        s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = tlim; s.parameters.num_search_workers = workers
        st = s.Solve(md)
        if st != cp_model.OPTIMAL: return dict(status='notoptimal:' + s.StatusName(st), it=it)
        xv = [s.Value(x[k]) for k in range(m)]
        new = [c for c in separate_int(U, parts, xv) if key(c) not in seen]
        for c in new: seen.add(key(c)); cuts.append(c)
        if not new:
            return dict(status='optimal', opt=int(round(s.ObjectiveValue())), bound=s.BestObjectiveBound(), it=it, ncuts=len(cuts),
                        K=[U[k] for k in range(m) if xv[k]], secs=round(time.time() - t0, 1))


def lp_bound(U, parts, forced, cuts):
    """LP relaxation of the full cut formulation, exact separation by min-cut per part."""
    m = len(U); cuts = list(cuts); seen = {key(c) for c in cuts}
    for it in range(500):
        ri, rj = [], []
        for r, cu in enumerate(cuts):
            for k in cu: ri.append(r); rj.append(k)
        A = coo_matrix((np.ones(len(ri)), (ri, rj)), shape=(len(cuts), m)).tocsr()
        lb = np.zeros(m); lb[forced] = 1
        res = milp(np.ones(m), constraints=LinearConstraint(A, 1, np.inf), integrality=np.zeros(m), bounds=Bounds(lb, np.ones(m)))
        x = res.x; new = []
        for (t, p, q, P) in parts:
            G = nx.Graph(); G.add_nodes_from(P)
            for k in inside(U, P):
                if x[k] > 1e-9: G.add_edge(*U[k], weight=x[k])
            if not nx.is_connected(G):
                for S in nx.connected_components(G):
                    c = cut_of(U, P, S)
                    if key(c) not in seen: new.append(c); seen.add(key(c))
                continue
            val, (S, T) = nx.stoer_wagner(G)
            if val < 1 - 1e-7:
                c = cut_of(U, P, set(S))
                if key(c) not in seen: new.append(c); seen.add(key(c))
        if not new: return float(res.fun), it
        cuts += new
    return float(res.fun), -1


def main():
    args = sys.argv[1:]; outp = args.pop(0)
    eng = 'HC'; linkforce = True; mx = 10 ** 9; lp = False
    if '--engines' in args: k = args.index('--engines'); eng = args[k + 1]; del args[k:k + 2]
    if '--nolinkforce' in args: args.remove('--nolinkforce'); linkforce = False
    if '--lp' in args: args.remove('--lp'); lp = True
    if '--max' in args: k = args.index('--max'); mx = int(args[k + 1]); del args[k:k + 2]
    out = open(outp, 'a'); ed = Engine(dump=True, maxstates=200000); ec = Engine(maxstates=400000)
    cnt = 0
    for f in args:
        for l in open(f):
            if cnt >= mx: break
            if l.startswith('{'):
                d = json.loads(l)
                if 'graph' not in d: continue
                l = d['graph']
            p = l.split()
            if len(p) < 3: continue
            rot = [list(map(int, r.split(','))) for r in p[2].split(';')]
            n = len(rot); E = {frozenset((u, v)) for u in range(1, n) for v in rot[u] if v != 0}
            js, tn, dump = ed.run(l)
            if tn is None: continue
            S = parse_dump(dump); cyc = cycles_in_R_law(S)
            if not cyc: print('no law cycle', p[0]); continue
            cnt += 1
            C = cyc[0]; cols = [[-1 if ch == '-' else int(ch) for ch in S[x]['col']] for x in C]
            U, parts, forced = build(n, E, cols, linkforce)
            nv = n - 1; base = 3 * nv - 8
            rec = dict(src=p[0], n=n, nedge=len(E), e_orig=len(E) - base, cyclen=len(C), Nprof=''.join(str(S[x]['N']) for x in C),
                       ground=len(U), addable=len(U) - len(E), nparts=len(parts), linkforce=linkforce)
            cuts0 = seed_cuts(U, parts)
            if lp:
                lv, lit = lp_bound(U, parts, forced, cuts0); rec['lp_bound'] = round(lv, 4); rec['lp_e'] = round(lv - base, 4)
            Kbest = None
            if 'H' in eng:
                r = solve_highs(U, parts, forced, cuts0)
                rec['highs'] = {k: v for k, v in r.items() if k not in ('K', 'cuts')}
                if r['status'] == 'optimal':
                    rec['highs']['e'] = r['opt'] - base; Kbest = r['K']
                    cutsH = r['cuts']
            if 'C' in eng:
                hint = None
                if Kbest is not None:
                    Ks = set(Kbest); hint = [1 if e in Ks else 0 for e in U]
                r = solve_cpsat(U, parts, forced, cuts0, hint=hint)
                rec['cpsat'] = {k: v for k, v in r.items() if k != 'K'}
                if r['status'] == 'optimal':
                    rec['cpsat']['e'] = r['opt'] - base
                    if Kbest is None: Kbest = r['K']
            if Kbest is not None:
                line = to_line(p[0] + '_Q', adjof({frozenset(e) for e in Kbest}, n)); js2, tn2, _ = ec.run(line)
                rec.update(kedges=len(Kbest), check_cyc=tn2['cyc'] if tn2 else None, graph=line)
                if 'H' in eng and rec['highs'].get('status') == 'optimal':
                    with open(os.path.join(os.path.dirname(outp), 'cert_%s.json' % p[0]), 'w') as fc:
                        json.dump(dict(src=p[0], n=n, ground=U, forced=forced, cols=cols, cuts=cutsH, opt=rec['highs']['opt'], base=base), fc)
            out.write(json.dumps(rec) + '\n'); out.flush()
            print(json.dumps({k: v for k, v in rec.items() if k != 'graph'}), flush=True)


if __name__ == '__main__':
    main()
