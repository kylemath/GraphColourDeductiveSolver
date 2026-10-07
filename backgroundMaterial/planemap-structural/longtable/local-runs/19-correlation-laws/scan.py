#!/usr/bin/env python3
"""[exploratory] Item 19 driver: per-class link-pattern counts at every degree 5..7 hole, gentri orders given.
usage: scan.py --orders 12 14 ... > patterns-ORDERS.jsonl     (3 workers, nice 10 children)"""
import json, os, subprocess, sys
from multiprocessing import Pool
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, "..", "common"))
from kempe_py import gentri_rotation
GENTRI = os.path.join(H, "..", "..", "..", "studiointel", "gentri"); KP = os.path.join(H, "kpat")

def work(task):
    n, gi, line = task; rot = gentri_rotation(line)
    inp = "%d\n" % len(rot) + "".join("%d %s\n" % (len(r), " ".join(map(str, r))) for r in rot)
    out = subprocess.run(["nice", "-n", "10", KP], input=inp, capture_output=True, text=True).stdout
    res = []
    for l in out.splitlines():
        o = json.loads(l); o["order"] = n; o["gentri_index"] = gi; res.append(o)
    return res

if __name__ == "__main__":
    orders = [int(x) for x in sys.argv[sys.argv.index("--orders") + 1:]]
    tasks = [(n, gi, l) for n in orders for gi, l in enumerate(x for x in open(os.path.join(GENTRI, "tri%d.txt" % n)) if x.strip())]
    with Pool(3) as pool:
        for res in pool.imap(work, tasks, chunksize=1):
            for r in res: print(json.dumps(r, separators=(",", ":")), flush=True)
