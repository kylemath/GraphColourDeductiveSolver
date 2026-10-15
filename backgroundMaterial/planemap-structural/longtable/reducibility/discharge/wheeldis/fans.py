"""Fans (exploratory): a degree-5 centre with link word over {5,6,7,8,F}, F = a link vertex left OUT of the
configuration (it becomes a ring vertex; its degree is free, so a reducible fan makes every wheel that agrees with it
on the non-F positions reducible, whatever the F degrees, e.g. >= 9).  Writes fans.txt (dfast/cfast format), ring <= 16.
Usage: python3 fans.py [maxF=2]"""
import sys, itertools, os
HERE = os.path.dirname(os.path.abspath(__file__))
MAXF = int(sys.argv[1]) if len(sys.argv) > 1 else 2
def canon(w):
    return min(min(s[k:] + s[:k] for k in range(5)) for s in (tuple(w), tuple(w)[::-1]))
def config(word):
    """word: 5 letters, 0 = F.  Build the full wheel free completion (F given degree 9), then interior = centre +
    non-F link vertices, ring = N(I) minus I, which must be an induced cycle."""
    deg = [d if d else 9 for d in word]
    adj = {}
    def E(a, b): adj.setdefault(a, set()).add(b); adj.setdefault(b, set()).add(a)
    ring = []
    for i, d in enumerate(deg):
        for p in range(d - 5): ring.append(('p', i, p))
        ring.append(('s', i))
    for j in range(len(ring)): E(ring[j], ring[(j + 1) % len(ring)])
    for i, d in enumerate(deg):
        x = ('x', i); E(('c',), x); E(x, ('x', (i + 1) % 5))
        E(x, ('s', (i - 1) % 5)); E(x, ('s', i))
        for p in range(d - 5): E(x, ('p', i, p))
    I = [('c',)] + [('x', i) for i in range(5) if word[i]]
    Is = set(I); RS = set(y for x in I for y in adj[x]) - Is
    for y in RS:
        if len(adj[y] & RS) != 2: return None
    start = sorted(RS)[0]; order = [start]; prev = None
    while True:
        cur = order[-1]; nb = sorted(adj[cur] & RS); nxt = nb[0] if nb[0] != prev else nb[1]
        if nxt == start: break
        order.append(nxt); prev = cur
    if len(order) != len(RS): return None
    ri = {y: j for j, y in enumerate(order)}; ii = {x: j for j, x in enumerate(I)}
    ia = [sorted(ii[y] for y in adj[x] if y in Is) for x in I]
    ra = [sorted(ri[y] for y in adj[x] if y in RS) for x in I]
    for x, nb in zip(I, ia):
        dx = 5 if x == ('c',) else deg[x[1]]
        assert len(adj[x]) == dx
    f = lambda Ls: ';'.join(','.join(map(str, v)) if v else '-' for v in Ls)
    return len(order), len(I), f(ra), f(ia)
seen = set(); out = []
for w in itertools.product((0, 5, 6, 7, 8), repeat=5):
    nf = w.count(0)
    if nf == 0 or nf > MAXF: continue
    k = canon(w)
    if k in seen: continue
    seen.add(k); c = config(list(k))
    if c is None or c[0] > 16: continue
    out.append((c[0], 'f_' + ''.join('F' if d == 0 else str(d) for d in k), c))
out.sort()
with open(os.path.join(HERE, 'fans.txt'), 'w') as fh:
    for r, nm, (rr, m, ra, ia) in out: fh.write('%s %d %d %s %s\n' % (nm, rr, m, ra, ia))
print(len(out), 'fans')
