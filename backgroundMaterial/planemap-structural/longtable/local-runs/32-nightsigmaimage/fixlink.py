"""[exploratory] Test on ALL states (not only Gamma) of (5,5,5,5,6) holes: for r = R3 at k=4 (resp. k=3) with Lock2 (so pi r = R+3 r):
k=4: sigma(r) Lock2-only  vs  sigma fixed at pi(r) (R1, k=1).  k=3: sigma(r) Lock1-only vs sigma fixed at pi^{-1}(r) (R1, k=1)."""
import sys, os, json
from collections import Counter
sys.argv = [sys.argv[0]] + sys.argv[1:]
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'simg.py')).read().split("if __name__")[0]
exec(src)
C = Counter(); ex = []
def run(rot, h, tag):
    uv_lib.load = lambda name, mirror: rot
    H = uv_lib.Hole('x', h, False); q = next(t for t in range(5) if len(rot[H.L[t]]) == 6)
    for r in range(H.S):
        if H.filled(r): continue
        j, ty, hi, roles = H.frame(r); k = (q - j) % 5
        if ty != 3 or k not in (3, 4): continue
        al, mu, A, B = roles
        if [H.col(r, H.w[(j + t) % 5]) for t in range(5)] != [B, A, B, mu, A]: continue
        l1, l2 = H.locks(r)
        s = H.sigma(r); a1, a2 = H.locks(s)
        if k == 4:
            if not l2: continue
            t = H.pi[r]; fx = H.sigma(t) == t
            C[('k4', 'DL' if l1 else 'L2only', 'fail' if a2 else 'ok', 'fixed@pi' if fx else 'nf@pi', 'piDL' if H.DL[t] else 'pinotDL', 'prevDL' if H.DL[H.pinv[r]] else 'prevnotDL')] += 1
        else:
            continue
            t = H.pinv[r]; fx = H.sigma(t) == t
            C[('k3', 'DL' if l2 else 'L1only', 'fail' if a1 else 'ok', 'fixed@pinv' if fx else 'nf@pinv', 'pinvDL' if H.DL[t] else 'pinvnotDL')] += 1
if __name__ == '__main__':
    G = os.path.join(HERE, '../../../studiointel/gentri/tri%d.txt')
    for n in [int(x) for x in sys.argv[1].split(',')]:
        for gi, l in enumerate(open(G % n)):
            if not l.startswith('G'): continue
            rot0 = gentri_rotation(l)
            for mir in (0, 1):
                rot = [list(reversed(x)) for x in rot0] if mir else rot0
                for h in holes6(rot): run(rot, h, '')
    d = json.load(open(os.path.join(HERE, '../27-studio-positive-config/jobuv/jobak-66dump.json'))); seen = set()
    if 'dump' in sys.argv:
        for r in d:
            key = (r['run'], r['name'], r['hole'])
            if key in seen: continue
            seen.add(key); run(r['rotation'], r['hole'], key)
    for k, v in sorted(C.items()): print(k, v)
