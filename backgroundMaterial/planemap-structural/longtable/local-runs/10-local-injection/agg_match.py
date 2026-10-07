#!/usr/bin/env python3
"""[exploratory] Aggregate the DDmatch field of qf.py --match output: per order, the k_min histogram over (class, j) with
DD_j > 0, the number saturated at each k <= 8, the maximum k_min with witnesses, k_min against DD_j and against room_j - DD_j
(tight cases), and how many (class, j) are tight (room_j = DD_j).  usage: agg_match.py match-*.jsonl > match-summary.json"""
import json, sys
from collections import Counter, defaultdict
hist = defaultdict(Counter); satk = defaultdict(Counter); wit = {}; tight = defaultdict(Counter); bydd = defaultdict(Counter); tot = Counter()
for fn in sys.argv[1:]:
    for l in open(fn):
        r = json.loads(l); n = r["order"]
        for k in r["classes"]:
            for m in (k.get("DDmatch") or []):
                km = m["k_min"]; hist[n][str(km)] += 1; tot[n] += 1
                for kk in range(1, 9):
                    if km is not None and km <= kk: satk[n][kk] += 1
                slack = m["room_j"] - m["DD_j"]
                tight[n]["slack0" if slack == 0 else "slack>0"] += 1
                if slack == 0: tight[n]["slack0_kmin_%s" % km] += 1
                bydd["DD_j=%d" % m["DD_j"] if m["DD_j"] <= 8 else "DD_j>8"][str(km)] += 1
                cur = wit.get(n)
                if km is None or cur is None or (cur["k_min"] is not None and km > cur["k_min"]):
                    if cur is None or cur["k_min"] is not None:
                        wit[n] = {"k_min": km, "gentri_index": r["gentri_index"], "hole": r["hole"], "size": k["size"], "j": m["j"],
                                  "DD_j": m["DD_j"], "room_j": m["room_j"], "matched_by_k": m["matched_by_k"], "dP_hist": k["dP_hist"], "D_cyc": k["D_cyc"]}
out = {"class_j_pairs_with_DD": dict(sorted(tot.items())), "k_min_hist": {n: dict(sorted(c.items())) for n, c in sorted(hist.items())},
       "saturated_by_k": {n: dict(sorted(c.items())) for n, c in sorted(satk.items())}, "max_k_min_witness": dict(sorted(wit.items())),
       "tightness": {n: dict(sorted(c.items())) for n, c in sorted(tight.items())}, "k_min_by_DD_j": {k: dict(sorted(v.items())) for k, v in sorted(bydd.items())}}
print(json.dumps(out, indent=1))
