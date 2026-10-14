"""Studio Job 6 (13 Oct 2026, exploratory): annealing flip walks over NON-4-colourable surface triangulations,
looking for a parity-clean Kempe class at a good hole (degree-5 h with T - h 4-colourable).  At a good hole no state
is filled, so a class with no lock-parity violator is a counterexample to surface-general LPC; by TrackF section 8.1
such a class consists only of all-DL pi-cycles.

Each step: a random edge flip (simplicial, min degree >= MINDEG).  The flip is kept only if T stays non-4-colourable
(exact SAT).  Score of T (lexicographic, larger is better):
   1. a parity-clean class at a good hole            -> 10^6 (counterexample; logged and the walk stops)
   2. all-DL pi-cycles at good holes (count)         x 1000
   3. longest DL pi-run at a good hole (maxDLrun)    x 30
   4. 1 - min violator fraction over classes          x 20
   5. number of good holes                            x 1
Metropolis acceptance at temperature TEMP.  Engine: TrackF kclass4 (unchanged).

usage: walk.py SURFACE SEED STEPS OUTPREFIX [--mindeg 5] [--n 12-36] [--seedfile out/existing_chi5.txt]
"""
import sys, os, json, random, subprocess, tempfile, argparse, math, time
import chilib, surfaces

K4 = os.path.join(chilib.TRACKF, 'src', 'kclass4')
CLS = 'cls2[size,filled,DL,unfilledNonDL,minKdeg,maxKdeg,lockParityViolations,onCycles,piPathEnds]'
CHI = {'torus': 0, 'klein': 0, 'rp2': 1, 'genus2': -2, 'rp2x3': -1}


def kclass(name, rot, holes):
    with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as f:
        f.write('%s %d %s\n' % (name, len(rot), ';'.join(','.join(map(str, r)) for r in rot))); fn = f.name
    out = subprocess.run([K4, fn, ','.join(map(str, holes))], capture_output=True, text=True, timeout=120).stdout
    os.unlink(fn)
    return [json.loads(l) for l in out.splitlines() if l.startswith('{')]


def evaluate(T, name, control=False):
    rot = chilib.rot_of(T.n, T.F); adj = chilib.adj_of_rot(rot)
    if control:   # power control (--control): T must stay 4-colourable; every degree-5 hole counts
        if chilib.colourable(adj, 4) is None: return None
        good = [h for h in range(len(rot)) if len(rot[h]) == 5]
    else:
        if chilib.colourable(adj, 4) is not None: return None
        good = chilib.good_holes(rot, adj)
    res = dict(name=name, n=T.n, good=good, cyc=0, maxrun=0, minviolfrac=1.0, clean=[], pid_bad=0, filled=0)
    if not good: return res, rot
    for r in kclass(name, rot, good):
        res['cyc'] += len(r['allDLcyc']); res['maxrun'] = max(res['maxrun'], r['maxDLrun']); res['pid_bad'] += sum(r['pid_bad'])
        for c in r[CLS]:
            res['filled'] += c[1]
            res['minviolfrac'] = min(res['minviolfrac'], c[6] / c[0])
            if c[6] == 0 and not control: res['clean'].append((r['hole'], c))
    return res, rot


def score(e):
    if e is None: return -1e9
    return (1e6 if e['clean'] else 0) + 1000 * e['cyc'] + 30 * e['maxrun'] + 20 * (1 - e['minviolfrac']) + len(e['good'])


