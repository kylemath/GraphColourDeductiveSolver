#!/usr/bin/env python3
"""[exploratory] Group statistics for the Euler-pressure scan. usage: analyze.py states.csv.gz out_prefix
Groups (disjoint): filled | unfilled_nonDL | DL_r2 | DL_r3p (all states; the floor tag of scan.py is ignored here).
Scope 'main' = orders 12-20 (floor-tagged rows excluded, they only occur at order 17); scope 'ext' = orders 12-22; 'floor' = all floor rows (orders 17, 21-24)."""
import sys, os, json, gzip
import numpy as np
src, outp = sys.argv[1], sys.argv[2]
cache = src + ".npy"
with gzip.open(src, "rt") as fh: cols = fh.readline().strip().split(",")
if os.path.exists(cache): X = np.load(cache)
else:
    X = np.loadtxt(src, delimiter=",", skiprows=1, dtype=np.float64); np.save(cache, X)
C = {c: X[:, i] for i, c in enumerate(cols)}
Q = ["min_sl", "mean_sl", "ky_min_c", "ky_mean_c", "sl_mu", "sl_alpha", "sl_A", "sl_B", "sl_mu_rel", "Uv", "Ue", "Urank", "Uslack",
     "Fv", "Fe", "Fslack", "ky_alpha", "ky_A", "ky_B", "ky_tot", "pen_alpha", "pen_A", "pen_B", "pen_tot", "ky_pen"]
fl, fi, dist, DL, order = C["floor"] * 0, C["filled"], C["dist"], C["DL"], C["order"]
hole_id = (order * 100000 + C["gi"]) * 100 + C["hole"]
_, hid = np.unique(hole_id, return_inverse=True)
unf = fi == 0
assert np.all(np.isnan(DL[fi == 1])) and not np.any(np.isnan(DL[unf]))
assert np.all(dist[(DL == 1)] >= 2)
G = {"filled": (fl == 0) & (fi == 1), "unfilled_nonDL": (fl == 0) & unf & (DL == 0),
     "DL_r2": (fl == 0) & (DL == 1) & (dist == 2), "DL_r3p": (fl == 0) & (DL == 1) & (dist >= 3),
     }
scopes = {"main": order <= 20, "ext": order <= 22}


def auc_less(x, y):
    """P(x < y) + 0.5 P(x == y) for x from group 1, y from group 2 (Mann-Whitney)."""
    x = x[~np.isnan(x)]; y = y[~np.isnan(y)]
    if len(x) == 0 or len(y) == 0: return float("nan")
    z = np.concatenate([x, y]); u, inv, cnt = np.unique(z, return_inverse=True, return_counts=True)
    cum = np.cumsum(cnt); avg = cum - (cnt - 1) / 2.0; rk = avg[inv]
    r1 = rk[:len(x)].sum(); U = r1 - len(x) * (len(x) + 1) / 2.0   # U = #(x>y)+0.5 ties
    return 1.0 - U / (len(x) * len(y))


def hole_matched(q, a, b, sel):
    """mean over holes having both group a and group b states of (mean_a - mean_b); fraction of such holes with mean_a < mean_b"""
    v = C[q]
    ma = sel & a & ~np.isnan(v); mb = sel & b & ~np.isnan(v)
    nh = hid.max() + 1
    na = np.bincount(hid[ma], minlength=nh); sa = np.bincount(hid[ma], weights=v[ma], minlength=nh)
    nb = np.bincount(hid[mb], minlength=nh); sb = np.bincount(hid[mb], weights=v[mb], minlength=nh)
    ok = (na > 0) & (nb > 0)
    if ok.sum() == 0: return None
    d = sa[ok] / na[ok] - sb[ok] / nb[ok]
    return {"holes": int(ok.sum()), "mean_diff": float(d.mean()), "frac_holes_a_lower": float(((d < 0).sum() + 0.5 * (d == 0).sum()) / ok.sum())}


res = {"columns": cols, "n_rows": int(len(X))}
for sc, sm in scopes.items():
    R = {"counts": {g: int((m & sm).sum()) for g, m in G.items()}, "stats": {}, "sep": {}, "matched": {}, "by_order": {}}
    for q in Q:
        v = C[q]; R["stats"][q] = {}
        for g, m in G.items():
            s = v[m & sm]; s = s[~np.isnan(s)]
            if len(s) == 0: continue
            R["stats"][q][g] = {"n": int(len(s)), "mean": float(s.mean()), "min": float(s.min()), "max": float(s.max()), "std": float(s.std()),
                                "q05": float(np.quantile(s, .05)), "median": float(np.median(s))}
        if sc in ("main", "ext"):
            R["sep"][q] = {}
            for g in ("DL_r2", "DL_r3p"):
                x = v[G[g] & sm]; y = v[G["unfilled_nonDL"] & sm]
                R["sep"][q][g + "_vs_nonDL_auc_DLlower"] = auc_less(x, y)
                R["matched"][q + "|" + g] = hole_matched(q, G[g], G["unfilled_nonDL"], sm)
            x = v[(G["DL_r2"] | G["DL_r3p"]) & sm]; y = v[G["unfilled_nonDL"] & sm]
            R["sep"][q]["DL_vs_nonDL_auc_DLlower"] = auc_less(x, y)
            R["matched"][q + "|DL"] = hole_matched(q, G["DL_r2"] | G["DL_r3p"], G["unfilled_nonDL"], sm)
        if sc == "floor":
            R["sep"][q] = {"floorDL_vs_floornonDL_auc_DLlower": auc_less(v[G["floor_DL"]], v[G["floor_nonDL"]])}
            R["matched"][q + "|floor"] = hole_matched(q, G["floor_DL"], G["floor_nonDL"], sm)
    # saturation counts
    sat = {}
    for g, m in G.items():
        mm = m & sm
        if not mm.any(): continue
        sat[g] = {"n": int(mm.sum()),
                  "Uslack0": int((C["Uslack"][mm] == 0).sum()), "Fslack0": int((C["Fslack"][mm] == 0).sum()),
                  "sl_mu0": int((C["sl_mu"][mm] == 0).sum()), "sl_alpha0": int((C["sl_alpha"][mm] == 0).sum()),
                  "min_sl0": int((C["min_sl"][mm] == 0).sum()), "min_sl_le2": int((C["min_sl"][mm] <= 2).sum()),
                  "Uslack_le2": int((C["Uslack"][mm] <= 2).sum()) if g not in ("filled", "floor_filled") else None,
                  "Urank0": int((C["Urank"][mm] == 0).sum()) if g not in ("filled", "floor_filled") else None}
    R["saturation"] = sat
    for o in sorted(set(order[sm])):
        R["by_order"][str(int(o))] = {g: int((m & (order == o)).sum()) for g, m in G.items()}
    res[sc] = R
json.dump(res, open(outp + ".json", "w"), indent=1)
print("rows", len(X)); print(json.dumps({sc: res[sc]["counts"] for sc in scopes}, indent=1))
