#!/usr/bin/env python3
"""[Track E] probe: parity of the Heawood count change dP under one chain swap vs link data of the chain."""
import sys, json
from collections import Counter, defaultdict
from phase_lib import *
GENTRI = '/Users/kylemathewson/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/studiointel/gentri/tri%d.txt'
tab = defaultdict(Counter)
for n in map(int, sys.argv[1:]):
    for line in open(GENTRI % n):
        rot = gentri_rotation(line)
        for h in range(len(rot)):
            if len(rot[h]) != 5: continue
            L = LSpace(rot, h); li = L.li
            for k in range(L.S):
                s = L.sp.states[k]; P0 = L.stats(k, PERMS[0])[0]
                for pq in PAIRS:
                    for K in L.comps[k][pq]:
                        k2, g2 = L.move(k, PERMS[0], pq, K); P1 = L.stats(k2, g2)[0]
                        inl = [t for t in range(5) if K >> li[t] & 1]
                        b = sum(1 for t in inl if (t + 1) % 5 in inl)
                        tot = sum(1 for t in range(5) if s[li[t]] in pq)   # link vertices with colour p or q
                        key = (len(inl), b, tot, len(set(s[i] for i in li)))
                        tab[key][(P1 - P0) % 2] += 1
for key in sorted(tab): print('nl=%d b=%d linkpq=%d linkcols=%d' % key, dict(tab[key]))
