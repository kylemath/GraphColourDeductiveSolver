# Bounded-cut level measure tau_J on a lifted boundary walk (heights in the triangular lattice Lambda = Z[w]).
#   even: min over <= J cut edges with jumps s_k in 2*Lambda, |s_k| = 2, sum s_k = t, of the circumradius of the closed
#         curve {H_i - S(i)} (S(i) = sum of the jumps before i).  variant 'nc' (default): no cancelling pair s_k = -s_l;
#         variant 'any': cancelling pairs allowed (each counts against J).
#   odd : exactly one reflection cut (free centre, as tau_step_odd) plus <= J-1 translation cuts as above.
# Exact threshold test: every transformed point lies in Lambda, so "radius <= T" <=> some closed disc D(z,T) holds all of
# them, and z can be taken from a finite candidate set (lattice points and pairwise circle intersections); for each
# maximal lattice set A = Lambda cap D(z,T) containing 0 a DP over the walk with state (A, offset, used-jump mask) and
# value = min number of cuts decides feasibility.  J = 1 reproduces tau_step / tau_step_odd (checked in sanity.py).
import math, itertools, functools
import numpy as np
S3 = math.sqrt(3)
W3 = complex(-0.5, S3/2)
def cz(p): return p[0] + p[1]*W3
STEP = {1: (1, 0), 2: (0, 1), 3: (-1, -1)}           # labels 1,2,3 -> 1, w, w^2
U = [(2, 0), (0, 2), (-2, -2), (-2, 0), (0, -2), (2, 2)]  # 2*units; d and d+3 are opposite
UI = {u: d for d, u in enumerate(U)}

@functools.lru_cache(None)
def asets(T=1.0):
    """maximal lattice subsets of a closed disc of radius T that contain 0 (as frozensets of int pairs)."""
    eps = 1e-9; R = int(math.ceil(2*T + 2))
    pts = [(a, b) for a in range(-2*R, 2*R+1) for b in range(-2*R, 2*R+1) if abs(cz((a, b))) <= 2*T + 1e-9]
    cands = [cz(p) for p in pts if abs(cz(p)) <= T + eps]
    for p, q in itertools.combinations(pts, 2):
        zp, zq = cz(p), cz(q); d = abs(zp - zq)
        if d > 2*T + eps or d < eps: continue
        m = (zp + zq)/2; h = math.sqrt(max(0.0, T*T - d*d/4)); n = 1j*(zq - zp)/d
        for z in (m + h*n, m - h*n):
            if abs(z) <= T + eps: cands.append(z)
    sets = set()
    for z in cands:
        A = frozenset(p for p in pts if abs(cz(p) - z) <= T + 1e-7)
        if (0, 0) in A: sets.add(A)
    sets = sorted(sets, key=len, reverse=True); out = []
    for A in sets:
        if not any(A < B for B in out): out.append(A)
    return tuple(out)

def int_walk(labels, signs):
    """labels[i] in {1,2,3} (c_i xor c_{i+1}), signs +-1 -> list of L+1 int points."""
    H = [(0, 0)]
    for l, s in zip(labels, signs):
        d = STEP[int(l)]; H.append((H[-1][0] + s*d[0], H[-1][1] + s*d[1]))
    return H

