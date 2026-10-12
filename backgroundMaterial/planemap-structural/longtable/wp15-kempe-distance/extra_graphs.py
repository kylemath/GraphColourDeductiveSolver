import json, sys, time, random
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE.parent))
from trigen import rotation_from_edges, grow
from kempe_distance import analyse_root
from mass_core import degree_five, parse_ascii

def run(name, rot, roots=None):
    out = []
    t = time.time()
    for r in (roots or degree_five(rot)):
        a = analyse_root(rot, r); a.pop("all"); 
        out.append(a)
    return out

def slim(a):
    return a

if __name__ == "__main__":
    mode = sys.argv[1]
    res = {}
    if mode == "kittell":
        d = json.load(open(HERE.parents[2] / "agent1720/groups/K6_kittell.json"))
        rot = rotation_from_edges(23, [tuple(e) for e in d["edges"]])
        rows = []
        for r in degree_five(rot):
            t = time.time(); a = analyse_root(rot, r)
            a["all"].pop("dist_q_pairs"); rows.append(a)
            print(r, a["nbr_degrees"], a["states"], "ecc", a["all"]["ecc"], "unr", a["all"]["unreachable"],
                  "classes", a["all"]["kempe_classes"], a["all"]["class_sizes"][:4], "noT", a["all"]["classes_without_target"],
                  "eccB", a["Bonly"]["ecc"], a["Bonly"]["unreachable"], f"{time.time()-t:.1f}s", flush=True)
        res = {"kittell": rows, "rotation": rot}
        (HERE / "kittell-results.json").write_text(json.dumps(res))
    elif mode == "random":
        n, count, seed = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
        rng = random.Random(seed)
        corpus = json.load(open(HERE.parents[1] / "mass-macro-results.json"))
        base = [parse_ascii(g["ascii"]) for o in corpus["orders"] if o["order"] == 20 for g in o["graphs_checked"]]
        rows = []
        for k in range(count):
            rot = grow(rng.choice(base), n, rng)
            roots = degree_five(rot)
            gr = {"n": n, "rotation": rot, "roots": []}
            t = time.time()
            for r in roots:
                a = analyse_root(rot, r); a["all"].pop("dist_q_pairs"); a["all"].pop("hard_examples")
                gr["roots"].append(a)
            e = [a["all"]["ecc"] for a in gr["roots"]]
            print(n, k, "ecc", e, "min", min(e), "unr", sum(a["all"]["unreachable"] for a in gr["roots"]),
                  "classes", [a["all"]["kempe_classes"] for a in gr["roots"]], "noT", sum(a["all"]["classes_without_target"] for a in gr["roots"]),
                  f"{time.time()-t:.0f}s", flush=True)
            rows.append(gr)
            (HERE / f"random-n{n}-seed{seed}.json").write_text(json.dumps(rows))
