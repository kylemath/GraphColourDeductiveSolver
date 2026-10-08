#!/usr/bin/env python3
"""Track F section 9 [exploratory]: annealing flip walks on non-spherical triangulations, aimed at LPC / LPC-1/4 at
FRAME-LIKE holes: degree-5 holes whose cyclic link-degree word has no three consecutive 5s and no consecutive 5,6,5.

Engine: kclass4 (= kclass_pi2.cpp; kclass_pi.cpp with per-class [onCycles, piPathEnds] appended), only frame-like holes.
Per class c = [size, filled, DL, single, minK, maxK, viol, onCycles, pathEnds]:
  cycle class      : onCycles > 0  (contains an all-DL pi-cycle)
  violator-free    : viol == 0 and size > filled (has unfilled states, all obey lock parity = D1, D2)
  LPC counterexample   : viol == 0 and filled == 0 (any class)
  LPC-1/4 counterexample: violator-free and filled/size < 1/4
Objective (maximise, lexicographic by tiers):
  no cycle class : maxDLrun + 2 * 1/(4*minFN)                 (minFN = min filled/size over violator-free classes; <= 2 + maxrun)
  cycle class    : 1000 + 300/(1+minviol) + 10*min(#cycle classes, 10) + 2/(4*minFN)
                   + 300 * 1/(4*minFNcyc) if some cycle class is violator-free (minFNcyc = its min filled/size)
i.e. (i) cycles at frame-like holes, then (ii) few violators in cycle classes, then (iii) low filled fraction.
Logs (OUT.jsonl, one JSON per line, deduplicated per walk by exact graph):
  {"ev":"cyc", ...}   every graph with a cycle class at a frame-like hole (graph line, per-hole word / cycles / classes)
  {"ev":"low", ...}   every graph with a violator-free class at a frame-like hole with filled/size <= 1/4 and size >= 8
                      (size-4 equality classes [4,1] are only counted: tot['eq4_evals'] = evaluations having one)
  {"ev":"cex", ...}   LPC or LPC-1/4 counterexample (also printed)
Progress: OUT.progress (JSON, rewritten after every walk).
usage: lpc2_search.py SURFACES(comma) WALKS STEPS NMIN NMAX SEED OUT [TIME_LIMIT_SECONDS]"""
import sys, json, random, math, os, subprocess, time, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import surfaces
KC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kclass4')
K2 = 'cls2[size,filled,DL,unfilledNonDL,minKdeg,maxKdeg,lockParityViolations,onCycles,piPathEnds]'
EVAL_TIMEOUT = float(os.environ.get('LPC2_EVAL_TIMEOUT', '90')); TIMEOUTS = [0]

def word(degs):
    best = None
    for s in (degs, degs[::-1]):
        for i in range(5):
            t = tuple(s[i:] + s[:i])
            if best is None or t < best: best = t
    return ('' if max(best) < 10 else ',').join(map(str, best))

def frame_like(degs):
    d = degs
    for i in range(5):
        a, b, c = d[i], d[(i + 1) % 5], d[(i + 2) % 5]
        if a == 5 and b == 5 and c == 5: return False
        if a == 5 and b == 6 and c == 5: return False
    return True

def frame_holes(rot):
    hs = []
    for h, r in enumerate(rot):
        if len(r) != 5: continue
        degs = [len(rot[x]) for x in r]
        if frame_like(degs): hs.append((h, word(degs)))
    return hs

def run_kc(line, holes, tmp, timeout=EVAL_TIMEOUT):
    open(tmp, 'w').write(line + '\n')
    try:
        out = subprocess.run([KC, tmp, ','.join(map(str, holes)) + ','], capture_output=True, text=True, timeout=timeout).stdout
    except subprocess.TimeoutExpired:
        TIMEOUTS[0] += 1; return None
    return [json.loads(l) for l in out.splitlines() if l.strip()]

def features(recs, words):
    f = dict(ncyccls=0, minviol=None, minFN=1.0, minFNcyc=None, maxrun=0, cex=[], cyc=[], low=[], states=0)
    for d in recs:
        h = d['hole']; f['maxrun'] = max(f['maxrun'], d['maxDLrun']); f['states'] += d['states']
        cyccls = [c for c in d[K2] if c[7] > 0]
        clean = [c for c in d[K2] if c[6] == 0 and c[0] > c[1]]
        for c in d[K2]:
            if c[6] == 0 and (c[1] == 0 or 4 * c[1] < c[0]): f['cex'].append(dict(hole=h, word=words[h], cls=c))
        for c in clean: f['minFN'] = min(f['minFN'], c[1] / c[0])
        lows = [c for c in clean if 4 * c[1] <= c[0]]
        f['nlow'] = f.get('nlow', 0) + len(lows); f['nlow4'] = f.get('nlow4', 0) + sum(1 for c in lows if c[0] == 4)
        lows = [c for c in lows if c[0] >= 8 or 4 * c[1] < c[0]]   # log only non-trivial equality classes (size >= 8) and breaks
        if lows: f['low'].append(dict(hole=h, word=words[h], cls=lows))
        if cyccls:
            f['ncyccls'] += len(cyccls)
            mv = min(c[6] for c in cyccls); f['minviol'] = mv if f['minviol'] is None else min(f['minviol'], mv)
            for c in cyccls:
                if c[6] == 0:
                    r = c[1] / c[0]; f['minFNcyc'] = r if f['minFNcyc'] is None else min(f['minFNcyc'], r)
            f['cyc'].append(dict(hole=h, word=words[h], allDLcyc=d['allDLcyc'], cyccls=cyccls, states=d['states'],
                                 minFNclean=min((c[1] / c[0] for c in clean), default=None)))
    return f

