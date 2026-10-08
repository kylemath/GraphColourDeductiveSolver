#!/usr/bin/env python3
"""Track H: falsification search for Conjecture RI (rigid isolation) on the SPHERE.
Flip walks on simplicial sphere triangulations (min degree 3), starting from plantri24 graphs.  Score of a graph =
- min over all degree-5 holes and all rigid DL states c of def(pi(c)), where def(d) = sum of (component counts of d in
its own frame) - (1,1,2,1,2,1) if d is DL, else 10 + that sum.  def = 0 would be a counterexample to RI.
Logs every graph reaching def <= 1 and every counterexample.
usage: th_risearch.py SEED WALKS STEPS OUT.jsonl GRAPHFILE"""
import sys, os, json, random, math, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'TrackF', 'src'))
import surfaces as S
from th_engine import Hole
from th_rigidscan_lib import counts

RIG = [1, 1, 2, 1, 2, 1]

def faces_from_rot(rot):
    F = set()
    for u in range(len(rot)):
        r = rot[u]; d = len(r)
        for t in range(d):
            a, b = r[t], r[(t + 1) % d]
            if b in rot[a] and u in rot[b] and a in rot[u]: F.add(tuple(sorted((u, a, b))))
    return sorted(F)

def evaluate(T, maxstates=6000):
    rot = [S.link_cycle(T.F, v) for v in range(T.n)]
    best = 99; where = None
    for h in [v for v in range(T.n) if len(rot[v]) == 5]:
        H = Hole(rot, h)
        if len(H.states) > maxstates: continue
        cache = {}
        def info(i):
            if i not in cache:
                r, col = H.analyse_state(i)
                cache[i] = (r, counts(H, col, r['roles']) if r['kind'] != 'F' else None)
            return cache[i]
        for i in range(len(H.states)):
            r, cs = info(i)
            if r['kind'] != 'DL' or cs != RIG or r['pi'] is None: continue
            r2, cs2 = info(r['pi'])
            if cs2 is None: continue
            d = sum(a - b for a, b in zip(cs2, RIG)) + (0 if r2['kind'] == 'DL' else 10)
            if d < best: best = d; where = (h, i, r['pi'], cs2, r2['kind'])
    return best, where, rot

def main():
    seed, walks, steps, out, gf = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5]
    rng = random.Random(seed); fo = open(out, 'a')
    lines = [l for l in open(gf) if l.strip()]
    t0 = time.time()
    for w in range(walks):
        p = rng.choice(lines).split(); rot = [list(map(int, r.split(','))) for r in p[2].split(';')]
        T = S.Tri(len(rot), faces_from_rot(rot))
        cur, where, _ = evaluate(T); temp = 1.0; best = cur
        for s in range(steps):
            a, b = rng.choice(list(T.E.keys())); old = list(T.F)
            if not T.flip(a, b, mindeg=3): continue
            sc, wh, rr = evaluate(T)
            if sc <= 1:
                rec = dict(seed=seed, walk=w, step=s, deficiency=sc, where=wh, valid=S.validate(T.n, T.F, 2) is None,
                           graph=f"ri{seed}_{w}_{s} {T.n} " + ';'.join(','.join(map(str, r)) for r in rr))
                fo.write(json.dumps(rec) + '\n'); fo.flush()
                if sc == 0: print('RI COUNTEREXAMPLE', json.dumps(rec)[:300], flush=True)
            if sc <= cur or rng.random() < math.exp(-(sc - cur) / temp): cur = sc
            else: T.F = old; T.rebuild()
            best = min(best, cur); temp = max(0.1, temp * 0.995)
        print(json.dumps(dict(walk=w, base=p[0], best=best, secs=round(time.time() - t0))), flush=True)

if __name__ == '__main__':
    main()
