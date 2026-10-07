#!/usr/bin/env python3
"""[exploratory] Local compute item 14(A): two-hole floor candidates. For every graph of studiointel/gentri/triN.txt and every
unordered pair {v, w} of degree-5 vertices (adjacent and non-adjacent), all Kempe classes of T - v - w via ./k2 (see k2.cpp).
Per class record: [size, Fv, Fw, Fboth, Fany, Fext, Fv_0..4, Uv_0..4, Fw_0..4, Uw_0..4] (per-j only for non-adjacent pairs).
usage: two_hole.py --orders 12 14 ... > pairs-ORDERS.jsonl   (one line per pair)"""
import json, os, subprocess, sys, tempfile, itertools
from multiprocessing import Pool
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, "..", "common"))
from kempe_py import gentri_rotation
GENTRI = os.path.join(H, "..", "..", "..", "studiointel", "gentri"); K2 = os.path.join(H, "k2")


def work(task):
    n, gi, line = task; rot = gentri_rotation(line)
    E = sorted({(min(a, b), max(a, b)) for a in range(len(rot)) for b in rot[a]})
    d5 = [v for v in range(len(rot)) if len(rot[v]) == 5]; pairs = list(itertools.combinations(d5, 2))
    with tempfile.NamedTemporaryFile("w", suffix=".in", delete=False) as fh:
        fh.write("%d %d\n" % (len(rot), len(E)) + "".join("%d %d\n" % e for e in E) + "%d\n" % len(pairs))
        for v, w in pairs: fh.write("%d %d %s %s\n" % (v, w, " ".join(map(str, rot[v])), " ".join(map(str, rot[w]))))
        p = fh.name
    out = subprocess.run(["nice", "-n", "10", K2, p], capture_output=True, text=True).stdout
    os.unlink(p)
    return [{"order": n, "gentri_index": gi, **json.loads(l)} for l in out.split("\n") if l.strip()]


if __name__ == "__main__":
    orders = [int(x) for x in sys.argv[sys.argv.index("--orders") + 1:]]
    tasks = [(n, gi, l) for n in orders for gi, l in enumerate(x for x in open(os.path.join(GENTRI, "tri%d.txt" % n)) if x.strip())]
    with Pool(6) as pool:
        for res in pool.imap(work, tasks, chunksize=1):
            for r in res: print(json.dumps(r), flush=True)
