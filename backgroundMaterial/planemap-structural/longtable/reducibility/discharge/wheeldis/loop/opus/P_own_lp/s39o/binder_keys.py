"""s39o: binder list of a lowerR2 cert in canonical keys.  usage: python3 binder_keys.py CERT.json [LABEL]
Prints every receiver row of the cert (w d LINK SWORD, the explore rows-file format, most negative weight first) plus its
canonical key: the lexicographically least (LINK, SWORD) over the 2d rotations/reflections of pcheck.instances
(rotation w_i -> w_{i+r}, s_i -> s_{i+r}; reflection w_i -> w_{r-i}, s_i -> s_{r-i-1})."""
import sys, json
from fractions import Fraction
def wv(w): return float(Fraction(w)) if isinstance(w, str) else float(w)
def ckey(lk, sv):
    d = len(lk); best = None
    for r in range(d):
        for refl in (0, 1):
            if refl: L = ''.join(lk[(r - i) % d] for i in range(d)); S = ''.join(sv[(r - i - 1) % d] for i in range(d))
            else: L = ''.join(lk[(i + r) % d] for i in range(d)); S = ''.join(sv[(i + r) % d] for i in range(d))
            if best is None or (L, S) < best: best = (L, S)
    return '%d:%s/%s' % (d, best[0], best[1])
C = json.load(open(sys.argv[1])); lab = sys.argv[2] if len(sys.argv) > 2 else sys.argv[1]
R = sorted(((wv(e['w']), e['row'][1], e['row'][2], e['row'][3]) for e in C if e['row'][0] in ('receiver', 'receiverR2')), key=lambda x: x[0])
print('# %s: the %d receiverR2 rows (w d link second-ring canonical-key), most negative weight first' % (lab, len(R)))
for w, d, lk, sv in R: print(w, d, lk, sv, ckey(lk, sv))
