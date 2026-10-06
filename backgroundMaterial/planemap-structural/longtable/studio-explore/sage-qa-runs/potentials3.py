#!/usr/bin/env python3
"""[exploratory] Sage QA run 5 (coordinator's list). For a degree-5 hole v of T: all 4-colourings of T - v up to renaming,
Kempe moves = whole two-colour components. For each candidate Phi (and for -Phi), count the UNFILLED states (link on 4 colours)
where no single move strictly lowers Phi ("stuck"). A candidate "works" iff no unfilled state is stuck. Tuples compare
lexicographically.
Link x_0..x_4 in cyclic order; for an unfilled state the repeat is c(x_j) = c(x_{j+2}); m = x_{j+1}, a = x_{j+3}, b = x_{j+4};
alpha = c(x_j), mu = c(m), A = c(a), B = c(b). Lock chains: the {mu,A}-component and the {mu,B}-component containing m.
Candidates:
  conn_pairs        number of colour pairs (of 6) whose two-colour subgraph is connected
  link_comps        number of two-colour components meeting the link (over all 6 pairs)
  link_comps_max    max over pairs of the number of components of that pair meeting the link
  lock_size         |{mu,A}-chain of m| + |{mu,B}-chain of m|
  lock_dist         sum over the two locks of the path length m -> a (resp. b) inside its chain (0 if not in the chain)
  K                 Intern D's vector (kappa_alpha, kappa_mu, kappa_A, kappa_B), kappa_c = sum of (6 - deg_T u) over colour class c
  Phi_beta/gamma/delta   kappa_alpha + kappa_mu / + kappa_A / + kappa_B (Intern D's Phi by role, coset_potential.py convention)
  lex_1_2_3         (conn_pairs, link_comps, lock_size)
  lex_3_1_2         (lock_size, conn_pairs, link_comps)
usage: potentials2.py --faces FILE.json HOLE | --plantri "LINE" HOLE"""
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
    while len(L) < len(nbr):  # walk the link cycle
        L.append([w for w in adj[L[-1]] if w in adj[hole] and w not in L][0])
    return adj, hole, L


