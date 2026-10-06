"""EXPLORATORY (D1-Hand). For each SEP-bad state and each unlocking one-swap neighbour c', find a shortest
Kempe sequence in G = T - x y (x coloured c(y), whole components) from c' to a colouring with c(x) != c(y)
for each admitting fan y, and print its steps (pair, size of component, whether it contains x, y)."""
import sys, itertools
from collections import deque
import tilley_apex as TA, vhphi_explore as E, d1hand_swaps as H

def comp_of(G, col, s, pair):
    comp = {s}; st = [s]
    while st:
        u = st.pop()
        for w in G[u]:
            if w not in comp and col[w] in pair: comp.add(w); st.append(w)
    return comp

def shortest(G, start, x, y, maxd=8):
    start = tuple(start); seen = {start: None}; q = deque([(start, 0)])
    while q:
        c, d = q.popleft()
        if c[x] != c[y]:
            path = []; cur = c
            while seen[cur] is not None:
                prev, info = seen[cur]; path.append(info); cur = prev
            return d, path[::-1]
        if d >= maxd: continue
        n = len(c)
        for a, b in itertools.combinations(range(4), 2):
            done = set()
            for s in range(n):
                if c[s] not in (a, b) or s in done: continue
                K = comp_of(G, c, s, (a, b)); done |= K
                nc = list(c)
                for w in K: nc[w] = b if c[w] == a else a
                nc = tuple(nc)
                if nc not in seen:
                    seen[nc] = (c, (a, b, len(K), x in K, y in K, sorted(K)))
                    q.append((nc, d + 1))
    return None, None

plantri = sys.argv[1]
only = int(sys.argv[2]) if len(sys.argv) > 2 else None
for gi in (0, 1):
    rows, rot = H.analyse(plantri, gi)
    adj = [set(r) for r in rot]
    for r in rows:
        x = r["x"]; u = r["u"]; ring = rot[x]; word = r["word(u0..u4)"]
        nm = {word[0]: "D", word[1]: "a", word[3]: "b", word[4]: "g"}
        print(f"\n17:{gi} x={x} u={u} word=DaDbg")
        seenstate = set()
        for (pair, size, ur, status, w2, c2, K) in r["swaps"]:
            if not status.startswith("SEP"): continue
            key = TA.canon(tuple(c2[i] for i in range(len(c2)) if i != x))
            if key in seenstate: continue
            seenstate.add(key)
            print(f"  neighbour: swap {''.join(nm[p] for p in pair)} K ring u-idx {ur} -> {status}")
            word2 = [c2[w] for w in ring]
            for i in range(5):
                y = u[i]
                if word2.count(c2[y]) != 1: continue
                G = [set(a) for a in adj]; G[x].discard(y); G[y].discard(x)
                c = list(c2); c[x] = c2[y]
                d, path = shortest(G, c, x, y)
                print(f"     fan apex u{i}: G-distance {d}")
                nn0 = {c2[u[0]]: 'D', c2[u[1]]: 'a', c2[u[3]]: 'b', c2[u[4]]: 'g'}
                if path:
                    for p in path:
                        a, b, sz, hx, hy, Kk = p
                        nn = nm
                        print(f"        swap {nn[a]}{nn[b]} |comp|={sz} contains x:{hx} y:{hy}  ring-u in comp: {[j for j in range(5) if u[j] in Kk]} comp={Kk}")
