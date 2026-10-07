#!/usr/bin/env python3
"""Track F: LPC falsification census on random surface triangulations (min degree 5).
For each graph: kclass2 at every degree-5 hole. Per Kempe class of T - h: size, #filled, #DL, #unfilled non-DL, #lock-parity violations.
LPC counterexample = a class with 0 filled states and 0 violations (every unfilled state obeys lock parity).
usage: lpc_census.py SURFACE COUNT NMIN NMAX SEED OUTPREFIX"""
import sys, json, random, subprocess, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
import surfaces
K = 'cls[size,filled,DL,unfilledNonDL,minKdeg,maxKdeg,lockParityViolations]'
KC = os.path.join(os.path.dirname(__file__), 'kclass2')

def evaluate(line, tmp):
    open(tmp, 'w').write(line + '\n')
    out = subprocess.run([KC, tmp, '5'], capture_output=True, text=True).stdout
    return [json.loads(l) for l in out.splitlines() if l.strip()]

def score(recs):
    """(#targetless, max obeying fraction among targetless classes, min #violations among targetless, #LPC counterexamples, pid_bad)"""
    tl = 0; best = -1.0; minv = None; cex = []; pid = 0
    for d in recs:
        pid += sum(d['pid_bad'])
        for c in d[K]:
            if c[1] == 0:
                tl += 1; u = c[2] + c[3]; fr = (u - c[6]) / u if u else 1.0
                best = max(best, fr); minv = c[6] if minv is None else min(minv, c[6])
                if c[6] == 0: cex.append((d['graph'], d['hole'], c))
    return tl, best, minv, cex, pid

if __name__ == '__main__':
    surf, count, nmin, nmax, seed, pref = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
    rng = random.Random(seed); tmp = pref + '.tmp'
    fo = open(pref + '.jsonl', 'w'); fg = open(pref + '.graphs.txt', 'w')
    agg = dict(graphs=0, holes=0, classes=0, targetless=0, best=-1.0, minviol=None, cex=0, pid_bad=0, dual_bad=0, unfilled_states=0)
    k = 0; tries = 0
    while k < count and tries < 20 * count:
        tries += 1
        T = surfaces.make(surf, rng.randint(nmin, nmax), rng)
        if T is None or not any(T.deg(v) == 5 for v in range(T.n)): continue
        name = f"{surf}_{seed}_{k}"; line = surfaces.to_line(name, T.n, T.F); k += 1
        recs = evaluate(line, tmp); tl, best, minv, cex, pid = score(recs)
        fg.write(line + '\n')
        for d in recs:
            fo.write(json.dumps(d) + '\n')
            agg['classes'] += d['classes']; agg['dual_bad'] += sum(d['dual_bad'])
            agg['unfilled_states'] += sum(c[2] + c[3] for c in d[K])
        agg['graphs'] += 1; agg['holes'] += len(recs); agg['targetless'] += tl; agg['best'] = max(agg['best'], best)
        if minv is not None: agg['minviol'] = minv if agg['minviol'] is None else min(agg['minviol'], minv)
        agg['cex'] += len(cex); agg['pid_bad'] += pid
        if cex: print('LPC COUNTEREXAMPLE', name, cex, flush=True)
    print(json.dumps({'surface': surf, 'nmin': nmin, 'nmax': nmax, 'seed': seed, **agg}), flush=True)
    os.unlink(tmp) if os.path.exists(tmp) else None
