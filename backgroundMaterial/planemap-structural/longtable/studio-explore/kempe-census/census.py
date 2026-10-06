#!/usr/bin/env python3
"""[exploratory] Kempe-radius census of plantri -m5 -c4 triangulations (min degree 5, no separating triangle).

For each graph: degree-5 vertices grouped into orbits under the full automorphism group (rotations and
reflections of the rotation system); one hole per orbit is run through Studio intel's fast/kempe.cpp
(commit 85529ac, sha256 1a9770da...95d0). Output: one JSON line per (graph, hole orbit) with rho and the
radius histogram; every orbit with rho >= SAVE (or rho null) keeps the graph (plantri ascii) and witness.
usage: plantri -m5 -c4 N -a | census.py N OUT.jsonl [--workers K] [--save 4]
"""
import json
import os
import subprocess
import sys
import tempfile
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
KEMPE = os.path.join(HERE, "kempe")


def parse(line):
    n, body = line.split()
    return [[ord(c) - 97 for c in r] for r in body.split(",")]


def faces_of(rot):
    seen, faces = set(), []
    for v, nb in enumerate(rot):
        d = len(nb)
        for i in range(d):
            # plantri lists neighbours clockwise; (v, w_{i+1}, w_i) is counter-clockwise
            f = (v, nb[(i + 1) % d], nb[i])
            k = min((f, f[1:] + f[:1], f[2:] + f[:2]))
            if k not in seen:
                seen.add(k)
                faces.append(f)
    return faces


def automorphisms(rot):
    """All automorphisms of the embedded triangulation (both orientations), as vertex maps."""
    n = len(rot)
    pos = [{w: i for i, w in enumerate(nb)} for nb in rot]
    u0, v0 = 0, rot[0][0]
    out = []
    for x in range(n):
        if len(rot[x]) != len(rot[u0]):
            continue
        for y in rot[x]:
            for sgn in (1, -1):
                m = [-1] * n
                m[u0] = x
                stack = [(u0, v0, x, y)]
                ok = True
                done = set()
                while stack and ok:
                    a, b, c, dd = stack.pop()
                    if a in done:
                        if m[a] != c:
                            ok = False
                        continue
                    done.add(a)
                    da, dc = len(rot[a]), len(rot[c])
                    if da != dc:
                        ok = False
                        break
                    ia, ic = pos[a][b], pos[c][dd]
                    for k in range(da):
                        w = rot[a][(ia + k) % da]
                        z = rot[c][(ic + sgn * k) % dc]
                        if m[w] == -1:
                            m[w] = z
                        elif m[w] != z:
                            ok = False
                            break
                        if w not in done:
                            stack.append((w, a, z, c))
                if ok and -1 not in m and len(set(m)) == n:
                    out.append(m)
    return out


def orbits5(rot):
    deg5 = [v for v in range(len(rot)) if len(rot[v]) == 5]
    auts = automorphisms(rot)
    rep, seen = [], set()
    for v in deg5:
        if v in seen:
            continue
        orb = sorted({m[v] for m in auts})
        seen.update(orb)
        rep.append((v, len(orb)))
    return rep, len(auts)


def work(item):
    idx, line, save = item
    rot = parse(line)
    faces = faces_of(rot)
    reps, naut = orbits5(rot)
    res = []
    with tempfile.NamedTemporaryFile("w", suffix=".tri", delete=False) as fh:
        fh.write("%d %d\n" % (len(rot), len(faces)))
        for f in faces:
            fh.write("%d %d %d\n" % f)
        path = fh.name
    try:
        for v, size in reps:
            r = subprocess.run([KEMPE, path, str(v)], capture_output=True, text=True)
            o = json.loads(r.stdout.strip().splitlines()[-1])
            rho = o.get("rho")
            rec = {"index": idx, "hole": v, "orbit_size": size, "n_aut": naut, "rho": rho,
                   "n_states": o.get("n_states"), "n_DL": o.get("n_DL"), "hist": o.get("DL_radius_hist"),
                   "unreached_DL": o.get("unreached_DL")}
            if "error" in o or "inconclusive" in o:
                rec["engine"] = o
            if rho is None or (isinstance(rho, int) and rho >= save):
                rec["graph"] = line
                rec["witness"] = o.get("witness")
            res.append(rec)
    finally:
        os.unlink(path)
    return res


def main():
    n, out = int(sys.argv[1]), sys.argv[2]
    workers = int(sys.argv[sys.argv.index("--workers") + 1]) if "--workers" in sys.argv else 8
    save = int(sys.argv[sys.argv.index("--save") + 1]) if "--save" in sys.argv else 4
    lines = [l for l in sys.stdin.read().splitlines() if l.strip()]
    hist, maxrho, nrec = {}, 0, 0
    with open(out, "w") as fo, Pool(workers) as pool:
        for recs in pool.imap(work, ((i, l, save) for i, l in enumerate(lines)), chunksize=4):
            for rec in recs:
                fo.write(json.dumps(rec) + "\n")
                k = str(rec["rho"])
                hist[k] = hist.get(k, 0) + 1
                nrec += 1
                if isinstance(rec["rho"], int):
                    maxrho = max(maxrho, rec["rho"])
    print(json.dumps({"order": n, "graphs": len(lines), "hole_classes": nrec, "rho_hist": hist, "max_rho": maxrho}))


if __name__ == "__main__":
    main()
