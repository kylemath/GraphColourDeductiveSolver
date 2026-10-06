#!/usr/bin/env python3
"""[exploratory] Sage QA run 5 (first pass, Studio compute's own candidate potentials; the path-4 list was not found on main).
For a degree-5 hole v of T: enumerate all 4-colourings of T - v up to renaming, the Kempe moves (whole two-colour components),
and for each candidate potential Phi count the UNFILLED states (link on 4 colours) where no single move strictly lowers Phi
("stuck states"). Phi = 0-target is not assumed; a potential "works" if no unfilled state is stuck.
Candidates (all on the state of T - v, link L = N(v), components = connected components of a two-colour subgraph):
  link_comps   number of two-colour components (over the 6 pairs) that meet L
  conn_pairs   number of colour pairs whose two-colour subgraph is disconnected  (fewer = more rigid)
  total_comps  total number of two-colour components over the 6 pairs
  locks        number of the two Birkhoff locks present (0, 1, 2) for the pattern c(x_j) = c(x_{j+2})
  link_spread  sum over pairs of the number of components meeting L, minus the number of pairs meeting L
  ring_pairs   number of pairs {i, i+2} of link vertices (cyclically) in DIFFERENT components of their two-colour subgraph
usage: potentials.py GRAPH.json HOLE   (Studio intel cert graph format {"faces": [...]}) or --plantri LINE HOLE"""
import itertools, json, sys
from collections import Counter


def load():
    if sys.argv[1] == "--plantri":
        rot = [[ord(c) - 97 for c in x] for x in sys.argv[2].split()[1].split(",")]
        adj = {v: set(nb) for v, nb in enumerate(rot)}; hole = int(sys.argv[3])
        link = list(rot[hole])
    else:
        F = json.load(open(sys.argv[1]))["faces"]; hole = int(sys.argv[2])
        adj = {}
        for f in F:
            for i in range(3):
                adj.setdefault(f[i], set()).add(f[(i + 1) % 3]); adj.setdefault(f[(i + 1) % 3], set()).add(f[i])
        succ = {f[(f.index(hole) + 1) % 3]: f[(f.index(hole) + 2) % 3] for f in F if hole in f}
        link = [next(iter(succ))]
        while len(link) < len(succ): link.append(succ[link[-1]])
    return adj, hole, link


def main():
    adj, hole, link = load()
    V = [v for v in adj if v != hole]
    A = {v: adj[v] - {hole} for v in V}
    order, seen = [link[0]], {link[0]}
    for x in order:
        for y in sorted(A[x]):
            if y not in seen: seen.add(y); order.append(y)
    pos = {v: i for i, v in enumerate(order)}
    states = []
    col = {}

    def rec(i, used):
        if i == len(order):
            states.append(tuple(col[v] for v in order)); return
        v = order[i]; forb = {col[w] for w in A[v] if w in col}
        for c in range(min(used + 1, 4)):
            if c not in forb:
                col[v] = c; rec(i + 1, max(used, c + 1)); del col[v]
    rec(0, 0)
    index = {s: k for k, s in enumerate(states)}

    def canon(c):
        mp = {}; return tuple(mp.setdefault(c[v], len(mp)) for v in order)

    def comps(c, p, q):
        Vs = {v for v in order if c[v] in (p, q)}; out = []; seen = set()
        for s in Vs:
            if s in seen: continue
            comp = {s}; st = [s]; seen.add(s)
            while st:
                x = st.pop()
                for y in A[x]:
                    if y in Vs and y not in seen: seen.add(y); comp.add(y); st.append(y)
            out.append(comp)
        return out

    L = set(link); pairs = list(itertools.combinations(range(4), 2))
    phis = {k: [] for k in ("link_comps", "conn_pairs", "total_comps", "locks", "link_spread", "ring_pairs")}
    nbrs, filled = [], []
    for s in states:
        c = dict(zip(order, s)); CP = {pq: comps(c, *pq) for pq in pairs}
        filled.append(len({c[x] for x in link}) <= 3)
        nb = set()
        for (p, q), cs in CP.items():
            for K in cs:
                d = dict(c)
                for v in K: d[v] = q if c[v] == p else p
                t = index[canon(d)]
                if t != index[s]: nb.add(t)
        nbrs.append(nb)
        phis["link_comps"].append(sum(1 for cs in CP.values() for K in cs if K & L))
        phis["conn_pairs"].append(sum(1 for cs in CP.values() if len(cs) > 1))
        phis["total_comps"].append(sum(len(cs) for cs in CP.values()))
        meet = [sum(1 for K in cs if K & L) for cs in CP.values()]
        phis["link_spread"].append(sum(meet) - sum(1 for m in meet if m))
        rp = 0
        for i in range(len(link)):
            a, b = link[i], link[(i + 2) % len(link)]
            pq = tuple(sorted((c[a], c[b])))
            if c[a] != c[b] and not any(a in K and b in K for K in CP[pq]): rp += 1
        phis["ring_pairs"].append(rp)
        lk = 0
        if not filled[-1]:
            n = len(link)
            for j in range(n):
                if c[link[j]] == c[link[(j + 2) % n]]:
                    m, a, b = link[(j + 1) % n], link[(j + 3) % n], link[(j + 4) % n]
                    for t in (a, b):
                        pq = tuple(sorted((c[m], c[t])))
                        lk += any(m in K and t in K for K in CP[pq])
                    break
        phis["locks"].append(lk)
    unfilled = [k for k in range(len(states)) if not filled[k]]
    out = {"hole": hole, "states": len(states), "unfilled": len(unfilled), "potentials": {}}
    for name, phi in phis.items():
        stuck = [k for k in unfilled if not any(phi[t] < phi[k] for t in nbrs[k])]
        out["potentials"][name] = {"stuck_unfilled_states": len(stuck), "works": not stuck,
                                   "phi_range_unfilled": [min(phi[k] for k in unfilled), max(phi[k] for k in unfilled)] if unfilled else None}
    print(json.dumps(out))


if __name__ == "__main__":
    main()
