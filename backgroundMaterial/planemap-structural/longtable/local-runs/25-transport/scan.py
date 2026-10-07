#!/usr/bin/env python3
"""[exploratory] Run 25: capacitated transport T and variants on every Kempe class with a positive pi-cycle, orders 12-24.
Reuses pi/lambda/DL code of ../22-winding-escape/escape.py (same class construction as ../23-positive-cycles/scan.py)."""
import sys, json, time, itertools
sys.path.insert(0, '../common'); sys.path.insert(0, '../22-winding-escape')
from collections import Counter
from kempe_py import Space, gentri_rotation, adj_from_rot
from escape import pi_of, is_DL, abpairs, GENTRI

def maxflow(src, snk, edges):
    """src: {z: supply}, snk: {n: cap}, edges: {z: set(n)} bipartite, unit-free augmenting paths (Ford-Fulkerson with bottleneck)."""
    cap = {}; adj = {}
    def add(u, v, c):
        cap[(u, v)] = cap.get((u, v), 0) + c; cap.setdefault((v, u), 0)
        adj.setdefault(u, []).append(v); adj.setdefault(v, []).append(u)
    for z, s in src.items(): add('S', ('z', z), s)
    for n, c in snk.items(): add(('n', n), 'T', c)
    for z, ns in edges.items():
        for n in ns: add(('z', z), ('n', n), 10 ** 9)
    flow = 0
    while True:
        par = {'S': None}; q = ['S']
        for u in q:
            for v in adj.get(u, []):
                if v not in par and cap[(u, v)] > 0: par[v] = u; q.append(v)
        if 'T' not in par: return flow
        b = 10 ** 9; v = 'T'
        while par[v] is not None: b = min(b, cap[(par[v], v)]); v = par[v]
        v = 'T'
        while par[v] is not None: cap[(par[v], v)] -= b; cap[(v, par[v])] += b; v = par[v]
        flow += b

def evaluate(pos, W, edges):
    """pos: list of positive cycle ids, W: winding; edges: {z: set of negative cycle ids}. Returns dict."""
    supply = {z: W[z] for z in pos}
    nbrs = set().union(*[edges.get(z, set()) for z in pos]) if pos else set()
    snk = {n: -W[n] for n in nbrs}
    f = maxflow(supply, snk, edges)
    tot = sum(supply.values()); capr = sum(snk.values())
    # Hall deficiency over subsets of positive cycles (npos <= ~12)
    best = None
    if len(pos) <= 14:
        for r in range(1, len(pos) + 1):
            for S in itertools.combinations(pos, r):
                N = set().union(*[edges.get(z, set()) for z in S]); c = sum(-W[n] for n in N); s = sum(W[z] for z in S)
                key = (c - s, c / s)
                if best is None or key < best[0]: best = (key, [W[z] for z in S], c, s)
    return dict(ok=(f == tot), flow=f, supply=tot, capreach=capr, slack=capr - tot,
                hall_slack=None if best is None else best[0][0], hall_ratio=None if best is None else round(best[0][1], 3),
                bad_cut=None if best is None else dict(Wset=best[1], cap=best[2], supply=best[3]))

