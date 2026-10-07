#!/usr/bin/env python3
"""Job AV [exploratory]: per (5,5,5,5,6) Gamma-cycle, an absolute-name, absolute-colour dump for the two-period analysis of A34' (NightA34 Sec. 1-2 conventions).
Fixed names from the hole (q = the degree-6 link vertex): p = x_q, x+ = x_{q+1}, x2, x3, x- = x_{q+4}; z = w_q, w+ = w_{q+1}, w2, w3, y = w_{q+4}; m = p's sixth neighbour.
Positions: 0 R3k4, 1 R1k1, 2 R3k3, 3 R1k0, 4 R3k2, 5 R1k4, 6 R3k1, 7 R1k3, 8 R3k0, 9 R1k2 (mod 10); the dump starts at an R3k4 state (position 0).
Absolute colours: start from the canonical colouring of the position-0 state; step t swaps the generic pi-move component (jobam.stepK logic) in absolute colours;
every step is checked to equal the next cycle state as a vertex partition (i.e. up to colour renaming).
Per cycle: 20 (or L) colourings; per step the swapped pair and component; K at positions 8 mod 10; the pocket at positions 9 mod 10 (the {c(p),c(m)}-component of m in
T - h - p - x+, and whether it contains w+); |K_{c(p),c(m)}(p)| at positions 0 mod 10 (k = 4 visits); J (y ~ z in G_{c(y),c(z)}) at every position;
break flags: k4fail / k3fail (sigma at R3k4 / R3k3 not lockless), step8break (J false at position 9 mod 10).
Census: orders 25-27 both orientations (uv_lib.Hole, full state space). Constructions: Job AS graphs, classes reached from 40 random colourings (seed 1), lib26.Eng."""
import sys, os, json, itertools, random
from collections import Counter
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../jobuv')); sys.path.insert(0, os.path.join(HERE, '../../26-transport-adversarial')); sys.path.insert(0, os.path.join(HERE, '../../25-transport'))
sys.path.insert(0, os.path.join(HERE, '../../common')); sys.path.insert(0, os.path.join(HERE, '../../22-winding-escape'))
POS = {(3, 4): 0, (1, 1): 1, (3, 3): 2, (1, 0): 3, (3, 2): 4, (1, 4): 5, (3, 1): 6, (1, 3): 7, (3, 0): 8, (1, 2): 9}
def comp(adj, col, v, a, b):
    if col[v] not in (a, b): return set()
    K = {v}; st = [v]
    while st:
        u = st.pop()
        for x in adj[u]:
            if x not in K and col[x] in (a, b): K.add(x); st.append(x)
    return K
def partition(col):
    d = {}
    for v, c in col.items(): d.setdefault(c, set()).add(v)
    return frozenset(frozenset(s) for s in d.values())
