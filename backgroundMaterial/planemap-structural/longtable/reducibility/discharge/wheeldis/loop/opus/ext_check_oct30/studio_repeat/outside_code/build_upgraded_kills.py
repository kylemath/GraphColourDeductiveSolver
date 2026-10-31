#!/usr/bin/env python3
"""
Step 1: Build and verify upgraded Spoke Kill Tables (kill_U7.npy, kill_U8.npy, kill_U9.npy,
kill6_U7.npy, kill6_U8.npy, kill6_U9.npy) and L3TAB Masks (studio_l3qtab_+1.json,
studio_l3qtab_-1.json, studio_l3qtabV8_+1.json, studio_l3qtabV8_-1.json) for:
  - Tier A (Pure Two-Engine + k3p): s39o/kill + nl51_kc.txt (8,200) + k3p_D.out (4)
    + k3p_C.cfast (6) + k3x_D.out / k3x_C.cfast (4,407 A100 two-engine configs).
  - Tier B (Full 2-Ball Reducible Set): Tier A + grow.rsst() (633) + grow.explore_kills() (12)
    + out/job30/kpriv.txt (16).

Uses the exact frame(), reqs(), table(), and setup() functions from WDIR/out/job31/st16_filter.py
and WDIR/out/job31/l3q_masks.py. Preserves the original WDIR/out/job31/s39o/kill files untouched.
"""

import os
import sys
import re
import glob
import json
import itertools
import collections
import time
import numpy as np

WDIR = "/Users/fulkanjou/kcfarm/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis"
GDIR = "/Users/fulkanjou/GCOct26"
S39O_KILL = os.path.join(WDIR, "out/job31/s39o/kill")
OUT_BASE = os.path.join(GDIR, "kill_upgraded")

os.chdir(WDIR)
G = {"__file__": os.path.join(WDIR, "loop", "k42", "grow.py"), "__name__": "grow"}
exec(open(G["__file__"]).read(), G)
LET = (5, 6, 7, 8, 9)


