"""WP14 shared helpers: load discovery tables (read-only) and analyse Kempe structure at a degree-5 root.

Independent of the WP11 producer except for mass_core.RootState (state enumeration and move lists),
whose move semantics (whole bichromatic components of T - r, interior components included,
canonical colourings modulo colour renaming) are the Gate-D macro semantics.
"""
import glob
import gzip
import itertools
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LT = HERE.parent
sys.path.insert(0, str(LT))
from mass_core import RootState  # noqa: E402

PAIRS = list(itertools.combinations(range(4), 2))


def tables():
    for f in sorted(glob.glob(str(LT / "wp11-discovery" / "tables" / "*.json.gz"))):
        yield os.path.basename(f)[:-8], json.load(gzip.open(f))


def comp_of(adj, col, v, a, b):
    """Vertex set of the {a,b}-component of v (v must have colour a or b)."""
    if col[v] not in (a, b):
        return frozenset()
    seen, st = {v}, [v]
    while st:
        x = st.pop()
        for y in adj[x]:
            if y not in seen and col[y] in (a, b):
                seen.add(y)
                st.append(y)
    return frozenset(seen)


def pattern(Bc):
    """Bc = colours on the cyclic boundary b0..b4 (p = 1 required).

    Returns (i, rho) where b_{i-1}, b_{i+1} carry the repeated colour rho and b_i is the APEX.
    The far singletons are b_{i+2}, b_{i+3}.
    """
    for i in range(5):
        if Bc[(i - 1) % 5] == Bc[(i + 1) % 5]:
            return i, Bc[(i + 1) % 5]
    raise ValueError("no repeated colour at distance two")


def lock(adj, col, B):
    """Kempe lock: apex joined to BOTH far singletons by the corresponding bichromatic chains."""
    Bc = [col[v] for v in B]
    i, _ = pattern(Bc)
    apex, f1, f2 = B[i], B[(i + 2) % 5], B[(i + 3) % 5]
    k1 = comp_of(adj, col, apex, col[apex], col[f1])
    k2 = comp_of(adj, col, apex, col[apex], col[f2])
    return (f1 in k1) and (f2 in k2)


def ncol(col, B):
    return len({col[v] for v in B})


def all_components(adj, col, verts):
    out = []
    for a, b in PAIRS:
        pend = {v for v in verts if col[v] in (a, b)}
        while pend:
            s = min(pend)
            K = comp_of(adj, col, s, a, b)
            pend -= K
            out.append(((a, b), K))
    return out


def swap(col, pr, K):
    a, b = pr
    out = dict(col)
    for v in K:
        out[v] = b if col[v] == a else a
    return out


def setup(d):
    rot = d["graph"]["rotation"]
    r = d["root"]
    B = list(d["boundary_cyclic_order"])
    assert B == list(rot[r])
    V = d["vertex_order"]
    adj = {v: [w for w in rot[v] if w != r] for v in V}
    return rot, r, B, V, adj
