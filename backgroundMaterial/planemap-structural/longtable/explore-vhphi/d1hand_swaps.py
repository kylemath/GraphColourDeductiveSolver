"""EXPLORATORY (D1-Hand team). For each SEP-bad (all admitting fans locked) state at a degree-5
vertex of 17:0 / 17:1: write the ring word u0..u4 (u0,u2 the doubled colour D; u1,u3,u4 singletons),
test path conditions P13 (u1~u3 in the pair-subgraph of T-x on colours c(u1),c(u3)) and
P14 (u1~u4), the component structure of the pair subgraphs of T-x, and classify EVERY single
Kempe swap of T-x (component K of a bichromatic subgraph of T-x): does the resulting state
become separable for some admitting fan, and which K is it.
Usage: python3 d1hand_swaps.py PLANTRI GRAPH_INDEX"""
import subprocess, sys, itertools
from collections import deque, Counter
import tilley_apex as TA, vhphi_explore as E, sep_any as SA

def comps(adj, col, S, x):
    """components of the subgraph of T-x induced on vertices with colour in S"""
    seen = {}; out = []
    for s in range(len(col)):
        if s == x or col[s] not in S or s in seen: continue
        comp = {s}; st = [s]
        while st:
            u = st.pop()
            for w in adj[u]:
                if w != x and w not in comp and col[w] in S: comp.add(w); st.append(w)
        for u in comp: seen[u] = len(out)
        out.append(comp)
    return out, seen

def analyse(plantri, gi, want_x=None, verbose=True):
    line = subprocess.run([plantri, "-m5", "17", "-a"], capture_output=True, text=True).stdout.splitlines()[gi]
    rot = TA.parse(line); n = len(rot); adj = [set(r) for r in rot]
    rows = []
    for x in range(n):
        if len(rot[x]) != 5: continue
        if want_x is not None and x != want_x: continue
        ring = rot[x]
        legal = {f[0] for f in E.legal_fans(rot, x, adj)}
        starts = {}
        for j in legal:
            y = ring[j]; G = [set(a) for a in adj]; G[x].discard(y); G[y].discard(x)
            allc = [TA.canon(c) for c in TA.colourings(G, n)]
            good = {c for c in allc if c[x] != c[y]}; q = deque(good)
            while q:
                c = q.popleft()
                for d in TA.kempe_nbrs(G, c):
                    if d not in good: good.add(d); q.append(d)
            for c in allc:
                if c[x] == c[y] and len({c[w] for w in ring}) == 4:
                    starts.setdefault(SA.forget(c, x), []).append((j, c in good, c))
        sepset = {k for k, v in starts.items() if any(s for _, s, _ in v)}
        for k, v in starts.items():
            if k in sepset: continue
            c = list(v[0][2]); c[x] = -1  # x uncoloured
            word = [c[w] for w in ring]
            # doubled colour positions
            D = [col for col in set(word) if word.count(col) == 2][0]
            pD = [i for i in range(5) if word[i] == D]
            # rotate so that u0,u2 are D
            if (pD[1] - pD[0]) % 5 == 2: p = pD[0]
            else: p = pD[1]
            u = [ring[(p + i) % 5] for i in range(5)]
            col = {i: c[u[i]] for i in range(5)}
            al, be, ga = col[1], col[3], col[4]
            def conn(a, b, S):
                cs, idx = comps(adj, c, S, x); return idx[a] == idx[b]
            P13 = conn(u[1], u[3], {al, be}); P14 = conn(u[1], u[4], {al, ga})
            info = {"graph": gi, "x": x, "u": u, "word(u0..u4)": [col[i] for i in range(5)], "P13": P13, "P14": P14}
            # component structure of pair subgraphs of T-x
            pc = {}
            for a, b in itertools.combinations(range(4), 2):
                cs, idx = comps(adj, c, {a, b}, x)
                pc[(a, b)] = [sorted(K) for K in cs]
            info["pair_comps"] = {f"{a}{b}": len(v) for (a, b), v in pc.items()}
            info["Dga_comps_u2|u0u4"] = None
            # swaps
            res = []
            for a, b in itertools.combinations(range(4), 2):
                cs, idx = comps(adj, c, {a, b}, x)
                for K in cs:
                    c2 = list(c)
                    for w in K: c2[w] = b if c[w] == a else a
                    key = TA.canon(tuple(vv for i, vv in enumerate(c2) if i != x))
                    ringcols = {c2[w] for w in ring}
                    if len(ringcols) < 4: status = "FILLED"
                    elif key in sepset:
                        fans = [j for j, g, _ in starts[key] if g]
                        status = "SEP fans=" + str(fans)
                    else: status = "locked"
                    ur = [i for i in range(5) if u[i] in K]
                    res.append(((a, b), len(K), ur, status, [c2[u[i]] for i in range(5)], tuple(c2), sorted(K)))
            info["swaps"] = res; info["c"] = tuple(c)
            rows.append(info)
    return rows, rot

if __name__ == "__main__":
    plantri, gi = sys.argv[1], int(sys.argv[2])
    rows, rot = analyse(plantri, gi)
    for r in rows:
        print({k: v for k, v in r.items() if k != "swaps"})
        for s in r["swaps"]:
            if s[2] or s[3] != "locked":
                print("   swap pair", s[0], "|K|", s[1], "ring pos in K (u-index)", s[2], "->", s[3], "new word", s[4])
