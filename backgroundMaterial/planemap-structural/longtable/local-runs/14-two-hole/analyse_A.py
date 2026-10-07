#!/usr/bin/env python3
"""[exploratory] Item 14(A) analysis of k2 output (complete files only). Per class [size, Fv, Fw, Fboth, Fany, Fext, Fv_i, Uv_j, Fw_i, Uw_j].
Candidates, split by adjacent / non-adjacent pairs: (i) Fv/size >= 1/4 and Fw/size >= 1/4; (ii) Fboth/size >= 1/16 (and the
minimum), and Fext/size (states extending to T); (iii) min Fany/size; (iv) per-j at v and at w: U_j <= F_{j+1}+F_{j+3}+F_{j+4}
(non-adjacent only); (v) classes with Fany = 0, Fboth = 0, Fext = 0. Exact fractions; first violation recorded.
usage: analyse_A.py pairs-12-20.jsonl pairs-21-22.jsonl > A-summary.json"""
import json, sys
from fractions import Fraction as Fr
from collections import Counter
out = {}
for adjflag in (False, True):
    m = {}; first = {}; cnt = Counter()
    def upd(key, val, wit, below=None):
        if key not in m or val < m[key][0]: m[key] = (val, wit)
        if below is not None and val < below: cnt["viol_" + key] += 1; first.setdefault(key, {**wit, "value": str(val)})
    for fn in sys.argv[1:]:
        for l in open(fn):
            r = json.loads(l)
            if r["adjacent"] != adjflag: continue
            cnt["pairs"] += 1
            for c in r["classes"]:
                cnt["classes"] += 1; s = c[0]
                wit = {"order": r["order"], "gentri_index": r["gentri_index"], "v": r["v"], "w": r["w"], "class_size": s}
                upd("Fv_frac", Fr(c[1], s), wit, Fr(1, 4)); upd("Fw_frac", Fr(c[2], s), wit, Fr(1, 4))
                upd("Fboth_frac", Fr(c[3], s), wit, Fr(1, 16)); upd("Fany_frac", Fr(c[4], s), wit); upd("Fext_frac", Fr(c[5], s), wit, Fr(1, 16))
                if c[4] == 0: cnt["no_fill_either"] += 1; first.setdefault("no_fill_either", wit)
                if c[3] == 0: cnt["no_fill_both"] += 1; first.setdefault("no_fill_both", wit)
                if c[5] == 0: cnt["no_extension_to_T"] += 1; first.setdefault("no_extension_to_T", wit)
                if not adjflag:
                    for off, nm in ((6, "v"), (16, "w")):
                        F = c[off:off + 5]; U = c[off + 5:off + 10]
                        for j in range(5):
                            if U[j] > F[(j + 1) % 5] + F[(j + 3) % 5] + F[(j + 4) % 5]:
                                cnt["perj_viol_" + nm] += 1; first.setdefault("perj_" + nm, {**wit, "j": j, "F": F, "U": U})
    out["adjacent" if adjflag else "non_adjacent"] = {"counts": dict(cnt), "minima": {k: {"value": str(v[0]), "float": float(v[0]), "witness": v[1]} for k, v in m.items()},
                                                     "first_violations": first}
print(json.dumps(out, indent=1))
