#!/usr/bin/env python3
"""Track J task 3: adversarial flip search on SPHERES for near-rigid structure.
Flip walks over simplicial sphere triangulations (min degree 3; TrackF surfaces.py, read-only import), scored with the
C engine at every degree-5 hole:  score = max over holes of  Rrun + 3*Rcyc + 0.5*min(inshape_sigma_closed, 6),
Rrun = longest pi-run of DL states with N <= 9, Rcyc = a pi-cycle with N <= 9 throughout (near-rigid cycle; would be a
counterexample to the near-rigid cycle claim), inshape_sigma_closed = in-shape N = 9 states whose P1 swap partner is in-shape.
Also flags any near-rigid closed class (counterexample to near-rigid LPC).
usage: tj_sphsearch.py SEED WALKS STEPS OUT.jsonl GRAPHFILE [maxstates]"""
import sys, os, json, random, math, time, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'TrackF', 'src'))
import surfaces as S


def faces_from_rot(rot):
    F = set()
    for u in range(len(rot)):
        r = rot[u]; d = len(r)
        for t in range(d):
            a, b = r[t], r[(t + 1) % d]
            if b in rot[a] and u in rot[b] and a in rot[u]: F.add(tuple(sorted((u, a, b))))
    return sorted(F)


class Eng:
    def __init__(self, maxstates):
        self.p = subprocess.Popen([os.path.join(HERE, 'tj_eng'), '--allholes', '--maxstates', str(maxstates)],
                                  stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)

    def run(self, line, nh):
        self.p.stdin.write(line + '\n'); self.p.stdin.flush()
        return [json.loads(self.p.stdout.readline()) for _ in range(nh)]


def evaluate(T, eng, name):
    rot = [S.link_cycle(T.F, v) for v in range(T.n)]
    nh = sum(1 for r in rot if len(r) == 5)
    line = f"{name} {T.n} " + ';'.join(','.join(map(str, r)) for r in rot)
    if nh == 0: return -1, None, line
    res = eng.run(line, nh); best = -1; where = None
    for d in res:
        if 'err' in d: continue
        sc = d['Rrun'] + 3 * d['Rcyc'] + 0.5 * min(d['inshape_sigma_closed'], 6)
        nr = [c for c in d['cls'] if c[0] == c[3] and c[6] == 0]
        if nr: sc += 100
        if sc > best: best = sc; where = dict(hole=d['hole'], Rrun=d['Rrun'], Rcyc=d['Rcyc'], inshape=d['inshape'], isc=d['inshape_sigma_closed'], nrclass=len(nr), ncyc=d['ncyc'])
    return best, where, line


def main():
    seed, walks, steps, out, gf = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5]
    maxst = int(sys.argv[6]) if len(sys.argv) > 6 else 20000
    rng = random.Random(seed); fo = open(out, 'a'); eng = Eng(maxst)
    lines = [l for l in open(gf) if len(l.split()) >= 3]
    t0 = time.time(); tlim = float(os.environ.get('TJ_TLIM', '1e9')); gbest = -1; nev = 0
    for w in range(walks):
        if time.time() - t0 > tlim: break
        p = rng.choice(lines).split(); rot = [list(map(int, r.split(','))) for r in p[2].split(';')]
        T = S.Tri(len(rot), faces_from_rot(rot))
        cur, where, _ = evaluate(T, eng, 'x'); temp = 1.0; best = cur
        for s in range(steps):
            a, b = rng.choice(list(T.E.keys())); old = list(T.F)
            if not T.flip(a, b, mindeg=3): continue
            sc, wh, line = evaluate(T, eng, f"sp{seed}_{w}_{s}"); nev += 1
            if wh and (wh['Rrun'] >= 6 or wh['Rcyc'] or wh['nrclass'] or wh['isc'] >= 2):
                fo.write(json.dumps(dict(seed=seed, walk=w, step=s, score=sc, where=wh, valid=S.validate(T.n, T.F, int(os.environ.get('TJ_CHI', '2'))) is None, graph=line)) + '\n'); fo.flush()
                if wh['Rcyc'] or wh['nrclass']: print('NEAR-RIGID', json.dumps(wh), line[:200], flush=True)
            if sc >= cur or rng.random() < math.exp((sc - cur) / temp): cur = sc
            else: T.F = old; T.rebuild()
            best = max(best, cur); temp = max(0.1, temp * 0.995)
        gbest = max(gbest, best)
        print(json.dumps(dict(walk=w, base=p[0], best=best, nev=nev, secs=round(time.time() - t0))), flush=True)
    print('DONE', json.dumps(dict(seed=seed, nev=nev, best=gbest, secs=round(time.time() - t0))), flush=True)


if __name__ == '__main__':
    main()
