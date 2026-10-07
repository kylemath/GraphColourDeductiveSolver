#!/usr/bin/env python3
"""Job AX [exploratory]: NightCutParity Sec. 3 test. u* = apex of the face on the ring edge w3-y away from x- (= x_{q+4}). omega = the colour shared by every swap pair
(= c(x+) at R3k4). Per period b (positions 10b .. 10b+9, starting at R3k4): (a) u* in exactly one of K_0, K_7; (b) u* in S_b = A_b xor A_{b+1} (A_b = omega-class at
the start of period b); (c) A_{b+2} = A_b; plus checks: every swap pair contains omega; the free steps ({c(w3),c(y)}-complement pairs) are exactly steps 0 and 7 and contain x-.
Degree 6: the jobav-cycles.jsonl replays. Other single-high-vertex patterns (5,5,5,5,7), (5,5,5,5,8) and (5,5,5,5,5) at orders 25-27, both orientations: replay here
(jobav.Frame / step logic, positions from the NightA34 table with q = the high-degree link vertex; at (5,5,5,5,5) every q = 0..4 is tried)."""
import sys, os, json
from collections import Counter
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../jobav')); sys.path.insert(0, os.path.join(HERE, '../jobuv'))
import jobav
from jobav import Frame, partition, POS
class FrameQ(Frame):
    def __init__(self, adj, link, w, q):
        self.adj, self.L, self.w, self.q = adj, link, w, q
        X = lambda i: link[(q + i) % 5]; W = lambda i: w[(q + i) % 5]
        self.names = dict(p=X(0), xp=X(1), x2=X(2), x3=X(3), xm=X(4), z=W(0), wp=W(1), w2=W(2), w3=W(3), y=W(4))
def ustar(adj, n):
    c = [v for v in adj[n['w3']] & adj[n['y']] if v != n['xm']]; assert len(c) == 1, c; return c[0]
def analyse(F, cyc):
    """cyc: colourings in pi order. Returns per-period rows or an error string."""
    L = len(cyc); P = [F.pos(c) for c in cyc]
    if None in P or 0 not in P: return 'no universal-period position labelling'
    s = P.index(0); cyc = cyc[s:] + cyc[:s]; P = P[s:] + P[:s]
    if any(P[t] != t % 10 for t in range(L)): return 'positions not 0..9 cyclic'
    n = F.names; us = ustar(F.adj, n); col = dict(cyc[0]); om = col[n['xp']]; A = []; Ks = []; pairs = []; free = []
    for t in range(L):
        if partition(col) != partition(cyc[t]): return 'replay diverged'
        if t % 10 == 0: A.append(frozenset(v for v, c in col.items() if c == om))
        pair, K = F.step(col); pairs.append(om in pair); Ks.append(K)
        if set(pair) == {0, 1, 2, 3} - {col[n['w3']], col[n['y']]}: free.append((t % 10, n['xm'] in K))
        a, b = pair; col = {v: (b if v in K and c == a else a if v in K and c == b else c) for v, c in col.items()}
    if partition(col) != partition(cyc[0]): return 'replay does not close'
    m = L // 10; rows = []
    for b in range(m):
        k0, k7 = us in Ks[10 * b], us in Ks[10 * b + 7]
        rows.append(dict(k0=k0, k7=k7, S_size=len(A[b] ^ A[(b + 1) % m]), one_of_K0K7=k0 != k7, in_S=us in (A[b] ^ A[(b + 1) % m]), A_period2=A[(b + 2) % m] == A[b], omega_in_all_pairs=all(pairs[10 * b:10 * b + 10]),
                         free_steps=sorted(f for f, _ in free if 10 * b <= 0 or True)))
    fs = Counter(f for f, _ in free); fx = all(x for _, x in free)
    Sall = frozenset.intersection(*[A[b] ^ A[(b + 1) % m] for b in range(m)]); inv = {v: k for k, v in n.items()}
    nb = lambda v: sorted(inv.get(u, 'far') for u in F.adj[v] if u in inv)
    return dict(L=L, m=m, rows=rows, S_all=[(v, inv.get(v, 'far'), nb(v)) for v in sorted(Sall)], ustar=us, free_step_positions=sorted(fs), xm_in_free=fx, A_recur_odd=any(A[(b + k) % m] == A[b] for b in range(m) for k in range(1, m, 2)))
