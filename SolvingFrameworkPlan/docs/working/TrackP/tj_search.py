#!/usr/bin/env python3
"""Track J task 2: annealing over general graphs for a NEAR-RIGID CLOSED class at hole h = 0:
a Kempe class of G - h all of whose states lie on all-DL pi-cycles, with N <= 9 at every state and N = 9 somewhere.

Graphs: h = 0 adjacent exactly to the induced 5-cycle 1..5 (link order 1,2,3,4,5); other vertices >= 6 with degree >= 3.
Moves: toggle 1-2 non-link-link edges.  Engine: tj_eng (C, this directory).

Rungs (nested):
  a  no constraint
  b  + chain-parity law at every pi-step of the class: N(pi c) - N(c) == [pi c DL] (mod 2)
  c  + G 4-colourable (some filled state of G - h exists, in any class)
  t  c + every edge of G - h in a triangle of G (soft: + 3 per edge in no triangle; hard if TJ_HARDTRI=1)
  h  c + the H3 edge balance E1 = E2+1 = E3+1 at every unfilled class state (score: + h3imb, the summed imbalance)
  d  c + both
  e  d + sphere edge count |E(G - h)| = 3n - 11 (with H3 this forces c_k - beta_k = 2,3,3, i.e. forests at rigid states); soft: + 2 per unit
bad(class) = (size - onCyc) + sum_{onCyc} max(0, N-9) + [b..] lawFail + [h,d] h3imb + (5 if no N = 9 state)
An example = a class with bad = 0 (and the graph constraints of the rung).
usage: tj_search.py RUNG SEED WALKS STEPS OUTPREFIX SEEDFILE [SEEDFILE...]   (seed files: 'name n adj;..' [hole])
"""
import sys, json, random, time, hashlib, os
from tj_lib import Engine, to_line, cls_dicts

RUNGS = 'abcthde'   # t = c + tri (hard); h = c + H3 balance; d = c + tri + H3


def load_seeds(files):
    out = []
    for f in files:
        for l in open(f):
            p = l.split()
            if len(p) < 3: continue
            rot = [list(map(int, r.split(','))) for r in p[2].split(';')]
            holes = [int(p[3])] if len(p) >= 4 and p[3].lstrip('-').isdigit() else ([0] if len(rot[0]) == 5 else [v for v in range(len(rot)) if len(rot[v]) == 5][:1])
            for h in holes:
                n = len(rot); lab = {h: 0}
                for t, x in enumerate(rot[h]): lab[x] = 1 + t
                for v in range(n):
                    if v not in lab: lab[v] = len(lab)
                E = set(frozenset((lab[u], lab[v])) for u in range(n) for v in rot[u] if u != h and v != h)
                out.append((p[0], n, E))
    return out


def tri_ok(adj, n):
    return notri(adj, n) == 0


def notri(adj, n):
    S = [set(a) for a in adj]
    return sum(1 for u in range(1, n) for v in adj[u] if v > u and not (S[u] & S[v]))


