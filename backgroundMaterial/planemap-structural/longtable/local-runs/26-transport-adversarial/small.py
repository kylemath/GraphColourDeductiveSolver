#!/usr/bin/env python3
"""small.py N: all (graph,hole) of order N from run-25 (positive classes) -> run-26 records for every positive class (full gentri enumeration)."""
import sys, json, time
sys.path.insert(0, '../common'); sys.path.insert(0, '../22-winding-escape')
from lib26 import *
from kempe_py import Space, gentri_rotation, adj_from_rot
from escape import GENTRI
import multiprocessing as mp
def run(a):
    n, gi, hs, line = a
    rot = gentri_rotation(line); adj = adj_from_rot(rot); recs = []
    for h in hs:
        sp = Space(adj, h, link=rot[h]); E = Eng(adj, h, rot[h]); seen = set()
        for s in sp.states:
            if s in seen: continue
            mem = E.bfs(s); seen |= set(mem)
            r = analyse_class(E, mem, dict(n=n, gentri=gi, hole=h))
            if r: recs.append(r)
    return recs
if __name__ == '__main__':
    n = int(sys.argv[1]); need = {}
    for l in open('../25-transport/out-%d.jsonl' % n):
        r = json.loads(l); need.setdefault(r['gentri'], set()).add(r['hole'])
    lines = [l for l in open(GENTRI % n) if l.startswith('G')]
    jobs = [(n, gi, sorted(hs), lines[gi - 1]) for gi, hs in need.items()]
    with mp.Pool(3) as p, open('small-%d.jsonl' % n, 'w') as out:
        for recs in p.imap_unordered(run, jobs):
            for r in recs: out.write(json.dumps(r) + '\n')