def census_job(args):
    from uv_lib import Hole
    lab, name, hole = args
    H = Hole(name, hole, lab.endswith('m')); adj = {v: set(r) - {hole} for v, r in enumerate(H.rot) if v != hole}
    deg = [len(H.rot[x]) for x in H.L]; hi = [t for t in range(5) if deg[t] >= 6]
    qs = hi if len(hi) == 1 else (list(range(5)) if not hi else [])
    out = []
    for ci, z in enumerate(H.cycles):
        if not all(H.DL[x] for x in z): continue
        cyc = [{v: H.col(x, v) for v in H.sp.order} for x in z]
        res = {q: analyse(FrameQ(adj, H.L, H.w, q), cyc) for q in qs}
        out.append(dict(run=lab, name=name, hole=hole, pattern=tuple(sorted(deg)), L=len(z), byq=res))
    return out
def summarise(tag, per):
    c = Counter()
    for rows in per:
        for r in rows['rows']:
            for k in ('one_of_K0K7', 'in_S', 'A_period2', 'omega_in_all_pairs'): c[(k, r[k])] += 1
        c[('a vertex flips omega-membership in every period (intersection of S_b nonempty)', bool(rows['S_all']))] += 1
        c[('u* flips in every period', all(r['in_S'] for r in rows['rows']))] += 1
        for r in rows['rows']:
            if not r['one_of_K0K7']: c[('u* failure kind', 'both K0 and K7' if r['k0'] else 'neither')] += 1
        c[('free steps', tuple(rows['free_step_positions']))] += 1; c[('x- in every free component', rows['xm_in_free'])] += 1; c[('A recurs at odd distance', rows['A_recur_odd'])] += 1
    print('%s: %d cycles, %d periods' % (tag, len(per), sum(r['m'] for r in per)))
    for k, v in sorted(c.items(), key=str): print('    ', v, k)
if __name__ == '__main__':
    out = {}
    per = []
    for l in open(os.path.join(HERE, '../jobav/jobav-cycles.jsonl')):
        r = json.loads(l); n = r['names']
        cols = [dict(zip(r['vertices'], c)) for c in r['colourings']]
        holeadj = None
        per.append((r['source'], r['name'], r['hole'], r['orientation'], cols))
    # rebuild frames for the degree-6 records directly from the graphs (census: Hole; constructions: jobaq loader)
    from jobag import canon
    holes = set()
    for lab in ['z25', 'z25m', 'z26', 'z26m', 'z27', 'z27m']:
        for l in open(os.path.join(HERE, '../out/%s.jsonl' % lab)):
            if '"jobs": {"pos": [{' not in l: continue
            r = json.loads(l); p = canon(r['linkdeg'])
            if p in ((5, 5, 5, 5, 6), (5, 5, 5, 5, 7), (5, 5, 5, 5, 8), (5, 5, 5, 5, 5)) and any(z['gamma'] for z in r['jobs']['pos']): holes.add((lab, r['name'], r['hole']))
    with Pool(12) as P: res = [x for xs in P.map(census_job, sorted(holes)) for x in xs]
    # constructions (degree 6) from the jobav replays: colourings already absolute and starting at R3k4
    sys.path.insert(0, os.path.join(HERE, '../jobaq')); import jobaq; jobaq.GDIR = os.path.join(HERE, '../jobas/')
    cons = []
    for src, name, hole, ori, cols in per:
        if src != 'construction': continue
        E, adj0, link, w = jobaq.load(name, hole, ori == 'mirror'); adj = {v: set(a) - {hole} for v, a in adj0.items() if v != hole}
        q = next(t for t in range(5) if len(adj0[link[t]]) >= 6)
        cons.append(dict(name=name, hole=hole, L=len(cols), byq={q: analyse(FrameQ(adj, link, w, q), cols)}))
    json.dump(dict(census=res, constructions=cons), open(os.path.join(HERE, 'jobax.json'), 'w'), default=list)
    for pat in ((5, 5, 5, 5, 6), (5, 5, 5, 5, 7), (5, 5, 5, 5, 8)):
        rr = [r for r in res if r['pattern'] == pat]; ok = [v for r in rr for v in r['byq'].values() if isinstance(v, dict)]
        err = Counter(v for r in rr for v in r['byq'].values() if isinstance(v, str))
        summarise('census %s' % (pat,), ok); print('     errors:', dict(err))
    summarise('constructions (5,5,5,5,6)', [v for r in cons for v in r['byq'].values() if isinstance(v, dict)])
    rr = [r for r in res if r['pattern'] == (5, 5, 5, 5, 5)]
    print('census (5,5,5,5,5): %d cycles; cycles with a universal-period labelling for some q: %d; by number of valid q: %s' % (len(rr),
          sum(any(isinstance(v, dict) for v in r['byq'].values()) for r in rr), dict(Counter(sum(isinstance(v, dict) for v in r['byq'].values()) for r in rr))))
    summarise('census (5,5,5,5,5), every valid q', [v for r in rr for v in r['byq'].values() if isinstance(v, dict)])
    print('     errors:', dict(Counter(v for r in rr for v in r['byq'].values() if isinstance(v, str))))
