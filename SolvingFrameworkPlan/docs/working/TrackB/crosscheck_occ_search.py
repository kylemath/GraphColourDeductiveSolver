#!/usr/bin/env python3
"""[Track B] Second, independent frame-class check with the repo's StudioMathReview-scripts/occ_search.py
(parses the Lean Occ structures itself, oriented faces input). For each graph: write faces JSON, run occ_search on the
4 namespaces, and compare 'any Occ found' with the expectation. Usage: python3 crosscheck_occ_search.py EXPECT(0|1) files..."""
import sys, json, subprocess, os, tempfile
from words import load
OS = '../StudioMathReview-scripts/occ_search.py'; PM = '../StudioMathLean/Mathlib/Combinatorics/SimpleGraph/PlaneMap/'
exp = int(sys.argv[1]); G = load(sys.argv[2:]); bad = 0
tmp = tempfile.NamedTemporaryFile('w', suffix='.json', delete=False, dir=os.environ.get('TMPDIR', '/tmp')); tmp.close()
for nm, n, rot in G:
    faces = set()
    for v, r in enumerate(rot):
        for i in range(len(r)):
            f = (v, r[i], r[(i + 1) % len(r)]); k = f.index(min(f)); faces.add(f[k:] + f[:k])
    assert len(faces) == 2 * n - 4
    json.dump({'faces': [list(f) for f in faces]}, open(tmp.name, 'w'))
    out = subprocess.run(['python3', '-I', OS, tmp.name, PM, 'DiamondP', 'DiamondM', 'C2122P', 'C2122M'], capture_output=True, text=True).stdout
    found = sum(int(l.split()[1]) for l in out.splitlines())
    if (found > 0) != bool(exp): bad += 1; print('DISAGREE', nm, out)
os.unlink(tmp.name)
print('checked', len(G), 'expect occ' if exp else 'expect occ-free', 'disagreements', bad)