class Frontier:
    """DP over the walk. state key (Aidx, phase, x, y, mask) -> min cuts. phase 0: point = H - (x,y);
    phase 1 (after the reflection cut, odd only): point = (x,y) - H. mask: bitmask of used jump displacement directions
    (only tracked for variant 'nc')."""
    def __init__(self, J, odd, variant='nc', T=1.0):
        self.J = J; self.odd = odd; self.nc = (variant == 'nc'); self.A = asets(T)
    def start(self):
        return {(k, 0, 0, 0, 0): 0 for k in range(len(self.A))}
    def _jump_ok(self, mask, d):
        return not (self.nc and (mask >> ((d + 3) % 6)) & 1)
    def adv(self, F, p, allow=True):
        """advance frontier F across one edge to the next point p (int pair); allow = a cut may sit on this edge."""
        A = self.A; J = self.J; G = {}
        def put(k, v):
            if G.get(k, 99) > v: G[k] = v
        for (a, ph, x, y, m), c in F.items():
            S = A[a]
            q = (p[0]-x, p[1]-y) if ph == 0 else (x-p[0], y-p[1])
            if q in S: put((a, ph, x, y, m), c)
            if not allow or c >= J: continue
            for d, u in enumerate(U):
                # displacement of subsequent points by -u (phase 0: offset += u; phase 1: centre-sum -= u)
                if not self._jump_ok(m, d): continue
                q2 = (q[0]-u[0], q[1]-u[1])
                if q2 in S:
                    m2 = m | (1 << d) if self.nc else 0
                    if ph == 0: put((a, 0, x+u[0], y+u[1], m2), c+1)
                    else: put((a, 1, x-u[0], y-u[1], m2), c+1)
            if self.odd and ph == 0:
                for r in S: put((a, 1, r[0]+p[0], r[1]+p[1], m), c+1)
        return G
    def close(self, F, HL, allow=True):
        """min cuts over accepting end states (closing edge L-1 -> 0 may carry a cut if allow). None if infeasible."""
        best = None; J = self.J
        for (a, ph, x, y, m), c in F.items():
            if not self.odd:
                if ph != 0: continue
                dx, dy = x - HL[0], y - HL[1]            # final offset must be t = HL
                if (dx, dy) == (0, 0): cc = c
                elif allow and (-dx, -dy) in UI and self._jump_ok(m, UI[(-dx, -dy)]): cc = c + 1
                else: continue
            else:
                if ph == 0:
                    if not allow: continue
                    cc = c + 1                            # reflection cut on the closing edge
                else:
                    dx, dy = x - HL[0], y - HL[1]         # centre-sum must be H_L (= 2q)
                    if (dx, dy) == (0, 0): cc = c
                    elif allow and (dx, dy) in UI and self._jump_ok(m, UI[(dx, dy)]): cc = c + 1
                    else: continue
            if cc <= J and (best is None or cc < best): best = cc
        return best

def ncuts(H, odd, J, variant='nc', T=1.0, allowed=None):
    """min number of cuts with radius <= T (None if > J needed). H: int points, len L+1. allowed[i]: edge i may be cut."""
    L = len(H) - 1; Fr = Frontier(J, odd, variant, T); F = Fr.start()
    for i in range(1, L):
        F = Fr.adv(F, H[i], True if allowed is None else allowed[i-1])
        if not F: return None
    return Fr.close(F, H[L], True if allowed is None else allowed[L-1])

def tau_value(H, odd, J, variant='nc', lo=0.0, hi=3.0, tol=1e-4):
    """circumradius value tau_J by bisection on T (exact test at each T)."""
    if ncuts(H, odd, J, variant, hi) is None: return float('inf')
    while hi - lo > tol:
        mid = (lo + hi)/2
        if ncuts(H, odd, J, variant, round(mid, 6)) is None: lo = mid
        else: hi = mid
    return hi

def cut_positions(H, odd, J, variant='nc', T=1.0, allowed=None):
    """one optimal configuration: list of cut edge indices (edge i joins point i and i+1 mod L). Brute DP with parents."""
    L = len(H) - 1; Fr = Frontier(J, odd, variant, T); F = Fr.start(); hist = [F]
    for i in range(1, L):
        F = Fr.adv(F, H[i], True if allowed is None else allowed[i-1]); hist.append(F)
        if not F: return None
    best = Fr.close(F, H[L], True if allowed is None else allowed[L-1])
    if best is None: return None
    # backtrack: find an end state realising best, then walk back choosing predecessors with consistent counts
    cuts = []
    def ends():
        for k, c in hist[-1].items():
            sub = Frontier(J, odd, variant, T).close({k: c}, H[L], True if allowed is None else allowed[L-1])
            if sub == best: return k, c, sub - c
    k, c, cl = ends()
    if cl: cuts.append(L-1)
    for i in range(L-1, 0, -1):
        prev = hist[i-1]
        found = None
        for kp, cp in prev.items():
            G = Fr.adv({kp: cp}, H[i], True if allowed is None else allowed[i-1])
            if G.get(k) == c:
                found = (kp, cp); break
        assert found is not None
        if found[1] != c: cuts.append(i-1)
        k, c = found
    return sorted(cuts)
