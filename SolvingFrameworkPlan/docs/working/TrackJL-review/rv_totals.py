#!/usr/bin/env python3
"""Sum check/fail counters over rv_eng logs given on the command line."""
import re, sys
tot = {}
for f in sys.argv[1:]:
    for l in open(f):
        m = re.match(r'\s+(.*?)\s+checks=(\d+) fails=(\d+)', l)
        if m:
            a, b = tot.get(m.group(1), (0, 0)); tot[m.group(1)] = (a + int(m.group(2)), b + int(m.group(3)))
for k, v in tot.items():
    print(f"{k:75s} {v[0]:>12d} {v[1]:>6d}")
