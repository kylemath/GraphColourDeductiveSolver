#!/usr/bin/env python3
"""[exploratory] Sage QA run 2 driver: every degree-5 hole orbit (orders 12-20 from km-N.jsonl hole list) through kreach
with unrestricted and with link-touching-only moves. usage: linkonly.py ORDERS..."""
import json, os, subprocess, sys
from collections import Counter
H = os.path.dirname(os.path.abspath(__file__)); P = os.path.expanduser("~/studio-scratch/plantri-src/plantri58/plantri")
for n in [int(x) for x in sys.argv[1:]]:
    lines = [l for l in subprocess.run([P, "-m5", "-c4", str(n), "-a"], capture_output=True, text=True).stdout.split("\n") if l.strip()]
    agg = Counter(); depth_pairs = Counter(); recs = []
    for l in open(os.path.join(H, "km-%d.jsonl" % n)):
        r = json.loads(l); rot = [[ord(c) - 97 for c in x] for x in lines[r["index"]].split()[1].split(",")]
        E = sorted({tuple(sorted((a, b))) for a, nb in enumerate(rot) for b in nb}); p = "/tmp/lo_%d.edges" % os.getpid()
        open(p, "w").write("%d %d\n" % (len(rot), len(E)) + "".join("%d %d\n" % e for e in E))
        for v in r["vertices"]:
            if v["deg"] != 5: continue
            a = json.loads(subprocess.run([os.path.join(H, "kreach"), p, str(v["v"])], capture_output=True, text=True).stdout)
            b = json.loads(subprocess.run([os.path.join(H, "kreach"), p, str(v["v"])], capture_output=True, text=True, env={**os.environ, "LINKONLY": "1"}).stdout)
            agg["holes"] += 1; agg["linkonly_targetless_holes"] += b["targetless_classes"] > 0
            agg["linkonly_more_classes"] += b["classes"] > a["classes"]
            depth_pairs[(a["depth"], b["depth"] if b["unreachable_states"] == 0 else "inf")] += 1
            if b["targetless_classes"]: recs.append({"order": n, "index": r["index"], "v": v["v"], "all": a, "linkonly": b, "graph": lines[r["index"]]})
    print(json.dumps({"order": n, **agg, "depth_all_vs_linkonly": {"%s->%s" % k: c for k, c in sorted(depth_pairs.items(), key=str)}, "targetless_examples": recs[:3]}))
