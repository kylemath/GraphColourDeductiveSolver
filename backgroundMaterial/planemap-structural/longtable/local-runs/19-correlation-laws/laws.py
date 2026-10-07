"""[exploratory] Item 19 task 2: all minimal valid inequalities  U(u) <= sum_{t in S} F(t)  (u an unfilled link sequence, S a set of filled
link sequences), valid in every class of the data, closed under the dihedral group of the link (rotations of x_0, mirror image).
Because the data are closed under D_d, it suffices to test one representative u per dihedral orbit; the conjugates follow.
The subset search is in minsets.cpp (all subsets up to size KMAX in size order, minimal ones kept).
usage: laws.py TAG (12-20 | 12-24) > laws-TAG.json"""
import json, subprocess, sys, time
import lib
tag = sys.argv[1]; KMAX = {5: 5, 6: 8, 7: 8}
out = {}
for d in (5, 6, 7):
    D = lib.Deg(d); data = json.load(open("classes-%d-%s.json" % (d, tag)))
    vecs = data["vectors"]; filled = D.filled; nf = len(filled)
    res = {"deg": d, "n_unique_classes": len(vecs), "orbits": []}
    invs = []
    for p in D.perm:
        inv = [0] * len(p)
        for i, j in enumerate(p): inv[j] = i
        invs.append(inv)
    for orb in D.orbits:
        u = orb[0]
        if lib.is_filled(D.seqs[u]): continue
        t0 = time.time()
        invs_u = sorted({tuple([inv[u]] + [inv[f] for f in filled]) for inv in invs})
        cons = set()
        for v in vecs:
            for t in invs_u:
                if v[t[0]] > 0: cons.add(tuple(v[x] for x in t))
        # Pareto thinning is skipped: the C++ search scans the tightest constraints first
        inp = "%d %d %d\n" % (nf, len(cons), KMAX[d]) + "".join(" ".join(map(str, c)) + "\n" for c in cons)
        o = subprocess.run(["nice", "-n", "10", "./minsets"], input=inp, capture_output=True, text=True).stdout.split("\n")
        masks = [int(x) for x in o if x and not x.startswith("ALL")]; allok = any(x == "ALL 1" for x in o)
        sets = [[i for i in range(nf) if m >> i & 1] for m in masks]
        res["orbits"].append({"rep": "".join(map(str, D.seqs[u])), "orbit_size": len(orb), "n_constraints": len(cons),
            "all_filled_valid": allok, "searched_up_to_size": min(KMAX[d], nf),
            "minimal_valid_S": [["".join(map(str, D.seqs[filled[i]])) for i in S] for S in sets],
            "min_size": min((len(S) for S in sets), default=None)})
        print(d, "".join(map(str, D.seqs[u])), "cons", len(cons), "minimal valid sets", len(sets), "min size", res["orbits"][-1]["min_size"], "%.1fs" % (time.time() - t0), flush=True)
    out[str(d)] = res
json.dump(out, open("laws-%s.json" % tag, "w"), indent=1)
