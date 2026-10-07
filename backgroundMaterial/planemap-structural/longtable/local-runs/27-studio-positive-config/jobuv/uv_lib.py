"""[exploratory] Jobs U and V helper: independent Python (kempe_py.Space + escape.pi_of/is_DL) for one hole of an order-27 plantri graph, either orientation."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../common')); sys.path.insert(0, os.path.join(HERE, '../../22-winding-escape'))
from kempe_py import Space
from escape import pi_of, is_DL
from collections import Counter
def load(name, mirror):
    order = name.split('#')[0][1:]
    for l in open(os.path.join(HERE, '../in-plantri-%s.txt' % order)):
        if l.startswith(name + ' '):
            _, n, r = l.split(' ', 2); rot = [[int(x) for x in s.split(',')] for s in r.strip().split(';')]
            return [list(reversed(x)) for x in rot] if mirror else rot
class Hole:
    def __init__(self, name, h, mirror):
        self.rot = load(name, mirror); self.h = h; adj = {v: set(x) for v, x in enumerate(self.rot)}
        self.sp = sp = Space(adj, h, link=self.rot[h]); S = len(sp.states); self.S = S; li = sp.linki
        self.pi = [0] * S; self.lam = [0] * S; self.kind = [None] * S
        for k in range(S): t, l, kd = pi_of(sp, k); self.pi[k] = t; self.lam[k] = l; self.kind[k] = kd
        self.pinv = [0] * S
        for k in range(S): self.pinv[self.pi[k]] = k
        self.cyc = [-1] * S; self.cycles = []; self.W = []
        for k in range(S):
            if self.cyc[k] >= 0: continue
            z = []; x = k
            while self.cyc[x] < 0: self.cyc[x] = len(self.cycles); z.append(x); x = self.pi[x]
            self.cycles.append(z); self.W.append(sum(self.lam[y] for y in z) // 5)
        self.DL = [is_DL(sp, k) for k in range(S)]
        L = self.rot[h]; self.L = L
        # w_t: third vertex of face x_t x_{t+1}
        self.w = []
        for t in range(5):
            a, b = L[t], L[(t + 1) % 5]; ra = self.rot[a]; p = ra.index(b); c1, c2 = ra[(p + 1) % len(ra)], ra[(p - 1) % len(ra)]
            self.w.append(c2 if c1 == h else c1)
    def col(self, k, v): return self.sp.states[k][self.sp.idx[v]]
    def linkc(self, k): return [self.col(k, x) for x in self.L]
    def filled(self, k): return len(set(self.linkc(k))) <= 3
    def frame(self, k):
        c = self.linkc(k); cnt = Counter(c); j = next(j for j in range(5) if c[j] == c[(j + 2) % 5] and cnt[c[j]] == 2)
        al, mu, A, B = c[j], c[(j + 1) % 5], c[(j + 3) % 5], c[(j + 4) % 5]
        w0, w3 = self.col(k, self.w[j]), self.col(k, self.w[(j + 3) % 5])
        ty = 1 if w0 == A else (2 if (w0 == B and w3 == al) else (3 if (w0 == B and w3 == mu) else 0))
        hi = [i for i in range(5) if len(self.rot[self.L[(j + i) % 5]]) >= 6]
        return j, ty, hi, (al, mu, A, B)
    def locks(self, k):
        s = self.sp.states[k]; c = self.linkc(k); cnt = Counter(c)
        if len(cnt) != 4: return None
        j = next(j for j in range(5) if c[j] == c[(j + 2) % 5] and cnt[c[j]] == 2); li = self.sp.linki
        mu, A, B = c[(j + 1) % 5], c[(j + 3) % 5], c[(j + 4) % 5]; m, a, b = li[(j + 1) % 5], li[(j + 3) % 5], li[(j + 4) % 5]
        l1 = any(K >> m & 1 and K >> a & 1 for K in self.sp.components(s, mu, A)); l2 = any(K >> m & 1 and K >> b & 1 for K in self.sp.components(s, mu, B))
        return (l1, l2)
    def sigma(self, k):
        s = self.sp.states[k]; c = self.linkc(k); cnt = Counter(c); j = next(j for j in range(5) if c[j] == c[(j + 2) % 5] and cnt[c[j]] == 2)
        al, mu = c[j], c[(j + 1) % 5]; m = self.sp.linki[(j + 1) % 5]
        K = next(K for K in self.sp.components(s, al, mu) if K >> m & 1); return self.sp.index[self.sp.swap(s, K, al, mu)]
    def isDDend(self, k): return self.DL[k] and (self.DL[self.pi[k]] or self.DL[self.pinv[k]])
    def f_after(self, s):
        y = self.pi[s]; f = 0
        while self.filled(y): f += 1; y = self.pi[y]
        return f
