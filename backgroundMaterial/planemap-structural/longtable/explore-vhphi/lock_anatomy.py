"""EXPLORATORY. Anatomy of Tilley-locked classes on 17:1 (and 17:0). Long Table 2026-10-05.

For each locked apex pair (x, y): list the locked starts as colourings c of G = T - xy with
c(x) = c(y). For each: (a) the Kempe class size in G, (b) whether the pure Kempe class of the
corresponding state (hole x, colouring of T - x) in T - x contains a filled state,
(c) the link word at x, (d) the chains: sizes of the {1,k} chains containing x and y, and
whether x's three chains are the same components as y's (that is the lock).

Usage: python3 lock_anatomy.py PLANTRI GRAPH_INDEX
"""
import itertools
import subprocess
import sys
from collections import Counter, deque

import tilley_apex as TA
import vhphi_explore as E


def classes(G, n):
    allc = [TA.canon(c) for c in TA.colourings(G, n)]
    comp = {}
    cid = 0
    for c in allc:
        if c in comp:
            continue
        comp[c] = cid
        q = deque([c])
        while q:
            u = q.popleft()
            for d in TA.kempe_nbrs(G, u):
                if d not in comp:
                    comp[d] = cid
                    q.append(d)
        cid += 1
    return allc, comp


def chain(G, st, v, other):
    a = st[v]
    seen, stack = {v}, [v]
    while stack:
        u = stack.pop()
        for w in G[u]:
            if w not in seen and st[w] in (a, other):
                seen.add(w)
                stack.append(w)
    return seen


def main():
    plantri, gi = sys.argv[1], int(sys.argv[2])
    line = subprocess.run([plantri, "-m5", "17", "-a"], capture_output=True, text=True).stdout.splitlines()[gi]
    rot = TA.parse(line)
    n = len(rot)
    adj = [set(r) for r in rot]
    for x in range(n):
        if len(rot[x]) != 5:
            continue
        legal = {f[0] for f in E.legal_fans(rot, x, adj)}
        for i, y in enumerate(rot[x]):
            if i not in legal:
                continue
            G = [set(a) for a in adj]
            G[x].discard(y)
            G[y].discard(x)
            allc, comp = classes(G, n)
            sep_cls = {comp[c] for c in allc if c[x] != c[y]}
            locked_cls = {comp[c] for c in allc if c[x] == c[y]} - sep_cls
            if not locked_cls:
                continue
            sizes = Counter(comp[c] for c in allc)
            # pure class at hole x in T - x
            rotlike = [sorted(a) for a in adj]
            rotlike[x] = list(rot[x])
            Tx = [set(a) for a in adj]
            print(f"pair x={x} y={y} deg y={len(rot[y])} link degs={[len(rot[w]) for w in rot[x]]} "
                  f"locked classes={len(locked_cls)} sizes={[sizes[k] for k in sorted(locked_cls)]}")
            for k in sorted(locked_cls):
                members = [c for c in allc if comp[c] == k]
                c0 = members[0]
                # hole state at x: remove x colour
                st = list(c0)
                st[x] = E.HOLE
                st = tuple(E.canon(st)) if False else tuple(st)
                # pure class in T - x
                seen = {st}
                q = deque([st])
                fill = False
                while q and len(seen) < 200000:
                    u = q.popleft()
                    if E.filled(rot, u):
                        fill = True
                        break
                    for d in E.kempe_moves(rot, u):
                        if d not in seen:
                            seen.add(d)
                            q.append(d)
                link = [c0[w] for w in rot[x]]
                ch = [(chain(G, c0, x, o) == chain(G, c0, y, o), len(chain(G, c0, x, o)))
                      for o in sorted(set(range(4)) - {c0[x]})]
                print(f"   class size {len(members)}; pure class at hole x reaches fill: {fill}; "
                      f"link word {link}; chains x~y same? (same, |chain|) {ch}")


if __name__ == "__main__":
    main()
