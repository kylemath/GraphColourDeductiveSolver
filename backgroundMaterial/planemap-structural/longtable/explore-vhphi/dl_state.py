"""EXPLORATORY. Dissect one doubly-locked state (no separable admitting fan): 17:1 vertex 5."""
import subprocess, sys
from collections import deque
import tilley_apex as TA, vhphi_explore as E, sep_any as SA

plantri, gi, X = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
line = subprocess.run([plantri, "-m5", "17", "-a"], capture_output=True, text=True).stdout.splitlines()[gi]
rot = TA.parse(line); n = len(rot); adj = [set(r) for r in rot]; deg = [len(a) for a in adj]
x = X; ring = rot[x]
print("link of x (rotation):", ring, "degrees", [deg[w] for w in ring])
legal = {f[0] for f in E.legal_fans(rot, x, adj)}
starts = {}; goods = {}
for j in legal:
    y = ring[j]; G = [set(a) for a in adj]; G[x].discard(y); G[y].discard(x)
    allc = [TA.canon(c) for c in TA.colourings(G, n)]
    good = {c for c in allc if c[x] != c[y]}; q = deque(good)
    while q:
        c = q.popleft()
        for d in TA.kempe_nbrs(G, c):
            if d not in good: good.add(d); q.append(d)
    goods[j] = good
    for c in allc:
        if c[x] == c[y] and len({c[w] for w in ring}) == 4:
            starts.setdefault(SA.forget(c, x), []).append((j, c in good, c))
bad = [k for k, v in starts.items() if not any(s for _, s, _ in v)]
print("doubly-locked states at this vertex:", len(bad))
k = bad[0]
v = starts[k]
c = v[0][2]
print("state colouring c (index: colour):", {w: c[w] for w in range(n) if w != x})
print("link word", [c[w] for w in ring], " singletons at ring positions", [i for i in range(5) if [c[w] for w in ring].count(c[ring[i]]) == 1])
for j, s, cc in v:
    y = ring[j]
    cs = list(cc)
    chains = {}
    for o in sorted(set(range(4)) - {cc[y]}):
        a = cc[y]; seen = {y}; st = [y]
        G = [set(a_) for a_ in adj]; G[x].discard(y); G[y].discard(x)
        while st:
            u = st.pop()
            for w in G[u]:
                if w not in seen and cc[w] in (a, o): seen.add(w); st.append(w)
        chains[o] = sorted(seen)
    print(f" fan j={j} apex y={y} separable={s}; chain from y in colour pair with each other colour:")
    for o, ch in chains.items(): print(f"    {{{cc[y]},{o}}}: size {len(ch)} contains x? {x in ch}  {ch}")
# escape: single swaps from the state
st = list(c); st[x] = E.HOLE; st = tuple(st)
print("one-swap neighbours that are separable for some admitting fan:")
cnt = 0
for nb in E.kempe_moves(rot, st):
    key = TA.canon(tuple(vv for i, vv in enumerate(nb) if i != x))
    sepk = [j for j in legal if any(key == SA.forget(cc2, x) and good for j2, good, cc2 in starts.get(key, []) if j2 == j)]
    if sepk:
        cnt += 1
        diff = [w for w in range(n) if w != x and TA.canon(tuple(vv for i, vv in enumerate(nb) if i != x))[w if w < x else w - 1] != TA.canon(tuple(vv for i, vv in enumerate(st) if i != x))[w if w < x else w - 1]]
        print("   swap changes colours of", len([w for w in range(n) if w!=x and nb[w]!=st[w]]), "vertices; separable fans", sepk)
print("count", cnt)
