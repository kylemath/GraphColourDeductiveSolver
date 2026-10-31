#!/usr/bin/env python3
"""
Step 2: Master Wheel LP Coupled to Compiled C++ Separator (sep3r_l3q)
=====================================================================

Couples the Master Wheel LP (HiGHS LP on Registry A100 with L3Q=1, L3Q8=1, FB=1,
RPATN3) to the compiled 14-thread C++ branch-and-bound separator (`bin/sep3r_l3q`)
in an outer cutting-plane loop across all unpooled 5^d x 5^d (d = 7..17) receiver
wheels, plus the live 125x125 max-plus DP for d = 18..30 and Karp's minimum mean
cycle lambda_9 for d > 30.

Evaluates both:
  1. Tier A (Pure Two-Engine + k3p Upgraded KILLDIR/L3TAB, use_unc=False, use_2126=False)
  2. Tier B (Full 2-Ball Upgraded KILLDIR/L3TAB + UNC + RSST 2.126 '5-6-5' 6-wheels)
and exports the globally verified primal solution to /Users/fulkanjou/GCOct26/sol_unified_a100.json.
"""

import collections
import io
import itertools
import json
import os
import subprocess
import sys
import time
from contextlib import redirect_stdout
from fractions import Fraction

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import hstack, lil_matrix

GDIR = "/Users/fulkanjou/GCOct26"
DIS_DIR = "/Users/fulkanjou/kcfarm/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge"
WDIR = os.path.join(DIS_DIR, "wheeldis")


def ensure_a100_args_file(wdir: str = WDIR) -> str:
    target = "/tmp/args_a100_clean.txt"
    if os.path.exists(target) and os.path.getsize(target) > 0:
        return target
    persisted = os.path.join(GDIR, "kill_upgraded", "args_a100_clean.txt")
    if os.path.exists(persisted) and os.path.getsize(persisted) > 0:
        import shutil
        shutil.copyfile(persisted, target)
        return target
    src = os.path.join(wdir, "loop", "studio", "opus_check", "s44A83", "argsA83_local_rpat_held128.txt")
    tokens = open(src).read().split()
    out_tokens = []
    for tok in tokens:
        if tok == "pat=loop/studio/opus_check/s44A83/k3x_D_240b5a08.out":
            tok = "pat=out/job30/k3x_D.out"
        elif tok == "cpat=loop/studio/opus_check/s44A83/k3x_C_240b5a08.cfast":
            tok = "cpat=out/job30/k3x_C.cfast"
        fn = tok.split("=", 1)[1] if "=" in tok else tok.lstrip("-")
        if fn.endswith(":all"):
            fn = fn[:-4]
        if tok == "w7plus" or os.path.exists(os.path.join(wdir, fn)):
            out_tokens.append(tok)
    content = "\n".join(out_tokens) + "\n"
    with open(target, "w") as f:
        f.write(content)
    if os.path.isdir(os.path.dirname(persisted)):
        with open(persisted, "w") as f:
            f.write(content)
    return target


def ensure_cached_a100_pools():
    """Restore cached A100 receiver pools from kill_upgraded/ if /tmp was wiped."""
    import shutil
    for fn in ("surv_certs.json", "a100_pool_rows.json", "a100_pos_rows.json", "d10_12_sep_rows.json"):
        tmp_p = os.path.join("/tmp", fn)
        pers_p = os.path.join(GDIR, "kill_upgraded", fn)
        if not os.path.exists(tmp_p) and os.path.exists(pers_p):
            shutil.copyfile(pers_p, tmp_p)



def load_st21_and_wlp3r6(argf: str, killdir: str, l3tab: str, l3tab8: str, wdir: str = WDIR):
    """Load st21_check.py and wlp3r6.py namespaces with the specified KILLDIR and L3TAB."""
    solf = os.path.join(wdir, "loop", "studio", "opus_check", "s44A83", "sol_q44fbA83.json")
    certf = os.path.join(wdir, "loop", "studio", "opus_check", "s44A83", "cert_q44nfA83L.json")
    sys.argv = ["st21_check.py", solf, certf, argf]
    os.environ["WLP_SEPF"] = "1"
    os.environ["WLP3X_DEF"] = "1"
    os.environ["V6"] = "0"
    os.environ["HAT5"] = "1"
    os.environ["L3Q"] = "1"
    os.environ["L3Q8"] = "1"
    os.environ["FB"] = "1"
    os.environ["XO"] = "0"
    os.environ["L3TAB"] = l3tab
    os.environ["L3TAB8"] = l3tab8
    os.environ["KILLDIR"] = killdir
    os.environ["RPATN"] = f"{wdir}/out/job31/s39o_rpatN3_studio.txt"
    os.environ["EXPECT_PAT"] = "18131,2229,158"
    os.environ["SEP_NODELIMIT"] = "0"

    code = open(os.path.join(wdir, "out", "job31", "st21_check.py")).read()
    code_prefix = code[:code.index("cres = {'five':")]
    code_defs = code[
        code.index("# ================= spec 4.5: pattern loader and matcher ================="):
        code.index("# ================= 12.8: exact lower check")
    ]
    ns = {"__name__": "__main__", "__file__": os.path.join(wdir, "out", "job31", "st21_check.py")}
    with redirect_stdout(io.StringIO()):
        exec(compile(code_prefix + "\n" + code_defs, "st21_check.py", "exec"), ns)

    # Load wlp3r6 definitions to generate SF and get NY, ix, I6B, TRI, states, BIGSTATE
    src = open(os.path.join(wdir, "wlp3r6.py")).read().replace(
        "os.path.abspath(__file__)", repr(os.path.join(wdir, "wlp3r6.py")), 1
    )
    sys.argv = ["wlp3r6", "tag=s16chk", "dmaxp=17"] + ns["ARGS"]
    ns_wlp = {"__name__": "studio_wlp3r6"}
    with redirect_stdout(io.StringIO()):
        exec(src[:src.index("DS, DSF = list(range(7, 13))")], ns_wlp)
    if "SEPX" in ns_wlp and ns_wlp["SEPX"].poll() is None:
        ns_wlp["SEPX"].stdin.close()
        ns_wlp["SEPX"].wait()
    ns["WLP"] = ns_wlp
    return ns


