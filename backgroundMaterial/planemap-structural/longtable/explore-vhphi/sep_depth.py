"""EXPLORATORY. Separation depth: for each state with no separable admitting fan, the number
of pure Kempe swaps (hole x fixed) to reach a state separable for some admitting fan.
Usage: python3 sep_depth.py PLANTRI ORDER"""
import subprocess, sys
from collections import Counter, deque
import tilley_apex as TA, vhphi_explore as E, sep_any as SA

def main():
    plantri, order = sys.argv[1], int(sys.argv[2])
    flags = sys.argv[3].split() if len(sys.argv) > 3 else ["-m5"]
    assert order <= 18
    lines = subprocess.run([plantri] + flags + [str(order), "-a"], capture_output=True, text=True).stdout.splitlines()
    depth = Counter(); rows = []
    for gi, line in enumerate(lines):
        rot = TA.parse(line); n = len(rot); adj = [set(r) for r in rot]
        for x in range(n):
            if len(rot[x]) != 5: continue
            ring = rot[x]
            legal = {f[0] for f in E.legal_fans(rot, x, adj)}
            starts = {}
            for j in legal:
                y = ring[j]
                G = [set(a) for a in adj]; G[x].discard(y); G[y].discard(x)
                allc = [TA.canon(c) for c in TA.colourings(G, n)]
                good = {c for c in allc if c[x] != c[y]}
                q = deque(good)
                while q:
                    c = q.popleft()
                    for d in TA.kempe_nbrs(G, c):
                        if d not in good: good.add(d); q.append(d)
                for c in allc:
                    if c[x] == c[y] and len({c[w] for w in ring}) == 4:
                        starts.setdefault(SA.forget(c, x), []).append((j, c in good))
            sepset = {k for k, v in starts.items() if any(s for _, s in v)}
            def to_state(k):
                t = list(k); t.insert(x, E.HOLE); return E.canon(tuple(t))
            def to_key(st):
                return TA.canon(tuple(v for i, v in enumerate(st) if i != x))
            for k, v in starts.items():
                if k in sepset: continue
                st = to_state(k); seen = {st: 0}; q = deque([st]); d = None
                while q and d is None:
                    u = q.popleft()
                    for w in E.kempe_moves(rot, u):
                        if w in seen: continue
                        seen[w] = seen[u] + 1
                        if to_key(w) in sepset: d = seen[w]; break
                        q.append(w)
                depth[d] += 1
                rows.append((gi, x, d, [j for j, _ in v]))
    print("order", order, "bad states by separation depth:", dict(depth))
    for r in rows: print("  graph index %d vertex %d depth %s admitting fans %s" % r)

if __name__ == "__main__":
    main()
