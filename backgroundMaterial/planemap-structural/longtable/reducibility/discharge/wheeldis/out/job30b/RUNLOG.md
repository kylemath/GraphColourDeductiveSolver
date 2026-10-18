# Job 30 part B (Rule T), Studio, 18 Oct

Spec: loop/opus/G_ruleT_lp/FINDINGS.md, option B (z read as small/big), with the floor reasoning in
H_floor_check/FINDINGS2.md (branch claude/project-thread-7uelj0). Code: sep3xt.cpp → bin/sep3xt, and wlp3xt.py.
This reworks the parked draft (studio/job30-ruleT-wip, 97bbe5d7).

## Model
- Y[r, f_a, f_e]: the five's share to its root u. The flag is "that spoke is 6 and the vertex beyond it is big".
- T[r, f_a, f_e, side]: the share routed across the 6 to z. Everything is keyed up to the reflection, which swaps the
  flags and the side.
- Sender rows: one for every non-R five word and every small/big assignment of the far vertices on its {6, big}
  spokes. Assignments are coupled through each 6-spoke: its wheel (5, x+1, zR, q, zL, x-1) must be non-R6 for some
  letters in the flag sets.
  Each row: Σ_{big roots} (Y + Σ_{flagged sides} T) ≥ 1 − t.
- Receiver, outflow: the link five at w_i uses Y[r, f], with f read from w_{i±1}, w_{i±2}.
  - In the bound this is the max over flags on the 125-state DP, which is admissible.
  - The exact var is charged once w_{i−2..i+2} are fixed (sep3x's RES table), as a correction ≤ 0.
  - Separation stays exact; only the bound is weaker than the 625-state version.
- Receiver, inflow: each s_j = 5 with {w_j, w_{j+1}} = {6, big b} receives the largest current T over the five's
  unknown letters (conservative per-transition version, 6-wheel side condition dropped). That completion's var goes
  into the row; one row per completion, generated lazily.
  - Any inflow means all start letters are searched.
- d > DMAXP rows and the Karp tail: max over flags plus inflow (conservative).

## Counts
- 1,356 Y and 1,194 sender rows: both equal Opus's option-B counts.
- 444 T vars vs Opus's 504 (resolved, `loop/studio/tc/tdiff.py`, `tdiff.out`). The difference is a side-label slip in
  tcount_flag.py: it appends the side after `key()` has possibly reflected the word, so 201 reflected roots get the
  wrong side.
  - Its T2 contains 231 impossible keys, e.g. ((7,5,5,7,6), 0, 1, 'a'): a T across side a, whose letter is 5.
  - Recomputing Opus's own enumeration with the physical side carried through the reflection gives exactly
    Studio's 444 keys.
  - All 444 Studio keys have the side letter 6 and that side's flag set.
  - Explicit pairs: (7,6,6,5,5) across side a → ((7,5,5,6,6), 0, 1, 'e'); (8,6,7,5,5) → ((8,5,5,7,6), 0, 1, 'e');
    (7,6,5,6,6) → itself, side a.

## Validation
- (2) z reads what the five sends (TCHECK): every T var (444) is receivable at its z through the inflow table, and every
  receivable var is a T var. No stray on either side.
- (1) Charge conservation: each T is a column with −1 in the sending five's rows and +1 in exactly the receiver rows
  where it is that inflow slot's chosen completion. The bijection above means every sent T has a receiving slot type.
- Weights (TSELF): random Y and T over d = 7..10 give 160 separated rows (12 with inflow). The separator's weight
  equals the Python row value to within 5e-10.
- (3) T = 0, flags merged (tmerge tzero):
  - Separator: byte-identical to sep3xf on the 6 regression queries.
  - Full LP: run t0val (notx, round-13 registry, warm tight_13). It must give 7/27 and the j28_13 dual
    (55667, 55767, 77777, d = 7 5675765/6577575; duplicate sender rows may split a dual weight).

## Run B (after A converges): A's registry plus round 38 (twoeng glob), L2 + Rule T, warm from A's final rows
- H30B: t*(A+T) < t*(A).
- Kill: t*(A+T) = t*(A) with FEASIBLE.
- Exactness: `feascheckt.py` (exhaustive sep3xt, letter-9 DP, Rule T sender rows) on B's solution must print FEASIBLE.


## Inputs for B (18 Oct, ~12:10Z; Long Table 11:43Z), prepared on the coordination core
`loop/studio/k42map/map42.py` maps explore's round-42 kills (loop/k42) into receiver windows.
- **The privates are outside u's arrangement.** u's LP row has only w_i and s_i, so no NF pattern on u can state p
  letters, and none of the 20 k42 configurations is a pattern on u's rows.
- **All six privates lie in the frames of w2 and w4** (d = 7). p2a/p2b are w2's link vertices and p1 is w2's s-vertex
  between w1 and s1; likewise p4a/p4b and p5 for w4.
  - A configuration whose image lies in F + link(F) + s-ring(F), for F in {w2, w4}, becomes a receiver window
    f7_<link>_<s> of F. It forbids every d = 7 arrangement matching it, which is valid wherever it occurs.
  - The s-frames of R*'s other 7s (s2, s3, s5) reach past the built patch, so they were not used.
- Soundness check, independent of grow.py: the configuration's interior must embed (exact degrees, induced,
  triangles onto triangles, networkx) into the window's receiver-arrangement model. A frame is skipped if two s
  images flank an unspecified link letter. sep3xf matcher test (`matchtest.py`) on the 10 windows: 1,159 base-allowed
  frames, 0 mismatches.
