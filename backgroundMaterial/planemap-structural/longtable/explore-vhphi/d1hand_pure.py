"""EXPLORATORY (D1-Hand). Pure distance (Kempe swaps at hole x of T-x) from each SEP-bad state to a filled
state, and the distance from each distinct neighbour. Usage: python3 d1hand_pure.py PLANTRI"""
import sys
from collections import deque
import tilley_apex as TA, vhphi_explore as E, d1hand_swaps as H

def dist_to_fill(rot, st, cap=7):
    seen = {st: 0}; q = deque([st])
    while q:
        u = q.popleft()
        if E.filled(rot, u): return seen[u]
        if seen[u] >= cap: continue
        for w in E.kempe_moves(rot, u):
            if w not in seen: seen[w] = seen[u] + 1; q.append(w)
    return None

plantri = sys.argv[1]
for gi in (0, 1):
    rows, rot = H.analyse(plantri, gi); n = len(rot)
    for r in rows:
        x = r["x"]; u = r["u"]; word = r["word(u0..u4)"]
        nm = {word[0]: "D", word[1]: "a", word[3]: "b", word[4]: "g"}
        def st_of(c2):
            t = list(c2); t[x] = E.HOLE; return E.canon(tuple(t))
        s0 = st_of(r["c"])
        print(f"17:{gi} x={x}: pure distance to fill from state = {dist_to_fill(rot, s0)}; pair comps {r['pair_comps']}")
        seen = {}
        for (pair, size, ur, status, w2, c2, K) in r["swaps"]:
            s1 = st_of(c2)
            if s1 == s0 or s1 in seen: continue
            seen[s1] = 1
            print(f"    neighbour swap {''.join(nm[p] for p in pair)} ring-u {ur} |K|={size}: pure dist {dist_to_fill(rot, s1)} {status}")
