#!/usr/bin/env python3
"""Track H: LPC on HIGHER-GENUS triangulated surfaces (genuine simplicial surfaces: every vertex link one cycle).
Motivation: the general-graph LPC counterexamples (th_gsearch_lp) have the edge density of a genus ~5 surface and
consist of 'rigid' states (pair-graph component counts (1,1,2,1,2,1)); on a surface of Euler characteristic chi a
rigid state needs cycle rank 2 - chi in each partition, so rigid classes are only possible for chi << 2.
Start: a Track H seed surface with a pi-cycle hole h, connected-summed with G copies of the 9-vertex torus torus(3,3) far
from h; then a flip walk (simplicial flips, min degree 3, never touching the star of h) scored by kclass4 at h:
min filled F over cycle classes, then (F = 0) min pi-path ends, then (both 0) min lock-parity violations.
Events: 'cexCF' (cycle class with F = 0), 'cexLPC' (F = 0 and no path ends), re-validated as simplicial surfaces.
usage: th_hgsearch.py SEED WALKS STEPS OUTPREFIX SEEDFILE GMIN GMAX"""
import sys, os, json, random, math, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'TrackF', 'src'))
import surfaces as S
from th_gsearch import evaluate

K7 = S.torus(3, 3)   # 9-vertex 6-regular torus (4-colourable; K7 itself is not 4-colourable)

def faces_from_rot(rot):
    F = set()
    for u in range(len(rot)):
        r = rot[u]; d = len(r)
        for t in range(d):
            a, b = r[t], r[(t + 1) % d]
            if b in rot[a] and u in rot[b] and a in rot[u]: F.add(tuple(sorted((u, a, b))))
    return sorted(F)

def dist_from(adj, h):
    d = {h: 0}; fr = [h]
    while fr:
        nx = []
        for u in fr:
            for w in adj[u]:
                if w not in d: d[w] = d[u] + 1; nx.append(w)
        fr = nx
    return d

def csum_far(n, F, h, rng):
    """connected sum with K7 along a face of the base far from h; base labels are kept (new vertices appended)."""
    adj = {v: set() for v in range(n)}
    for a, b, c in F: adj[a] |= {b, c}; adj[b] |= {a, c}; adj[c] |= {a, b}
    d = dist_from(adj, h); far = max(min(d[v] for v in f) for f in F)
    f1 = rng.choice([f for f in F if min(d[v] for v in f) >= max(2, far - 1)])
    n2, F2 = K7; f2 = rng.choice(F2)
    m = {f2[0]: f1[0], f2[1]: f1[1], f2[2]: f1[2]}; k = n
    for v in range(n2):
        if v not in m: m[v] = k; k += 1
    Fn = [f for f in F if f != f1] + [tuple(m[v] for v in f) for f in F2 if f != f2]
    return k, Fn

def line_of(T, h, name):
    rot = [S.link_cycle(T.F, v) for v in range(T.n)]
    return f"{name} {T.n} " + ';'.join(','.join(map(str, r)) for r in rot), rot

def score(r):
    if r is None or r.get('states', 0) == 0: return -1e9, None
    cls = r['cls2[size,filled,DL,unfilledNonDL,minKdeg,maxKdeg,lockParityViolations,onCycles,piPathEnds]']
    cyc = [c for c in cls if c[7] > 0]
    if cyc:
        b = min(cyc, key=lambda c: (c[1], c[8], c[6], c[0]))
        return (1000 + 500.0 / (1 + b[1]) + (300.0 / (1 + b[8]) if b[1] == 0 else 0)
                + (300.0 / (1 + b[6]) if b[1] == 0 and b[8] == 0 else 0) - 0.002 * b[0]), cyc
    return r['maxDLrun'] + 0.0, None

def main():
    seed, walks, steps, pref, sf, gmin, gmax = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5], int(sys.argv[6]), int(sys.argv[7])
    rng = random.Random(seed); tmp = pref + '.tmp'; log = open(pref + '.jsonl', 'a')
    seeds = []
    for l in open(sf):
        p = l.split()
        if len(p) >= 4: seeds.append((p[0], [list(map(int, r.split(','))) for r in p[2].split(';')], int(p[3])))
    t0 = time.time(); nev = 0
    for w in range(walks):
        nm, rot, h = seeds[w % len(seeds)]; n = len(rot); F = faces_from_rot(rot)
        chi0 = n - sum(len(r) for r in rot) // 2 + len(F)
        g = rng.randint(gmin, gmax)
        for _ in range(g): n, F = csum_far(n, F, h, rng)
        chi = chi0 - 2 * g
        assert S.validate(n, F, chi) is None, S.validate(n, F, chi)
        T = S.Tri(n, F); star = set(rot[h]) | {h}
        def ev(T):
            line, rr = line_of(T, h, 'x')
            adj = [list(r) for r in rr]
            return evaluate(adj, T.n, tmp, h), line
        r, _ = ev(T); cur = score(r)[0]; temp = 3.0
        for s in range(steps):
            a, b = rng.choice(list(T.E.keys()))
            if a in star and b in star: continue
            if h in (a, b): continue
            old = list(T.F)
            if not T.flip(a, b, mindeg=3): continue
            if S.link_cycle(T.F, h) is None or len(S.link_cycle(T.F, h)) != 5: T.F = old; T.rebuild(); continue
            r, line = ev(T); nev += 1
            if r is None: T.F = old; T.rebuild(); continue
            sc, cyc = score(r)
            if r.get('states', 0) > 80000: sc -= 500
            if cyc:
                cf = [c for c in cyc if c[1] == 0]; lp = [c for c in cf if c[8] == 0]
                evn = 'cexLPC' if lp else ('cexCF' if cf else 'cyc')
                if evn != 'cyc' or rng.random() < 0.02:
                    ok = S.validate(T.n, T.F, chi) is None
                    log.write(json.dumps(dict(ev=evn, seed=seed, walk=w, step=s, base=nm, g=g, chi=chi, valid=ok, n=T.n, hole=h, cyc=cyc,
                                              allDLcyc=r['allDLcyc'], states=r['states'], dual_bad=r['dual_bad'], pid_bad=r['pid_bad'],
                                              graph=line.replace('x ', f'hg{seed}_{w}_{s} ', 1))) + '\n'); log.flush()
            if sc >= cur or rng.random() < math.exp(max(-50, (sc - cur) / temp)): cur = sc
            else: T.F = old; T.rebuild()
            temp = max(0.2, temp * 0.999)
        print(json.dumps(dict(walk=w, base=nm, g=g, chi=chi, n=T.n, best=cur, nev=nev, secs=round(time.time() - t0))), flush=True)

if __name__ == '__main__':
    main()
