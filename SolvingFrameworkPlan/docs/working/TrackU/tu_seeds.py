#!/usr/bin/env python3
"""Track U: export Tait duals of surface holes (via TrackT tt_lib.tait_dual, read-only) to tu_eng graph lines.
usage: tu_seeds.py GRAPHFILE name:hole ... > seeds.txt"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'TrackT'))
from tt_lib import load_graphs, tait_dual

def line(g):
    return ' '.join(map(str, [g.n, g.m] + [x for e in g.E for x in e] + list(g.fv)))

if __name__ == '__main__':
    G = load_graphs(sys.argv[1], {s.rsplit(':', 1)[0] for s in sys.argv[2:]})
    for spec in sys.argv[2:]:
        nm, h = spec.rsplit(':', 1)
        g = tait_dual(G[nm], int(h))
        print(line(g))
        print(spec, g.n, g.m, file=sys.stderr)
