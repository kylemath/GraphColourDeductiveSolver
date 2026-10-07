#!/usr/bin/env python3
"""[exploratory] Item 6 (4): link-pattern blocks of every degree-5 Kempe class at exactly 1/4 (from quarter-classes.jsonl).
For each class, the states are grouped by link colour pattern (letters by first occurrence from link position 0). Each block
is reported with its size, kind (filled / DL / non-DL; DL = unfilled and no single swap fills) and, for unfilled
blocks, the repeat pair {j, j+2}. Tests the "4 equal blocks" description: one filled pattern with singleton at i, plus
the three unfilled frames whose repeat pair avoids i, every block of size F = #filled.
usage: blocks.py > blocks-deg5.jsonl ; last line is the summary"""
import json, os, sys
from collections import Counter
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H); sys.path.insert(0, os.path.join(H, "..", "common"))
from quarter_struct import Space, gentri_rotation, adj_from_rot, GENTRI, pattern

lines = {}; summ = Counter(); first_other = None
for l in open(os.path.join(H, "quarter-classes.jsonl")):
    r = json.loads(l)
    if r["deg"] != 5: continue
    n = r["order"]
    if n not in lines: lines[n] = [x for x in open(os.path.join(GENTRI, "tri%d.txt" % n)) if x.strip()]
    rot = gentri_rotation(lines[n][r["gentri_index"]]); adj = adj_from_rot(rot)
    S = Space(adj, r["hole"], link=rot[r["hole"]]); S.build_graph(); cl, ncl = S.classes()
    filled = [S.filled(k) for k in range(len(S.states))]
    fills1 = [filled[s] or any(filled[t] for t in S.G[s]) for s in range(len(S.states))]
    for k in range(ncl):
        C = [s for s in range(len(S.states)) if cl[s] == k]; F = sum(filled[s] for s in C)
        if 4 * F != len(C): continue
        blocks = {}
        for s in C:
            p = pattern(S, s); kind = "filled" if filled[s] else ("nonDL" if fills1[s] else "DL")
            b = blocks.setdefault(p, Counter()); b[kind] += 1
        desc = []
        for p, b in sorted(blocks.items()):
            rp = None
            if len(set(p)) == 4: rp = [j for j in range(5) if p[j] == p[(j + 2) % 5]][0]; rp = sorted([rp, (rp + 2) % 5])
            desc.append({"pattern": p, "size": sum(b.values()), "kinds": dict(b), "repeat_pair": rp})
        fp = [d for d in desc if "filled" in d["kinds"]]
        four_equal = (len(desc) == 4 and all(d["size"] == F for d in desc) and len(fp) == 1)
        if four_equal:
            i = [j for j in range(5) if fp[0]["pattern"].count(fp[0]["pattern"][j]) == 1][0]
            four_equal = all(i not in d["repeat_pair"] for d in desc if d["repeat_pair"])
        homog = all(len(d["kinds"]) == 1 for d in desc)
        summ["classes"] += 1; summ["four_equal_blocks" if four_equal else "other"] += 1; summ["blocks_kind_homogeneous" if homog else "blocks_mixed"] += 1
        if four_equal:
            for d in desc:
                if d["repeat_pair"]:
                    rel = sorted(((d["repeat_pair"][0] - i) % 5, (d["repeat_pair"][1] - i) % 5))
                    summ["pair_rel_to_singleton_%d%d_%s" % (rel[0], rel[1], "/".join(sorted(d["kinds"])))] += 1
        print(json.dumps({"order": n, "gentri_index": r["gentri_index"], "hole": r["hole"], "size": len(C), "filled": F,
                          "four_equal_blocks": four_equal, "blocks": desc}))
print(json.dumps({"summary": dict(summ)}))
