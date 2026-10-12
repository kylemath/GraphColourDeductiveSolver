#!/usr/bin/env python3
"""Track A: re-verify a search best graph with both engines (picyc and kempe_py) + full frame-class summary.
usage: verify_best.py BEST.json OUT.json"""
import sys, json
from tracka_lib import rot_from_faces, G
from holes import picyc_holes, py_holes, score
d = json.load(open(sys.argv[1])); rot = rot_from_faces([tuple(t) for t in d['faces']])
s = G(rot).summary(); a = picyc_holes(rot); b = py_holes(rot)
agree = set(a) == set(b) and all(sorted(a[h]) == b[h] for h in a)
sa = score(a)
res = dict(src=sys.argv[1], seed=d.get('seed'), n=s['n'], frame=s['frame'], occ=s['occ'], nosep=s['nosep'], tri=s['tri'], mindeg=s['mindeg'], maxdeg=s['maxdeg'],
           engines_agree=agree, deg5=sa['deg5'], npc=sa['npc'], margin=sa['margin'], worst=sa['worst'], classes={str(h): a[h] for h in a})
json.dump(res, open(sys.argv[2], 'w'), indent=1)
print({k: v for k, v in res.items() if k != 'classes'})
