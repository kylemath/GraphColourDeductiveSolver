# Second engine for Opus's t* = 1/4 (P_own_lp, 0daf5198), Studio, 18 Oct ~18:50Z
Inputs (copied from claude/project-thread-7uelj0 at 0daf5198): sol_s2x.json, cert_s2x.json, argsA.txt (local copy
argsA_local.txt with their absolute k42map path pointed at k42map_C_cons.cfast here), k42map_C_cons.cfast.
- Registry diff vs Studio: their args = Studio's base (round-13 args + loop/n9) + addA_dfast18 + k3x_D (3 D) +
  k3x_C (11 C, including f7_.557657_.56.77. and f7_5567567_56.77.6) + their k42map_C_cons. That last file is Studio's
  10 claim-grade k42 windows, without the two [E2, broad X] RSST 126.8168 windows. So it is Studio's B registry minus
  the broad pair, and without Rule T.
- **Upper:** `feascheck.py sol_s2x.json` with WLP3X_DEF=1 (excl = hr1_or1 only) and WLP_SEPF=1 (whole-arrangement
  patterns), exhaustive sep3xf, d = 7..15, plus the d > 15 DP: 0 violated at every d, **FEASIBLE** at t = 1/4
  (feas_s2x.log). 16,413 parse patterns, plus the NF section.
- **Lower:** `lowercheck.py` rebuilds the 5 certificate rows with Studio's own wlp3x code (sender rows; recv_row with
  L2 transfer types).
  - The d = 8 receiver 85556565/65866655 passes sep3xf `c` on the same registry. The 4 senders are Studio sender rows.
  - With exact rational weights 1/4, 1/8, 1/8, 1/4, 1/4, every y and x term cancels. The t coefficient is −1 and the rhs
    is −1/4, so **t ≥ 1/4** (lower_s2x.log).
- So t* = 1/4 exactly on that registry, on two engines (Opus's jsep2 and Studio's sep3xf/wlp3x).

## Second engine for t* = 5/21 (P_own_lp, 9a914f8c: argsA + L2 + the k43 kill), 18 Oct ~20:05Z
- Args diff vs Studio's 1/4 registry: only cpat k43_C.cfast (f8_...55565_...5...., the window Studio verified, 54e6a39e).
- **Upper:** feascheck sol_s6.json (WLP3X_DEF=1, WLP_SEPF=1, exhaustive, d = 7..15 + DP): 0 violated everywhere,
  **FEASIBLE** at t = 5/21 (feas_s6.log).
- **Lower:** lowercheck on cert_s6.json: all 25 rows rebuilt as Studio rows (16 senders, 9 receivers, each allowed by
  sep3xf `c`, 0 rejects). The exact combination has every y and x term cancelling, t coefficient −1, rhs −5/21, so
  **t ≥ 5/21** (lower_s6.log).
- So t* = 5/21 exactly on that registry, on two engines.

## Second engine for t* = 11/47 (P_own_lp, bbd46d73: argsA + the full k43 batch + RSST-D + Rule T option B + L2), ~20:30Z
- Args diff vs Studio: argsA43 = argsA6 with the single-window k43_C swapped for k43_kills_df.out (184 D) and
  k43_kills_cf.cfast (198 C). Both are byte-identical to explore's loop/k43 files (c5a71dc0).
- RSST-D enters through `rpat=` (their rpatD.txt is byte-identical to Studio's loop/studio/rsstD/out/rpatD.txt). It
  was **not** in Studio's A/B base registry; it was used only in the rD1 re-solve. wlp3.py now reads `rpat=` (raw sep3
  patterns).
- Keys: all 1,036 Y and 104 T keys of sol_s6t43.json are canonical under Studio's ykey/tkey (0 not canonical), so
  nothing is merged or double-counted. They load into wlp3xt's indices without error.
- **Upper:** feascheckt.py (wlp3xt option B, sep3xt exhaustive, WLP_SEPF=1, excl = hr1_or1, RSST-D loaded). Sender
  rows evaluated directly; d = 7..15 receivers 0 violated; DP tail clean: **FEASIBLE** at t = 11/47 (feas_s6t43.log).
- **Lower:** lowercheckt.py rebuilds all 24 rows with Studio's code:
  - 12 senderT rows matched to Studio's sender rows by word + bits;
  - 4 mrows T[key] ≤ M_b, each key a Studio inflow completion for b;
  - 8 receiverT rows, each allowed by sep3xt `c`, with inflow slots carrying M_b.
  - Exact combination: every term cancels, t coefficient −1, rhs −11/47, so **t ≥ 11/47** (lower_s6t43.log).
- So t* = 11/47 exactly with Rule T on that registry, on two engines.
