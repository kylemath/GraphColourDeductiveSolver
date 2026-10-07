"""exact rational least squares (normal equations in Fractions; numpy BLAS on this machine gives spurious matmul warnings)"""
from fractions import Fraction
def solve(M, b):
    n = len(M); A = [[Fraction(x) for x in row] + [Fraction(bb)] for row, bb in zip(M, b)]
    piv = []; r = 0
    for c in range(n):
        p = next((i for i in range(r, n) if A[i][c] != 0), None)
        if p is None: continue
        A[r], A[p] = A[p], A[r]
        A[r] = [x / A[r][c] for x in A[r]]
        for i in range(n):
            if i != r and A[i][c] != 0:
                f = A[i][c]; A[i] = [x - f * y for x, y in zip(A[i], A[r])]
        piv.append(c); r += 1
    x = [Fraction(0)] * n
    for i, c in enumerate(piv): x[c] = A[i][n]
    return x, len(piv)
def lsq(rows, y):
    """rows: list of feature tuples (ints); y: ints. returns (coef Fractions, rank, exact: bool, max |resid| float, n_bad)"""
    k = len(rows[0])
    M = [[sum(Fraction(r[a]) * r[b] for r in rows) for b in range(k)] for a in range(k)]
    v = [sum(Fraction(r[a]) * yy for r, yy in zip(rows, y)) for a in range(k)]
    x, rk = solve(M, v)
    res = [yy - sum(c * f for c, f in zip(x, r)) for r, yy in zip(rows, y)]
    bad = sum(1 for e in res if e != 0)
    return x, rk, bad == 0, float(max(abs(e) for e in res)), bad

def nullspace(rows):
    """exact rational nullspace of the matrix with the given integer rows (list of tuples). returns list of basis vectors (Fractions)"""
    k = len(rows[0]); A = []
    # incremental row reduction keeping a reduced basis of the row space
    basis = []   # list of (pivot, row)
    for r in rows:
        v = [Fraction(x) for x in r]
        for p, b in basis:
            if v[p] != 0:
                f = v[p]; v = [x - f * y for x, y in zip(v, b)]
        p = next((c for c in range(k) if v[c] != 0), None)
        if p is None: continue
        v = [x / v[p] for x in v]
        basis = [(pp, [x - bb[p] * y for x, y in zip(bb, v)] if bb[p] != 0 else bb) for pp, bb in basis]
        basis.append((p, v))
    piv = {p for p, _ in basis}; free = [c for c in range(k) if c not in piv]; out = []
    for f in free:
        x = [Fraction(0)] * k; x[f] = Fraction(1)
        for p, b in basis: x[p] = -b[f]
        out.append(x)
    return out
