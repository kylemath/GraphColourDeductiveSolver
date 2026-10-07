#!/usr/bin/env python3
"""[exploratory] Item 7 (1)-(2): test every rotation-family inequality  U_j <= sum_{a in A} F_{j+a}  (A a nonempty subset of
Z5, offsets relative to the repeat start j, all j at once) on every degree-5 class in counts-*.jsonl. Also the same with
U_j replaced by its non-DL part (U_j - D_j) and by its DL part D_j. The coordinator's single-term form F_i >= U_j is
A = {i - j}, i.e. offset d = j - i = -a. Mirror symmetry maps a -> 2 - a.
Reports per A: #classes where it fails for some j, #(class, j) violations, #(class, j) equalities with U_j > 0,
#classes where it is tight for all j. Then the minimal valid families giving sum U <= 3 sum F.
usage: ineq.py counts-12-22.jsonl counts-23-24.jsonl > ineq-results.json"""
import json, sys, itertools
from collections import Counter
classes = []
for fn in sys.argv[1:]:
    for l in open(fn):
        r = json.loads(l)
        for c in r["classes"]: classes.append((r["order"], r["gentri_index"], r["hole"], c))
subsets = [A for k in range(1, 6) for A in itertools.combinations(range(5), k)]
res = {"classes": len(classes), "families": {}}
for lhs in ("U", "nonDL", "DL"):
    for A in subsets:
        fail_cl = viol = eq = tight_all = 0; first = None; maxgap = None
        for (n, gi, h, c) in classes:
            F = c[1:6]; U = c[6:11]; D = c[11:16]
            L = U if lhs == "U" else ([U[j] - D[j] for j in range(5)] if lhs == "nonDL" else D)
            bad = False; tall = True
            for j in range(5):
                rhs = sum(F[(j + a) % 5] for a in A)
                if L[j] > rhs:
                    viol += 1; bad = True
                    if first is None: first = {"order": n, "gentri_index": gi, "hole": h, "j": j, "counts": c}
                if L[j] == rhs and L[j] > 0: eq += 1
                if L[j] != rhs: tall = False
            fail_cl += bad; tight_all += tall
        res["families"]["%s_j <= F at offsets %s" % (lhs, list(A))] = {"lhs": lhs, "A": list(A), "size": len(A), "valid": fail_cl == 0,
            "classes_failing": fail_cl, "class_j_violations": viol, "class_j_equalities_positive": eq, "classes_tight_all_j": tight_all,
            "first_violation": first}
V = {k: v for k, v in res["families"].items() if v["valid"] and v["lhs"] == "U"}
minimal = [k for k, v in V.items() if not any(set(w["A"]) < set(v["A"]) for w in V.values())]
res["valid_U_families_minimal"] = minimal
res["valid_U_families_size_le_3"] = [k for k in minimal if V[k]["size"] <= 3]
for lhs in ("nonDL", "DL"):
    Vl = {k: v for k, v in res["families"].items() if v["valid"] and v["lhs"] == lhs}
    res["valid_%s_families_minimal" % lhs] = [k for k, v in Vl.items() if not any(set(w["A"]) < set(v["A"]) for w in Vl.values())]
print(json.dumps(res, indent=1))
