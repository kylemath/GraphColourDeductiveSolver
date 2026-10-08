#!/usr/bin/env python3
"""Census29: two-engine re-check of special graphs (all holes): picyc --full classes (with sum w per class, Theorem W:
4F - N = -5 sum w) vs kempe_py classes; prints small classes with their picyc clsig and the pi-cycle histogram of the hole.
usage: check_special.py FILE"""
import sys, os, json, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(os.path.dirname(ROOT), 'TrackA'))
sys.path.insert(0, '/Users/kylemathewson/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/local-runs/common')
from holes import py_holes
for line in open(sys.argv[1]):
    p = line.split(); name = p[0]; rot = [list(map(int, x.split(','))) for x in p[2].split(';')]
    o = subprocess.run([os.path.join(ROOT, 'bin/picyc'), '/dev/stdin', '--full'], input=' '.join(p[:3]) + '\n', capture_output=True, text=True).stdout
    H = {r['hole']: r for r in map(json.loads, o.splitlines()) if r['kind'] == 'hole'}
    P = py_holes(rot); ok = all(sorted((c[0], c[1]) for c in H[h]['clsig']) == P[h] for h in H) and set(H) == set(P)
    print(name, 'engines agree' if ok else 'ENGINE MISMATCH', 'holes', len(H))
    for h, r in H.items():
        small = [c for c in r['clsig'] if c[0] <= 64]
        if small:
            print('  hole', h, 'linkdeg', r['linkdeg'], 'small classes [N,F,sumw,DD,N0,E2,tau]', small, 'W check', all(4 * c[1] - c[0] == -5 * c[2] for c in r['clsig']))
            print('     pi hist [w,L,count]', [x for x in r['hist'] if x[1] <= 16])
