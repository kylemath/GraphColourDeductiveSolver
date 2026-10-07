"""[exploratory] Item 19: build the deduplicated class vectors (counts per link sequence) per degree and order range, plus observed floors.
Writes classes-DEG-ORDERS.json (unique count vectors, NOT closed under the dihedral group; closure is done in laws.py)."""
import json, sys, lib
from fractions import Fraction
files = ["patterns-12-17.jsonl", "patterns-18-20.jsonl", "patterns-21-24.jsonl"]
for lo, hi, tag in ((12, 20, "12-20"), (12, 22, "12-22"), (12, 23, "12-23"), (12, 24, "12-24")):
    for d in (5, 6, 7):
        D = lib.Deg(d); uniq = {}; floor = None; nholes = 0
        for deg, order, gi, h, size, pc in lib.load(files, degs=(d,), maxorder=hi, minorder=lo):
            vec = [0] * len(D.seqs)
            for p, c in pc.items(): vec[D.idx[tuple(int(ch) for ch in p)]] = c
            assert sum(vec) == size
            key = tuple(vec)
            if key not in uniq: uniq[key] = (order, gi, h)
            fr = Fraction(sum(vec[i] for i in D.filled), size)
            if floor is None or fr < floor[0]: floor = (fr, order, gi, h, size)
        json.dump({"deg": d, "orders": tag, "n_unique_classes": len(uniq), "min_filled_fraction": str(floor[0]), "floor_witness": floor[1:],
                   "seqs": ["".join(map(str, w)) for w in D.seqs], "filled_idx": D.filled,
                   "vectors": [list(k) for k in uniq], "first_seen": list(uniq.values())}, open("classes-%d-%s.json" % (d, tag), "w"))
        print(tag, d, len(uniq), floor, flush=True)
