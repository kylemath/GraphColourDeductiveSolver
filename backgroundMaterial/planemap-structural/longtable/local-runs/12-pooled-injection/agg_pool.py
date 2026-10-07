#!/usr/bin/env python3
"""[exploratory] Aggregate the DDpool field (class-level pooled matching): per order, histogram of pooled k_min over classes
with DD > 0, max with witness, capacity check (capacity = sum_j room_j), and, where DDmatch is present, the per-j max k_min
of the same class for comparison. usage: agg_pool.py FILES... > pool-summary.json"""
import gzip, json, sys
from collections import Counter, defaultdict
hist = defaultdict(Counter); wit = {}; bad = Counter(); comp = defaultdict(Counter); special = None; holes = Counter()
for fn in sys.argv[1:]:
    for l in (gzip.open(fn, "rt") if fn.endswith(".gz") else open(fn)):
        r = json.loads(l); n = r["order"]; holes[n] += 1
        for k in r["classes"]:
            p = k.get("DDpool")
            if not p: continue
            km = p["k_min"]; hist[n][str(km)] += 1
            if p["capacity"] != sum(pj[1] + pj[2] + pj[3] + pj[4] for pj in k["perj"]) or p["DD"] != sum(k["DD"]): bad[n] += 1
            rec = {"gentri_index": r["gentri_index"], "hole": r["hole"], "size": k["size"], "DD": p["DD"], "capacity": p["capacity"],
                   "k_min": km, "matched_by_k": p["matched_by_k"]}
            if k.get("DDmatch"):
                mj = max(m["k_min"] for m in k["DDmatch"]); rec["perj_max_k_min"] = mj; comp[n]["perj%d_pool%s" % (mj, km)] += 1
            if n not in wit or (km or 99) > (wit[n]["k_min"] or 99): wit[n] = rec
            if (n, r["gentri_index"], r["hole"]) == (24, 1460, 19): special = special or []; special.append(rec)
print(json.dumps({"holes_scanned": dict(sorted(holes.items())), "pooled_k_min_hist": {n: dict(sorted(c.items())) for n, c in sorted(hist.items())},
                  "max_pooled_k_min_witness": dict(sorted(wit.items())), "capacity_or_DD_mismatch": dict(bad),
                  "perj_vs_pooled": {n: dict(sorted(c.items())) for n, c in sorted(comp.items())}, "order24_gentri1460_hole19": special}, indent=1))
