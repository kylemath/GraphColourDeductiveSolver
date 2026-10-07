"""[exploratory] All strict R3 states at k = 4 (resp. k = 3) of (5,5,5,5,6) holes: excursion (i, u, f) of a Lock2-only (resp. Lock1-only) sigma-image, and the
run of lock types along it; also the lockless images' f."""
import sys, os, json
from collections import Counter
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'simg.py')).read().split("if __name__")[0]
exec(src)
C = Counter()
def lk(H, s):
    a, b = H.locks(s); return 'DL' if a and b else 'L1' if a else 'L2' if b else 'no'
def run(rot, h):
    uv_lib.load = lambda name, mirror: rot
    H = uv_lib.Hole('x', h, False); q = next(t for t in range(5) if len(rot[H.L[t]]) == 6)
    for r in range(H.S):
        if H.filled(r): continue
        j, ty, hi, (al, mu, A, B) = H.frame(r); k = (q - j) % 5
        if ty != 3 or k not in (3, 4) or [H.col(r, H.w[(j + t) % 5]) for t in range(5)] != [B, A, B, mu, A]: continue
        s = H.sigma(r); t = lk(H, s)
        a = s; i = 0
        while not H.filled(H.pinv[a]): a = H.pinv[a]; i += 1
        u = 0; b = a; seq = []
        while not H.filled(b): seq.append(lk(H, b)); b = H.pi[b]; u += 1
        f = 0
        while H.filled(b): b = H.pi[b]; f += 1
        C[(k, lk(H, r), t, i, u, f)] += 1
G = os.path.join(HERE, '../../../studiointel/gentri/tri%d.txt')
for n in [int(x) for x in sys.argv[1].split(',')]:
    for gi, l in enumerate(open(G % n)):
        if not l.startswith('G'): continue
        rot0 = gentri_rotation(l)
        for mir in (0, 1):
            rot = [list(reversed(x)) for x in rot0] if mir else rot0
            for h in holes6(rot): run(rot, h)
for k, v in sorted(C.items()): print(k, v)
