"""Rule X's hat z (r in w2's frame) as a degree-d receiver under the 7/27 y, first order.
Arrangement: link lk[0..d-1], s-word sv (sv[i] between lk[i], lk[i+1]).  e-class firing at j: lk[j]=6, lk[j+1]=5,
sv[j]=5, sv[j+1]=5 (or the mirror lk[j]=5, lk[j+1]=6, sv[j]=5, sv[j-1]=5).  Any-X firing: sv[j]=5, {lk[j],lk[j+1]}={5,6}.
Fixed: lk[0]=6, lk[1]=5, sv[0]=5, sv[1]=5.  Output: top arrangements by load, c-check (sep3) applied, and
cap = (BAR - load)/k.  usage: python3 zload.py D"""
import sys, itertools, heapq
from load import yv, ix, root, check
d = int(sys.argv[1]); FIX2 = len(sys.argv) > 2 and sys.argv[2] == "x4"; L5 = (5, 6, 7, 8, 9); BAR = d - 6 + 7 / 27
Yc = {}
def Y(w):
    if w not in Yc:
        r = root(list(w), 0); Yc[w] = yv[ix[r]] if r in ix else None   # None: R5 word (forbidden)
    return Yc[w]
def load(lk, sv):
    out = 0.0
    for i in range(d):
        if lk[i] == 5:
            y = Y((min(d, 9), lk[(i + 1) % d], sv[i], sv[i - 1], lk[i - 1]))
            if y is None: return None
            out += y
    return out
def ke(lk, sv):
    k = 0
    for j in range(d):
        a, b = lk[j], lk[(j + 1) % d]
        if sv[j] == 5 and a == 6 and b == 5 and sv[(j + 1) % d] == 5: k += 1
        if sv[j] == 5 and a == 5 and b == 6 and sv[j - 1] == 5: k += 1
    return k
def kT(lk, sv): return sum(1 for j in range(d) if sv[j] == 5 and min(lk[j], lk[(j + 1) % d]) == 6 and max(lk[j], lk[(j + 1) % d]) >= 7)
def kall(lk, sv): return sum(1 for j in range(d) if sv[j] == 5 and {lk[j], lk[(j + 1) % d]} == {5, 6})
from array import array
import numpy as np
LO = {}; CO = {}; n = 0
for code, (rest, srest) in enumerate(itertools.product(itertools.product(L5, repeat=d - 2), itertools.product(L5, repeat=d - 2))):
    lk = (6, 5) + rest; sv = (5, 5) + srest; n += 1
    if FIX2 and lk[2] != 6: continue
    v = load(lk, sv)
    if v is None: continue
    if v < BAR - 0.3: continue
    k = ke(lk, sv) + 10 * min(kT(lk, sv), 1)
    LO.setdefault(k, array('d')).append(v); CO.setdefault(k, array('q')).append(code)
def decode(code):
    m = 5 ** (d - 2); a, b = divmod(code, m)
    def dig(x):
        out = []
        for _ in range(d - 2): x, r = divmod(x, 5); out.append(L5[r])
        return tuple(reversed(out))
    return (6, 5) + dig(a), (5, 5) + dig(b)
print('# d', d, 'arrangements', n, 'non-R5', sum(len(x) for x in LO.values()))
for k in sorted(LO):
    lo = np.frombuffer(LO[k]); order = np.argsort(-lo); shown = 0; tried = 0; kk = k % 10
    for i in order:
        lk, sv = decode(CO[k][i]); L = ''.join(map(str, lk)); S = ''.join(map(str, sv)); tried += 1
        if check(d, L, S):
            v = lo[i]
            print('k_e=%d kT=%d kall=%d load %.4f cap %.4f  link %s s %s  (rank %d)' % (kk, kT(lk, sv), kall(lk, sv), v, (BAR - v) / kk if kk else float('nan'), L, S, tried)); shown += 1
            if shown >= 3: break
