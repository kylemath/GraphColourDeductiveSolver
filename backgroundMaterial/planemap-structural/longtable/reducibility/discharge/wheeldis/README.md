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

### 6.2 Stopped work (coordinator: continue d = 8, 10..15 only if the d = 7 bound passed; it did not)

- d = 10 lone-5 family (`pairs.py 10 5`): **203 of the 556 classes at ring ≤ 16 tested, 203/203 D**
  (`out/pairs_D10_k5_dfast_partial.out`, rings 10–15 so far). The run was stopped.
- Lone families at d = 13: 174 classes, rings 16–23, only 2 at ring ≤ 16. For d ≥ 13 the receiver-centred route is
  outside dfast's ring ≤ 16 range.
- None of this can change §6.1: the lower bounds there come from HARD rows at d = 7..9.

## 7. Richer rule classes for d = 7..15: bound tests for the 24 Oct K = 2 plan (pre-registration, written 15 Oct 2026 21:40 MDT, before any computation in this section) [exploratory]

**Question.** Is there any rule class, still built on the 2-ball framework, that can reach t* ≤ 0 at d = 7..15? If so,
what reducibility work does it need?

**R_opt (the optimistic R used by every bound in this section).**
- The §6.1 R: wheel R (Job 17 D 5-/6-wheels, certified C wheels), D fans, diamond, 2.122, D 7-/8-wheels, and every
  receiver-centred configuration (u of exact degree d + sender set S, |S| ≥ 2, + the links of S, other big vertices B
  free; the `pairs`/`pairs2`/`gen.py` type) that is D or C.
- **Plus, counted reducible: every configuration of these families that has not been tested.** A receiver-centred
  configuration counts as non-reducible only if dfast says not D (dfast18 at ring 17–19) **and** cfast
  (`--search`, |X| ≤ 4) finds no C-candidate. A 7-/8-wheel counts as non-reducible only if dfast says not D at its ring.
  A 6-wheel containing a letter ≥ 8 is untested (Job 17 covers letters 5–7 only), so it counts as reducible.
- Not in R_opt: 5-centred 2-ball keys (the K-key route, §8–10 of `discharge/README.md`) and anything larger than the
  receiver-centred family. Every candidate obstruction found here is afterwards tested against those larger
  configurations and the result is reported, because that is exactly the fallback the gate must price.

**Rule classes.** All move charge only from a degree-5 vertex v to an adjacent vertex u of degree ≥ 7, except (b).
- (a) y depends on v's 2-ball rooted at u (degrees of v's second ring too). This sees u's whole link word.
- (b) as §6 (rooted words), plus transfers between adjacent big vertices (7→7, 8→7), depending on both endpoints'
  2-balls (RSST-style sharing).
- (c) y depends on u's 2-ball and the position of v in u's link (receiver-side averaging).
- (G), the umbrella: any rule with finite reach, with any information.

**Test G first (cheapest; one success kills (a), (b) and (c) together).** An *isolated positive defect* is a finite
cluster Y of vertices of degree 5 and ≥ 7, with charge c(Y) = Σ(6 − deg) > 0, embedded in a sea of degree-6 vertices
(every vertex outside Y has degree 6), such that nothing in the patch is in R_opt. (A cluster of charge +1 has the far
field of a lone 5, so 12 copies placed at the 5s of a large geodesic icosahedral sphere would give a sphere with no
configuration of R_opt.)
- *Bound.* In (a), (c), and (b), charge moves only between adjacent vertices of degree ≠ 6. Y is closed under such
  moves, so summing Y's sender and receiver rows with dual weight 1 gives **t* ≥ c(Y)/|Y|**, an exact rational
  certificate. For a rule of reach ρ through 6s, the same sum over the ρ-neighbourhood N_ρ(Y) gives
  t* ≥ c(Y)/|N_ρ(Y)| > 0.
- *Search.* Small clusters (two or three big vertices of degree 7) whose every big vertex has exactly the sender sets
  of an existing not-D configuration. Seeds: the Job 27 "neither" two-sender overloads at a 7 (type 1 + 1/2 and
  1 + 1/3), then the LP-guided not-D sets. Each candidate patch is built with `b8b/rings.py` (cluster + 6-sea) and
  checked with `ball.class_check`. Then: every 5-/6-/7-wheel is checked against the lists; every receiver-centred
  configuration with |S| ≥ 2 is checked against the dfast registry, and any untested one is run (dfast, cfast).
