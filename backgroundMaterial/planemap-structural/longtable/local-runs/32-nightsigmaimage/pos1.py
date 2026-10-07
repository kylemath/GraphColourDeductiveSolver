"""[exploratory] Windows r0 -> t -> r2 with t = R1 at k = 1 (period position 1) and r0 = pi^{-1} t, r2 = pi t (strict R3 at k = 4, 3), all DL:
joint distribution of (k=4 failure at r0, sigma fixed at t, k=3 failure at r2). Gentri orders given + the jobak dump holes."""
import sys, os, json
from collections import Counter
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'simg.py')).read().split("if __name__")[0]
exec(src)
C = Counter()
def strict(H, r):
    j, ty, hi, (al, mu, A, B) = H.frame(r)
    return ty == 3 and [H.col(r, H.w[(j + t) % 5]) for t in range(5)] == [B, A, B, mu, A]
def run(rot, h, gam):
    uv_lib.load = lambda name, mirror: rot
    H = uv_lib.Hole('x', h, False); q = next(t for t in range(5) if len(rot[H.L[t]]) == 6)
    for t in range(H.S):
        if not H.DL[t]: continue
        j, ty, hi, roles = H.frame(t)
        if ty != 1 or (q - j) % 5 != 1: continue
        r0, r2 = H.pinv[t], H.pi[t]
        if not (H.DL[r0] and H.DL[r2] and strict(H, r0) and strict(H, r2)): continue
        if (q - H.frame(r0)[0]) % 5 != 4 or (q - H.frame(r2)[0]) % 5 != 3: continue
        f0 = H.locks(H.sigma(r0))[1]; f2 = H.locks(H.sigma(r2))[0]; fx = H.sigma(t) == t
        g = all(H.DL[x] for x in H.cycles[H.cyc[t]])
        C[('Gamma' if g else 'open', int(f0), int(fx), int(f2))] += 1
G = os.path.join(HERE, '../../../studiointel/gentri/tri%d.txt')
for n in [int(x) for x in sys.argv[1].split(',') if x]:
    for gi, l in enumerate(open(G % n)):
        if not l.startswith('G'): continue
        rot0 = gentri_rotation(l)
        for mir in (0, 1):
            rot = [list(reversed(x)) for x in rot0] if mir else rot0
            for h in holes6(rot): run(rot, h, False)
if 'dump' in sys.argv:
    d = json.load(open(os.path.join(HERE, '../27-studio-positive-config/jobuv/jobak-66dump.json'))); seen = set()
    for r in d:
        key = (r['run'], r['name'], r['hole'])
        if key in seen: continue
        seen.add(key); run(r['rotation'], r['hole'], True)
print('(cycle kind, fail k=4 at pos 0, sigma fixed at pos 1, fail k=3 at pos 2): count')
for k, v in sorted(C.items()): print(' ', k, v)
