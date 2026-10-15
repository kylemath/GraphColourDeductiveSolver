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
