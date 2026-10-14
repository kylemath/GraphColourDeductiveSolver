#!/usr/bin/env python3
"""S2: complex-level annealing on closed pseudo-surfaces (arm A) or closed surfaces (arm B).
usage: s2_search.py ARM(A|B) SEED TLIM OUTPREFIX NMIN NMAX HANDLES_MIN HANDLES_MAX [SEEDFILE]
 State: a face list F in which every edge lies in exactly two faces (checked after every move).
 Moves: edge flip; insert a vertex in a face; remove a degree-3 vertex; tube between two vertex-disjoint faces
 (adds a handle or crosscap; used only to build the start, genus is fixed during a walk); arm A only: pinch (identify two vertices with disjoint closed stars) and unpinch.
 Holes: every degree-5 vertex whose link is one cycle (sf_eng --allholes on the 1-skeleton).
 Score (minimise): min over holes and over classes containing a cycle state of log2(1 + gap), gap = size - onCyc
   (0 = frozen class = LPC fails); if no class with a cycle anywhere: 25 + max(0, 20 - max DLrun)/2; no hole or no
   colouring: 40.
 Logs: every cycle class (deduplicated) with its gap; every frozen class (HIT)."""
import sys, json, random, time, hashlib
from collections import defaultdict
from sf_lib import Engine, cls_dicts, to_line, complex_to_adj, edges_of, link_cycles, euler, orientable


def sphere(n, rng):
    """random sphere triangulation: octahedron + random 1-3 insertions"""
    F = [(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 1), (5, 2, 1), (5, 3, 2), (5, 4, 3), (5, 1, 4)]
    nxt = 6
    while nxt < n:
        i = rng.randrange(len(F)); a, b, c = F.pop(i); F += [(a, b, nxt), (b, c, nxt), (c, a, nxt)]; nxt += 1
    return F


def valid(F):
    E = edges_of(F)
    if any(len(x) != 2 for x in E.values()): return False
    if len({tuple(sorted(f)) for f in F}) != len(F): return False
    return True


def graph_edges(F):
    return set(edges_of(F).keys())


def mv_flip(F, rng):
    E = edges_of(F); e = rng.choice(list(E.keys())); i, k = E[e]; a, b = e
    c = [x for x in F[i] if x not in e][0]; d = [x for x in F[k] if x not in e][0]
    if c == d or tuple(sorted((c, d))) in E: return None
    G = [f for t, f in enumerate(F) if t not in (i, k)] + [(a, c, d), (b, c, d)]
    return G


def mv_insert(F, rng):
    i = rng.randrange(len(F)); a, b, c = F[i]; v = max(x for f in F for x in f) + 1
    return [f for t, f in enumerate(F) if t != i] + [(a, b, v), (b, c, v), (c, a, v)]


def mv_remove3(F, rng):
    deg = defaultdict(set)
    for f in F:
        for x in f: deg[x] |= set(f) - {x}
    cand = [v for v in deg if len(deg[v]) == 3]
    if not cand: return None
    v = rng.choice(cand); a, b, c = sorted(deg[v])
    if any(set(f) == {a, b, c} for f in F): return None
    return [f for f in F if v not in f] + [(a, b, c)]


def mv_tube(F, rng):
    for _ in range(20):
        f1, f2 = rng.sample(F, 2)
        if set(f1) & set(f2): continue
        E = graph_edges(F); a, b, c = f1; d, e, f = rng.sample(f2, 3)
        new = [(a, b, e), (a, e, d), (b, c, f), (b, f, e), (c, a, d), (c, d, f)]
        ne = {tuple(sorted(p)) for t in new for p in ((t[0], t[1]), (t[1], t[2]), (t[0], t[2]))} - {tuple(sorted(p)) for p in ((a, b), (b, c), (a, c), (d, e), (e, f), (d, f))}
        if ne & E: continue
        return [x for x in F if x not in (f1, f2)] + new
    return None


def mv_pinch(F, rng):
    nbr = defaultdict(set)
    for f in F:
        for x in f: nbr[x] |= set(f) - {x}
    V = list(nbr)
    for _ in range(30):
        u, v = rng.sample(V, 2)
        if v in nbr[u] or (nbr[u] & nbr[v]): continue
        return [tuple(u if x == v else x for x in f) for f in F]
    return None


def mv_unpinch(F, rng):
    lc = link_cycles(F); cand = [v for v, k in lc.items() if k >= 2]
    if not cand: return None
    v = rng.choice(cand)
    # find one link component of v
    L = [(f, tuple(x for x in f if x != v)) for f in F if v in f]
    adj = defaultdict(list)
    for f, (p, q) in L: adj[p].append(q); adj[q].append(p)
    s = L[0][1][0]; comp = {s}; st = [s]
    while st:
        y = st.pop()
        for z in adj[y]:
            if z not in comp: comp.add(z); st.append(z)
    w = max(x for f in F for x in f) + 1
    return [tuple(w if x == v else x for x in f) if (v in f and set(f) - {v} <= comp) else f for f in F]


