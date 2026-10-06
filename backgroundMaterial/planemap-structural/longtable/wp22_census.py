#!/usr/bin/env python3
"""wp22_census.py -- S2b: exhaustive census of doubly locked states of the stacked antiprisms A_3, A_4, A_5 (WP22).

A_r is built here from the description in a-structure.md section 1 (own implementation; nothing imported from the
prototypes): vertices v, ring vertices (i,t) i=0..r-1, t in Z_5, and a cap c; order 5r+2.  Edges: v~(0,t);
(i,t)~(i,t+1); strip: (i+1,t)~(i,t) and (i,t+1); c~(r-1,t).  Labels: v = 0, (i,t) = 1+5i+t, c = 5r+1.
Triangles: (v,(0,t),(0,t+1)); (i,t),(i,t+1),(i+1,t) and (i+1,t),(i+1,t+1),(i,t+1); (c,(r-1,t+1),(r-1,t)).
Orientation made consistent by a traversal; check: order, 3n-6 edges, 2n-4 faces, degrees 5 and 6 only.

Census: for every degree-5 hole h of A_r (12 holes for each r>=3; ALL of them by default, no symmetry used), every
proper 4-colouring of A_r - h with 4 colours on the link, up to colour renaming, is enumerated; each doubly locked
state gets a record  {"graph","v","faces_sha256","state","doubly_locked":true,"radius", ...}.  `state` is the
canonical colouring with entry v = -1 (WP22-interface.md).  Extra fields: "chain" (F-chain length, capped at 40),
"status" (found / closed / capped / depth).  radius is null for a capped state and "inf" for a closed targetless
class (this would be a KILL-2 candidate and is flagged in the summary).
Symmetry (optional, --reduced): the rotation sigma: (i,t)->(i,t+1) is an automorphism fixing v and c and mapping the
oriented triangulation to itself; holes are then taken up to sigma (orbits {v}, {c}, ring 0, ring r-1).  This is
NOT the default; wp22_tests.py checks on A_3 and A_4 that orbit-mates give identical radius multisets.
"""
import json
import sys
import time

import wp22_radius as R

CHAIN_CAP = 40


def build_A(r):
    """oriented faces of A_r (own construction)."""
    def vid(i, t):
        return 1 + 5 * i + (t % 5)
    cap = 5 * r + 1
    tris = []
    for t in range(5):
        tris.append((0, vid(0, t), vid(0, t + 1)))
    for i in range(r - 1):
        for t in range(5):
            tris.append((vid(i, t), vid(i, t + 1), vid(i + 1, t)))
            tris.append((vid(i + 1, t), vid(i + 1, t + 1), vid(i, t + 1)))
    for t in range(5):
        tris.append((cap, vid(r - 1, t + 1), vid(r - 1, t)))
    return orient_faces(tris)


def orient_faces(tris):
    """make a set of triangles of a sphere consistently oriented (each directed edge in exactly one face)."""
    tris = [tuple(f) for f in tris]
    ef = {}
    for i, f in enumerate(tris):
        for k in range(3):
            ef.setdefault(frozenset((f[k], f[(k + 1) % 3])), []).append(i)
    res = {0: tris[0]}
    stack = [0]
    while stack:
        i = stack.pop()
        f = res[i]
        for k in range(3):
            a, b = f[k], f[(k + 1) % 3]
            for j in ef[frozenset((a, b))]:
                if j == i or j in res:
                    continue
                g = tris[j]
                has = any((g[m], g[(m + 1) % 3]) == (a, b) for m in range(3))
                res[j] = (g[0], g[2], g[1]) if has else g
                stack.append(j)
    if len(res) != len(tris):
        raise ValueError("faces not connected")
    return [res[i] for i in range(len(tris))]


def check_A(r):
    """order 5r+2 (17, 22, 27 for r=3,4,5), degrees only 5 and 6, planar triangulation.  Returns the Hole at v=0."""
    faces = build_A(r)
    H = R.Hole(faces, 0)
    assert H.check() is None, H.check()
    assert H.n == 5 * r + 2, H.n
    assert set(H.degree.values()) <= {5, 6}, set(H.degree.values())
    assert len(faces) == 2 * H.n - 4
    return H


def holes_of(r, reduced=False):
    """degree-5 vertices of A_r (labels); reduced: one representative per sigma-orbit."""
    faces = build_A(r)
    H = R.Hole(faces, 0)
    deg5 = sorted(u for u, d in H.degree.items() if d == 5)
    assert len(deg5) == 12, deg5
    if not reduced:
        return [(h, 1) for h in deg5]
    reps = [0, 5 * r + 1, 1, 1 + 5 * (r - 1)]
    return [(h, 1 if h in (0, 5 * r + 1) else 5) for h in reps]


def census_hole(graph, r, hole, deadline=None, cap=R.ENUM_CAP, out=None, max_states=None):
    """census of one hole.  Returns (records, summary).  Records are produced for EVERY doubly locked state."""
    faces = build_A(r)
    sha = R.faces_sha256(faces)
    H = R.Hole(faces, hole)
    states = R.all_states(H)
    if max_states is not None:
        states = states[:max_states]
    records = []
    hist = {}
    chain_hist = {}
    n_dl = 0
    inf_chain = 0
    kill = []
    capped = 0
    for st in states:
        col = list(st)
        if not H.is_dl(col):
            continue
        n_dl += 1
        rr, info = R.radius(H, st, cap=cap, deadline=deadline)
        full = [-1] * H.n
        for i, u in enumerate(H.labels):
            full[u] = st[i]
        ch = H.chain_len(col, CHAIN_CAP)
        chain_hist[ch] = chain_hist.get(ch, 0) + 1
        if ch >= CHAIN_CAP:
            inf_chain += 1
        if rr is None:
            capped += 1
            rad = None
        elif rr == float("inf"):
            rad = "inf"
            kill.append(R.make_cert(H, st, {"radius": None, "class_closed_no_filled": True,
                                            "class_size": info["class_size"]}))
        else:
            rad = rr
        hist[str(rad)] = hist.get(str(rad), 0) + 1
        records.append({"graph": graph, "v": hole, "faces_sha256": sha, "state": full, "doubly_locked": True,
                        "radius": rad, "chain": ch, "status": info["status"]})
    summary = {"graph": graph, "v": hole, "faces_sha256": sha, "order": H.n, "states_four_link": len(states),
               "doubly_locked": n_dl, "radius_hist": dict(sorted(hist.items())),
               "chain_hist": {str(k): v for k, v in sorted(chain_hist.items())},
               "infinite_chain_classes": inf_chain, "capped": capped, "kill2_candidates": kill}
    return records, summary


def dumps_records(records):
    """canonical JSON-lines text (byte-stable)."""
    return "".join(json.dumps(r, sort_keys=True, separators=(",", ":")) + "\n" for r in records)


def groups(reduced=False, orders=(3, 4, 5)):
    """the S2b shard list: (graph name, r, hole, weight), one shard per hole."""
    out = []
    for r in orders:
        for h, w in holes_of(r, reduced):
            out.append(("A_%d" % r, r, h, w))
    return out


if __name__ == "__main__":
    for r in (3, 4, 5):
        H = check_A(r)
        print("A_%d order %d degrees %s" % (r, H.n, sorted(set(H.degree.values()))))
        t = time.process_time()
        rec, s = census_hole("A_%d" % r, r, 0)
        print({k: v for k, v in s.items() if k != "kill2_candidates"}, "cpu %.1f" % (time.process_time() - t))
