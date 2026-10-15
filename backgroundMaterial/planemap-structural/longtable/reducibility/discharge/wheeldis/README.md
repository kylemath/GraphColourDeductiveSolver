# Wheel-level discharging (Long Table, 14–15 Oct 2026) [exploratory]

## 0. Pre-registration (written 23:44 MDT 14 Oct, before any computation in this folder)

**Setup.** Charge 6 − deg(v); total 12. A minimal counterexample G is an internally 6-connected triangulation,
min degree 5, containing no configuration of R. R at wheel level = the D 5-/6-wheels of `studio17/wheels17_verdicts.txt`,
the 11 Lean-certified C 5-wheels + 66666, and the 6 certified C 6-wheels (`dcheck/CWheels.lean`). The six 565xxx
6-wheels are NOT used. Link words containing a letter 9 (= degree ≥ 9) are treated as non-R.

**Rule shape.** A vertex u of degree d ≥ 7 sends x(w, π) to each adjacent degree-5 vertex v, where w is v's link word
(canonical, over {5,6,7,8,9}) and π the orbit of u's position in w. Receiver rows: u's link w_0..w_{d−1} and the
shared second-ring vertices s_i (common to w_i, w_{i+1}); every degree-5 w_i has word (u, w_{i+1}, s_i, s_{i−1},
w_{i−1}), which must be non-R; a degree-6 w_i must admit some private p_i making its 6-wheel non-R. Max over all
cyclic arrangements by a transfer-matrix DP (constraint generation). Degree ≥ 9 receivers: letter 9 sends a
d-independent amount; the bound for all d comes from the maximum mean cycle weight of the DP transfer matrix.

- **HA (prediction, expected to hold).** The wheel-level LP is INFEASIBLE. Predicted binding pair: the lone-big
  5-type 6666d (all link degrees 6 except one d ≥ 7; 66667 is "neither" in Job 17) must receive 1 from its
  only big neighbour, and a d-vertex with link 5,6,5,6,… carries ⌊d/2⌋ such 5s, so ⌊d/2⌋ ≤ d − 6 fails for
  d = 7..11 (d = 7: two 66667 senders already exceed 7 − 6 = 1). Optimal deficit t* ≥ 1/2 or so.
  *Kill:* the LP is feasible (t* ≤ 0) — then the rule is reported and checked for all d.
- **HA2.** Adding small receiver-centred configurations (a 7 with two lone-7 66667 neighbours; ring ≤ 14 where
  possible) to R, some are D- or C-reducible. *Kill:* every candidate with ring ≤ 14 is neither D nor C (cfast,
  |X| ≤ 4) — then report that wheel-plus-few-2-ball rules cannot close without ring ≥ 15 configurations.
- **HB (Task B, `Rx` of discharge README §10).** The sub-configuration argument is sound: in an internally
  6-connected triangulation with min degree 5 the 2-ball of a degree-5 vertex is regular (proved, not assumed),
  every link vertex of a first-ring x_k lies in the 2-ball with its exact degree in the key, and x_k's wheel has a
  simple ring. *Kill:* a key where `k2size_v3.link_hit` reads a link word that differs from the word read off
  `ball.build(key)`'s adjacency, or a step of the regularity proof that fails.

## 1. Task A: wheel-level LP (results, 15 Oct 2026 00:00–03:00 MDT)

**R used at wheel level** (`wlp.py`):
- the D 5-/6-wheels of Job 17;
- the Lean-certified C wheels (11 C 5-wheels + 66666; 6 C 6-wheels; the 565xxx six excluded);
- diamond and 2.122 (dfast D, `diam.txt`: ring 6 and 7);
- **D-reducible fans** (`fans.py`, `out/fans_dfast.out`). A fan is a 5-centre with 1–2 link positions F left out of
  the configuration as ring vertices, so the F degree is free (any degree ≥ 7, ≥ 9 included). 213 fans with ring
  ≤ 16 were tested. 7 are D: F5555, FF555, F5556, F5565, FF565, F5656, and **F5665**. Only F5665 is not a diamond
  pattern.
- Every 5-word with a 9 (degree ≥ 9) that no fan covers counts as non-R.

**Sender rows.** 342 non-R 5-words with a big letter. **Variables:** 942 rooted words.

**Receiver rows.** The arrangement (w_i, s_i) around u is maximised by a max-plus DP, by constraint generation, for
every d = 7..30. For d ≥ 9 the bound comes from the Karp max cycle mean λ of the letter-9 transfer matrix (a closed
walk of length d weighs ≤ dλ).