- *Then, for any defect found:* its 5-centred 2-ball keys and the exact-degree 2-ball of each of its 7s are run by
  dfast (engine level), to see which larger family would remove it.

**Tests (a), (c), (b), run only if G finds no defect.** Lower-bound LPs in the spirit of §6.1:
- rows come from locally consistent radius-3 patches around the senders of the §6.1 HARD certificates;
- variables are tied by isomorphism of the class's information (rooted 2-ball for (a), receiver 2-ball for (c));
- order (a), (c), (b).

A class with lower bound > 0 is dead. A class whose optimistic LP reaches t ≤ 0 passes, and is sized (configurations,
rings, dfast CPU-h at about 1 h per key at ring 17 and about 165 h at ring 19; count above ring 16).

**H7 (the hypothesis under test).** Some class among (a), (b), (c) reaches t* ≤ 0 at d = 7..15 under R_opt.

**Prediction (mine, written before computing): H7 is killed by test G.** I expect an R_opt-free isolated positive
defect with two 7s and three 5s (charge +1, t* ≥ 1/5 for (a), (b), (c)), built from the 23 Job 27 "neither" overloads
of type 1 + 1/2 (a lone sender plus a 5 shared with a second 7). If one exists, the configuration families
themselves are avoidable near such a cluster, so no rule of any kind can close d = 7 with R_opt. The fix must then be
larger configurations: the cluster itself, i.e. a 7's 3-ball or its exact-degree 2-ball.

**Kill criterion for H7.**
- H7 is killed if test G finds a defect whose every configuration in R_opt has been tested and found non-reducible. It
  is also killed if, for each of (a), (b), (c), a lower-bound LP certificate gives t > 0.
- H7 survives for a class if its optimistic LP reaches t ≤ 0 (to 1e-7), with d ≥ 16 covered as in §1.
- If test G finds no defect after the planned search (seeds exhausted), that is reported as a null result, not as
  evidence for H7, and the per-class LPs decide.

**Also sized (task 4): the fallback "3-balls centred at 7s".**
- Count of the 7-centred configurations it needs, i.e. the extensions of the HARD 7-arrangements of §6.1.
- Ring-size distribution from a random sample built with the layered builder (exact-degree 2-ball: ring = third ring;
  3-ball: ring = fourth ring).
- CPU-h from the Job 22 per-ring dfast18 means.

All verdicts are engine level (dfast/cfast, no Lean). At most 4 dfast/cfast processes at once.

### 7.1 Results of test G (15–16 Oct 2026; dfast and cfast only, engine level, no Lean)

**Tools.**
- `defect.py` → `defectc.cpp` (`bin/defectc`): DFS over ring degrees around a centre of degree 5, 6 or 7. Rings < K
  take degrees 5–7, ring K and beyond are all 6. Every wheel is checked as soon as its link is complete, with wildcard
  look-ahead tables from `defect_tables.py`. The C++ port gives the same leaves as the Python version at K = 2 for all
  three centres and at K = 3 for centre 5.
- The disc's link order was checked against `b8b/rings.py` on 5,655 vertices: 0 mismatches.
- `defect_check2.py`: the receiver-centred check, done on the explicit patch.
  - When the ring of u + S + links is a simple induced cycle in the patch, the configuration is the `gen.py` one, looked
    up by key.
  - When two senders share the same free big vertex B, the ring is pinched in G. The configuration that actually
    appears then has that B inside at its exact degree. It is built from the graph and tested on its own.
  - The first checker (`defect_check.py`, key lookup only) missed this case. It wrongly passed two K = 3 candidates:
    their pinched configuration (ring 10) is D.
- `defect_verify.py`: an independent rebuild of a defect from its signature with `b8b/rings.py`, which then:
  - writes every wheel within distance 1 of Y and every receiver-centred configuration straight from the graph;
  - checks the 6-sea;
  - checks for separating 3-/4-cycles and nontrivial separating 5-cycles within distance 3 of Y;
  - checks for diamond and 2.122;
  - prints the closed-set certificate.

