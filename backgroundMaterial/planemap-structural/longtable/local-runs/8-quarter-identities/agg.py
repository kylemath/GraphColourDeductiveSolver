#!/usr/bin/env python3
"""[exploratory] Aggregate qf.py output. usage: agg.py qf-12-20.jsonl qf-21-22.jsonl qf-23.jsonl qf-24-floorholes.jsonl > summary.json
Collision and identity totals are reported per file group: exhaustive orders (all holes) and the order-24 floor-hole subset."""
import json, sys
from collections import Counter
out = {}
for fn in sys.argv[1:]:
    c = Counter(); dP = Counter(); dcyc = Counter(); maxDD = 0; maxDDboth = 0; dld = Counter(); c5 = Counter(); rr = Counter()
    floor = Counter(); floor_terms = Counter(); floor_dld = Counter(); nonblock = []; first_cross = None; maxDD_w = None
    worst_room = None
    for l in open(fn):
        r = json.loads(l); c["holes"] += 1
        c["phi_collisions_cross_j"] += r["phi_collisions_cross_j"]; c["phi_collisions_same_j"] += r["phi_collisions_same_j"]
        c["phi_preimage_max"] = max(c["phi_preimage_max"], r["phi_preimage_max"])
        for k, v in r["C2_bad"].items(): c["C2_bad_" + k] += v
        if r["first_cross_j"] and first_cross is None: first_cross = {"order": r["order"], "gentri_index": r["gentri_index"], "hole": r["hole"], **r["first_cross_j"]}
        for k in r["classes"]:
            c["classes"] += 1; c["identity_mismatch"] += not k["identity_ok"]; c["perj_mismatch"] += k["perj_bad"]; c["bad_path"] += k["bad_path"]
            for d, m in k["dP_hist"].items(): dP[int(d)] += m
            dcyc[k["D_cyc"]] += 1
            if max(k["DD"]) > maxDD: maxDD = max(k["DD"]); maxDD_w = {"order": r["order"], "gentri_index": r["gentri_index"], "hole": r["hole"], "size": k["size"], "DD": k["DD"]}
            maxDDboth = max(maxDDboth, max(k["DDboth"]))
            for j, pj in enumerate(k["perj"]):
                room = pj[1] + pj[2] + pj[3] + pj[4]
                if pj[5] > 0 and (worst_room is None or pj[5] - room > worst_room[0]): worst_room = (pj[5] - room, {"order": r["order"], "gentri_index": r["gentri_index"], "hole": r["hole"], "size": k["size"], "j": j, "DD_j": pj[5], "room": room})
            for d, m in k["DL_dist_hist"].items(): dld[int(d)] += m
            for a, b in k["C5"].items(): c5[a] += b
            for a, b in k["RF_RB"].items(): rr[a] += b
            if 4 * k["F"] == k["size"]:
                floor["classes"] += 1
                terms = tuple(t for t, v in (("N0", k["N0"]), ("L_F", k["L_F"]), ("D_cyc", k["D_cyc"]), ("d!=1", any(int(d) != 1 for d in k["dP_hist"]))) if v)
                floor_terms[",".join(terms) or "all zero"] += 1
                for d, m in k["DL_dist_hist"].items(): floor_dld[int(d)] += m
                floor["all_DL_at_dist_2"] += set(k["DL_dist_hist"]) <= {"2"}
                multi_i = sum(1 for x in k["F_i"] if x) > 1
                # per-j equality U_j = F_{j+1}+F_{j+3}+F_{j+4}: perj[0] is LHS - U_j
                floor["equality_all_j"] += all(pj[0] == 0 for pj in k["perj"])
                if terms or multi_i:
                    nonblock.append({"order": r["order"], "gentri_index": r["gentri_index"], "hole": r["hole"], "size": k["size"], "F_i": k["F_i"],
                                     "multi_i": multi_i, "N0": k["N0"], "L_F": k["L_F"], "D_cyc": k["D_cyc"], "dP_hist": k["dP_hist"], "DD": k["DD"],
                                     "DL_dist_hist": k["DL_dist_hist"], "RF_RB": k["RF_RB"], "C5": k["C5"]})
    out[fn] = {"totals": dict(c), "dP_hist": dict(sorted(dP.items())), "D_cyc_hist_over_classes": dict(sorted(dcyc.items())),
               "max_DD_j": maxDD, "max_DD_j_witness": maxDD_w, "max_DD_and_DDprime_j": maxDDboth,
               "largest_DD_j_minus_room": worst_room, "DL_dist_hist": dict(sorted(dld.items())), "C5": dict(c5), "RF_RB": dict(rr),
               "floor": dict(floor), "floor_nonzero_terms": dict(floor_terms), "floor_DL_dist_hist": dict(sorted(floor_dld.items())),
               "floor_nonblock_classes": nonblock, "first_cross_j_collision": first_cross}
print(json.dumps(out, indent=1))