| R at the receiver | t* (exact optimum, converged) | dual certificate |
|---|---|---|
| wheels + fans only (`out/wlp_base.txt`) | **3/5** | 0.4·(55667) + 0.4·(55757) + 0.2·(a 7 with 2× rooted 7\|5566 and 4× rooted 7\|5575). Simplest instance: a 7 with link 5,5,6,5,5,6,6 and every s_i = 6 has 4 lone-7 senders (words 56667), so 4(1−t) ≤ 1+t. |
| + D 7-/8-wheels, ring ≤ 14 (`bigwheels.py`; 418 tested, 91 D: 36 c7, 55 c8; `out/bigwheels_dfast.out`) (`out/wlp_bigw.txt`) | **1/2** | 0.75·(55667) + 0.25·(a 7 carrying three lone-7 senders 55667 and one 7\|5578). Example link 5565568, s = 5665656. |
| + "a 7 has ≤ 1 and an 8 has ≤ 2 lone-big senders" (§2) (`out/wlp_bigw_cap7=1_cap8=2.txt`) | **3/7** | 2/7·(55667) + 3/7·(55757) + 2/7·(a 7 with one lone sender 7\|5566, three 7\|5575 and one 7\|5759). 55757 has two 7s, so each 7 owes it (1−t)/2, and 1 + 3/2 > 1. |

7-/8-wheels at ring 15–16: 211 of the 702 were tested (the run was stopped for CPU), and **0 were D**
(`out/bigwheels1516_dfast_partial.out`).

**HA survives: the wheel-level LP is infeasible.** The binding receiver is always a **degree-7** vertex. The binding
senders are 5s with one or two big neighbours (55667, 56667, 66667, 55757). The prediction "⌊d/2⌋ lone senders, d up
to 11" was wrong in detail: d = 7 binds first, and adjacent-5 senders (55667) pack 4 to a 7.

**Uniform rule for large d (proved at wheel level, `eqsplit.py`, `out/eqsplit_*.txt`).** *Equal split*: every vertex
of degree ≥ 7 sends 1/b to each adjacent 5 that has b neighbours of degree ≥ 7. Every non-R 5 then ends at exactly 0.

For a receiver of degree d, the maximum demand Σ 1/b over all wheel-level-consistent arrangements is:

| d | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | ≥ 18 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| max demand | 3 | 4 | 6 | 6 | 7 | 8 | 8 | 9 | 10 | 10 | 11 | 12 | ≤ 2d/3 |
| d − 6 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | d − 6 |

Here λ₉ = 2/3: demand ≤ 2d/3 ≤ d − 6 for all d ≥ 18, and the DP gives d = 16, 17 directly. **So equal split is valid
for every d ≥ 16, using only wheel facts.** The worst case is the pattern 5,5,6 repeated around u (all lone senders
55669-type). Degrees 7..15 need receiver-centred configurations.

## 2. What closes it: receiver-centred configurations (dfast, D only, engine level, not Lean)

`pairs.py D k` builds u (degree D) + k LONE-BIG senders + their links, with every degree exact. The ring is the
free completion, built with `b8b/rings.py` Layered and checked to be an induced cycle.

| family | classes | already R | tested (ring ≤ 16) | D |
|---|---|---|---|---|
| 7 with 2 lone-7 senders | 62 | 3 | 59 (rings 9–14) | **59/59** |
| 8 with 3 lone-8 senders | 298 | 42 | 256 (rings 10–16) | **256/256** |
| 9 with 4 lone-9 senders (u exactly 9) | 732 | 198 | 524 (rings 10–16; 10 more at 17–18 untested) | **524/524** |
| control: 7 or 8 with 1 lone sender (= the 5-wheel) | 5 + 5 | – | 10 | 0 (matches Job 17 "neither") |

Consequence: **a 7 has ≤ 1, an 8 has ≤ 2 and a 9 has ≤ 3 lone senders** in a minimal counterexample (engine level).
The 9 cap has one gap: the 10 ring 17–18 classes are untested. The caps for 7 and 8 move t* from 1/2 to 3/7. The
LP did not use the 9 cap: letter 9 stands for every d ≥ 9.

