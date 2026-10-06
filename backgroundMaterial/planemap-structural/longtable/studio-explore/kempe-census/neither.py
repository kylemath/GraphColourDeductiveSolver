#!/usr/bin/env python3
"""[exploratory] Per order: which graphs contain neither the Birkhoff diamond (RSST 0.7322) nor RSST 2.122
(Studio intel rsst_contain.py, commit 7f99280), and the rho histogram / max rho over their hole classes.
usage (cwd = studiointel): plantri -m5 -c4 N -a | neither.py N"""
import json, os, sys
sys.path.insert(0, os.getcwd()); sys.path.insert(0, os.path.join(os.getcwd(), "routeb"))
import rsst_parse, rsst_contain as rc
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
from rsst_check import graph
n = int(sys.argv[1])
P = [rc.prep_conf(c) for c in rsst_parse.parse('routeb/rsst/unavoidable.conf')[:2]]
lines = [l for l in sys.stdin.read().splitlines() if l.strip()]
neither = {i for i, l in enumerate(lines) if not any(rc.contains(*graph(l), p) for p in P)}
hist, mx, recs = {}, None, []
for l in open(os.path.join(H, "out-%d.jsonl" % n)):
    r = json.loads(l)
    if r["index"] in neither:
        hist[str(r["rho"])] = hist.get(str(r["rho"]), 0) + 1
        if r["rho"] is not None and (mx is None or r["rho"] > mx): mx = r["rho"]
        if r["rho"] is None or r["rho"] >= 4: recs.append({**r, "graph": lines[r["index"]]})
print(json.dumps({"order": n, "graphs": len(lines), "graphs_neither": len(neither), "rho_hist_neither": hist, "max_rho_neither": mx, "rho_ge4_neither": recs}))
