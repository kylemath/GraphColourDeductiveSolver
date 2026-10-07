"""[exploratory] fixed-point (f_i = 1, i.e. sigma fixed <=> G_{alpha,mu} connected) patterns along Gamma-cycles and open DL runs."""
import sys, os, json
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../27-studio-positive-config/jobuv'))
import uv_lib
from kempe_py import gentri_rotation
from w2e import holes6, NM
C = Counter()
def run(rot, h):
    uv_lib.load = lambda name, mirror: rot
    H = uv_lib.Hole('x', h, False)
    q = next(t for t in range(5) if len(rot[H.L[t]]) == 6)
    def pos(k):
        j, ty, hi, roles = H.frame(k); return NM.get((ty, (q - j) % 5))
    for Z in H.cycles:
        dl = [H.DL[x] for x in Z]
        if not any(dl): continue
        n = len(Z); fx = [H.DL[x] and H.sigma(x) == x for x in Z]; P = [pos(x) if H.DL[x] else None for x in Z]
        g = all(dl)
        for i in range(n):
            if not dl[i]: continue
            # length of DL run through i (both directions), capped
            if g: kind = 'Gamma'
            else: kind = 'open'
            if P[i] is None: continue
            # triples of fixed points at i, i+2, i+4 inside DL
            if all(dl[(i + d) % n] for d in range(5)):
                pat = ''.join('F' if fx[(i + d) % n] else '-' for d in range(5))
                C[(kind, 'window5 from pos', P[i], pat)] += 1
for a in sys.argv[1:]:
    if a == 'dump':
        d = json.load(open(os.path.join(HERE, '../27-studio-positive-config/jobuv/jobak-66dump.json'))); seen = set()
        for r in d:
            key = (r['run'], r['name'], r['hole'])
            if key in seen: continue
            seen.add(key); run(r['rotation'], r['hole'])
    else:
        n = int(a); G = os.path.join(HERE, '../../../studiointel/gentri/tri%d.txt')
        for l in open(G % n):
            if not l.startswith('G'): continue
            rot0 = gentri_rotation(l)
            for mir in (0, 1):
                rot = [list(reversed(x)) for x in rot0] if mir else rot0
                for h in holes6(rot): run(rot, h)
# summarise: per kind and start pos, patterns with F at offsets 0,2,4
S = Counter()
for (kind, _, p, pat), v in C.items():
    S[(kind, p, pat[0] + pat[2] + pat[4])] += v
for k in sorted(S): print(k, S[k])
print('full 5-patterns with >=3 F:')
for k in sorted(C):
    if k[3].count('F') >= 3: print(' ', k, C[k])