**Equal-split overload at a 7** (`pairs2.py 7 k`). These are the minimal sender sets with Σ 1/b > 1. The other big
neighbours are left OUT of the configuration as ring vertices, so a D verdict covers every degree ≥ 7 for them,
9+ included:
- k = 2: 706 classes, 19 already R; 687 at rings 9–15. Demand types: 1+1 (62, the same 62 as `pairs.py`), 1+1/2
  (322), 1+1/3 (242), 1+1/4 (72), 1+1/5 (8).
- k = 3: 14,638 classes, 1,444 already R. 13,107 have ring ≤ 16 and 87 have ring 17–19; 12,026 have ring ≤ 14.
Results in §2.1.

**To close d = 7..15 under equal split, R must contain every minimal overloaded configuration:**
- at a 7: k = 2..7 sender sets;
- at an 8: Σ > 2;
- at 9..15: Σ > d − 6, with u of exact degree d. The ring grows with d, and the families are not enumerated for
  d ≥ 10 or k ≥ 4 at d = 7.

d ≥ 16 needs nothing beyond wheels.

## 3. Task B: the `Rx` sub-configuration argument (discharge README §10)

**Code check** (`rxcheck.py`, `out/rxcheck.txt`).
- Every canonical K ≤ 2 key was enumerated: DMAX 8, 334,284 keys = 888 + 22,428 + 310,968.
- For every first-ring x_k of degree 5 or 6 (1,244,023 links), the word that `k2size_v3.link_hit` reads by index
  arithmetic, `[5, x_{k-1}, s_{k-1}, privs, s_k, x_{k+1}]`, was compared with the word read off the adjacency of
  `ball.build(key)`. For the second reading, x_k's neighbours are ordered as the induced cycle they form.
- **0 mismatches.** Every such x_k has all its neighbours inside the 2-ball, as many as its degree, and they induce a
  simple cycle. Both readers flag the same 96,038 keys (any status).
- Index conventions agree with `ball.py`: s_k is shared by x_k and x_{k+1}. Private order cannot matter, because a
  degree-6 x_k has exactly one private.
- A re-run of `k2size_v3.py` (copy `k2size_v3_rerun.py`, output `out/k2size_v3.txt`) reproduces Rc = 1,254,
  **Rx = 10,625** and 92,771 non-R exactly.

**Proof that "appears" holds.** G is an internally 6-connected triangulation (no separating 3- or 4-cycle; a
separating 5-cycle only around one vertex), min degree 5. v has degree 5 with link x_0..x_4.

