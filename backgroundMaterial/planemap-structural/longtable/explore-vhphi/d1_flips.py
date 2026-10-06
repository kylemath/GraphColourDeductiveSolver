"""EXPLORATORY (D1-test, 2026-10-05). One-edge-flip neighbours of the -m5 order-17 graphs that stay
minimum degree 5 and 4-connected (no separating triangle); results are matched against the
plantri -m5 17 list by a canonical rotation-system code (both orientations).  Then SEP on the
distinct results.  Usage: python3 d1_flips.py PLANTRI OUT.json [seed indices, default all]"""
import json, subprocess, sys
import tilley_apex as TA, sep_any as SA
from multiprocessing import Pool

def canon_code(rot):
    best = None
    for flip in (False, True):
        R = [list(reversed(r)) if flip else list(r) for r in rot]
        for u in range(len(R)):
            for k in range(len(R[u])):
                lab = {u: 0}; order = [u]; code = []; start = {u: k}
                i = 0
                while i < len(order):
                    a = order[i]; i += 1
                    r = R[a]; s = start[a]
                    for t in range(len(r)):
                        w = r[(s + t) % len(r)]
                        if w not in lab:
                            lab[w] = len(order); order.append(w)
                            start[w] = R[w].index(a)
                        code.append(lab[w])
                    code.append(-1)
                code = tuple(code)
                if best is None or code < best: best = code
    return best

def flip(rot, u, v):
    """Flip edge uv: remove uv, add wz where uvw, vuz are the faces. Return new rotation or None."""
    ru, rv = rot[u], rot[v]
    iu = ru.index(v); z = ru[(iu - 1) % len(ru)]; w = ru[(iu + 1) % len(ru)]
    # faces on uv in rotation system: (u, v, w) with w next after v around u; z previous
    if z == w or w in rot[z]: return None
    new = [list(r) for r in rot]
    iv = rv.index(u)
    # verify w,z adjacent to v too
    assert rv[(iv - 1) % len(rv)] == w and rv[(iv + 1) % len(rv)] == z, "orientation"
    new[u].remove(v); new[v].remove(u)
    iw = new[w].index(u); jw = new[w].index(v)
    # in w's rotation, u and v are consecutive; insert z between them
    if (iw + 1) % len(rot[w]) == jw: new[w].insert(jw, z)
    else: new[w].insert(iw, z)
    iz = new[z].index(u); jz = new[z].index(v)
    if (iz + 1) % len(rot[z]) == jz: new[z].insert(jz, w)
    else: new[z].insert(iz, w)
    return new

def check_tri(rot):
    n = len(rot); adj = [set(r) for r in rot]
    assert sum(len(r) for r in rot) == 6 * (n - 2)
    for u in range(n):
        r = rot[u]
        for i in range(len(r)):
            assert r[(i + 1) % len(r)] in adj[r[i]]
    faces = {frozenset((u, r[i], r[(i + 1) % len(r)])) for u in range(n) for r in [rot[u]] for i in range(len(r))}
    assert len(faces) == 2 * (n - 2)
    sep = []
    for u in range(n):
        for v in adj[u]:
            if v > u:
                for w in adj[u] & adj[v]:
                    if w > v and frozenset((u, v, w)) not in faces: sep.append((u, v, w))
    return not sep

def main():
    plantri, out = sys.argv[1], sys.argv[2]
    lines = subprocess.run([plantri, "-m5", "17", "-a"], capture_output=True, text=True).stdout.splitlines()
    rots = [TA.parse(l) for l in lines]
    codes = {canon_code(r): i for i, r in enumerate(rots)}
    assert len(codes) == len(rots)
    seeds = [int(a) for a in sys.argv[3:]] or range(len(rots))
    results = []; distinct = {}
    for s in seeds:
        rot = rots[s]
        for u in range(17):
            for v in rot[u]:
                if v < u or len(rot[u]) < 6 or len(rot[v]) < 6: continue
                new = flip(rot, u, v)
                if new is None: continue
                assert check_tri(new) or True
                ok4 = check_tri(new)
                md = min(len(r) for r in new)
                if md < 5 or not ok4: results.append({"seed": s, "edge": [u, v], "min5": md >= 5, "c4": ok4}); continue
                c = canon_code(new)
                m = codes.get(c)
                assert m is not None, "flip result not in plantri -m5 17 list"
                results.append({"seed": s, "edge": [u, v], "min5": True, "c4": True, "matches_plantri_index": m})
                distinct[m] = 1
    print("plantri -m5 17 graphs:", len(rots), "degree-5 counts:", [sum(len(r) == 5 for r in R) for R in rots])
    print("flips tried from seeds", list(seeds), ":", len(results), "valid min5+c4:", sum(1 for r in results if "matches_plantri_index" in r),
          "distinct targets", sorted(distinct))
    # SEP on every graph of the list (also covers all flip targets)
    with Pool(13) as pool:
        recs = [r for part in pool.imap(SA.examine, list(enumerate(lines))) for r in part]
    summary = {}
    for g in range(len(rots)):
        rs = [r for r in recs if r["idx"] == g]
        summary[g] = {"deg5": len(rs), "states": sum(r["states"] for r in rs), "bad": sum(r["bad_states"] for r in rs)}
    print("SEP per -m5 17 graph (index: deg5, states, bad):", summary)
    json.dump({"flips": results, "targets": sorted(distinct), "sep": summary, "plantri_lines": lines}, open(out, "w"))
if __name__ == "__main__":
    main()
