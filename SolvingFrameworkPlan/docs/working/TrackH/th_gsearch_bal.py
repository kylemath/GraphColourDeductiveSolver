#!/usr/bin/env python3
"""Track H (variant BAL: as th_gsearch_lp, plus the per-state EDGE BALANCE of closed triangulated surfaces --
at every unfilled state of the cycle class, the edges of G - h split over the partitions {am|AB}, {aA|mB}, {aB|mA} as
(m+1, m, m) (equivalent to the Euler identity c_k - beta_k = chi + [k != 1]); cex = F = 0, no path ends, LP = 0 AND balanced.
Original header: LPC in general graphs with BOTH hypotheses: no pi-path ends (D) and no lock-parity violations (LP); cex = class with filled = 0 AND no pi-path ends, i.e. a union of all-DL pi-cycles): does "an all-DL pi-cycle forces a filled state in its class" (CF) need a surface at all?
Annealing over ARBITRARY graphs G: a hole h adjacent exactly to a 5-cycle x0..x4 (no link chords), plus n-6 other
vertices with arbitrary edges (no surface, no triangulation).  pi, locks, DL, classes are purely graph-theoretic,
so the engine kclass4 (TrackF, read-only use) evaluates them.  Logs every graph with an all-DL pi-cycle; flags
  CF-fail : a class with onCycles > 0 and filled = 0,
  LPCg-fail: a class with filled = 0, onCycles > 0 (same), and kclass4 viol = 0 (parity-based; only meaningful on surfaces).
usage (mode ball: freeze the 2-ball of h of the seed surface): th_gsearch_lp.py SEED NMIN NMAX WALKS STEPS OUTPREFIX [--mode free|tri]
  mode tri: only accept graphs in which every edge of G - h lies in >= 1 triangle of G (a weak local-triangulation filter)."""
import sys, json, random, subprocess, os, time

KC = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'TrackF', 'src', 'kclass4')

def to_line(name, adj, n):
    return f"{name} {n} " + ';'.join(','.join(map(str, adj[v])) for v in range(n))

def evaluate(adj, n, tmp):
    with open(tmp, 'w') as f: f.write(to_line('g', adj, n) + '\n')
    try:
        out = subprocess.run([KC, tmp, '0'], capture_output=True, text=True, timeout=60).stdout
    except subprocess.TimeoutExpired:
        return None
    for l in out.splitlines():
        if l.startswith('{'): return json.loads(l)
    return None

def tri_ok(adj, n):
    S = [set(a) for a in adj]
    for u in range(1, n):
        for v in adj[u]:
            if v > u and v != 0 and not (S[u] & S[v]): return False
    return True

from th_engine import Hole as _Hole

def imbalance(adj, n):
    try:
        H = _Hole(adj, 0).build()
    except Exception:
        return 999
    cyc = H.allDL_cycles()
    if not cyc: return 999
    best = 999
    for c in cyc:
        mem = H.class_members(c[0]); tot = 0
        for i in mem:
            r = H.info[i]
            if r['kind'] == 'F': continue
            col = H.col(i); al, mu, A, B = r['roles']
            part = {frozenset((al, mu)): 0, frozenset((A, B)): 0, frozenset((al, A)): 1, frozenset((mu, B)): 1, frozenset((al, B)): 2, frozenset((mu, A)): 2}
            E = [0, 0, 0]
            for v in H.V:
                for w in H.adj[v]:
                    if w > v: E[part[frozenset((col[v], col[w]))]] += 1
            tot += abs(E[0] - E[1] - 1) + abs(E[1] - E[2])
        best = min(best, tot)
    return best

def score(r):
    if r is None or r['states'] == 0: return -1e9, None
    cls = r['cls2[size,filled,DL,unfilledNonDL,minKdeg,maxKdeg,lockParityViolations,onCycles,piPathEnds]']
    cyc = [c for c in cls if c[7] > 0]
    if cyc:
        b = min(cyc, key=lambda c: (c[1], c[8], c[6], c[0]))
        return (1000 + 500.0 / (1 + b[1]) + (300.0 / (1 + b[8]) if b[1] == 0 else 0)
                + (300.0 / (1 + b[6]) if b[1] == 0 and b[8] == 0 else 0) - 0.002 * b[0]), cyc
    return r['maxDLrun'] + 0.0, None

