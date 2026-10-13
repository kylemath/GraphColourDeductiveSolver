"""Vertex substitution along a 5-cycle: T = (A - u) glued to (B - u') along the links of u and u' (both degree 5).

The link of u in A is identified with the link of u' in B, in reverse cyclic order (so the result is orientable),
rotated by `shift` (0..4). If both links are chordless on their own side, the link becomes a nontrivial separating
5-cycle of T (each side has >= 2 vertices when A and B have >= 7 vertices). Faces of T are the faces of A not at u and
the faces of B not at u' (relabelled, orientation reversed); the rotation system is rebuilt from the faces.

    from glue import glue
    rot, mapA, mapB = glue(rotA, u, rotB, u2, shift)

Exploratory tooling for the gluing-lock experiment (GLUING.md). Uses 4square's mapio for faces -> rotation system.
"""
import os, sys
sys.path.insert(0, os.path.expanduser('~/4square'))
from mapio import rot_from_faces, check_rot  # noqa: E402


def faces_of(rot):
    out = set()
    for u in range(len(rot)):
        d = len(rot[u])
        for i in range(d):
            f = (u, rot[u][i], rot[u][(i + 1) % d])
            k = f.index(min(f)); out.add(f[k:] + f[:k])
    return sorted(out)


def glue(rotA, u, rotB, u2, shift=0):
    CA, CB = list(rotA[u]), list(rotB[u2])
    assert len(CA) == 5 and len(CB) == 5
    nA, nB = len(rotA), len(rotB)
    mapA, k = {}, 0
    for x in range(nA):
        if x != u: mapA[x] = k; k += 1
    # B's link vertex CB[i] is glued to A's CA[(shift - i) % 5]: reversed order
    mapB = {}
    for i, y in enumerate(CB): mapB[y] = mapA[CA[(shift - i) % 5]]
    for y in range(nB):
        if y != u2 and y not in mapB: mapB[y] = k; k += 1
    F = [tuple(mapA[x] for x in f) for f in faces_of(rotA) if u not in f]
    F += [tuple(mapB[x] for x in reversed(f)) for f in faces_of(rotB) if u2 not in f]
    rot = rot_from_faces(F)
    assert check_rot(rot), 'glued map is not a sphere'
    return rot, mapA, mapB


def line(name, rot):
    return '%s %d %s' % (name, len(rot), ';'.join(','.join(map(str, r)) for r in rot))