def load_configs():
    # 1. Load all kc lines across loop/k[0-9]*/* and nl51_kc.txt
    kc_by_name = {}
    nl51_configs = []
    nl51_path = os.path.join(WDIR, "loop/studio/opus_check/s39o/nl51_kc.txt")
    for l in open(nl51_path).read().splitlines():
        f = l.split()
        if len(f) == 5 and f[1].isdigit() and f[2].isdigit() and ";" in f[3] + f[4]:
            cfg = G["kcline"](l, "nl51")
            nl51_configs.append(cfg)
            if f[0] not in kc_by_name:
                kc_by_name[f[0]] = cfg

    for fn in sorted(glob.glob(os.path.join(WDIR, "loop", "k[0-9]*", "*"))):
        if not os.path.isfile(fn):
            continue
        try:
            lines = open(fn).read().splitlines()
        except UnicodeDecodeError:
            continue
        for l in lines:
            f = l.split()
            if (
                len(f) == 5
                and f[0] not in kc_by_name
                and f[1].isdigit()
                and f[2].isdigit()
                and ";" in f[3] + f[4]
            ):
                kc_by_name[f[0]] = G["kcline"](l, "twoeng")

    def read_names(files):
        names = []
        for fn in files:
            p = fn if os.path.isabs(fn) else os.path.join(WDIR, fn)
            for l in open(p):
                if re.match(r"^[epf]\d+_\S+ r=\d+ ", l):
                    names.append(l.split()[0])
        return list(dict.fromkeys(names))

    k3p_configs = []
    for fn in ("out/job30/k3p_D.out", "out/job30/k3p_C.cfast"):
        for l in open(os.path.join(WDIR, fn)):
            if not l or l[0].isspace() or l.startswith("#"):
                continue
            f = l.split()
            if len(f) >= 5 and f[1].isdigit() and f[2].isdigit() and ";" in f[3] + f[4]:
                k3p_configs.append(G["kcline"](l, "k3p"))
    k3x_names = read_names(["out/job30/k3x_D.out", "out/job30/k3x_C.cfast"])
    k3x_configs = [kc_by_name[n] for n in k3x_names if n in kc_by_name]

    kpriv_configs = []
    kpriv_path = os.path.join(WDIR, "out/job30/kpriv.txt")
    if os.path.exists(kpriv_path):
        for l in open(kpriv_path).read().splitlines():
            if not l or l.startswith("#") or "|" not in l:
                continue
            rhs = l.split("|")[-1].strip()
            f = rhs.split()
            if len(f) == 5 and f[1].isdigit() and f[2].isdigit() and ";" in f[3] + f[4]:
                kpriv_configs.append(G["kcline"](rhs, "kpriv"))

    # RSST D2/C2cons (582 configs in s39o baseline)
    ver = {}
    for l in open(os.path.join(WDIR, "loop", "k44", "rsst_verdicts.txt")):
        if l.startswith("#") or not l.strip():
            continue
        f = l.split()
        v = [x for x in f if x.startswith("verdict=")]
        ver[f[0].split("_")[0]] = v[0][8:] if v else None
    rsst_all = G["rsst"]()
    rsst_582 = [c for c in rsst_all if ver.get(c[0]) in ("D2", "C2cons")]
    explore_12 = G["explore_kills"]()

    def dedupe(cfg_list):
        seen = set()
        out = []
        for c in cfg_list:
            if c[0] not in seen:
                seen.add(c[0])
                out.append(c)
        return out

    forb_tierA = dedupe(rsst_582 + k3x_configs + k3p_configs + nl51_configs)
    forb_tierB = dedupe(rsst_all + explore_12 + kpriv_configs + k3x_configs + k3p_configs + nl51_configs)
    forb_rsst_extra = [
        c for c in dedupe(rsst_all + explore_12 + kpriv_configs) if c[0] not in {x[0] for x in forb_tierA}
    ]

    stats = {
        "nl51": len(nl51_configs),
        "k3p": len(k3p_configs),
        "kpriv": len(kpriv_configs),
        "k3x_a100": len(k3x_configs),
        "rsst_582": len(rsst_582),
        "rsst_all": len(rsst_all),
        "explore_12": len(explore_12),
        "tierA_total": len(forb_tierA),
        "tierB_total": len(forb_tierB),
    }
    return forb_tierA, forb_tierB, forb_rsst_extra, stats


def frame_st16(D, LK, SV):
    G["D"] = D
    G["LK"] = LK
    G["SV"] = dict(SV)
    r2 = {("s", j): v for j, v in SV.items()}
    adj, name, faces = G["build2"](r2)
    nm = {v: x for v, x in name.items()}
    pa = {x: {name[y] for y in adj[v] if y in name} for v, x in nm.items()}
    pf = {frozenset(name[y] for y in f) for f in faces if all(y in name for y in f)}
    return pa, pf


def reqs_forb(forb, P, pa, pf, fd):
    Ps = set(P)
    pa2 = {x: pa[x] & Ps for x in P}
    pf2 = {f for f in pf if f <= Ps}
    out = set()
    for c in forb:
        for e in G["embeddings"](c, P, pa2, pf2, fd):
            r = tuple(sorted((v, c[3][u]) for u, v in e if v not in fd))
            out.add(r)
    return out


J = 2
KN_W = [("w", J - 2), ("w", J - 1), ("w", J + 1), ("w", J + 2)]
KN_S = [("s", J - 2), ("s", J - 1), ("s", J), ("s", J + 1)]
SLOTS = KN_W + KN_S + [("p", J, 1)]


