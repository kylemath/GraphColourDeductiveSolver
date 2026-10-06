"""EXPLORATORY (D1-Hand). Census of ALL locked members on 17:0 and 17:1 (192). For each member c (a
colouring of T-x, class member of a locked G=T-xy class): word, apex role (M = middle singleton u1,
L = u3, R = u4), whether every chain {c(y),k} is the full colour pair (rigid), per-pair component
count and cyclomatic number in T-x (identity: sum comps - sum cyc = 8), number of legal admitting fans
that are locked for the state.  Usage: python3 d1hand_table.py PLANTRI"""
import sys, itertools, json
from collections import Counter, deque
import tilley_apex as TA, vhphi_explore as E, sep_any as SA, lock_anatomy as LA, d1hand_swaps as H

def pair_stats(adj, c, x, N):
    out = {}
    for a, b in itertools.combinations(range(4), 2):
        cs, idx = H.comps(adj, c, {a, b}, x)
        V = [w for w in range(N) if w != x and c[w] in (a, b)]
        e = sum(1 for u in V for w in adj[u] if w > u and w != x and c[w] in (a, b))
        out[(a, b)] = (len(cs), e - len(V) + len(cs))   # comps, cyclomatic
    return out

plantri = sys.argv[1]
out = []
for gi in (0, 1):
    line = subprocess.run if False else None
import subprocess
for gi in (0, 1):
    line = subprocess.run([plantri, "-m5", "17", "-a"], capture_output=True, text=True).stdout.splitlines()[gi]
    rot = TA.parse(line); N = len(rot); adj = [set(r) for r in rot]
    for x in range(N):
        if len(rot[x]) != 5: continue
        ring = rot[x]
        legal = {f[0] for f in E.legal_fans(rot, x, adj)}
        starts = {}; classes = {}
        for j in legal:
            y = ring[j]; G = [set(a) for a in adj]; G[x].discard(y); G[y].discard(x)
            allc, comp = LA.classes(G, N)
            sepc = {comp[c] for c in allc if c[x] != c[y]}
            for c in allc:
                if c[x] == c[y] and len({c[w] for w in ring}) == 4:
                    starts.setdefault(SA.forget(c, x), []).append((j, comp[c] in sepc, c, G))
        for key, v in starts.items():
            nloc = sum(1 for j, s, c, G in v if not s)
            nadm = len(v)
            for j, s, c, G in v:
                if s: continue
                y = ring[j]; one = c[y]
                word = [c[w] for w in ring]
                full = {}
                for o in sorted(set(range(4)) - {one}):
                    full[o] = LA.chain(G, c, y, o) == {w for w in range(N) if c[w] in (one, o)}
                # role of apex
                pD = [i for i in range(5) if word.count(word[i]) == 2]
                p = pD[0] if (pD[1] - pD[0]) % 5 == 2 else pD[1]
                role = {1: "M", 3: "L", 4: "R"}[(j - p) % 5]
                ps = pair_stats(adj, c, x, N)
                cyc = sum(v_[1] for v_ in ps.values()); comps = sum(v_[0] for v_ in ps.values())
                sizes = sorted(Counter(c[w] for w in range(N) if w != x).values())
                out.append(dict(g=gi, x=x, j=j, role=role, nlocked=nloc, nadm=nadm, rigid=all(full.values()),
                                comps=comps, cyc=cyc, sizes=sizes, pair=sorted((k, v_) for k, v_ in ps.items()),
                                key=str(key)))
print("members", len(out))
agg = Counter((m["rigid"], m["nlocked"], m["nadm"], m["comps"], m["cyc"]) for m in out)
print("(rigid, #locked admitting fans of the state, #legal admitting fans, sum comps, sum cyclomatic): members")
for k, v in sorted(agg.items()): print(" ", k, v)
agg2 = Counter((m["rigid"], m["role"]) for m in out); print("rigid x role:", dict(agg2))
print("sizes:", Counter(tuple(m["sizes"]) for m in out))
print("graph x vertices with non-rigid:", Counter((m["g"], m["x"], m["nlocked"]) for m in out if not m["rigid"]))
json.dump(out, open("/private/tmp/claude-501/-Users-fulkanjou-GraphColour/28402cc5-3e09-4c31-94e9-5ae923a5533c/scratchpad/d1hand_table.json", "w"))
