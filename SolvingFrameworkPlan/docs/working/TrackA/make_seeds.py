#!/usr/bin/env python3
"""Track A: build out/seeds.json for the search = the K most marginal census frame graphs (lowest margin, then lowest worst)
from out/census-*.jsonl + distinct cleaned constructed graphs (out/seeds-constructed.json, deduplicated by canonical face set)."""
import json, glob, sys
from tracka_lib import parse_line, faces_from_rot
K = int(sys.argv[1]) if len(sys.argv) > 1 else 8; KC = int(sys.argv[2]) if len(sys.argv) > 2 else 8
P = '/Users/kylemathewson/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/local-runs/27-studio-positive-config/'
recs = [json.loads(l) for fn in sorted(glob.glob('out/census-*.jsonl')) for l in open(fn)]
recs = [r for r in recs if r['frame']]
lines = {}
for fn in glob.glob('out/frame-*.txt') + glob.glob('out/frame28-*.txt'):
    for l in open(fn):
        if l.strip(): lines[l.split()[0]] = l
seeds = []
by_margin = sorted(recs, key=lambda r: (r['margin'], r['worst']))[:K]
by_worst = sorted(recs, key=lambda r: (r['worst'], r['margin']))[:K]
for r in by_margin + by_worst:
    if any(s['name'] == r['name'] for s in seeds) or r['name'] not in lines: continue
    seeds.append(dict(name=r['name'], faces=faces_from_rot(parse_line(lines[r['name']])[1]), margin=r['margin'], worst=r['worst']))
C = json.load(open('out/seeds-constructed.json')); seen = set(); nc = 0
for c in sorted(C, key=lambda c: c['name']):
    k = frozenset(frozenset(t) for t in c['faces'])
    if k in seen or nc >= KC: continue
    seen.add(k); nc += 1; seeds.append(dict(name=c['name'], faces=c['faces']))
json.dump(seeds, open('out/seeds.json', 'w'))
for s in seeds: print(s['name'], s.get('margin'), s.get('worst'))