def build_kill_table(U, forb, base_K=None, single_frame_only=False):
    Dd = U if U in (7, 8) else 9
    K = np.zeros((5,) * 9, dtype=bool) if base_K is None else base_K.copy().astype(bool)
    frames = [(6, 6)] if single_frame_only else list(itertools.product((5, 6), repeat=2))
    for c1, c2 in frames:
        LKf = [6] * Dd
        LKf[J] = 6
        LKf[J - 1] = c1
        LKf[J + 1] = c2
        LKf[J - 2] = 6
        LKf[J + 2] = 6
        SVf = {i: 6 for i in range(Dd)}
        pa, pf = frame_st16(Dd, LKf, SVf)
        known = ([("u",)] if U == 7 else []) + [("w", J)] + SLOTS
        fd = {("w", J): 6}
        if U == 7:
            fd[("u",)] = U
        P = list(known)
        rs = reqs_forb(forb, P, pa, pf, fd)
        for r in rs:
            rd = dict(r)
            if ("p", J, 1) not in rd:
                continue
            w1, w2 = rd.get(("w", J - 1)), rd.get(("w", J + 1))
            if not single_frame_only:
                if w1 is not None and (w1 == 5) != (c1 == 5):
                    continue
                if w2 is not None and (w2 == 5) != (c2 == 5):
                    continue
            idx = []
            for k, sl in enumerate(SLOTS):
                if sl in rd:
                    idx.append(rd[sl] - 5)
                elif not single_frame_only and k == 1:
                    idx.append(slice(0, 1) if c1 == 5 else slice(1, 5))
                elif not single_frame_only and k == 2:
                    idx.append(slice(0, 1) if c2 == 5 else slice(1, 5))
                else:
                    idx.append(slice(None))
            K[tuple(idx)] = True
    return K


def mirror(K):
    return np.transpose(K, (3, 2, 1, 0, 7, 6, 5, 4, 8))


def build_l3q_tables(D_val, forb, base_rows_by_sig=None):
    def frame_l3(lk_fill, sv_fill):
        LK = [7] + [lk_fill] * 4 + [9] * (D_val - 5)
        G["D"] = D_val
        G["LK"] = LK
        G["SV"] = {i: sv_fill for i in range(D_val)}
        adj, name, faces = G["build2"]({("s", j): sv_fill for j in range(D_val)})
        pa = {x: {name[y] for y in adj[v] if y in name} for v, x in name.items()}
        pf = {frozenset(name[y] for y in f) for f in faces if all(y in name for y in f)}
        return pa, pf

    def setup(sig, pa):
        W = lambda k: ("w", k % D_val)
        S = lambda k: ("s", k % D_val)
        a = S(0) if sig == 1 else S(-1)
        o = S(-1) if sig == 1 else S(0)
        priv = [x for x in pa if x[0] == "p" and x[1] == 0]
        a2 = [x for x in priv if a in pa[x]]
        assert len(a2) == 1, (sig, priv, a2)
        return {"c": W(sig), "w2": W(2 * sig), "w3": W(3 * sig), "w4": W(4 * sig), "a": a, "o": o, "a2": a2[0]}

    base_map = {}
    if base_rows_by_sig is not None:
        for sig in (1, -1):
            for c_, a_, w2, w3, w4, o_, m_ in base_rows_by_sig[sig]:
                base_map[(sig, c_, a_, w2, w3, w4, o_)] = m_

    out_rows = {}
    stats = collections.Counter()
    for sig in (1, -1):
        pa, pf = frame_l3(6, 6)
        var = setup(sig, pa)
        inv = {v: k for k, v in var.items()}
        P = [("u",), ("w", 0)] + list(var.values())
        fd = {("u",): D_val, ("w", 0): 7}
        rs = reqs_forb(forb, P, pa, pf, fd)
        req_sig = [{inv[v]: g for v, g in r} for r in rs]
        rows = []
        for c_, a_ in itertools.product((5, 6), repeat=2):
            for w2, w3, w4, o_ in itertools.product(LET, repeat=4):
                ent = {"c": c_, "a": a_, "w2": w2, "w3": w3, "w4": w4, "o": o_}
                killA = set()
                for r in req_sig:
                    if all(ent[k] == v for k, v in r.items() if k != "a2"):
                        if "a2" in r:
                            killA.add(r["a2"])
                mA = sum(1 << (L - 5) for L in LET if L not in killA)
                if (sig, c_, a_, w2, w3, w4, o_) in base_map:
                    mA &= base_map[(sig, c_, a_, w2, w3, w4, o_)]
                rows.append([c_, a_, w2, w3, w4, o_, int(mA)])
                stats[int(mA)] += 1
        out_rows[sig] = rows
    return out_rows, dict(sorted(stats.items()))


