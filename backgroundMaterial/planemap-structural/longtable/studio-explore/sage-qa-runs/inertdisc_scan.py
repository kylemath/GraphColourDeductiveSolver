#!/usr/bin/env python3
"""[exploratory] inertdisc_a.py over every degree-5 hole orbit of plantri -m5 -c4 order N (from km-N.jsonl). usage: inertdisc_scan.py N"""
import json, os, subprocess, sys
from collections import Counter
H = os.path.dirname(os.path.abspath(__file__)); n = int(sys.argv[1])
lines = [l for l in subprocess.run([os.path.expanduser("~/studio-scratch/plantri-src/plantri58/plantri"), "-m5", "-c4", str(n), "-a"], capture_output=True, text=True).stdout.split("\n") if l.strip()]
tot, inside, kinds, first = 0, 0, Counter(), None
for l in open(os.path.join(H, "km-%d.jsonl" % n)):
    r = json.loads(l)
    for v in r["vertices"]:
        if v["deg"] != 5: continue
        o = json.loads(subprocess.run([sys.executable, os.path.join(H, "inertdisc_a.py"), "--plantri", lines[r["index"]], str(v["v"])], capture_output=True, text=True).stdout)
        tot += o["shortest_fill_swaps_from_DL_checked"]; inside += o["violations"]; kinds.update(o["violation_kinds"])
        if o["violations"] and first is None: first = {"order": n, "index": r["index"], "graph": lines[r["index"]], "hole": v["v"], "example": o["examples"][0]}
print(json.dumps({"order": n, "swaps_checked": tot, "inside_disc_offlink": inside, "by_dist_and_disc": dict(kinds), "first_instance": first}))
