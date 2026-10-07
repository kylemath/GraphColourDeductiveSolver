"""[exploratory] sigma-images of the R1 states of a Gamma-cycle Z that are DL: which cycle, which period position, offset."""
import json, sys
from collections import Counter
src = open('simg.py').read().split("if __name__")[0]; exec(src)
d = json.load(open(os.path.join(HERE, '../27-studio-positive-config/jobuv/jobak-66dump.json'))); seen = set(); C = Counter(); M = Counter()
for r in d:
    key = (r['run'], r['name'], r['hole'])
    if key in seen: continue
    seen.add(key); res, H = analyse(r['rotation'], r['hole'], '')
    q = next(t for t in range(5) if len(r['rotation'][H.L[t]]) == 6)
    def pos(x):
        j, ty, hi, ro = H.frame(x); return NM.get((ty, (q - j) % 5))
    for z in res:
        Z = H.cycles[z['cyc']]; L = len(Z); Ts = Counter()
        for n, x in enumerate(Z):
            j, ty, hi, ro = H.frame(x)
            if ty != 1: continue
            s = H.sigma(x)
            if s == x or not H.DL[s]: continue
            T = H.cyc[s]; TG = all(H.DL[y] for y in H.cycles[T])
            C[('onZ' if T == z['cyc'] else 'otherGamma' if TG else 'nonGamma', pos(x), pos(s), (Z.index(s) - n) % L if T == z['cyc'] else '')] += 1
            if T != z['cyc'] and TG: Ts[T] += 1
        M[len(Ts)] += 1
for k, v in sorted(C.items(), key=str): print(k, v)
print('number of distinct other Gamma-cycles hit by R1 images, per Z:', dict(M))
