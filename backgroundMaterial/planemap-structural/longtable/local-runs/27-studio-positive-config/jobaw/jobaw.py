#!/usr/bin/env python3
"""Job AW [exploratory]: adversarial edge-flip hill-climb (Job AS machinery inverted). State = oriented face list; a move is an edge flip keeping the core class
(simple, min degree 5, max degree 8, no separating triangle: flipsearch.core_ok) AND keeping the hole's link pattern (5,5,5,5,6) AND a Gamma-cycle at the hole
(either orientation). Evaluator = ../picyc.n --jobm --jobn --holes h (full enumeration of T - h), plantri and mirror orientation.
Per Gamma-cycle (jobm sequence aligned to start at R3k4, blocks of 10 = periods; jobn rows give lockless and |K_{c(p),c(m)}(p)| at each k = 4 visit):
  A34: score = (max over consecutive period pairs of #k4 failures (2 = consecutive failures = A34' counterexample), min |K(p)| over that pair, #failing periods)
  W2s: score = (max over periods of [k2 fixed] + [k0 fixed] (2 = W2* counterexample), total k <= 2 fixed points)
  W3:  score = (max over periods of #fixed among k = 2, 1, 0 (3 = counterexample), total k <= 2 fixed points)
Walk: random valid flip; accept if score >= current, else with probability 0.15; hits (score[0] at its maximum) are saved.
usage: jobaw.py  (runs all seeds x objectives x 6 walks on a 12-process pool)"""
import sys, os, json, random, subprocess, tempfile, itertools
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../jobas')); sys.path.insert(0, os.path.join(HERE, '../jobuv'))
from flipsearch import rotation, core_ok, flip, canon
PICYC = os.path.join(HERE, '../picyc.n')
K = {1: 0, 2: 1, 4: 2, 8: 3, 16: 4}
def faces_of_rot(rot):
    F = set()
    for v, r in enumerate(rot):
        for i in range(len(r)):
            t = (v, r[(i + 1) % len(r)], r[i]); k = min(range(3), key=lambda s: t[s]); F.add(t[k:] + t[:k])
    return sorted(F)
def cycles(F, hole):
    rot = rotation(F); line = 'g %d %s\n' % (len(rot), ';'.join(','.join(map(str, r)) for r in rot))
    with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as fh: fh.write(line); fn = fh.name
    out = []
    try:
        for mir in (False, True):
            o = subprocess.run([PICYC, fn, '--jobm', '--jobn', '--holes', str(hole)] + (['--mirror'] if mir else []), capture_output=True, text=True).stdout
            for l in o.splitlines():
                r = json.loads(l)
                if r.get('kind') != 'hole' or canon(r.get('linkdeg', [0])) != (5, 5, 5, 5, 6): continue
                for seq, vis in zip(r.get('jobm', []), r.get('jobn', [])):
                    s0 = next((i for i, x in enumerate(seq) if x[0] == 3 and K[x[1]] == 4), None)
                    if s0 is None or len(seq) % 10: out.append(dict(bad=True, L=len(seq))); continue
                    kp = {row[0]: (row[2], row[10]) for row in vis if row[1] == 4}
                    P = len(seq) // 10; blocks = []
                    for b in range(P):
                        blk = [seq[(s0 + 10 * b + i) % len(seq)] for i in range(10)]
                        ex = {K[x[1]]: x[2] for x in blk if x[0] == 3}
                        i4 = (s0 + 10 * b) % len(seq)
                        blocks.append(dict(ex=ex, k4fail=ex[4] != 'L', k3fail=ex[3] != 'L', Kp=kp.get(i4, (None, None))[1]))
                    out.append(dict(mirror=mir, L=len(seq), blocks=blocks))
    finally: os.unlink(fn)
    return out
