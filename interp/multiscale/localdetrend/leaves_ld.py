# Task 1b: leaves/pockets set of hodge/leaves_pair.py (same rng -> same discs): take the Hodge-pair colouring at T = 1
# (hc.sat_disc_pair) and evaluate tau_hodge / tau_strip / tau_step (and the odd step measure) on every pocket walk.
import sys, json, random, time, math, collections
sys.path.insert(0, '/mnt/project-files/multiscale/localdetrend/'); sys.path.insert(0, '/mnt/project-files/multiscale/hodge')
import ld, ic, hc
from wk import Disc, G, build_tree
from lev import bfs
from e1_hier import make
from hier import check
out = open('/mnt/project-files/multiscale/localdetrend/leaves_ld.jsonl', 'w'); rng = random.Random(3); T0 = time.time()
def test(cls, name, D):
    if time.time() - T0 > 200: return
    r = hc.sat_disc_pair(D, D.pockets, 1.0, budget=2*10**6)
    rec = dict(cls=cls, map=name, n=len(D.S), pockets=len(D.pockets), sat=r not in (None, 'UNK'))
    if rec['sat']:
        rec['vals'] = []
        for W in D.pockets:
            H = ld.walk_ic(W, r); m = ld.measures(H, W['odd']); rec['vals'].append(m)
    out.write(json.dumps(rec)+'\n'); out.flush()
for name in ['ico10', 'ico20', 'flip10_1']:
    g = G(make(name)); poles = [v for v in range(g.n) if len(g.adj[v]) % 2]
    for k in range(6):
        c = rng.randrange(g.n); S = set(bfs(g.adj, c, rng.randint(3, 8)))
        if check(g, S)[0] in ('ok', 'chord'): test('ball', name, Disc(g, S))
    if name.startswith('ico'):
        P = sorted(poles); d0 = {p: bfs(g.adj, p) for p in P[:12]}
        pairs = sorted(((d0[p][q], p, q) for p in P for q in P if p < q))[:4]
        for dd, p, q in pairs:
            mid = min(range(g.n), key=lambda v: abs(d0[p][v]-d0[q][v])*10 + d0[p][v])
            for k in (1, 2, 3):
                S = set(bfs(g.adj, mid, dd//2 + k))
                if sum(1 for v in S if v in d0) == 2 and check(g, S)[0] != 'nodisc': test('cap2', name, Disc(g, S))
        for p in P[:3]:
            near = sorted(P, key=lambda q: d0[p][q])[1:3]
            for k in (1, 2):
                c = min(range(g.n), key=lambda v: max(d0[x][v] for x in [p] + near)); r0 = max(d0[x][c] for x in [p] + near) + k
                S = set(bfs(g.adj, c, r0)); D = Disc(g, S)
                if sum(1 for v in S if v in d0 and v not in D.bset) == 3: test('vor3', name, D)
    if name == 'flip10_1':
        nodes = build_tree(g, L=40, seed=0); leaves = [nd for nd in nodes if not nd['kids']]
        for nd in rng.sample(leaves, min(40, len(leaves))): test('wleaf', name, Disc(g, nd['S']))
# summary
rows = [json.loads(l) for l in open('/mnt/project-files/multiscale/localdetrend/leaves_ld.jsonl')]
ev = [m for r in rows if r['sat'] for m in r['vals'] if not m['odd']]; od = [m for r in rows if r['sat'] for m in r['vals'] if m['odd']]
print('discs', len(rows), 'sat', sum(r['sat'] for r in rows), 'even walks', len(ev), 'odd walks', len(od))
print('even: step<=1', sum(m['step'] <= 1+1e-6 for m in ev), 'hodge<=1', sum(m['hodge'] <= 1+1e-6 for m in ev), 'strip<=1', sum(m['strip'] <= 1+1e-6 for m in ev), 'max step', max(m['step'] for m in ev), 'step<hodge', sum(m['step'] < m['hodge']-1e-6 for m in ev), 'step>hodge', sum(m['step'] > m['hodge']+1e-6 for m in ev), 't=2', sum(m['t'] > 1 for m in ev))
print('odd: fp<=1', sum(m['fp'] <= 1+1e-6 for m in od), 'step_odd<=1', sum(m['step'] <= 1+1e-6 for m in od), 'max', max(m['step'] for m in od))
