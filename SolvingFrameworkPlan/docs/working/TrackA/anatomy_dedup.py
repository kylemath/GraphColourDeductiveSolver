#!/usr/bin/env python3
"""Track A task 2: (a) graph dedup by invariant over census 27-28 + W-best graphs; distinct equality classes;
(b) picyc hist: pi-cycles with w = 0 and L = 4 in all holes vs those inside equality classes (plantri orientation)."""
import json, subprocess, tempfile, os
from collections import Counter
from anatomy_pi import ROT
from tracka_lib import rot_line
from holes import PICYC
A = [json.loads(l) for fn in ('anat/anat-census27-28.jsonl', 'anat/anat-wbest.jsonl') for l in open(fn)]
inv = {}
for r in A:
    rot = ROT[r['name']]
    key = (r['n'], tuple(sorted(len(x) for x in rot)), tuple(sorted(Counter((N, F) for h, N, F in r['allclasses']).items())),
           tuple(sorted(tuple(sorted(len(rot[y]) for y in rot[x])) for x in range(len(rot)))))
    inv.setdefault(key, []).append(r['name'])
dup = [v for v in inv.values() if len(v) > 1]
print('graphs', len(A), 'distinct by invariant', len(inv), '; duplicate groups', len(dup), dup[:12])
keep = {v[0] for v in inv.values()}
eq = [(r['name'], r['n'], h, N, F) for r in A if r['name'] in keep for h, N, F in r['allclasses'] if 4 * F == N]
allc = [(r['n'], N, F) for r in A if r['name'] in keep for h, N, F in r['allclasses']]
print('distinct graphs: classes', len(allc), '; equality classes', len(eq), 'by (n,N):', dict(sorted(Counter((n, N) for _, n, _, N, _ in eq).items())),
      '; graphs with >=1 equality class', len({x[0] for x in eq}))
print('classes by n (distinct graphs):', dict(sorted(Counter(n for n, *_ in allc).items())))
# (b)
tot = 0; inEq = 0; holesW = 0
eqpi = Counter()
for l in open('anat/anat-pi.jsonl'):
    r = json.loads(l)
    if not r['mirror'] and 4 * r['F'] == r['N'] and r['name'] in keep:
        eqpi[(r['name'], r['hole'])] += sum(1 for L, w in r['cycles'] if L == 4 and w == 0)
for name in sorted(keep):
    with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as fh: fh.write(rot_line(name, ROT[name]) + '\n'); fn = fh.name
    o = subprocess.run([PICYC, fn, '--full'], capture_output=True, text=True).stdout; os.unlink(fn)
    for line in o.splitlines():
        h = json.loads(line)
        if h['kind'] != 'hole': continue
        c = sum(cnt for w, L, cnt in h['hist'] if w == 0 and L == 4)
        tot += c; inEq += eqpi.get((name, str(h['hole'])), 0); holesW += c > 0
print('pi-cycles with w = 0, L = 4 (plantri orientation, distinct graphs):', tot, 'in', holesW, 'holes; inside equality classes:', inEq, '; inside larger classes:', tot - inEq)
