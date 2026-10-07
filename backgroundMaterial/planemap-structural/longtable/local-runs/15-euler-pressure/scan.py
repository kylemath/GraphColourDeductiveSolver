#!/usr/bin/env python3
"""[exploratory] Euler-pressure scan: Euler-slack features of every state of T - v, all degree-5 holes v.
Reuses ../common/kempe_py.py (Space: states up to renaming, Kempe move graph, classes, dist_to_filled).
usage: scan.py --orders 12 14 ... [--floor-orders 21 22 23 24] [--workers 3] --out states.csv.gz
 main orders  : every degree-5 hole of every gentri graph; every state recorded; states of classes with filled fraction exactly 1/4 are tagged floor=1
 floor orders : only the degree-5 holes listed in ../6-quarter-floor/quarter-classes.jsonl (they contain a 1/4 class); ONLY states of 1/4 classes are recorded (floor=1)"""
import os, sys, json, gzip, time
from multiprocessing import Pool
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, "..", "common")); sys.path.insert(0, H)
from kempe_py import Space, gentri_rotation, adj_from_rot
from euler_features import features, FEATURES
GENTRI = os.path.join(H, "..", "..", "..", "studiointel", "gentri")
QC = os.path.join(H, "..", "6-quarter-floor", "quarter-classes.jsonl")
COLS = ["order", "gi", "hole", "floor", "filled", "dist", "cls_size", "cls_filled"] + FEATURES


def args(flag):
    if flag not in sys.argv: return []
    i = sys.argv.index(flag) + 1; out = []
    while i < len(sys.argv) and not sys.argv[i].startswith("--"): out.append(int(sys.argv[i])); i += 1
    return out


def do_hole(n, gi, rot, hole, floor_only):
    sp = Space(adj_from_rot(rot), hole, link=rot[hole])
    sp.build_graph(); sp.classes(); sp.dist_to_filled()
    size = [0] * sp.ncl; fil = [0] * sp.ncl
    for k in range(len(sp.states)):
        size[sp.cl[k]] += 1; fil[sp.cl[k]] += sp.filled(k)
    # adjacency of G in Space index order
    N = sp.N
    adj = [[j for j in range(N) if sp.nbm[i] >> j & 1] for i in range(N)]
    rows = []
    for k, s in enumerate(sp.states):
        c = sp.cl[k]; fl = int(4 * fil[c] == size[c])
        if floor_only and not fl: continue
        f, fr = features(adj, list(s), sp.linki)
        rows.append([n, gi, hole, fl, int(sp.filled(k)), sp.dist[k], size[c], fil[c]] + [f[x] for x in FEATURES])
    return rows


def work(task):
    n, gi, line, holes, floor_only = task
    rot = gentri_rotation(line); out = []
    for h in range(len(rot)):
        if len(rot[h]) != 5: continue
        if holes is not None and h not in holes: continue
        out += do_hole(n, gi, rot, h, floor_only)
    return out


def main():
    orders, forders = args("--orders"), args("--floor-orders")
    wk = args("--workers")[0] if "--workers" in sys.argv else 3
    out = sys.argv[sys.argv.index("--out") + 1]
    qh = {}
    for l in open(QC):
        x = json.loads(l)
        if x["deg"] == 5: qh.setdefault((x["order"], x["gentri_index"]), set()).add(x["hole"])
    tasks = []
    for n in orders:
        for gi, l in enumerate(x for x in open(os.path.join(GENTRI, "tri%d.txt" % n)) if x.strip()):
            tasks.append((n, gi, l, None, False))
    for n in forders:
        for gi, l in enumerate(x for x in open(os.path.join(GENTRI, "tri%d.txt" % n)) if x.strip()):
            if (n, gi) in qh: tasks.append((n, gi, l, qh[(n, gi)], True))
    t0 = time.time(); nrows = 0
    with gzip.open(out, "wt") as fh, Pool(wk) as pool:
        fh.write(",".join(COLS) + "\n")
        for res in pool.imap(work, tasks, chunksize=1):
            for r in res: fh.write(",".join(repr(x) if isinstance(x, float) else str(x) for x in r) + "\n")
            nrows += len(res)
    print("tasks", len(tasks), "rows", nrows, "sec", round(time.time() - t0), file=sys.stderr)


if __name__ == "__main__":
    main()