def main():
    seed, nmin, nmax, walks, steps, pref = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
    mode = sys.argv[sys.argv.index('--mode') + 1] if '--mode' in sys.argv else 'free'
    rng = random.Random(seed); tmp = pref + '.tmp'; log = open(pref + '.jsonl', 'a')
    nev = 0; t0 = time.time(); best_all = -1e9; ncyc = 0
    seeds = []
    if '--seeds' in sys.argv:
        for l in open(sys.argv[sys.argv.index('--seeds') + 1]):
            p = l.split()
            if len(p) >= 4: seeds.append((p[0], int(p[1]), [list(map(int, r.split(','))) for r in p[2].split(';')], int(p[3])))
    for w in range(walks):
        if seeds:
            nm, n, rot, h = seeds[w % len(seeds)]
            # relabel: h -> 0, link rot[h] -> 1..5, rest -> 6..
            lab = {h: 0}
            for t, x in enumerate(rot[h]): lab[x] = 1 + t
            for v in range(n):
                if v not in lab: lab[v] = len(lab)
            E = set(frozenset((lab[u], lab[v])) for u in range(n) for v in rot[u] if u != h and v != h)
        else:
            n = rng.randint(nmin, nmax)
            E = set()
            for t in range(5): E.add(frozenset((1 + t, 1 + (t + 1) % 5)))
        cand = [frozenset((u, v)) for u in range(1, n) for v in range(u + 1, n)
                if not (u <= 5 and v <= 5)]
        if mode == 'ball' and seeds:
            # freeze the triangulated 2-ball of h: every edge at a link vertex, and every edge between two
            # neighbours of a common link vertex (the faces around the link vertices); everything else is free
            NB = {t: {u for e in E if t in e for u in e if u != t} for t in range(1, 6)}
            cand = [e for e in cand if not (set(e) & {1, 2, 3, 4, 5}) and not any(set(e) <= NB[t] for t in range(1, 6))]
        if not seeds:
            p = rng.uniform(0.15, 0.35)
            for e in cand:
                if rng.random() < p: E.add(e)
        def adjof(E):
            adj = [[] for _ in range(n)]; adj[0] = [1, 2, 3, 4, 5]
            for t in range(1, 6): adj[t].append(0)
            for e in E:
                u, v = tuple(e); adj[u].append(v); adj[v].append(u)
            return adj
        def ok(E):
            adj = adjof(E)
            if any(len(adj[v]) < 3 for v in range(6, n)): return None
            if mode == 'tri' and not tri_ok(adj, n): return None
            return adj
        adj = ok(E); tries = 0
        while adj is None and tries < 1000:
            e = rng.choice(cand); E.add(e); adj = ok(E); tries += 1
        cur = score(evaluate(adj, n, tmp))[0] if adj else -1e9; nev += 1
        T = 3.0
        for s in range(steps):
            E2 = set(E); e = rng.choice(cand)
            if e in E2: E2.remove(e)
            else: E2.add(e)
            if rng.random() < 0.3:
                e = rng.choice(cand)
                if e in E2: E2.remove(e)
                else: E2.add(e)
            adj2 = ok(E2)
            if adj2 is None: continue
            r = evaluate(adj2, n, tmp); nev += 1
            sc, cyc = score(r)
            if r and r.get('states', 0) > 40000: sc -= 500
            bal = None
            if cyc and any(c[1] == 0 and c[8] == 0 and c[6] == 0 for c in cyc):
                bal = imbalance(adj2, n); sc += 300.0 / (1 + bal)
            if cyc:
                ncyc += 1
                fail = [c for c in cyc if c[1] == 0 and c[8] == 0 and c[6] == 0] if bal == 0 else []
                log.write(json.dumps(dict(ev='cex' if fail else 'cyc', seed=seed, walk=w, step=s, n=n, mode=mode, cyc=cyc,
                                          allDLcyc=r['allDLcyc'], bal=bal, states=r['states'], dual_bad=r['dual_bad'], graph=to_line(f'g{seed}_{w}_{s}', adj2, n))) + '\n'); log.flush()
            if sc >= cur or rng.random() < pow(2.718, (sc - cur) / T):
                E, cur = E2, sc
            T = max(0.2, T * 0.999)
            best_all = max(best_all, cur)
        print(json.dumps(dict(walk=w, n=n, best=cur, nev=nev, ncyc=ncyc, secs=round(time.time() - t0))), flush=True)
    os.unlink(tmp) if os.path.exists(tmp) else None

if __name__ == '__main__':
    main()