class FastSeparatorTables:
    """Precomputes cell->signature mappings so binary tables for sep3r_l3q build in ~0.05s per round."""

    def __init__(self, ns, use_unc: bool, use_2126: bool, tag: str, extra_rules_path: str = None):
        self.ns = ns
        self.use_unc = use_unc
        self.use_2126 = use_2126
        self.tag = tag
        self.extra_rules_path = extra_rules_path
        self.LET = ns["LET"]
        self.AP = ns["AP"]
        self.canon = ns["canon"]
        self.isR6 = ns["isR6"]
        self.pmask = ns["pmask"]
        self.sig2_of = ns["sig2_of"]
        self.ap = ns["ap"]
        self.cand2 = ns["cand2"]
        self.h2_of = ns["h2_of"]
        self.key_receiver = ns["key_receiver"]
        self.MASK = ns["MASK"]
        self.MASK8 = ns["MASK8"]
        self.val = ns["val"]
        self.UNC_tuples = {self.canon(tuple(int(ch) for ch in w)) for w in ns["UNC"]}
        self.is_rsst_2_126 = lambda w: any(
            w[i] == 5 and w[(i + 1) % 6] == 6 and w[(i + 2) % 6] == 5 for i in range(6)
        )

        wlp = ns["WLP"]
        self.SF = wlp["SF"]
        self.NY = wlp["NY"]
        self.ix = wlp["ix"]
        self.I6B = wlp["I6B"]
        self.N6B = wlp["N6B"]
        self.OMAX = wlp["OMAX"]

        os.makedirs("/tmp/sep_tables", exist_ok=True)
        self.ex6f = f"/tmp/sep_tables/ex6_{tag}.bin"
        self.rtf = f"/tmp/sep_tables/rtab_{tag}.bin"
        self.l3f = f"/tmp/sep_tables/l3q_{tag}.bin"
        self.l8f = f"/tmp/sep_tables/l3q8_{tag}.bin"
        self.fbf = f"/tmp/sep_tables/fb_{tag}.bin"
        self.fxf = f"/tmp/sep_tables/fullx_{tag}.txt"
        self.f2bf = f"/tmp/sep_tables/f2b_{tag}.bin" if extra_rules_path else None

        with open(self.fxf, "w") as f:
            f.write("\n".join(ns["FULLX"]) + "\n")

        # Write static zero FB table (since fb6/fb7 == 0.0)
        fbrel = np.zeros((3, 125, 25), dtype="<f8")
        fbx = np.zeros((3,) + (5,) * 9, dtype="<f8")
        with open(self.fbf, "wb") as f:
            f.write(fbrel.tobytes())
            f.write(fbx.tobytes())

        # Precompute EX6 cell -> sg index mapping
        t0 = time.time()
        sg_to_idx = {}
        self.unique_sgs = []
        self.sg_cands = []
        cell_sg_idx = np.full((3,) + (5,) * 8, -1, dtype=np.int32)
        pmask8_arr = np.zeros((3,) + (5,) * 8, dtype=np.uint8)

        for ui, U in enumerate((7, 8, 9)):
            K_u = ns["KT"][U]
            # Vectorized pmask computation over (5,)*8
            pm = np.zeros((5,) * 8, dtype=np.int32)
            for b in range(5):
                pm |= (~K_u[..., b]).astype(np.int32) << b
            pmask8_arr[ui] = pm.astype(np.uint8)
            for ix8 in itertools.product(range(5), repeat=8):
                wm2, wm1, wp1, wp2, sm2, sm1, s0, sp1 = (q + 5 for q in ix8)
                mk = int(pm[ix8])
                sg = self.sig2_of(U, wp1, s0, sm1, wm1, self.ap(wp2), self.ap(wm2)) + (mk,)
                idx = sg_to_idx.get(sg)
                if idx is None:
                    cands = [
                        hk
                        for hk in self.cand2(sg)
                        if not (self.use_unc and self.canon(hk[:6]) in self.UNC_tuples)
                        and not (self.use_2126 and self.is_rsst_2_126(hk[:6]))
                    ]
                    if cands:
                        idx = len(self.unique_sgs)
                        sg_to_idx[sg] = idx
                        self.unique_sgs.append(sg)
                        self.sg_cands.append(cands)
                    else:
                        idx = -1
                        sg_to_idx[sg] = -1
                cell_sg_idx[(ui,) + ix8] = idx
        self.cell_sg_idx = cell_sg_idx

        # Precompute V6B candidate lists per i6
        self.v6b_cands = [[] for _ in range(self.N6B)]
        for k6, i6 in self.I6B.items():
            if (self.use_unc and self.canon(k6) in self.UNC_tuples) or (
                self.use_2126 and self.is_rsst_2_126(k6)
            ):
                continue
            self.v6b_cands[i6] = [self.h2_of(k6, a, b) for a in self.AP for b in self.AP]

        # Precompute REX_ keys
        self.rex_keys = []
        for wm1, w0, wp1, wp2, sm1, sp1 in itertools.product(self.LET, repeat=6):
            self.rex_keys.append(self.key_receiver([wm1, w0, wp1, wp2], [sm1, 5, sp1, 5], 1))

        # Precompute static F2B tables if extra_rules_path is set
        if self.extra_rules_path is not None:
            hk_to_idx = {}
            self.unique_hks = []
            h2_cands_idx = np.full((3, 5, 5, 5, 5, 2, 2, 5), -1, dtype=np.int32)
            for ui, U in enumerate((7, 8, 9)):
                for wm1, sm1, s0, wp1 in itertools.product(range(5), repeat=4):
                    for ap_m2 in (0, 1):
                        for ap_p2 in (0, 1):
                            ar = 7 if ap_p2 else 5
                            al = 7 if ap_m2 else 5
                            for b in range(5):
                                k6 = (U, wp1 + 5, s0 + 5, b + 5, sm1 + 5, wm1 + 5)
                                if self.isR6(k6):
                                    continue
                                if self.use_unc and self.canon(k6) in self.UNC_tuples:
                                    continue
                                if self.use_2126 and self.is_rsst_2_126(k6):
                                    continue
                                hk = self.h2_of(k6, ar, al)
                                h_idx = hk_to_idx.get(hk)
                                if h_idx is None:
                                    h_idx = len(self.unique_hks)
                                    hk_to_idx[hk] = h_idx
                                    self.unique_hks.append(hk)
                                h2_cands_idx[ui, wm1, sm1, s0, wp1, ap_m2, ap_p2, b] = h_idx
            self.h2_cands_idx = h2_cands_idx

            l3_mk0 = np.zeros(31250, dtype=np.uint8)
            for (sg_, c_, a_, w2_, w3_, w4_, o_), m_ in self.MASK.items():
                idx = ((((((0 if sg_ == 1 else 1) * 5 + c_ - 5) * 5 + a_ - 5) * 5 + w2_ - 5) * 5 + w3_ - 5) * 5 + w4_ - 5) * 5 + o_ - 5
                l3_mk0[idx] = int(m_)
            l8_mk0 = np.zeros(31250, dtype=np.uint8)
            for (sg_, c_, a_, w2_, w3_, w4_, o_), m_ in self.MASK8.items():
                idx = ((((((0 if sg_ == 1 else 1) * 5 + c_ - 5) * 5 + a_ - 5) * 5 + w2_ - 5) * 5 + w3_ - 5) * 5 + w4_ - 5) * 5 + o_ - 5
                l8_mk0[idx] = int(m_)

            def serialize_rule_buckets(rlist, d_val: int) -> bytes:
                bucket_maps = [{} for _ in range(25)]
                for p_deg, w_req, s_req in rlist:
                    kill_bit = 1 << (int(p_deg) - 5)
                    forb_w = 0
                    for off, allowed in w_req:
                        off_mod = (int(off) % d_val + d_val) % d_val
                        allowed_bits = sum(1 << (int(x) - 5) for x in allowed)
                        forb_w |= ((~allowed_bits) & 31) << (5 * off_mod)
                    forb_s = 0
                    s_dict = {}
                    for off, req_s in s_req:
                        s_dict[int(off)] = int(req_s) - 5
                        off_mod = (int(off) % d_val + d_val) % d_val
                        allowed_bits = 1 << (int(req_s) - 5)
                        forb_s |= ((~allowed_bits) & 31) << (5 * off_mod)
                    req_sm1 = s_dict.get(-1, s_dict.get(d_val - 1))
                    req_s0 = s_dict.get(0)
                    sm1_range = [req_sm1] if req_sm1 is not None else range(5)
                    s0_range = [req_s0] if req_s0 is not None else range(5)
                    for sm1 in sm1_range:
                        for s0 in s0_range:
                            b_idx = sm1 * 5 + s0
                            key = (forb_w, forb_s)
                            bucket_maps[b_idx][key] = bucket_maps[b_idx].get(key, 0) | kill_bit
                chunks = []
                for b_idx in range(25):
                    items = sorted(bucket_maps[b_idx].items())
                    chunks.append(np.array([len(items)], dtype="<u4").tobytes())
                    if items:
                        arr = np.array([(fw, fs, km) for (fw, fs), km in items], dtype="<u8")
                        chunks.append(arr.tobytes())
                return b"".join(chunks)

            rules_data = json.load(open(self.extra_rules_path))
            rule_bytes = b"".join([
                serialize_rule_buckets(rules_data["d7_w6"], 7),
                serialize_rule_buckets(rules_data["d8_w6"], 8),
                serialize_rule_buckets(rules_data["d9_w6"], 9),
                serialize_rule_buckets(rules_data["d7_w7"]["1"], 7),
                serialize_rule_buckets(rules_data["d7_w7"]["-1"], 7),
                serialize_rule_buckets(rules_data["d8_w7"]["1"], 8),
                serialize_rule_buckets(rules_data["d8_w7"]["-1"], 8),
            ])
            self.static_f2b_bytes = (
                pmask8_arr.tobytes()
                + l3_mk0.tobytes()
                + l8_mk0.tobytes()
                + rule_bytes
            )

        print(
            f"  [FastSeparatorTables:{tag}] Precomputed {len(self.unique_sgs):,d} active 6-window signatures in {time.time() - t0:.2f}s"
        )

    def get_v(self, sol_map, k):
        return sol_map[k] if (sol_map is not None and k in sol_map) else float(self.val(k))

    @staticmethod
    def tauo_to_tau(t: int) -> int:
        hi = t % 3125
        lo = (t // 3125) % 3125
        fti = t // (3125 * 3125)
        s1 = lo // 25
        s2 = hi // 25
        return (fti * 125 + min(s1, s2)) * 125 + max(s1, s2)

    def coarse_tau_windows(self, tau_c: int):
        xo_q = self.ns["xo_q"]
        s2_c = tau_c % 125
        s1_c = (tau_c // 125) % 125
        fi, ti = divmod(tau_c // 15625, 3)
        fl, tl = 7 + fi, 7 + ti
        T1 = ((s1_c // 25) + 5, ((s1_c // 5) % 5) + 5, (s1_c % 5) + 5)
        T2 = ((s2_c // 25) + 5, ((s2_c // 5) % 5) + 5, (s2_c % 5) + 5)
        out = set()
        for role, (V_, U_) in (("in", (fl, tl)), ("out", (tl, fl))):
            for P_, M_ in ((T1, T2), (T2, T1)):
                if role == "in":
                    ep, sp, fp = P_
                    bm, pm, am = M_
                    for rp in (5, 6, 7, 8, 9):
                        for qm in (5, 6, 7, 8, 9):
                            wnd = (U_, am, bm, V_, ep, fp, pm, qm, rp, sp)
                            if xo_q(*wnd) is not None:
                                out.add(wnd)
                else:
                    ep, fp, rp = P_
                    bm, am, qm = M_
                    for sp in (5, 6, 7, 8, 9):
                        for pm in (5, 6, 7, 8, 9):
                            wnd = (U_, am, bm, V_, ep, fp, pm, qm, rp, sp)
                            if xo_q(*wnd) is not None:
                                out.add(wnd)
        return out

    def write_tables_and_spawn(self, sol_map, xo_mode: bool = False):
        LET = self.LET
        get_v = lambda k: self.get_v(sol_map, k)

        # 1. yv and V6B
        yv = np.zeros(self.NY, dtype=float)
        for k, idx in self.ix.items():
            yv[idx] = get_v(("y", k))

        v6b = np.zeros(self.N6B, dtype=float)
        for i6, cands in enumerate(self.v6b_cands):
            if cands:
                v6b[i6] = max(get_v(("h", hk)) for hk in cands)

        # 2. EX6
        sg_vals = np.zeros(len(self.unique_sgs) + 1, dtype="<f8")
        for idx, cands in enumerate(self.sg_cands):
            sg_vals[idx] = max(get_v(("h", hk)) for hk in cands)
        sg_vals[-1] = 0.0
        ex6_arr = sg_vals[self.cell_sg_idx]
        ex6_arr.astype("<f8").tofile(self.ex6f)

        # 3. RTAB
        rex = np.array([get_v(("r", rk)) for rk in self.rex_keys], dtype="<f8")
        rex_6d = rex.reshape(5, 5, 5, 5, 5, 5)  # wm1, w0, wp1, wp2, sm1, sp1
        rrel = np.zeros((125, 25), dtype="<f8")
        rrel[:, :5] = rex_6d.max(axis=(3, 5)).transpose(0, 3, 1, 2).reshape(125, 5)
        with open(self.rtf, "wb") as f:
            f.write(rrel.tobytes())
            f.write(rex.tobytes())

        # 4. L3Q (d=7)
        l3r = np.zeros((125, 25), dtype="<f8")
        l3x = np.zeros(31250, dtype="<f8")
        l3p = np.zeros(125, dtype="<f8")
        for c_, a_, a2 in itertools.product((5, 6), (5, 6), LET):
            l3p[((c_ - 5) * 5 + a_ - 5) * 5 + a2 - 5] = get_v(("lq", (c_, a_, a2)))
        qeff_cache = {}
        ubq = {}
        for (sg_, c_, a_, w2_, w3_, w4_, o_), m_ in self.MASK.items():
            qk = (c_, a_, m_)
            if qk not in qeff_cache:
                qeff_cache[qk] = max(
                    [get_v(("lq", (c_, a_, a2))) for a2 in LET if (m_ >> (a2 - 5)) & 1] + [0.0]
                )
            qv = qeff_cache[qk]
            ubq[(c_, a_)] = max(ubq.get((c_, a_), 0.0), qv)
            idx = ((((((0 if sg_ == 1 else 1) * 5 + c_ - 5) * 5 + a_ - 5) * 5 + w2_ - 5) * 5 + w3_ - 5) * 5 + w4_ - 5) * 5 + o_ - 5
            l3x[idx] = qv
        ub = lambda c_, a_: ubq.get((c_, a_), 0.0) if c_ in (5, 6) and a_ in (5, 6) else 0.0
        for wm1, sm1, s0, wp1 in itertools.product(LET, repeat=4):
            l3r[(wm1 - 5) * 25 + (sm1 - 5) * 5 + 2, (s0 - 5) * 5 + (wp1 - 5)] = ub(wp1, s0) + ub(wm1, sm1)
        with open(self.l3f, "wb") as f:
            f.write(l3r.tobytes())
            f.write(l3x.tobytes())
            f.write(l3p.tobytes())

        # 5. L3Q8 (d=8 / V=8)
        l8r = np.zeros((125, 25), dtype="<f8")
        l8x = np.zeros(31250, dtype="<f8")
        l8p = np.zeros(125, dtype="<f8")
        for c_, a_, a2 in itertools.product((5, 6), (5, 6), LET):
            l8p[((c_ - 5) * 5 + a_ - 5) * 5 + a2 - 5] = get_v(("lq", (8, c_, a_, a2)))
        qeff8_cache = {}
        ubq8 = {}
        for (sg_, c_, a_, w2_, w3_, w4_, o_), m_ in self.MASK8.items():
            qk = (8, c_, a_, m_)
            if qk not in qeff8_cache:
                qeff8_cache[qk] = max(
                    [get_v(("lq", (8, c_, a_, a2))) for a2 in LET if (m_ >> (a2 - 5)) & 1] + [0.0]
                )
            qv = qeff8_cache[qk]
            ubq8[(c_, a_)] = max(ubq8.get((c_, a_), 0.0), qv)
            idx = ((((((0 if sg_ == 1 else 1) * 5 + c_ - 5) * 5 + a_ - 5) * 5 + w2_ - 5) * 5 + w3_ - 5) * 5 + w4_ - 5) * 5 + o_ - 5
            l8x[idx] = qv
        ub8 = lambda c_, a_: ubq8.get((c_, a_), 0.0) if c_ in (5, 6) and a_ in (5, 6) else 0.0
        for wm1, sm1, s0, wp1 in itertools.product(LET, repeat=4):
            l8r[(wm1 - 5) * 25 + (sm1 - 5) * 5 + 2, (s0 - 5) * 5 + (wp1 - 5)] = ub8(wp1, s0) + ub8(wm1, sm1)
        with open(self.l8f, "wb") as f:
            f.write(l8r.tobytes())
            f.write(l8x.tobytes())
            f.write(l8p.tobytes())

        # 6. F2B (exact full2ball leaf adjustment table)
        if self.f2bf is not None:
            hk_vals = np.zeros(len(self.unique_hks) + 1, dtype="<f8")
            for idx, hk in enumerate(self.unique_hks):
                hk_vals[idx] = get_v(("h", hk))
            hk_vals[-1] = 0.0
            h2_tab = hk_vals[self.h2_cands_idx].astype("<f8")
            with open(self.f2bf, "wb") as f:
                f.write(h2_tab.tobytes())
                f.write(self.static_f2b_bytes)

        # 7. xv dict and optional XO=1 (SEP_FB6) 9-slot window table
        x_keys = set(self.ns["X"].keys())
        has_xo = False
        if sol_map is not None:
            x_keys |= {k[1] for k in sol_map if k[0] == "x"}
            has_xo = any(k[0] == "xo" for k in sol_map)
        xv = {tq: get_v(("x", tq)) for tq in x_keys if get_v(("x", tq)) > 1e-12}

        if xo_mode or has_xo:
            xo_q = self.ns["xo_q"]
            xo_cands = self.ns["xo_cands"]
            xov = {k[1]: float(v) for k, v in (sol_map or {}).items() if k[0] == "xo"}
            split_coarse = {self.tauo_to_tau(t_o) for t_o in xov}
            active_coarse = set(xv.keys()) | split_coarse
            get_xo_val = lambda t_o: xov[t_o] if t_o in xov else xv.get(self.tauo_to_tau(t_o), 0.0)
            xq_cache = {}
            fbrel = np.zeros((3, 125, 25), dtype="<f8")
            fbx = np.zeros((3,) + (5,) * 9, dtype="<f8")
            seen_w = set()
            for tau_c in active_coarse:
                for wnd in self.coarse_tau_windows(tau_c):
                    if wnd in seen_w:
                        continue
                    seen_w.add(wnd)
                    U, wm2, wm1, w0, wp1, wp2, sm2, sm1, s0, sp1 = wnd
                    qk = xo_q(*wnd)
                    if qk is None:
                        continue
                    if qk not in xq_cache:
                        xq_cache[qk] = max(get_xo_val(ti_o) - get_xo_val(to_o) for _, _, ti_o, to_o in xo_cands(qk))
                    v = xq_cache[qk]
                    if v == 0.0:
                        continue
                    ui = U - 7
                    fbx[ui, wm2 - 5, wm1 - 5, w0 - 5, wp1 - 5, wp2 - 5, sm2 - 5, sm1 - 5, s0 - 5, sp1 - 5] = v
                    s_idx = (wm1 - 5) * 25 + (sm1 - 5) * 5 + (w0 - 5)
                    a_idx = (s0 - 5) * 5 + (wp1 - 5)
                    if v > fbrel[ui, s_idx, a_idx]:
                        fbrel[ui, s_idx, a_idx] = v
            with open(self.fbf, "wb") as f:
                f.write(fbrel.tobytes())
                f.write(fbx.tobytes())
            xv = {}
            self._fb_dirty = True
        elif getattr(self, "_fb_dirty", False):
            fbrel = np.zeros((3, 125, 25), dtype="<f8")
            fbx = np.zeros((3,) + (5,) * 9, dtype="<f8")
            with open(self.fbf, "wb") as f:
                f.write(fbrel.tobytes())
                f.write(fbx.tobytes())
            self._fb_dirty = False

        sepenv = dict(
            os.environ,
            SEP_NODELIMIT="0",
            SEP_ARRKEY="1",
            SEP_EXACT6=self.ex6f,
            SEP_RTAB=self.rtf,
            SEP_FULLX=self.fxf,
            SEP_L3Q=self.l3f,
            SEP_L3Q8=self.l8f,
            SEP_FB6=self.fbf,
        )
        if self.f2bf is not None:
            sepenv["SEP_F2B"] = self.f2bf
        proc = subprocess.Popen(
            [os.path.join(GDIR, "bin", "sep3r_l3q"), self.SF],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            env=sepenv,
        )
        return proc, yv, xv, v6b

    def query_sepx(self, proc, d: int, yv, xv, v6b, thr: float, cap: int = 5000):
        xs = [(tau, v) for tau, v in xv.items() if v > 1e-12]
        cmd = "q %d %.12f %d %d\n%s\nX %d %s\nR %d %s\n" % (
            d,
            thr,
            cap,
            self.OMAX,
            " ".join("%.12f" % x for x in yv),
            len(xs),
            " ".join("%d %.12f" % kv for kv in xs),
            self.N6B,
            " ".join("%.12f" % x for x in v6b),
        )
        proc.stdin.write(cmd)
        proc.stdin.flush()
        out = []
        while True:
            line = proc.stdout.readline()
            if not line:
                raise RuntimeError("sep3r_l3q terminated unexpectedly")
            f = line.split()
            if f[0] == "END":
                return out, int(f[2])
            out.append((float(f[1]), f[2], f[3]))


def make_recv_spec_full2ball(ns, extra_rules_path: str):
    """Build a cached recv_spec function incorporating full-wheel 2-ball single-slot private kills."""
    rules_data = json.load(open(extra_rules_path))

    def index_rules(rlist):
        by_s = collections.defaultdict(list)
        for p_deg, w_req, s_req in rlist:
            mask = 1 << (int(p_deg) - 5)
            w_t = tuple((int(idx), tuple(int(x) for x in allowed)) for idx, allowed in w_req)
            s_t = tuple((int(idx), int(val)) for idx, val in s_req)
            s_dict = dict(s_t)
            s_other = tuple((idx, val) for idx, val in s_t if idx not in (0, -1))
            by_s[(s_dict.get(-1), s_dict.get(0))].append((w_t, s_other, mask))
        return by_s

    rules_d7_w6 = index_rules(rules_data["d7_w6"])
    rules_d7_w7_p1 = index_rules(rules_data["d7_w7"]["1"])
    rules_d7_w7_m1 = index_rules(rules_data["d7_w7"]["-1"])
    rules_d8_w6 = index_rules(rules_data["d8_w6"])
    rules_d8_w7_p1 = index_rules(rules_data["d8_w7"]["1"])
    rules_d8_w7_m1 = index_rules(rules_data["d8_w7"]["-1"])
    rules_d9_w6 = index_rules(rules_data["d9_w6"])

    pmask = ns["pmask"]
    sig2_of = ns["sig2_of"]
    ap = ns["ap"]
    cand2 = ns["cand2"]
    key_receiver = ns["key_receiver"]
    root5 = ns["root5"]
    tau = ns["tau"]
    side = ns["side"]
    MASK = ns["MASK"]
    MASK8 = ns["MASK8"]
    base_recv_spec = ns["recv_spec"]
    spec_cache = {}

    def match_extra_fast(d: int, w, s, i: int, rule_idx_map) -> int:
        sm1 = s[(i - 1) % d]
        s0 = s[i]
        extra = 0
        for key in ((sm1, s0), (sm1, None), (None, s0), (None, None)):
            cands = rule_idx_map.get(key)
            if not cands:
                continue
            for w_t, s_other, mask in cands:
                if (extra & mask) == mask:
                    continue
                ok = True
                for off, allowed in w_t:
                    if w[(i + off) % d] not in allowed:
                        ok = False
                        break
                if not ok:
                    continue
                for off, deg_req in s_other:
                    if s[(i + off) % d] != deg_req:
                        ok = False
                        break
                if ok:
                    extra |= mask
        return extra

    def recv_spec_full2ball(d: int, link: str, sword: str):
        ck = (d, link, sword)
        res = spec_cache.get(ck)
        if res is not None:
            return res
        U = min(d, 9)
        w = [int(ch) for ch in link]
        s = [int(ch) for ch in sword]
        W = lambda k: w[k % d]
        S = lambda k: s[k % d]
        r = {}
        r_w6 = rules_d7_w6 if d == 7 else (rules_d8_w6 if d == 8 else rules_d9_w6)
        for i in range(d):
            if s[i] == 5:
                k_ = ("r", key_receiver(w, s, i))
                r[k_] = r.get(k_, 0) + 1
            if w[i] == 5:
                k_ = ("y", root5((U, W(i + 1), S(i), S(i - 1), W(i - 1))))
                r[k_] = r.get(k_, 0) + 1
            elif w[i] == 6:
                mk = pmask(U, W(i - 2), W(i - 1), W(i + 1), W(i + 2), S(i - 2), S(i - 1), S(i), S(i + 1))
                if d <= 9:
                    mk &= ~match_extra_fast(d, w, s, i, r_w6)
                sg = sig2_of(U, W(i + 1), S(i), S(i - 1), W(i - 1), ap(W(i + 2)), ap(W(i - 2))) + (mk,)
                if cand2(sg):
                    r[("M", sg)] = r.get(("M", sg), 0) + 1
            else:
                ti = tau(w[i], U, side(W(i - 1), S(i - 1), W(i - 2)), side(W(i + 1), S(i), W(i + 2)))
                to = tau(U, w[i], side(W(i - 1), W(i - 2), S(i - 1)), side(W(i + 1), W(i + 2), S(i)))
                r[("x", ti)] = r.get(("x", ti), 0) + 1
                r[("x", to)] = r.get(("x", to), 0) - 1
        if d == 7:
            for i in range(d):
                if w[i] == 7:
                    for sg_ in (1, -1):
                        key = (W(i + sg_), W(i + 2 * sg_), W(i + 3 * sg_))
                        if key[0] in (5, 6) and key[1] in (5, 6):
                            r[("lq", key)] = r.get(("lq", key), 0) - 1
                        c_, a_, o_ = W(i + sg_), (S(i) if sg_ == 1 else S(i - 1)), (S(i - 1) if sg_ == 1 else S(i))
                        if c_ in (5, 6) and a_ in (5, 6):
                            m_ = MASK[(sg_, c_, a_, W(i + 2 * sg_), W(i + 3 * sg_), W(i + 4 * sg_), o_)]
                            r_w7 = rules_d7_w7_p1 if sg_ == 1 else rules_d7_w7_m1
                            m_ &= ~match_extra_fast(d, w, s, i, r_w7)
                            r[("lQ", (c_, a_, m_))] = r.get(("lQ", (c_, a_, m_)), 0) + 1
                elif w[i] == 8:
                    for sg_ in (1, -1):
                        key = (8, W(i + sg_), W(i + 2 * sg_), W(i + 3 * sg_))
                        if key[1] in (5, 6) and key[2] in (5, 6):
                            r[("lq", key)] = r.get(("lq", key), 0) - 1
        elif d == 8:
            for i in range(d):
                if w[i] == 7:
                    for sg_ in (1, -1):
                        c_, a_, o_ = W(i + sg_), (S(i) if sg_ == 1 else S(i - 1)), (S(i - 1) if sg_ == 1 else S(i))
                        if c_ in (5, 6) and a_ in (5, 6):
                            m_ = MASK8[(sg_, c_, a_, W(i + 2 * sg_), W(i + 3 * sg_), W(i + 4 * sg_), o_)]
                            r_w7 = rules_d8_w7_p1 if sg_ == 1 else rules_d8_w7_m1
                            m_ &= ~match_extra_fast(d, w, s, i, r_w7)
                            r[("lQ", (8, c_, a_, m_))] = r.get(("lQ", (8, c_, a_, m_)), 0) + 1
        res = {k: v for k, v in r.items() if v != 0}
        spec_cache[ck] = res
        return res

    return recv_spec_full2ball


def eval_row_exact(
    ns,
    d: int,
    lk: str,
    sv: str,
    sol_map,
    use_unc: bool,
    use_2126: bool,
    h_max_cache: dict,
    lq_max_cache: dict,
    recv_spec_fn=None,
) -> float:
    LET = ns["LET"]
    cand2 = ns["cand2"]
    canon = ns["canon"]
    val = ns["val"]
    UNC_tuples = {canon(tuple(int(ch) for ch in w)) for w in ns["UNC"]}
    is_rsst_2_126 = lambda w: any(
        w[i] == 5 and w[(i + 1) % 6] == 6 and w[(i + 2) % 6] == 5 for i in range(6)
    )
    get_v = lambda k: sol_map[k] if (sol_map is not None and k in sol_map) else float(val(k))

    r = (recv_spec_fn if recv_spec_fn is not None else ns["recv_spec"])(d, lk, sv)
    tot = 0.0
    for k, cf in r.items():
        if k[0] == "fb":
            continue
        elif k[0] == "M":
            sg = k[1]
            if sg not in h_max_cache:
                cands = [
                    get_v(("h", hk))
                    for hk in cand2(sg)
                    if not (use_unc and canon(hk[:6]) in UNC_tuples)
                    and not (use_2126 and is_rsst_2_126(hk[:6]))
                ]
                h_max_cache[sg] = max(cands) if cands else 0.0
            v_k = h_max_cache[sg]
        elif k[0] == "lQ":
            qk = k[1]
            if qk not in lq_max_cache:
                m_ = qk[-1]
                prefix = qk[:-1]
                cands = [get_v(("lq", prefix + (a2_,))) for a2_ in LET if (m_ >> (a2_ - 5)) & 1]
                lq_max_cache[qk] = max(cands) if cands else 0.0
            v_k = lq_max_cache[qk]
        else:
            v_k = get_v(k)
        tot += cf * v_k
    return tot


_STAGE3_CTX = {}


def _eval_single_stage3_row(r_key):
    P = _STAGE3_CTX["P"]
    rsst_rules = _STAGE3_CTX["rsst_rules"]
    nl26_rules = _STAGE3_CTX["nl26_rules"]
    KT7_B = _STAGE3_CTX["KT7_B"]
    KT9_B = _STAGE3_CTX["KT9_B"]
    grow = _STAGE3_CTX["grow"]
    cfgs_rsst_all = _STAGE3_CTX["cfgs_rsst_all"]

    d, lk_s, sv_s = r_key
    lk = [int(ch) for ch in lk_s]
    sw = [int(ch) for ch in sv_s]
    lk_win = [min(x, 8) for x in lk]
    w_win = P.Window(d, lk_win, sw)
    for i_w, deg_w in enumerate(lk):
        if deg_w >= 9:
            w_win.deg[("w", i_w)] = deg_w
            w_win._rot[("w", i_w)] = (
                "path",
                [
                    ("p", i_w, 3),
                    ("s", i_w),
                    ("w", (i_w + 1) % d),
                    ("u",),
                    ("w", (i_w - 1) % d),
                    ("s", (i_w - 1) % d),
                    ("p", i_w, 1),
                ],
            )
    m_priv = len(w_win.priv)
    raw = P.rsst_instances(w_win, rsst_rules, [("u",)] + [("w", i) for i in range(d)])
    agg = collections.defaultdict(list)
    for nm, h, tg, al in raw:
        agg[(nm, h, tg)].append(al)
    inst_r = [(nm, h, tg, 1, als) for (nm, h, tg), als in agg.items()]
    pairs_u = [(("u",), x) for x in w_win.rot(("u",))[1]] + [(x, ("u",)) for x in w_win.rot(("u",))[1]]
    inst_n = P.nl_instances(w_win, nl26_rules, pairs_u)

    # Fast active-private projection check for unfiltered_ok
    u_v = ("u",)
    act_p = sorted({v for _, a, b, _, alts in inst_r + inst_n if u_v in (a, b) for al in alts for v in al.c})
    m_act = len(act_p)
    F_act = np.array(list(itertools.product(range(6, 10), repeat=m_act)), dtype=np.int8).reshape((4 ** m_act, m_act))
    F_sub = np.full((len(F_act), m_priv), 6, dtype=np.int8)
    for j_act, v_p in enumerate(act_p):
        F_sub[:, w_win.priv.index(v_p)] = F_act[:, j_act]
    lo_r_sub, _, _ = P.u_ledger(w_win, F_sub, inst_r)
    lo_n_sub, _, _ = P.u_ledger(w_win, F_sub, inst_n)
    if not ((lo_r_sub > 0).any() or (lo_n_sub > 0).any()):
        return r_key, "unfiltered"

    # Full F6 check for non-unfiltered rows
    F6 = np.array(list(itertools.product(range(6, 10), repeat=m_priv)), dtype=np.int8).reshape((4 ** m_priv, m_priv))
    lo_r, _, _ = P.u_ledger(w_win, F6, inst_r)
    lo_n, _, _ = P.u_ledger(w_win, F6, inst_n)
    pos_mask = (lo_r > 0) | (lo_n > 0)
    if not pos_mask.any():
        return r_key, "unfiltered"

    F6_pos = F6[pos_mask]
    surv = np.ones(len(F6_pos), dtype=bool)
    col_map = {nm: idx_c for idx_c, nm in enumerate(w_win.priv)}
    KT_u = KT7_B if d == 7 else KT9_B
    if 9 not in lk:
        for i in range(d):
            if lk[i] == 6 and ("p", i, 1) in col_map:
                wm2, wm1, wp1, wp2 = lk[(i - 2) % d], lk[(i - 1) % d], lk[(i + 1) % d], lk[(i + 2) % d]
                sm2, sm1, s0, sp1 = sw[(i - 2) % d], sw[(i - 1) % d], sw[i], sw[(i + 1) % d]
                K_vec = KT_u[wm2 - 5, wm1 - 5, wp1 - 5, wp2 - 5, sm2 - 5, sm1 - 5, s0 - 5, sp1 - 5]
                for b_idx in range(5):
                    if K_vec[b_idx]:
                        surv &= ~(F6_pos[:, col_map[("p", i, 1)]] == (b_idx + 5))
    if not surv.any():
        return r_key, [d, lk_s, sv_s, "kt_only", []]

    grow.D = d
    grow.LK = lk_win
    grow.SV = {j: sv_v for j, sv_v in enumerate(sw)}
    VAR = list(w_win.priv)
    grow.VAR = VAR
    r2_base = {("s", j): sv_v for j, sv_v in enumerate(sw)}
    for nm in VAR:
        r2_base[nm] = 6
    adj, name, faces = grow.build2(r2_base)
    inv = {v: x for x, v in name.items()}
    P_v = [x for x in inv]
    pa = {x: {name[y] for y in adj[inv[x]] if y in name} for x in P_v}
    pf = {frozenset(name[y] for y in f) for f in faces if all(y in name for y in f)}
    fd = {}
    if d <= 8:
        fd[("u",)] = d
    for i in range(d):
        if lk[i] <= 8:
            fd[("w", i)] = lk[i]
    for j, v in grow.SV.items():
        if v <= 8:
            fd[("s", j)] = v
    used_cfgs = []
    for c_idx, c_cfg in enumerate(cfgs_rsst_all):
        killed_any = False
        for emb in grow.embeddings(c_cfg, P_v, pa, pf, fd):
            phi = dict(emb)
            if any(v not in fd and v not in VAR for v in phi.values()):
                continue
            req_d = {v: c_cfg[3][u] for u, v in emb if v in VAR}
            m_req = np.ones(len(F6_pos), dtype=bool)
            for nm, deg_req in req_d.items():
                m_req &= (F6_pos[:, col_map[nm]] == deg_req)
            if (surv & m_req).any():
                surv &= ~m_req
                killed_any = True
        if killed_any:
            used_cfgs.append(c_idx)
        if not surv.any():
            break
    assert not surv.any(), f"Row {(d, lk_s, sv_s)} failed Stage 3 2-ball closure!"
    return r_key, [d, lk_s, sv_s, "grow", used_cfgs]


def compute_stage3_closure(results_summary: dict, all_pool_set: set, prev_data: dict = None) -> dict:
    """Verify Stage 3 exhaustive private-filling closure across all positive-excess rows from Step 2."""
    import multiprocessing

    union_all = set()
    for t_nm in ("tierA", "tierB", "tierB_full2ball"):
        if t_nm not in results_summary:
            continue
        for sb_nm in ("non_degrading", "buffered"):
            for d, lk, sv, _ in results_summary[t_nm][sb_nm]["pos_rows"]:
                union_all.add((int(d), lk, sv))

    union_all_sorted = sorted(union_all)
    union_pool_sorted = [r for r in union_all_sorted if r in all_pool_set]

    existing_stage3 = prev_data.get("stage3_closure") if prev_data else None
    if (
        existing_stage3 is not None
        and existing_stage3.get("u_all_count") == len(union_all_sorted)
        and existing_stage3.get("u_pool_count") == len(union_pool_sorted)
    ):
        return existing_stage3

    cache_path = os.path.join(GDIR, "stage3_row_cache.json")
    prev_cache = {}
    if os.path.exists(cache_path):
        try:
            raw_c = json.load(open(cache_path))
            for k_s, v_c in raw_c.items():
                d_s, lk_s, sv_s = k_s.split("|")
                prev_cache[(int(d_s), lk_s, sv_s)] = v_c
        except Exception:
            prev_cache = {}

    if existing_stage3 is not None and prev_data is not None:
        prev_union = set()
        for t_nm in ("tierA", "tierB", "tierB_full2ball"):
            if t_nm not in prev_data:
                continue
            for sb_nm in ("non_degrading", "buffered"):
                if sb_nm in prev_data[t_nm]:
                    for d, lk, sv, _ in prev_data[t_nm][sb_nm]["pos_rows"]:
                        prev_union.add((int(d), lk, sv))
        if len(prev_union) == existing_stage3.get("u_all_count"):
            non_unfilt_map = {
                (int(r[0]), r[1], r[2]): [int(r[0]), r[1], r[2], r[3], list(r[4])]
                for r in existing_stage3.get("non_unfiltered_rows", [])
            }
            for r_key in prev_union:
                if r_key not in prev_cache:
                    prev_cache[r_key] = non_unfilt_map.get(r_key, "unfiltered")

    rows_to_check = [r_key for r_key in union_all_sorted if r_key not in prev_cache]
    if rows_to_check:
        sys.path.insert(0, os.path.join(WDIR, "loop", "k42"))
        os.chdir(os.path.join(WDIR, "loop", "k42"))
        import grow
        kpriv_cfgs = []
        kpriv_path = os.path.join(WDIR, "out", "job30", "kpriv.txt")
        if os.path.exists(kpriv_path):
            for l in open(kpriv_path).read().splitlines():
                if not l or l.startswith("#") or "|" not in l:
                    continue
                rhs = l.split("|")[-1].strip()
                f = rhs.split()
                if len(f) == 5 and f[1].isdigit() and f[2].isdigit() and ";" in f[3] + f[4]:
                    kpriv_cfgs.append(grow.kcline(rhs, "kpriv"))
        cfgs_rsst_all = grow.rsst() + grow.explore_kills() + kpriv_cfgs

        sys.path.insert(0, os.path.join(WDIR, "loop", "pubrules"))
        os.chdir(os.path.join(WDIR, "loop", "pubrules"))
        import pubrules as P
        rsst_rules = P.load_rsst()
        nl26_rules = P.load_nl26()
        os.chdir(WDIR)

        KT7_B = np.load(os.path.join(GDIR, "kill_upgraded", "tierB", "kill_U7.npy"))
        KT9_B = np.load(os.path.join(GDIR, "kill_upgraded", "tierB", "kill_U9.npy"))

        _STAGE3_CTX.update(
            P=P,
            rsst_rules=rsst_rules,
            nl26_rules=nl26_rules,
            KT7_B=KT7_B,
            KT9_B=KT9_B,
            grow=grow,
            cfgs_rsst_all=cfgs_rsst_all,
        )
        t_s3 = time.time()
        print(f"\n  [Stage 3 Closure] Evaluating {len(rows_to_check):,d} new positive-excess rows across 12 workers...")
        ctx = multiprocessing.get_context("fork")
        with ctx.Pool(processes=min(12, os.cpu_count() or 8)) as pool:
            for r_key, res_v in pool.imap_unordered(_eval_single_stage3_row, rows_to_check, chunksize=32):
                prev_cache[r_key] = res_v
        print(f"  [Stage 3 Closure] Evaluated {len(rows_to_check):,d} rows in {time.time() - t_s3:.2f}s")
        serial_cache = {f"{d}|{lk}|{sv}": v for (d, lk, sv), v in sorted(prev_cache.items())}
        with open(cache_path, "w") as f:
            json.dump(serial_cache, f)

    u_pool_f6 = 0
    u_pool_unfilt = 0
    u_pool_kt = 0
    u_pool_grow = 0
    u_all_f6 = 0
    u_all_unfilt = 0
    u_all_kt = 0
    u_all_grow = 0
    non_unfiltered_rows = []

    for r_key in union_all_sorted:
        d, lk_s, sv_s = r_key
        in_pool = r_key in all_pool_set
        cached = prev_cache[r_key]
        n_f6 = 4 ** sum({5: 0, 6: 1, 7: 2}.get(min(int(ch), 8), 3) for ch in lk_s)
        u_all_f6 += n_f6
        if in_pool:
            u_pool_f6 += n_f6
        if cached == "unfiltered":
            u_all_unfilt += 1
            if in_pool:
                u_pool_unfilt += 1
        else:
            non_unfiltered_rows.append(cached)
            if cached[3] == "kt_only":
                u_all_kt += 1
                if in_pool:
                    u_pool_kt += 1
            else:
                u_all_grow += 1
                if in_pool:
                    u_pool_grow += 1

    non_unfiltered_rows.sort(key=lambda x: (x[0], x[1], x[2]))
    return {
        "u_pool_count": len(union_pool_sorted),
        "u_pool_f6_total": u_pool_f6,
        "u_pool_unfiltered_ok": u_pool_unfilt,
        "u_pool_kt_only_ok": u_pool_kt,
        "u_pool_grow_ok": u_pool_grow,
        "u_all_count": len(union_all_sorted),
        "u_all_f6_total": u_all_f6,
        "u_all_unfiltered_ok": u_all_unfilt,
        "u_all_kt_only_ok": u_all_kt,
        "u_all_grow_ok": u_all_grow,
        "non_unfiltered_rows": non_unfiltered_rows,
    }


def compute_s51_xo_closure(ns, recv_spec, base_sender_nofb, base_cons2_nofb, active_2308, persisted_cpp_rows):
    """Evaluate s51 (XO=1) outer-letter transfer refinement across the 15 d=7 binders, 2,320-row pool, xo77, and full Dantzig-Wolfe XO=1."""
    xo_q = ns["xo_q"]
    xo_cands = ns["xo_cands"]
    cand2 = ns["cand2"]
    canon = ns["canon"]
    LET = ns["LET"]
    val = ns["val"]
    T_fb = float(ns["T"])
    UNC_tuples = {canon(tuple(int(ch) for ch in w)) for w in ns["UNC"]}
    is_rsst_2_126 = lambda w: any(w[i] == 5 and w[(i + 1) % 6] == 6 and w[(i + 2) % 6] == 5 for i in range(6))

    def tauo_to_tau(t):
        hi = t % 3125
        lo = (t // 3125) % 3125
        fti = t // (3125 * 3125)
        s1 = lo // 25
        s2 = hi // 25
        return (fti * 125 + min(s1, s2)) * 125 + max(s1, s2)

    binders_15 = [
        (7, "5557666", "5776767"), (7, "5557666", "5777777"), (7, "5557766", "5775777"),
        (7, "5575766", "5777676"), (7, "5575775", "5775677"), (7, "5577557", "5757577"),
        (7, "5757577", "5577567"), (7, "5757677", "5556655"), (7, "5757757", "5755575"),
        (7, "5757767", "5575665"), (7, "5766767", "5676665"), (7, "6676666", "5665676"),
        (7, "7665566", "6675676"), (7, "7665566", "6775676"), (7, "7665566", "7765766"),
    ]

    def get_full_xo_spec(d, lk, sv):
        r = {k: v for k, v in recv_spec(d, lk, sv).items() if k[0] not in ("fb", "x")}
        w = [int(c) for c in lk]
        s = [int(c) for c in sv]
        U = min(d, 9)
        W = lambda k: w[k % d]
        S = lambda k: s[k % d]
        for i in range(d):
            if w[i] >= 7:
                qk = xo_q(U, W(i - 2), W(i - 1), w[i], W(i + 1), W(i + 2), S(i - 2), S(i - 1), S(i), S(i + 1))
                if qk is not None:
                    r[("XQ", qk)] = r.get(("XQ", qk), 0) + 1
        return {k: v for k, v in r.items() if v != 0}

    def solve_xo_subset(rows_in, sender_buffered=True):
        row_dicts = [r for _, r in base_sender_nofb]
        n_send = len(row_dicts)
        row_labels = [("senderR2", w) for w, _ in base_sender_nofb]
        m_sgs = set()
        lq_Qks = set()
        xq_Qks = set()
        cur_r = []
        seen_sk = set()
        for d, lk, sv in rows_in:
            r = get_full_xo_spec(d, lk, sv)
            sk = (d, tuple(sorted(r.items(), key=str)))
            if sk not in seen_sk:
                seen_sk.add(sk)
                cur_r.append((d, lk, sv, r))
                for k in r:
                    if k[0] == "M":
                        m_sgs.add(k[1])
                    elif k[0] == "lQ":
                        lq_Qks.add(k[1])
                    elif k[0] == "XQ":
                        xq_Qks.add(k[1])
                row_dicts.append(r)
                row_labels.append(("receiverR2", d, lk, sv))
        for qk in sorted(lq_Qks):
            m_ = qk[-1]
            prefix = qk[:-1]
            for a2_ in LET:
                if (m_ >> (a2_ - 5)) & 1:
                    row_dicts.append({("lq", prefix + (a2_,)): 1, ("lQ", qk): -1})
                    row_labels.append(("mrowL", qk))
        for sg in sorted(m_sgs):
            for hk in sorted(cand2(sg)):
                if canon(hk[:6]) in UNC_tuples or is_rsst_2_126(hk[:6]):
                    continue
                row_dicts.append({("h", hk): 1, ("M", sg): -1})
                row_labels.append(("mrowR2", sg))
        for qk in sorted(xq_Qks):
            for eA, eB, ti, to in xo_cands(qk):
                rd = {("XQ", qk): -1}
                if ti != to:
                    rd[("xo", ti)] = 1
                    rd[("xo", to)] = -1
                row_dicts.append(rd)
                row_labels.append(("mrowX", qk))
        all_cols = sorted({k for r in row_dicts + base_cons2_nofb for k in r}, key=str)
        col_idx = {k: j for j, k in enumerate(all_cols)}
        n_cols = len(all_cols) + 1
        b_ub = (
            [-1.0 if sender_buffered else (-1.0 + T_fb)] * n_send
            + [float(r[0] - 6) for r in cur_r]
            + [0.0] * (len(row_dicts) - n_send - len(cur_r))
        )
        t_coeffs = (
            [-1.0 if sender_buffered else 0.0] * n_send
            + [-1.0] * len(cur_r)
            + [0.0] * (len(row_dicts) - n_send - len(cur_r))
        )
        A_ub = lil_matrix((len(row_dicts), n_cols), dtype=float)
        for i, r in enumerate(row_dicts):
            for k, cf in r.items():
                A_ub[i, col_idx[k]] = float(cf)
            A_ub[i, n_cols - 1] = t_coeffs[i]
        A_eq = lil_matrix((len(base_cons2_nofb), n_cols), dtype=float)
        for i, r in enumerate(base_cons2_nofb):
            for k, cf in r.items():
                A_eq[i, col_idx[k]] = float(cf)
        c_clean = np.zeros(n_cols)
        c_clean[-1] = 1.0
        bounds = [
            (0.0, None)
            if k[0] in ("M", "lQ")
            else ((-3.0, 3.0) if k[0] == "XQ" else ((0.0, 3.0) if k[0] in ("x", "lq", "xo") else (0.0, None)))
            for k in all_cols
        ] + [(None, None)]
        res = linprog(
            c_clean,
            A_ub=A_ub.tocsc(),
            b_ub=np.array(b_ub),
            A_eq=A_eq.tocsc(),
            b_eq=np.zeros(len(base_cons2_nofb)),
            bounds=bounds,
            method="highs-ipm",
        )
        duals = -res.ineqlin.marginals
        act = [
            (row_labels[i][1], row_labels[i][2], row_labels[i][3], str(Fraction(duals[i]).limit_denominator(100000)))
            for i in range(len(row_labels))
            if duals[i] > 1e-7 and row_labels[i][0] == "receiverR2"
        ]
        return float(res.x[-1]), act, len(cur_r), len(xq_Qks)

    t15_bf, act15_bf, _, xq15 = solve_xo_subset(binders_15, sender_buffered=True)
    t15_nd, act15_nd, _, _ = solve_xo_subset(binders_15, sender_buffered=False)
    pool_2320 = sorted(set(active_2308) | set(binders_15))
    t2320_bf, act2320_bf, _, xq2320 = solve_xo_subset(pool_2320, sender_buffered=True)
    t2320_nd, act2320_nd, _, _ = solve_xo_subset(pool_2320, sender_buffered=False)

    all_rows = sorted(set(active_2308) | set(persisted_cpp_rows))
    row_base_info = []
    for d, lk, sv in all_rows:
        r_base = {k: v for k, v in recv_spec(d, lk, sv).items() if k[0] not in ("fb", "x")}
        w = [int(c) for c in lk]
        s = [int(c) for c in sv]
        U = min(d, 9)
        W = lambda k: w[k % d]
        S = lambda k: s[k % d]
        big_pos = []
        for i in range(d):
            if w[i] >= 7:
                ti = ns["tau"](w[i], U, ns["side"](W(i - 1), S(i - 1), W(i - 2)), ns["side"](W(i + 1), S(i), W(i + 2)))
                to = ns["tau"](U, w[i], ns["side"](W(i - 1), W(i - 2), S(i - 1)), ns["side"](W(i + 1), W(i + 2), S(i)))
                qk = xo_q(U, W(i - 2), W(i - 1), w[i], W(i + 1), W(i + 2), S(i - 2), S(i - 1), S(i), S(i + 1))
                big_pos.append((ti, to, qk, U, w[i]))
        row_base_info.append((d, lk, sv, r_base, big_pos))

    # xo77 ((U, V) = (7, 7) decoupled outer-split across all 37,376 unique specs)
    xo77_rows = []
    seen_sk77 = set()
    m_sgs77 = set()
    lq_Qks77 = set()
    xq_Qks77 = set()
    for d, lk, sv, r_base, big_pos in row_base_info:
        r = dict(r_base)
        for ti, to, qk, U, wi in big_pos:
            if U == 7 and wi == 7:
                if qk is not None:
                    r[("XQ", qk)] = r.get(("XQ", qk), 0) + 1
                    xq_Qks77.add(qk)
            elif ti != to:
                r[("x", ti)] = r.get(("x", ti), 0) + 1
                r[("x", to)] = r.get(("x", to), 0) - 1
        r = {k: v for k, v in r.items() if v != 0}
        sk = (d, tuple(sorted(r.items(), key=str)))
        if sk not in seen_sk77:
            seen_sk77.add(sk)
            xo77_rows.append((d, lk, sv, r))
            for k in r:
                if k[0] == "M":
                    m_sgs77.add(k[1])
                elif k[0] == "lQ":
                    lq_Qks77.add(k[1])
    rd77 = [r for _, r in base_sender_nofb] + [r for _, _, _, r in xo77_rows]
    n_send = len(base_sender_nofb)
    n_recv77 = len(xo77_rows)
    for qk in sorted(lq_Qks77):
        m_ = qk[-1]
        prefix = qk[:-1]
        for a2_ in LET:
            if (m_ >> (a2_ - 5)) & 1:
                rd77.append({("lq", prefix + (a2_,)): 1, ("lQ", qk): -1})
    for sg in sorted(m_sgs77):
        for hk in sorted(cand2(sg)):
            if canon(hk[:6]) in UNC_tuples or is_rsst_2_126(hk[:6]):
                continue
            rd77.append({("h", hk): 1, ("M", sg): -1})
    for qk in sorted(xq_Qks77):
        for eA, eB, ti_o, to_o in xo_cands(qk):
            rd = {("XQ", qk): -1}
            if ti_o != to_o:
                rd[("xo", ti_o)] = 1
                rd[("xo", to_o)] = -1
            rd77.append(rd)
    cols77 = sorted({k for r in rd77 + base_cons2_nofb for k in r}, key=str)
    cidx77 = {k: j for j, k in enumerate(cols77)}
    ncols77 = len(cols77) + 1
    A_eq77 = lil_matrix((len(base_cons2_nofb), ncols77), dtype=float)
    for i, r in enumerate(base_cons2_nofb):
        for k, cf in r.items():
            A_eq77[i, cidx77[k]] = float(cf)
    A_eq77_csc = A_eq77.tocsc()
    b_eq77 = np.zeros(len(base_cons2_nofb))
    c_clean77 = np.zeros(ncols77)
    c_clean77[-1] = 1.0
    xo77_res = {"unique_specs": n_recv77, "xq_keys": len(xq_Qks77), "non_degrading": {}, "buffered": {}}
    for sb_flag, sb_key in [(False, "non_degrading"), (True, "buffered")]:
        b_ub77 = (
            [-1.0 if sb_flag else (-1.0 + T_fb)] * n_send
            + [float(r[0] - 6) for r in xo77_rows]
            + [0.0] * (len(rd77) - n_send - n_recv77)
        )
        t_c77 = [-1.0 if sb_flag else 0.0] * n_send + [-1.0] * n_recv77 + [0.0] * (len(rd77) - n_send - n_recv77)
        A_ub77 = lil_matrix((len(rd77), ncols77), dtype=float)
        for i, r in enumerate(rd77):
            for k, cf in r.items():
                A_ub77[i, cidx77[k]] = float(cf)
            A_ub77[i, ncols77 - 1] = t_c77[i]
        A_ub77_csc = A_ub77.tocsc()
        b_ub77_arr = np.array(b_ub77)
        for dl in [0.05, 0.10, 0.25, None]:
            bnds = []
            for k in cols77:
                if k[0] in ("M", "lQ"):
                    bnds.append((0.0, None))
                elif k[0] == "XQ":
                    bnds.append((-3.0, 3.0))
                elif dl is None:
                    bnds.append((0.0, 3.0) if k[0] in ("x", "xo", "lq") else (0.0, None))
                else:
                    v0 = float(val(("x", tauo_to_tau(k[1])))) if k[0] == "xo" else float(val(k))
                    hi_cap = 3.0 if k[0] in ("x", "xo", "lq") else None
                    bnds.append((max(0.0, v0 - dl), min(hi_cap, v0 + dl) if hi_cap is not None else v0 + dl))
            bnds.append((None, None))
            r77 = linprog(c_clean77, A_ub=A_ub77_csc, b_ub=b_ub77_arr, A_eq=A_eq77_csc, b_eq=b_eq77, bounds=bnds, method="highs-ipm")
            t_v = float(r77.x[-1])
            xo77_res[sb_key][str(dl)] = {
                "T_star": t_v,
                "T_star_frac": str(Fraction(t_v).limit_denominator(100000)),
            }

    # Full Dantzig-Wolfe XO=1 column generation across all 37,379 unique global specs
    split_taus = set()
    for d, lk, sv, r_base, big_pos in row_base_info:
        if (d, lk, sv) in binders_15:
            for ti, to, qk, _, _ in big_pos:
                split_taus.add(ti)
                split_taus.add(to)

    dw_iters = []
    for it in range(8):
        row_dicts = [r for _, r in base_sender_nofb]
        m_sgs = set()
        lq_Qks = set()
        xq_Qks = set()
        recv_idx_map = []
        seen_sk = set()
        for idx_r, (d, lk, sv, r_base, big_pos) in enumerate(row_base_info):
            r = dict(r_base)
            for ti, to, qk, _, _ in big_pos:
                if ti in split_taus or to in split_taus:
                    if qk is not None:
                        r[("XQ", qk)] = r.get(("XQ", qk), 0) + 1
                        xq_Qks.add(qk)
                elif ti != to:
                    r[("x", ti)] = r.get(("x", ti), 0) + 1
                    r[("x", to)] = r.get(("x", to), 0) - 1
            r = {k: v for k, v in r.items() if v != 0}
            sk = (d, tuple(sorted(r.items(), key=str)))
            if sk in seen_sk:
                continue
            seen_sk.add(sk)
            for k in r:
                if k[0] == "M":
                    m_sgs.add(k[1])
                elif k[0] == "lQ":
                    lq_Qks.add(k[1])
            row_dicts.append(r)
            recv_idx_map.append(idx_r)
        n_recv = len(recv_idx_map)
        for qk in sorted(lq_Qks):
            m_ = qk[-1]
            prefix = qk[:-1]
            for a2_ in LET:
                if (m_ >> (a2_ - 5)) & 1:
                    row_dicts.append({("lq", prefix + (a2_,)): 1, ("lQ", qk): -1})
        for sg in sorted(m_sgs):
            for hk in sorted(cand2(sg)):
                if canon(hk[:6]) in UNC_tuples or is_rsst_2_126(hk[:6]):
                    continue
                row_dicts.append({("h", hk): 1, ("M", sg): -1})
        for qk in sorted(xq_Qks):
            for eA, eB, ti_o, to_o in xo_cands(qk):
                rd = {("XQ", qk): -1}
                if ti_o != to_o:
                    ti_c = tauo_to_tau(ti_o)
                    to_c = tauo_to_tau(to_o)
                    k_in = ("xo", ti_o) if ti_c in split_taus else ("x", ti_c)
                    k_out = ("xo", to_o) if to_c in split_taus else ("x", to_c)
                    if k_in != k_out:
                        rd[k_in] = rd.get(k_in, 0) + 1
                        rd[k_out] = rd.get(k_out, 0) - 1
                row_dicts.append(rd)
        all_cols = sorted({k for r in row_dicts + base_cons2_nofb for k in r}, key=str)
        col_idx = {k: j for j, k in enumerate(all_cols)}
        n_cols = len(all_cols) + 1
        b_ub = [-1.0] * n_send + [float(row_base_info[idx_r][0] - 6) for idx_r in recv_idx_map] + [0.0] * (len(row_dicts) - n_send - n_recv)
        t_coeffs = [-1.0] * n_send + [-1.0] * n_recv + [0.0] * (len(row_dicts) - n_send - n_recv)
        A_ub = lil_matrix((len(row_dicts), n_cols), dtype=float)
        for i, r in enumerate(row_dicts):
            for k, cf in r.items():
                A_ub[i, col_idx[k]] = float(cf)
            A_ub[i, n_cols - 1] = t_coeffs[i]
        A_eq = lil_matrix((len(base_cons2_nofb), n_cols), dtype=float)
        for i, r in enumerate(base_cons2_nofb):
            for k, cf in r.items():
                A_eq[i, col_idx[k]] = float(cf)
        A_ub_csc = A_ub.tocsc()
        A_eq_csc = A_eq.tocsc()
        b_ub_arr = np.array(b_ub)
        b_eq_arr = np.zeros(len(base_cons2_nofb))
        c_clean = np.zeros(n_cols)
        c_clean[-1] = 1.0
        bounds = [
            (0.0, None)
            if k[0] in ("M", "lQ")
            else ((-3.0, 3.0) if k[0] == "XQ" else ((0.0, 3.0) if k[0] in ("x", "lq", "xo") else (0.0, None)))
            for k in all_cols
        ] + [(None, None)]
        res = linprog(c_clean, A_ub=A_ub_csc, b_ub=b_ub_arr, A_eq=A_eq_csc, b_eq=b_eq_arr, bounds=bounds, method="highs-ipm")
        duals = -res.ineqlin.marginals
        new_taus = set()
        binders = []
        for j_r in range(n_recv):
            dv = duals[n_send + j_r]
            if dv > 1e-7:
                idx_r = recv_idx_map[j_r]
                d, lk, sv, _, big_pos = row_base_info[idx_r]
                binders.append([d, lk, sv, str(Fraction(dv).limit_denominator(100000))])
                for ti, to, qk, _, _ in big_pos:
                    if ti not in split_taus:
                        new_taus.add(ti)
                    if to not in split_taus:
                        new_taus.add(to)
        t_bf_val = float(res.x[-1])
        dw_iters.append({
            "iter": it,
            "split_taus_count": len(split_taus),
            "xq_keys_count": len(xq_Qks),
            "T_star_buffered": t_bf_val,
            "T_star_buffered_frac": str(Fraction(t_bf_val).limit_denominator(100000)),
            "binders_count": len(binders),
            "new_taus_count": len(new_taus),
        })
        if not new_taus:
            # Also evaluate non_degrading unanchored and delta sweep on converged 205-tau XO=1 matrix
            b_ub_nd = [-1.0 + T_fb] * n_send + [float(row_base_info[idx_r][0] - 6) for idx_r in recv_idx_map] + [0.0] * (len(row_dicts) - n_send - n_recv)
            A_ub_nd = A_ub.copy()
            for i_s in range(n_send):
                A_ub_nd[i_s, n_cols - 1] = 0.0
            A_ub_nd_csc = A_ub_nd.tocsc()
            b_ub_nd_arr = np.array(b_ub_nd)
            res_nd = linprog(c_clean, A_ub=A_ub_nd_csc, b_ub=b_ub_nd_arr, A_eq=A_eq_csc, b_eq=b_eq_arr, bounds=bounds, method="highs-ipm")
            t_nd_val = float(res_nd.x[-1])
            dw_delta_sweep = {"non_degrading": {}, "buffered": {}}
            for dl in [0.05, 0.10, 0.15, 0.25]:
                b_dl = []
                for k in all_cols:
                    if k[0] in ("M", "lQ"):
                        b_dl.append((0.0, None))
                    elif k[0] == "XQ":
                        b_dl.append((-3.0, 3.0))
                    else:
                        v0 = float(val(("x", tauo_to_tau(k[1])))) if k[0] == "xo" else float(val(k))
                        hi_cap = 3.0 if k[0] in ("x", "xo", "lq") else None
                        b_dl.append((max(0.0, v0 - dl), min(hi_cap, v0 + dl) if hi_cap is not None else v0 + dl))
                b_dl.append((None, None))
                r_bf_dl = linprog(c_clean, A_ub=A_ub_csc, b_ub=b_ub_arr, A_eq=A_eq_csc, b_eq=b_eq_arr, bounds=b_dl, method="highs-ipm")
                r_nd_dl = linprog(c_clean, A_ub=A_ub_nd_csc, b_ub=b_ub_nd_arr, A_eq=A_eq_csc, b_eq=b_eq_arr, bounds=b_dl, method="highs-ipm")
                dw_delta_sweep["buffered"][str(dl)] = {
                    "T_star": float(r_bf_dl.x[-1]),
                    "T_star_frac": str(Fraction(float(r_bf_dl.x[-1])).limit_denominator(100000)),
                }
                dw_delta_sweep["non_degrading"][str(dl)] = {
                    "T_star": float(r_nd_dl.x[-1]),
                    "T_star_frac": str(Fraction(float(r_nd_dl.x[-1])).limit_denominator(100000)),
                }
            break
        split_taus |= new_taus

    binder_deg_counts = {str(k): v for k, v in sorted(collections.Counter(b[0] for b in binders).items())}
    return {
        "binders_15_xo1": {
            "rows_count": 15,
            "xq_keys": xq15,
            "T_star_buffered": t15_bf,
            "T_star_buffered_frac": str(Fraction(t15_bf).limit_denominator(100000)),
            "binders_buffered": act15_bf,
            "T_star_non_degrading": t15_nd,
            "binders_non_degrading": act15_nd,
        },
        "pool_2320_xo1": {
            "rows_count": len(pool_2320),
            "xq_keys": xq2320,
            "T_star_buffered": t2320_bf,
            "binders_buffered": act2320_bf,
            "T_star_non_degrading": t2320_nd,
            "binders_non_degrading": act2320_nd,
        },
        "xo77_global_37376": xo77_res,
        "dw_full_xo1_global_37379": {
            "unique_specs": n_recv,
            "converged_split_taus": len(split_taus),
            "converged_xq_keys": len(xq_Qks),
            "T_star_buffered_unanchored": t_bf_val,
            "T_star_buffered_unanchored_frac": str(Fraction(t_bf_val).limit_denominator(100000)),
            "T_star_non_degrading_unanchored": t_nd_val,
            "T_star_non_degrading_unanchored_frac": str(Fraction(t_nd_val).limit_denominator(100000)),
            "iterations": dw_iters,
            "converged_binders": binders,
            "binder_degree_counts": binder_deg_counts,
            "delta_sweep": dw_delta_sweep,
        },
    }


def main():
    os.chdir(WDIR)
    argf = ensure_a100_args_file(WDIR)
    ensure_cached_a100_pools()

    # Load cached A100 receiver pools
    surv_certs = [tuple(r) for r in json.load(open("/tmp/surv_certs.json"))]
    all_pool = [tuple(r) for r in json.load(open("/tmp/a100_pool_rows.json"))]
    data_pos = json.load(open("/tmp/a100_pos_rows.json"))
    pos_pool = [(r[1], r[2], r[3]) for r in data_pos["pos"]]
    near_pool = [(r[1], r[2], r[3]) for r in data_pos["near"]]
    d10_12_data = json.load(open("/tmp/d10_12_sep_rows.json"))
    d10_12_pos = [(r[1], r[2], r[3]) for r in d10_12_data if r[0] > 1e-9]
    d10_12_near = [(r[1], r[2], r[3]) for r in d10_12_data if r[0] <= 1e-9]

    active_2308 = sorted(set(surv_certs) | set(pos_pool) | set(near_pool) | set(d10_12_pos) | set(d10_12_near))
    all_global = sorted(set(all_pool) | set(surv_certs) | set(d10_12_pos) | set(d10_12_near))

    from global_discharging_closure import _compute_karp_and_dp_tail

    out_json = os.path.join(GDIR, "step2_cutting_plane_results.json")
    prev_data = None
    if os.path.exists(out_json):
        try:
            prev_data = json.load(open(out_json))
        except Exception:
            prev_data = None

    results_summary = {}

    for tier_name, kill_subdir, use_unc, use_2126, use_full2ball in [
        ("tierA", os.path.join(GDIR, "kill_upgraded", "tierA"), False, False, False),
        ("tierB", os.path.join(GDIR, "kill_upgraded", "tierB"), True, True, False),
        ("tierB_full2ball", os.path.join(GDIR, "kill_upgraded", "tierB"), True, True, True),
    ]:
        print("\n" + "=" * 80)
        print(f"RUNNING STEP 2 OUTER C++ CUTTING-PLANE LOOP FOR {tier_name.upper()}")
        print("=" * 80)
        l3tab = (
            f"{kill_subdir}/studio_l3qtab_+1.json,"
            f"{kill_subdir}/studio_l3qtab_-1.json"
        )
        l3tab8 = (
            f"{kill_subdir}/studio_l3qtabV8_+1.json,"
            f"{kill_subdir}/studio_l3qtabV8_-1.json"
        )
        extra_rules_file = os.path.join(kill_subdir, "full2ball_extra_rules.json") if use_full2ball else None
        ns = load_st21_and_wlp3r6(argf, kill_subdir, l3tab, l3tab8, WDIR)
        fast_sep = FastSeparatorTables(
            ns,
            use_unc=use_unc,
            use_2126=use_2126,
            tag=tier_name,
            extra_rules_path=extra_rules_file,
        )

        SENDERS = ns["SENDERS"]
        sender_row = ns["sender_row"]
        cons2_row = ns["cons2_row"]
        recv_spec = (
            make_recv_spec_full2ball(ns, extra_rules_file)
            if use_full2ball
            else ns["recv_spec"]
        )
        recv_spec_fn_opt = recv_spec if use_full2ball else None
        cand2 = ns["cand2"]
        canon = ns["canon"]
        isR6 = ns["isR6"]
        LET = ns["LET"]
        val = ns["val"]
        T_fb = float(ns["T"])
        UNC_tuples = {canon(tuple(int(ch) for ch in w)) for w in ns["UNC"]}
        is_rsst_2_126 = lambda w: any(
            w[i] == 5 and w[(i + 1) % 6] == 6 and w[(i + 2) % 6] == 5 for i in range(6)
        )

        # Prebuild base senderR2 and cons2 (no-fb)
        ALL6 = sorted({canon(L) for L in itertools.product(LET, repeat=6) if not isR6(L)})
        base_sender_nofb = []
        for w in SENDERS:
            sixes = [k for k in range(5) if w[k] == 6]
            hats = list(range(5))
            seen_nf = set()
            for hb in itertools.product((0, 1), repeat=len(hats)):
                for fb in itertools.product((0, 1), repeat=len(sixes)):
                    r = sender_row(w, dict(zip(hats, hb)), dict(zip(sixes, fb)))
                    if r is not None:
                        r_nf = {k: -cf for k, cf in r.items() if k[0] != "fb"}
                        key_nf = tuple(sorted(r_nf.items(), key=str))
                        if key_nf not in seen_nf:
                            seen_nf.add(key_nf)
                            base_sender_nofb.append((w, r_nf))

        seen_cons2_nofb = set()
        base_cons2_nofb = []
        for L in ALL6:
            for s in itertools.product((5, 7), repeat=6):
                r = cons2_row(L, s)
                key_nf = tuple(sorted(((k, v) for k, v in r.items() if k[0] != "fb"), key=str))
                if key_nf not in seen_cons2_nofb:
                    seen_cons2_nofb.add(key_nf)
                    base_cons2_nofb.append(dict(key_nf))

        def solve_lp(
            recv_rows,
            anchor_delta=0.02,
            sender_buffered=False,
            clean_duals=False,
            use_ipm=True,
            two_stage_lex=False,
            ref_sol_map=None,
        ):
            row_dicts = [r for _, r in base_sender_nofb]
            cons2_list = base_cons2_nofb
            s_labels = [w for w, _ in base_sender_nofb]
            b_ub = [-1.0 if sender_buffered else (-1.0 + T_fb)] * len(row_dicts)
            t_coeffs = [-1.0 if sender_buffered else 0.0] * len(row_dicts)
            row_labels = [("senderR2", w) for w in s_labels]

            m_sgs = set()
            lq_Qks = set()
            for d, lk, sv in recv_rows:
                r = {k: v for k, v in recv_spec(d, lk, sv).items() if k[0] != "fb"}
                for k in r:
                    if k[0] == "M":
                        m_sgs.add(k[1])
                    elif k[0] == "lQ":
                        lq_Qks.add(k[1])
                row_dicts.append(r)
                t_coeffs.append(-1.0)
                b_ub.append(float(d - 6))
                row_labels.append(("receiverR2", d, lk, sv))

            for qk in sorted(lq_Qks):
                m_ = qk[-1]
                prefix = qk[:-1]
                for a2_ in LET:
                    if (m_ >> (a2_ - 5)) & 1:
                        row_dicts.append({("lq", prefix + (a2_,)): 1, ("lQ", qk): -1})
                        t_coeffs.append(0.0)
                        b_ub.append(0.0)
                        row_labels.append(("mrowL", qk, prefix + (a2_,)))

            for sg in sorted(m_sgs):
                for hk in sorted(cand2(sg)):
                    if use_unc and canon(hk[:6]) in UNC_tuples:
                        continue
                    if use_2126 and is_rsst_2_126(hk[:6]):
                        continue
                    row_dicts.append({("h", hk): 1, ("M", sg): -1})
                    t_coeffs.append(0.0)
                    b_ub.append(0.0)
                    row_labels.append(("mrowR2", sg, hk))

            all_cols = sorted({k for r in row_dicts + cons2_list for k in r}, key=str)
            col_idx = {k: j for j, k in enumerate(all_cols)}
            n_cols = len(all_cols) + 1

            # 1-column per variable with 1e-5 / 1e-4 secondary regularization
            # (100x above HiGHS 1e-7 dual feasibility tolerance to prevent simplex cycling)
            bounds = []
            c_base = []
            for k in all_cols:
                hi_cap = 3.0 if k[0] in ("x", "lq") else None
                if anchor_delta is None or k[0] in ("M", "lQ"):
                    bounds.append((0.0, hi_cap))
                    c_base.append(1e-5 if (anchor_delta is not None and k[0] in ("M", "lQ")) else 0.0)
                    continue
                v0 = float(val(k))
                lo = max(0.0, v0 - anchor_delta)
                hi = min(hi_cap, v0 + anchor_delta) if hi_cap is not None else (v0 + anchor_delta)
                bounds.append((lo, hi))
                c_base.append(1e-4 if v0 == 0.0 else (1e-5 if k[0] in ("y", "h", "r") else 0.0))

            bounds.append((None, None))
            c_base.append(1.0)

            A_ub = lil_matrix((len(row_dicts), n_cols), dtype=float)
            for i, r in enumerate(row_dicts):
                for k, cf in r.items():
                    A_ub[i, col_idx[k]] = float(cf)
                A_ub[i, n_cols - 1] = t_coeffs[i]
            A_eq = lil_matrix((len(cons2_list), n_cols), dtype=float)
            for i, r in enumerate(cons2_list):
                for k, cf in r.items():
                    A_eq[i, col_idx[k]] = float(cf)
            b_eq = np.zeros(len(cons2_list), dtype=float)

            A_ub_csc = A_ub.tocsc()
            A_eq_csc = A_eq.tocsc()
            b_ub_arr = np.array(b_ub)
            if (clean_duals or two_stage_lex) and anchor_delta is not None:
                c_clean = np.zeros(n_cols, dtype=float)
                c_clean[-1] = 1.0
                res_clean = linprog(
                    c_clean,
                    A_ub=A_ub_csc,
                    b_ub=b_ub_arr,
                    A_eq=A_eq_csc,
                    b_eq=b_eq,
                    bounds=bounds,
                    method="highs-ipm" if use_ipm else "highs",
                )
                assert res_clean.success
                duals = (
                    -res_clean.ineqlin.marginals
                    if (res_clean.ineqlin is not None and res_clean.ineqlin.marginals is not None)
                    else np.zeros(len(row_labels))
                )
                active_recvs = [
                    (row_labels[i][1], row_labels[i][2], row_labels[i][3], str(Fraction(duals[i]).limit_denominator(100000)))
                    for i in range(len(row_labels))
                    if duals[i] > 1e-7 and row_labels[i][0] == "receiverR2"
                ]
                t_clean = float(res_clean.x[-1])
                if not two_stage_lex:
                    return t_clean, None, active_recvs

                # Stage 2: Non-epigraph column-split L1 regularization around ref_sol_map (or SOL0)
                # Epigraph variables M(sg) and lQ(qk) remain single-column with +1e-5 weight so they stay tight.
                is_epig = [k[0] in ("M", "lQ") for k in all_cols]
                v_ref_arr = np.zeros(n_cols, dtype=float)
                col_map_s2 = []
                bnds_s2 = []
                c_s2 = []
                idx_s2 = 0
                for j, k in enumerate(all_cols):
                    lo_j, hi_j = bounds[j]
                    if is_epig[j]:
                        col_map_s2.append((idx_s2,))
                        bnds_s2.append((lo_j, hi_j))
                        c_s2.append(1e-5)
                        idx_s2 += 1
                    else:
                        vr = (
                            float(ref_sol_map[k])
                            if (ref_sol_map is not None and k in ref_sol_map)
                            else float(val(k))
                        )
                        if lo_j is not None:
                            vr = max(lo_j, vr)
                        if hi_j is not None:
                            vr = min(hi_j, vr)
                        v_ref_arr[j] = vr
                        col_map_s2.append((idx_s2, idx_s2 + 1))
                        bnds_s2.append((0.0, (hi_j - vr) if hi_j is not None else None))
                        bnds_s2.append((0.0, max(0.0, vr - (lo_j if lo_j is not None else 0.0))))
                        w_j = 1e-4 if float(val(k)) == 0.0 else 1e-5
                        c_s2.extend([w_j, w_j])
                        idx_s2 += 2
                t_col_s2 = idx_s2
                bnds_s2.append((t_clean - 1e-11, t_clean + 1e-9))
                c_s2.append(1.0)
                n_s2 = idx_s2 + 1

                b_ub_s2 = b_ub_arr - A_ub_csc.dot(v_ref_arr)
                b_eq_s2 = b_eq - A_eq_csc.dot(v_ref_arr)

                def _expand_csc_s2(M_csc):
                    M_coo = M_csc.tocoo()
                    rows_l, cols_l, data_l = [], [], []
                    for r_i, c_j, d_v in zip(M_coo.row, M_coo.col, M_coo.data):
                        if c_j == n_cols - 1:
                            rows_l.append(r_i)
                            cols_l.append(t_col_s2)
                            data_l.append(d_v)
                        elif is_epig[c_j]:
                            rows_l.append(r_i)
                            cols_l.append(col_map_s2[c_j][0])
                            data_l.append(d_v)
                        else:
                            c_p, c_m = col_map_s2[c_j]
                            rows_l.append(r_i)
                            cols_l.append(c_p)
                            data_l.append(d_v)
                            rows_l.append(r_i)
                            cols_l.append(c_m)
                            data_l.append(-d_v)
                    from scipy.sparse import csc_matrix
                    return csc_matrix((data_l, (rows_l, cols_l)), shape=(M_csc.shape[0], n_s2))

                res_lex = linprog(
                    np.array(c_s2, dtype=float),
                    A_ub=_expand_csc_s2(A_ub_csc),
                    b_ub=b_ub_s2,
                    A_eq=_expand_csc_s2(A_eq_csc),
                    b_eq=b_eq_s2,
                    bounds=bnds_s2,
                    method="highs-ipm" if use_ipm else "highs",
                )
                assert res_lex.success, f"Stage 2 lex LP failed: {res_lex.message}"
                sol_map_lex = {}
                for j, k in enumerate(all_cols):
                    if is_epig[j]:
                        sol_map_lex[k] = float(res_lex.x[col_map_s2[j][0]])
                    else:
                        c_p, c_m = col_map_s2[j]
                        sol_map_lex[k] = float(v_ref_arr[j] + res_lex.x[c_p] - res_lex.x[c_m])
                return t_clean, sol_map_lex, active_recvs, float(res_lex.x[t_col_s2])

            c_obj = np.array(c_base, dtype=float)
            res = linprog(
                c_obj,
                A_ub=A_ub_csc,
                b_ub=b_ub_arr,
                A_eq=A_eq_csc,
                b_eq=b_eq,
                bounds=bounds,
                method="highs-ipm" if (use_ipm and anchor_delta is not None) else "highs",
            )
            assert res.success, f"LP failed: {res.message}"
            duals = (
                -res.ineqlin.marginals
                if (res.ineqlin is not None and res.ineqlin.marginals is not None)
                else np.zeros(len(row_labels))
            )
            active_recvs = [
                (row_labels[i][1], row_labels[i][2], row_labels[i][3], str(Fraction(duals[i]).limit_denominator(100000)))
                for i in range(len(row_labels))
                if duals[i] > 1e-7 and row_labels[i][0] == "receiverR2"
            ]
            sol_map = {k: float(res.x[j]) for j, k in enumerate(all_cols)}
            return float(res.x[-1]), sol_map, active_recvs

        # 1. Check active-pool LP and 25-cert LP (unanchored)
        t_unanc_25, _, act_unanc_25 = solve_lp(surv_certs, anchor_delta=None, sender_buffered=True)
        t_unanc_2308, _, act_unanc_2308 = solve_lp(active_2308, anchor_delta=None, sender_buffered=True)
        print(f"  [{tier_name}] Unanchored 25-row Cert LP:          T* = {t_unanc_25:+.12f}, binders = {act_unanc_25}")
        print(f"  [{tier_name}] Unanchored 2,308-row Active Pool LP: T* = {t_unanc_2308:+.12f}, binders = {act_unanc_2308}")

        cpp_rows_file = os.path.join(GDIR, "cpp_separated_rows.json")
        persisted_cpp_rows = []
        if os.path.exists(cpp_rows_file):
            persisted_cpp_rows = [tuple(r) for r in json.load(open(cpp_rows_file))]

        # Precompute specs for all 71,562 global pool rows first, then any persisted unpooled C++ rows
        all_global_set = set(all_global)
        all_global_specs = []
        pool_row_specs = []
        seen_global_spec_keys = set()
        for d, lk, sv in all_global:
            r_nf = {k: v for k, v in recv_spec(d, lk, sv).items() if k[0] != "fb"}
            sk = (d, tuple(sorted(r_nf.items(), key=str)))
            pool_row_specs.append((d, lk, sv, sk))
            if sk not in seen_global_spec_keys:
                seen_global_spec_keys.add(sk)
                all_global_specs.append((d, lk, sv, r_nf, sk))
        for d, lk, sv in sorted(set(persisted_cpp_rows) - all_global_set):
            r_nf = {k: v for k, v in recv_spec(d, lk, sv).items() if k[0] != "fb"}
            sk = (d, tuple(sorted(r_nf.items(), key=str)))
            if sk not in seen_global_spec_keys:
                seen_global_spec_keys.add(sk)
                all_global_specs.append((d, lk, sv, r_nf, sk))

        def run_cutting_plane_for_config(
            sb_flag: bool,
            sb_name: str,
            cur_delta: float = 0.02,
            count_pos_rows: bool = True,
            two_stage_lex: bool = False,
            ref_sol_map=None,
        ):
            nonlocal persisted_cpp_rows
            print(f"\n  [{tier_name} | {sb_name} | delta={cur_delta}] Starting Outer LP + C++ sep3r_l3q Cutting-Plane Loop...")
            cur_rows = []
            cur_spec_keys = set()
            for d, lk, sv in sorted(set(active_2308) | set(persisted_cpp_rows)):
                r_nf = {k: v for k, v in recv_spec(d, lk, sv).items() if k[0] != "fb"}
                sk = (d, tuple(sorted(r_nf.items(), key=str)))
                if sk not in cur_spec_keys:
                    cur_spec_keys.add(sk)
                    cur_rows.append((d, lk, sv))

            def _solve_cur(rows_in):
                if two_stage_lex:
                    tc, sm, ar, _ = solve_lp(
                        rows_in,
                        anchor_delta=cur_delta,
                        sender_buffered=sb_flag,
                        two_stage_lex=True,
                        ref_sol_map=ref_sol_map,
                    )
                    return tc, sm, ar
                return solve_lp(rows_in, anchor_delta=cur_delta, sender_buffered=sb_flag)

            # Warm-start phase on global pool rows (including any persisted C++ cuts)
            for it_pool in range(15):
                T_star, sol_map, act_recvs = _solve_cur(cur_rows)
                h_max = {}
                lq_max = {}
                get_v = lambda k: sol_map[k] if k in sol_map else float(val(k))
                new_pool_viol = []
                cur_set = set(cur_rows)
                for d, lk, sv, r, sk in all_global_specs:
                    if sk in cur_spec_keys:
                        continue
                    ex = 0.0
                    for k, cf in r.items():
                        if k[0] == "M":
                            sg = k[1]
                            if sg not in h_max:
                                cands = [
                                    get_v(("h", hk))
                                    for hk in cand2(sg)
                                    if not (use_unc and canon(hk[:6]) in UNC_tuples)
                                    and not (use_2126 and is_rsst_2_126(hk[:6]))
                                ]
                                h_max[sg] = max(cands) if cands else 0.0
                            v_k = h_max[sg]
                        elif k[0] == "lQ":
                            qk = k[1]
                            if qk not in lq_max:
                                m_ = qk[-1]
                                prefix = qk[:-1]
                                cands = [get_v(("lq", prefix + (a2_,))) for a2_ in LET if (m_ >> (a2_ - 5)) & 1]
                                lq_max[qk] = max(cands) if cands else 0.0
                            v_k = lq_max[qk]
                        else:
                            v_k = get_v(k)
                        ex += cf * v_k
                    ex -= (d - 6)
                    if ex > T_star + 1e-7:
                        new_pool_viol.append((ex, d, lk, sv, sk))
                if not new_pool_viol:
                    break
                new_pool_viol.sort(reverse=True)
                for _, d, lk, sv, sk in new_pool_viol[:2000]:
                    if sk not in cur_spec_keys:
                        cur_spec_keys.add(sk)
                        cur_set.add((d, lk, sv))
                cur_rows = sorted(cur_set)

            print(f"    - Pool warm-start converged at T* = {T_star:+.9f} ({len(cur_rows):,d} active LP rows)")

            # Outer C++ sep3r_l3q separation across all 5^d x 5^d (d = 7..17)
            cpp_rounds = 0
            total_unpooled_added = []
            while True:
                cpp_rounds += 1
                t_sep0 = time.time()
                proc, yv, xv, v6b = fast_sep.write_tables_and_spawn(sol_map)
                h_max = {}
                lq_max = {}
                cur_set = set(cur_rows)
                round_new = []
                per_d_stats = {}
                try:
                    for d in range(7, 18):
                        thr = (d - 6) + T_star + 1e-7
                        used_cap = 2000
                        out, nodes = fast_sep.query_sepx(proc, d, yv, xv, v6b, thr, cap=used_cap)
                        exact_viol = []
                        max_dev = 0.0
                        for idx_o, (wq, lk, sv) in enumerate(out):
                            if idx_o < 50:
                                v_ex = eval_row_exact(ns, d, lk, sv, sol_map, use_unc, use_2126, h_max, lq_max, recv_spec_fn=recv_spec_fn_opt)
                                max_dev = max(max_dev, abs(wq - v_ex))
                            else:
                                v_ex = wq
                            if v_ex > thr:
                                exact_viol.append((v_ex - (d - 6), d, lk, sv))
                        assert max_dev < 1e-8, f"C++ separator leaf mismatch at d={d}: max_dev={max_dev}"
                        exact_viol.sort(reverse=True)
                        added_d = 0
                        for _, d_, lk, sv in exact_viol:
                            r_nf = {k: v for k, v in recv_spec(d_, lk, sv).items() if k[0] != "fb"}
                            sk = (d_, tuple(sorted(r_nf.items(), key=str)))
                            if sk not in cur_spec_keys:
                                cur_spec_keys.add(sk)
                                round_new.append((d_, lk, sv))
                                cur_set.add((d_, lk, sv))
                                if sk not in seen_global_spec_keys:
                                    seen_global_spec_keys.add(sk)
                                    all_global_specs.append((d_, lk, sv, r_nf, sk))
                                added_d += 1
                                if added_d >= 800:
                                    break
                        per_d_stats[d] = {
                            "rel_above": len(out),
                            "exact_viol": len(exact_viol),
                            "added": added_d,
                            "nodes": nodes,
                            "cap": used_cap,
                        }
                finally:
                    proc.stdin.close()
                    proc.wait()

                sep_dt = time.time() - t_sep0
                d_summary = {d: per_d_stats[d]["exact_viol"] for d in range(7, 18) if per_d_stats[d]["exact_viol"] > 0}
                if not round_new:
                    print(
                        f"    - C++ sep3r_l3q Round {cpp_rounds} (sep={sep_dt:.2f}s): T* = {T_star:+.9f}, "
                        f"0 violations across all d=7..17!"
                    )
                    for d in range(7, 18):
                        assert per_d_stats[d]["exact_viol"] == 0 and per_d_stats[d]["rel_above"] < per_d_stats[d]["cap"], (
                            f"Expected 0 violators at convergence for d={d}, got {per_d_stats[d]}"
                        )
                    break
                total_unpooled_added.extend(round_new)
                persisted_cpp_rows = sorted(set(persisted_cpp_rows) | set(round_new))
                with open(cpp_rows_file, "w") as f:
                    json.dump(persisted_cpp_rows, f)
                cur_rows = sorted(cur_set)
                t_lp0 = time.time()
                T_star_prev = T_star
                T_star, sol_map, act_recvs = _solve_cur(cur_rows)
                lp_dt = time.time() - t_lp0
                print(
                    f"    - C++ sep3r_l3q Round {cpp_rounds} (sep={sep_dt:.2f}s, lp={lp_dt:.2f}s, rows={len(cur_rows):,d}): "
                    f"T* {T_star_prev:+.9f} -> {T_star:+.9f}, new cuts: {len(round_new)} (viol by d: {d_summary})"
                )

            # Extract clean unregularized dual certificate on the converged LP row set
            if not two_stage_lex:
                _, _, act_recvs = solve_lp(cur_rows, anchor_delta=cur_delta, sender_buffered=sb_flag, clean_duals=True, use_ipm=True)

            # Evaluate live 125x125 max-plus DP (d=18..30) and Karp cycle-mean lambda_9
            lam, dp_max, dp18, dp30, z9 = _compute_karp_and_dp_tail(
                ns, sol_map=sol_map, use_unc=use_unc, use_2126=use_2126
            )
            d0_karp = (6.0 - T_star) / (1.0 - lam)
            assert dp_max < T_star and d0_karp <= 31.0

            pos_rows = []
            pool_pos_rows = []
            pool_pos_by_d = {}
            pos_by_d = {}
            if count_pos_rows and T_star > 1e-9:
                h_max = {}
                lq_max = {}
                sk_ex_cache = {}
                seen_eval = set()
                for d, lk, sv, _, sk in all_global_specs:
                    if (d, lk, sv) in seen_eval:
                        continue
                    seen_eval.add((d, lk, sv))
                    ex = eval_row_exact(ns, d, lk, sv, sol_map, use_unc, use_2126, h_max, lq_max, recv_spec_fn=recv_spec_fn_opt) - (d - 6)
                    sk_ex_cache[sk] = ex
                    if ex > 1e-9:
                        pos_rows.append((d, lk, sv, ex))
                pool_pos_rows = [(d, lk, sv, sk_ex_cache[sk]) for d, lk, sv, sk in pool_row_specs if sk_ex_cache[sk] > 1e-9]
                pool_pos_by_d = dict(sorted(collections.Counter(d for d, _, _, _ in pool_pos_rows).items()))
                pos_by_d = dict(sorted(collections.Counter(d for d, _, _, _ in pos_rows).items()))

            print(
                f"    - CONVERGED [{tier_name} | {sb_name} | delta={cur_delta}]: T*_global-LP = {T_star:+.9f} | "
                f"binders: {len(act_recvs)} | "
                f"71,562 pool pos rows: {len(pool_pos_rows)} ({pool_pos_by_d}) | "
                f"total deduplicated pos rows (incl C++ cuts): {len(pos_rows)} ({pos_by_d}) | "
                f"DP d=18..30 <= {dp_max:+.6f} | Karp lambda_9 = {lam:.9f} (d >= {d0_karp:.3f})"
            )

            res_dict = {
                "anchor_delta": cur_delta,
                "T_star": T_star,
                "cpp_rounds": cpp_rounds,
                "unpooled_added_count": len(total_unpooled_added),
                "unpooled_added_rows": total_unpooled_added,
                "active_lp_rows": len(cur_rows),
                "binders": act_recvs,
                "pool_pos_rows_count": len(pool_pos_rows),
                "pool_pos_rows_by_d": pool_pos_by_d,
                "pool_pos_rows": [(d, lk, sv, round(ex, 12)) for d, lk, sv, ex in pool_pos_rows],
                "pos_rows_count": len(pos_rows),
                "pos_rows_by_d": pos_by_d,
                "pos_rows": [(d, lk, sv, round(ex, 12)) for d, lk, sv, ex in pos_rows],
                "dp_max_18_30": dp_max,
                "dp_30": dp30,
                "karp_lambda_9": lam,
                "karp_d0": d0_karp,
                "z9": z9,
                "per_d_stats": per_d_stats,
            }
            return res_dict, sol_map, T_star, cur_rows

        # 2. Run Outer C++ Cutting-Plane Loop for both sender_buffered=False and sender_buffered=True at delta=0.02
        tier_res = {
            "t_unanchored_25": t_unanc_25,
            "binders_unanchored_25": act_unanc_25,
            "t_unanchored_2308": t_unanc_2308,
            "binders_unanchored_2308": act_unanc_2308,
        }

        for sb_flag, sb_name in [(False, "non_degrading"), (True, "buffered")]:
            res_dict, sol_map, T_star, cur_rows_002 = run_cutting_plane_for_config(sb_flag, sb_name, cur_delta=0.02, count_pos_rows=True)
            tier_res[sb_name] = res_dict

            # Export primal solutions in exact st21_check.py JSON format
            if tier_name == "tierA" and not sb_flag:
                export_solution_json(ns, sol_map, T_star, os.path.join(GDIR, "sol_unified_a100_tierA_nondeg.json"))
            elif tier_name == "tierA" and sb_flag:
                export_solution_json(ns, sol_map, T_star, os.path.join(GDIR, "sol_unified_a100_tierA.json"))
                export_solution_json(ns, sol_map, T_star, os.path.join(GDIR, "sol_unified_a100.json"))
            elif tier_name == "tierB" and not sb_flag:
                export_solution_json(ns, sol_map, T_star, os.path.join(GDIR, "sol_unified_a100_tierB_nondeg.json"))
            elif tier_name == "tierB" and sb_flag:
                export_solution_json(ns, sol_map, T_star, os.path.join(GDIR, "sol_unified_a100_tierB.json"))
            elif tier_name == "tierB_full2ball" and not sb_flag:
                export_solution_json(ns, sol_map, T_star, os.path.join(GDIR, "sol_unified_a100_tierB_full2ball_nondeg.json"))
            elif tier_name == "tierB_full2ball" and sb_flag:
                export_solution_json(ns, sol_map, T_star, os.path.join(GDIR, "sol_unified_a100_tierB_full2ball.json"))

        if tier_name == "tierB_full2ball":
            print("\n" + "=" * 80)
            print("RUNNING WIDENED-DELTA T*_global-LP <= 0 C++ CUTTING-PLANE CLOSURE")
            print("=" * 80)
            widened_closure = {}
            sol_005_map = {}
            for sb_flag, sb_name, w_delta, out_sol_fn in [
                (False, "non_degrading_delta005", 0.05, "sol_unified_a100_tierB_full2ball_delta005_nondeg.json"),
                (True, "buffered_delta005", 0.05, "sol_unified_a100_tierB_full2ball_delta005_buffered.json"),
            ]:
                w_res, w_sol, w_T, cur_rows_w = run_cutting_plane_for_config(sb_flag, sb_name, cur_delta=w_delta, count_pos_rows=True)
                if not sb_flag:
                    assert w_T < 0.0, f"Expected T* < 0 for {sb_name}, got {w_T}"
                export_solution_json(ns, w_sol, w_T, os.path.join(GDIR, out_sol_fn))
                widened_closure[sb_name] = w_res
                sol_005_map[sb_flag] = w_sol

            for sb_flag, sb_name, w_delta, out_sol_fn in [
                (False, "non_degrading_delta015", 0.15, "sol_unified_a100_tierB_full2ball_delta015_nondeg.json"),
                (True, "buffered_delta015", 0.15, "sol_unified_a100_tierB_full2ball_delta015_buffered.json"),
            ]:
                w_res, w_sol, w_T, cur_rows_w = run_cutting_plane_for_config(
                    sb_flag,
                    sb_name,
                    cur_delta=w_delta,
                    count_pos_rows=False,
                    two_stage_lex=True,
                    ref_sol_map=sol_005_map[sb_flag],
                )
                if not sb_flag:
                    assert w_T < 0.0, f"Expected T* < 0 for {sb_name}, got {w_T}"
                export_solution_json(ns, w_sol, w_T, os.path.join(GDIR, out_sol_fn))
                widened_closure[sb_name] = w_res

            # Also run the full delta sweep across [0.02, 0.05, 0.10, 0.15, 0.25, 0.50, 1.0] on the converged global row set
            print("\n  [tierB_full2ball] Running Global Active-Pool Widened-Delta Sweep (delta in [0.02, 0.05, 0.10, 0.15, 0.25, 0.50, 1.0])...")
            pool_sweep = {"non_degrading": {}, "buffered": {}}
            for sb_flag, sb_key in [(False, "non_degrading"), (True, "buffered")]:
                for sw_delta in [0.02, 0.05, 0.10, 0.15, 0.25, 0.50, 1.0]:
                    sw_T, sw_sol, _ = solve_lp(cur_rows_w, anchor_delta=sw_delta, sender_buffered=sb_flag)
                    sw_lam, sw_dp, _, sw_dp30, sw_z9 = _compute_karp_and_dp_tail(
                        ns, sol_map=sw_sol, use_unc=use_unc, use_2126=use_2126
                    )
                    sw_d0 = (6.0 - sw_T) / (1.0 - sw_lam) if abs(1.0 - sw_lam) > 1e-9 else float("inf")
                    sw_T_clean, sw_sol_lex, sw_binders_clean, sw_T_lex = solve_lp(
                        cur_rows_w,
                        anchor_delta=sw_delta,
                        sender_buffered=sb_flag,
                        two_stage_lex=True,
                        ref_sol_map=sol_005_map[sb_flag],
                    )
                    sw_lam_lex, sw_dp_lex, _, sw_dp30_lex, sw_z9_lex = _compute_karp_and_dp_tail(
                        ns, sol_map=sw_sol_lex, use_unc=use_unc, use_2126=use_2126
                    )
                    sw_d0_lex = (6.0 - sw_T_clean) / (1.0 - sw_lam_lex) if abs(1.0 - sw_lam_lex) > 1e-9 else float("inf")
                    pool_sweep[sb_key][str(sw_delta)] = {
                        "anchor_delta": sw_delta,
                        "T_star": sw_T,
                        "T_star_clean": sw_T_clean,
                        "T_star_clean_frac": str(Fraction(sw_T_clean).limit_denominator(100000)),
                        "T_star_lex": sw_T_lex,
                        "clean_binders": sw_binders_clean,
                        "active_lp_rows": len(cur_rows_w),
                        "dp_max_18_30": sw_dp,
                        "dp_30": sw_dp30,
                        "karp_lambda_9": sw_lam,
                        "karp_d0": sw_d0,
                        "z9": sw_z9,
                        "dp_max_18_30_lex": sw_dp_lex,
                        "dp_30_lex": sw_dp30_lex,
                        "karp_lambda_9_lex": sw_lam_lex,
                        "karp_d0_lex": sw_d0_lex,
                        "z9_lex": sw_z9_lex,
                    }
                    print(
                        f"    * [{sb_key:13s} | delta={sw_delta:.2f}]: clean T* = {sw_T_clean:+.12f} (lex T* = {sw_T_lex:+.12f}) | "
                        f"DP_lex d=18..30 <= {sw_dp_lex:+.6f} | Karp_lex lambda_9 = {sw_lam_lex:.9f} (d0 = {sw_d0_lex:.3f})"
                    )
            widened_closure["global_pool_delta_sweep"] = pool_sweep
            results_summary["widened_delta_closure"] = widened_closure
            print("\n  [tierB_full2ball] Running s51 (XO=1) Outer-Letter Transfer Refinement Closure...")
            results_summary["s51_xo_closure"] = compute_s51_xo_closure(
                ns, recv_spec, base_sender_nofb, base_cons2_nofb, active_2308, persisted_cpp_rows
            )

        results_summary[tier_name] = tier_res

    results_summary["stage3_closure"] = compute_stage3_closure(results_summary, set(all_global), prev_data)
    with open(out_json, "w") as f:
        json.dump(results_summary, f, indent=2)
    print(f"\nSaved Step 2 cutting-plane results (including s51_xo_closure & stage3_closure) to {out_json}")


def export_solution_json(ns, sol_map, T_star: float, out_path: str, xo_mode: bool = False, fast_sep=None):
    """Export primal solution in exact st21_check.py JSON format (supports both XO=0 and XO=1)."""
    SOL0 = ns["SOL"]
    val = ns["val"]
    LET = ns["LET"]
    MASK = ns["MASK"]
    MASK8 = ns["MASK8"]
    get_v = lambda k: max(0.0, float(sol_map[k])) if k in sol_map else max(0.0, float(val(k)))

    y_keys = set(ns["Y"].keys()) | {k[1] for k in sol_map if k[0] == "y"}
    y_dict = {f"{k[0]}|{''.join(map(str, k[1:]))}": get_v(("y", k)) for k in sorted(y_keys)}

    g_keys = set(ns["G"].keys()) | {k[1] for k in sol_map if k[0] == "g"}
    g_list = [[list(k), get_v(("g", k))] for k in sorted(g_keys)]

    h_keys = set(ns["H"].keys()) | {k[1] for k in sol_map if k[0] == "h"}
    h_list = [[list(k), get_v(("h", k))] for k in sorted(h_keys)]

    x_keys = set(ns["X"].keys()) | {k[1] for k in sol_map if k[0] == "x"}
    has_xo = xo_mode or any(k[0] == "xo" for k in sol_map)

    if has_xo:
        assert fast_sep is not None, "fast_sep is required when exporting XO=1 solutions"
        xo_q = ns["xo_q"]
        xo_cands = ns["xo_cands"]
        xv = {tq: min(3.0, get_v(("x", tq))) for tq in x_keys if get_v(("x", tq)) > 1e-12}
        xov_raw = {k[1]: max(0.0, min(3.0, float(v))) for k, v in sol_map.items() if k[0] == "xo"}
        split_coarse = {fast_sep.tauo_to_tau(t_o) for t_o in xov_raw}
        active_coarse = set(xv.keys()) | split_coarse
        get_xo_val = lambda t_o: xov_raw[t_o] if t_o in xov_raw else xv.get(fast_sep.tauo_to_tau(t_o), 0.0)
        xo_full = {}
        seen_w = set()
        for tau_c in active_coarse:
            for wnd in fast_sep.coarse_tau_windows(tau_c):
                if wnd in seen_w:
                    continue
                seen_w.add(wnd)
                qk = xo_q(*wnd)
                if qk is None:
                    continue
                for _, _, ti_o, to_o in xo_cands(qk):
                    for t_o in (ti_o, to_o):
                        if t_o not in xo_full:
                            vo = get_xo_val(t_o)
                            if vo > 1e-12:
                                xo_full[t_o] = vo
        x_dict = {}
        xo_dict = {str(k): v for k, v in sorted(xo_full.items())}
        z_val = max([v for k, v in xo_full.items() if (int(k) // (3125 * 3125)) % 3 == 2] + [0.0])
    else:
        x_dict = {str(k): min(3.0, get_v(("x", k))) for k in sorted(x_keys) if get_v(("x", k)) > 0.0}
        xo_dict = {}
        z_val = max([v for k, v in x_dict.items() if (int(k) // 15625) % 3 == 2] + [0.0])

    r_keys = set(ns["RR"].keys()) | {k[1] for k in sol_map if k[0] == "r"}
    r_list = [[list(k), get_v(("r", k))] for k in sorted(r_keys) if get_v(("r", k)) > 0.0]

    lq_keys = set(ns["LQ"].keys()) | {k[1] for k in sol_map if k[0] == "lq"}
    lq_list = [[list(k), min(3.0, get_v(("lq", k)))] for k in sorted(lq_keys, key=str) if get_v(("lq", k)) > 0.0]

    # Recompute lQ from Qeff / Qeff8 over MASK and MASK8
    lQ_dict = {}
    for (sg_, c_, a_, w2_, w3_, w4_, o_), m_ in MASK.items():
        qk = (c_, a_, m_)
        if qk not in lQ_dict:
            qv = max([min(3.0, get_v(("lq", (c_, a_, a2)))) for a2 in LET if (m_ >> (a2 - 5)) & 1] + [0.0])
            if qv > 0.0:
                lQ_dict[qk] = qv
    for (sg_, c_, a_, w2_, w3_, w4_, o_), m_ in MASK8.items():
        qk = (8, c_, a_, m_)
        if qk not in lQ_dict:
            qv = max([min(3.0, get_v(("lq", (8, c_, a_, a2)))) for a2 in LET if (m_ >> (a2 - 5)) & 1] + [0.0])
            if qv > 0.0:
                lQ_dict[qk] = qv
    lQ_list = [[list(k), v] for k, v in sorted(lQ_dict.items(), key=str)]

    out_sol = {
        "model": SOL0.get("model", "R6x2"),
        "apex": SOL0.get("apex", True),
        "apexcls": SOL0.get("apexcls", True),
        "zh": SOL0.get("zh", False),
        "v6": False,
        "hat5": True,
        "l3q": True,
        "lqcap": SOL0.get("lqcap", 3),
        "t": T_star,
        "z": z_val,
        "y": y_dict,
        "g": g_list,
        "h": h_list,
        "x": x_dict,
        "r": r_list,
        "lq": lq_list,
        "lQ": lQ_list,
        "fb": [],
        "v": [],
        "V": [],
    }
    if has_xo:
        out_sol["xoflag"] = True
        out_sol["xo"] = xo_dict
    with open(out_path, "w") as f:
        json.dump(out_sol, f)
    print(f"    - Exported primal solution to {out_path} (has_xo={has_xo})")


if __name__ == "__main__":
    main()
