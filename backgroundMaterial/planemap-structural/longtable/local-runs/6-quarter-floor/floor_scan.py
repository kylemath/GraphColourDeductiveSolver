#!/usr/bin/env python3
"""[exploratory] Local compute item 6: exhaustive check of Local Intel's empirical 1/4 floor on the filled fraction of a
Kempe class. For every graph of studiointel/gentri/triN.txt (4-connected min-degree-5 triangulations; counts equal
plantri -m5 -c4) and EVERY vertex v of the requested degrees: all Kempe classes of T - v (../common/krad, states up to
renaming, whole-component swaps), each with size and #filled (filled = the link of v uses <= 3 colours).
Also per hole: the labelled ratio #filled labelled colourings / #labelled colourings of T - v (= n_filled / n_states,
since every state uses >= 3 colours and so stands for exactly 24 labelled colourings), and P(T,4)/P(T-v,4)
(= states(T) / states(T - v) for the same reason).
usage: floor_scan.py --orders 12 14 ... --degrees 5 [6 7] [--workers 6] > out.jsonl  (one line per hole)"""
import json, os, subprocess, sys, tempfile
from multiprocessing import Pool
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, "..", "common"))
from kempe_py import gentri_rotation
GENTRI = os.path.join(H, "..", "..", "..", "studiointel", "gentri"); KRAD = os.path.join(H, "..", "common", "krad")


def args(flag):
    i = sys.argv.index(flag) + 1; out = []
    while i < len(sys.argv) and not sys.argv[i].startswith("--"): out.append(int(sys.argv[i])); i += 1
    return out


def work(task):
    n, gi, line, degs = task
    rot = gentri_rotation(line)
    E = sorted({(min(a, b), max(a, b)) for a in range(len(rot)) for b in rot[a]})
    with tempfile.NamedTemporaryFile("w", suffix=".el", delete=False) as fh:
        fh.write("%d %d\n" % (len(rot), len(E)) + "".join("%d %d\n" % e for e in E)); p = fh.name
    run = lambda h: json.loads(subprocess.run(["nice", "-n", "10", KRAD, p, str(h)], capture_output=True, text=True).stdout)
    T = run(-1); out = []
    for v in range(len(rot)):
        if len(rot[v]) not in degs: continue
        o = run(v)
        out.append({"order": n, "gentri_index": gi, "hole": v, "deg": len(rot[v]), "states": o["n_states"], "filled": o["n_filled"],
                    "states_T": T["n_states"], "kappa_T": T["n_classes"], "rho": o["rho"],
                    "classes": [[c["size"], c["filled"]] for c in o["classes"]]})
    os.unlink(p)
    return out


def main():
    orders, degs = args("--orders"), set(args("--degrees"))
    wk = args("--workers")[0] if "--workers" in sys.argv else 6
    tasks = [(n, gi, l, degs) for n in orders for gi, l in enumerate(x for x in open(os.path.join(GENTRI, "tri%d.txt" % n)) if x.strip())]
    with Pool(wk) as pool:
        for res in pool.imap(work, tasks, chunksize=2):
            for r in res: print(json.dumps(r), flush=True)


if __name__ == "__main__":
    main()
