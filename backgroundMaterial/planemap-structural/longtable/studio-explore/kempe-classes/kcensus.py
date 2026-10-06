#!/usr/bin/env python3
"""[exploratory] Kempe-class multiplicity census (outside-advisor calibration).
Per graph: number of Kempe classes of the 4-colourings of T (kclass, hole -1). Per vertex orbit of degree 5, 6 or 7
(full automorphism group): classes of T - v, and the number of TARGETLESS classes (no state whose link uses <= 3
colours). Degree 6 and 7 holes are the negative control (R* is only conjectured at degree 5).
usage: plantri -m5 -c4 N -a | kcensus.py N OUT.jsonl [--workers K]
"""
import json
import os
import subprocess
import sys
import tempfile
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from census import parse, automorphisms  # noqa: E402

KCLASS = os.path.join(HERE, "kclass")


def orbits(rot, degs):
    auts = automorphisms(rot)
    rep, seen = [], set()
    for v in range(len(rot)):
        if len(rot[v]) not in degs or v in seen:
            continue
        orb = {m[v] for m in auts}
        seen |= orb
        rep.append((v, len(orb)))
    return rep, len(auts)


def run(path, h):
    o = subprocess.run([KCLASS, path, str(h)], capture_output=True, text=True).stdout.strip().splitlines()[-1]
    return json.loads(o)


def work(item):
    idx, line = item
    rot = parse(line)
    E = {tuple(sorted((v, w))) for v, nb in enumerate(rot) for w in nb}
    with tempfile.NamedTemporaryFile("w", suffix=".edges", delete=False) as fh:
        fh.write("%d %d\n" % (len(rot), len(E)))
        for e in sorted(E):
            fh.write("%d %d\n" % e)
        path = fh.name
    try:
        t = run(path, -1)
        reps, naut = orbits(rot, (5, 6, 7))
        holes = []
        for v, size in reps:
            o = run(path, v)
            rec = {"hole": v, "deg": len(rot[v]), "orbit_size": size, "n_states": o.get("n_states"),
                   "n_classes": o.get("n_classes"), "targetless": o.get("targetless_classes"),
                   "class_sizes": o.get("class_sizes")}
            if "error" in o or "inconclusive" in o:
                rec["engine"] = o
            if o.get("targetless_classes"):
                rec["graph"] = line
            holes.append(rec)
    finally:
        os.unlink(path)
    return {"index": idx, "n_aut": naut, "T_states": t.get("n_states"), "T_classes": t.get("n_classes"),
            "T_class_sizes": t.get("class_sizes"), "holes": holes}


def main():
    n, out = int(sys.argv[1]), sys.argv[2]
    workers = int(sys.argv[sys.argv.index("--workers") + 1]) if "--workers" in sys.argv else 8
    lines = [l for l in sys.stdin.read().splitlines() if l.strip()]
    S = {d: {"orbits": 0, "instances": 0, "inst_ge2": 0, "orb_ge2": 0, "max_classes": 0, "targetless_orbits": 0}
         for d in (5, 6, 7)}
    tmax, tge2 = 0, 0
    with open(out, "w") as fo, Pool(workers) as pool:
        for r in pool.imap(work, ((i, l) for i, l in enumerate(lines)), chunksize=4):
            fo.write(json.dumps(r) + "\n")
            tmax = max(tmax, r["T_classes"] or 0)
            tge2 += (r["T_classes"] or 0) >= 2
            for h in r["holes"]:
                s = S[h["deg"]]
                k = h["n_classes"] or 0
                s["orbits"] += 1
                s["instances"] += h["orbit_size"]
                s["inst_ge2"] += h["orbit_size"] * (k >= 2)
                s["orb_ge2"] += k >= 2
                s["max_classes"] = max(s["max_classes"], k)
                s["targetless_orbits"] += (h["targetless"] or 0) > 0
    for s in S.values():
        s["f2"] = round(s["inst_ge2"] / s["instances"], 4) if s["instances"] else None
    print(json.dumps({"order": n, "graphs": len(lines), "T_classes_max": tmax, "T_graphs_ge2": tge2, "holes": S}))


if __name__ == "__main__":
    main()
