"""Q1: numerical check of the disc Stokes formula
   12*S_a + 4*sum_{ring v, c(v)=a} t(v) = 3*E + 12*Psi_a(word)     for each colour a,
S_a = sum of spins of interior vertices of colour a, t(v)=fan turn (f-b) of ring vertex v,
E = sum over triangles of orientation sign, 12*Psi_a = sum_{b!=a} sgn(a,b,c,d) delta(c->d)."""
import sys, csv, random, collections
import numpy as np
from scipy.spatial import ConvexHull
sys.path.insert(0, '/mnt/project-files/multiscale/spin_windows')
from spinlib import *

def cap_disc(n, seed, z0):
    rng = np.random.default_rng(seed); p = rng.normal(size=(n, 3)); p /= np.linalg.norm(p, axis=1)[:, None]
    h = ConvexHull(p); T = [t for t in h.simplices.tolist() if all(p[x][2] > z0 for x in t)]
    ecount = collections.Counter()
    for a, b, c in T:
        for e in ((a, b), (b, c), (a, c)): ecount[tuple(sorted(e))] += 1
    bd = [e for e, k in ecount.items() if k == 1]
    V = set(x for t in T for x in t)
    if len(V) - len(ecount) + len(T) != 1: return None
    nb = collections.defaultdict(list)
    for a, b in bd: nb[a].append(b); nb[b].append(a)
    if any(len(v) != 2 for v in nb.values()): return None
    cyc = [bd[0][0]]; prev = None
    while True:
        x = cyc[-1]; nx_ = [y for y in nb[x] if y != prev][0]
        if nx_ == cyc[0]: break
        prev = x; cyc.append(nx_)
    if len(cyc) != len(nb): return None
    order = cyc + sorted(V - set(cyc)); idx = {v: i for i, v in enumerate(order)}
    adj = [set() for _ in order]
    for e in ecount:
        a, b = idx[e[0]], idx[e[1]]; adj[a].add(b); adj[b].add(a)
    return adj, len(cyc)

def check(adj, r, col, rot, succ, s):
    n = len(adj); S = [0] * 4; tau4 = [0] * 4
    for v in range(r, n): S[col[v]] += spin(col, rot, v)
    for v in range(r): tau4[col[v]] += fan_turn(col, rot, v)
    T = triangles(adj, rot, r); E = sum(orient_sign(col, rot, t) for t in T)
    assert len(T) == r + 2 * (n - r) - 2
    P = Psi12([col[v] for v in ring_word(succ, r)], s)
    lhs = [12 * S[a] + 4 * tau4[a] for a in range(4)]; rhs = [3 * E + P[a] for a in range(4)]
    # fan-turn constraints
    for v in range(r):
        k = len(rot[v]) - 1; t = fan_turn(col, rot, v); assert abs(t) <= k and (t - k) % 2 == 0
    return lhs == rhs, E, S

stats = collections.Counter(); Es = collections.Counter(); multiK = 0
for s in (1, -1):
    ok = 0; tot = 0
    for seed in range(4):
        d = cap_disc(600, seed, 0.3)
        if d is None: continue
        adj, r = d; rot, succ = embed_disc(adj, r)
        for c in sat_colourings(adj, k=5, seed=seed):
            g, E, S = check(adj, r, c, rot, succ, s); ok += g; tot += 1
    print('sign s=%+d: identity holds on %d/%d trial colourings' % (s, ok, tot))
S_SIGN = 1  # fixed below by the trial
res = {}
for s in (1, -1):
    good = True
    d = cap_disc(400, 99, 0.2); adj, r = d; rot, succ = embed_disc(adj, r)
    for c in sat_colourings(adj, k=3, seed=1): good &= check(adj, r, c, rot, succ, s)[0]
    res[s] = good
S_SIGN = [s for s in res if res[s]][0]
print('S_SIGN =', S_SIGN)

# large test: random caps
nd = 0; nc = 0; fails = 0; Ehist = collections.Counter(); same_ring_diffE = 0; same_ring_tests = 0
for seed in range(200):
    n = random.Random(seed).choice([200, 400, 800, 1500]); z0 = random.Random(seed + 7).uniform(-0.3, 0.7)
    d = cap_disc(n, 1000 + seed, z0)
    if d is None: continue
    adj, r = d; rot, succ = embed_disc(adj, r); nd += 1
    cols = sat_colourings(adj, k=4, seed=seed)
    for c in cols:
        g, E, S = check(adj, r, c, rot, succ, S_SIGN); nc += 1; fails += (not g)
        Ehist[E] += 1
    # fix the ring colouring of cols[0], resample interior: does E (the free integer) change?
    fixed = {v: cols[0][v] for v in range(r)}
    Eset = set()
    for c in sat_colourings(adj, fixed=fixed, k=6, seed=seed + 1):
        g, E, S = check(adj, r, c, rot, succ, S_SIGN); fails += (not g); nc += 1; Eset.add(E)
    same_ring_tests += 1; same_ring_diffE += (len(Eset) > 1)
print('random caps: discs %d, coloured discs %d, identity failures %d' % (nd, nc, fails))
print('rings where E varies across interior extensions: %d/%d' % (same_ring_diffE, same_ring_tests))

# windows from the dataset
rows = list(csv.DictReader(open('/mnt/project-files/explore/dataset/windows_judged.tsv'), delimiter='\t'))
random.Random(5).shuffle(rows); nw = nfail = nembfail = 0
for row in rows[:3000]:
    r, m = int(row['ring']), int(row['m'])
    adj = parse_window(r, m, row['ring_adj'], row['int_adj'])
    try: rot, succ = embed_disc(adj, r)
    except ValueError: nembfail += 1; continue
    degs_ok = all(len(adj[r + j]) == int(x) for j, x in enumerate(row['int_degrees'].split(',')))
    assert degs_ok
    for c in sat_colourings(adj, k=2, seed=nw):
        nw += 1; nfail += (not check(adj, r, c, rot, succ, S_SIGN)[0])
print('dataset windows: coloured windows %d, identity failures %d, embedding failures %d' % (nw, nfail, nembfail))
