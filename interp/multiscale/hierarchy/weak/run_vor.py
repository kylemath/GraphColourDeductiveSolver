# W1 on hierarchies that ignore chords: Voronoi leaf cells (levelling/e4_recursion.voronoi_cells), balanced
# matching rounds of adjacent pairs whose union is a disc. pick='any' (smallest neighbour) or 'maxchord'
# (neighbour maximising internal chords of the union: adversarial). Usage: python run_vor.py name seed pick
import sys, json, time, random, collections, os
sys.path.insert(0, '/mnt/project-files/multiscale/hierarchy/weak'); sys.path.insert(0, '/mnt/project-files/multiscale/hierarchy')
sys.path.insert(0, '/mnt/project-files/multiscale/levelling')
from wk import *
from e1_hier import make
from e4_recursion import voronoi_cells
import hier
name, seed, pick = sys.argv[1], int(sys.argv[2]), sys.argv[3]
g = G(make(name)); rng = random.Random(seed); t0 = time.time()
cells = voronoi_cells(g, 3, rng)
assert all(check(g, c)[0] != 'nodisc' for c in cells)
col = {}; leaves = []
for c in cells:
    D = Disc(g, c); r = sat(D, D.pockets, 1.0, budget=None); leaves.append(dict(n=len(c), chords=len(D.chords), ok=r is not None))
    col.update(r if r else sat(D, [], 1.0, budget=None))
os.makedirs('logs', exist_ok=True); log = open('logs/vor_%s_s%d_%s.jsonl' % (name, seed, pick), 'w')
clusters = [set(c) for c in cells]; recs = []; level = 0
while sum(1 for c in clusters if c) > 2:
    level += 1; alive = [i for i, c in enumerate(clusters) if c]
    own = {v: i for i in alive for v in clusters[i]}
    nb = {i: set(own[w] for v in clusters[i] for w in g.adj[v] if own[w] != i) for i in alive}
    order = sorted(alive, key=lambda i: (len(clusters[i]), rng.random())); used = set(); merged = 0
    for i in order:
        if i in used or sum(1 for c in clusters if c) <= 2: continue
        cand = [j for j in nb[i] if j not in used]
        opts = []
        for j in cand:
            st = check(g, clusters[i] | clusters[j])
            if st[0] == 'nodisc': continue
            D = Disc(g, clusters[i] | clusters[j])
            opts.append(((-len(D.chords) if pick == 'maxchord' else 0, len(clusters[j]), rng.random()), j, D))
        if not opts: continue
        opts.sort(key=lambda t: t[0]); _, j, D = opts[0]
        rec = do_merge(g, D, clusters[i], clusters[j], col, dep=level); recs.append(rec)
        log.write(json.dumps(rec)+'\n'); log.flush()
        clusters[i] = clusters[i] | clusters[j]; clusters[j] = None; used |= {i, j}; merged += 1
    if not merged: print('stuck'); break
last = [c for c in clusters if c]; A, B = last[0], last[1]
E = set((u, w) for u in range(g.n) for w in g.adj[u] if u < w); best = None
for p in PERMS:
    cc = {v: col[v] for v in A}; cc.update({v: p[col[v]] for v in B})
    K = set(x for (u, w) in E if cc[u] == cc[w] for x in (u, w))
    if best is None or len(K) < len(best[0]): best = (K, cc)
K, cc = best
Rf, cf = proper_repair(g, set(range(g.n)), E, cc, K, 14) if K else (0, cc)
DA, DB = Disc(g, A), Disc(g, B)
ch = [r for r in recs if r['chords']]; cl = [r for r in recs if not r['chords']]
H = lambda rs, k: dict(sorted(collections.Counter(str(r[k]) for r in rs).items()))
summ = dict(name=name, seed=seed, pick=pick, n=g.n, merges=len(recs), chorded_merges=len(ch), R_final=Rf, nconf_final=len(K),
            sizes=[len(A), len(B)], chords_final=[len(DA.chords), len(DB.chords)], pockets_final=[len(DA.pockets), len(DB.pockets)],
            proper=cf is not None, R_chordless=H(cl, 'R'), R_chorded=H(ch, 'R'), w_chordless=H(cl, 'w'), w_chorded=H(ch, 'w'),
            max_chords=max(r['chords'] for r in recs), max_pockets=max(r['pockets'] for r in recs),
            fallbacks=collections.Counter(r['fallback'] for r in recs if r['fallback']),
            max_ptau_before=max(r['ptau_before'] for r in recs), max_strict_tau=max(r['strict_tau_after'] for r in recs),
            leaves=len(leaves), leaves_chorded=sum(l['chords'] > 0 for l in leaves), leaves_not_weak=sum(not l['ok'] for l in leaves), sec=round(time.time()-t0))
print(json.dumps(summ), flush=True); open('summary_vor.jsonl', 'a').write(json.dumps(summ)+'\n')
