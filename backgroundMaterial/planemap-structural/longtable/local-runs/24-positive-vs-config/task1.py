import sys, json, glob, os
sys.path.insert(0, '../common'); sys.path.insert(0, '../22-winding-escape'); sys.path.insert(0, '../23-positive-cycles')
from kempe_py import gentri_rotation
from conf import configs, dist_to
from escape import GENTRI
import collections
rows = []; graphs = {}
for n in range(12, 25):
    f = '../23-positive-cycles/out-%d.jsonl' % n
    if not os.path.exists(f): continue
    lines = [l for l in open(GENTRI % n) if l.startswith('G')]
    pos = collections.defaultdict(list)
    for l in open(f):
        r = json.loads(l)
        if r['kind'] == 'class': pos[r['gentri']].append(r)
    for gi, recs in sorted(pos.items()):
        rot = gentri_rotation(lines[gi - 1]); cs = configs(rot)
        kinds = collections.Counter(c[0] for c in cs)
        verts = set(); [verts.update(c[1] + c[2]) for c in cs]
        for r in recs:
            h = r['hole']; link = set(rot[h])
            d = dist_to(rot, h, verts) if verts else None
            rows.append(dict(n=n, gentri=gi, hole=h, w=[c['w'] for c in r['cycles']], diamonds=kinds['diamond'], c2122=kinds['2.122'],
                             hole_in=h in verts, hole_adj=bool(link & verts), link_meets=bool(link & verts), dist=d))
json.dump(rows, open('task1.json', 'w'))
G = {(r['n'], r['gentri']) for r in rows}
print('classes', len(rows), 'graphs', len(G))
print('graphs with diamond', len({(r['n'], r['gentri']) for r in rows if r['diamonds']}), 'with 2.122', len({(r['n'], r['gentri']) for r in rows if r['c2122']}),
      'with neither', len({(r['n'], r['gentri']) for r in rows if not r['diamonds'] and not r['c2122']}))
print('classes: hole in config', sum(r['hole_in'] for r in rows), 'hole adjacent (link meets) but not in', sum(r['hole_adj'] and not r['hole_in'] for r in rows),
      'neither', sum(not r['hole_adj'] and not r['hole_in'] for r in rows))
print('dist hist', sorted(collections.Counter(r['dist'] for r in rows).items(), key=lambda x: (x[0] is None, x[0])))
byn = collections.defaultdict(lambda: [0, 0, 0])
for g in G:
    pass
for n in sorted({r['n'] for r in rows}):
    gs = {r['gentri'] for r in rows if r['n'] == n}
    print(n, 'graphs', len(gs), 'classes', sum(r['n'] == n for r in rows))
