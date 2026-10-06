#!/usr/bin/env python3
"""[exploratory] Run 4 follow-up: for every multi-class T, every vertex v: does deleting v merge all of T's classes
(kmap: max_T_classes_per_H_class == kappa(T))? Fractions by degree of v (5, 6, 7+); whether a degree-5 merging vertex
always exists; whether a merging v ever has kappa(T - v) >= 2. usage: plantri -m5 -c4 N -a | mergefrac.py N"""
import json, os, subprocess, sys
from collections import Counter
from multiprocessing import Pool
H = os.path.dirname(os.path.abspath(__file__))
def work(item):
    idx, line = item
    rot = [[ord(c) - 97 for c in x] for x in line.split()[1].split(",")]
    E = sorted({tuple(sorted((a, b))) for a, nb in enumerate(rot) for b in nb}); p = "/tmp/mf_%d_%d.edges" % (os.getpid(), idx)
    open(p, "w").write("%d %d\n" % (len(rot), len(E)) + "".join("%d %d\n" % e for e in E))
    res = []
    try:
        for v in range(len(rot)):
            o = json.loads(subprocess.run([os.path.join(H, "kmap"), p, "v", str(v)], capture_output=True, text=True).stdout.splitlines()[0])
            if o["kT"] < 2: return {"index": idx, "kT": o["kT"]}
            res.append((len(rot[v]), o["max_T_classes_per_H_class"] == o["kT"], o["kH"], o["new_classes"]))
    finally:
        os.unlink(p)
    return {"index": idx, "kT": res[0] and None, "v": res}
def main():
    n = int(sys.argv[1]); lines = [l for l in sys.stdin.read().splitlines() if l.strip()]
    tot, mer = Counter(), Counter(); no5 = 0; multi = 0; merge_multi_H = 0; new = 0
    with Pool(4) as pool:
        for r in pool.imap(work, enumerate(lines), chunksize=4):
            if "v" not in r: continue
            multi += 1; has5 = False
            for d, m, kH, nw in r["v"]:
                key = str(d) if d < 7 else "7+"; tot[key] += 1; mer[key] += m
                if m and d == 5: has5 = True
                if m and kH >= 2: merge_multi_H += 1
                new += nw > 0
            no5 += not has5
    print(json.dumps({"order": n, "multi_class_T": multi, "merging_fraction_by_degree": {k: [mer[k], tot[k], round(mer[k] / tot[k], 3)] for k in sorted(tot)},
                      "multi_class_T_without_degree5_merging_vertex": no5, "merging_v_with_kappa_T_minus_v_ge2": merge_multi_H, "vertex_deletions_with_new_class": new}))
if __name__ == "__main__":
    main()
