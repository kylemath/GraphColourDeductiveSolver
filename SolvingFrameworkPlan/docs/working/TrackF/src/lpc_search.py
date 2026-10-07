#!/usr/bin/env python3
"""Track F: adversarial flip walks against LPC.
Objective (maximise): if the graph has a targetless class at some degree-5 hole: 1 + max over targetless classes of
(fraction of its unfilled states obeying lock parity); else max over classes of (1 - filled/size) (pressure towards
targetless classes).  Moves: random edge flips keeping the triangulation simplicial and min degree >= 5 (order and
surface fixed).  Simulated annealing; every improvement and every LPC counterexample is logged.
usage: lpc_search.py SURFACE WALKS STEPS NMIN NMAX SEED OUTPREFIX"""
import sys, json, random, math, os, copy
sys.path.insert(0, os.path.dirname(__file__))
import surfaces, lpc_census

def objective(recs):
    tl, best, minv, cex, pid = lpc_census.score(recs)
    if tl: return 1.0 + best, tl, best, minv, cex
    m = 0.0
    for d in recs:
        for c in d[lpc_census.K]: m = max(m, 1 - c[1] / c[0])
    return m, 0, -1, None, []

if __name__ == '__main__':
    surf, walks, steps, nmin, nmax, seed, pref = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), sys.argv[7]
    rng = random.Random(seed); tmp = pref + '.tmp'; log = open(pref + '.log', 'a')
    overall = dict(surface=surf, walks=0, evals=0, best_obj=-1, best_frac=-1, cex=0, max_tl=0)
    for w in range(walks):
        T = None
        while T is None: T = surfaces.make(surf, rng.randint(nmin, nmax), rng)
        name = f"{surf}_s{seed}_w{w}"
        cur = objective(lpc_census.evaluate(surfaces.to_line(name, T.n, T.F), tmp)); overall['evals'] += 1
        best = cur; bestF = list(T.F); temp = 0.05
        for t in range(steps):
            F0 = list(T.F); a, b = rng.choice(list(T.E.keys()))
            if not T.flip(a, b, 5): continue
            if not any(T.deg(v) == 5 for v in range(T.n)): T.F = F0; T.rebuild(); continue
            new = objective(lpc_census.evaluate(surfaces.to_line(name, T.n, T.F), tmp)); overall['evals'] += 1
            if new[4]:
                line = surfaces.to_line(name + f"_t{t}", T.n, T.F)
                log.write(json.dumps({'LPC_COUNTEREXAMPLE': new[4], 'graph': line}) + '\n'); log.flush(); overall['cex'] += 1
                print('LPC COUNTEREXAMPLE', name, t, new[4], flush=True)
            if new[0] >= cur[0] or rng.random() < math.exp((new[0] - cur[0]) / temp):
                cur = new
                if new[0] > best[0]:
                    best = new; bestF = list(T.F)
                    log.write(json.dumps({'walk': w, 'step': t, 'obj': new[0], 'targetless': new[1], 'frac': new[2], 'minviol': new[3], 'graph': surfaces.to_line(name + '_best', T.n, T.F)}) + '\n'); log.flush()
            else:
                T.F = F0; T.rebuild()
            temp = max(0.005, temp * 0.995)
        overall['walks'] += 1; overall['best_obj'] = max(overall['best_obj'], best[0]); overall['best_frac'] = max(overall['best_frac'], best[2]); overall['max_tl'] = max(overall['max_tl'], best[1])
        print(json.dumps({'walk': w, 'n': T.n, 'best_obj': best[0], 'best_frac': best[2], 'tl': best[1]}), flush=True)
    print(json.dumps(overall), flush=True)