def analyse(n, gi, h, sp, recs):
    S = len(sp.states); pi = [None] * S; lam = [0] * S
    for k in range(S):
        t, l, _ = pi_of(sp, k); pi[k] = t; lam[k] = l
    cyc_of = [-1] * S; cycles = []
    for k in range(S):
        if cyc_of[k] >= 0: continue
        z = []; x = k
        while cyc_of[x] < 0: cyc_of[x] = len(cycles); z.append(x); x = pi[x]
        sl = sum(lam[x] for x in z); assert sl % 5 == 0
        cycles.append((z, sl // 5))
    posall = [ci for ci, (z, w) in enumerate(cycles) if w > 0]
    if not posall: return
    linkmask = 0
    for i in sp.linki: linkmask |= 1 << i
    mvc = {}
    def mv(k):
        if k not in mvc: mvc[k] = sp.moves(k)
        return mvc[k]
    done = set()
    for c0 in posall:
        if cycles[c0][0][0] in done: continue
        mem = [cycles[c0][0][0]]; seen = {mem[0]}
        for x in mem:
            for t, *_ in mv(x):
                if t not in seen: seen.add(t); mem.append(t)
        done |= seen
        cls = sorted({cyc_of[x] for x in mem})
        W = {ci: cycles[ci][1] for ci in cls}
        pos = [ci for ci in cls if W[ci] > 0]
        # directed labelled adjacency over ALL cycles of the class (link-free swaps only)
        # E[ci][cj] = set of flags: 'any', 'DL', 'DLab' (DL & {alpha,A}/{alpha,B}), 'DLother'
        E = {ci: {} for ci in cls}
        for ci in cls:
            for x in cycles[ci][0]:
                dl = is_DL(sp, x); ab = abpairs(sp, x) if dl else None
                for t, p, q, K in mv(x):
                    if t == x or K & linkmask: continue
                    cj = cyc_of[t]
                    if cj == ci: continue
                    fl = E[ci].setdefault(cj, set()); fl.add('any')
                    if dl:
                        fl.add('DL'); fl.add('DLab' if frozenset((p, q)) in ab else 'DLother')
        neg = [c for c in cls if W[c] < 0]; zero = [c for c in cls if W[c] == 0]
        def direct(flag):
            return {z: {c for c, fl in E[z].items() if flag in fl and W[c] < 0} for z in pos}
        def relay(first, second, via):
            ed = {}
            for z in pos:
                s = {c for c, fl in E[z].items() if first in fl and W[c] < 0}
                for m, fl in E[z].items():
                    if first in fl and m != z and via(m):
                        s |= {c for c, f2 in E[m].items() if second in f2 and W[c] < 0}
                ed[z] = s
            return ed
        V = {
            'T1_DL': direct('DL'), 'T2_any': direct('any'), 'T3_DLalphaAB': direct('DLab'), 'T3x_DLotherpair': direct('DLother'),
            'T4_d2_DL_zero': relay('DL', 'any', lambda m: W[m] == 0),   # relay only through zero-winding cycles, first hop from DL
            'T4_d2_any_zero': relay('any', 'any', lambda m: W[m] == 0),
            'T4_d2_any_anycycle': relay('any', 'any', lambda m: True),
            'T4_d2_DL_anycycle': relay('DL', 'any', lambda m: True),
        }
        # d2 variants must keep the d1 sinks too (relay() starts with direct set s) -> yes s initialised with first-hop negatives
        rec = dict(n=n, gentri=gi, hole=h, states=len(mem), ncyc=len(cls), npos=len(pos), nneg=len(neg), nzero=len(zero),
                   posW=sorted((W[z] for z in pos), reverse=True), minW=min(W.values()),
                   v={k: evaluate(pos, W, ed) for k, ed in V.items()})
        recs.append(rec)

def run(args):
    n, gi, line = args
    rot = gentri_rotation(line); adj = adj_from_rot(rot); recs = []
    for h in range(len(rot)):
        if len(rot[h]) != 5: continue
        try: sp = Space(adj, h, link=rot[h])
        except AssertionError: continue
        analyse(n, gi, h, sp, recs)
    return n, gi, recs

if __name__ == '__main__':
    import multiprocessing as mp
    n = int(sys.argv[1])
    # restrict to graphs that have a positive class, using run-23 output
    gset = {json.loads(l)['gentri'] for l in open('../23-positive-cycles/out-%d.jsonl' % n) if '"class"' in l}
    lines = [l for l in open(GENTRI % n) if l.startswith('G')]
    jobs = [(n, gi, l) for gi, l in enumerate(lines, 1) if gi in gset]
    t0 = time.time()
    with mp.Pool(3) as pool, open('out-%d.jsonl' % n, 'w') as out:
        for _, gi, recs in pool.imap_unordered(run, jobs, chunksize=1):
            for r in recs: out.write(json.dumps(r) + '\n')
            out.flush()
    print(n, len(jobs), 'graphs', '%.0fs' % (time.time() - t0), flush=True)
