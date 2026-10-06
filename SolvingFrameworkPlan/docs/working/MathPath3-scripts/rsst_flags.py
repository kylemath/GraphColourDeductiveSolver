#!/usr/bin/env python3
"""[UNTESTED] Authoritative Birkhoff-diamond (RSST 0.7322, index 0) and RSST 2.122 (index 1) containment for the
path 3 instances, using Studio intel's rsst_contain.py and routeb/rsst_parse.py UNCHANGED (as rsst_check.py does).
The builder's diamond / 2.122 flags are proxies only; this script decides.
Usage (cwd must be backgroundMaterial/planemap-structural/studiointel):
    python3 PATH/rsst_flags.py OUTDIR [--all633] > OUTDIR/rsst.jsonl
"""
import glob
import json
import os
import sys

sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.path.join(os.getcwd(), "routeb"))
import rsst_parse  # noqa: E402
import rsst_contain as rc  # noqa: E402


def main():
    outdir = sys.argv[1]
    confs = rsst_parse.parse("routeb/rsst/unavoidable.conf")
    P = [rc.prep_conf(c) for c in confs]
    assert confs[0]["name"] == "0.7322" and confs[1]["name"] == "2.122"
    for p in sorted(glob.glob(os.path.join(outdir, "*.json"))):
        info = json.load(open(p))
        if "rotation" not in info:
            continue
        adj = {v: set(r) for v, r in enumerate(info["rotation"])}
        tf = {frozenset(f) for f in info["faces_oriented"]}
        rec = {"name": info["name"], "n": info["n"], "diamond": rc.contains(adj, tf, P[0]),
               "c2122": rc.contains(adj, tf, P[1])}
        if "--all633" in sys.argv:
            rec["n_rsst"] = sum(rc.contains(adj, tf, q) for q in P)
        print(json.dumps(rec), flush=True)


if __name__ == "__main__":
    main()
