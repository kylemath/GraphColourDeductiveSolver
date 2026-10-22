# Base-point-free level measures on a lifted boundary walk H (complex array, H[0..L], H[L] = H[0] + t, unit steps).
#   tau_hodge(H) : circumradius of {H_i - (i/L) t}, i < L                      (uniform arclength detrend)
#   tau_strip(H) : half-width of the narrowest strip parallel to t containing H (t = 0: circumradius)
#   tau_step(H)  : min over cuts j of circumradius of {H_i : i <= j} u {H_i - t : j < i < L}   (step detrend)
#   fp_radius(H) : odd walks, max_i |H_i - (H_0 + H_L)/2|
# All three agree when t = 0 (they reduce to the circumradius of the closed walk).
import sys, math, numpy as np
sys.path.insert(0, '/mnt/project-files/multiscale/canonical/')
from pi import mec, mecc, walk, signs, EV, W3

def tvec(H): return H[-1] - H[0]

def tau_hodge(H):
    L = len(H) - 1; t = tvec(H)
    return float(mec(H[:L] - np.arange(L) / L * t))

def tau_strip(H):
    L = len(H) - 1; t = tvec(H)
    if abs(t) < 1e-9: return float(mec(H[:L]))
    n = 1j * t / abs(t); pr = (H[:L] * np.conj(n)).real
    return float((pr.max() - pr.min()) / 2)

def fp_radius(H):
    q = (H[0] + H[-1]) / 2; return float(np.max(np.abs(H - q)))

def _inc_radii(P, T=None):
    """radii r[k] = mec(P[0..k]) incrementally; stops after the first r > T (if T given) returning the list so far."""
    out = []; c, r = P[0], 0.0
    for k in range(len(P)):
        p = P[k]
        if abs(p - c) > r + 1e-9:
            c, r = mecc(np.array(P[:k+1]))
        out.append(r)
        if T is not None and r > T + 1e-9: break
    return out

def _after(H, odd):
    """the holonomy undone: even -> H_i - t, odd -> 2q - H_i (point reflection through q = (H_0+H_L)/2)."""
    L = len(H) - 1
    if odd: return 2*((H[0] + H[L]) / 2) - H[:L]
    return H[:L] - tvec(H)

def tau_step_full(H, odd=False):
    """exact min over all cuts j (L circumradius computations). returns (tau, j)."""
    L = len(H) - 1; t = tvec(H); P = H[:L]
    if not odd and abs(t) < 1e-9: return float(mec(P)), L - 1
    A = _after(H, odd); best = (1e9, None)
    for j in range(L):
        r = float(mec(np.concatenate([P[:j+1], A[j+1:]])))
        if r < best[0]: best = (r, j)
    return best

def tau_step_le(H, T=1.0, odd=False):
    """fast threshold test. returns (ok, value, j): ok iff tau_step(H) <= T; value = min over the feasible cut
    window of the union radius (None if the window is empty), which equals tau_step(H) whenever ok."""
    L = len(H) - 1; t = tvec(H); P = list(H[:L])
    if not odd and abs(t) < 1e-9:
        r = float(mec(np.array(P))); return r <= T + 1e-9, r, L - 1
    A = _after(H, odd)
    pre = _inc_radii(P, T); jmax = len(pre) - 1 if pre[-1] <= T + 1e-9 else len(pre) - 2
    if jmax < 0: return False, None, None
    suf = _inc_radii(P[::-1], T)                      # suf[k] = radius of P[L-1-k .. L-1]
    nsuf = len(suf) if suf[-1] <= T + 1e-9 else len(suf) - 1   # largest valid suffix length
    jmin = L - 1 - nsuf                                # S_j = P[j+1..L-1] has length L-1-j <= nsuf
    if jmin > jmax: return False, None, None
    best = (1e9, None); Pa = np.array(P)
    for j in range(jmin, jmax + 1):
        r = float(mec(np.concatenate([Pa[:j+1], A[j+1:]])))
        if r < best[0]: best = (r, j)
    return best[0] <= T + 1e-9, best[0], best[1]

def measures(H, odd):
    """dict of all measures for a walk."""
    if odd:
        ts, j = tau_step_full(H, True); return dict(odd=True, t=None, fp=round(fp_radius(H), 4), step=round(ts, 4), cut=j)
    t = abs(tvec(H)); ts, j = tau_step_full(H)
    return dict(odd=False, t=round(float(t), 3), hodge=round(tau_hodge(H), 4), strip=round(tau_strip(H), 4), step=round(ts, 4), cut=j)

def walk_from(B, s, col):
    return walk(B, np.asarray(s), np.array([col[b] for b in B]))

def walk_ic(W, col):
    """walk in half-lattice coords (intrinsic/ic.heights) -> complex unit-step walk."""
    S3 = math.sqrt(3)
    import ic
    Hh = ic.heights(W, col)
    if Hh is None: return None
    return np.array([complex((p[0] - p[1] / 2) / 2, p[1] * S3 / 4) for p in Hh])

def tau_step_cuts(H, odd, cuts):
    """min over the given cut indices j (jump on the edge (b_j, b_{j+1})) of the union radius. (None, None) if no cuts."""
    L = len(H) - 1; P = H[:L]
    if not odd and abs(tvec(H)) < 1e-9:
        r = float(mec(P)); return r, L - 1
    A = _after(H, odd); best = (None, None)
    for j in cuts:
        r = float(mec(np.concatenate([P[:j+1], A[j+1:]])))
        if best[0] is None or r < best[0]: best = (r, j)
    return best
