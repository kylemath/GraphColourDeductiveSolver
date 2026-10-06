#!/usr/bin/env python3
"""[exploratory] Intern D's Conjecture M on every vertex deletion (degree 5, 6, 7) that merges T-classes, from km-N.jsonl,
using kmap_m (kmap.cpp with KMAP_BRIDGE). Strict form: every merged pair has a bridge with exactly 1 unfilled state.
Weak form: the merged T-classes are connected using bridges with <= 1 unfilled state. usage: bridge.py ORDERS..."""
import json, os, subprocess, sys
from collections import Counter
H = os.path.dirname(os.path.abspath(__file__))
P = os.path.expanduser("~/studio-scratch/plantri-src/plantri58/plantri")
for n in [int(x) for x in sys.argv[1:]]:
    lines = [l for l in subprocess.run([P, "-m5", "-c4", str(n), "-a"], capture_output=True, text=True).stdout.split("\n") if l.strip()]
    pairs, weak, holes, recs = Counter(), Counter(), Counter(), []
    for l in open(os.path.join(H, "km-%d.jsonl" % n)):
        r = json.loads(l)
        for v in r["vertices"]:
            if not v.get("merging_H_classes"):
                continue
            rot = [[ord(c) - 97 for c in x] for x in lines[r["index"]].split()[1].split(",")]
            E = sorted({tuple(sorted((a, b))) for a, nb in enumerate(rot) for b in nb})
            p = "/tmp/bridge_%d.edges" % os.getpid()
            open(p, "w").write("%d %d\n" % (len(rot), len(E)) + "".join("%d %d\n" % e for e in E))
            o = subprocess.run([os.path.join(H, "kmap_m"), p, "v", str(v["v"])], capture_output=True, text=True,
                               env={**os.environ, "KMAP_BRIDGE": "1"}).stdout.strip().splitlines()
            b = json.loads(o[-1])
            d = v["deg"]; holes[d] += 1
            for k, c in b["bridge_unfilled_hist"].items():
                pairs[(d, k)] += c
            weak[(d, "ok" if b["not"] == 0 else "FAIL")] += 1
            recs.append({"order": n, "index": r["index"], "v": v["v"], "deg": d, **b})
    print(json.dumps({"order": n, "merging_holes_by_degree": {str(k): c for k, c in sorted(holes.items())},
                      "pair_bridge_hist": {"deg%d:%s" % k: c for k, c in sorted(pairs.items())},
                      "weak_form": {"deg%d:%s" % k: c for k, c in sorted(weak.items())}}))
    with open(os.path.join(H, "bridge-%d.jsonl" % n), "w") as f:
        for x in recs: f.write(json.dumps(x) + "\n")
