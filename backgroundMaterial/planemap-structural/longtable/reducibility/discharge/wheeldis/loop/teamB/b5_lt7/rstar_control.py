"""Control for contain.py on round B1's R*: every non-zero R* case (round 42 found each dead to an RSST
configuration) should get a hit; report hit rate on non-zero and on a sample of zero cases."""
import sys, os, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'b1_rsst'))
import contain, rstar

def disc(key):
    s1, s4 = int(key[0]), int(key[1]); priv = tuple(int(c) for c in key[2:])
    rot, deg, w, S, R3 = rstar.build(s1, s4, priv)
    known = {x for x in deg if deg[x] is not None and len(rot[x]) == deg[x]}
    return rot, deg, known

def hit(key, mode='strict'):
    rot, deg, known = disc(key)
    for c in contain.CONFS:
        if contain.embed(c, rot, deg, known, mode):
            return c[0]
    return None

nz = [l.split()[0] for l in open(os.path.join(HERE, '..', 'nonzero.txt')) if not l.startswith('#')]
random.seed(1)
S = random.sample(nz, 300)
h = sum(1 for k in S if hit(k))
print('R* non-zero sample: %d/300 contain a published configuration (strict)' % h)
nzs = set(nz)
allk = ['%d%d%s' % (a, b, ''.join(p)) for a in (6, 7, 8, 9) for b in (6, 7, 8, 9)
        for p in [tuple(random.choice('56789') for _ in range(6)) for _ in range(40)]]
Z = [k for k in allk if k not in nzs][:300]
hz = [k for k in Z if hit(k)]
print('R* zero-score sample: %d/%d contain one (strict)' % (len(hz), len(Z)), hz[:5])
