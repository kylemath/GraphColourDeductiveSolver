#!/usr/bin/env python3
"""Track H: LPC / CF on PSEUDO-surfaces (triangulated 2-complexes in which every edge lies in exactly two faces, but a
vertex link may be several cycles: surfaces with pinch points).  (F1)-(F3) of LockParity.md hold, so Theorem P holds;
the hole duality D may fail.  Annealing from the Track H seed surfaces with moves
  flip  : edge uv with faces uvw, uvz -> wz (wz not an edge; uv not at h, not a link edge),
  pinch : identify two vertices u, v (both off N[h], non-adjacent, N(u) and N(v) disjoint), at most MAXPINCH times.
Score: cycle class with min filled F, then (if F = 0) min pi-path ends.  Logs 'cyc' events; 'cexCF' if a cycle class has
F = 0; 'cexLPC' if moreover it has no pi-path ends (a union of all-DL pi-cycles) -- these are re-verified by th_engine.
usage: th_psearch.py SEED WALKS STEPS OUTPREFIX SEEDFILE [MAXPINCH]"""
import sys, json, random, os, math, time
from th_gsearch import evaluate, score as _unused  # noqa: F401  (evaluate = kclass4 wrapper)

def faces_from_rot(rot):
    F = set()
    for u in range(len(rot)):
        r = rot[u]; d = len(r)
        for t in range(d):
            a, b = r[t], r[(t + 1) % d]
            if b in rot[a] and u in rot[b] and a in rot[u]:
                F.add(frozenset((u, a, b)))
    return F

def check_faces(F, n):
    cnt = {}
    for f in F:
        a, b, c = tuple(f)
        for e in (frozenset((a, b)), frozenset((a, c)), frozenset((b, c))): cnt[e] = cnt.get(e, 0) + 1
    return all(v == 2 for v in cnt.values()), cnt

def link_order(F, h):
    fs = [tuple(x for x in f if x != h) for f in F if h in f]
    nb = {}
    for a, b in fs: nb.setdefault(a, []).append(b); nb.setdefault(b, []).append(a)
    start = fs[0][0]; order = [start]; prev = None; cur = start
    while True:
        nxt = [w for w in nb[cur] if w != prev]
        w = nxt[0] if prev is not None or len(nxt) == 1 else nxt[0]
        if w == start: break
        order.append(w); prev, cur = cur, w
        if len(order) > 10: return None
    return order

def adj_from_faces(F, n, h):
    A = [set() for _ in range(n)]
    for f in F:
        a, b, c = tuple(f); A[a] |= {b, c}; A[b] |= {a, c}; A[c] |= {a, b}
    lo = link_order(F, h)
    adj = [sorted(A[v]) for v in range(n)]; adj[h] = lo
    return adj

def compact(F, n):
    used = sorted({v for f in F for v in f}); mp = {v: i for i, v in enumerate(used)}
    return set(frozenset(mp[v] for v in f) for f in F), len(used), mp

def score(r):
    if r is None or r.get('states', 0) == 0: return -1e9, None
    cls = r['cls2[size,filled,DL,unfilledNonDL,minKdeg,maxKdeg,lockParityViolations,onCycles,piPathEnds]']
    cyc = [c for c in cls if c[7] > 0]
    if cyc:
        b = min(cyc, key=lambda c: (c[1], c[8], c[0]))
        return 1000 + 500.0 / (1 + b[1]) + (300.0 / (1 + b[8]) if b[1] == 0 else 0) - 0.002 * b[0], cyc
    return r['maxDLrun'] + 0.0, None

