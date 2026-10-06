#!/usr/bin/env python3
"""studiointel sample_big.py -- [exploratory] configuration-free sampling at n = 56..64 (coordinator point 3).
For each seed IPR dual: a seeded random walk of W accepted flips that keep min degree >= 5, max degree <= 8, no separating triangle, and
no Birkhoff diamond / 2.122 (RSST #0, #1); then the exact radius (fast engine) at every degree-5 hole, in parallel.
usage: sample_big.py OUT.jsonl WORKERS WALK SEED pcfile:index ..."""
import sys, os, json, random
from multiprocessing import Pool
sys.path.insert(0, '.'); sys.path.insert(0, 'fast')
import graphs, radius, fast, ipr_run
import causal_test as CT
def walk(F, W, rng):
    cur = F; acc = 0; tries = 0
    while acc < W and tries < 50 * W:
        tries += 1
        es = sorted({(min(f[i], f[(i + 1) % 3]), max(f[i], f[(i + 1) % 3])) for f in cur for i in range(3)})
        a, b = es[rng.randrange(len(es))]; nf = graphs.flip(cur, a, b)
        if nf is None or not CT.legal(nf) or CT.occ(nf): continue
        cur = nf; acc += 1
    return cur, acc
def job(a):
    tag, F, h = a; r = fast.analyse(F, h); r.pop('witness', None); r.pop('targetless', None); return tag, h, r
if __name__ == '__main__':
    out, Wk, W, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    graphs_ = []
    for spec in sys.argv[5:]:
        pc, k = spec.rsplit(':', 1); F0 = ipr_run.read_pc(pc)[int(k)]
        F, acc = walk(F0, W, random.Random(seed + int(k))); tag = '%s:%s:walk%d:seed%d' % (pc.split('/')[-1], k, acc, seed)
        os.makedirs('bigsample', exist_ok=True); json.dump({'faces': [list(f) for f in F], 'source': tag}, open('bigsample/%s.json' % radius.graph_hash(F)[:16], 'w'))
        graphs_.append((tag, F, radius.graph_hash(F)[:16]))
    tasks = [(tag + '|' + hsh, F, h) for tag, F, hsh in graphs_ for h, d in sorted(graphs.degrees(F).items()) if d == 5]
    with Pool(Wk) as p, open(out, 'a') as fo:
        for tag, h, r in p.imap_unordered(job, tasks):
            fo.write(json.dumps({'graph': tag, 'hole': h, **r}) + '\n'); fo.flush()
            if r.get('rho') is None or (r.get('rho') or 0) >= 5: print('ALERT', tag, h, r.get('rho'), flush=True)
