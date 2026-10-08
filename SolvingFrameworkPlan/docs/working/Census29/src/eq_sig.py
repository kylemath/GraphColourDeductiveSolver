#!/usr/bin/env python3
"""Census29: picyc --full clsig [N, F, sumw, DD, N0, E2, tau] of every quarter-floor equality class (4F = N) in the census.
Re-runs picyc on the graphs that have one (from out/eval-*.jsonl). Writes out/eq_classes.jsonl and prints a tally."""
import json, os, subprocess, collections, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); O = os.path.join(ROOT, 'out')
names = {}
for f in sorted(glob.glob(os.path.join(O, 'eval-*.jsonl'))):
    for l in open(f):
        r = json.loads(l)
        if r['quarter_eq']: names[r['name']] = r['n']
lines = [l for n in sorted(set(names.values())) for l in open(os.path.join(O, 'frame-%d.txt' % n)) if l.split()[0] in names]
inp = ''.join(' '.join(l.split()[:3]) + '\n' for l in lines)
out = subprocess.run([os.path.join(ROOT, 'bin/picyc'), '/dev/stdin', '--full'], input=inp, capture_output=True, text=True).stdout
T = collections.Counter(); rows = []
for r in map(json.loads, out.splitlines()):
    if r['kind'] != 'hole': continue
    for c in r['clsig']:
        if 4 * c[1] == c[0]:
            rows.append(dict(name=r['name'], n=r['n'], hole=r['hole'], linkdeg=r['linkdeg'], clsig=c))
            T[(c[0], c[1], 'sumw=%d' % c[2], 'DD>0' if c[3] else 'DD=0', 'N0>0' if c[4] else 'N0=0', 'E2>0' if c[5] else 'E2=0', 'tau>0' if c[6] else 'tau=0')] += 1
with open(os.path.join(O, 'eq_classes.jsonl'), 'w') as f:
    for x in rows: f.write(json.dumps(x) + '\n')
print('equality classes:', len(rows), 'in', len(names), 'graphs')
for k, v in sorted(T.items()): print(v, k)
