"""B8b (exploratory): case (a) at degree 7 — explicit class graphs around a 7 for the block-model arrangements with
the most relaxed senders; counts lone-7 senders whose keys are untested (U) or tested not D-reducible (notD).
Usage: search7.py D MINSENDERS MAXARR"""
import sys, os, random, itertools
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import ball, construct, patch
from maxsend import BLOCKS, count
from centred import canon
from rings import Layered, close

d, mins, maxarr = map(int, sys.argv[1:4])
seen = set(); arrs = []
for seq in itertools.product(range(6), repeat=d):
    c = canon([BLOCKS[b] for b in seq])
    if c in seen: continue
    seen.add(c); k, who = count(list(c), d)
    if k >= mins: arrs.append((k, c))
arrs.sort(key=lambda z: -z[0]); best = (0, None)
fn = os.path.join(HERE, 'out', 'search%d.txt' % d)
open(fn, 'w').close()
for k, c in arrs[:maxarr]:
    flat = []
    for dw, p, s in c:
        if p is not None: flat.append(p)
        flat.append(s)
    flat = [flat[-1]] + flat[:-1]
    got = None
    for seed in range(1, 25):
        L = Layered(d); L.add_ring([b[0] for b in c])
        try:
            L.add_ring(flat)
            R = L.ring(); L.add_ring([L.inn[x] + 4 for x in R])     # third ring all degree 6 (out 2)
            R = L.ring(); L.add_ring([L.inn[x] + 4 for x in R])
        except AssertionError: break
        res = close(L, random.Random(seed), maxtries=200)
        if res: got = res[0]; break
    if got is None: print('relaxed %d  %s  no closure' % (k, c)); continue
    S = patch.senders(got, 0)
    lone = [s for s in S if s['lone']]; nonR = [s for s in lone if s['status'] in ('U', 'notD')]
    print('relaxed %d  lone %d  nonR(a) %d  notD %d  %s' % (k, len(lone), len(nonR),
          sum(s['status'] == 'notD' for s in lone), c))
    patch.write_graph(fn, 'd%d_' % d + '_'.join('%d.%s.%d' % (a, '-' if b is None else b, e) for a, b, e in c), got)
    if len(nonR) > best[0]: best = (len(nonR), c)
print('best case-(a) count', best)
