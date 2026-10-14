"""Studio gluing run, 13 Oct 2026 (GLUING.md follow-up; exploratory adversarial search, Track A style).

Modes (one glued graph per task; tasks are sampled with a fixed seed, deduplicated by name):
  wideB   A = the three floor-tight seeds (p27#8475, p28#218651, p28#44900), every degree-5 u;
          B = all 19 frame graphs of orders 22-26 (Census29), random degree-5 u', random shift. Full evaluation.
  tight33 A = an order-33 census graph with a floor-tight hole h (eval-33 mf = 1/4); u = a degree-5 vertex at
          distance 2..3 from h; B as above. Evaluates the image of h only (as round2.py does).
  glue4   gluing along a separating 4-cycle: delete an edge xy of A and an edge x'y' of B (the two faces at each
          become a quadrilateral) and identify the two quadrilaterals (reversed order, shift 0..3). A from the 19
          small frame graphs or the tight seeds (edge at distance <= 3 from a tight hole), B from the 19. Full evaluation.
  aimpos  A = a glued graph of run-tight.jsonl with a positive-winding pi-cycle at hole h; u = a degree-5 vertex at
          distance 2..3 from h; B as above. Evaluates the image of h only, records the Kempe class of every positive
          cycle (picyc --full "pos[].class").
Every glued T passes TrackB's `frame` filter before evaluation (run_glue.evaluate).  Requires n <= 65 (picyc).

    python3 studio_wide.py MODE OUT.jsonl --limit N --workers W [--seed S]
"""
import sys, os, json, random, argparse, tempfile, subprocess, collections, gzip, time
from multiprocessing import Pool
from glue import glue, faces_of, line
from run_glue import read
sys.path.insert(0, os.path.expanduser('~/4square'))
from mapio import rot_from_faces, check_rot  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
W = '/Users/kylemathewson/GraphColourDeductiveSolver/SolvingFrameworkPlan/docs/working'
SMALL = [g for k in range(22, 27) for g in read('%s/Census29/out/frame-%d.txt' % (W, k))]
SEEDS = {'p27#8475': 27, 'p28#218651': 28, 'p28#44900': 28}


def seed_graphs():
    out = []
    for k in (27, 28):
        for l in open('%s/Census29/out/frame-%d.txt' % (W, k)):
            nm = l.split()[0]
            if nm in SEEDS:
                out.append(read_line(l))
    return out


def read_line(l):
    p = l.split()
    return (p[0], [[int(x) for x in r.split(',')] for r in p[2].split(';')])


def dist_from(rot, s):
    d = [-1] * len(rot); d[s] = 0; q = collections.deque([s])
    while q:
        x = q.popleft()
        for w in rot[x]:
            if d[w] < 0: d[w] = d[x] + 1; q.append(w)
    return d


def glue4(rotA, xy, rotB, xy2, shift=0):
    """Glue along a 4-cycle: remove edge xy from A (faces (x,y,a), (y,x,b)) and x'y' from B, identify the quadrilaterals
    y,a,x,b (the boundary order of the hole, as rot[u] for a vertex) with B's, reversed, rotated by shift (0..3)."""
    def hole(rot, x, y):
        i = rot[x].index(y); d = len(rot[x])
        a, b = rot[x][(i + 1) % d], rot[x][(i - 1) % d]  # faces (x, y, a) and (x, b, y)
        return [y, a, x, b], {tuple(sorted(f)) for f in ((x, y, a), (x, b, y))}
    CA, remA = hole(rotA, *xy); CB, remB = hole(rotB, *xy2)
    assert len(set(CA)) == 4 and len(set(CB)) == 4
    nA, nB = len(rotA), len(rotB)
    mapA = {x: x for x in range(nA)}; k = nA
    mapB = {y: CA[(shift - i) % 4] for i, y in enumerate(CB)}
    for y in range(nB):
        if y not in mapB: mapB[y] = k; k += 1
    F = [f for f in faces_of(rotA) if tuple(sorted(f)) not in remA]
    F += [tuple(mapB[x] for x in reversed(f)) for f in faces_of(rotB) if tuple(sorted(f)) not in remB]
    rot = rot_from_faces(F)
    assert check_rot(rot), 'glued map is not a sphere'
    return rot, mapA, mapB


def evaluate(name, rot, holes=None):
    with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as f:
        f.write(line(name, rot) + '\n'); fn = f.name
    fr = subprocess.run([os.path.join(HERE, 'frame')], input=open(fn).read(), capture_output=True, text=True)
    if not fr.stdout.strip():
        os.unlink(fn); return {'name': name, 'frame': False}
    P = subprocess.run(['nice', '-n', '10', os.path.join(HERE, 'picyc'), fn, '--full'] + (['--holes', ','.join(map(str, holes))] if holes else []),
                       capture_output=True, text=True)
    os.unlink(fn)
    hs = []
    for l in P.stdout.splitlines():
        r = json.loads(l)
        if r.get('kind') != 'hole': continue
        cls = r['clsig']; mfn = min(c[1] / c[0] for c in cls)
        hs.append({'h': r['hole'], 'ld': r['linkdeg'], 'S': r['states'], 'ncls': r['nclasses'], 'minFN': mfn,
                   'frozen': sum(1 for c in cls if c[1] == 0), 'npos': r['npos'], 'maxw': r['maxw'], 'sumw': r['sumw'],
                   'bad': r['cls_bad'] or r['f5_bad'] or r['cyc_split'], 'clsig': cls if mfn <= 0.26 else None,
                   'pos': [[p['w'], p['L'], p['class']['states'], p['class']['F'], p['class']['sumw'], p['class']['thmW']] for p in r.get('pos', [])]})
    return {'name': name, 'frame': True, 'n': len(rot), 'holes': hs, 'holesOnly': holes,
            'Rstar': (any(h['frozen'] == 0 for h in hs) if not holes else None),
            'minFN': min(h['minFN'] for h in hs) if hs else None, 'frozenHoles': sum(1 for h in hs if h['frozen']),
            'tight': sum(1 for h in hs if abs(h['minFN'] - 0.25) < 1e-9), 'stderr': P.stderr.strip()[-300:]}


