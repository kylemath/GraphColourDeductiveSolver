#!/usr/bin/env python3
"""S1: TrackJ-style annealing from the rung-d graphs with a graph-level surface-defect penalty.
usage: s1_search.py ARM(A|B|CA|CB|0) LAMBDA SEED TLIM_SECONDS OUTPREFIX SEEDJSONL
 score (minimise) = gapscore + LAMBDA * defect_ARM ; ARM 0 = no defect term (control C1)
 A/B: graph-level (flag) defects; CA/CB: complex level = (#edges in < 2 triangles, deficit summed) + 3, or 3 if no
 face set with every edge in exactly two faces exists (SAT), CB: 2 if face sets exist but none has all links single cycles.
 gapscore = min over classes with a cycle state of (size - onCyc), else 40 + max(0, 20 - DLrun)
 Moves: toggle 1-2 edges among vertices >= 1 (never edges at h = 0, never link-link edges), or (p=0.1) stack a
 new vertex on a random triangle of G - h, or (p=0.05) delete a random vertex >= 6 of degree <= 4.
Logs: Pareto front of (gapscore, defect) and every hit with gap = 0 and defect = 0."""
import sys, json, random, time
from sf_lib import Engine, cls_dicts, to_line, parse_line, defects
from sf_cplx import lower_defect, solve


def main():
    arm, lam, seed, tlim, pref, src = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), sys.argv[5], sys.argv[6]
    rng = random.Random(seed); eng = Engine(hole=0, maxstates=30000)
    seeds = [parse_line(json.loads(l)['graph'])[1] for l in open(src)]
    log = open(pref + '.jsonl', 'w'); t0 = time.time(); nev = 0
    front = {}   # defect -> best gap
    hits = 0

    def dfun(adj):
        d = defects(adj)
        if arm in ('CA', 'CB'):   # complex level: edges in < 2 triangles, then SAT for a face set (sf_cplx)
            ld = lower_defect(adj); d['lower'] = ld
            if ld > 0: return ld + 3, d
            a, b, K = solve(adj, armB=(arm == 'CB'))
            d['satA'] = a; d['satB'] = b
            if not a: return 3, d
            if arm == 'CB' and b is not True: return 2, d
            d['faces'] = K
            return 0, d
        return 0 if arm == '0' else (d['dA'] if arm == 'A' else d['dB']), d

    def evaluate(E, n):
        adj = [[] for _ in range(n)]; adj[0] = [1, 2, 3, 4, 5]
        for t in range(1, 6): adj[t].append(0)
        for u, v in sorted(E): adj[u].append(v); adj[v].append(u)
        if any(len(adj[v]) < 3 for v in range(6, n)): return None
        js = eng.run(to_line('g', adj))[0]
        if 'err' in js: return None
        cl = cls_dicts(js)
        gap = min((c['size'] - c['onCyc'] for c in cl), default=None)
        gs = gap if gap is not None else 40 + max(0, 20 - js['DLrun'])
        dd, d = dfun(adj)
        return gs, dd, d, js, adj

    w = 0
    while time.time() - t0 < tlim:
        adj0 = seeds[w % len(seeds)]; n = len(adj0)
        E = set((min(u, v), max(u, v)) for u in range(1, n) for v in adj0[u] if v != 0)
        r = evaluate(E, n); nev += 1
        if r is None: w += 1; continue
        cur = r[0] + lam * r[1]; T = 3.0; wb = (r[0], r[1])
        for s in range(4000):
            if time.time() - t0 > tlim: break
            E2 = set(E); n2 = n; x = rng.random()
            if x < 0.10:   # stack
                adjs = {}
                for u, v in E: adjs.setdefault(u, set()).add(v); adjs.setdefault(v, set()).add(u)
                tris = [(a, b, c) for a in adjs for b in adjs[a] if b > a for c in adjs[a] & adjs[b] if c > b]
                if not tris or n >= 60: continue
                a, b, c = rng.choice(tris); E2 |= {(a, n), (b, n), (c, n)}; n2 = n + 1
            elif x < 0.15:   # delete a low-degree vertex
                deg = {}
                for u, v in E: deg[u] = deg.get(u, 0) + 1; deg[v] = deg.get(v, 0) + 1
                cand = [v for v in range(6, n) if deg.get(v, 0) <= 4]
                if not cand: continue
                z = rng.choice(cand); last = n - 1
                E2 = set()
                for u, v in E:
                    if z in (u, v): continue
                    u = z if u == last else u; v = z if v == last else v
                    E2.add((min(u, v), max(u, v)))
                n2 = n - 1
            else:
                for _ in range(1 if rng.random() < 0.7 else 2):
                    u = rng.randrange(1, n); v = rng.randrange(1, n)
                    if u == v or (u <= 5 and v <= 5): continue
                    E2.symmetric_difference_update({(min(u, v), max(u, v))})
            r = evaluate(E2, n2); nev += 1
            if r is None: continue
            gs, dd, d, js, adj = r
            if dd not in front or gs < front[dd]:
                front[dd] = gs
                log.write(json.dumps(dict(ev='front', gap=gs, defect=dd, n=n2, d=d, states=js['states'], filled=js['filled'],
                                          graph=to_line(f's1{arm}_{seed}_{w}_{s}', adj))) + '\n'); log.flush()
            if gs == 0 and dd == 0 and arm != '0':
                hits += 1
                log.write(json.dumps(dict(ev='HIT', n=n2, d=d, js=js, graph=to_line(f's1{arm}_{seed}_{w}_{s}', adj))) + '\n'); log.flush()
            if arm == '0' and gs == 0: hits += 1
            sc = gs + lam * dd
            if sc <= cur or rng.random() < pow(2.718, (cur - sc) / T):
                E, n, cur = E2, n2, sc
                if (gs, dd) < wb: wb = (gs, dd)
            T = max(0.2, T * 0.999)
        print(json.dumps(dict(walk=w, best=wb, nev=nev, hits=hits, secs=round(time.time() - t0))), flush=True)
        w += 1
    pf = sorted(front.items())
    print('DONE', json.dumps(dict(arm=arm, lam=lam, nev=nev, hits=hits, front=pf[:40])), flush=True)


if __name__ == '__main__':
    main()
