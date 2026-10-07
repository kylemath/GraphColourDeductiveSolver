"""[exploratory] Item 19 task 4: compare the minimal valid S with the abstract single-swap neighbourhoods (swaps.py).
usage: pattern.py TAG > pattern-TAG.json"""
import json, sys
import lib, swaps
tag = sys.argv[1]; L = json.load(open("laws-%s.json" % tag)); out = {}
for d in (5, 6, 7):
    D = lib.Deg(d); rows = []
    for o in L[str(d)]["orbits"]:
        u = tuple(int(c) for c in o["rep"]); run, uni = swaps.neighbours(u)
        run = {"".join(map(str, w)) for w in run}; uni = {"".join(map(str, w)) for w in uni}
        sets = [set(S) for S in o["minimal_valid_S"]]
        core = set.intersection(*sets) if sets else set()
        minS = [S for S in sets if len(S) == min(map(len, sets))]
        r = {"rep": o["rep"], "N_run": sorted(run), "N_union": sorted(uni), "core_of_all_minimal_S": sorted(core),
             "core_contains_N_run": run <= core, "core_contains_N_union": uni <= core,
             "N_run_in_every_minimal_S": all(run <= S for S in sets), "N_union_in_every_minimal_S": all(uni <= S for S in sets),
             "n_minimal_S": len(sets), "min_size": min(map(len, sets)),
             "smallest_S": [{"S": sorted(S), "extra_beyond_N_union": sorted(S - uni), "N_union_not_in_S": sorted(uni - S)} for S in minS[:6]]}
        rows.append(r)
    out[str(d)] = rows
json.dump(out, open("pattern-%s.json" % tag, "w"), indent=1)
for d in "567":
    for r in out[d]:
        print(d, r["rep"], "|N_run|", len(r["N_run"]), "|N_union|", len(r["N_union"]), "minS", r["min_size"], "nmin", r["n_minimal_S"], "core", len(r["core_of_all_minimal_S"]),
              "N_run<=core", r["core_contains_N_run"], "N_union<=core", r["core_contains_N_union"], "N_union<=every S", r["N_union_in_every_minimal_S"])
        sm = r["smallest_S"][0]; print("    smallest S extra beyond N_union:", sm["extra_beyond_N_union"], "missing N:", sm["N_union_not_in_S"])
