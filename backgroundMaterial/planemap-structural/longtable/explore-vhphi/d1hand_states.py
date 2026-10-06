"""EXPLORATORY (D1-Hand). State-level census of the unfilled states on 17:0 / 17:1 that are locked for at
least one legal admitting fan.  Per state: word letters (D doubled, a = middle singleton u1, b = u3, g = u4),
which fans (roles M,L,R) are locked, per-locked-fan chain fullness, pair components/cyclomatic numbers in
letters, and the class degree-excess check  sum_{v in V_i}(deg_T v - 5) == n-4-3 n_i (+1 for a).
Usage: python3 d1hand_states.py PLANTRI"""
import sys, itertools, subprocess
from collections import Counter
import tilley_apex as TA, vhphi_explore as E, sep_any as SA, lock_anatomy as LA, d1hand_swaps as H
from d1hand_lib import pair_stats

plantri = sys.argv[1]
rows = []
for gi in (0, 1):
    line = subprocess.run([plantri, "-m5", "17", "-a"], capture_output=True, text=True).stdout.splitlines()[gi]
    rot = TA.parse(line); N = len(rot); adj = [set(r) for r in rot]
    for x in range(N):
        if len(rot[x]) != 5: continue
        ring = rot[x]
        legal = {f[0] for f in E.legal_fans(rot, x, adj)}
        starts = {}
        for j in legal:
            y = ring[j]; G = [set(a) for a in adj]; G[x].discard(y); G[y].discard(x)
            allc, comp = LA.classes(G, N)
            sepc = {comp[c] for c in allc if c[x] != c[y]}
            for c in allc:
                if c[x] == c[y] and len({c[w] for w in ring}) == 4:
                    starts.setdefault(SA.forget(c, x), []).append((j, comp[c] in sepc, c, G))
        for key, v in starts.items():
            locked = [(j, c, G) for j, s, c, G in v if not s]
            if not locked: continue
            c0 = locked[0][1]
            word = [c0[w] for w in ring]
            pD = [i for i in range(5) if word.count(word[i]) == 2]
            p = pD[0] if (pD[1] - pD[0]) % 5 == 2 else pD[1]
            u = [ring[(p + i) % 5] for i in range(5)]
            D, al, be, ga = c0[u[0]], c0[u[1]], c0[u[3]], c0[u[4]]
            nm = {D: "D", al: "a", be: "b", ga: "g"}
            ps = pair_stats(adj, c0, x, N)
            pst = {"".join(sorted(nm[k] for k in pr)): vv for pr, vv in ps.items()}
            fans = {}
            for j, c, G in locked:
                y = ring[j]; role = {1: "M", 3: "L", 4: "R"}[(j - p) % 5]
                fl = {}
                nmc = {c[u[0]]: "D", c[u[1]]: "a", c[u[3]]: "b", c[u[4]]: "g"}
                for o in set(range(4)) - {c[y]}:
                    fl[nmc[o]] = LA.chain(G, c, y, o) == {w for w in range(N) if c[w] in (c[y], o)}
                fans[role] = "".join(sorted(k for k, f in fl.items() if f))  # letters of FULL chains
            nl = len(locked); nadm = len(v)
            sizes = {nm[k]: sum(1 for w in range(N) if w != x and c0[w] == k) for k in nm}
            exc = {nm[k]: sum(len(adj[w]) - 5 for w in range(N) if w != x and c0[w] == k) for k in nm}
            rows.append((gi, x, "".join(["DaDbg"[i] for i in range(5)]), nl, nadm, tuple(sorted(fans.items())), tuple(sorted((k, vv) for k, vv in pst.items())), tuple(sorted(sizes.items())), tuple(sorted(exc.items()))))
agg = Counter((r[3], r[5], r[6]) for r in rows)
print("states with >=1 locked fan:", len(rows))
for (nl, fans, pst), cnt in sorted(agg.items(), key=lambda t: (-t[0][0], t[0][1])):
    print(f"#locked={nl} count={cnt}\n   full-chain letters per locked fan role: {dict(fans)}\n   pair (comps,cyc): {dict(pst)}")
print()
for r in rows:
    if r[3] == 3:
        print("TRIPLE", r[0], r[1], "fans", dict(r[5]), "sizes", dict(r[7]), "excess", dict(r[8]))