**Search.**
- K = 2 (cluster within distance 1 of the centre): **no** candidate with c ≥ 1 for any centre.
- K = 3, complete: **153** wheel-level candidates (`out/defect_K3_candidates.txt`): 142 with c = 1, 11 with c = 2. **All 153 are
  removed** by receiver-centred configurations. Tests: 138 dfast runs (`out/def_r1.out`), 181 + 3 cfast runs
  (`out/def_r1.cfast`, `out/def_open2.cfast`), and the pinched configuration (`out/def_k3g.out`).
- K = 4: these runs were **partial**, stopped for CPU.
  - Centre 5: 4,370 candidates checked. Needed 45 dfast + 101 cfast runs (`out/def_k4c5.out`,
    `out/def_k4c5[ab].cfast`). **3 survive.**
  - Centre 6: 11,333 checked (`out/def_k4c6.out`). **2 survive**, 2 still open.
  - Centre 7: 253,839 candidates not checked.
  - Survivors: `out/defect_K4_survivors.txt`.

**A defect that survives R_opt, fully verified: D3** = `5|55667|776675755|75576667557657` (centre 5; the ring degree
words follow, then all 6).
- Y has **11 fives and 10 sevens; c(Y) = +1**, and every other vertex out to distance 4 has degree 6.
- The 10 sevens have 4, 4, 3, 3, 3, 3, 2, 2, 1, 1 five-neighbours. Two of the 5s are lone senders (57665, 56675). The
  others have 2–4 big neighbours (55777, 67757, 75757, 77775, 75667, …).
- `defect_verify.py`:
  - no separating triangle, no separating 4-cycle and no nontrivial separating 5-cycle within distance 3 of Y;
  - no diamond or 2.122;
  - no 5- or 6-wheel word in R (Job 17, fans, the six 565xxx counted as R);
  - 83 configurations taken from the graph: 43 wheels (5-, 6- and the ten 7-wheels) and 40 receiver-centred, 4 of them
    the pinched in-G versions. Rings 8–14.
- **All 83 are not D** (dfast, `out/def_verify_K4.out`) **and have no C-candidate** (cfast |X| ≤ 4:
  `out/def_verify_D3_[012].cfast` for the 73 non-7-wheels; `out/def_w7_D3_[012].cfast` for its eight 7-wheel words).

**Other survivors, under the pre-registered R_opt only.**
- The pre-registration tested 7-wheels for D only. A cfast run on 7-wheels shows that many are C-candidates: 11 of the
  first 18 not-D 7-wheels tested (`out/def_w7_part1.cfast`). One of them is **5666567** (|X| = 4, triad;
  `out/def_verify_K4_[012].partial.cfast`). Counting C-candidate 7-wheels as reducible is stricter than
  pre-registered, so it can only make the kill harder.
- D1 (`5|55667|767666675|765757557756665`, |Y| = 19), D2 (|Y| = 21), E1 (`6|556667|65766755757|5767557666666666`,
  |Y| = 17) and E2 (|Y| = 19) all contain the 7-wheel 5666567. They survive the pre-registered R_opt but not the
  strict one.
- **D3 survives both.** Its eight 7-wheel words have no C-candidate.

**Certificates (exact rationals; dual weight 1 on every row of Y).**
- Summing the sender rows (Σ out ≥ 1 − t) of D3's 11 fives and the receiver rows (Σ in ≤ 1 + t) of its 10 sevens
  gives 11(1 − t) ≤ 10(1 + t), so **t* ≥ 1/21**.
- Transfers between adjacent big vertices cancel inside Y, because every big neighbour of a vertex of Y is in Y.
- This holds for **(a), (b) and (c)**, and for the rooted-word rules of §6.

| rule class | lower bound on t* | binding receivers | upper bound on t* |
|---|---|---|---|
| (a) sender's rooted 2-ball | **1/21** (D3, strict R_opt); 1/17 (E1, pre-registered R_opt) | the ten 7s of D3 | ≤ 5/17 |
| (b) + 7→7 / 8→7 sharing | **1/21** (Y closed under big adjacency; the sea is 6) | same | ≤ 5/17 |
| (c) receiver's 2-ball | **1/21** | same | ≤ 5/17 |
| any single-round rule with reach ρ and information radius r, through 6s as well | 1/\|N_{ρ+r}(Y)\|: 1/43, 1/68, 1/97 for ρ + r = 1, 2, 3 | | |

