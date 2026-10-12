#!/usr/bin/env python3
"""[Track E, C4] Lock graph on labelled unfilled colourings: edge = swap of a lock chain (lock1 or lock2).  Singly locked
states have degree 1, doubly locked (DL) degree 2, unlocked degree 0, so components are paths and cycles.  A fixed-point-
free involution on the locked states made of lock swaps exists iff every path component has an even number of states and
every cycle is even (perfect matching).  Also: is the image of a lock swap again locked by the same chain (it must be)?"""
import sys, json
from collections import Counter, defaultdict
from phase_lib import *
GENTRI = '/Users/kylemathewson/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/studiointel/gentri/tri%d.txt'
C = Counter()
for n in map(int, sys.argv[1:]):
    lines = open(GENTRI % n).read().splitlines()
    for gi, line in enumerate(lines):
        rot = gentri_rotation(line)
        for h in range(len(rot)):
            if len(rot[h]) != 5: continue
            L = LSpace(rot, h); S = L.S; C['holes'] += 1
            adj = defaultdict(set)
            for k in range(S):
                for lkc in L.locks(k):
                    if lkc is None: continue
                    for g_i, g in enumerate(PERMS):
                        k2, g2 = L.move(k, g, *lkc); a, b = k * 24 + g_i, k2 * 24 + PIDX[g2]
                        adj[a].add(b); adj[b].add(a)
            seen = set(); hole_ok = True
            for x in adj:
                if x in seen: continue
                comp = [x]; seen.add(x)
                for y in comp:
                    for z in adj[y]:
                        if z not in seen: seen.add(z); comp.append(z)
                degs = Counter(len(adj[y]) for y in comp)
                assert max(degs) <= 2
                kind = 'cycle' if degs.get(1, 0) == 0 else 'path'
                C['%s components' % kind] += 1
                if len(comp) % 2: C['%s components with odd #states' % kind] += 1; hole_ok = False
                C['%s max length' % kind] = max(C['%s max length' % kind], len(comp))
            C['holes where a lock-swap perfect matching exists'] += hole_ok
    print(n, json.dumps(dict(C))); sys.stdout.flush()
