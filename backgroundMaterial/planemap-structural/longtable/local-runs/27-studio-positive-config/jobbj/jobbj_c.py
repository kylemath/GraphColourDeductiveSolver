#!/usr/bin/env python3
"""Job BJ addendum (NightStatementC §4) [exploratory]: flip search minimising, over (5,5,5,5,6) Gamma-cycles Z at the hole (both orientations), the best sigma-target ratio
rho(Z) = max over sigma-images of -w(T) / w(Z) (picyc.bk --jobbk row field 8). rho < 1 kills statement (c). Score = -min_Z rho; hit = score > -1.
Seeds: p27#315977 h22, p26#75311 h19, p27#186395 h22 (census) + the Job BJ seed set (deduplicated AW hits + AS)."""
import sys, os, json, random, subprocess, tempfile
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__))
for d in ('../jobaw', '../jobas', '../jobuv'): sys.path.insert(0, os.path.join(HERE, d))
from jobaw import move, faces_of_rot
from flipsearch import rotation, canon
PICYC = os.path.join(HERE, '../picyc.bk')
def evaluate(F, hole):
    rot = rotation(F); line = 'g %d %s\n' % (len(rot), ';'.join(','.join(map(str, r)) for r in rot))
    with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as fh: fh.write(line); fn = fh.name
    vals = []; ok = True
    try:
        for m in ([], ['--mirror']):
            o = subprocess.run([PICYC, fn, '--jobbk', '--holes', str(hole)] + m, capture_output=True, text=True).stdout
            for l in o.splitlines():
                r = json.loads(l)
                if r.get('kind') != 'hole': continue
                if canon(r['linkdeg']) != (5, 5, 5, 5, 6): ok = False
                for row in r.get('jobbk', {}).get('pos', []):
                    if row[2]: vals.append(row[8] / row[0])
    finally: os.unlink(fn)
    return -min(vals) if ok and vals else None
def walk(args):
    name, F0, hole, w, steps = args
    rng = random.Random(104729 * w + 3); F = [tuple(t) for t in F0]; s = evaluate(F, hole)
    if s is None: return dict(seed=name, walk=w, error='seed has no (5,5,5,5,6) Gamma-cycle')
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
        if s2 > -1 and len(hits) < 5: hits.append(dict(it=it, score=s2, faces=[list(t) for t in G]))
    return dict(seed=name, hole=hole, walk=w, steps=steps, evaluations=nev, start=start, best=best, best_faces=[list(t) for t in bestF], log=log, hits=hits)
if __name__ == '__main__':
    from uv_lib import load
    seeds = [(n, faces_of_rot(load(n, False)), h) for n, h in (('p27#315977', 22), ('p26#75311', 19), ('p27#186395', 22))]
    V = json.load(open(os.path.join(HERE, '../jobaw/jobaw-verified.json'))); seen = set()
    for i, v in enumerate(V):
        k = (v['seed'], v['objective'], v['walk'])
        if k in seen: continue
        seen.add(k); d = json.load(open(os.path.join(HERE, '../jobbi/hitgraphs/best-hit%02d.json' % i))); seeds.append(('hit%02d' % i, d['faces'], d['hole']))
    for g, h in [('A7f1', 22), ('A7f2', 22), ('A7f3', 34), ('A7f4', 22), ('walk-best-A7f1-1', 22), ('walk-best-A7f1-3', 22)]:
        seeds.append((g, json.load(open(os.path.join(HERE, '../jobas/best-%s.json' % g)))['faces'], h))
    steps = int(sys.argv[1]) if len(sys.argv) > 1 else 600
    jobs = [(n, F, h, w, steps) for n, F, h in seeds for w in range(6)]
    with Pool(12) as P, open(os.path.join(HERE, 'jobbj-c-walks.jsonl'), 'w') as f:
        for r in P.imap_unordered(walk, jobs):
            f.write(json.dumps(r) + '\n'); f.flush(); print(r['seed'], r['walk'], 'start', r.get('start'), 'best', r.get('best'), 'hits', len(r.get('hits', [])), r.get('error', ''), flush=True)
