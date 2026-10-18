"""Rule H's hat b (new w2 frame 7665675) as a degree-d receiver under the 7/27 y, first order (y fixed, new flows
uniform).  b's link (x3 6, y 6, x4 5, ...), s-word (e 5, s2 7, ...).  kH = s-slots sv[j] = 5 between two link 6s
(rule-H firings; lone-ness of that five is not visible here, so all are counted).  kT = T inflow slots.
cap = (BAR - load) / kH.  usage: python3 hload.py D"""
import sys, itertools
import numpy as np
from load import yv, ix, root, check
d = int(sys.argv[1]); L5 = (5, 6, 7, 8, 9); BAR = d - 6 + 7 / 27; Yc = {}
def Y(w):
    if w not in Yc:
        r = root(list(w), 0); Yc[w] = yv[ix[r]] if r in ix else None
    return Yc[w]
def load(lk, sv):
    out = 0.0
    for i in range(d):
        if lk[i] == 5:
            y = Y((min(d, 9), lk[(i + 1) % d], sv[i], sv[i - 1], lk[i - 1]))
            if y is None: return None
            out += y
    return out
kH = lambda lk, sv: sum(1 for j in range(d) if sv[j] == 5 and lk[j] == 6 and lk[(j + 1) % d] == 6)
kT = lambda lk, sv: sum(1 for j in range(d) if sv[j] == 5 and min(lk[j], lk[(j + 1) % d]) == 6 and max(lk[j], lk[(j + 1) % d]) >= 7)
rows = []
for rest in itertools.product(L5, repeat=d - 3):
    lk = (6, 6, 5) + rest
    for srest in itertools.product(L5, repeat=d - 2):
        sv = (5, 7) + srest; v = load(lk, sv)
        if v is None or v < BAR - 0.4: continue
        rows.append(((BAR - v) / kH(lk, sv), v, lk, sv))
rows.sort(key=lambda r: r[0]); shown = 0
for cap, v, lk, sv in rows:
    L = ''.join(map(str, lk)); S = ''.join(map(str, sv))
    if check(d, L, S):
        print('cap %.4f load %.4f kH %d kT %d link %s s %s' % (cap, v, kH(lk, sv), kT(lk, sv), L, S)); shown += 1
        if shown >= 8: break