def main():
    seed, walks, steps, pref, sf = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5]
    maxp = int(sys.argv[6]) if len(sys.argv) > 6 else 3
    rng = random.Random(seed); tmp = pref + '.tmp'; log = open(pref + '.jsonl', 'a')
    seeds = []
    for l in open(sf):
        p = l.split()
        if len(p) >= 4: seeds.append((p[0], [list(map(int, r.split(','))) for r in p[2].split(';')], int(p[3])))
    t0 = time.time(); nev = 0
    for w in range(walks):
        nm, rot, h = seeds[w % len(seeds)]
        F = faces_from_rot(rot); n = len(rot)
        ok, _ = check_faces(F, n); assert ok, nm
        npinch = 0
        def ev(F, n, h):
            adj = adj_from_faces(F, n, h)
            if adj[h] is None or len(adj[h]) != 5: return None, None
            return evaluate(adj, n, tmp, h), adj
        want = rng.randint(1, maxp); tries = 0
        while npinch < want and tries < 200:
            tries += 1
            A = adj_from_faces(F, n, h); Nh = set(A[h]) | {h}
            u, v = rng.sample([x for x in range(n) if x not in Nh], 2)
            if v in A[u] or set(A[u]) & set(A[v]): continue
            Fp, n2, mp = compact(set(frozenset(u if x == v else x for x in f) for f in F), n)
            rr, _ = ev(Fp, n2, mp[h])
            if rr is None or rr.get('states', 0) == 0: continue
            F, n, h = Fp, n2, mp[h]; npinch += 1
        r, adj = ev(F, n, h); cur = score(r)[0]; T = 3.0
        for s in range(steps):
            F2 = set(F); n2 = n; h2 = h; kind = 'flip'
            if False:
                kind = 'pinch'
                A = adj_from_faces(F, n, h); Nh = set(A[h]) | {h}
                cand = [v for v in range(n) if v not in Nh]
                u, v = rng.sample(cand, 2)
                if v in A[u] or set(A[u]) & set(A[v]): continue
                F2 = set(frozenset(u if x == v else x for x in f) for f in F2)
                F2, n2, mp = compact(F2, n)
                h2 = mp[h]
            else:
                f1 = rng.choice(list(F2)); a, b = rng.sample(sorted(f1), 2)
                if h2 in (a, b): continue
                fs = [f for f in F2 if a in f and b in f]
                if len(fs) != 2: continue
                w1 = next(iter(fs[0] - {a, b})); w2 = next(iter(fs[1] - {a, b}))
                if w1 == w2: continue
                A = adj_from_faces(F2, n2, h2)
                if w2 in A[w1]: continue
                if len(A[a]) <= 3 or len(A[b]) <= 3: continue
                if a in A[h2] and b in A[h2]: continue
                F2 -= set(fs); F2 |= {frozenset((a, w1, w2)), frozenset((b, w1, w2))}
            r, adj2 = ev(F2, n2, h2); nev += 1
            if r is None: continue
            sc, cyc = score(r)
            if r.get('states', 0) > 60000: sc -= 500
            if cyc:
                cf = [c for c in cyc if c[1] == 0]; lp = [c for c in cf if c[8] == 0]
                evn = 'cexLPC' if lp else ('cexCF' if cf else 'cyc')
                if evn != 'cyc' or rng.random() < 0.05:
                    log.write(json.dumps(dict(ev=evn, seed=seed, walk=w, step=s, n=n2, pinches=npinch + (kind == 'pinch'), cyc=cyc, allDLcyc=r['allDLcyc'],
                                              states=r['states'], dual_bad=r['dual_bad'], pid_bad=r['pid_bad'],
                                              graph=f"p{seed}_{w}_{s} {n2} " + ';'.join(','.join(map(str, a)) for a in adj2) + f" {h2}")) + '\n'); log.flush()
            if sc >= cur or rng.random() < math.exp(max(-50, (sc - cur) / T)):
                F, n, h, cur = F2, n2, h2, sc
                if kind == 'pinch': npinch += 1
            T = max(0.2, T * 0.999)
        print(json.dumps(dict(walk=w, seed=nm, best=cur, pinches=npinch, nev=nev, secs=round(time.time() - t0))), flush=True)

if __name__ == '__main__':
    main()