def deg5(rot): return [u for u in range(len(rot)) if len(rot[u]) == 5]


def tasks(mode, rng, limit):
    T = []
    if mode == 'wideB':
        for na, ra in seed_graphs():
            for u in deg5(ra):
                for nb, rb in SMALL:
                    T.append(('v', na, ra, u, nb, rb, rng.choice(deg5(rb)), rng.randrange(5), None))
    elif mode == 'tight33':
        tight = []
        with gzip.open('%s/Census33/out/eval-33.jsonl.gz' % W, 'rt') as f:
            for l in f:
                r = json.loads(l)
                hs = [int(h) for h, v in r['holes'].items() if abs(v.get('mf', 1) - 0.25) < 1e-6]
                if hs: tight.append((r['name'], hs))
        rng.shuffle(tight); want = {nm for nm, _ in tight[:limit]}
        rots = {}
        for l in open('%s/Census33/out/frame-33.txt' % W):
            nm = l.split()[0]
            if nm in want: rots[nm] = read_line(l)[1]
        for nm, hs in tight[:limit]:
            ra = rots[nm]; h = rng.choice(hs); d = dist_from(ra, h)
            us = [u for u in deg5(ra) if 2 <= d[u] <= 3]
            if not us: continue
            nb, rb = rng.choice(SMALL)
            T.append(('v', nm, ra, rng.choice(us), nb, rb, rng.choice(deg5(rb)), rng.randrange(5), [h]))
    elif mode == 'glue4':
        seeds = seed_graphs(); tightH = {}
        for na, ra in seeds:  # tight holes of the seeds
            e = evaluate(na, ra); tightH[na] = [x['h'] for x in e['holes'] if abs(x['minFN'] - 0.25) < 1e-9]
        pool = SMALL + seeds
        for _ in range(limit * 3):
            na, ra = rng.choice(pool); nb, rb = rng.choice(SMALL)
            if na in tightH and tightH[na]:
                d = dist_from(ra, rng.choice(tightH[na]))
                es = [(x, y) for x in range(len(ra)) for y in ra[x] if x < y and max(d[x], d[y]) <= 3 and min(d[x], d[y]) >= 1]
            else:
                es = [(x, y) for x in range(len(ra)) for y in ra[x] if x < y]
            e1 = rng.choice(es); e2 = rng.choice([(x, y) for x in range(len(rb)) for y in rb[x] if x < y])
            T.append(('q', na, ra, e1, nb, rb, e2, rng.randrange(4), None))
    elif mode == 'aimpos':
        src = []
        for l in open(os.path.join(HERE, 'run-tight.jsonl')):
            r = json.loads(l)
            if not r.get('frame'): continue
            for h in r['holes']:
                if h['npos'] > 0: src.append((r['name'], [[int(x) for x in s.split(',')] for s in r['rot'].split(';')], h['h']))
        for _ in range(limit * 2):
            na, ra, h = rng.choice(src); d = dist_from(ra, h)
            us = [u for u in deg5(ra) if 2 <= d[u] <= 3]
            nb, rb = rng.choice(SMALL)
            T.append(('v', na, ra, rng.choice(us), nb, rb, rng.choice(deg5(rb)), rng.randrange(5), [h]))
    rng.shuffle(T); seen = set(); out = []
    for t in T:
        nm = '%s@%s+%s@%s/%s%d' % (t[1], t[3] if t[0] == 'v' else '%d-%d' % t[3], t[4], t[6] if t[0] == 'v' else '%d-%d' % t[6], 's' if t[0] == 'v' else 'q', t[7])
        if nm in seen: continue
        seen.add(nm); out.append((nm,) + t)
        if len(out) >= limit: break
    return out


def work(t):
    nm, kind, na, ra, u, nb, rb, u2, s, holes = t
    try:
        rot, mA, _ = (glue if kind == 'v' else glue4)(ra, u, rb, u2, s)
    except AssertionError as e:
        return {'name': nm, 'error': str(e)}
    if len(rot) > 65: return {'name': nm, 'error': 'n > 65'}
    t0 = time.time()
    r = evaluate(nm, rot, [mA[h] for h in holes] if holes else None)
    r['rot'] = ';'.join(','.join(map(str, x)) for x in rot); r['sec'] = round(time.time() - t0, 1)
    if holes: r['parentHoles'] = holes
    return r


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('mode'); ap.add_argument('out')
    ap.add_argument('--limit', type=int, default=100); ap.add_argument('--workers', type=int, default=2); ap.add_argument('--seed', type=int, default=13)
    a = ap.parse_args()
    done = set()
    if os.path.exists(a.out):
        done = {json.loads(l)['name'] for l in open(a.out)}
    T = [t for t in tasks(a.mode, random.Random(a.seed), a.limit) if t[0] not in done]
    print(a.mode, len(T), 'tasks', flush=True)
    with Pool(a.workers) as p, open(a.out, 'a') as out:
        for r in p.imap_unordered(work, T):
            out.write(json.dumps(r) + '\n'); out.flush()
            if r.get('frame'):
                print('%s n=%d minFN %.4f tight %d frozen %d npos %d %ss' % (r['name'], r['n'], r['minFN'] or -1, r['tight'], r['frozenHoles'],
                                                                       sum(h['npos'] for h in r['holes']), r['sec']), flush=True)
