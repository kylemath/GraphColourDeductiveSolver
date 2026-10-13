#!/usr/bin/env python3
"""D-reducibility check (Birkhoff/Heesch/RSST style) for a configuration given by its ring
size and interior adjacency.  Independent of StudioMathReview-scripts/gen_cert.py.

Model (vertex-colour form of RSST's edge-colour 'consistent signed matchings'):
  colours = Z2 x Z2 = {0,1,2,3} with XOR; a Kempe pairing theta in {1,2,3} splits the colours
  into classes {x, x^theta}.  Around the ring, a 'transition' is a ring edge whose ends lie in
  different classes.  Outside the ring (a near-triangulated disc) the Kempe components in the two
  classes are the regions cut out by a non-crossing perfect matching of the transitions
  (RSST's matching).  A colouring k is good at level i+1 if for some theta, for EVERY non-crossing
  perfect matching of its transitions, SOME set of regions can be XOR-ed with theta (each region
  is one Kempe component, so this is a legal set of Kempe interchanges) to give a level-i good
  colouring.  Level 0 = colourings that extend to the interior.  D-reducible iff the closure is
  all proper ring colourings.  Colourings are handled up to renaming (canonical form).

Usage: python3 dred.py            (Birkhoff diamond)
"""
import itertools, sys, time


def canon(k):
    m = {}
    for x in k:
        m.setdefault(x, len(m))
    return tuple(m[x] for x in k)


def ring_colourings(r):
    out = set()
    for k in itertools.product(range(4), repeat=r):
        if all(k[i] != k[(i + 1) % r] for i in range(r)):
            out.add(canon(k))
    return sorted(out)


def extends(k, ringadj, intadj, m):
    for c in itertools.product(range(4), repeat=m):
        ok = True
        for a in range(m):
            if any(c[a] == k[t] for t in ringadj[a]) or any(c[a] == c[b] for b in intadj[a] if b > a):
                ok = False
                break
        if ok:
            return c
    return None


def nc_matchings(pts):
    """Non-crossing perfect matchings of points listed in cyclic order."""
    if not pts:
        yield []
        return
    a = pts[0]
    for j in range(1, len(pts), 2):
        inner, outer = pts[1:j], pts[j + 1:]
        for m1 in nc_matchings(inner):
            for m2 in nc_matchings(outer):
                yield [(a, pts[j])] + m1 + m2


def regions(r, trans, matching):
    """Ring vertices grouped into regions.  Transition t sits on ring edge (t, t+1).  A chord
    (s,t) separates; the ring vertices are 'arcs' between consecutive transitions.  Two arcs lie in
    one region iff no chord separates them.  Implemented by union-find on arcs: arc after
    transition s and arc after the matched partner region-connect via chord sides."""
    if not trans:
        return [list(range(r))]
    T = sorted(trans)
    # arcs: arc j = ring vertices T[j]+1 .. T[j+1] (cyclic)
    n = len(T)
    arcs = []
    for j in range(n):
        s, e = T[j], T[(j + 1) % n]
        v, a = (s + 1) % r, []
        while True:
            a.append(v)
            if v == e:
                break
            v = (v + 1) % r
        arcs.append(a)
    idx = {t: j for j, t in enumerate(T)}
    par = list(range(n))

    def f(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x
    # chord between transitions T[i] and T[j] (i<j): arc i-1 (before T[i]) and arc j (after T[j])
    # are on the same side of the chord, as are arc i and arc j-1.  Non-crossing => regions.
    for (s, t) in matching:
        i, j = sorted((idx[s], idx[t]))
        for x, y in (((i - 1) % n, j), (i, (j - 1) % n)):
            par[f(x)] = f(y)
    groups = {}
    for j in range(n):
        groups.setdefault(f(j), []).extend(arcs[j])
    return list(groups.values())


def closure(r, ringadj, intadj, m, verbose=True):
    allk = ring_colourings(r)
    good = {k for k in allk if extends(k, ringadj, intadj, m) is not None}
    levels = [set(good)]
    if verbose:
        print(f"ring {r}: {len(allk)} colouring classes, {len(good)} extend")
    it = 0
    while True:
        it += 1
        new = set()
        for k in allk:
            if k in good:
                continue
            for th in (1, 2, 3):
                trans = [i for i in range(r) if (k[i] ^ k[(i + 1) % r]) not in (0, th)]
                ok_all = True
                for M in nc_matchings(trans):
                    regs = regions(r, trans, M)
                    found = False
                    for mask in range(1, 1 << len(regs)):
                        k2 = list(k)
                        for b, reg in enumerate(regs):
                            if mask >> b & 1:
                                for v in reg:
                                    k2[v] ^= th
                        if canon(k2) in good:
                            found = True
                            break
                    if not found:
                        ok_all = False
                        break
                if ok_all:
                    new.add(k)
                    break
        if not new:
            break
        good |= new
        levels.append(new)
        if verbose:
            print(f"  level {it}: +{len(new)} (total {len(good)})")
    return allk, good, levels


# Birkhoff diamond, ring positions 0..5 (same layout as StudioMathLean DiamondCert.lean)
DIAMOND = dict(r=6, m=4,
               ringadj=[[0, 1], [1, 2, 3], [3, 4], [0, 4, 5]],
               intadj=[[1, 2, 3], [0, 2], [0, 1, 3], [0, 2]])

if __name__ == "__main__":
    t = time.time()
    d = DIAMOND
    allk, good, levels = closure(d["r"], d["ringadj"], d["intadj"], d["m"])
    print("D-reducible:", good == set(allk), f"({time.time()-t:.2f}s)")
    print("extendable classes:", sorted(levels[0]))
    bad = [k for k in allk if k not in good]
    if bad:
        print("not reached:", bad)
