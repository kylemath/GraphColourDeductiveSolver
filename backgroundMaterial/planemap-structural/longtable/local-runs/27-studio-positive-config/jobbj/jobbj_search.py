#!/usr/bin/env python3
"""Job BJ (2) [exploratory]: Job AW flip-search machinery (jobaw.move: core-class flips + degree repair, hole star untouched, link pattern (5,5,5,5,6) kept) with the
objective turned onto the live statements. Evaluator: picyc.bj --jobbj --full --holes h, both orientations. Objectives (maximised; a hit = the statement is violated):
  U : max over orientations of the largest sum w over (sigma u sigma')-groups containing a positive cycle       (hit: > 0, SigmaUnionC false)
  ND: minus the min over Gamma-cycles of #states whose sigma-image is not DL (needs a Gamma-cycle)             (hit: 0, 'every Gamma-cycle has a non-DL sigma-image' false)
  FL: minus the min over Kempe classes of F/N                                                                  (hit: F/N < 1/4, the quarter floor false)
Seeds: one hit graph per distinct (seed, objective, walk) of Job AW, plus the 6 AS constructions."""
import sys, os, json, random, subprocess, tempfile
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__))
for d in ('../jobaw', '../jobas'): sys.path.insert(0, os.path.join(HERE, d))
from jobaw import move
from flipsearch import rotation, canon
PICYC = os.path.join(HERE, '../picyc.bj')
def evaluate(F, hole):
    rot = rotation(F); line = 'g %d %s\n' % (len(rot), ';'.join(','.join(map(str, r)) for r in rot))
    with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as fh: fh.write(line); fn = fh.name
    out = []
    try:
        for m in ([], ['--mirror']):
            o = subprocess.run([PICYC, fn, '--jobbj', '--full', '--holes', str(hole)] + m, capture_output=True, text=True).stdout
            for l in o.splitlines():
                r = json.loads(l)
                if r.get('kind') == 'hole' and 'jobbj' in r: out.append((canon(r['linkdeg']), r['jobbj']))
    finally: os.unlink(fn)
    return out
def score(ev, obj):
    if not ev or any(p != (5, 5, 5, 5, 6) for p, _ in ev): return None
    if obj == 'U': return max(b['U_max_sumw_posgroups'] for _, b in ev)
    if obj == 'ND':
        v = [b['gamma_min_nonDL_sigma'] for _, b in ev if b['gamma'] > 0]
        return -min(v) if v else None
    return -min(b['min_F_over_N'] for _, b in ev)
def hit(s, obj): return (obj == 'U' and s > 0) or (obj == 'ND' and s == 0) or (obj == 'FL' and s > -0.25)
def walk(args):
    name, F0, hole, obj, w, steps = args
    rng = random.Random(7919 * w + 13); F = [tuple(t) for t in F0]; s = score(evaluate(F, hole), obj)
    if s is None: return dict(seed=name, objective=obj, walk=w, error='seed invalid for objective')
    best, bestF, start, nev, hits, log = s, F, s, 0, [], [(0, s)]
    for it in range(steps):
        G = None
        for _ in range(400):
            H = move(F, hole, rng)
            if H is None: continue
            nev += 1; s2 = score(evaluate(H, hole), obj)
            if s2 is not None: G = H; break
        if G is None: break
        if s2 >= s or rng.random() < 0.15: F, s = G, s2
        if s2 > best: best, bestF = s2, G; log.append((it, s2))
        if hit(s2, obj) and len(hits) < 5: hits.append(dict(it=it, score=s2, faces=[list(t) for t in G]))
    return dict(seed=name, hole=hole, objective=obj, walk=w, steps=steps, evaluations=nev, start=start, best=best, best_faces=[list(t) for t in bestF], log=log, hits=hits)
if __name__ == '__main__':
    V = json.load(open(os.path.join(HERE, '../jobaw/jobaw-verified.json'))); seeds = []; seen = set()
    for i, v in enumerate(V):
        k = (v['seed'], v['objective'], v['walk'])
        if k in seen: continue
        seen.add(k); d = json.load(open(os.path.join(HERE, '../jobbi/hitgraphs/best-hit%02d.json' % i))); seeds.append(('hit%02d' % i, d['faces'], d['hole']))
    for g, h in [('A7f1', 22), ('A7f2', 22), ('A7f3', 34), ('A7f4', 22), ('walk-best-A7f1-1', 22), ('walk-best-A7f1-3', 22)]:
        seeds.append((g, json.load(open(os.path.join(HERE, '../jobas/best-%s.json' % g)))['faces'], h))
    steps = int(sys.argv[1]) if len(sys.argv) > 1 else 600
    jobs = [(n, F, h, obj, w, steps) for n, F, h in seeds for obj in ('U', 'ND', 'FL') for w in range(6)]
    print('seeds', len(seeds), 'walks', len(jobs), flush=True)
    with Pool(12) as P, open(os.path.join(HERE, 'jobbj-walks.jsonl'), 'w') as f:
        for r in P.imap_unordered(walk, jobs):
            f.write(json.dumps(r) + '\n'); f.flush()
            print(r['seed'], r['objective'], r['walk'], 'start', r.get('start'), 'best', r.get('best'), 'hits', len(r.get('hits', [])), r.get('error', ''), flush=True)
