"""[exploratory] NightPotential engine: pi / frame / locks / sigma on colourings given as dicts {vertex: colour},
for a rotation system with a hole h (vertex h deleted).  Mirrors eng.py (30-nighta34) and uv_lib.py but needs no Space."""
from collections import Counter
NM = {(3,4):0,(1,1):1,(3,3):2,(1,0):3,(3,2):4,(1,4):5,(3,1):6,(1,3):7,(3,0):8,(1,2):9}
class Hole:
    def __init__(s, rot, h):
        s.rot = rot; s.h = h; L = rot[h]; s.L = L
        s.V = [v for v in range(len(rot)) if v != h]
        s.nb = {v: [u for u in rot[v] if u != h] for v in s.V}
        s.w = []
        for t in range(5):
            a, b = L[t], L[(t+1) % 5]; ra = rot[a]; p = ra.index(b); c1, c2 = ra[(p+1) % len(ra)], ra[(p-1) % len(ra)]
            s.w.append(c2 if c1 == h else c1)
        hi = [t for t in range(5) if len(rot[L[t]]) >= 6]
        s.q = hi[0] if len(hi) == 1 else None
        if s.q is not None:
            q = s.q; s.p = L[q]; s.y = s.w[(q+4) % 5]; s.z = s.w[q]
            s.M = [u for u in rot[s.p] if u not in (h, L[(q+1) % 5], L[(q+4) % 5], s.y, s.z)]; s.m = s.M[0]
        s.E = [(u, v) for u in s.V for v in s.nb[u] if u < v]
    def comp(s, c, v, a, b, avoid=()):
        if c[v] not in (a, b) or v in avoid: return set()
        S = {v}; st = [v]
        while st:
            u = st.pop()
            for t in s.nb[u]:
                if t not in S and t not in avoid and c[t] in (a, b): S.add(t); st.append(t)
        return S
    def ncomp(s, c, a, b):
        seen = set(); n = 0
        for v in s.V:
            if c[v] in (a, b) and v not in seen: seen |= s.comp(c, v, a, b); n += 1
        return n
    def rank(s, c, a, b):
        Vab = sum(1 for v in s.V if c[v] in (a, b)); Eab = sum(1 for u, v in s.E if c[u] in (a, b) and c[v] in (a, b))
        return Eab - Vab + s.ncomp(c, a, b)
    def swap(s, c, K, a, b):
        d = dict(c)
        for v in K: d[v] = b if c[v] == a else a
        return d
    def lc(s, c): return [c[x] for x in s.L]
    def filled(s, c): return len(set(s.lc(c))) <= 3
    def frame(s, c):
        lc = s.lc(c); cnt = Counter(lc)
        if len(cnt) != 4: return None
        j = next(j for j in range(5) if lc[j] == lc[(j+2) % 5] and cnt[lc[j]] == 2)
        al, mu, A, B = lc[j], lc[(j+1) % 5], lc[(j+3) % 5], lc[(j+4) % 5]
        w0, w3 = c[s.w[j]], c[s.w[(j+3) % 5]]
        ty = 1 if w0 == A else (2 if (w0 == B and w3 == al) else (3 if (w0 == B and w3 == mu) else 0))
        k = (s.q - j) % 5 if s.q is not None else None
        return j, ty, k, (al, mu, A, B)
    def locks(s, c):
        f = s.frame(c)
        if f is None: return None
        j, ty, k, (al, mu, A, B) = f; X = s.L
        K1 = s.comp(c, X[(j+1) % 5], mu, A); K2 = s.comp(c, X[(j+1) % 5], mu, B)
        return X[(j+3) % 5] in K1, X[(j+4) % 5] in K2, K1, K2
    def DL(s, c):
        l = s.locks(c); return bool(l and l[0] and l[1])
    def pi(s, c):
        X = s.L; lc = s.lc(c); cnt = Counter(lc)
        if len(cnt) == 4:
            j, ty, k, (al, mu, A, B) = s.frame(c)
            if X[(j+4) % 5] in s.comp(c, X[(j+1) % 5], mu, B):
                K = s.comp(c, X[(j+2) % 5], al, A); return s.swap(c, K, al, A), 'R3', K, (al, A)
            K = s.comp(c, X[(j+4) % 5], mu, B); return s.swap(c, K, mu, B), 'phiB', K, (mu, B)
        i = next(i for i in range(5) if cnt[lc[i]] == 1)
        Wc, Xc, Yc = lc[i], lc[(i+1) % 5], lc[(i+2) % 5]; Zc = ({0,1,2,3} - {Wc, Xc, Yc}).pop()
        K = s.comp(c, X[(i+2) % 5], Yc, Zc)
        if X[(i+4) % 5] not in K: return s.swap(c, K, Yc, Zc), 'phiA', K, (Yc, Zc)
        K = s.comp(c, X[(i+3) % 5], Wc, Xc); return s.swap(c, K, Wc, Xc), 'tau', K, (Wc, Xc)
    def Ksig(s, c):
        j, ty, k, (al, mu, A, B) = s.frame(c); return s.comp(c, s.L[(j+1) % 5], al, mu)
    def sigma(s, c):
        j, ty, k, (al, mu, A, B) = s.frame(c); return s.swap(c, s.Ksig(c), al, mu)
    def J(s, c): return s.z in s.comp(c, s.y, c[s.y], c[s.z])
    def pos(s, c):
        f = s.frame(c); return None if f is None else NM.get((f[1], f[2]))
    def lockless_exit(s, c):
        t = s.sigma(c)
        if s.filled(t): return False
        l = s.locks(t); return not l[0] and not l[1]
def key(c): return tuple(sorted(c.items()))
def canon(c):
    mp = {}; return tuple(mp.setdefault(c[v], len(mp)) for v in sorted(c))
