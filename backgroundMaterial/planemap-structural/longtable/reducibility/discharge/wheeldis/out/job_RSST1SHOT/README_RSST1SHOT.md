# RSST-1SHOT (Studio): independent third engine for the RSST discharging fixed point

Built from `in/RSSTFP_SPEC.md` (33338de6) alone. §13 (d = 9..14) was built later from spec v2 (a7915274, branch
claude/project-thread-phexa1 @ 4e73e105d, copied to `in_spec_v2_a7915274.md`).

The only repo inputs used are `rsst_drules.v` (5ee470f8), `unavoidable.conf` (26aeba66), `rsst_verdicts.txt`
(b6f7a314), and the `prep` / `contains` logic of rsst_rows.py (c9f344bd). I re-typed that logic, and wrote my own
`.conf` parser rather than importing rsst_parse. I also used `in/inputs/dom_{A,B,C,T}.json` and parts71.txt (as a
cross-check only).

I did not open or run anything of W6r's: no pubrules.py, nothing under rsst_fp/code or rsst_closure/code, and none
of W6r's or W6b's result files before the runs finished. Two exceptions, both at the coordinator's instruction:
- W6b's DECISIONS.md (f099d732). I read it only after recording my own §7 verdict.
- Spec v2 §13. It contains W6r's d9 result tables, and I could not avoid seeing them when reading the method.
Limits respected: nice 20, at most 2 processes, python3 3.9 + numpy, no installs, no existing file modified, no
commits.

## 1. §7 (Assumption H): HOLDS. Verdict written first, in `S7_VERDICT.md`

`S7_VERDICT.md` has md5 e6e62927. It was recorded before DECISIONS.md was read; see `logs/S7_VERDICT.md5`.

**Hypotheses.**
- T is a simple sphere triangulation with minimum degree 5.
- T has no separating cycle of length ≤ 4.
- Every separating 5-cycle has a single vertex on one side (Birkhoff ring-5).

Under these, the drawn window together with the real 9+ middles is an induced subgraph of T with no
identifications, and every triangle in it is a face. So the "relaxed" host rule, extended to the privates, is
sound.

**Verdict on W6b's (a)–(d)** (DECISIONS.md §7 steps 1–4):
- **(a) Link chordless.** Correct: a chord gives a non-facial triangle at u.
- **(b) Ring-2 positions distinct, 9+ middles included.** Correct.
  - j = i+1: x is the third vertex of a face on w_i w_{i+1}, so x = s_i.
  - Otherwise, the 4-cycle u w_i x w_j has w's on both sides.
  - Note: when a shared apex s_i also appears in some seg_k, one must pick whichever of i, i+1 is not adjacent to k
    (d ≥ 5). W6b leaves this implicit.
- **(c) No extra u/w edges into R2.** Correct. rot(u) and rot(w) list every neighbour, so an extra edge would be an
  identification, which (b) excludes.
- **(d) R2 has no chord except the drawn s_{i-1} s_i at a degree-5 w_i.** Correct.
  - W6b's last case reaches "w_{i+1} has degree 5 and {a, b} = {s_i, s_{i+1}}", which contradicts the minimal
    choice of i, j, since then a and b share seg_{i+1}.
  - My version argues instead that the singleton side holds w_{i+1} plus ≥ 2 seg_{i+1} vertices. Both are fine.
  - This is the only step that uses the 5-cycle clause.
- **Gap:** none in the logic. The verdict is conditional on the frame class being internally 6-connected in the sense
  above. Like W6b's, the argument is not machine-checked in Lean.

**Brute-force check** (`code/s7_check.py`, `logs/s7_check.log`).
- It builds real windows, where a ≥ 9 vertex is drawn with its real deg − 5 privates.
- For every pair of R2 vertices it searches for an obstruction: a separating cycle of length ≤ 4, or a 5-cycle with
  ≥ 2 window vertices on each side, through the new adjacency.
