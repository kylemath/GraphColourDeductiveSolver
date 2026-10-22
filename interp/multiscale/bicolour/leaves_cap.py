# Item 2: is "max bicoloured run <= k0 on every pocket walk" satisfiable on the leaf/pocket sets of intrinsic/leaves.py?
# Same disc generation as intrinsic/leaves.py (rng seed 3). For each disc and each level notion
# (none / intrinsic tau_int<=1 / Hodge pair T=1) report the least k0 in 2..8 that is SAT.
import sys, json, random, time, math, itertools
sys.path.insert(0, '/mnt/project-files/multiscale/intrinsic'); sys.path.insert(0, '/mnt/project-files/multiscale/hodge')
import ic
import importlib.util
spec = importlib.util.spec_from_file_location('hc', '/mnt/project-files/multiscale/hodge/hc.py'); hc = importlib.util.module_from_spec(spec); spec.loader.exec_module(hc)
from wk import Disc, G, build_tree
from lev import bfs
from e1_hier import make
from hier import check
OUT = open('/mnt/project-files/multiscale/bicolour/leaves_cap.jsonl', 'w')
rng = random.Random(3)
def maxrun(walk, col):
    m = len(walk); eq = [col[walk[i]] == col[walk[(i+2) % m]] for i in range(m)]
    if all(eq): return m
    best = 0; s = eq.index(False); cur = 0
    for j in range(1, m+1):
        if eq[(s+j) % m]: cur += 1; best = max(best, cur)
        else: cur = 0
    return best + 2
def add_cap(enc, W, k0):
    walk = W['walk']; m = len(walk)
    if m <= k0: return
    e = []
    for i in range(m):
        v = enc.new(); e.append(v); u, w = walk[i], walk[(i+2) % m]
        for c in range(4): enc.cls.append([-enc.x(u, c), -enc.x(w, c), v])
    for i in range(m):   # window of k0+1 consecutive vertices i..i+k0 is not bicoloured
        enc.cls.append([-e[(i+j) % m] for j in range(k0-1)])
def solve(D, k0, lev):
    enc = (hc.HEnc if lev == 'pair' else ic.Enc)(sorted(D.S))
    for u, w in D.edges: enc.neq(u, w)
    f = D.g.faces[next(iter(D.tris))]
    for j in range(3): enc.fix(f[j], j)
    for W in D.pockets:
        if lev == 'int': enc.walk_int(W, 1.0)
        elif lev == 'pair': enc.walk_pair(W, 1.0)
        add_cap(enc, W, k0)
    r = ic.solve(enc, budget=2*10**6)
    if r not in (None, 'UNK'):
        assert all(r[u] != r[w] for u, w in D.edges)
        assert max(maxrun(W['walk'], r) for W in D.pockets) <= k0
        if lev == 'int': assert all(ic.tau_int(W, r) <= 1+1e-9 for W in D.pockets)
        if lev == 'pair': assert all(hc.pair_ok(W, r, 1.0) for W in D.pockets)
    return r
def test(cls, name, D):
    rec = dict(cls=cls, map=name, n=len(D.S), pockets=len(D.pockets), m=[len(W['walk']) for W in D.pockets][:6], odd=[W['odd'] for W in D.pockets][:6])
    t0 = time.time()
    for lev in ('none', 'int', 'pair'):
        rec[lev] = None; rec[lev+'_unk'] = []
        for k0 in range(2, 9):
            r = solve(D, k0, lev)
            if r == 'UNK': rec[lev+'_unk'].append(k0); continue
            if r is not None: rec[lev] = k0; break
    rec['sec'] = round(time.time()-t0, 1)
    OUT.write(json.dumps(rec)+'\n'); OUT.flush(); print(rec, flush=True)
for name in ['ico10', 'ico20', 'flip10_1']:
    g = G(make(name)); poles = [v for v in range(g.n) if len(g.adj[v]) % 2]
    for k in range(6):
        c = rng.randrange(g.n); S = set(bfs(g.adj, c, rng.randint(3, 8)))
        if check(g, S)[0] in ('ok', 'chord'): test('ball', name, Disc(g, S))
    if name.startswith('ico'):
        P = sorted(poles)
        d0 = {p: bfs(g.adj, p) for p in P[:12]}
        pairs = sorted(((d0[p][q], p, q) for p in P for q in P if p < q))[:4]
        for dd, p, q in pairs:
            mid = min(range(g.n), key=lambda v: abs(d0[p][v]-d0[q][v])*10 + d0[p][v])
            for k in (1, 2, 3):
                S = set(bfs(g.adj, mid, dd//2 + k))
                if sum(1 for v in S if v in d0) == 2 and check(g, S)[0] != 'nodisc': test('cap2', name, Disc(g, S))
        for p in P[:3]:
            near = sorted(P, key=lambda q: d0[p][q])[1:3]
            for k in (1, 2):
                c = min(range(g.n), key=lambda v: max(d0[x][v] for x in [p] + near))
                r0 = max(d0[x][c] for x in [p] + near) + k
                S = set(bfs(g.adj, c, r0)); D = Disc(g, S)
                if sum(1 for v in S if v in d0 and v not in D.bset) == 3: test('vor3', name, D)
    if name == 'flip10_1':
        nodes = build_tree(g, L=40, seed=0)
        leaves = [nd for nd in nodes if not nd['kids']]
        for nd in rng.sample(leaves, min(40, len(leaves))): test('wleaf', name, Disc(g, nd['S']))
print('done')
