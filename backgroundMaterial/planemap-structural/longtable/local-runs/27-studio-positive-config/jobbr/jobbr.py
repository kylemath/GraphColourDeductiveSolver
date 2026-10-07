#!/usr/bin/env python3
"""Job BR [exploratory]: flip search (Job AW machinery: core-class flips + degree repair, hole star untouched) at a (6,6,6,6,6) hole, keeping the hole's link all degree 6.
Objective: maximise the longest maximal DL run along pi at the hole (picyc.bo --jobbo --nocls, both orientations); a hit = an all-DL pi-cycle (G66^0 counterexample).
Score = (number of all-DL cycles, longest DL run). Seeds: IPR fullerene duals C60-C80 (one pentagon hole each), plus census graphs with a 66666 hole if any."""
import sys, os, json, random, subprocess, tempfile
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__))
for d in ('../jobaw', '../jobas', '../jobuv'): sys.path.insert(0, os.path.join(HERE, d))
from jobaw import move, faces_of_rot
from flipsearch import rotation
PICYC = os.path.join(HERE, '../picyc.bo')
def evaluate(F, hole):
    rot = rotation(F); line = 'g %d %s\n' % (len(rot), ';'.join(','.join(map(str, r)) for r in rot))
    with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as fh: fh.write(line); fn = fh.name
    sc = None
    try:
        for m in ([], ['--mirror']):
            o = subprocess.run([PICYC, fn, '--jobbo', '--nocls', '--holes', str(hole)] + m, capture_output=True, text=True).stdout
            for l in o.splitlines():
                r = json.loads(l)
                if r.get('kind') != 'hole': continue
                if r.get('pattern') != '6,6,6,6,6' or 'jobbo' not in r: return None
                s = (len(r['jobbo']['all_DL_cycles']), r['jobbo']['maxrun']); sc = s if sc is None or s > sc else sc
    finally: os.unlink(fn)
    return sc
def walk(args):
    name, F0, hole, w, steps = args
    rng = random.Random(32452843 * w + 5); F = [tuple(t) for t in F0]; s = evaluate(F, hole)
    if s is None: return dict(seed=name, walk=w, error='seed hole not 66666')
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
        if s2[0] > 0 and len(hits) < 5: hits.append(dict(it=it, score=s2, faces=[list(t) for t in G]))
    return dict(seed=name, hole=hole, walk=w, steps=steps, evaluations=nev, start=start, best=best, best_faces=[list(t) for t in bestF], log=log, hits=hits)
if __name__ == '__main__':
    seeds = []
    for l in open(os.path.join(HERE, '../in-ipr.txt')):
        name, n, r = l.split(' ', 2)
        if int(n) > 42: continue
        rot = [[int(x) for x in s.split(',')] for s in r.strip().split(';')]
        h = next(v for v in range(len(rot)) if len(rot[v]) == 5); seeds.append((name, faces_of_rot(rot), h))
    steps = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    jobs = [(n, F, h, w, steps) for n, F, h in seeds for w in range(4)]
    print('seeds', len(seeds), 'walks', len(jobs), flush=True)
    with Pool(int(sys.argv[2]) if len(sys.argv) > 2 else 4) as P, open(os.path.join(HERE, 'jobbr-walks.jsonl'), 'w') as f:
        for r in P.imap_unordered(walk, jobs):
            f.write(json.dumps(r) + '\n'); f.flush(); print(r['seed'], r['walk'], 'start', r.get('start'), 'best', r.get('best'), 'hits', len(r.get('hits', [])), r.get('error', ''), flush=True)