- Identifications use only witnesses that are guaranteed distinct (u, the w's, and same-rotation ring-2 vertices).
- Results: d = 5 (888 windows, degrees 5..10), d = 6 (430 windows), d = 7 (198 windows). 228,744 identifications and
  202,413 chords tested, **0 unobstructed**.
- Control (`logs/s7_control.log`): drop the 5-cycle clause and unobstructed chords appear at once, e.g. 655555:
  p0.1~s2, and 555555: s5~s2. So the brute force does detect real gaps.
- A first, over-strict witness mode (u/w only) flagged false gaps; it is kept in `logs/s7_check_uwmode_tooStrict.log`.

## 2. What was built (code/, md5)

| file | md5 | role |
|---|---|---|
| rcore.py | 3d133146 | parts (§3.1–3.2: 71 parts, identical line by line to parts71.txt), window (§2), fits (§3.3–3.5), ledger (§4), `.conf` parser, containment as all-embedding requirement sets (§7) |
| rows78.py | da1ee1b8 | d7/8 domain rows: §8.1 grouping, numpy lo/hi, §8.2 minimal-member kills, §9 fields, lazy kill-every-group variant |
| run_sets.py | 67a53216 | runs all 1,243 set rows |
| fullworld.py | 34a1e1a2 | all letters free (d5, d6, and a domain-free d7/d8 world). Exhaustive DFS over the read variables with valid bounds, monotone kills, dominance (§13 A.3.2) |
| d9.py | d2389004 | §13 second engine, d = 9..14: c⁺ table, link-word DFS, per-word DFS, u as host |
| check_vectors.py / check_vectors13.py | f1ccf351 / f1385a77 | vector comparison |
| s7_check.py | 15cf1122 | §7 brute force |
| sample_check.py | b1672d87 | random 2-balls, ledger plus direct containment (no DFS) |
| onlycover.py / summarize.py / p21.py | 57eb7ca6 / d67e9404 / 5bb32c7e | tables |

## 3. Test vectors

| file | vectors | result |
|---|---|---|
| test_vectors_ext.json | 25, plus 7 all-5 d9..15 | **0 mismatches** (lo, hi, n_fits, fits fired with sure/possible, contained configs) |
| §13 A.4 vectors (spec v2) | 20, plus the 37-fit ledger list | **0 mismatches** (hi = lo, contained configs with u as host) |
| test_vectors.json | 8 | 2 exact MATCH. The other 6 differ **only** in `fills_lo_pos` / `fills_hi_pos` / `fills_hi_pos_after_proved` |

The 6 differences in test_vectors.json are a counting convention, not a computation error:
- The vectors count multiplicity only over sites that hold a relevant private.
- §8.1 says Π over **all** sites, and the coordinator's addendum B and spec v2 §12 confirm this. I follow §8.1.
- A diagnostic counter that uses the vectors' convention reproduces every one of those values.
- Everything else matches on all 8 vectors: the other summary fields, every fit touching u with its condition, and
  every listed filling's privates, lo, hi, fits fired and contained configs (`logs/vectors_both.log`).
- I did not tune the code to the vectors.

**Planted controls.**
- **hatside** (`RSST_CONTROL=hatside`): the §3.3 hat is read across x–xn instead of xp–x. This gives 14/32 ext,
  7/8 tv and 7/21 §13 mismatches.
- **notinduced** (containment without the induced test): 4 ext mismatches.
- **drop2122** (633 minus 2.122 and 0.7322, at d = 11): positive survivors appear (27,977 before I stopped it; max
  8 at 55555556556), whereas the real run has 0.

## 4. Results

### d7/8 domain sets (all 1,243 rows, spec-exact counts; `results/summary_sets.tsv`, `rows_sets.tsv`)

| set | rows | fillings | +rows dom | max hi | +fills dom | +rows K582 (max) | +fills K582 | +rows K633 |
|---|---|---|---|---|---|---|---|---|
| A | 162 | 45,994,346 | 38 | 5 | 494,980 | 0 | 0 | 0 |
| B | 495 | 424,257,897 | 98 | 6 | 2,897,748 | 4 (1) | 167,152 | 0 |
| C | 281 | 27,137,688 | 25 | 1 | 228,600 | 0 | 0 | 0 |
| T | 305 | 44,162,865 | 35 | 5 | 310,542 | 1 (1) | 1,152 | 0 |

No row was `not done`, and inexact = 0. The coordinator's kill-every-group reading (B) gives the same pass/fail; its
per-set maxima after kills are K633 0 and K582 1.

The 5 rows that depend on a none configuration:
- B 8 76576756/65555556 and T 8 56765767/56655555: 2.126.
- B 7 8557766/7565755: 124.1324817 / 2.126.
- B 7 8565766/5557656 and /5557657: 128.1324802.

### Full world, all letters free, no K3gB5n domains (fullworld.py)

| d | link classes | no-kill max (argmax) | K633 | K582: positive states left, all killed only by none (dominance-reduced) | genuine survivors |
|---|---|---|---|---|---|
| 5 | 377 | 10 (55555) | pass, all 29 positive links killed at link level by proved configs | 0 | 0 |
| 6 | 1,505 | 24 (all 5) | pass, 0 leaves | 3,917, every one needs **only 2.126** | 0 |
| 7 | 5,895 | 32 (all 5) | pass | 84,292 (29 none configs, 26 sole killers) | 0 |
| 8 | 25,395 | 28 (all 5) | pass | 55,752 (30 none configs, 23 sole killers) | 0 |

So **every d7/d8 label passes under K633 even with no domains at all.** This is stronger than the sets result. I do
not have V2ROW_SPEC §3, so I could not run the full world with K3gB5n domains. The domain-free world needs far more
none configurations than the domain sets do.

Spot check (`sample_check.py`, no DFS): 6,500 random 2-balls at d5/6/7, of which 2,648 have hi > 0. All 2,648 contain a
config. At d6, 83 contain only none configs.

### d = 9..14 (d9.py, §13; u is a host)

- **K633 passes at every d = 9..14**, with 0 survivors. Words searched: 2,905 / 1,911 / 949 / 266 / 30 / 2.
- **K582** leaves positive states, all killed only by none configs:
  - d9: 31,139 states, max 7 (555665566);
  - d10: 409 states, max 3 (5555556657);
  - d11..14: 0.
- Genuine survivors: 0.

**d ≥ 15.** The spec justifies this by c⁺ ≤ 6 per hub, which gives charge ≤ 60 − 4d ≤ 0 (§8.4: tight Karp mean −4).
In d9.py the cyclic c⁺ bound leaves 0 words at d = 15, 16 and 20.

My c⁺ table reproduces §13's checksums:
- fits per hub letter: 80 / 80 / 70 / 9;
- c⁺ max: 6, 6, 6, 4, 0.

### Needs-none (addendum A) and only-cover (item 3)

- `results/NEEDS_NONE.tsv` lists, for each none config, the rows and fillings that no proved config covers.
- `results/ONLY_COVER.tsv` and `results/needs_none_sets.tsv` give, per degree, the states each none config is in and
  the states where it is the **only** none config.

Sole killers per degree:
| degree / source | sole killers |
|---|---|
| d6 | 2.126 (3,917) |
| d7 sets | 128.1324802 (84 groups / 126,000 fillings), 124.1324817 (12 / 30,000) |
| d8 sets | 2.126 (144 / 2,304) |
| d9 | 12 configs |
| d10 | 5 configs |
| d7 domain-free world | 26 configs |
| d8 domain-free world | 23 configs |

The 12 at d9 are 439326.126 3591, 126.1306802 454, 2.126 367, 453963.126 316, 439328.136 219, 453963.364 154,
453963.136 153, 3.1324806 64, 439589.122 62, 126.442802 41, 3.1324802 31 and 443166.126 22. Adding d10's
26359326.126 gives 13 for d9..14.

Union of sole killers:
- over d5, d6, the d7/8 sets and d9..14: **15 configs** (the 13 of §13 plus 124.1324817 and 128.1324802);
- including the domain-free d7/d8 world: all 51.

**P21** (fix_404d45e819, own proved kill at d6; `results/P21_d6.tsv`): of the 3,917 d6 K582 states, 46 have some P21
row among their apex completions. **P21 wholly removes none of them**: every one keeps an apex at 9+ or a non-P21
apex word. So the d6 needs are unchanged (2.126 only).

## 5. Ambiguities and how I resolved them

1. **fills_* multiplicity.** The spec text (§8.1, all sites) disagrees with the vectors. I followed the spec, and
   the vectors' convention is reproduced by the diagnostic counter (§3 above).
2. **Kill-checking only hi > 0 groups (§8.3) versus every group (§9, addendum B).** Spec-mode fields are reported
   as `*_after`, and lazy every-group fields as `*_allkill`.
3. **u as a host at d ≥ 9.** §7 and §10.2 say u is not a host (the ext vectors match only that way), while §13 A.1
   says it is. I implemented both behind a flag: §10.2 for the ext vectors, §13 for the d9..14 engine. u as a host
   is sound (exact degree d).
4. **The displayed group filling** sets irrelevant privates to 9, even where the domain lacks 9 (§8.1 "for example
   9"). The vectors agree.
5. **Ties in argmax** go to the first group in C order (site 0 slowest, classes in first-seen domain order). This
   matches all vectors.
6. **Spec v2 §§1–12 are identical to 33338de6** except one added §12 bullet (W6b's two reporting flags). The diff is
   in `logs/spec_diff_33338de6_vs_a7915274.txt`.

## 6. Comparison with W6r / W6b after the run (allowed now)

- **d7/8 sets.** Every spec-exact count equals W6b's DECISIONS.md figures:
  - dom: A 494,980, T 310,542, C 228,600, B 2,897,748;
  - K582: T 1,152, B 167,152.
- **Positive rows** (38/98/25/35; K582 B4/T1; the 5 none rows and their configs) equal W6r §11.
- **d9..14.** State counts 31,139 / 409, maxima 7 / 3, and the 13-config hitting set equal spec v2 §13.

## 7. Not done or limits

- **Full-world d7/d8 with K3gB5n domains:** not possible, because I have no V2ROW_SPEC §3 domain generator. The
  domain-free world, which is stronger, is done.
- The 12 tneg labels not in dom_T were not separately run; they are covered by the domain-free world.
- My K633 d6 run used the pre-dominance DFS. It is a superset search, so the result is valid.
- The aborted non-dominance d6 582 log is in `logs/*ABORTED*.gz`.
- **Lean:** nothing here is machine-checked. The §7 argument is on paper plus brute force.
