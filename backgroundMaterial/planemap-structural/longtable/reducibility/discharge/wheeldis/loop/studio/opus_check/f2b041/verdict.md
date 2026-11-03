# f2b041: Studio's independent [E2] upper check of the outside team's Tier A full2ball solution

Studio, 3 Nov 2026. This is the request of the coordinator relay of 31 Oct, 21:47Z.

## Verdict

**Upper FEASIBLE at the solution's t = 0.0415648 (stored as 0.041565 = 8313/200000), with the full2ball rules on. Not 17/409:**
the sender rows need t ≥ 0.0415647932, which is about 1e-9 above 17/409 (Opus note, 3 Nov). At 0.041565 Studio's sender min slack
is 2.07e-7.

Everything was checked exhaustively:
- **Senders:** senderR2 20,676 rows, 0 violated.
- **cons2:** 994 + 430 words, 0 violated.
- **Masks:** mrowL (V7) and V8 mrowL 0 violated.
- **Bounds:** 0 negative values; max x = 0.178 (cap 3).
- **Receivers:** d = 7..17, 0 exact violators at every degree.
- **Tail:** DP over d = 18..30 is clean, and the Karp tail has λ = 0.633625577, so it is covered for d ≥ 16.263.
- **Patterns:** D 18,159, C 2,257, RPAT 158. This equals EXPECT_PAT, built from a subset of the outside args, so the pattern set is
  stricter than or equal to theirs.

**The controls fail as they must:**
- with the rules off, at d = 7, 8 and 9;
- with either half of the rules removed, at d = 7, 8 and 9;
- with an empty rule file on the new binary, exactly as with the frozen binary.

Only the upper check was run here (SKIP_LOWER=1). No lower certificate is part of this request.

**[E2] scope.** This verdict covers the LP feasibility of the given solution under the given forbidden set, l3q / V8 tables and
full2ball rules. The rules JSON was used as data. **Studio has not independently re-derived or validated the 5,954 rules** (§6).
Whether the C entries this solution needs are Lean-backed is open (§5 (a), (b)).

## 1. Independence statement
- **Built from:**
  - the coordinator's relay (31 Oct 21:47Z);
  - the outside team's step2_cutting_plane.py (make_recv_spec_full2ball and match_extra_fast), as reference only;
  - the SEP_F2B leaf section of sep3r_l3q_fast.cpp (read for the layout only; Studio's code is its own design: an exact M table
    over 32 masks, an exact Qeff table, and bucketed rule bitsets);
  - build_upgraded_kills.py (read to understand where the rules come from; not run);
  - the data files in in/ (copied from 8a2b1b09 studio_repeat, without README.md).
- **Not opened:** Opus code (engine, cmd scripts, pricer, port_*.py, pcheck.py, f2b.py, st21_f2b.py, sep3r_f2b.cpp),
  README.md result numbers, and Team B material. README.md is to be compared only after this commit.
- **Studio code:**
  - out/job31/st21_check_f2b.py: a copy of st21_check.py. The opt-in F2B=<rules> applies the rules as receiver-row mask shrinks,
    writes the leaf tables, and runs the self-test. It also adds the DLIST degree split. With F2B unset its code path is the frozen
    one.
  - sep3r_f2bS.cpp → bin/sep3r_f2bS: a copy of sep3r_l3q.cpp with an opt-in SEP_F2BS leaf delta and an `f` self-test command.
    With SEP_F2BS unset the delta is 0.
  - Earlier, for the Tier A tables: the opt-in EXTRA_KC blocks in out/job31/st16_filter.py and l3q_masks.py.
- **Frozen files, unchanged** (git clean): sep3r_l3q.cpp / bin/sep3r_l3q, st21_check.py, wlp3r6.py, wlp3.py, wlp3x.py, sep3r.cpp,
  bin/sep3r.

## 2. Inputs (md5)
- **Solution:** in/gc/sol_c_repaired.json e0ad3fcc. Each run used its own copy (run/sol_<tag>.json) and SEPTAG f2bS_<tag>.
- **Rules:** in/gc/kill_upgraded/tierA/full2ball_extra_rules.json b9de962e, 5,954 rules:
  - d7_w6: 1,386
  - d7_w7 ±1: 938 each
  - d8_w6: 1,176
  - d8_w7 ±1: 728 each
  - d9_w6: 60
