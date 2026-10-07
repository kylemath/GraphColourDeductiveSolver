#!/usr/bin/env python3
"""[Track E, C0b] longer flip walks at n = 13..16 to exercise the cyclic-Q_s cancellation on more pairs."""
import sys, json, random
import c0_barnette as B
seen = set(); rnd = random.Random(7)
for n in (13, 14, 15, 16):
    for seed in range(3):
        for F in B.enum_eulerian(n, 600000, 1000 * n + seed):
            c = B.canon(F)
            if c in seen: continue
            seen.add(c)
            for t0i in range(len(F) // 2):
                r = B.analyse(F, rnd, t0i); print(json.dumps(r)); sys.stdout.flush()
