"""Cross-validation of the C engine (macro2.c) against the frozen corpus and the Python reference.

Part A: for every graph of orders 12-20 in mass-macro-results.json and every degree-five root,
        engine under (p, q) must reproduce coloring_orbits, non_target_orbits, one_swap_stuck_orbits,
        two_swap_stuck_orbits per root and the published failing_roots per graph.
Part B: for orders 12..MAXB, engine vs a Python reference built directly from wp11_cert.features /
        wp11_cert.endpoints (mass_core.RootState for the state set) under a list of weight vectors
        including lin: per root and weight, good/bad, two- and one-swap stuck counts, first stuck
        colouring, plus orbit / non-target / hard counts.
Read-only on all existing files; writes crossval-results.json here.
"""
import json
import sys
import time
from multiprocessing import Pool
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from engine import E, run_engine  # noqa: E402
from mass_core import FIXTURES, degree_five, parse_ascii  # noqa: E402
from wp11_cert import endpoints, features, root_setup  # noqa: E402

WEIGHTS_B = [E[k] for k in E] + [[1, 1, 0, 0, 0, 0, 0, 0], [2, 0, 3, 0, 0, 0, 0, 0], [1, 0, 0, 0, 3, 0, 0, 0],
                                 [3, 0, 0, 0, 0, 0, 0, 2], [1, -2, 0, 0, 0, 0, 0, 0], [0, 1, 0, -1, 2, 0, 1, 0]]


def ref_root(args):
    rot, r, weights = args
    t = time.time()
    s, adj, B = root_setup(rot, r)
    nt = hard = 0
    st1 = [0] * len(weights)
    st2 = [0] * len(weights)
    first = [None] * len(weights)
    for c in s.C:
        col = dict(zip(s.V, c))
        p, f = features(adj, B, col)
        if p != 1:
            continue
        nt += 1
        eps = endpoints(adj, col)
        ev = [(m2 is None, features(adj, B, c2)) for _, _, m2, c2 in eps]
        if not any(p2 == 0 for _, (p2, _) in ev):
            hard += 1
        for k, w in enumerate(weights):
            r0 = (1, sum(a * f[n] for a, n in zip(w, f)))
            ranks = [(one, (p2, sum(a * f2[n] for a, n in zip(w, f2)))) for one, (p2, f2) in ev]
            if not any(rk < r0 for one, rk in ranks if one):
                st1[k] += 1
            if not any(rk < r0 for _, rk in ranks):
                st2[k] += 1
                if first[k] is None:
                    first[k] = list(c)
    return {"orbits": len(s.C), "non_target": nt, "hard": hard, "one": st1, "two": st2, "first": first,
            "seconds": time.time() - t}


def main():
    maxb = int(sys.argv[1]) if len(sys.argv) > 1 else 18
    table = json.loads((FIXTURES / "mass-macro-results.json").read_text())
    out = {"part_A": [], "part_B": [], "weights_B": WEIGHTS_B, "max_order_B": maxb}
    okA = True
    tA = time.time()
    eng_time = 0.0
    for o in table["orders"]:
        for g in o["graphs_checked"]:
            rot = parse_ascii(g["ascii"])
            failing = []
            for rr in g["roots"]:
                t = time.time()
                res = run_engine(rot, rr["root"], [E["q"]])
                eng_time += time.time() - t
                w = res["results"][0]
                if not w["good"]:
                    failing.append(rr["root"])
                same = (res["coloring_orbits"] == rr["coloring_orbits"] and res["non_target"] == rr["non_target_orbits"]
                        and w["one_swap_stuck"] == rr["one_swap_stuck_orbits"]
                        and w["two_swap_stuck"] == rr["two_swap_stuck_orbits"]
                        and res["vertex_order"] == rr["vertex_order"]
                        and res["boundary_cyclic_order"] == rr["boundary_cyclic_order"])
                okA &= same
                if not same:
                    print("MISMATCH A", o["order"], g["graph_index"], rr["root"], res, rr)
            match = sorted(failing) == sorted(g["failing_roots"])
            okA &= match
            out["part_A"].append({"order": o["order"], "graph_index": g["graph_index"],
                                  "published_failing_roots": g["failing_roots"], "engine_failing_roots": failing,
                                  "match": match})
    out["part_A_all_match"] = okA
    out["part_A_seconds_total"] = time.time() - tA
    out["part_A_engine_seconds_incl_process_spawn"] = eng_time
    print("Part A all match:", okA, f"{time.time() - tA:.1f}s", "roots:", sum(len(g["roots"]) for o in table["orders"] for g in o["graphs_checked"]))

    jobs, meta = [], []
    for o in table["orders"]:
        if o["order"] > maxb:
            continue
        for g in o["graphs_checked"]:
            rot = parse_ascii(g["ascii"])
            for r in degree_five(rot):
                jobs.append((rot, r, WEIGHTS_B))
                meta.append((o["order"], g["graph_index"], r))
    tB = time.time()
    with Pool(12) as pool:
        refs = pool.map(ref_root, jobs, chunksize=1)
    tref = time.time() - tB
    okB = True
    eng_time = 0.0
    for (order, gi, r), (rot, _, _), ref in zip(meta, jobs, refs):
        t = time.time()
        res = run_engine(rot, r, WEIGHTS_B)
        eng_time += time.time() - t
        rows = res["results"]
        same = (res["coloring_orbits"] == ref["orbits"] and res["non_target"] == ref["non_target"]
                and res["hard"] == ref["hard"]
                and [x["one_swap_stuck"] for x in rows] == ref["one"]
                and [x["two_swap_stuck"] for x in rows] == ref["two"]
                and [x["first_stuck"]["coloring"] if x["first_stuck"] else None for x in rows] == ref["first"])
        okB &= same
        if not same:
            print("MISMATCH B", order, gi, r, res, ref)
        out["part_B"].append({"order": order, "graph_index": gi, "root": r, "orbits": ref["orbits"],
                              "non_target": ref["non_target"], "hard": ref["hard"],
                              "two_swap_stuck": ref["two"], "one_swap_stuck": ref["one"], "match": same,
                              "ref_seconds": ref["seconds"]})
    out["part_B_all_match"] = okB
    out["part_B_roots"] = len(jobs)
    out["part_B_reference_wall_seconds_12proc"] = tref
    out["part_B_reference_cpu_seconds"] = sum(x["seconds"] for x in refs)
    out["part_B_engine_seconds_incl_process_spawn"] = eng_time
    lin_bad = [(m[0], m[1], m[2]) for m, ref in zip(meta, refs) if ref["two"][1] > 0]
    out["lin_bad_roots_B"] = lin_bad
    print("Part B all match:", okB, "roots", len(jobs), f"ref wall {tref:.1f}s cpu {out['part_B_reference_cpu_seconds']:.1f}s engine {eng_time:.1f}s")
    print("lin bad roots:", lin_bad)
    (HERE / f"crossval-results-B{maxb}.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main()
