"""[exploratory] All R3 states with k <= 2 at (5,5,5,5,6) holes (gentri orders given): lock type of sigma(r) by lock type of r."""
import sys, os, json
from collections import Counter
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'simg.py')).read().split("if __name__")[0]
exec(src)
C = Counter()
G = os.path.join(HERE, '../../../studiointel/gentri/tri%d.txt')
for n in [int(x) for x in sys.argv[1].split(',')]:
    for gi, l in enumerate(open(G % n)):
        if not l.startswith('G'): continue
        rot0 = gentri_rotation(l)
        for mir in (0, 1):
            rot = [list(reversed(x)) for x in rot0] if mir else rot0
            for h in holes6(rot):
                uv_lib.load = lambda name, mirror: rot
                H = uv_lib.Hole('x', h, False); q = next(t for t in range(5) if len(rot[H.L[t]]) == 6)
                for r in range(H.S):
                    if H.filled(r): continue
                    j, ty, hi, roles = H.frame(r); k = (q - j) % 5
                    al, mu, A, B = roles
                    if ty == 3 and [H.col(r, H.w[(j + t) % 5]) for t in range(5)] != [B, A, B, mu, A]: ty = 4
                    l1, l2 = H.locks(r); s = H.sigma(r); a1, a2 = H.locks(s)
                    tr = 'DL' if l1 and l2 else 'L1' if l1 else 'L2' if l2 else 'no'
                    ts = 'fix' if s == r else 'DL' if a1 and a2 else 'L1' if a1 else 'L2' if a2 else 'no'
                    C[(ty, k, tr, ts)] += 1
for k, v in sorted(C.items()): print(k, v)
