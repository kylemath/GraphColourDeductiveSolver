#!/usr/bin/env python3
"""Track N: randomized local search complementing tn_forest.py when ADDING edges is allowed.
For a law-respecting pi-cycle C in R (found with tn_eng --dump), keep at every state of C the vertex partition of every
pair graph (so C stays a law-respecting pi-cycle in R, see tn_forest.py).  Edge set K starts at G - h.  Moves:
  delete: an edge (not a link-cycle edge) that is a non-bridge of its pair graph at EVERY state of C;
  add:    an 'addable' non-edge (properly coloured at every state and inside one pair-graph component at every state).
Descent on |K| with plateau / uphill moves (add, then greedily delete).  Reports the minimum excess
|K| - (3n - 11) found (excess 0 with connectivity preserved <=> Lemma E sphere constants at every rigid state of C; at
9-states it is then re-checked with tn_eng).
usage: tn_addlocal.py OUT.jsonl ITERS FILE [FILE ...]"""
import sys, json, random, time
import networkx as nx
from tn_forest import Engine, parse_dump, cycles_in_R_law, PAIRS
from tn_flow import addable
from tn_lib import adjof, to_line


def bridges_all(K, cols, n):
    """set of edges of K that are a bridge of their pair graph at SOME state."""
    bad = set()
    for c in cols:
        for (p, q) in PAIRS:
            G = nx.Graph(); G.add_edges_from(e for e in K if c[e[0]] in (p, q) and c[e[1]] in (p, q))
            for (u, v) in nx.bridges(G): bad.add((min(u, v), max(u, v)))
    return bad


def run(n, E, cols, iters, rng):
    link = {(t, t % 5 + 1) if t < 5 else (1, 5) for t in range(1, 6)}
    K = set(tuple(sorted(e)) for e in E)
    A = addable(n, E, cols)
    target = 3 * n - 11
    def descend(K):
        while True:
            D = [e for e in K - bridges_all(K, cols, n) if e not in link]
            if not D: return K
            K = set(K); K.discard(rng.choice(D))
    K = descend(K); best = len(K); bestK = set(K)
    for it in range(iters):
        K2 = set(K)
        for _ in range(rng.randint(1, 3)):
            cand = [f for f in A if f not in K2]
            if cand: K2.add(rng.choice(cand))
        K2 = descend(K2)
        if len(K2) <= len(K) or rng.random() < 0.05:
            K = K2
        if len(K) < best: best = len(K); bestK = set(K)
        if best == target: break
    return best - target, bestK, len(A)


def main():
    out = open(sys.argv[1], 'a'); iters = int(sys.argv[2]); rng = random.Random(7)
    ed = Engine(dump=True, maxstates=200000); ec = Engine(maxstates=400000)
    for f in sys.argv[3:]:
        for l in open(f):
            if l.startswith('{'):
                d = json.loads(l)
                if 'graph' not in d or d.get('ev', 'example') != 'example': continue
                l = d['graph']
            p = l.split()
            if len(p) < 3: continue
            rot = [list(map(int, r.split(','))) for r in p[2].split(';')]
            n = len(rot); E = {frozenset((u, v)) for u in range(1, n) for v in rot[u] if v != 0}
            js, tn, dump = ed.run(l)
            if tn is None: continue
            S = parse_dump(dump); cyc = cycles_in_R_law(S)
            if not cyc: continue
            C = cyc[0]; cols = [[-1 if ch == '-' else int(ch) for ch in S[x]['col']] for x in C]
            t0 = time.time(); exc, K, na = run(n, E, cols, iters, rng)
            line = to_line(p[0] + '_L', adjof({frozenset(e) for e in K}, n)); js2, tn2, _ = ec.run(line)
            rec = dict(src=p[0], n=n, nedge=len(E), addable=na, min_excess_edges=exc, kedges=len(K), check_cyc=tn2['cyc'] if tn2 else None,
                       check_win=tn2['win'] if tn2 else None, secs=round(time.time() - t0, 1), graph=line)
            out.write(json.dumps(rec) + '\n'); out.flush()
            print(json.dumps({k: v for k, v in rec.items() if k != 'graph'}), flush=True)


if __name__ == '__main__':
    main()