def score(f):
    base = 2.0 / (4 * max(f['minFN'], 1e-9))
    if not f['ncyccls']: return f['maxrun'] + base
    s = 1000 + 300.0 / (1 + f['minviol']) + 10 * min(f['ncyccls'], 10) + base
    if f['minFNcyc'] is not None: s += 300.0 / (4 * max(f['minFNcyc'], 1e-9))
    return s

def evaluate(T, name, tmp):
    line = surfaces.to_line(name, T.n, T.F)
    rot = [list(map(int, r.split(','))) for r in line.split()[2].split(';')]
    hw = frame_holes(rot)
    if not hw: return None, line
    recs = run_kc(line, [h for h, _ in hw], tmp)
    if recs is None: return None, line
    f = features(recs, dict(hw)); f['nholes'] = len(hw)
    return f, line

# ---- seeded walks (env LPC2_SEEDS=file of graph lines; LPC2_GLUE=1: seeds are spherical and each walk starts from the
# connected sum of a random seed with a small triangulation of the walk's surface, glued at the face farthest from the
# seed's frame-like cycle holes, so the hole neighbourhood is untouched; without LPC2_GLUE the seed line is used as is and
# its surface is taken from the name prefix)
SEEDS = [l.strip() for l in open(os.environ['LPC2_SEEDS'])] if os.environ.get('LPC2_SEEDS') else []
CHI = dict(torus=0, klein=0, rp2=1, genus2=-2, rp2x3=-1, sphere=2)

PIECES = {}
def colourable(n, F, tmp):
    line = surfaces.to_line('piece', n, F); open(tmp, 'w').write(line + '\n')
    out = subprocess.run([KC, tmp, 'none'], capture_output=True, text=True, timeout=60).stdout
    return json.loads(out.splitlines()[0])['states'] > 0

def piece(surf, rng, tmp):
    """a small 4-colourable min-degree-5 triangulation of surf (pool of 6 per surface, n = 9..15)"""
    pool = PIECES.setdefault(surf, [])
    while len(pool) < 6:
        T = surfaces.make(surf, rng.randint(9, 15), rng)
        if T is not None and colourable(T.n, T.F, tmp): pool.append((T.n, list(T.F)))
    return rng.choice(pool)

def faces_of(rot):
    F = set()
    for v, r in enumerate(rot):
        for i in range(len(r)): F.add(frozenset((v, r[i], r[(i + 1) % len(r)])))
    return [tuple(sorted(f)) for f in F]

def seeded(surf, rng, tmp):
    line = rng.choice(SEEDS); rot = [list(map(int, r.split(','))) for r in line.split()[2].split(';')]; n = len(rot)
    F = faces_of(rot)
    if not os.environ.get('LPC2_GLUE'):
        T = surfaces.Tri(n, F); T.seed = line.split()[0]; return T
    toks = dict(t.split('=', 1) for t in line.split()[3:] if '=' in t)
    holes = list(map(int, toks['holes'].split(','))) if 'holes' in toks else [h for h, _ in frame_holes(rot)]
    dist = {h: 0 for h in holes}; q = list(holes)
    for u in q:
        for w in rot[u]:
            if w not in dist: dist[w] = dist[u] + 1; q.append(w)
    far = max(dist.get(min(f, key=lambda v: dist.get(v, 0)), 0) for f in F)
    f1 = rng.choice([f for f in F if min(dist.get(v, 0) for v in f) == far])
    n2, F2 = piece(surf, rng, tmp + '.piece'); f2 = rng.choice(F2); perm = list(f1); rng.shuffle(perm)
    m = {f2[i]: perm[i] for i in range(3)}; nxt = n
    for v in range(n2):
        if v not in m: m[v] = nxt; nxt += 1
    FF = [f for f in F if f != f1] + [tuple(m[v] for v in f) for f in F2 if tuple(f) != tuple(f2)]
    if surfaces.validate(nxt, FF, CHI[surf]) is not None or surfaces.orientable(FF) != (surf in ('torus', 'genus2')): return None
    T = surfaces.Tri(nxt, FF)
    if T.mindeg() < 5: return None
    T.seed = line.split()[0]; return T

