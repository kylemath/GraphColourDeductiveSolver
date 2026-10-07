#!/usr/bin/env python3
"""Job BQ (2) [exploratory]: flip search (Job AW machinery) minimising the restricted B' slack: min over sigma u sigma' groups CONTAINING A POSITIVE CYCLE of
2 N0 + E2 + 3 tau - 2|R_rho| (picyc.bq --jobbq min_slack_posgroups), at the seed hole, both orientations. Hit = negative slack (sigmaUnionC_of_budget_pos fails).
Score = -min slack. Seeds: the 12 Job BV (c)-hit graphs, the 16 deduplicated AW hits, the 6 AS constructions. Graphs must keep a positive cycle at the hole."""
import sys, os, json, random, subprocess, tempfile
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__))
for d in ('../jobaw', '../jobas'): sys.path.insert(0, os.path.join(HERE, d))
from jobaw import move
from flipsearch import rotation
PICYC = os.path.join(HERE, '../picyc.bq'); BIG = 1 << 39
def evaluate(F, hole):
    rot = rotation(F); line = 'g %d %s\n' % (len(rot), ';'.join(','.join(map(str, r)) for r in rot))
    with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as fh: fh.write(line); fn = fh.name
    v = []
    try:
        for m in ([], ['--mirror']):
            o = subprocess.run([PICYC, fn, '--jobbq', '--holes', str(hole)] + m, capture_output=True, text=True).stdout
            for l in o.splitlines():
                r = json.loads(l)
                if r.get('kind') == 'hole' and 'jobbq' in r and r['jobbq']['min_slack_posgroups'] < BIG: v.append(r['jobbq']['min_slack_posgroups'])
    finally: os.unlink(fn)
    return -min(v) if v else None
def walk(args):
    name, F0, hole, w, steps = args
    rng = random.Random(15485863 * w + 11); F = [tuple(t) for t in F0]; s = evaluate(F, hole)
    if s is None: return dict(seed=name, walk=w, error='no positive group at the hole')
    best, bestF, start, nev, hits, log = s, F, s, 0, [], [(0, s)]
    for it in range(steps):
        G = None
        for _ in range(400):
            H = move(F, hole, rng)
            if H is None: continue
            nev += 1; s2 = evaluate(H, hole)
            if s2 is not None: G = H; break
        if G is None: break
        if s2 >= s or rng.random() < 0.15: F, s = G, s2
        if s2 > best: best, bestF = s2, G; log.append((it, s2))
        if s2 > 0 and len(hits) < 5: hits.append(dict(it=it, score=s2, faces=[list(t) for t in G]))
    return dict(seed=name, hole=hole, walk=w, steps=steps, evaluations=nev, start=start, best=best, best_faces=[list(t) for t in bestF], log=log, hits=hits)
if __name__ == '__main__':
    seeds = []
    for g, h, *_ in json.load(open(os.path.join(HERE, '../jobbj/chits/list.json'))): seeds.append((g, json.load(open(os.path.join(HERE, '../jobbj/chits/best-%s.json' % g)))['faces'], h))
    V = json.load(open(os.path.join(HERE, '../jobaw/jobaw-verified.json'))); seen = set()
    for i, v in enumerate(V):
        k = (v['seed'], v['objective'], v['walk'])
        if k in seen: continue
        seen.add(k); d = json.load(open(os.path.join(HERE, '../jobbi/hitgraphs/best-hit%02d.json' % i))); seeds.append(('hit%02d' % i, d['faces'], d['hole']))
    for g, h in [('A7f1', 22), ('A7f2', 22), ('A7f3', 34), ('A7f4', 22), ('walk-best-A7f1-1', 22), ('walk-best-A7f1-3', 22)]:
        seeds.append((g, json.load(open(os.path.join(HERE, '../jobas/best-%s.json' % g)))['faces'], h))
    steps = int(sys.argv[1]) if len(sys.argv) > 1 else 600
    jobs = [(n, F, h, w, steps) for n, F, h in seeds for w in range(4)]
    with Pool(10) as P, open(os.path.join(HERE, 'jobbq-walks.jsonl'), 'w') as f:
        for r in P.imap_unordered(walk, jobs):
            f.write(json.dumps(r) + '\n'); f.flush(); print(r['seed'], r['walk'], 'start', r.get('start'), 'best', r.get('best'), 'hits', len(r.get('hits', [])), r.get('error', ''), flush=True)
