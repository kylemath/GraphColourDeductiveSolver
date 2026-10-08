#!/usr/bin/env python3
"""Track F section 9: the Census29 sphere graphs with all-DL pi-cycles (eval-*.jsonl field allDL > 0), run through the
same analysis as the off-sphere search (kclass4 at every degree-5 hole; word, frame-like flag, cycle classes, violator-free
classes).  Writes out/lpc2/sphere_graphs.txt, out/lpc2/sphere_holes.jsonl (every degree-5 hole), out/lpc2/sphere_items.jsonl
(cycle holes, input to lpc2_verify.py)."""
import os, sys, json, glob
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
from lpc2_search import frame_like, word, run_kc, K2
C29 = os.path.join(D, '..', '..', 'Census29', 'out'); OUT = os.path.join(D, '..', 'out', 'lpc2')
names = {}
for f in sorted(glob.glob(os.path.join(C29, 'eval-*.jsonl'))):
    for l in open(f):
        d = json.loads(l)
        if d.get('allDL'): names[d['name']] = d['allDL']
lines = []
for f in sorted(glob.glob(os.path.join(C29, 'frame-*.txt'))):
    for l in open(f):
        p = l.split()
        if p and p[0] in names: lines.append(' '.join(p[:3]))
assert len(lines) == len(names), (len(lines), len(names))
open(os.path.join(OUT, 'sphere_graphs.txt'), 'w').write('\n'.join(lines) + '\n')
hol = open(os.path.join(OUT, 'sphere_holes.jsonl'), 'w'); items = open(os.path.join(OUT, 'sphere_items.jsonl'), 'w')
ncyc = 0
for line in lines:
    rot = [list(map(int, r.split(','))) for r in line.split()[2].split(';')]
    hs = [h for h in range(len(rot)) if len(rot[h]) == 5]
    recs = run_kc(line, hs, os.path.join(OUT, 'sphere.tmp'), timeout=3600)
    for d in recs:
        h = d['hole']; degs = [len(rot[x]) for x in rot[h]]
        r = dict(graph=line.split()[0], hole=h, word=word(degs), frame_like=frame_like(degs), states=d['states'],
                 allDLcyc=d['allDLcyc'], cls2=d[K2])
        hol.write(json.dumps(r) + '\n')
        if d['allDLcyc']:
            ncyc += len(d['allDLcyc'])
            items.write(json.dumps(dict(graph=line, hole=h, word=r['word'], frame_like=r['frame_like'], surface='sphere', n=len(rot))) + '\n')
os.unlink(os.path.join(OUT, 'sphere.tmp'))
print('graphs', len(lines), 'cycles', ncyc, 'expected', sum(names.values()))
