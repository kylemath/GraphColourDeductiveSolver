#!/usr/bin/env python3
"""[exploratory] Local compute item 7: per-class link-position counts at every degree-5 hole (gentri lists).
For each class: [size, F0..F4, U0..U4, D0..D4] from ./krad5 (see krad5.cpp), link positions in rotation order rot[v].
usage: counts_scan.py --orders 12 14 ... > counts-ORDERS.jsonl   (one line per hole)"""
import json, os, subprocess, sys, tempfile
from multiprocessing import Pool
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, "..", "common"))
from kempe_py import gentri_rotation
GENTRI = os.path.join(H, "..", "..", "..", "studiointel", "gentri"); K5 = os.path.join(H, "krad5")


def work(task):
    n, gi, line = task; rot = gentri_rotation(line)
    E = sorted({(min(a, b), max(a, b)) for a in range(len(rot)) for b in rot[a]}); out = []
    for v in range(len(rot)):
        if len(rot[v]) != 5: continue
        with tempfile.NamedTemporaryFile("w", suffix=".el", delete=False) as fh:
            fh.write("%d %d\n" % (len(rot), len(E)) + "".join("%d %d\n" % e for e in E) + " ".join(map(str, rot[v])) + "\n"); p = fh.name
        o = json.loads(subprocess.run(["nice", "-n", "10", K5, p, str(v)], capture_output=True, text=True).stdout); os.unlink(p)
        out.append({"order": n, "gentri_index": gi, "hole": v, "classes": o["classes"]})
    return out


if __name__ == "__main__":
    orders = [int(x) for x in sys.argv[sys.argv.index("--orders") + 1:]]
    tasks = [(n, gi, l) for n in orders for gi, l in enumerate(x for x in open(os.path.join(GENTRI, "tri%d.txt" % n)) if x.strip())]
    with Pool(6) as pool:
        for res in pool.imap(work, tasks, chunksize=2):
            for r in res: print(json.dumps(r), flush=True)
