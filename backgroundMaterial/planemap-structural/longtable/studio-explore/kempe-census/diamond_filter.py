#!/usr/bin/env python3
"""[exploratory] Filter plantri -a lines: keep graphs with >= K pairwise vertex-disjoint Birkhoff diamonds
(4 degree-5 vertices, two faces sharing an edge). Prints the kept lines; count to stderr. usage: diamond_filter.py K"""
import sys, itertools
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from analyse import parse, diamonds
K = int(sys.argv[1]); kept = tot = 0
for line in sys.stdin:
    if not line.strip(): continue
    tot += 1
    ds = diamonds(parse(line))
    if len(ds) < K: continue
    ok = any(all(not (a & b) for a, b in itertools.combinations(c, 2)) for c in itertools.combinations(ds, K))
    if ok: kept += 1; sys.stdout.write(line)
sys.stderr.write("kept %d of %d\n" % (kept, tot))
