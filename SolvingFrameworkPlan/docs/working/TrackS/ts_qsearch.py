#!/usr/bin/env python3
"""Track S: adversarial flip search on SPHERES for Q-cycles (all-DL pi-cycles with F13 connected, i.e. P2 = (2,1), at every
state) of low H-level, in particular Q-cycles through rigid states (counterexamples to Q-escape; an R-cycle would refute NRC).
Engine: TrackJ C engine tj_eng --allholes --dump (read-only); flips: TrackF surfaces.py (read-only).
Per hole: Q-cycles with their min k(H) (= #P1 - 1), and the longest pi-run inside Q that contains a rigid state.
score = max over holes of  qr + 4*[Q-cycle] + 6*[Q-cycle with min kH <= 2] + 100*[Q-cycle through a rigid state]
usage: ts_qsearch.py SEED WALKS STEPS OUT.jsonl GRAPHFILE[,GRAPHFILE...] [maxstates]"""
import sys, os, json, random, math, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'TrackF', 'src'))
sys.path.insert(0, os.path.join(HERE, '..', 'TrackJ'))
import surfaces as S
from tj_lib import Engine
from tj_sphsearch import faces_from_rot


def hole_stats(sts):
    by = {s['i']: s for s in sts}
    Q = lambda s: s['kind'] == 1 and s['c6'][2] + s['c6'][3] == 3
    rig = lambda s: s['kind'] == 1 and s['N'] == 8
    # Q-cycles
    on = set(); qcyc = []
    for s in sts:
        if not Q(s) or s['i'] in on: continue
        path = []; pos = {}; k = s['i']
        while k >= 0 and Q(by[k]) and k not in pos and k not in on:
            pos[k] = len(path); path.append(k); k = by[k]['pi']
        on.update(path)
        if k >= 0 and k in pos:
            c = path[pos[k]:]; qcyc.append(min(by[x]['c6'][0] + by[x]['c6'][1] - 1 for x in c))
    # longest Q-run containing a rigid state
    pre = set(by[s['i']]['pi'] for s in sts if Q(s) and s['pi'] >= 0 and Q(by[s['pi']]))
    qr = 0
    for s in sts:
        if not Q(s) or s['i'] in pre: continue
        k = s['i']; L = 0; hasr = False; seen = set()
        while k >= 0 and Q(by[k]) and k not in seen:
            seen.add(k); L += 1; hasr |= rig(by[k]); k = by[k]['pi']
        if hasr: qr = max(qr, L)
    return qcyc, qr


ENG = {}


def evaluate(T, name, maxst):
    rot = [S.link_cycle(T.F, v) for v in range(T.n)]
    holes = [h for h in range(T.n) if len(rot[h]) == 5]
    line = f"{name} {T.n} " + ';'.join(','.join(map(str, r)) for r in rot)
    best = -1; where = None
    if not holes: return best, where, line
    if 'e' not in ENG: ENG['e'] = Engine(dump=True, allholes=True, maxstates=maxst)
    for js, sts in ENG['e'].run(line, len(holes)):
        if sts is None: continue
        h = js.get('hole')
        qcyc, qr = hole_stats(sts)
        sc = qr + 4 * bool(qcyc) + 6 * any(m <= 2 for m in qcyc) + 100 * any(m <= 1 for m in qcyc)
        if sc > best: best = sc; where = dict(hole=h, qr=qr, qcyc=qcyc)
    return best, where, line


def main():
    seed, walks, steps, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    gfs = sys.argv[5].split(','); maxst = int(sys.argv[6]) if len(sys.argv) > 6 else 30000
    rng = random.Random(seed); fo = open(out, 'a')
    lines = [l for gf in gfs for l in open(gf) if len(l.split()) >= 3]
    t0 = time.time(); tlim = float(os.environ.get('TS_TLIM', '1e9')); nev = 0
    for w in range(walks):
        if time.time() - t0 > tlim: break
        p = rng.choice(lines).split(); rot = [list(map(int, r.split(','))) for r in p[2].split(';')]
        T = S.Tri(len(rot), faces_from_rot(rot))
        cur, where, _ = evaluate(T, 'x', maxst); temp = 2.0; best = cur
        for s in range(steps):
            if time.time() - t0 > tlim: break
            a, b = rng.choice(list(T.E.keys())); old = list(T.F)
            if not T.flip(a, b, mindeg=4): continue
            if T.n > 40: T.F = old; T.rebuild(); continue
            sc, wh, line = evaluate(T, f"qs{seed}_{w}_{s}", maxst); nev += 1
            if wh and (wh['qcyc'] or wh['qr'] >= 7):
                fo.write(json.dumps(dict(seed=seed, walk=w, step=s, score=sc, where=wh,
                                         valid=S.validate(T.n, T.F, 2) is None, graph=line)) + '\n'); fo.flush()
                if any(m <= 1 for m in wh['qcyc']): print('Q-ESCAPE FAILS', json.dumps(wh), line[:200], flush=True)
            if sc >= cur or rng.random() < math.exp((sc - cur) / temp): cur = sc
            else: T.F = old; T.rebuild()
            best = max(best, cur); temp = max(0.2, temp * 0.99)
        print(json.dumps(dict(walk=w, base=p[0], best=best, nev=nev, secs=round(time.time() - t0))), flush=True)
    print('DONE', json.dumps(dict(seed=seed, nev=nev, secs=round(time.time() - t0))), flush=True)


if __name__ == '__main__':
    main()