def ghash(T):
    return hashlib.md5(repr(sorted(T.E.keys())).encode()).hexdigest()[:16]

if __name__ == '__main__':
    surfs = sys.argv[1].split(','); walks, steps, nmin, nmax, seed = map(int, sys.argv[2:7]); out = sys.argv[7]
    tlim = float(sys.argv[8]) if len(sys.argv) > 8 else 1e18
    rng = random.Random(seed); tmp = out + '.tmp'; log = open(out + '.jsonl', 'a'); t0 = time.time()
    tot = dict(surfaces=surfs, seed=seed, nrange=[nmin, nmax], walks=0, evals=0, timeouts=0, cyc_graphs=0, low_graphs=0, cex=0,
               best_minviol=None, best_minFNcyc=None, best_minFN=1.0, by_surface={})
    def prog():
        tot['elapsed'] = round(time.time() - t0); tot['timeouts'] = TIMEOUTS[0]; open(out + '.progress', 'w').write(json.dumps(tot) + '\n')
    def record(f, T, w, t, surf, bs, name, seen):
        gh = ghash(T)
        if gh not in seen and (f['cyc'] or f['low'] or f['cex']):
            seen.add(gh); gl = surfaces.to_line(f"{name}_t{t}", T.n, T.F)
            base = dict(surface=surf, n=T.n, walk=w, step=t, seed=getattr(T, 'seed', None), graph=gl)
            if f['cyc']:
                log.write(json.dumps(dict(ev='cyc', cyc=f['cyc'], **base)) + '\n'); tot['cyc_graphs'] += 1; bs['cyc_graphs'] += 1
            if f['low']:
                log.write(json.dumps(dict(ev='low', low=f['low'], **base)) + '\n'); tot['low_graphs'] += 1; bs['low_graphs'] += 1
            if f['cex']:
                log.write(json.dumps(dict(ev='cex', cex=f['cex'], **base)) + '\n'); tot['cex'] += len(f['cex'])
                print('COUNTEREXAMPLE?', surf, gl.split()[0], f['cex'], flush=True)
            log.flush()
        if f['minviol'] is not None and (tot['best_minviol'] is None or f['minviol'] < tot['best_minviol']): tot['best_minviol'] = f['minviol']
        if f['minFNcyc'] is not None and (tot['best_minFNcyc'] is None or f['minFNcyc'] < tot['best_minFNcyc']): tot['best_minFNcyc'] = f['minFNcyc']
        tot['best_minFN'] = min(tot['best_minFN'], f['minFN']); tot['eq4_evals'] = tot.get('eq4_evals', 0) + (f.get('nlow4', 0) > 0)
    for w in range(walks):
        if time.time() - t0 > tlim: break
        surf = surfs[w % len(surfs)]; cur = None
        for attempt in range(20):
            T = seeded(surf, rng, tmp) if SEEDS else surfaces.make(surf, rng.randint(nmin, nmax), rng)
            if T is None: continue
            if SEEDS and not os.environ.get('LPC2_GLUE'): surf = T.seed.split('_')[0]
            name = f"{surf}_s{seed}_w{w}"
            bs = tot['by_surface'].setdefault(surf, dict(walks=0, evals=0, cyc_graphs=0, low_graphs=0))
            f, line = evaluate(T, name, tmp); tot['evals'] += 1; bs['evals'] += 1
            if f is not None: cur = f; break
        if cur is None: continue
        seen = set(); record(cur, T, w, -1, surf, bs, name, seen)
        cs = score(cur); best = cs; temp = 1.0
        for t in range(steps):
            if time.time() - t0 > tlim: break
            F0 = list(T.F); a, b = rng.choice(list(T.E.keys()))
            if not T.flip(a, b, 5): continue
            f, line = evaluate(T, name, tmp); tot['evals'] += 1; bs['evals'] += 1
            if f is None:
                T.F = F0; T.rebuild(); continue
            record(f, T, w, t, surf, bs, name, seen)
            ns = score(f)
            if ns >= cs or rng.random() < math.exp((ns - cs) / temp):
                cs = ns; best = max(best, ns)
            else:
                T.F = F0; T.rebuild()
            temp = max(0.2, temp * 0.997)
        tot['walks'] += 1; bs['walks'] += 1
        print(json.dumps(dict(walk=w, surface=surf, n=T.n, seed=getattr(T, 'seed', None), best=round(best, 2), elapsed=round(time.time() - t0))), flush=True)
        prog()
    prog(); print(json.dumps(tot), flush=True)
    if os.path.exists(tmp): os.unlink(tmp)