def extract_full2ball_rules(D_val, w0, forb, u_exact=True):
    G["D"] = D_val
    G["LK"] = [w0] + [5] * (D_val - 1)
    G["SV"] = {j: 6 for j in range(D_val)}
    adj, name, faces = G["build2"]({("s", j): 6 for j in range(D_val)})
    nm = {v: x for v, x in name.items()}
    pa = {x: {name[y] for y in adj[v] if y in name} for v, x in nm.items()}
    pf = {frozenset(name[y] for y in f) for f in faces if all(y in name for y in f)}
    priv0 = sorted(x for x in pa if x[0] == "p" and x[1] == 0)
    priv_set = set(priv0)
    P = ([("u",)] if u_exact else []) + [("w", k) for k in range(D_val)] + [("s", k) for k in range(D_val)] + priv0
    Ps = set(P)
    pa_s = {x: pa[x] & Ps for x in P}
    pf_s = {f for f in pf if f <= Ps}

    rules_by_p = {p_v: set() for p_v in priv0}
    for c in forb:
        _, _, U, g, E, tri = c
        if not any(5 <= g[u] <= 8 for u in U):
            continue
        order = [max(U, key=lambda u: (len(E[u]), g[u]))]
        while len(order) < len(U):
            order.append(max((u for u in U if u not in order), key=lambda u: (len(E[u] & set(order)), g[u])))
        phi = {}

        def ok(u, v):
            if v == ("u",):
                return g[u] == D_val
            if v == ("w", 0):
                return g[u] == w0
            return 5 <= g[u] <= 8

        def is_s_adj(v1, v2):
            return v1[0] == "s" and v2[0] == "s" and (v1[1] - v2[1]) % D_val in (1, D_val - 1)

        def rec(i):
            if i == len(order):
                p_used = [v for v in phi.values() if v in priv_set]
                if len(p_used) != 1:
                    return
                if not all(frozenset(phi[x] for x in t) in pf_s for t in tri):
                    return
                p_v = p_used[0]
                inv_phi = {v: u for u, v in phi.items()}
                p_deg = g[inv_phi[p_v]]
                w_req = {}
                s_req = {}
                for u, v in phi.items():
                    if v[0] == "w" and v[1] != 0:
                        k_off = v[1] if (u_exact or v[1] <= 4) else (v[1] - D_val)
                        w_req[k_off] = (g[u],)
                    elif v[0] == "s":
                        j_off = v[1] if (u_exact or v[1] <= 3) else (v[1] - D_val)
                        s_req[j_off] = g[u]
                ok_frame = True
                for k in range(1, D_val):
                    s_prev, s_cur = ("s", (k - 1) % D_val), ("s", k % D_val)
                    if s_prev in inv_phi and s_cur in inv_phi:
                        u1, u2 = inv_phi[s_prev], inv_phi[s_cur]
                        need_5 = u2 in E[u1]
                        k_off = k if (u_exact or k <= 4) else (k - D_val)
                        if k_off in w_req:
                            if (w_req[k_off] == (5,)) != need_5:
                                ok_frame = False
                                break
                        else:
                            w_req[k_off] = (5,) if need_5 else (6, 7, 8, 9)
                if not ok_frame:
                    return
                rule = (
                    int(p_deg),
                    tuple((int(k), tuple(int(x) for x in allowed)) for k, allowed in sorted(w_req.items())),
                    tuple((int(j), int(req_s)) for j, req_s in sorted(s_req.items())),
                )
                rules_by_p[p_v].add(rule)
                return

            u = order[i]
            pl = [w for w in order[:i] if w in E[u]]
            cand = set.intersection(*[pa_s[phi[w]] for w in pl]) if pl else set(P)
            for v in cand:
                if v in phi.values() or not ok(u, v):
                    continue
                if v in priv_set and any(x in priv_set for x in phi.values()):
                    continue
                bad = False
                for w in order[:i]:
                    vw_in_pa = phi[w] in pa_s[v]
                    w_in_Eu = w in E[u]
                    if vw_in_pa != w_in_Eu:
                        if not (vw_in_pa and not w_in_Eu and is_s_adj(v, phi[w])):
                            bad = True
                            break
                if bad:
                    continue
                phi[u] = v
                rec(i + 1)
                del phi[u]

        rec(0)
    return {p_v: sorted(rules) for p_v, rules in rules_by_p.items()}