def main():
    rung, seed, walks, steps, pref = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    R = RUNGS.index(rung)
    seeds = load_seeds(sys.argv[6:])
    rng = random.Random(seed); eng = Engine(hole=0, maxstates=30000)
    log = open(pref + '.jsonl', 'a'); seen = set()
    nev = nex = 0; t0 = time.time(); best_overall = -1e9

    def adjof(E, n):
        adj = [[] for _ in range(n)]; adj[0] = [1, 2, 3, 4, 5]
        for t in range(1, 6): adj[t].append(0)
        for e in sorted(tuple(sorted(e)) for e in E):
            u, v = e; adj[u].append(v); adj[v].append(u)
        # link vertices: put link neighbours first in a fixed order (engine only needs adj[0] cyclic)
        return adj

    def ok(E, n):
        adj = adjof(E, n)
        if any(len(adj[v]) < 3 for v in range(6, n)): return None
        if rung in 'tde' and os.environ.get('TJ_HARDTRI') == '1' and not tri_ok(adj, n): return None
        return adj

    def score(js, adj=None):
        if js is None or 'err' in js: return -1e9, None
        cl = cls_dicts(js)
        if not cl: return -300.0, None
        best = None
        for c in cl:
            bad = (c['size'] - c['onCyc']) + c['exc'] + (5 if c['n9'] == 0 else 0)
            if R >= 1: bad += c['lawFail']
            if rung in 'hde': bad += c['h3imb']
            if best is None or (bad, c['size']) < (best[0], best[1]['size']): best = (bad, c)
        pen = 0
        if R >= 2 and js['filled'] == 0: pen = 40
        if rung in 'tde' and adj is not None: pen += 3 * notri(adj, len(adj))   # soft triangle constraint (0 at an example)
        if rung == 'e' and adj is not None:
            m = sum(len(a) for a in adj) // 2 - 5; pen += 2 * abs(m - (3 * len(adj) - 11))
        return -(best[0] + pen) - 0.001 * best[1]['size'], (best[0] + pen, best[1])

    import os
    tlim = float(os.environ.get('TJ_TLIM', '1e9'))
    for w in range(walks):
        if time.time() - t0 > tlim: break
        nm, n, E = seeds[w % len(seeds)]; E = set(E)
        grow = int(os.environ.get('TJ_GROW', '0'))
        if grow:   # stack new vertices on random triangles of G - h (keeps the Kempe structure and the H3 differences)
            for _ in range(rng.randint(0, grow)):
                adjs = {}
                for e in E:
                    u, v = tuple(e); adjs.setdefault(u, set()).add(v); adjs.setdefault(v, set()).add(u)
                tris = [(a, b, c) for a in adjs for b in adjs[a] if b > a for c in adjs[a] & adjs[b] if c > b]
                if not tris: break
                a, b, c = rng.choice(tris); E |= {frozenset((n, a)), frozenset((n, b)), frozenset((n, c))}; n += 1
        # randomise the start a little
        cand = [frozenset((u, v)) for u in range(1, n) for v in range(u + 1, n) if not (u <= 5 and v <= 5)]
        for _ in range(0 if w < len(seeds) else rng.randint(0, 1)):
            e = rng.choice(cand); E.symmetric_difference_update({e})
        adj = ok(E, n); tries = 0
        while adj is None and tries < 2000:
            e = rng.choice(cand); E.symmetric_difference_update({e}); adj = ok(E, n); tries += 1
        if adj is None: continue
        cur, _ = score(eng.run(to_line('g', adj, n))[0][0], adj); nev += 1
        T = 2.0; wbest = cur
        for s in range(steps):
            E2 = set(E)
            for _ in range(1 if rng.random() < 0.7 else 2):
                E2.symmetric_difference_update({rng.choice(cand)})
            adj2 = ok(E2, n)
            if adj2 is None: continue
            line = to_line(f'j{rung}{seed}_{w}_{s}', adj2, n)
            js = eng.run(line)[0][0]; nev += 1
            sc, info = score(js, adj2)
            if info is not None and info[0] == 0:
                key = hashlib.md5(str(sorted(tuple(sorted(e)) for e in E2)).encode()).hexdigest()
                if key not in seen:
                    seen.add(key); nex += 1
                    log.write(json.dumps(dict(ev='example', rung=rung, seed=seed, walk=w, step=s, src=nm, n=n, cls=info[1],
                                              filled=js['filled'], states=js['states'], cyclens=js['cyclens'], graph=line)) + '\n'); log.flush()
            elif info is not None and info[0] <= 2 and rng.random() < 0.02:
                log.write(json.dumps(dict(ev='near', rung=rung, bad=info[0], cls=info[1], filled=js['filled'], graph=line)) + '\n'); log.flush()
            if info is not None and sc > wbest and info[0] <= 15:
                c = info[1]
                log.write(json.dumps(dict(ev='wbest', rung=rung, walk=w, step=s, bad=info[0], offcyc=c['size'] - c['onCyc'], exc=c['exc'], law=c['lawFail'],
                                          h3imb=c['h3imb'], no9=int(c['n9'] == 0), filled=js['filled'], cls=c, graph=line)) + '\n'); log.flush()
            if sc >= cur or rng.random() < pow(2.718, (sc - cur) / T):
                E, cur = E2, sc
            wbest = max(wbest, cur); T = max(0.15, T * 0.9995)
        best_overall = max(best_overall, wbest)
        print(json.dumps(dict(walk=w, src=nm, n=n, best=round(wbest, 3), cur=round(cur, 3), nev=nev, nex=nex, secs=round(time.time() - t0))), flush=True)
    print('DONE', json.dumps(dict(rung=rung, seed=seed, nev=nev, examples=nex, best=best_overall, secs=round(time.time() - t0))), flush=True)
    eng.close()


if __name__ == '__main__':
    main()