class Frame:
    def __init__(self, adj, link, w):
        self.adj, self.L, self.w = adj, link, w
        q = next(t for t in range(5) if len(adj[link[t]]) + 1 >= 6); self.q = q
        X = lambda i: link[(q + i) % 5]; W = lambda i: w[(q + i) % 5]
        self.names = dict(p=X(0), xp=X(1), x2=X(2), x3=X(3), xm=X(4), z=W(0), wp=W(1), w2=W(2), w3=W(3), y=W(4))
        M = [u for u in adj[X(0)] if u not in (X(1), X(4), W(0), W(4))]; assert len(M) == 1, M
        self.names['m'] = M[0]
    def lframe(self, col):
        c = [col[x] for x in self.L]; cnt = Counter(c)
        if len(cnt) != 4: return None
        j = next(j for j in range(5) if c[j] == c[(j + 2) % 5] and cnt[c[j]] == 2)
        al, mu, A, B = c[j], c[(j + 1) % 5], c[(j + 3) % 5], c[(j + 4) % 5]
        w0, w3 = col[self.w[j]], col[self.w[(j + 3) % 5]]
        ty = 1 if w0 == A else (2 if (w0 == B and w3 == al) else (3 if (w0 == B and w3 == mu) else 0))
        return j, ty, (al, mu, A, B)
    def step(self, col):     # jobam.stepK in absolute colours; returns (pair, component)
        li = self.L; c = [col[x] for x in li]; cnt = Counter(c); adj = self.adj
        if len(cnt) == 4:
            j = next(j for j in range(5) if c[j] == c[(j + 2) % 5] and cnt[c[j]] == 2); al, mu, A, B = c[j], c[(j + 1) % 5], c[(j + 3) % 5], c[(j + 4) % 5]
            if li[(j + 4) % 5] in comp(adj, col, li[(j + 1) % 5], mu, B): return (al, A), comp(adj, col, li[(j + 2) % 5], al, A)
            return (mu, B), comp(adj, col, li[(j + 4) % 5], mu, B)
        i = next(i for i in range(5) if cnt[c[i]] == 1); Wc, Xc, Yc = c[i], c[(i + 1) % 5], c[(i + 2) % 5]; Zc = ({0, 1, 2, 3} - {Wc, Xc, Yc}).pop()
        K = comp(adj, col, li[(i + 2) % 5], Yc, Zc)
        if li[(i + 4) % 5] not in K: return (Yc, Zc), K
        return (Wc, Xc), comp(adj, col, li[(i + 3) % 5], Wc, Xc)
    def lockless(self, col):
        f = self.lframe(col)
        if f is None: return False
        j, ty, (al, mu, A, B) = f; li = self.L
        return li[(j + 3) % 5] not in comp(self.adj, col, li[(j + 1) % 5], mu, A) and li[(j + 4) % 5] not in comp(self.adj, col, li[(j + 1) % 5], mu, B)
    def sigma(self, col):
        j, ty, (al, mu, A, B) = self.lframe(col); K = comp(self.adj, col, self.L[(j + 1) % 5], al, mu)
        return {v: (mu if v in K and c == al else al if v in K and c == mu else c) for v, c in col.items()}
    def pos(self, col):
        j, ty, _ = self.lframe(col); return POS.get((ty, (self.q - j) % 5))
def trace(F, cyc):
    """cyc: list of colourings (dict vertex -> colour), in pi order. Returns the dump record (or an error)."""
    L = len(cyc); P = [F.pos(c) for c in cyc]
    if None in P: return dict(error='state with no universal-period position', positions=P)
    s = P.index(0); cyc = cyc[s:] + cyc[:s]; P = P[s:] + P[:s]
    if any(P[t] != t % 10 for t in range(L)): return dict(error='positions not 0..9 cyclic', positions=P)
    N = F.names; n = N; adj = F.adj
    col = dict(cyc[0]); cols, steps, J, k4p, pockets, K8, brk = [], [], [], [], [], [], dict(k4fail=[], k3fail=[], step8break=[])
    for t in range(L):
        if partition(col) != partition(cyc[t]): return dict(error='absolute replay diverged at step %d' % t)
        cols.append([col[v] for v in sorted(col)])
        cy, cz = col[n['y']], col[n['z']]
        J.append(None if cy == cz else n['z'] in comp(adj, col, n['y'], cy, cz))
        if t % 10 == 0:
            k4p.append(len(comp(adj, col, n['p'], col[n['p']], col[n['m']])))
            brk['k4fail'].append(not F.lockless(F.sigma(col)))
        if t % 10 == 2: brk['k3fail'].append(not F.lockless(F.sigma(col)))
        if t % 10 == 9:
            a, b = col[n['p']], col[n['m']]; sub = {v: (c if v not in (n['p'], n['xp']) else -1) for v, c in col.items()}
            Pk = comp(adj, sub, n['m'], a, b); pockets.append(dict(pos=t, pair=sorted((a, b)), vertices=sorted(Pk), reaches_wp=n['wp'] in Pk))
            brk['step8break'].append(J[-1] is False)
        pair, K = F.step(col)
        steps.append(dict(pos=t, pair=sorted(pair), K=sorted(K)))
        if t % 10 == 8: K8.append(dict(pos=t, pair=sorted(pair), vertices=sorted(K)))
        a, b = pair; col = {v: (b if v in K and c == a else a if v in K and c == b else c) for v, c in col.items()}
    if partition(col) != partition(cyc[0]): return dict(error='replay does not close')
    rho = {}
    for v in col: rho.setdefault(cyc[0][v], col[v])
    return dict(L=L, names=N, vertices=sorted(cyc[0]), colourings=cols, steps=steps, K8=K8, pockets=pockets, Kpm_at_k4=k4p, J=J, breaks=brk,
                closing_colour_map={str(a): b for a, b in sorted(rho.items())})