def filter_extra_w6(rules, D_val, u_exact=True):
    in_w = {1, 2, D_val - 2, D_val - 1} if u_exact else {1, 2, -2, -1}
    in_s = {0, 1, D_val - 2, D_val - 1} if u_exact else {0, 1, -2, -1}
    return [r for r in rules if any(k not in in_w for k, _ in r[1]) or any(j not in in_s for j, _ in r[2])]


def filter_extra_w7(rules_by_p, D_val):
    out = {}
    for sg, p_v in ((-1, ("p", 0, 1)), (1, ("p", 0, 2))):
        in_w = {(m * sg) % D_val for m in (1, 2, 3, 4)}
        in_s = {0, D_val - 1}
        out[str(sg)] = [r for r in rules_by_p[p_v] if any(k not in in_w for k, _ in r[1]) or any(j not in in_s for j, _ in r[2])]
    return out


def build_extra_rules_dict(forb, base_extra=None):
    e7_6 = set(filter_extra_w6(extract_full2ball_rules(7, 6, forb, True)[("p", 0, 1)], 7, True))
    e7_7 = filter_extra_w7(extract_full2ball_rules(7, 7, forb, True), 7)
    e8_6 = set(filter_extra_w6(extract_full2ball_rules(8, 6, forb, True)[("p", 0, 1)], 8, True))
    e8_7 = filter_extra_w7(extract_full2ball_rules(8, 7, forb, True), 8)
    e9_6 = set(filter_extra_w6(extract_full2ball_rules(9, 6, forb, False)[("p", 0, 1)], 9, False))
    e7_7_m = set(e7_7["-1"])
    e7_7_p = set(e7_7["1"])
    e8_7_m = set(e8_7["-1"])
    e8_7_p = set(e8_7["1"])
    if base_extra is not None:
        e7_6 |= set(base_extra["d7_w6"])
        e7_7_m |= set(base_extra["d7_w7"]["-1"])
        e7_7_p |= set(base_extra["d7_w7"]["1"])
        e8_6 |= set(base_extra["d8_w6"])
        e8_7_m |= set(base_extra["d8_w7"]["-1"])
        e8_7_p |= set(base_extra["d8_w7"]["1"])
        e9_6 |= set(base_extra["d9_w6"])
    return {
        "d7_w6": sorted(e7_6),
        "d7_w7": {"-1": sorted(e7_7_m), "1": sorted(e7_7_p)},
        "d8_w6": sorted(e8_6),
        "d8_w7": {"-1": sorted(e8_7_m), "1": sorted(e8_7_p)},
        "d9_w6": sorted(e9_6),
    }


