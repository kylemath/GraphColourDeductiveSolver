"""[exploratory] Item 19 task 4 (cont.): abstract swap distance (swaps.py moves on all proper link words) from the unfilled rep u to every filled word,
versus membership in the minimal valid S. For every minimal S of the 12-24 data: histogram of distances of its members; and for the smallest S.
usage: pattern2.py TAG > pattern2-TAG.json"""
import itertools, json, sys
from collections import Counter, deque
import lib, swaps
tag = sys.argv[1]; L = json.load(open("laws-%s.json" % tag)); out = {}
def moves(w):
    res = set(); d = len(w)
    for p, q in itertools.combinations(range(4), 2):
        R = swaps.runs(w, p, q)
        for r in range(1, len(R) + 1):
            for sub in itertools.combinations(R, r):
                K = set(x for c in sub for x in c); t = swaps.flip(w, K, p, q)
                if t != w: res.add(t)
    return res
for d in (5, 6, 7):
    D = lib.Deg(d); mv = {w: moves(w) for w in D.seqs}; rows = []
    for o in L[str(d)]["orbits"]:
        u = tuple(int(c) for c in o["rep"]); dist = {u: 0}; q = deque([u])
        while q:
            x = q.popleft()
            for y in mv[x]:
                if y not in dist: dist[y] = dist[x] + 1; q.append(y)
        fd = {"".join(map(str, w)): dist[w] for w in D.seqs if lib.is_filled(w) and w in dist}
        allS = o["minimal_valid_S"]; mins = min(map(len, allS)); sm = [S for S in allS if len(S) == mins]
        rows.append({"rep": o["rep"], "dist_to_each_filled": fd, "dist_histogram_of_filled": dict(Counter(fd.values())),
                     "smallest_S_dist_histograms": [dict(Counter(fd[w] for w in S)) for S in sm[:8]],
                     "all_minimal_S_union_of_dist_hist_maxdist": max(fd[w] for S in allS for w in S)})
        print(d, o["rep"], "filled dist hist", dict(Counter(fd.values())), "smallest S hists", [dict(sorted(Counter(fd[w] for w in S).items())) for S in sm[:4]], flush=True)
    out[str(d)] = rows
json.dump(out, open("pattern2-%s.json" % tag, "w"), indent=1)