def census_job(args):
    from uv_lib import Hole
    lab, name, hole = args
    H = Hole(name, hole, lab.endswith('m')); adj = {v: set(r) for v, r in enumerate(H.rot) if v != hole}
    for v in adj: adj[v].discard(hole)
    F = Frame(adj, H.L, H.w); out = []
    for z in H.cycles:
        if not all(H.DL[x] for x in z): continue
        cyc = [{v: H.col(x, v) for v in H.sp.order} for x in z]
        r = trace(F, cyc); r.update(source='census', run=lab, name=name, hole=hole, orientation='mirror' if lab.endswith('m') else 'plantri'); out.append(r)
    return out
def construction_job(args):
    gname, hole, mirror = args
    import jobaq
    jobaq.GDIR = os.path.join(HERE, '../jobas/')
    E, adj0, link, w = jobaq.load(gname, hole, mirror)
    adj = {v: set(a) - {hole} for v, a in adj0.items() if v != hole}
    if sorted(len(adj0[x]) for x in link) != [5, 5, 5, 5, 6]: return []
    F = Frame(adj, link, w); rng = random.Random(1); done = set(); out = []
    for s0 in [E.randcol(rng) for _ in range(40)]:
        if s0 in done: continue
        mem = E.bfs(s0); done |= set(mem); pi = {x: E.pi_of(x)[0] for x in mem}; seen = set()
        for x in mem:
            if x in seen: continue
            z = []; y = x
            while y not in seen: seen.add(y); z.append(y); y = pi[y]
            if all(E.dl_info(u) is not None for u in z):
                r = trace(F, [dict(zip(E.order, u)) for u in z]); r.update(source='construction', name=gname, hole=hole, orientation='mirror' if mirror else 'plantri'); out.append(r)
    return out
if __name__ == '__main__':
    sys.path.insert(0, os.path.join(HERE, '../jobaq'))
    from jobag import canon
    holes = set()
    for lab in ['z25', 'z25m', 'z26', 'z26m', 'z27', 'z27m']:
        for l in open(os.path.join(HERE, '../out/%s.jsonl' % lab)):
            if '"jobs": {"pos": [{' not in l: continue
            r = json.loads(l)
            if canon(r['linkdeg']) == (5, 5, 5, 5, 6) and any(z['gamma'] for z in r['jobs']['pos']): holes.add((lab, r['name'], r['hole']))
    cons = sorted({(g, h, m) for g, h in [('A7f1', 22), ('A7f2', 22), ('A7f3', 34), ('A7f4', 22), ('walk-best-A7f1-1', 22), ('walk-best-A7f1-3', 22)] for m in (False, True)})
    with Pool(12) as P:
        res = [x for xs in P.map(census_job, sorted(holes)) for x in xs] + [x for xs in P.map(construction_job, cons) for x in xs]
    with open(os.path.join(HERE, 'jobav-cycles.jsonl'), 'w') as f:
        for r in res: f.write(json.dumps(r) + '\n')
    print('records', len(res), 'errors', Counter(r.get('error') for r in res if 'error' in r))
