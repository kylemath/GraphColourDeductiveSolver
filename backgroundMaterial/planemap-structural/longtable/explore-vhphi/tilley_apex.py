"""EXPLORATORY. Tilley separability of apex fans (literature-check.md bridge). Long Table 2026-10-05.

For a degree-5 vertex x and neighbour y whose apex fan is legal (T/xy simple), the starts at
(x, tau_y) are the colourings of T/xy, i.e. colourings of G = T - xy with c(x) = c(y).
A start is *Tilley-separable* if Kempe changes in G (whole components, x coloured) reach a
colouring with c(x) != c(y). By the bridge, a separable start has a pure fill at x.
Reports, per pair, the number of non-separable starts, and whether a Birkhoff diamond
(4 degree-5 vertices a,b,c,d with faces abd, cbd) has x or y among its 6 ring vertices.

Usage: plantri ... -a | python3 tilley_apex.py N OUT.json [WORKERS]   (N <= 17)
"""
import itertools
import json
import sys
from collections import deque
from multiprocessing import Pool

import vhphi_explore as E

PAIRS = list(itertools.combinations(range(4), 2))


def parse(line):
    _, body = line.split()
    return [[ord(c) - 97 for c in r] for r in body.split(",")]


def canon(st):
    seen = {}
    return tuple(seen.setdefault(x, len(seen)) for x in st)


def colourings(adj, n):
    order = list(range(n))
    cur = [0] * n
    out = []

    def go(i, top):
        if i == n:
            out.append(tuple(cur))
            return
        blocked = {cur[j] for j in adj[i] if j < i}
        for a in range(min(3, top + 1) + 1):
            if a not in blocked:
                cur[i] = a
                go(i + 1, max(top, a))

    go(0, -1)
    return out


def kempe_nbrs(adj, st):
    n = len(st)
    for a, b in PAIRS:
        seen = set()
        for s in range(n):
            if st[s] not in (a, b) or s in seen:
                continue
            comp = {s}
            stack = [s]
            while stack:
                u = stack.pop()
                for w in adj[u]:
                    if w not in comp and st[w] in (a, b):
                        comp.add(w)
                        stack.append(w)
            seen |= comp
            nxt = list(st)
            for u in comp:
                nxt[u] = b if st[u] == a else a
            yield canon(nxt)


def diamonds(rot, adj):
    """Birkhoff diamonds: degree-5 a,b,c,d with b~d, a~b,a~d,c~b,c~d, a !~ c; ring = N(abcd) minus them."""
    n = len(rot)
    d5 = {v for v in range(n) if len(rot[v]) == 5}
    out = []
    for b in d5:
        for d in adj[b]:
            if d <= b or d not in d5:
                continue
            common = [w for w in adj[b] & adj[d] if w in d5]
            for a, c in itertools.combinations(common, 2):
                if c in adj[a]:
                    continue
                core = {a, b, c, d}
                ring = set().union(*(adj[v] for v in core)) - core
                out.append((tuple(sorted(core)), tuple(sorted(ring))))
    return out


def examine(args):
    idx, line = args
    rot = parse(line)
    n = len(rot)
    adj = [set(r) for r in rot]
    dia = diamonds(rot, adj)
    recs = []
    for x in range(n):
        if len(rot[x]) != 5:
            continue
        legal = {f[0]: f for f in E.legal_fans(rot, x, adj)}
        for i, y in enumerate(rot[x]):
            if i not in legal:
                continue
            G = [set(a) for a in adj]
            G[x].discard(y)
            G[y].discard(x)
            allc = [canon(c) for c in colourings(G, n)]
            starts = [c for c in allc if c[x] == c[y]]
            # flood from separated colourings backwards (Kempe moves are reversible)
            sep = {c for c in allc if c[x] != c[y]}
            good = set(sep)
            q = deque(sep)
            while q:
                c = q.popleft()
                for d in kempe_nbrs(G, c):
                    if d not in good:
                        good.add(d)
                        q.append(d)
            locked = [c for c in starts if c not in good]
            near = [D for D in dia if x in D[1] or y in D[1] or x in D[0] or y in D[0]]
            recs.append({"idx": idx, "x": x, "y": y, "deg_y": len(rot[y]), "starts": len(starts),
                         "locked_starts": len(locked), "diamond_near": len(near)})
    return recs


def main():
    n = int(sys.argv[1])
    assert n <= 18
    lines = [l for l in sys.stdin if l.strip()]
    workers = int(sys.argv[3]) if len(sys.argv) > 3 else 12
    res = []
    with Pool(workers) as pool:
        for r in pool.imap_unordered(examine, enumerate(lines), chunksize=8):
            res.extend(r)
    pairs = len(res)
    locked_pairs = [r for r in res if r["locked_starts"]]
    with_d = [r for r in res if r["diamond_near"]]
    print("order", n, "graphs", len(lines), "apex pairs", pairs,
          "pairs with a locked start", len(locked_pairs),
          "of which diamond-near", sum(1 for r in locked_pairs if r["diamond_near"]),
          "| diamond-near pairs", len(with_d), flush=True)
    json.dump({"order": n, "records": res}, open(sys.argv[2], "w"))


if __name__ == "__main__":
    main()
