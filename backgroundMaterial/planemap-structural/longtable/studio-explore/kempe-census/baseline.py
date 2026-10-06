#!/usr/bin/env python3
"""[exploratory] Baseline: diamond / 2.122 containment at the hole for a random sample of census records of every rho
(graph regenerated from plantri by index). usage (cwd = studiointel): plantri -m5 -c4 N -a | baseline.py N SAMPLE SEED"""
import json, os, random, sys
sys.path.insert(0, os.getcwd()); sys.path.insert(0, os.path.join(os.getcwd(), "routeb"))
import rsst_parse, rsst_contain as rc
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rsst_check import graph, contains_hole
n, k, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
lines = [l for l in sys.stdin.read().splitlines() if l.strip()]
recs = [json.loads(l) for l in open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "out-%d.jsonl" % n))]
random.seed(seed); sample = random.sample(recs, k)
P = [rc.prep_conf(c) for c in rsst_parse.parse('routeb/rsst/unavoidable.conf')[:2]]
for r in sample:
    adj, tf = graph(lines[r["index"]])
    print(json.dumps({"order": n, "index": r["index"], "hole": r["hole"], "rho": r["rho"],
                      "diamond_at_hole": contains_hole(adj, tf, P[0], r["hole"]), "c2122_at_hole": contains_hole(adj, tf, P[1], r["hole"])}))