def wl_hash(adj):
    col = [len(a) for a in adj]
    for _ in range(3):
        col = [hash((col[v], tuple(sorted(col[w] for w in adj[v])))) for v in range(len(adj))]
    return hashlib.md5(str(sorted(col)).encode()).hexdigest()[:12]


def main():
    arm, seed, tlim, pref = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
    nmin, nmax, hmin, hmax = map(int, sys.argv[5:9])
    seedfile = sys.argv[9] if len(sys.argv) > 9 else None
    rng = random.Random(seed); eng = Engine(allholes=True, maxstates=40000)
    log = open(pref + '.jsonl', 'w'); t0 = time.time(); nev = 0; seen = set(); ncyc = 0; hits = 0; best_gap = 10 ** 9
    seedF = [json.loads(l)['faces'] for l in open(seedfile)] if seedfile else []

    def evaluate(F):
        adj, idx = complex_to_adj(F)
        if len(adj) > 63: return 40, None, adj
        lc = link_cycles(F); inv = {i: v for v, i in idx.items()}
        holes = [i for i in range(len(adj)) if len(adj[i]) == 5 and lc[inv[i]] == 1]
        nh = sum(1 for a in adj if len(a) == 5)
        if not holes: return 40, None, adj
        res = eng.run(to_line('g', adj), nh)
        best = 40; info = []; import math
        for js in res:
            if 'err' in js: continue
            for c in cls_dicts(js):
                g = c['size'] - c['onCyc']; info.append((js['hole'], g, c, js['states'], js['filled']))
                best = min(best, math.log2(1 + g))
            if js['states'] > 0: best = min(best, 25 + max(0, 20 - js['DLrun']) / 2)
        return best, info, adj

    w = 0
    while time.time() - t0 < tlim:
        if seedF and w % 2 == 0:
            F = [tuple(f) for f in seedF[rng.randrange(len(seedF))]]
            for _ in range(rng.randint(hmin, hmax)):   # optional extra handles/crosscaps on a seeded start
                G = mv_tube(F, rng)
                if G: F = G
        else:
            n0 = rng.randint(nmin, nmax); F = sphere(max(6, n0 - 0), rng)
            for _ in range(rng.randint(hmin, hmax)):
                G = mv_tube(F, rng)
                if G: F = G
            for _ in range(3 * len(F)):
                G = mv_flip(F, rng)
                if G and valid(G): F = G
        cur, info, adj = evaluate(F); nev += 1; T = 1.0; wb = cur
        for s in range(3000):
            if time.time() - t0 > tlim: break
            x = rng.random()
            if x < 0.70: G = mv_flip(F, rng)
            elif x < 0.78: G = mv_insert(F, rng)
            elif x < 0.86: G = mv_remove3(F, rng)
            elif x < 0.90: G = mv_flip(F, rng)   # genus fixed during a walk (tubes only at the start)
            elif arm == 'A' and x < 0.96: G = mv_pinch(F, rng)
            elif arm == 'A': G = mv_unpinch(F, rng)
            else: G = mv_flip(F, rng)
            if G is None or not valid(G): continue
            nV = len({v for f in G for v in f})
            if nV > nmax + 8 or nV < 8: continue
            if arm == 'B' and any(k != 1 for k in link_cycles(G).values()): continue
            if arm == 'A' and sum(k - 1 for k in link_cycles(G).values()) > 4: continue   # at most 4 extra link cycles
            sc, info, adj = evaluate(G); nev += 1
            if info:
                hsh = wl_hash(adj)
                for hole, g, c, states, filled in info:
                    key = (hsh, len(adj[hole]) if hole < len(adj) else 0, tuple(c[k] for k in ('size', 'filled', 'DL', 'onCyc')))
                    if key in seen: continue
                    seen.add(key); ncyc += 1
                    lcG = link_cycles(G)
                    rec = dict(ev='HIT' if g == 0 else 'cyc', gap=g, hole=hole, cls=c, states=states, filled=filled, n=len(adj),
                               chi=euler(G), orientable=orientable(G), pinched=sum(1 for k in lcG.values() if k > 1),
                               edges=len(edges_of(G)), faces=G if g <= 2 else None, graph=to_line(f's2{arm}_{seed}_{w}_{s}', adj))
                    log.write(json.dumps(rec) + '\n'); log.flush()
                    if g == 0: hits += 1
                    best_gap = min(best_gap, g)
            if sc <= cur or rng.random() < pow(2.718, (cur - sc) / T):
                F, cur = G, sc; wb = min(wb, cur)
            T = max(0.1, T * 0.998)
        V = {v for f in F for v in f}
        print(json.dumps(dict(walk=w, best=wb, cur=cur, n=len(V), chi=euler(F), nev=nev, cycclasses=ncyc, hits=hits,
                              best_gap=best_gap, secs=round(time.time() - t0))), flush=True)
        w += 1
    print('DONE', json.dumps(dict(arm=arm, seed=seed, nev=nev, cycclasses=ncyc, hits=hits, best_gap=best_gap)), flush=True)


if __name__ == '__main__':
    main()