1. *The 2-ball is regular* (`ball.ball_at`'s 'ok' case: second ring a simple chordless cycle, each y seeing exactly
   the expected x's).
   - x_i x_j adjacent for non-consecutive i, j gives the separating triangle v x_i x_j.
   - y adjacent to x_i, x_j non-consecutive gives the 4-cycle v x_i y x_j. Both sides contain a link vertex, so it
     separates.
   - y ≠ s_k adjacent to x_k and x_{k+1} gives the triangle x_k x_{k+1} y. It is not a face, so it separates.
   - A chord y z of the second ring:
     - same x_k: the triangle x_k y z separates, as y and z are not consecutive around x_k;
     - x_k and x_{k+1}: the 4-cycle x_k y z x_{k+1} has s_k on one side and v on the other;
     - x_k and x_{k+2}: the 5-cycle v x_k y z x_{k+2} has {x_{k+1}, s_k, …} on one side and {x_{k+3}, x_{k+4}} on
       the other, so it is a nontrivial separating 5-cycle.

   All are excluded. So the key model and its degrees describe G exactly. §8.4 item 5's "assumed" regularity is
   proved here for the degree-5 centre.
2. *x_k's wheel lies in the ball with exact degrees.* Its link is v, x_{k±1}, s_{k-1}, (p_k), s_k: all at distance
   ≤ 2 from v, with degrees in the key. Keys enumerate exact degrees 5..8; 9+ keys are not enumerated, so no "8 means
   ≥ 8" ambiguity arises. Ring vertices of the x_k-wheel lie at distance 3 from v. They are free in the
   configuration, so their degrees are not needed.
3. *x_k's wheel has an injective ring.* A ring vertex r adjacent to non-consecutive link vertices y_i, y_j of x_k
   gives the 4-cycle x_k y_i r y_j, with link vertices on both sides. If y_i, y_j are consecutive, r ≠ their shared
   vertex gives a separating triangle. A ring vertex is never a link vertex, and the link is induced (no separating
   triangle). Chords between ring vertices only remove ring colourings, so they are harmless to a D/C argument.
4. *C admissibility does not depend on the outside.* All 17 certified wheels used by `Rx` (11 C5 + 6 C6) have
   X = {I0-I1}, an interior edge. G/X is loopless and smaller whatever the outside is. This is not true of the 565xxx
   six (ring–ring merges), and `Rx` correctly excludes them.

**Verdict on HB: survives, sound with conditions.**
- The conditions are internal 6-connectivity + min degree 5, which steps 1 and 3 use, and the Lean caveats shared by
  every result here (DCheckSound S1/S3).
- Harmless dead code: 66666 ∈ C5x can never fire for a degree-5 x_k, because x_k's link contains v.
- No hole was found where a link degree is undetermined.

### 2.1 Equal-split overloads at a 7 (dfast; `out/eq_D7_dfast.out`, `out/eq_D7_summary.txt`)

12,713 configurations were tested: all of k = 2, and k = 3 at ring ≤ 14. Every other big neighbour is a free ring
vertex.

| demand type | D | not D |
|---|---|---|
| 1 + 1 | 59 | 0 |
| 1 + 1/2 | 286 | **24** |
| 1 + 1/3 | 130 | 108 |
| 1 + 1/4 | 24 | 48 |
| 1 + 1/5 | 0 | 8 |
| 1/2 + 1/2 + 1/2 | 1,649 | 100 |
| 1/2 + 1/2 + 1/3 | 2,674 | 1,103 |
| 1/2 + 1/3 + 1/3 | 1,424 | 1,711 |
| 1/2 + 1/2 + 1/4 | 663 | 358 |
| 1/2 + 1/3 + 1/4 | 696 | 1,315 |
| 1/2 + 1/2 + 1/5 | 48 | 56 |
| 1/2 + 1/3 + 1/5 | 45 | 184 |
| **total** | **7,733** | **4,980** |

The share that is not D rises with the number of free big vertices. Example not D:
`e7_556...6_6B....6_1110001`, ring 11. A lone 56667 sits next to a 5 with word 7,6,B,6,5, where B is free.

**Reading (HA2).** HA2 survives: many ring ≤ 14 receiver-centred candidates are D, and every lone-lone family at
7/8/9 is D. **But the equal-split rule does not close at d = 7 with D configurations and free big vertices.** The
4,980 non-D overloads would need one of three things:
- the B degrees fixed (7, 8 exactly; ring grows by the B's own neighbours);
- C-reducibility (cfast; not run here);
- a non-equal split, i.e. the LP over rooted words with these D configurations as forbidden receiver patterns. That
  LP is not built: it needs a demand-tracking DP state at d = 7.

d = 8 (Σ > 2) and d = 10..15 (Σ > d − 6) overload families are not enumerated.

## 4. Verdicts

- **Task A: infeasible at wheel level (HA survives).**
  - t* = 3/5 with the 5-/6-wheel R plus fans. It drops to 1/2 with the D 7-/8-wheels, and to 3/7 with the D lone-pair
    and lone-triple receiver configurations.
  - The binding receiver is always a 7. The binding senders are 5s with one or two big neighbours: 55667/56667/66667
    (lone) and 55757 (two 7s).
  - The uniform rule "send 1/b" holds for every d ≥ 16 from wheel facts alone, by the DP plus Karp λ₉ = 2/3.
  - d = 7..15 needs receiver-centred configurations. The lone-sender ones are all D (59 + 256 + 524). 4,980 of 12,713
    equal-split overloads at a 7 with free big neighbours are not D.
- **Task B: sound with conditions** (§3).

## 5. Process notes

- All D verdicts are dfast at engine level, not Lean.
- Twice, briefly, 8 dfast processes ran instead of the allowed 4: the D8 k3 batch alongside the ring 15–16 wheel run,
  and the eq batch for a few minutes. The eq batch was killed and restarted.
- The ring 15–16 7-/8-wheel run was stopped at 211/702 to free CPU for the receiver families.

## 6. Receiver-centred LP for d = 7..15 (pre-registration, written 15 Oct 2026 before any computation in this section) [exploratory]

**Question.** Can receiver-centred configurations close d = 7..15, i.e. drive the wheel-level LP of §1 to t* ≤ 0?

**Method (`wlp2.py`, new).**
- Same sender rows and rooted-word variables as `wlp.py bigw` (wheel R + certified C wheels + D fans + D 7-/8-wheels).
- Receiver rows for every exact d = 7..15 are generated by an exact separation search over whole arrangements
  (w_i, s_i), i < d (a DFS bounded by the max-plus DP of `wlp.py`), that **skips every arrangement containing a
  forbidden pattern**. d = 16..30 rows use the plain DP of `wlp.py`, and the Karp letter-9 bound is reported as before.
- A forbidden pattern is a receiver-centred configuration with a dfast D verdict: u of exact degree d, a sender set S,
  and the abstract rooted word (letters 5, 6, B; B = degree ≥ 7, left free as a ring vertex) of every sender. An
  arrangement contains it when some rotation/reflection puts S on degree-5 link positions whose rooted words abstract
  to the pattern's words. The B letters cover 7, 8 and 9 alike, which is what the dfast verdict (B free) covers.
- Pattern sets: lone-sender families (2 at a 7, 3 at an 8, 4 at a 9; `out/pairs_D*_dfast.out`), the 7,733 D
  equal-split overloads at a 7 (`out/eq_D7_dfast.out`), and the new families below.
- New families: the minimal equal-split overloads (Σ 1/b > d − 6) at d = 8 and d = 10..15, enumerated by `pairs2.py`
  as for d = 7, and tested by dfast at ring ≤ 16 (4 processes at most, ring order, smallest first). Families too large
  to enumerate or test completely are reported with counts by ring and the share tested.
- C verdicts: Job 27 (Studio, cfast on the 4,980 not-D overloads at a 7) is pending. t* is reported without them,
  and, as an upper bound on what they can do, with all 4,980 treated as forbidden.

**H6 (the hypothesis under test).** With every D receiver-centred configuration at ring ≤ 16 used as a forbidden
pattern, the LP reaches t* ≤ 0 for d = 7..15.

**Prediction (mine, written before computing): H6 fails.** Reasons: (i) an overload at d needs ≥ d − 5 senders, so for
d ≥ 11 or so the minimal overloads have rings > 16 and cannot be tested by dfast; (ii) 4,980 of the 12,713 tested
overloads at a 7 are not D. I expect t* to stay > 0, binding at d = 7 (if the not-D overloads still bind) or move to
d = 8..10.

**Kill criterion for H6.** t* > 0 after all D configurations at ring ≤ 16 are used as forbidden patterns. If killed,
report the binding receiver (d, link word, s word, senders) and the pattern families it would need.
**H6 survives** only if t* ≤ 0 (to 1e-7) with the Karp bound covering d ≥ 16.

All D verdicts in this section are dfast only (engine level, no second engine, no Lean): nothing here counts as a
claim. Also unproved for receiver-centred configurations: that they appear in G as built (the degree-5 regularity
proof of §3 does not cover a degree-7..15 centre).

### 6.1 Results (15–16 Oct 2026; dfast only, engine level, no second engine, no Lean)

**Correction to §2.1.** The table rows sum to **7,698 D / 5,015 not D** (12,713), not 7,733 / 4,980.
`out/eq_D7_dfast.out` has 7,698 D lines. Job 27's list (`job27/notD.txt`) has the right count, 5,015.

**Tools.**
- `wlp2.py` + `sep.cpp`: the §1 LP. Receiver rows for exact d = 7..15 come from an exact branch-and-bound separation
  (`bin/sep`) that skips every arrangement containing a forbidden pattern. Rows for d = 16..30 use the plain DP, and
  the Karp letter-9 bound covers larger d.
- Validation: it reproduces t* = 1/2 (`out/wlp2_val0.txt`) and t* = 3/7 (lone caps as patterns, `out/wlp2_lone78.txt`).
- `gen.py`: LP-guided configurations. For a receiver arrangement, every sender set S (|S| ≥ 2) gives a pairs2-type
  configuration: u + S + the links of S, with B free. Its ring is counted by an Euler formula, which matches all 18,456
  earlier builds. Greedy mode tests each arrangement's cheapest untested S until either one is D (the arrangement is
  killed) or every S with ring ≤ 16 has been tested and none is D (the arrangement is **HARD**).
- `hardlp.py`: the LP with sender rows plus HARD receiver rows only. Its optimum t_hard is a **lower bound** that no
  further D verdict at ring ≤ 16 can lower. Its dual certificates were rechecked in exact rational arithmetic.

**Configurations tested (dfast, ring ≤ 16).**
- d = 8 equal-split minimal overloads, k = 3 (`pairs2.py 8 3`; `eq_D8_k3.txt.gz`, `out/eq_D8_k3_dfast.out`):
  **3,192 D of 3,462**. All 3,462 with ring ≤ 16 are done; 10 at ring 17–18 are untested.
  - By type (D/not): 1+1+1 256/0, 1+1+1/2 1,795/6, 1+1+1/3 906/215, 1+1+1/4 214/47, 1+1+1/5 21/2.
- LP-guided sender sets from tight rows of 9 LP rounds (`out/lp_dfast.out`): **433 D of 6,345**.
  - By receiver degree (D/total): d = 7 68/1,782, 8 224/2,418, 9 133/2,045, 10 8/100.
  - Small sender sets that are not minimal overloads are mostly not D.
- d = 10..15 minimal-overload families were not enumerated in full. pairs2-style enumeration is 3^(~13+) per sender
  set, and the families run to 10^4–10^6 classes at rings 12–22.
  - Lone-sender sizes (`pairs.py d d−5`): d = 10 has 976 classes (556 at ring ≤ 16); d = 11 has 836 (263); d = 12 has
    452 (45). From d = 12 on, rings are mostly ≥ 17.
  - dfast on the d = 10 lone-5 family is running; it is reported in §6.2 if it finishes.

**Hard results: t* > 0 in both cases (H6 KILLED).**

| case | patterns forbidden | upper bound t_D (full LP) | lower bound t_hard (HARD rows) |
|---|---|---|---|
| D only (`out/hardlp_noC.txt`) | all D above + lone families + D overloads at 7 | **5/17 ≈ 0.294** (`out/wlp2_A6.txt`) | **47/163 ≈ 0.288** |
| every one of the 5,015 not-D overloads at a 7 treated as reducible (Job 27 upper bound; `out/hardlp_allC.txt`) | as above + all 12,713 overloads at 7 | **2/7 ≈ 0.286** (`out/wlp2_B4.txt`) | **24/227 ≈ 0.106** |
| same, d = 7 receivers only (`out/hardlp_allC_d7only.txt`) | — | — | **1/23 ≈ 0.043** |

- The lower bounds come from 8,015 HARD arrangements (`out/hard_rows.txt`: d = 7 5,115, d = 8 2,716, d = 9 184;
  5,771 contain no Job 27 configuration). In each, every sender set with ring ≤ 16 has been tested by dfast and is not
  D.
- So **no D verdict on receiver-centred configurations of this type at ring ≤ 16 can make t* ≤ 0**. The same holds
  with every pending C verdict counted as a success, and with d = 7 alone. No verdict on this pattern class can close
  d = 7 for rooted-word rules.
- **Binding receivers.**
  - D only: always **d = 7**. Example certificate: link 5567576, s 5755556, roots 7|5566 + 7|5576 + 7|7557. That is a
    lone 55667 sender plus a 55767 sender, whose two 7s have the same rooted word, so each 7 owes it (1−t)/2.
  - With all C counted: d = 7 and d = 8 receivers whose senders mix 7s and 8s, e.g. 7: link 5857585, s 7588575.
  - The d = 7-only certificate uses senders 57577, 57677 and 57777, i.e. 5s with three big neighbours. Example
    receivers: link 5575575, s 7777777; link 5657575, s 7755787.
- In the full LP (t_D) the binding receivers are d = 7, 8 and 9 at once; under "all C" d = 10 also binds, with 6 lone
  senders at a 10, which needs the lone-5-at-10 family. λ₉ ≈ 0.48, so d ≥ 11 are slack in both runs.
- Without C, the noC certificate needs the 9 pending configurations listed below to be not C. Each is in Job 27's list:
  `e7_556...6_5B....6_1110001`, `e7_B5B655._56.65.._1111110`, `e7_B55B565_B6.B565_1111111`, `e7_B55B56._B6B56.._1111110`,
  `e7_B55B565_B6.565B_1111111`, `e7_B55B565_.66565B_1111111`, `e7_B55B56._666B5.._1111110`,
  `e7_B55B565_.66B565_1111111`, `e7_B55B56._66656.._1111110`. The "all C" row of the table does not depend on them.

**Reading.**
- The obstruction lives in the rule class. A rooted-word rule cannot tell apart two big neighbours whose rooted words
  are equal, and many binding senders have 2–3 free big neighbours (B).
- What could still help:
  - B fixed to 7 or 8 inside the configuration (bigger rings, 17+);
  - C verdicts on the 5,912 LP-guided not-D sender sets (no cfast run here);
  - rules that look past the sender's link, e.g. the receiver's other senders.
- Untested: whether receiver-centred configurations appear in G as built (§6 caveat).
