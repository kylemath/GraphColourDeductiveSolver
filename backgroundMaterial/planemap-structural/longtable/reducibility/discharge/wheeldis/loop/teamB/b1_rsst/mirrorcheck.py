"""Self-check: the symmetrized rule list must give the same transfer on every directed edge of a sphere and of its
mirror image (all rotations reversed).  Spheres: random closed layered discs from b8b/rings.close."""
import sys, os, random
HERE = os.path.dirname(os.path.abspath(__file__))
DIS = os.path.abspath(os.path.join(HERE, '../../../..'))
sys.path.insert(0, os.path.join(DIS, 'b8b')); sys.path.insert(0, DIS); sys.path.insert(0, HERE)
from rings import Layered, close
import rsst
from collections import Counter

rng = random.Random(1)
nsph = 0; nedge = 0; nunits = 0; bad = 0; tot_ok = 0
for trial in range(60):
    d = rng.choice([5, 6, 7, 8])
    L = Layered(d)
    L.add_ring([rng.choice([5, 5, 6, 6, 7]) for _ in L.ring()])
    res = close(L, rng)
    if res is None:
        continue
    rot = res[0]
    deg = {v: min(len(r), 9) for v, r in enumerate(rot)}
    M = rsst.Map(rot, deg)
    Mm = rsst.Map([list(reversed(r)) for r in rot], deg)
    c1 = Counter(); c2 = Counter()
    for v in range(len(rot)):
        for t, nm in M.sends(v): c1[(v, t)] += 1
        for t, nm in Mm.sends(v): c2[(v, t)] += 1
    nsph += 1; nedge += len(set(c1) | set(c2)); nunits += sum(c1.values())
    if c1 != c2: bad += 1
    score = sum(10 * (6 - len(rot[v])) for v in range(len(rot)))
    if score == 120: tot_ok += 1
print(f'spheres {nsph}, edges with transfer {nedge}, units {nunits}, mirror mismatches {bad}, Euler ok {tot_ok}')
