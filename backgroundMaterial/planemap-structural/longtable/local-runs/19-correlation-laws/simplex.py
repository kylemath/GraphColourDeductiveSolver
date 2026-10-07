"""[exploratory] Tiny exact LP: maximise c.x  s.t.  A x <= b (b >= 0), x >= 0, Bland's rule, Fractions."""
from fractions import Fraction as Fr
def maximise(c, A, b):
    m, n = len(A), len(c)
    T = [[Fr(x) for x in A[i]] + [Fr(1 if j == i else 0) for j in range(m)] + [Fr(b[i])] for i in range(m)]
    z = [Fr(-x) for x in c] + [Fr(0)] * (m + 1)
    basis = [n + i for i in range(m)]
    while True:
        e = next((j for j in range(n + m) if z[j] < 0), None)
        if e is None: break
        rows = [(T[i][-1] / T[i][e], basis[i], i) for i in range(m) if T[i][e] > 0]
        if not rows: return None, None  # unbounded
        _, _, r = min(rows)
        pv = T[r][e]; T[r] = [x / pv for x in T[r]]
        for i in range(m):
            if i != r and T[i][e] != 0:
                f = T[i][e]; T[i] = [x - f * y for x, y in zip(T[i], T[r])]
        f = z[e]; z = [x - f * y for x, y in zip(z, T[r])]; basis[r] = e
    x = [Fr(0)] * (n + m)
    for i, bi in enumerate(basis): x[bi] = T[i][-1]
    return z[-1], x[:n]
