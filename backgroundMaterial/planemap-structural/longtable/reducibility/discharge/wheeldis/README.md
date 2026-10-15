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
| 9 with 4 lone-9 senders (u exactly 9) | 732 | 198 | 524 (rings 10–16; 10 more at 17–18 untested) | see §2.1 |
| control: 7 or 8 with 1 lone sender (= the 5-wheel) | 5 + 5 | – | 10 | 0 (matches Job 17 "neither") |

Consequence: **a 7 has ≤ 1 and an 8 has ≤ 2 lone senders** in a minimal counterexample (engine level). These caps are
what moves t* from 1/2 to 3/7.

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
