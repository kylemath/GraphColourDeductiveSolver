"""B8b (exploratory): WheelMain/dfast configuration of an arbitrary vertex set I of a triangulation, with ring
= N(I) \\ I (must be an induced cycle; checked).  Format as ball.fmt_config: name r m ringadj intadj."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import ball


def config(rot, I, name):
    I = sorted(I); Is = set(I); adj = [set(r) for r in rot]
    ringset = set(y for x in I for y in adj[x]) - Is
    # order the ring: walk; each ring vertex must have exactly 2 ring neighbours
    for y in ringset:
        if len(adj[y] & ringset) != 2: return None, 'ring not an induced cycle at %d' % y
    start = min(ringset); order = [start]; prev = None; cur = start
    while True:
        nb = sorted(adj[cur] & ringset); nxt = nb[0] if nb[0] != prev else nb[1]
        if nxt == start: break
        order.append(nxt); prev, cur = cur, nxt
    if len(order) != len(ringset): return None, 'ring has several components'
    ri = {y: j for j, y in enumerate(order)}; ii = {x: j for j, x in enumerate(I)}
    ia = [sorted(ii[y] for y in adj[x] if y in Is) for x in I]
    ra = [sorted(ri[y] for y in adj[x] if y in ringset) for x in I]
    D = [len(rot[x]) for x in I]
    return ball.fmt_config(name, (len(order), len(I), D, ia, ra)), 'ok'
