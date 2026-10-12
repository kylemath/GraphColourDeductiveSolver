#!/usr/bin/env python3
"""Track F: re-check every all-DL pi-cycle hole found by kclass3 with the Python engine (lpc_detail.analyse):
cycle lengths, [onCycles, filled] per class containing a cycle, and the full class list.
usage: lpc_cycverify.py GRAPHS.txt KCLASS3.jsonl"""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
import lpc_detail
K = 'cls[size,filled,DL,unfilledNonDL,minKdeg,maxKdeg,lockParityViolations]'
G = {}
for l in open(sys.argv[1]):
    p = l.split(); G[p[0]] = [list(map(int, r.split(','))) for r in p[2].split(';')]
n = mis = 0
for l in open(sys.argv[2]):
    d = json.loads(l)
    if not d['allDLcyc']: continue
    res, _ = lpc_detail.analyse(G[d['graph']], d['hole'], False); n += 1
    a = sorted(d[K]) == res['cls'] and sorted(d['allDLcyc']) == res['allDLcyc'] and \
        sorted([c[0], c[2]] for c in d['cycClasses[onCycles,pathEnds,filled]']) == res['cycClasses']
    if not a: mis += 1; print('MISMATCH', d['graph'], d['hole'], flush=True)
print(json.dumps(dict(cycle_holes=n, mismatches=mis)))
