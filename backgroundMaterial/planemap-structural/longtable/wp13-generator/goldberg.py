"""Goldberg-Coxeter (geodesic) icosahedral triangulations GC(a,b), n = 10(a^2+ab+b^2)+2.

Construction (geometric, then purely combinatorial verification):
  lattice points of the Eisenstein lattice inside the big triangle (0, A, A*omega), A = a + b*omega,
  are mapped barycentrically onto every face of the regular icosahedron and projected to the unit
  sphere; duplicates on shared edges/corners are merged; the triangulation is the convex hull,
  found by brute force (a triple is a face iff every other point lies strictly on one side of its
  plane).  The result is then checked combinatorially: simple triangulation, n = 10T+2, exactly 12
  degree-5 vertices and all others degree 6, pairwise graph distance between degree-5 vertices
  >= a+b (the lattice distance between adjacent pentagon centres).  numpy is used only for the hull.
"""
import itertools
import math

import numpy as np

from trimap import check_triangulation, orient_fix

PHI = (1 + 5 ** 0.5) / 2


def icosahedron():
    V = []
    for s1 in (1, -1):
        for s2 in (1, -1):
            V += [(0, s1, s2 * PHI), (s1, s2 * PHI, 0), (s2 * PHI, 0, s1)]
    V = np.array(V, float)
    F = [t for t in itertools.combinations(range(12), 3)
         if all(abs(np.linalg.norm(V[i] - V[j]) - 2) < 1e-9 for i, j in itertools.combinations(t, 2))]
    assert len(F) == 20
    # orient every face counter-clockwise seen from outside (needed for chiral classes, b != 0)
    F = [(i, j, k) if np.dot(np.cross(V[j] - V[i], V[k] - V[i]), V[i] + V[j] + V[k]) > 0 else (i, k, j)
         for i, j, k in F]
    return V, F


def gc_points(a, b):
    V, F = icosahedron()
    s3 = math.sqrt(3)

    def xy(x, y):  # Eisenstein (x + y*omega) -> plane
        return np.array([x + y / 2, y * s3 / 2])

    P0, P1, P2 = xy(0, 0), xy(a, b), xy(-b, a + b)
    M = np.array([[P1[0] - P0[0], P2[0] - P0[0]], [P1[1] - P0[1], P2[1] - P0[1]]])
    Minv = np.linalg.inv(M)
    R = a + b + 1
    pts = []
    for x in range(-R, R + 1):
        for y in range(-R, 2 * R + 1):
            l1, l2 = Minv @ (xy(x, y) - P0)
            l0 = 1 - l1 - l2
            if min(l0, l1, l2) >= -1e-9:
                pts.append((l0, l1, l2))
    out = []
    for f in F:
        A, B, C = V[list(f)]
        for l0, l1, l2 in pts:
            p = l0 * A + l1 * B + l2 * C
            out.append(p / np.linalg.norm(p))
    out = np.array(out)
    uniq = []
    for p in out:
        if not any(np.linalg.norm(p - q) < 1e-7 for q in uniq):
            uniq.append(p)
    return np.array(uniq)


def hull_rotation(P):
    n = len(P)
    D = np.linalg.norm(P[:, None, :] - P[None, :, :], axis=2)
    dmin = np.min(D + np.eye(n) * 9)
    faces = []
    for i, j, k in itertools.combinations(range(n), 3):
        if D[i, j] > 2.2 * dmin or D[i, k] > 2.2 * dmin or D[j, k] > 2.2 * dmin:
            continue
        nrm = np.cross(P[j] - P[i], P[k] - P[i])
        s = (P - P[i]) @ nrm
        s[[i, j, k]] = 0
        if np.all(s < 1e-12):
            pass
        elif np.all(s > -1e-12):
            nrm = -nrm
            j, k = k, j
        else:
            continue
        others = np.delete(s, [i, j, k])
        assert np.all(np.abs(others) > 1e-9), "coplanar quadruple: hull face not a triangle"
        faces.append((i, j, k))  # outward normal: (j-i)x(k-i) points outward... orientation fixed below
    assert len(faces) == 2 * n - 4, (len(faces), n)
    nxt = [dict() for _ in range(n)]
    for (i, j, k) in faces:
        for p, q, r in ((i, j, k), (j, k, i), (k, i, j)):
            nxt[p][q] = r
    rot = []
    for v in range(n):
        start = next(iter(nxt[v]))
        cyc, w = [start], nxt[v][start]
        while w != start:
            cyc.append(w)
            w = nxt[v][w]
        assert len(cyc) == len(nxt[v])
        rot.append(cyc)
    return orient_fix(rot)


def bfs_dist(rot, s):
    dist = {s: 0}
    q = [s]
    for x in q:
        for y in rot[x]:
            if y not in dist:
                dist[y] = dist[x] + 1
                q.append(y)
    return dist


def goldberg_coxeter(a, b):
    rot = hull_rotation(gc_points(a, b))
    T = a * a + a * b + b * b
    check_triangulation(rot)
    assert len(rot) == 10 * T + 2
    degs = sorted(len(x) for x in rot)
    assert degs.count(5) == 12 and degs.count(6) == len(rot) - 12
    five = [v for v in range(len(rot)) if len(rot[v]) == 5]
    md = min(bfs_dist(rot, u)[w] for u in five for w in five if u < w)
    assert md == a + b, (md, a, b)
    return rot


if __name__ == "__main__":
    for a, b in [(1, 0), (1, 1), (2, 0), (2, 1), (3, 0), (2, 2), (3, 1)]:
        r = goldberg_coxeter(a, b)
        print(a, b, len(r), "ok")