def score(cyc, obj):
    best = None
    for c in cyc:
        if c.get('bad'): continue
        B = c['blocks']; P = len(B); fixed = sum(1 for b in B for k in (0, 1, 2) if b['ex'][k] == 'X')
        if obj == 'A34':
            pairs = [(B[b]['k4fail'] + B[(b + 1) % P]['k4fail'], min(B[b]['Kp'] or 0, B[(b + 1) % P]['Kp'] or 0)) for b in range(P)] if P > 1 else [(int(B[0]['k4fail']), B[0]['Kp'] or 0)]
            s = max(pairs) + (sum(b['k4fail'] for b in B),)
        elif obj == 'W2s': s = (max((b['ex'][2] == 'X') + (b['ex'][0] == 'X') for b in B), fixed)
        else: s = (max(sum(b['ex'][k] == 'X' for k in (0, 1, 2)) for b in B), fixed)
        best = s if best is None or s > best else best
    return best
TOP = {'A34': 2, 'W2s': 2, 'W3': 3}
def move(F, hole, rng):
    """random flip avoiding the hole's star, then up to 3 repair flips raising a degree-4 vertex (flip an edge of its link); None if no core-class result"""
    es = sorted({(min(a, b), max(a, b)) for t in F for a, b in itertools.combinations(t, 2)})
    a, b = rng.choice(es)
    if hole in (a, b): return None
    if any(hole in t for t in F if a in t and b in t): return None
    G = flip(F, a, b)
    for _ in range(4):
        if G is None: return None
        deg = {}
        for t in G:
            for x in t: deg[x] = deg.get(x, 0) + 1     # each vertex appears in deg(v) faces
        low = [v for v, d in deg.items() if d < 5]
        if not low: return G if core_ok(G) else None
        v = rng.choice(low); opp = [tuple(x for x in t if x != v) for t in G if v in t]
        rng.shuffle(opp); H = None
        for c, d in opp:
            if hole in (c, d) or any(hole in t for t in G if c in t and d in t): continue
            H = flip(G, c, d)
            if H is not None: break
        G = H
    return None
def walk(args):
    seedname, F0, hole, obj, w, steps = args
    rng = random.Random(1000 * w + 7); F = [tuple(t) for t in F0]
    s = score(cycles(F, hole), obj); bests, bestF = s, F; log = [(0, s)]; hits = []; nev = 0
    def edges(F): return sorted({(min(a, b), max(a, b)) for t in F for a, b in itertools.combinations(t, 2)})
    for it in range(steps):
        G = None
        for _ in range(400):
            H = move(F, hole, rng)
            if H is None: continue
            cy = cycles(H, hole); nev += 1; s2 = score(cy, obj)
            if s2 is not None: G = H; break
        if G is None: break
        if s2 >= s or rng.random() < 0.15: F, s = G, s2
        if s2 > bests:
            bests, bestF = s2, G; log.append((it, s2))
        if s2[0] >= TOP[obj] and len(hits) < 5: hits.append(dict(it=it, score=s2, faces=[list(t) for t in G], cycles=cy))
    return dict(seed=seedname, hole=hole, objective=obj, walk=w, steps=steps, evaluations=nev, start=log[0][1], best=bests, best_faces=[list(t) for t in bestF],
                best_cycles=cycles(bestF, hole), log=log, hits=hits)
if __name__ == '__main__':
    from uv_lib import load
    seeds = []
    for gid, h in [('p25#16945', 3), ('p26#36087', 15), ('p26#38516', 20), ('p26#87942', 22), ('p27#146733', 20), ('p27#152697', 20), ('p27#186395', 22), ('p27#315977', 22)]:
        seeds.append((gid, faces_of_rot(load(gid, False)), h))
    for g, h in [('A7f1', 22), ('A7f2', 22), ('A7f3', 34), ('A7f4', 22), ('walk-best-A7f1-1', 22), ('walk-best-A7f1-3', 22)]:
        seeds.append((g, [tuple(t) for t in json.load(open(os.path.join(HERE, '../jobas/best-%s.json' % g)))['faces']], h))
    steps = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    jobs = [(sn, F, h, obj, w, steps) for sn, F, h in seeds for obj in ('A34', 'W2s', 'W3') for w in range(6)]
    with Pool(12) as P, open(os.path.join(HERE, 'jobaw-walks.jsonl'), 'w') as f:
        for r in P.imap_unordered(walk, jobs):
            f.write(json.dumps(r) + '\n'); f.flush()
            print(r['seed'], r['objective'], r['walk'], 'evals', r['evaluations'], 'start', r['start'], 'best', r['best'], 'hits', len(r['hits']), flush=True)
