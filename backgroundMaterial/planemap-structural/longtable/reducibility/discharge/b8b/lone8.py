"""B8b (exploratory): explicit class graphs around a receiver u (vertex 0) of degree d.
  hemi(d)          : link all 6, the d private second-ring vertices of degree 5, rest 6; cylinder; mirror cap.
                     Total curvature per cap 6, so the sphere is cap + cylinder (circumference 2d) + cap.
  alt(d, S)        : link all 6, private second-ring vertices p_i of degree 5 for i in S, all else 6 out to
                     radius 4; closed by rings.close (random shrinking schedule, class-checked).
  linkfives(d, S)  : link vertices w_i of degree 5 for i in S (distance-1 senders), rest as alt with no p-5s.
Every graph is checked by ball.class_check (+ diamond/2.122 test) and analysed by patch.report.
Graphs are appended to b8b/out/patches.txt ('name n rot')."""
import sys, os, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
import ball, construct
from rings import Layered, close
import patch


def hemi(d, cyl=3):
    L = Layered(d); L.add_ring([6] * d)
    R = L.ring(); L.add_ring([5 if L.inn[x] == 1 else 6 for x in R])
    for _ in range(cyl): R = L.ring(); L.add_ring([6] * len(R))
    R = L.ring(); L.add_ring([5 if j % 2 == 0 else 6 for j in range(len(R))])
    R = L.ring(); L.add_ring([L.inn[x] + 3 for x in R])
    return L.rot()


def alt(d, S, seed=1, flat=2, linkdeg=None):
    L = Layered(d); L.add_ring(linkdeg or [6] * d)
    R = L.ring(); degs = []; pi = 0
    # private second-ring vertices are those with in == 1; number them in ring order
    for x in R:
        if L.inn[x] == 1: degs.append(5 if pi in S else 6); pi += 1
        else: degs.append(6)
    L.add_ring(degs)
    for _ in range(flat): R = L.ring(); L.add_ring([L.inn[x] + 4 for x in R])     # all 6 if in = 2, 5..: out 2
    res = close(L, random.Random(seed))
    return None if res is None else res[0]


def check(rot, name, fn=None):
    cc = ball.class_check(rot); dia = construct.has_diamond_or_2122(rot)
    print('#', name, 'class', cc, 'diamond/2.122', dia)
    S = patch.report(rot, 0, name)
    if fn: patch.write_graph(fn, name, rot)
    return cc['in_class'], S


if __name__ == '__main__':
    fn = os.path.join(HERE, 'out', 'patches.txt')
    if os.path.exists(fn): os.remove(fn)
    for d in (7, 8, 9, 10):
        check(hemi(d), 'hemi%d' % d, fn)
    # flat lone-big senders at every other private position
    for d, S in ((7, {0, 2, 4}), (8, {0, 2, 4, 6}), (8, {0, 3, 5})):
        for seed in range(1, 40):
            rot = alt(d, S, seed)
            if rot is not None: break
        if rot is None: print('alt', d, S, 'no closure found'); continue
        check(rot, 'alt%d_%s' % (d, ''.join(map(str, sorted(S)))), fn)
