#!/usr/bin/env python3
"""Track A: which constructed graphs (Job AS / AW / BI hit graphs / BV / BQ / BJ (c)-hits) are in the frame class?"""
import json, glob, os
from tracka_lib import rot_from_faces, G
P = '/Users/kylemathewson/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/local-runs/27-studio-positive-config/'
pats = ['jobas/best-*.json', 'jobbi/hitgraphs/*.json', 'jobbv/graphs/*.json', 'jobbq/best/*.json', 'jobbj/chits/best-*.json', 'jobaw/hits/*.json']
res = []
for p in pats:
    for fn in sorted(glob.glob(P + p)):
        try: d = json.load(open(fn))
        except Exception: continue
        if not isinstance(d, dict) or 'faces' not in d: continue
        s = G(rot_from_faces([tuple(t) for t in d['faces']])).summary()
        res.append(dict(file=fn[len(P):], n=s['n'], frame=s['frame'], occ=s['occ'], nosep=s['nosep'], mindeg=s['mindeg'], tri=s['tri']))
json.dump(res, open('out/constructed-frame-check.json', 'w'), indent=1)
print(len(res), 'graphs;', sum(r['frame'] for r in res), 'in frame class')
for r in res:
    if r['frame']: print(r)
from collections import Counter
print(Counter((r['file'].split('/')[0], r['frame']) for r in res))
