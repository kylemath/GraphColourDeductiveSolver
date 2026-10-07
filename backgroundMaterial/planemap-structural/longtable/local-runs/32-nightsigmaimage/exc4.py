"""[exploratory] Every excursion of every class at (5,5,5,5,6) holes (gentri orders given): for u >= 2, what is sigma(start) and sigma(end)
(frame type ty, k, strict R3?, locks)?  Tests whether the (u=4, f=1) excursions are exactly the k = 4 failure images."""
import sys, os, json
from collections import Counter
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'simg.py')).read().split("if __name__")[0]
exec(src)
C = Counter()
def lk(H, s):
    a, b = H.locks(s); return 'DL' if a and b else 'L1' if a else 'L2' if b else 'no'
def desc(H, q, r):
    j, ty, hi, (al, mu, A, B) = H.frame(r); k = (q - j) % 5
    st = ty == 3 and [H.col(r, H.w[(j + t) % 5]) for t in range(5)] == [B, A, B, mu, A]
    return ('R3s' if st else 'ty%d' % ty, k, lk(H, r))
def run(rot, h):
    uv_lib.load = lambda name, mirror: rot
    H = uv_lib.Hole('x', h, False); q = next(t for t in range(5) if len(rot[H.L[t]]) == 6)
    for a in range(H.S):
        if H.filled(a) or not H.filled(H.pinv[a]): continue
        u = 0; b = a; last = a
        while not H.filled(b): last = b; b = H.pi[b]; u += 1
        f = 0
        while H.filled(b): b = H.pi[b]; f += 1
        if u < 2: continue
        sa = H.sigma(a); se = H.sigma(last)
        C[(u if u <= 5 else '6+', f if f <= 2 else '3+', 'start', desc(H, q, a)[:2], 'sig', 'fix' if sa == a else desc(H, q, sa))] += 1
G = os.path.join(HERE, '../../../studiointel/gentri/tri%d.txt')
for n in [int(x) for x in sys.argv[1].split(',')]:
    for gi, l in enumerate(open(G % n)):
        if not l.startswith('G'): continue
        rot0 = gentri_rotation(l)
        for mir in (0, 1):
            rot = [list(reversed(x)) for x in rot0] if mir else rot0
            for h in holes6(rot): run(rot, h)
for k, v in sorted(C.items(), key=str): print(k, v)
