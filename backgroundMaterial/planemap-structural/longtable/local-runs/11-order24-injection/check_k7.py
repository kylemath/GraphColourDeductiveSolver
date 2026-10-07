#!/usr/bin/env python3
"""[exploratory] Re-check the first k_min = 7 case (order 24, gentri 1460, hole 19, j = 4) with a separate, direct computation:
for each DD_4 state of the class, the BFS distance (in the full move graph, plain kempe_py) to the nearest unit of room_4, and
the distinct units at each distance. usage: check_k7.py > check-k7.json"""
import json, os, sys
from collections import deque
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, "..", "common")); sys.path.insert(0, os.path.join(H, "..", "8-quarter-identities"))
sys.argv = ["x"]
from kempe_py import gentri_rotation
import qf
GENTRI = os.path.join(H, "..", "..", "..", "studiointel", "gentri")
line = [x for x in open(os.path.join(GENTRI, "tri24.txt")) if x.strip()][1460]
rot = gentri_rotation(line); hole = 19; J = 4
qf.MATCH = True
r = qf.analyse(rot, hole)
cls = [k for k in r["classes"] if k.get("DDmatch") and any(m["j"] == J and m["k_min"] == 7 for m in k["DDmatch"])]
print(json.dumps({"order": 24, "gentri_index": 1460, "hole": hole, "plantri_style": "%d %s" % (len(rot), ",".join("".join(chr(97 + w) for w in x) for x in rot)),
                  "class": {a: cls[0][a] for a in ("size", "F", "U", "N0", "D", "D_cyc", "L_F", "dP_hist", "DD", "DDmatch", "DDloc")}}, indent=1))

# ---- independent recomputation (no qf code): locks, long bits, units of room_4, DD_4, BFS distances ----
from kempe_py import Space, adj_from_rot
from collections import Counter
S = Space(adj_from_rot(rot), hole, link=rot[hole]); S.build_graph(); cl, _ = S.classes(); L = S.linki


def j_(fn, c, cm, u, w, cols): return bool(S.flood(1 << u, cm[cols[0]] | cm[cols[1]]) >> w & 1)


def desc(s):
    c = S.states[s]; cm = S.cmasks(c); lc = [c[x] for x in L]
    if len(set(lc)) <= 3:
        i = [t for t in range(5) if lc.count(lc[t]) == 1][0]; x = [L[(i + t) % 5] for t in range(5)]
        W, X, Y = lc[i], lc[(i + 1) % 5], lc[(i + 2) % 5]; Z = 6 - W - X - Y
        return ("F", i, j_(0, c, cm, x[2], x[4], (Y, Z)), j_(0, c, cm, x[1], x[3], (X, Z)))
    j = [t for t in range(5) if lc[t] == lc[(t + 2) % 5]][0]; x = [L[(j + t) % 5] for t in range(5)]
    mu, A, B, al = lc[(j + 1) % 5], lc[(j + 3) % 5], lc[(j + 4) % 5], lc[j]
    l1 = j_(0, c, cm, x[1], x[3], (mu, A)); l2 = j_(0, c, cm, x[1], x[4], (mu, B))
    r3 = S.index[S.swap(c, S.flood(1 << x[2], cm[al] | cm[A]), al, A)] if l2 else None
    return ("U", j, l1, l2, r3)
D = {s: desc(s) for s in range(len(S.states))}
dl = lambda s: D[s][0] == "U" and D[s][2] and D[s][3]
target = cl[[s for s in range(len(S.states)) if D[s][0] == "U" and D[s][1] == J and dl(s) and dl(D[s][4])][0]]
C = [s for s in range(len(S.states)) if cl[s] == target]
units = [s for s in C if (D[s][0] == "F" and ((D[s][1] == (J + 4) % 5 and D[s][2]) or (D[s][1] in ((J + 3) % 5, (J + 1) % 5) and D[s][3])))
         or (D[s][0] == "U" and not D[s][2] and not D[s][3] and D[s][1] in (J, (J + 3) % 5))
         or (D[s][0] == "U" and D[s][1] == J and not D[s][2] and D[s][3] and not dl(D[s][4]))]
DDJ = [s for s in C if D[s][0] == "U" and D[s][1] == J and dl(s) and dl(D[s][4])]
dist = {u: 0 for u in units}; q = deque(units)
while q:
    x = q.popleft()
    for t in S.G[x]:
        if t not in dist: dist[t] = dist[x] + 1; q.append(t)
print(json.dumps({"independent_check": {"class_size": len(C), "room_4_units": len(units), "DD_4": len(DDJ),
                                        "nearest_room4_unit_distance_per_DD4_state": sorted(dist[s] for s in DDJ)}}))
