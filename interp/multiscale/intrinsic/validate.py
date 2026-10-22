# Step 1: validate the SAT encoding of tau_int <= T against the brute-force evaluator on small discs.
# For each small disc: enumerate ALL proper colourings (first triangle fixed), and for each colouring and each
# threshold T check  SAT(colouring fixed, tau_int <= T on every pocket)  ==  [max_pocket tau_int(colouring) <= T].
# Also: SAT existence (free colouring) == brute-force existence.
import sys, random, json, collections, itertools, time
sys.path.insert(0, '/mnt/project-files/multiscale/intrinsic')
from ic import *
from wk import Disc, G
from lev import bfs
from e1_hier import make
from hier import check

def colourings(D, cap=3000):
    V = sorted(D.S); adj = {v: [w for w in D.g.adj[v] if w in D.S] for v in V}
    f = D.g.faces[next(iter(D.tris))]; col = {f[0]: 0, f[1]: 1, f[2]: 2}
    order = [v for v in V if v not in col]; out = []
    def rec(i):
        if len(out) >= cap: return
        if i == len(order): out.append(dict(col)); return
        v = order[i]
        for c in range(4):
            if all(col.get(w) != c for w in adj[v]): col[v] = c; rec(i+1); del col[v]
    rec(0); return out

def discs(g, rng, k):
    out = []; tries = 0
    while len(out) < k and tries < 5000:
        tries += 1
        c = rng.randrange(g.n); S = set(bfs(g.adj, c, 1))
        tgt = rng.randint(7, 13)
        while len(S) < tgt:
            fr = [w for v in S for w in g.adj[v] if w not in S]; S.add(rng.choice(fr))
        if check(g, S)[0] != 'ok': continue
        D = Disc(g, S)
        if not any(not W['odd'] for W in D.pockets): continue
        out.append(D)
    return out

if __name__ == '__main__':
    rng = random.Random(1); Ts = [0.5, 0.87, 1.0, 1.32, 1.5, 1.74, 2.0, 2.5, 3.0]
    stats = collections.Counter(); t0 = time.time(); tvals = collections.Counter()
    for name in ['flip10_1', 'BASE_defect_ico17', 'BASE_rand22']:
        g = G(make(name)); Ds = discs(g, rng, 25)
        for D in Ds:
            cols = colourings(D, cap=400)
            for col in cols:
                ti = max(tau_int(W, col) for W in D.pockets)
                for W in D.pockets:
                    t = tvec(W, col)
                    if t: tvals[(round(math.sqrt(n2(t)), 2), round(tau_int(W, col), 2))] += 1
                for T in rng.sample(Ts, 3):
                    r = sat_disc(D, D.pockets, T, fixed=col)
                    sat = r not in (None, 'UNK'); truth = ti <= T + 1e-9
                    stats['agree' if sat == truth else 'DISAGREE'] += 1
                    if sat != truth: print('DISAGREE', name, len(D.S), T, ti, [tau_int(W, col) for W in D.pockets], flush=True)
            for T in [0.87, 1.0, 1.5]:
                bf = any(max(tau_int(W, c) for W in D.pockets) <= T + 1e-9 for c in cols)
                r = sat_disc(D, D.pockets, T); sat = r not in (None, 'UNK')
                if len(cols) < 400: stats['exist_' + ('agree' if bf == sat else 'DISAGREE')] += 1
                if sat: assert max(tau_int(W, r) for W in D.pockets) <= T + 1e-9
        print(name, dict(stats), round(time.time()-t0), flush=True)
    print('t!=0 walks seen (|t|, tau_int):', sorted(tvals.items())[:40])
    json.dump(dict(stats=dict(stats), tvals=[[list(k), v] for k, v in tvals.items()]), open('/mnt/project-files/multiscale/intrinsic/validate.json', 'w'))
