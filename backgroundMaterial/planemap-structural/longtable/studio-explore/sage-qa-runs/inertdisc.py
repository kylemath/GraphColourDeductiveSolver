#!/usr/bin/env python3
"""[exploratory] Inert-disc check (Fable sage, via the coordinator). For a degree-5 hole v: every swap s -> t on a shortest
filling sequence (dist[t] = dist[s] - 1, dist = moves to the filled set) out of an unfilled DL state s. Lock curves of s:
C1 = v + a shortest path m ~ a inside the {mu,A}-chain of m; C2 = v + a shortest path m ~ b inside the {mu,B}-chain of m
(frame: repeat x_j = x_{j+2}, m = x_{j+1}, a = x_{j+3}, b = x_{j+4}). Each C_i is a cycle of T, so T - C_i splits into the
two Jordan sides; the "disc" of C_i is taken to be the side containing x_{j+2} (the repeat partner; stated convention).
The swapped component K is a VIOLATION iff it meets neither lock chain and lies strictly inside a lock disc (all of K in
the disc of C1 or of C2). Only DL states are checked (the locks exist only there).
usage: inertdisc.py --faces FILE.json HOLE | --plantri "LINE" HOLE"""
import itertools, json, sys
from collections import deque


def load():
    if sys.argv[1] == "--plantri":
        rot = [[ord(c) - 97 for c in x] for x in sys.argv[2].split()[1].split(",")]
        adj = {v: set(nb) for v, nb in enumerate(rot)}; hole = int(sys.argv[3]); return adj, hole, list(rot[hole])
    d = json.load(open(sys.argv[2])); F = d.get("faces") or d.get("faces_ccw"); hole = int(sys.argv[3]); adj = {}
    for f in F:
        for i in range(3):
            adj.setdefault(f[i], set()).add(f[(i + 1) % 3]); adj.setdefault(f[(i + 1) % 3], set()).add(f[i])
    nbr = sorted(adj[hole]); L = [nbr[0]]
    while len(L) < len(nbr): L.append([w for w in adj[L[-1]] if w in adj[hole] and w not in L][0])
    return adj, hole, L


def main():
    adj, hole, link = load()
    V = [u for u in adj if u != hole]; A = {u: adj[u] - {hole} for u in V}
    order, seen = [link[0]], {link[0]}
    for x in order:
        for y in sorted(A[x]):
            if y not in seen: seen.add(y); order.append(y)
    states, col = [], {}

    def rec(i, used):
        if i == len(order): states.append(tuple(col[u] for u in order)); return
        u = order[i]; forb = {col[w] for w in A[u] if w in col}
        for c in range(min(used + 1, 4)):
            if c not in forb: col[u] = c; rec(i + 1, max(used, c + 1)); del col[u]
    rec(0, 0)
    index = {s: k for k, s in enumerate(states)}
    canon = lambda d: (lambda mp: tuple(mp.setdefault(d[u], len(mp)) for u in order))({})

    def comps(c, p, q):
        Vs = {u for u in order if c[u] in (p, q)}; out, sn = [], set()
        for s in Vs:
            if s in sn: continue
            comp, st = {s}, [s]; sn.add(s)
            while st:
                x = st.pop()
                for y in A[x]:
                    if y in Vs and y not in sn: sn.add(y); comp.add(y); st.append(y)
            out.append(comp)
        return out

    def path(K, s, t):
        prev = {s: None}; q = deque([s])
        while q:
            x = q.popleft()
            if x == t: break
            for y in A[x]:
                if y in K and y not in prev: prev[y] = x; q.append(y)
        P, x = [], t
        while x is not None: P.append(x); x = prev[x]
        return P

    def disc(cycle, ref):
        rest = set(adj) - set(cycle); comp = {ref}; st = [ref]
        while st:
            x = st.pop()
            for y in adj[x]:
                if y in rest and y not in comp: comp.add(y); st.append(y)
        return comp
    moves, filled = [], []
    for s in states:
        c = dict(zip(order, s)); mv = []
        for (p, q) in itertools.combinations(range(4), 2):
            for K in comps(c, p, q):
                d = dict(c)
                for u in K: d[u] = q if c[u] == p else p
                mv.append((index[canon(d)], frozenset(K)))
        moves.append(mv); filled.append(len({c[x] for x in link}) <= 3)
    dist = [-1] * len(states); q = deque(k for k in range(len(states)) if filled[k])
    for k in q: dist[k] = 0
    while q:
        x = q.popleft()
        for t, _ in moves[x]:
            if dist[t] < 0: dist[t] = dist[x] + 1; q.append(t)
    checked = viol = 0; examples = []; from collections import Counter; kinds = Counter()
    for si, s in enumerate(states):
        if filled[si]: continue
        c = dict(zip(order, s)); lc = [c[x] for x in link]
        j = [j for j in range(5) if lc[j] == lc[(j + 2) % 5]][0]
        m, a, b, x2 = link[(j + 1) % 5], link[(j + 3) % 5], link[(j + 4) % 5], link[(j + 2) % 5]
        ch = {}
        for t in (a, b):
            ch[t] = [K for K in comps(c, *sorted((c[m], c[t]))) if m in K][0]
        if a not in ch[a] or b not in ch[b]: continue  # not DL
        D1 = disc([hole] + path(ch[a], m, a), x2); D2 = disc([hole] + path(ch[b], m, b), x2)
        for t, K in moves[si]:
            if dist[t] != dist[si] - 1: continue
            checked += 1
            if K & ch[a] or K & ch[b]: continue
            if K <= D1 or K <= D2:
                viol += 1; kinds[("contains_x2" if x2 in K else "meets_link" if K & set(link) else "interior")] += 1
                if (x2 not in K) and len(examples) < 10: examples.append({"state_dist": dist[si], "component": sorted(K), "in_disc1": K <= D1, "in_disc2": K <= D2,
                                                       "colouring": {str(u): c[u] for u in order}, "frame_j": j})
    print(json.dumps({"hole": hole, "states": len(states), "max_dist": max(dist), "shortest_fill_swaps_from_DL_checked": checked,
                      "violations": viol, "violation_kinds": dict(kinds), "examples": examples}))


if __name__ == "__main__":
    main()
