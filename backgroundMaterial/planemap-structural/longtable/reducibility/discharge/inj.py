"""B8 (exploratory): how the free-completion ring of a 2-ball sits in the graph.
For each degree-5 hole v: B2 = vertices at distance <= 2, N3 = vertices adjacent to B2 outside it.
Free completion ring size r = ball.ring_size(key).  'inj' iff |N3| == r (no two ring positions identified).
Usage: inj.py GRAPHFILE [names-file]   prints counts"""
import sys, os, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ball
only = set(open(sys.argv[2]).read().split()) if len(sys.argv) > 2 else None
C = collections.Counter(); ex = {}
for line in open(sys.argv[1]):
    name, rot = ball.parse_line(line)
    if only is not None and name not in only: continue
    for v in range(len(rot)):
        if len(rot[v]) != 5: continue
        w, key, st = ball.ball_at(rot, v)
        if key is None: C['irregular'] += 1; continue
        B = {v} | set(rot[v]); B |= {z for x in rot[v] for z in rot[x]}
        N3 = {z for x in B for z in rot[x]} - B
        r = ball.ring_size(key)
        k = 'inj' if len(N3) == r else 'identified'
        C[k] += 1
        if k == 'identified' and len(ex) < 5: ex[name + ':%d' % v] = (r, len(N3))
print(dict(C), ex)