- **Tier A tables, rebuilt by Studio:** out/job31/f2bA/kill (§14'), l3q V7 studio_l3qtab_±1 f4b86569, V8 studio_l3qtabV8_±1
  2e8e8f5e. These are cell-by-cell equal to the outside tables (steps 1-2, reported 31 Oct).
- **Args:** tierA/args_f2b_local_strict.txt 5f64d27b (D 18,159 / C 2,257 / RPAT 158). It includes held128/part0{0,1}.cfast,
  i.e. job30 with the 128 ring-merge entries held out.
- **Binaries and code:** sep3r_f2bS.cpp 8d6f0b53, bin/sep3r_f2bS 255f401b, st21_check_f2b.py b2394f62.
- **Run environment** (run/f2bS_run.sh): L3Q=1, L3Q8=1, HAT5=1, V6=0, FB=0, XO=0, RPATN=s39o_rpatN3_studio.txt, KILLDIR=f2bA/kill,
  DMAXP=17, EXPECT_T=0.041565, EXPECT_PAT=18159,2257,158.

## 3. The correction
**Receiver rows (Python).** These follow make_recv_spec_full2ball. At position i of a d-row, a rule (p, w_req, s_req) kills letter
p when every (offset, allowed letters) and every (offset, value) holds, with offsets taken mod d. The correction then shrinks masks
as follows:
- **w_i = 6, d ≤ 9:** the §14' private mask becomes pmask & ~extra(d{d}_w6).
- **w_i = 7, d = 7:** the l3q payee mask becomes MASK & ~extra(d7_w7, by side).
- **w_i = 7, d = 8:** the V8 payee mask becomes MASK8 & ~extra(d8_w7, by side).

**Separator leaf (C++).** After every other exact term, the leaf adds
- MT[window][m0 & ~ex] − MT[window][m0] at each link 6 (d ≤ 9), and
- QF[c][a][m0 & ~ex] − QF[c][a][m0] at each link-7 payee (d = 7 V7; d = 8 V8).

Here MT[(U, w+1, s0, s−1, w−1, ap(w+2), ap(w−2))][mask] = Mval of the sig2 with that mask, and QF = Qeff / Qeff8, both written
from Python.

**Checks on the tables:**
- MT at the unreduced mask equals SEP_EXACT6 on all 1,171,875 windows (0 mismatches).
- MT, Qeff and Qeff8 are monotone under removing a mask bit (0 violations), so every delta is ≤ 0.
- The relaxed pruning bound is unchanged and remains an upper bound, so the search stays exhaustive.
- The check "spec rows vs Studio relaxed rows" (603 arrangements) found 0 cases of the relaxed row below the exact one.

**Self-test** (every run, seed 41): 6,000 arrangements, 85% of them built to satisfy a random rule. The spec delta (spec_val with
the rules on minus off) was compared with the C++ leaf delta.
- full rules: 3,773 nonzero, 0 positive, 0 mismatches;
- empty rules: 0 nonzero;
- even half: 3,417 nonzero, 0 mismatches;
- odd half: 3,403 nonzero, 0 mismatches.

The calibration (the sep leaf weight against the spec row on the heaviest 20) differs by at most 4.6e-10 at every d = 7..16.

## 4. Results by degree (full rules)
| d | relaxation reports | exact violated | time | run |
|---|---|---|---|---|
| 7 | 0 | 0 | 245 s | m7 |
| 8 | 0 | 0 | 1152 s | m8 |
| 9 | 0 | 0 | 1405 s | m9 |
| 10 | 0 | 0 | 700 s | m10b |
| 11 | 0 | 0 | 365 s | m10b |
| 12 | 0 | 0 | 153 s | m10b |
| 13 | 0 | 0 | 63 s | m10b |
| 14 | 0 | 0 | 24 s | m10b |
| 15 | 0 | 0 | 9 s | m10b |
| 16 | 0 | 0 | 3 s | m10b |
| 17 | 0 | 0 | 1 s | m10b |
| 18..30 | DP clean | | | all runs |
| tail | Karp λ = 0.633625577, covered for d ≥ 16.263 | | | all runs |

The first d = 10..17 run (m10) did not finish. It calibrated d = 7..16 (all ≤ 4.6e-10), then spent 45 h on the d = 17 calibration
search (top 20 with no threshold) on the loaded box, and was killed on 2 Nov. m10b reran d = 10..17 exhaustively with CALD=9; the f2b
rules act only at d ≤ 9. m10.log is kept.

**Controls** (d = 7..9; CAP 5,000 means more than 5,000 exact violators, so the check is incomplete and FAILs):
| run | rules | binary | d=7 | d=8 | d=9 | verdict |
|---|---|---|---|---|---|---|
| c0off | off (frozen code path) | bin/sep3r_l3q | 5000+ | 5000+ | 1531 | FAIL |
| c1empty | empty JSON | bin/sep3r_f2bS | 5000+ | 5000+ | 1531 | FAIL, identical to c0off |
| h0 | even-indexed half | bin/sep3r_f2bS | 5000+ | 5000+ | 1090 | FAIL |
| h1 | odd-indexed half | bin/sep3r_f2bS | 5000+ | 5000+ | 369 | FAIL |

## 5. Gate items (coordinator, 31 Oct 21:57Z)
**(a) C entries the solution needs: open.** The s52c cover method (keep a candidate set, re-run, then drop a sole entry as the
control) needs more than s52c did, because the full2ball rules are derived from the whole forbidden set
(build_upgraded_kills.extract_full2ball_rules), as are the §14' kill tables and the l3q / V8 masks. A keep-only run must:
1. rebuild the kill tables and the V7 and V8 masks for the keep set (as in s52c), and
2. restrict the rules to those justified by kept configurations (or by D entries).

Step 2 needs a Studio rule extractor or per-rule provenance. The proposed design: keep set = all D entries plus every Lean-backed C
entry. If it is FEASIBLE, (b) is closed with nothing outside Lean. If not, the violators name the non-Lean entries that are needed.
This has not been run yet.

**(b) Lean coverage, first pass only** (c_lean_status_pass1.txt): this covers every C-REDUCIBLE entry in the args, not yet the
needed cover. There are 2,282 names, 2,257 of them distinct. Lean sources: CCover 1c56a79e, CXInt 95ba762d, CXRing 2a4bc4cf,
CCover2 f2acc3e7, CCover3 a6efb310, CWheels.lean, k63f (aa74d7ec, 111), k63o (77078449, 3).

| Lean status | entries |
|---|---|
| CXInt | 343 |
| CXRing (91 also in k63f) | 96 |
| CCover / CCover2 / CCover3 | 22 / 6 / 13 |
| k63f only / k63o | 18 / 3 |
| **not in any Lean set** | **1,756** |

The 1,756 not in Lean come from:
| source file | entries |
|---|---|
| k3x_C_A111.cfast | 840 |
| held128 part00 / part01 | 429 / 425 |
| job27 k2a / k2b | 11 / 13 |
| job28 r_12 / r_1 | 15 / 9 |
| k42map_C_cons | 9 |
| def_r1 | 4 |
| cert_bf | 1 |

The held128 part files are job30 with the 128 FAIL entries already removed, so all 854 of these are non-held entries.

Until (a) is done, **the C side of this upper is not shown to be Lean-backed**, and the result should enter the gate as [E2] with
that qualifier.

**(c) Provenance of nl51_kc.txt** (md5 b9bc6e8b, 8,200 configurations):
- **Source:** Explore committed it at wheeldis/loop/k51/nl51_kc.txt in 42b2b3fc3 (19 Oct, "explore round 51 part 3"; the 2026 set D
  of 8,200 configurations, arXiv:2603.24880, github.com/near-linear-4ct, MIT).
- **Byte-identical copies:** loop/studio/opus_check/s39o/nl51_kc.txt (545aa972a) and f2b041/tierA/nl51_kc.txt.
- **Confirmation:** Explore's round 54d closed at 6368d2f5f (20 Oct 14:06Z, COORDINATOR-STATE line 175). All 8,200 configurations
  are D on both engines, kc (loop/kc/kc) and dfast18, with C 0, mismatch 0 and timeout 0. 494 configurations were run on both
  machines with 0 disagreements. Explore's verdict file is loop/k53/nl54d_verdicts.txt (md5 952575ca, per the coordinator state).
- **Studio's own two-engine runs:**
  - nl54d: rings 16-18, 610/610 D, kc + dfast18; out/job54d, final commit e09747eb5; batch aca4c7e8e.
  - nl54e: ring 15, 1,535/1,535 D; out/job54e, batch ff9c1f836.
  - Merged at da31feea.
  - Explore covered rings 6-14 (f673a0bc6).
- **Two-engine count check:** 8,202 resolved vs 8,200 because the 2 missing are the one-vertex degree-3 and degree-4
  configurations (a611525fa).
- **Earlier use:** Studio's s39o verdict (s39o_verdict.md) used the same file, b9bc6e8b, as the source of rpatN3.
- **New rerun:** the 3 Nov XR rerun (1961bb2b) re-ran kc on 3,906 nl rows at rings 14-18: 3,906/3,906 D.

## 6. Not covered here
- **The full2ball rules were not validated.** Each rule claims that some forbidden configuration embeds using the private letter p.
  Studio did not re-derive the rules or check them against its own embedding code (the l3q_masks.py machinery could do it).
- **Mapping risk, not checked.** In extract_full2ball_rules the w7 rule sides map −1 → private (p, 0, 1) and +1 → (p, 0, 2). If that
  side mapping disagrees with the l3q a2 convention, the w7 rules would kill the wrong private. A per-rule embedding check would
  settle it.
- **No lower check.**

## Files
- run/: f2bS_run.sh, the logs (st1, m7, m8, m9, m10 (stalled), m10b, c0off, c1empty, h0, h1), rules_empty.json.
- c_lean_status_pass1.txt.
- tierA/: args and Tier A inputs.
- out/job31/f2bA/: Studio's Tier A tables.
- Code: sep3r_f2bS.cpp and out/job31/st21_check_f2b.py.
