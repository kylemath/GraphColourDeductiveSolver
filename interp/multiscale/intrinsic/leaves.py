# Step 2: smallest T in {1,1.5,...} with tau_int <= T satisfiable on every leaf/pocket class.
# Classes: E1-type chordless balls; weak-hierarchy leaves (all pockets, wk.build_tree L=40); two-vortex caps;
# 3-vortex balls; also T = sqrt3/2 for information.
import sys, json, random, collections, time, math
sys.path.insert(0, '/mnt/project-files/multiscale/intrinsic')
import ic
from wk import Disc, G, build_tree
from lev import bfs, multi_bfs
from e1_hier import make
from hier import check
out = open('/mnt/project-files/multiscale/intrinsic/leaves.jsonl', 'a')
rng = random.Random(3)
def test(cls, name, D):
    for T in (0.87, 1.0):
        t0 = time.time(); r = ic.sat_disc(D, D.pockets, T, dmax=2.0, budget=2*10**6)
        ok = r not in (None, 'UNK')
        rec = dict(cls=cls, map=name, n=len(D.S), pockets=len(D.pockets), chords=len(D.chords), odd=[W['odd'] for W in D.pockets][:5],
                   T=T, sat=('UNK' if r == 'UNK' else ok), sec=round(time.time()-t0, 1))
        if ok:
            rec['tau_int'] = round(max(ic.tau_int(W, r) for W in D.pockets), 3); rec['onelap'] = round(max(ic.tau_walk(W, r) for W in D.pockets), 3)
            rec['t'] = [round(math.sqrt(ic.n2(t)), 2) for t in (ic.tvec(W, r) for W in D.pockets) if t]
        out.write(json.dumps(rec)+'\n'); out.flush()
        if ok: break
for name in ['ico10', 'ico20', 'flip10_1']:
    g = G(make(name)); poles = [v for v in range(g.n) if len(g.adj[v]) % 2]
    for k in range(6):   # chordless balls
        c = rng.randrange(g.n); S = set(bfs(g.adj, c, rng.randint(3, 8)))
        if check(g, S)[0] in ('ok', 'chord'): test('ball', name, Disc(g, S))
    if name.startswith('ico'):
        P = sorted(poles)
        d0 = {p: bfs(g.adj, p) for p in P[:12]}
        pairs = sorted(((d0[p][q], p, q) for p in P for q in P if p < q))[:4]
        for dd, p, q in pairs:   # two-vortex caps: ball around the midpoint
            mid = min(range(g.n), key=lambda v: abs(d0[p][v]-d0[q][v])*10 + d0[p][v])
            for k in (1, 2, 3):
                S = set(bfs(g.adj, mid, dd//2 + k))
                if sum(1 for v in S if v in d0) == 2 and check(g, S)[0] != 'nodisc': test('cap2', name, Disc(g, S))
        for p in P[:3]:   # three-vortex balls
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
