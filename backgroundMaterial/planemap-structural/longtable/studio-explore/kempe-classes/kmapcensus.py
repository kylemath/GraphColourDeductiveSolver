#!/usr/bin/env python3
"""[exploratory] Workstream A census with kmap.cpp: per graph, for every vertex orbit of degree 5, 6 or 7 and every
edge orbit (full automorphism group): kappa(T), kappa(H) for H = T - v or T - e, new classes (created by the
deletion), merging classes; the degree-5 holes are joined with rho from the radius census (out-N.jsonl).
Records with new classes keep the graph line. usage: plantri -m5 -c4 N -a | kmapcensus.py N OUT.jsonl [--workers K] [--no-edges]"""
import json, os, subprocess, sys, tempfile
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from census import parse, automorphisms  # noqa: E402
KMAP = os.path.join(HERE, "kmap")
EDGES = "--no-edges" not in sys.argv


def run(path, *a):
    o = subprocess.run([KMAP, path] + [str(x) for x in a], capture_output=True, text=True).stdout.strip().splitlines()
    return json.loads(o[0]) if o else {"error": "no output"}


def work(item):
    idx, line = item
    rot = parse(line)
    auts = automorphisms(rot)
    E = sorted({tuple(sorted((v, w))) for v, nb in enumerate(rot) for w in nb})
    with tempfile.NamedTemporaryFile("w", suffix=".edges", delete=False) as fh:
        fh.write("%d %d\n" % (len(rot), len(E)))
        for e in E:
            fh.write("%d %d\n" % e)
        path = fh.name
    out = {"index": idx, "n_aut": len(auts), "vertices": [], "edges": []}
    try:
        seen = set()
        for v in range(len(rot)):
            if len(rot[v]) not in (5, 6, 7) or v in seen:
                continue
            orb = {m[v] for m in auts}; seen |= orb
            o = run(path, "v", v)
            rec = {"v": v, "deg": len(rot[v]), "orbit_size": len(orb), **{k: o.get(k) for k in ("kT", "kH", "new_classes", "merging_H_classes", "max_T_classes_per_H_class")}}
            if "error" in o or "inconclusive" in o: rec["engine"] = o
            if o.get("new_classes"): rec["graph"] = line
            out["vertices"].append(rec)
        if EDGES:
            seen = set()
            for e in E:
                if e in seen:
                    continue
                orb = {tuple(sorted((m[e[0]], m[e[1]]))) for m in auts}; seen |= orb
                o = run(path, "e", e[0], e[1])
                rec = {"e": list(e), "degs": [len(rot[e[0]]), len(rot[e[1]])], "orbit_size": len(orb), **{k: o.get(k) for k in ("kT", "kH", "new_classes", "merging_H_classes", "max_T_classes_per_H_class")}}
                if "error" in o or "inconclusive" in o: rec["engine"] = o
                if o.get("new_classes"): rec["graph"] = line
                out["edges"].append(rec)
    finally:
        os.unlink(path)
    return out


def main():
    n, outp = int(sys.argv[1]), sys.argv[2]
    w = int(sys.argv[sys.argv.index("--workers") + 1]) if "--workers" in sys.argv else 6
    lines = [l for l in sys.stdin.read().splitlines() if l.strip()]
    rho = {}
    rp = os.path.join(HERE, "out-%d.jsonl" % n)
    if os.path.exists(rp):
        for l in open(rp):
            r = json.loads(l); rho[(r["index"], r["hole"])] = r["rho"]
    with open(outp, "w") as fo, Pool(w) as pool:
        for r in pool.imap(work, ((i, l) for i, l in enumerate(lines)), chunksize=4):
            for v in r["vertices"]:
                if v["deg"] == 5: v["rho"] = rho.get((r["index"], v["v"]))
            fo.write(json.dumps(r) + "\n")
    print(json.dumps({"order": n, "graphs": len(lines), "done": True}))


if __name__ == "__main__":
    main()
