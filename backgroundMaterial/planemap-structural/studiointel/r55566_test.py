#!/usr/bin/env python3
"""studiointel r55566_test.py -- [exploratory] kill test of Math's Theorem R5^3 (MathRstar55566.md item 1), written from its statement only:
 T with no separating triangle; v of degree 5, link y0..y4 in rotation order with deg y0 = deg y1 = deg y2 = 5 (y3, y4 any degree).
 Claim: every DL state at v has radius <= 7, and <= 6 when the repeat pair is {y3,y0} or {y2,y4}.
Radius = exact, by BFS over whole-component swaps in T - v (radius.py definitions). Every frame (choice of three consecutive 5s, either
rotation sense) is tested. Input: graph JSON files, or gen_tri output files (prefix gt:)."""
import sys, json, itertools
from collections import deque, Counter, defaultdict
sys.path.insert(0, '.')
import radius, graphs
from coset_potential import orient

def graphs_from(arg):
    if arg.startswith('gt:'):
        for line in open(arg[3:]):
            t = line.split()
            if not t or t[0] != 'G': continue
            nf = int(t[3]); x = list(map(int, t[4:4 + 3 * nf]))
            yield '%s#%s' % (arg[3:].split('/')[-1], t[2][:12]), orient([tuple(x[3 * i:3 * i + 3]) for i in range(nf)])
    else:
        yield arg, [tuple(f) for f in json.load(open(arg))['faces']]

viol = []; stat = Counter(); maxr = defaultdict(int); nh = 0
for arg in sys.argv[1:]:
    for name, F in graphs_from(arg):
        assert graphs.check_triangulation(F)[0]
        if graphs.n_separating_triangles(F): stat['skipped: separating triangle'] += 1; continue
        deg = graphs.degrees(F)
        for v in sorted(u for u in deg if deg[u] == 5):
            order, idx, nb, link = radius.prepare(F, v); L = [order[i] for i in link]
            frames = []
            for i in range(5):
                for sense in (1, -1):
                    Y = [L[(i + sense * k) % 5] for k in range(5)]
                    if all(deg[Y[k]] == 5 for k in (0, 1, 2)): frames.append(Y)
            if not frames: continue
            nh += 1
            states = radius.enumerate_states(nb, 10 ** 7); cls = {s: radius.classify(nb, link, s) for s in states}
            dist = {s: 0 for s in states if cls[s] != 2}; q = deque(dist)
            while q:
                s = q.popleft()
                for t in radius.swaps(nb, s):
                    if t not in dist: dist[t] = dist[s] + 1; q.append(t)
            cl = tuple(sorted(deg[y] for y in L))
            for s in states:
                if cls[s] != 2: continue
                r = 1 + dist[s] if s in dist else None
                col = {order[i]: s[i] for i in range(len(s))}
                rep = [y for y in L if sum(col[z] == col[y] for z in L) == 2]
                maxr[cl] = max(maxr[cl], 99 if r is None else r); stat['DL states'] += 1
                for Y in frames:
                    special = set(rep) in ({Y[3], Y[0]}, {Y[2], Y[4]})
                    bound = 6 if special else 7
                    if r is None or r > bound:
                        viol.append({'graph': name, 'hole': v, 'frame': Y, 'repeat': rep, 'radius': r, 'bound': bound, 'state': {str(order[i]): s[i] for i in range(len(s))}})
print('holes tested', nh, dict(stat))
print('max radius per link-degree class (sorted):', dict(sorted(maxr.items())))
print('VIOLATIONS', len(viol))
for x in viol[:5]: print(json.dumps(x))
json.dump(viol, open('r55566_violations.json', 'w'))
