#!/usr/bin/env python3
"""[exploratory] Aggregate the DD-locality fields (DDloc) of qf.py output: for each order, histogram of the Kempe distance
from DD states (DL states whose R+3 image is DL) to the nearest compensating unit (E path start, U^ff, filled with a long
bit), by order and by d(P) of the state's Gamma-path ("cyc" = on a DL cycle); per-kind nearest distances; and the room
decomposition of every class with D_cyc > 0.  usage: agg_dd.py ddloc-*.jsonl > ddloc-summary.json"""
import json, sys
from collections import Counter, defaultdict
by_order = defaultdict(Counter); by_d = defaultdict(Counter); kind = defaultdict(Counter); maxw = {}; cyc = []; cls = Counter()
for fn in sys.argv[1:]:
    for l in open(fn):
        r = json.loads(l); n = r["order"]
        for k in r["classes"]:
            x = k.get("DDloc")
            if k["D_cyc"] > 0:
                room = [pj[1] + pj[2] + pj[3] + pj[4] for pj in k["perj"]]
                cyc.append({"order": n, "gentri_index": r["gentri_index"], "hole": r["hole"], "size": k["size"], "F": k["F"], "U": k["U"],
                            "N0": k["N0"], "N1": k["N1"], "D": k["D"], "D_cyc": k["D_cyc"], "L_F": k["L_F"], "paths": k["paths"], "dP_hist": k["dP_hist"],
                            "per_j_[lhs,L_j,Uff_j,Uff_j+3,E_j,DD_j]": k["perj"], "room_per_j": room, "DD": k["DD"],
                            "room_sum_parts": {"L": sum(pj[1] for pj in k["perj"]), "Uff_j+Uff_j+3": sum(pj[2] + pj[3] for pj in k["perj"]),
                                               "E": sum(pj[4] for pj in k["perj"])}, "DDloc": x})
            if not x: continue
            cls[n] += 1
            for key, m in x["hist_d_dist"].items():
                d, dist = key.split(":"); dist = int(dist)
                by_order[n][dist] += m; by_d[d][dist] += m
                if dist > maxw.get(n, (-9,))[0]: maxw[n] = (dist, {"gentri_index": r["gentri_index"], "hole": r["hole"], "size": k["size"], "d": d})
            for key, m in x["hist_kind_dist"].items(): kind[n][key] += m
out = {"classes_with_DD_by_order": dict(sorted(cls.items())),
       "dist_hist_by_order": {n: dict(sorted(c.items())) for n, c in sorted(by_order.items())},
       "max_dist_by_order": {n: maxw[n] for n in sorted(maxw)},
       "dist_hist_by_dP": {d: dict(sorted(c.items())) for d, c in sorted(by_d.items(), key=lambda kv: (kv[0] == "cyc", int(kv[0]) if kv[0] != "cyc" else 0))},
       "nearest_by_kind_by_order": {n: dict(sorted(c.items())) for n, c in sorted(kind.items())},
       "classes_with_DL_cycles": cyc}
print(json.dumps(out, indent=1))
