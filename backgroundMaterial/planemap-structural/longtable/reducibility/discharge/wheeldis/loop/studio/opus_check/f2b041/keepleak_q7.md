# keepleak_q7: the 5 q7-_ k3p C entries that leaked into the keep tables (Studio, 4 Nov)

**Result: the 0.041565 upper does not need them.**
- The clean rebuild, keep95p131f (without the 5), is **FEASIBLE** for sol_c_repaired at 0.041565:
  - receivers d = 7..17: 0 exact violators;
  - senders: 0 violated, min slack 2.07e-7;
  - DP 18..30: clean;
  - Karp tail: λ = 0.633625577.
- The 5 are now also re-proved C anyway (Q5: two engines + Lean), so both routes close the gap.

## The leak
- **The bug:** Studio's keep filter, used in the keep, keep95 and keep95p131 builds, recognised a cfast header with
  `^([A-Za-z]\w*_\S+) `. That pattern misses names whose prefix before the first `_` has a non-word character, and names with no
  `_` at all.
- **Audit against every source file** (the table inputs and every cpat= file of the strict args):
  - **Table inputs:** only `q7-_` is missed, i.e. 5 entries in tierA/k3p_C.cfast. They stayed in the k3p_C_keep*.cfast copies.
  - **Receiver cpat files:** hash-named headers are also missed:
    - 13 k… names in c_all.cfast;
    - 17 g… names in def_k4c5a.cfast, def_k4c5b.cfast and def_loop_new1_2.cfast;
    - 4 h… names in hl3c.cfast.

    These have no effect. st21 makes receiver C patterns only from `^[epf]\d+_` names, so these never enter as patterns, kept or
    not. The receiver pattern count is 608 with either filter.
- **The 5 leaked entries:**
  - q7-_....556_...756._::::::5_p3R1/s3=5
  - q7-_....556_...756._::::::5_s3#2=5
  - q7-_...5566_...56.._:::::5:5
  - q7-_....556_....567_5*::::::5
  - q7-_...5566_...567._:::::5:5
- **Other lists:**
  - keep, keep95 and keep95p131 all contained the leaked 5 in their tables. keep and keep95 stay INFEASIBLE, so the conclusions
    stand, since the leak only strengthened them.
  - The rsst118 and CK108 lists were built from names, not from this filter, and are unaffected. They contain no q7-_ entry.

## (a) Q5: the 5 re-proved C (ckq5/)
- **Two engines** (Studio kc 07e79fae, cfast de59e72f; results5.tsv): all 5 have kc -C X = {I0-I1}, and cfast --fixed gives
  leftover 0. All 5 are C on both engines with the same X. None is D, and none is rim-pinned.
- **Lean** (ckq5/lean/, built on ~/studio_lean_builds/rsst118_fb35d2d1):
  - CKQ5: q5Entries_ok (XRData.ok: admissibleX ∧ foldSafeX ∧ the side condition), exit 0.
  - Q5All: hC_0..4 and hC_all by native_decide, exit 0, sorry 0.
  - Axioms: propext, Classical.choice, Quot.sound, plus native_decide aux.

## (b) keep95p131f, the clean rebuild (keep95p131f/)
- **Filter:** keep_filter_fix.py (25734d56). A header is any non-indented line whose second field is `r=…` or a digit. The same
  rule was used for the table C files.
- **Forbidden set: 12,268** (keep95p131 has 12,273). The k3p C file keeps 1 entry and drops 5.

| artifact | md5 |
|---|---|
| keep list | 4fbc0b93 (= keep95p131) |
| k3x C | cd81c111 (= keep95p131) |
| k3p C | 3c0de547 |
| args | affcf34f |

**Diff against keep95p131** (diff_vs_keep95p131.txt):
- **§14' kill tables:** 0 cells changed. The md5s are identical: kill_U7 f2d89893, U8/U9 c9e2d251, kill6_U7 c0527d29,
  kill6_U8/U9 618eb300.
- **V7 / V8 masks:** 0 kills changed (f4b86569 / 2e8e8f5e).
- **Studio-derived rules: exactly 70 lost and 0 gained** (rules_studio_keep95p131f.json, 45a4c6d1). These are exactly the 70 that
  rule_provenance.tsv attributes only to the 5.

| d7_w6 | d8_w6 | d9_w6 | d7_w7 ±1 | d8_w7 ±1 |
|---|---|---|---|---|
| 2,455 → 2,437 | 1,756 → 1,738 | 481 → 463 | 1,444 → 1,440 each | 908 → 904 each |

- **Outside rules:** all 5,954 pass on keep95p131f. None needed the 5.
- **Receivers:** 608 C patterns. Dry run: D 18,159 / C 608 / RPAT 158.
- **Self-test:** 6,000 arrangements, 0 mismatches, 0 positive.
- **Provenance:** keep95p131f/rule_provenance.tsv.

**Upper, sol_c_repaired (e0ad3fcc) at 0.041565, on keep95p131f: FEASIBLE** (keep95p131f/run/f_d*.log).

| d | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| exact violators | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| time | 228 s | 1076 s | 1491 s | 623 s | 325 s | 137 s | 56 s | 20 s | 7 s | 3 s | 1 s |

Senders: 0 violated. DP 18..30: clean. Karp λ = 0.633625577.

## The kept k3p C entry
- **The one k3p C entry kept** in keep95p131f is **q7u_.556676_.5...6._::::::5**. It is one of the 13 k3x C names of the cover, not
  Lean531 or CCover3.
- **It is backed by CK108:**
  - two-engine C with kc X {I0-I2};
  - CK108.lean entry 5 (XRData.ok);
  - `K108V.hC_5` in module K108V00, exit 0, sorry 0.
  - The CK108 hC_all assembly comes when the remaining modules finish.
- **Opus's `q7-_....556_....56._::::::5` and `…_s5/p6L1=5` are not this entry.** They are tierA/k3p_D.out lines 1–2, "D=true (two
  engines …)", i.e. k3p **D** entries. They are kept in every keep set and need no C proof.

## C side of the keep95p131f upper
| entries | Lean backing |
|---|---|
| 531 | Lean531 |
| 118 RSST C2cons | CR118 / R118All |
| 13 k3x C + 95 core95 | CK108: 111 lines; hC in progress, 9 of 19 modules done |
| 5 q7-_ | Q5 (no longer needed by the upper) |

When CK108 finishes, every C entry of keep95p131f is Lean-backed: **531 + 118 + 108 = 757** names, which equals keep95p131f_C.txt.