def start(surface, rng, a):
    if a.control:   # random TrackF-style start (surfaces.make), checked 4-colourable
        while True:
            T = surfaces.make(surface, rng.randint(a.nmin, a.nmax), rng)
            if T is not None and T.mindeg() >= a.mindeg and chilib.colourable(chilib.adj_of_rot(chilib.rot_of(T.n, T.F)), 4) is not None:
                return T, 'control:make'
    """a non-4-colourable start: an existing chi>=5 graph of this surface (TrackF data) or a seed + growth"""
    def surf_of(nm):
        rest = nm.split('_', 1)[1]
        return next((x for x in ('rp2x3', 'genus2', 'klein', 'rp2', 'torus') if rest.startswith(x)), None)
    pool = [l for l in open(a.seedfile) if surf_of(l.split()[0]) == surface] if a.seedfile else []
    if pool and rng.random() < 0.7:
        name, rot = chilib.read_line(rng.choice(pool))
        F = set()
        for v, r in enumerate(rot):
            for i in range(len(r)): F.add(tuple(sorted((v, r[i], r[(i + 1) % len(r)]))))
        return surfaces.Tri(len(rot), sorted(F)), 'existing:' + name
    s = [x for x in chilib.seeds(rng) if x[0] == surface]
    sf, chi, n, F = rng.choice(s)
    target = rng.randint(a.nmin, a.nmax)
    T = surfaces.Tri(n, F)
    while T.n < target:            # grow: subdivide a face, then flip to raise the new vertex, keeping chi >= 5
        n2, F2 = surfaces.subdivide(T.n, list(T.F), rng); T = surfaces.Tri(n2, F2)
    for _ in range(4000):          # raise min degree while staying non-4-colourable
        if T.mindeg() >= a.mindeg: break
        low = [v for v in range(T.n) if T.deg(v) < a.mindeg]; v = rng.choice(low)
        lc = surfaces.link_cycle(T.F, v); k = rng.randrange(len(lc)); x, y = lc[k], lc[(k + 1) % len(lc)]
        if T.deg(x) - 1 < 4 or T.deg(y) - 1 < 4: continue
        old = list(T.F)
        if not T.flip(x, y, check=False): continue
        if chilib.colourable(chilib.adj_of_rot(chilib.rot_of(T.n, T.F)), 4) is not None: T.F = old; T.rebuild()
    return T, 'seed:%s' % sf


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('surface'); ap.add_argument('seed', type=int); ap.add_argument('steps', type=int); ap.add_argument('out')
    ap.add_argument('--mindeg', type=int, default=5); ap.add_argument('--nmin', type=int, default=12); ap.add_argument('--nmax', type=int, default=36)
    ap.add_argument('--seedfile', default='out/existing_chi5.txt'); ap.add_argument('--temp', type=float, default=3.0); ap.add_argument('--walklen', type=int, default=1500); ap.add_argument('--control', action='store_true')
    a = ap.parse_args()
    rng = random.Random(a.seed); chi = CHI[a.surface]
    log = open(a.out + '.jsonl', 'a'); t0 = time.time(); steps = 0; walk = 0
    while steps < a.steps:
        T, origin = start(a.surface, rng, a); walk += 1
        if T.mindeg() < a.mindeg or surfaces.validate(T.n, T.F, chi): continue
        name = '%s_s%d_w%d' % (a.surface, a.seed, walk)
        ev = evaluate(T, name, a.control); cur = score(ev[0] if ev else None); best = cur
        if ev is None: continue
        log.write(json.dumps(dict(kind='start', origin=origin, **{k: ev[0][k] for k in ('name', 'n', 'good', 'cyc', 'maxrun', 'minviolfrac')})) + '\n')
        for it in range(a.walklen):
            steps += 1
            a_, b_ = rng.choice(list(T.E.keys())); old = list(T.F)
            if not T.flip(a_, b_, a.mindeg): continue
            ev = evaluate(T, name, a.control)
            sc = score(ev[0] if ev else None)
            if sc >= cur or rng.random() < math.exp((sc - cur) / a.temp):
                cur = sc; e, rot = ev
                if e['clean'] or e['cyc'] or e['pid_bad'] or (e['filled'] and not a.control):
                    rec = dict(kind='event', step=it, **e, line='%s %d %s' % (name, T.n, ';'.join(','.join(map(str, r)) for r in rot)))
                    log.write(json.dumps(rec) + '\n'); log.flush()
                if sc > best:
                    best = sc
                    log.write(json.dumps(dict(kind='best', step=it, name=name, n=T.n, good=e['good'], cyc=e['cyc'], maxrun=e['maxrun'], minviolfrac=e['minviolfrac'],
                                              line='%s %d %s' % (name, T.n, ';'.join(','.join(map(str, r)) for r in rot)))) + '\n'); log.flush()
                if e['clean']:
                    print('PARITY-CLEAN CLASS', name, e['clean'], flush=True); break
                if a.control and e['cyc']:   # power control: time to the first all-DL pi-cycle, then next walk
                    log.write(json.dumps(dict(kind='hit', step=it, name=name, n=T.n, cyc=e['cyc'], sec=round(time.time() - t0))) + '\n'); log.flush(); break
            else:
                T.F = old; T.rebuild()
        log.write(json.dumps(dict(kind='end', name=name, best=best, steps=steps, sec=round(time.time() - t0))) + '\n'); log.flush()


if __name__ == '__main__':
    main()
