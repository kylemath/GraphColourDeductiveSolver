#!/usr/bin/env python3
"""Track F: adversarial flip walks for all-DL pi-cycles on non-spherical surfaces (the only possible LPC counterexamples:
a targetless class with no lock-parity violator is a union of all-DL pi-cycles, LockParity.md section 5).
Objective (maximise): 1000 * #all-DL pi-cycles + max over degree-5 holes of the longest DL pi-run (kclass3 'maxDLrun').
With env LPC_OBJ=ratio, once a cycle exists the objective is 1000 + 1000 * max over classes containing cycles of
onCycles / (onCycles + pathEnds + filled), which is 1 exactly at an LPC counterexample.
Every graph with an all-DL pi-cycle is logged with the classes containing it ([onCycles, pathEnds, filled]); every LPC
counterexample (class with 0 filled states and 0 lock-parity violations) is logged separately.
usage: lpc_cycsearch.py SURFACE WALKS STEPS NMIN NMAX SEED OUTPREFIX"""
import sys, json, random, math, os, subprocess
sys.path.insert(0, os.path.dirname(__file__))
import surfaces
KC = os.path.join(os.path.dirname(__file__), 'kclass3')
K = 'cls[size,filled,DL,unfilledNonDL,minKdeg,maxKdeg,lockParityViolations]'
C = 'cycClasses[onCycles,pathEnds,filled]'
OBJ = os.environ.get('LPC_OBJ', 'count')
HOLES = os.environ.get('LPC_HOLES', 'all')   # 'no555': only degree-5 holes with no three consecutive degree-5 link vertices

def holes_of(line):
    rot = [r.split(',') for r in line.split()[2].split(';')]
    hs = []
    for h, r in enumerate(rot):
        if len(r) != 5: continue
        if HOLES == 'no555':
            d = [len(rot[int(x)]) == 5 for x in r]
            if any(d[i] and d[(i + 1) % 5] and d[(i + 2) % 5] for i in range(5)): continue
        hs.append(h)
    return hs

def evaluate(line, tmp):
    hs = holes_of(line)
    if not hs: return -1, 0, [], []
    open(tmp, 'w').write(line + '\n')
    out = subprocess.run([KC, tmp, ','.join(map(str, hs)) + ','], capture_output=True, text=True).stdout
    recs = [json.loads(l) for l in out.splitlines() if l.strip()]
    ncyc = sum(len(d['allDLcyc']) for d in recs); mr = max((d['maxDLrun'] for d in recs), default=0)
    cex = [(d['hole'], c) for d in recs for c in d[K] if c[1] == 0 and c[6] == 0]
    cyc = [(d['hole'], d['allDLcyc'], d[C]) for d in recs if d['allDLcyc']]
    if OBJ == 'ratio' and cyc:   # phase 2: push the cycle's Kempe class towards being all-cycle (LPC counterexample = ratio 1)
        r = max(c[0] / (c[0] + c[1] + c[2]) for d in recs for c in d[C])
        return 1000 + 1000 * r, mr, cyc, cex
    return 1000 * ncyc + mr, mr, cyc, cex

if __name__ == '__main__':
    surf, walks, steps, nmin, nmax, seed, pref = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), sys.argv[7]
    rng = random.Random(seed); tmp = pref + '.tmp'; log = open(pref + '.log', 'a')
    tot = dict(surface=surf, walks=0, evals=0, best_maxrun=0, cyc_graphs=0, cex=0)
    for w in range(walks):
        T = None
        while T is None:
            T = surfaces.make(surf, rng.randint(nmin, nmax), rng)
            if T is not None and not any(T.deg(v) == 5 for v in range(T.n)): T = None
        name = f"{surf}_c{seed}_w{w}"
        cur = evaluate(surfaces.to_line(name, T.n, T.F), tmp); tot['evals'] += 1; best = cur; temp = 1.0
        for t in range(steps):
            F0 = list(T.F); a, b = rng.choice(list(T.E.keys()))
            if not T.flip(a, b, 5): continue
            if not any(T.deg(v) == 5 for v in range(T.n)): T.F = F0; T.rebuild(); continue
            new = evaluate(surfaces.to_line(name, T.n, T.F), tmp); tot['evals'] += 1
            if new[2] or new[3]:
                line = surfaces.to_line(name + f"_t{t}", T.n, T.F)
                log.write(json.dumps({'ALLDL_CYCLE': new[2], 'LPC_COUNTEREXAMPLE': new[3], 'graph': line}) + '\n'); log.flush()
                tot['cyc_graphs'] += 1; tot['cex'] += len(new[3])
                if new[3]: print('LPC COUNTEREXAMPLE', name, t, new[3], flush=True)
            if new[0] >= cur[0] or rng.random() < math.exp((new[0] - cur[0]) / temp):
                cur = new
                if new[0] > best[0]:
                    best = new
                    log.write(json.dumps({'walk': w, 'step': t, 'maxrun': new[1], 'cyc': new[2], 'graph': surfaces.to_line(name + '_best', T.n, T.F)}) + '\n'); log.flush()
            else:
                T.F = F0; T.rebuild()
            temp = max(0.2, temp * 0.997)
        tot['walks'] += 1; tot['best_maxrun'] = max(tot['best_maxrun'], best[1])
        print(json.dumps({'walk': w, 'n': T.n, 'best_maxrun': best[1], 'best_cyc': len(best[2])}), flush=True)
    print(json.dumps(tot), flush=True)
    if os.path.exists(tmp): os.unlink(tmp)