def save_tier(out_dir, K7, K9, l3_d7, l3_d8, extra_rules=None):
    os.makedirs(out_dir, exist_ok=True)
    TAB = {7: K7, 8: K9.copy(), 9: K9}
    for U in (7, 8, 9):
        K = TAB[U]
        np.save(os.path.join(out_dir, f"kill_U{U}.npy"), K)
        A = np.zeros((5,) * 8, dtype=np.uint8)
        for b_ in range(5):
            A |= K[..., b_].astype(np.uint8) << b_
        np.save(os.path.join(out_dir, f"kill6_U{U}.npy"), np.ascontiguousarray(A))
    for sig in (1, -1):
        fn7 = os.path.join(out_dir, f"studio_l3qtab_{sig:+d}.json")
        json.dump(l3_d7[sig], open(fn7, "w"))
        fn8 = os.path.join(out_dir, f"studio_l3qtabV8_{sig:+d}.json")
        json.dump(l3_d8[sig], open(fn8, "w"))
    if extra_rules is not None:
        json.dump(extra_rules, open(os.path.join(out_dir, "full2ball_extra_rules.json"), "w"))


def main():
    t0 = time.time()
    base_u7 = np.load(os.path.join(S39O_KILL, "kill_U7.npy"))
    base_u9 = np.load(os.path.join(S39O_KILL, "kill_U9.npy"))
    base_l3_d7 = {
        +1: json.load(open(os.path.join(WDIR, "out/job31/s39o/studio_l3qtab_+1.json"))),
        -1: json.load(open(os.path.join(WDIR, "out/job31/s39o/studio_l3qtab_-1.json"))),
    }
    base_l3_d8 = {
        +1: json.load(open(os.path.join(WDIR, "out/job31/s42a/V8/studio_l3qtabV8_+1.json"))),
        -1: json.load(open(os.path.join(WDIR, "out/job31/s42a/V8/studio_l3qtabV8_-1.json"))),
    }

    forb_tierA, forb_tierB, forb_rsst_extra, cfg_stats = load_configs()
    print(f"[Step 1] Config counts: {cfg_stats}", flush=True)

    # Single-frame (6,6) diagnostic on Tier A
    K7_sf = build_kill_table(7, forb_tierA, base_K=base_u7, single_frame_only=True)
    K9_sf = build_kill_table(9, forb_tierA, base_K=base_u9, single_frame_only=True)

    # Exact 4-frame st16_filter.py on Tier A
    K7_tierA = build_kill_table(7, forb_tierA, base_K=base_u7, single_frame_only=False)
    K9_tierA = build_kill_table(9, forb_tierA, base_K=base_u9, single_frame_only=False)
    l3_d7_tierA, hist_d7_tierA = build_l3q_tables(7, forb_tierA, base_l3_d7)
    l3_d8_tierA, hist_d8_tierA = build_l3q_tables(8, forb_tierA, base_l3_d8)
    extra_tierA = build_extra_rules_dict(forb_tierA)

    # Exact 4-frame st16_filter.py on Tier B (incremental on top of Tier A)
    K7_tierB = build_kill_table(7, forb_rsst_extra, base_K=K7_tierA, single_frame_only=False)
    K9_tierB = build_kill_table(9, forb_rsst_extra, base_K=K9_tierA, single_frame_only=False)
    l3_d7_tierB, hist_d7_tierB = build_l3q_tables(7, forb_rsst_extra, l3_d7_tierA)
    l3_d8_tierB, hist_d8_tierB = build_l3q_tables(8, forb_rsst_extra, l3_d8_tierA)
    extra_tierB = build_extra_rules_dict(forb_rsst_extra, base_extra=extra_tierA)

    save_tier(os.path.join(OUT_BASE, "tierA"), K7_tierA, K9_tierA, l3_d7_tierA, l3_d8_tierA, extra_tierA)
    save_tier(os.path.join(OUT_BASE, "tierB"), K7_tierB, K9_tierB, l3_d7_tierB, l3_d8_tierB, extra_tierB)
    save_tier(OUT_BASE, K7_tierA, K9_tierA, l3_d7_tierA, l3_d8_tierA, extra_tierA)

    base_hist_d7 = dict(
        sorted(collections.Counter(r[6] for s in (+1, -1) for r in base_l3_d7[s]).items())
    )
    base_hist_d8 = dict(
        sorted(collections.Counter(r[6] for s in (+1, -1) for r in base_l3_d8[s]).items())
    )

    summary = {
        "config_counts": cfg_stats,
        "baseline_s39o": {
            "KT7_killed": int(base_u7.sum()),
            "KT9_killed": int(base_u9.sum()),
            "total_cells": int(base_u7.size),
            "L3TAB_d7_hist": base_hist_d7,
            "L3TAB_d8_hist": base_hist_d8,
        },
        "tierA_single_frame_66": {
            "KT7_killed": int(K7_sf.sum()),
            "KT7_delta_over_s39o": int(K7_sf.sum() - base_u7.sum()),
            "KT9_killed": int(K9_sf.sum()),
            "KT9_delta_over_s39o": int(K9_sf.sum() - base_u9.sum()),
        },
        "tierA": {
            "KT7_killed": int(K7_tierA.sum()),
            "KT7_delta_over_s39o": int(K7_tierA.sum() - base_u7.sum()),
            "KT7_mirror_exceptions": int((K7_tierA != mirror(K7_tierA)).sum()),
            "KT9_killed": int(K9_tierA.sum()),
            "KT9_delta_over_s39o": int(K9_tierA.sum() - base_u9.sum()),
            "KT9_mirror_exceptions": int((K9_tierA != mirror(K9_tierA)).sum()),
            "L3TAB_d7_hist": hist_d7_tierA,
            "L3TAB_d8_hist": hist_d8_tierA,
            "full2ball_extra_rules": {
                "d7_w6": len(extra_tierA["d7_w6"]),
                "d7_w7_m1": len(extra_tierA["d7_w7"]["-1"]),
                "d7_w7_p1": len(extra_tierA["d7_w7"]["1"]),
                "d8_w6": len(extra_tierA["d8_w6"]),
                "d8_w7_m1": len(extra_tierA["d8_w7"]["-1"]),
                "d8_w7_p1": len(extra_tierA["d8_w7"]["1"]),
                "d9_w6": len(extra_tierA["d9_w6"]),
            },
        },
        "tierB": {
            "KT7_killed": int(K7_tierB.sum()),
            "KT7_delta_over_s39o": int(K7_tierB.sum() - base_u7.sum()),
            "KT7_delta_over_tierA": int(K7_tierB.sum() - K7_tierA.sum()),
            "KT7_mirror_exceptions": int((K7_tierB != mirror(K7_tierB)).sum()),
            "KT9_killed": int(K9_tierB.sum()),
            "KT9_delta_over_s39o": int(K9_tierB.sum() - base_u9.sum()),
            "KT9_delta_over_tierA": int(K9_tierB.sum() - K9_tierA.sum()),
            "KT9_mirror_exceptions": int((K9_tierB != mirror(K9_tierB)).sum()),
            "L3TAB_d7_hist": hist_d7_tierB,
            "L3TAB_d8_hist": hist_d8_tierB,
            "full2ball_extra_rules": {
                "d7_w6": len(extra_tierB["d7_w6"]),
                "d7_w7_m1": len(extra_tierB["d7_w7"]["-1"]),
                "d7_w7_p1": len(extra_tierB["d7_w7"]["1"]),
                "d8_w6": len(extra_tierB["d8_w6"]),
                "d8_w7_m1": len(extra_tierB["d8_w7"]["-1"]),
                "d8_w7_p1": len(extra_tierB["d8_w7"]["1"]),
                "d9_w6": len(extra_tierB["d9_w6"]),
            },
        },
        "elapsed_sec": round(time.time() - t0, 2),
    }

    with open(os.path.join(OUT_BASE, "summary.json"), "w") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    main()

