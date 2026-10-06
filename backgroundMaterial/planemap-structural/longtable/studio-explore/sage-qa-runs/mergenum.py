#!/usr/bin/env python3
"""[exploratory] Sage QA run 4: merge number of T = the fewest vertices X such that every Kempe class of T restricts into
ONE Kempe class of T - X (kmap_s: max_T_classes_per_H_class == kappa(T)). Searches |X| = 1, 2, 3 exhaustively (T - X
must stay connected); reports > 3 otherwise. usage: plantri -m5 -c4 N -a | mergenum.py N [--workers K]"""
import itertools, json, os, subprocess, sys
from collections import Counter
from multiprocessing import Pool
H = os.path.dirname(os.path.abspath(__file__))
def work(item):
    idx, line = item
    rot = [[ord(c) - 97 for c in x] for x in line.split()[1].split(",")]
    E = sorted({tuple(sorted((a, b))) for a, nb in enumerate(rot) for b in nb}); p = "/tmp/mn_%d_%d.edges" % (os.getpid(), idx)
    open(p, "w").write("%d %d\n" % (len(rot), len(E)) + "".join("%d %d\n" % e for e in E))
    try:
        kT = None
        for k in (1, 2, 3):
            for X in itertools.combinations(range(len(rot)), k):
                o = json.loads(subprocess.run([os.path.join(H, "kmap_s"), p, "v", ",".join(map(str, X))], capture_output=True, text=True).stdout.splitlines()[0])
                if "error" in o: continue
                kT = o["kT"]
                if kT < 2: return {"index": idx, "kT": kT, "merge_number": 0}
                if o["max_T_classes_per_H_class"] == kT:
                    return {"index": idx, "kT": kT, "merge_number": k, "X": X, "X_degrees": [len(rot[x]) for x in X]}
        return {"index": idx, "kT": kT, "merge_number": ">3"}
    finally:
        os.unlink(p)
def main():
    n = int(sys.argv[1]); w = int(sys.argv[sys.argv.index("--workers") + 1]) if "--workers" in sys.argv else 4
    lines = [l for l in sys.stdin.read().splitlines() if l.strip()]
    with Pool(w) as pool, open(os.path.join(H, "mergenum-%d.jsonl" % n), "w") as f:
        res = list(pool.imap(work, enumerate(lines)))
        for r in res: f.write(json.dumps(r) + "\n")
    tab = Counter((r["kT"], str(r["merge_number"])) for r in res)
    print(json.dumps({"order": n, "graphs": len(lines), "kT_mergenumber": {"kT=%s,m=%s" % k: c for k, c in sorted(tab.items(), key=str)}}))


if __name__ == "__main__":
    main()