- Verdict sets:
  - "C cons." = kc -C's conservative X, accepted by cfast --fixed with leftover 0 (k42/cut_kcc.out, cut_fixedkc.cfast).
  - "D" = dfast D and kc D.
  - "C broad" = cfast's search X, accepted by kc -C2 -x with leftover 0 (loop/k3studio/k42broad_C2.kc, run here;
    kc -C2 was validated against cfast on two-ring-vertex X shapes in explore round 40, ad376d04). Under -C, kc rejects
    that X (k42broad_C.kc).
- Per configuration:
| k42 tag | configuration | verdict set | result |
|---|---|---|---|
| k42_f7_5566757_ooo5ooo_6xx55xxx | explore C | C cons. | PASS f7_7665575_5...... (C) |
| k42_f7_5566757_ooo5ooo_x6xxx55x | explore C | C cons. | PASS f7_7575566_......5 (C) |
| k42_f7_5667576_oo5oooo_6xx56xxx | explore C | C cons. | PASS f7_7665675_5...... (C) |
| k42_f7_5667576_oo5oooo_x6xxx65x | explore C | C cons. | PASS f7_7576566_......5 (C) |
| k42_rsst003_xx5xxxxx | RSST 2.126 | C broad | fail: leaves w2/w4 frames |
| k42_rsst025_xxxxxxx5 | RSST 122.126 | C cons. | fail: leaves w2/w4 frames |
| k42_rsst031_6x555xxx | RSST 122.368 | C cons. | PASS f7_.6655.._.5..... (C) |
| k42_rsst031_x6xxx555 | RSST 122.368 | C cons. | PASS f7_...5566_.....5. (C) |
| k42_rsst062_6xx55xxx | RSST 3.3700806 | C cons. | fail: leaves w2/w4 frames |
| k42_rsst080_6x655xxx | RSST 2.3701166 | D | fail: leaves w2/w4 frames |
| k42_rsst095_6x665xxx | RSST 2.3711966 | C cons. | fail: leaves w2/w4 frames |
| k42_rsst136_6x5xxxxx | RSST 2.490806 | C cons. | PASS f7_766...5_55..... (C) |
| k42_rsst136_x6xxxxx5 | RSST 2.490806 | C cons. | PASS f7_75...66_.....55 (C) |
| k42_rsst137_6xx5xxxx | RSST 122.1031 | C cons. | fail: leaves w2/w4 frames |
| k42_rsst137_x6xxxx5x | RSST 122.1031 | C cons. | fail: leaves w2/w4 frames |
| k42_rsst142_6xx5xxxx | RSST 126.8168 | C broad | PASS f7_7665..5_5...... (Cbroad) |
| k42_rsst142_x6xxxx5x | RSST 126.8168 | C broad | PASS f7_75..566_......5 (Cbroad) |
| k42_rsst187_6xx65xxx | RSST 126.61686 | C cons. | fail: leaves w2/w4 frames |
| k42_rsst187_x6xxx56x | RSST 126.61686 | C cons. | fail: leaves w2/w4 frames |
| k42_rsst189_6xx65xxx | RSST 126.490086 | C cons. | PASS f7_76665.5_5...... (C) |
| k42_rsst189_x6xxx56x | RSST 126.490086 | C cons. | PASS f7_75.5666_......5 (C) |
| k42_rsst217_6x6xxxxx | RSST 2.211701966 | C cons. | fail: leaves w2/w4 frames |
| k42_rsst251_7x55xxxx | RSST 2.504980 | C cons. | fail: leaves w2/w4 frames |
| k42_rsst251_x7xxxx55 | RSST 2.504980 | C cons. | fail: leaves w2/w4 frames |
- **Claim-grade windows: 10 C** (RSST 122.368, 2.490806, 126.490086, and explore's f7_5667576 / f7_5566757 frames,
  each in its w2 and w4 orientations): `k42map_C.cfast`. **[broad] windows: 2** (RSST 126.8168 in w2 and w4):
  `k42map_C_broad.cfast`, kept out of the claim LP. RSST 2.3701166 (the D) and RSST 2.126 leave both frames
  (2.3701166 through u's s0), so they cannot enter.
- Forced private letters (p5 ≥ 6; s1 = 6 ⇒ p1 ≥ 7, p2a ≥ 6, (p2a, p2b) ≠ (6, 5); s4 = 6 ⇒ p4b ≥ 6, (p4a, p4b) ≠ (5, 6)):
  - B's option-B sender rows read only small/big z flags, so they cannot carry these.
  - The LP feels them only through the 10 windows on w2/w4's receiver rows, and only for configurations inside those
    frames.
  - The rest needs option F (full z and p letters in the five's 2-ball words), which Long Table ordered pre-built.

## Long Table ruling (11:52Z): RSST 126.8168 enters B's claim load, tagged [E2, broad X]
- Windows: f7_7665..5_5...... and f7_75..566_......5, now appended to `k42map_C.cfast`, so B's claim load is 12 C windows.
- Reason: the X is cfast's own search X, so it is admissible under the C definition the registry already rests on.
  kc -C2 independently reaches leftover 0 on the same X (k3studio/k42broad_C2.kc). kc -C2 was validated against cfast
  on 483 configurations of that X shape in explore round 40 (ad376d04, 0 mismatches). That meets the same-X
  two-engine rule. The exploratory second B run is dropped.
- The 10 non-fitting k42 hits and RSST 2.3701166 go to option F.

## Validation (3) result: t0val converged (18 Oct ~12:10Z, 339 iterations, 33,295 rows)
- T = 0 with flags merged (notx, round-13 registry, warm tight_13): **t* = 7/27, with the j28_13 dual reproduced
  exactly**: 10/27 sender 55667, 5/27 sender 55767, 2/27 sender 77777, 10/27 receiver d = 7 5675765/6577575.
  (The sender rows are printed with their flag bits; merged flags make the bit rows duplicates.)

## Run B launch (18 Oct ~17:25Z, Long Table 17:16Z: start B now, in parallel with A)
- Model: wlp3xt (option B, Rule T) + L2 transfers (xcap 3).
- Registry: A's (run29b's + addA) + twoeng at launch (3 D, 11 C, now including the two n1 C windows
  f7_.557657_.56.77. and f7_5567567_56.77.6, 8fd1fe03 / a2c5e767) + k42map_C.cfast (12 windows, 2 of them [E2, broad X]).
- Warm start: A's latest row dump (out/wlp3x_j30A_x_rows.txt, iteration 5, 103,736 rows); each row is re-checked by sep `c`.
- H30B: t*(A+T) < t*(A). Kill line: t*(A+T) = t*(A), with FEASIBLE (feascheckt).
- A is capped at iteration 20 (capA.sh). The A snapshot (re-solve of A's iteration-5 rows + exhaustive feascheck) runs
  in parallel (snapA.sh).
