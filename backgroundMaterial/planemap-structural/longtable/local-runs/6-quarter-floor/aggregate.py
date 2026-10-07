#!/usr/bin/env python3
"""[exploratory] Aggregate floor_scan.py output: per degree and order, the classes, minimum filled fraction (exact),
classes at exactly 1/4, histogram of fractions in [0.25, 0.30], minimum labelled ratio n_filled/n_states, minimum
P(T,4)/P(T-v,4) = states_T/states. usage: aggregate.py holes-*.jsonl > summary.json"""
import json, sys
from fractions import Fraction as Fr
from collections import Counter, defaultdict
agg = defaultdict(lambda: {"holes": 0, "classes": 0, "min_frac": None, "min_frac_witness": None, "at_quarter": 0,
                           "quarter_sizes": Counter(), "below_quarter": 0, "hist_025_030": Counter(), "min_lab_ratio": None,
                           "min_lab_witness": None, "min_PT_ratio": None, "targetless": 0, "graphs": set()})
for fn in sys.argv[1:]:
    for l in open(fn):
        r = json.loads(l); a = agg[(r["deg"], r["order"])]; a["holes"] += 1; a["graphs"].add(r["gentri_index"])
        lab = Fr(r["filled"], r["states"]); pt = Fr(r["states_T"], r["states"])
        if a["min_lab_ratio"] is None or lab < a["min_lab_ratio"]: a["min_lab_ratio"] = lab; a["min_lab_witness"] = [r["gentri_index"], r["hole"]]
        if a["min_PT_ratio"] is None or pt < a["min_PT_ratio"]: a["min_PT_ratio"] = pt
        for size, f in r["classes"]:
            a["classes"] += 1; fr = Fr(f, size)
            if f == 0: a["targetless"] += 1
            if a["min_frac"] is None or fr < a["min_frac"]:
                a["min_frac"] = fr; a["min_frac_witness"] = {"gentri_index": r["gentri_index"], "hole": r["hole"], "size": size, "filled": f}
            if fr == Fr(1, 4): a["at_quarter"] += 1; a["quarter_sizes"][size] += 1
            if fr < Fr(1, 4): a["below_quarter"] += 1
            if Fr(1, 4) <= fr <= Fr(3, 10): a["hist_025_030"][str(fr)] += 1
out = {}
for (d, n), a in sorted(agg.items()):
    out["deg%d_order%d" % (d, n)] = {"graphs_with_such_hole": len(a["graphs"]), "holes": a["holes"], "classes": a["classes"],
        "targetless": a["targetless"], "min_frac": str(a["min_frac"]), "min_frac_float": float(a["min_frac"]) if a["min_frac"] is not None else None,
        "min_frac_witness": a["min_frac_witness"], "classes_at_exactly_1/4": a["at_quarter"], "below_1/4": a["below_quarter"],
        "quarter_class_sizes": dict(sorted(a["quarter_sizes"].items())),
        "fractions_in_[1/4,3/10]": dict(sorted(a["hist_025_030"].items(), key=lambda kv: Fr(kv[0]))),
        "min_labelled_ratio_filled_over_all": str(a["min_lab_ratio"]), "min_labelled_ratio_float": float(a["min_lab_ratio"]),
        "min_labelled_ratio_witness": a["min_lab_witness"], "min_P(T)/P(T-v)": str(a["min_PT_ratio"]), "min_P(T)/P(T-v)_float": float(a["min_PT_ratio"])}
print(json.dumps(out, indent=1))