def main():
    adj, hole, link = load()
    deg = {v: len(adj[v]) for v in adj}
    V = [v for v in adj if v != hole]; A = {v: adj[v] - {hole} for v in V}
    order, seen = [link[0]], {link[0]}
    for x in order:
        for y in sorted(A[x]):
            if y not in seen: seen.add(y); order.append(y)
    states, col = [], {}

    def rec(i, used):
        if i == len(order): states.append(tuple(col[v] for v in order)); return
        v = order[i]; forb = {col[w] for w in A[v] if w in col}
        for c in range(min(used + 1, 4)):
            if c not in forb: col[v] = c; rec(i + 1, max(used, c + 1)); del col[v]
    rec(0, 0)
    index = {s: k for k, s in enumerate(states)}
    canon = lambda c: (lambda mp: tuple(mp.setdefault(c[v], len(mp)) for v in order))({})

    def comps(c, p, q):
        Vs = {v for v in order if c[v] in (p, q)}; out = []; sn = set()
        for s in Vs:
            if s in sn: continue
            comp = {s}; st = [s]; sn.add(s)
            while st:
                x = st.pop()
                for y in A[x]:
                    if y in Vs and y not in sn: sn.add(y); comp.add(y); st.append(y)
            out.append(comp)
        return out

    def pathlen(K, s, t):
        dist = {s: 0}; q = deque([s])
        while q:
            x = q.popleft()
            if x == t: return dist[x]
            for y in A[x]:
                if y in K and y not in dist: dist[y] = dist[x] + 1; q.append(y)
        return 0
    L = set(link); pairs = list(itertools.combinations(range(4), 2)); kk = {v: 6 - deg[v] for v in V}
    phi, nbrs, unf = {}, [], []
    for si, s in enumerate(states):
        c = dict(zip(order, s)); CP = {pq: comps(c, *pq) for pq in pairs}
        nb = set()
        for (p, q), cs in CP.items():
            for K in cs:
                d = dict(c)
                for v in K: d[v] = q if c[v] == p else p
                t = index[canon(d)]
                if t != si: nb.add(t)
        nbrs.append(nb)
        lc = [c[x] for x in link]
        if len(set(lc)) <= 3: unf.append(False); continue
        unf.append(True)
        j = [j for j in range(5) if lc[j] == lc[(j + 2) % 5]][0]
        al, mu, Ac, Bc = lc[j], lc[(j + 1) % 5], lc[(j + 3) % 5], lc[(j + 4) % 5]
        m, a, b = link[(j + 1) % 5], link[(j + 3) % 5], link[(j + 4) % 5]
        ch = {}
        for t, ct in ((a, Ac), (b, Bc)):
            K = [K for K in CP[tuple(sorted((mu, ct)))] if m in K][0]; ch[t] = K
        kap = [sum(kk[v] for v in V if c[v] == x) for x in range(4)]
        Kv = (kap[al], kap[mu], kap[Ac], kap[Bc])
        f = {"conn_pairs": sum(1 for cs in CP.values() if len(cs) == 1),
             "link_comps": sum(1 for cs in CP.values() for K in cs if K & L),
             "link_comps_max": max(sum(1 for K in cs if K & L) for cs in CP.values()),
             "lock_size": len(ch[a]) + len(ch[b]),
             "lock_dist": (pathlen(ch[a], m, a) if a in ch[a] else 0) + (pathlen(ch[b], m, b) if b in ch[b] else 0),
             "K": Kv, "Phi_beta": Kv[0] + Kv[1], "Phi_gamma": Kv[0] + Kv[2], "Phi_delta": Kv[0] + Kv[3]}
        f["lex_1_2_3"] = (f["conn_pairs"], f["link_comps"], f["lock_size"])
        f["lex_3_1_2"] = (f["lock_size"], f["conn_pairs"], f["link_comps"])
        phi[si] = f
    names = list(next(iter(phi.values())).keys()) if phi else []
    U = [k for k in range(len(states)) if unf[k]]
    neg = lambda x: tuple(-y for y in x) if isinstance(x, tuple) else -x
    out = {"hole": hole, "states": len(states), "unfilled": len(U), "candidates": {}}
    for nm in names:
        res = {}
        for sign, g in (("lower", lambda x: x), ("raise", neg)):
            # a move into a filled state always counts as progress (it reaches the target)
            stuck = [k for k in U if not any((not unf[t]) or g(phi[t][nm]) < g(phi[k][nm]) for t in nbrs[k])]
            res[sign] = len(stuck)
        out["candidates"][nm] = res
    if "--leastk" in sys.argv:
        # distance of every state to the filled set (its radius-like depth)
        from collections import deque as _dq
        dist = [-1] * len(states); q = _dq(k for k in range(len(states)) if not unf[k])
        for k in q: dist[k] = 0
        while q:
            x = q.popleft()
            for t in nbrs[x]:
                if dist[t] < 0: dist[t] = dist[x] + 1; q.append(t)
        out["leastk"] = {}
        for nm in ("lock_size", "lock_dist", "lexsd"):
            val = (lambda k: (phi[k]["lock_size"], phi[k]["lock_dist"])) if nm == "lexsd" else (lambda k, nm=nm: phi[k][nm])
            hist, pairs = {}, {}
            for k0 in U:
                v0 = val(k0); seen = {k0}; frontier = [k0]; kk = 0; found = None
                while frontier and found is None:
                    kk += 1; nxt = []
                    for x in frontier:
                        for t in nbrs[x]:
                            if t in seen: continue
                            seen.add(t)
                            if (not unf[t]) or val(t) < v0: found = kk; break
                            nxt.append(t)
                        if found: break
                    frontier = nxt
                hist[str(found)] = hist.get(str(found), 0) + 1
                pairs["%s|%s" % (dist[k0], found)] = pairs.get("%s|%s" % (dist[k0], found), 0) + 1
            out["leastk"][nm] = {"hist": hist, "dist_to_fill|least_k": pairs}
    print(json.dumps(out))


if __name__ == "__main__":
    main()