The upper bound 5/17 is the §6.1 rooted-word optimum with D-only patterns. Every class here contains the rooted-word
rules, and R_opt ⊇ the D-only R.

The last row needs an argument, because 6s may also send charge:
- A 6 whose information radius does not reach Y sees a flat hexagonal patch.
- That view is invariant under the half-turn, so two such vertices send each other equal amounts.
- Net flow across the boundary of N_{ρ+r}(Y) is therefore 0, while the charge inside is +1.

**Verdict: H7 KILLED** (pre-registered kill criterion: test G found a defect whose every configuration in R_opt is
tested and non-reducible). No rule class in (a), (b), (c) reaches t* ≤ 0 under R_opt, and **no local rule of any kind
can**. The receiver-centred family with B free is locally avoidable.

The cone argument of §7 (twelve copies in a geodesic sphere would make R_opt avoidable globally) was not carried out
here; no sphere was built.

**What removes the defects (engine level, `out/def_bigger16.partial.out`, ring ≤ 16, partial run).**
- *"B fixed" receiver-centred configurations*: u + S + every link vertex of S at its exact degree, with the shared 7s
  inside. D for all three of D1–D3: 2 of 29, 3 of 34 and 12 of 60 tested, **rings 12–15**. Examples:
  `D3_BF_5_0-13` (ring 12) and `D1_BF_5_0-1-14` (ring 14).
- *5-centred 2-balls with three or more big vertices* (the K-key family beyond K = 2): D at **ring 14–15** for each of
  D1–D3 (`D3_K5_0`, `D1_K5_0`, `D1_K5_2`, `D2_K5_0`).
- The exact-degree 2-balls of the 7s have rings 16–20, and the cluster itself (N_1(Y)) has ring 24. Neither was needed.

### 7.2 Sizing (task 4 and the blanket alternatives; `k2plan_size.py`, `out/k2plan_size.txt`)

CPU-h use the Job 22 dfast18 per-ring means. Nothing in this subsection was run.

| family | configurations | ring ≤ 16 | ring 17–19 | ring ≥ 20 (no engine) |
|---|---|---|---|---|
| B fixed (7, 8 or free) variants of the 4,008 B-free overloads at a 7 that are neither D nor C-candidate | 557,130 | 203,801 (2,800 CPU-h) | 259,769 (≈ 514,000 CPU-h) | 93,560 |
| same at an 8 (270 not-D) | 3,114 | 1,605 (24 CPU-h) | 1,384 (1,943 CPU-h) | 125 |
| **fallback, exact-degree 2-balls at 7s** (completions of the 5,115 §6.1 HARD 7-arrangements; privates 5–8) | 4,220 of the 5,115 contain a letter 9 and have no exact 2-ball; the other 895 give 1.57·10^7 | 44,160 (874 CPU-h) | 318,208 (≈ 9.8·10^5 CPU-h) | 1.53·10^7 |
| **fallback, 3-balls at 7s** (ring = fourth ring) | 4^13 to 4^40 completions per 2-ball | 1.1% of a random sample have ring ≤ 19 | | median ring 39, max 77 |

- With one completion per arrangement (all privates 6), the exact-degree 2-balls at 7s have rings 14–34, mostly 19–24.
- The ringf ring formula was checked against the layered build on 334 sampled B-fixed variants: 334 agree.
- **Reading.** No blanket enumeration is feasible:
  - 3-balls at 7s: rings are mostly ≥ 20, beyond every engine here;
  - exact 2-balls at 7s: about 10^6 CPU-h at rings 17–19, and 10^7 configurations at ring ≥ 20;
  - B-fixed variants: about 5·10^5 CPU-h.
- The configurations that actually removed the defects (§7.1) are few and small (rings 12–15). That argues for a
  *guided* loop instead: find a defect or a hard LP row, test only the configurations that kill it, and repeat.
