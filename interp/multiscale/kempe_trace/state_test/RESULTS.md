# State test: do the minimal obstructing collars expose a missing state feature?

23 Oct 2026, ~80 min. Labels: [P] proved (argument given here), [M] measured (exact SAT/CSP per instance), [C] conjecture.
Code: `st.py` (dual Kempe trace, canonicalisation, state), `run.py` (populations), `run_h.py` (height-matched populations),
`minimal.py` (minimal collars vs. their one-vertex deletions), `contain.py`, `analyze.py`. Data: `pop_*.json`, `hpop_*.json`,
`minimal_vs_deletions.json`, `containment.json`, `analysis.json`. `v1/` = first population run (same design, other seeds; same conclusions).

## Setup

**Outcome.** A collar is *obstructing* iff the window-k0 collar target (`collar.Collar.target_window`) is UNSAT, with the
experiment's L, w, k0 (k0 = min window − 1 of the original half, as in `run_minbad.py`). Free vertices are at depth 1..w−1;
the seam row (depth 0) and depth ≥ w are fixed.

**State of a coloured collar**, recorded for every row r = 0..w:
- height of row r: (|t|, tau_H) from `hodge/pairrow.pair` (4 d.p.);
- dual Kempe trace of the region R_r = rows r..bottom, with row r as its outer boundary. Port i is the row edge (i, i+1),
  Tait label = col XOR col. For each Tait label γ ∈ {1,2,3}, the edges with label ≠ γ form paths through the triangles.
  The trace records which port each port is paired with (or "ends on another boundary"), the parity of each chain (number
  of triangles mod 2), and the number of closed cycles;
- canonicalised **jointly** over all rows by a single rotation/reflection plus colour permutation. A colour permutation acts
  on the Tait labels through its S3 part. A variant canonicalises each row independently.
- Localised cut data: not applicable. These are straight tubes and the collar experiment defines no cut.

Variants tested as "states": `height_row0`, `height_all` (heights of all rows), `trace_row0(+h)` (outer boundary only),
`trace_roww` (depth-w row alone), `trace_rows0,w` (rows 0 and w, jointly aligned), `prefix_0..r`, `trace_all_indep`,
`FULL` (all rows, jointly aligned, with heights), `FULL_noparity`.

**Populations**, for each of the 14 tube experiments (L = 10, 11, 12, 13, 14, 15, 18, sides A/B). The tube is rows 0..w*+2, as in `run_minbad.py`.
- `orig`: the stored half;
- `all` (150): same seam word, every vertex at depth ≥ 1 resampled (random sequential SAT sampler);
- `collar` (10): seam word and depth ≥ w kept, collar resampled;
- `deep` (80): rows 0..w−1 kept, depth ≥ w resampled;
- `below` (80): rows 0..w kept, depth > w resampled;
- `hmatch` (`run_h.py`): *other* seam words with the same (|t|, tau_H), found by random search (1–30 words, 6 interiors each).

That is 321 samples per experiment plus 6–180 height-matched samples: 6,126 tube collars in total, with 1,238 passing
and 4,888 obstructing (per-experiment counts are in the table below).

**Minimal collars.** For all 16 minimal collars, `minimal.py` rebuilds S_min, checks that it is UNSAT, and tests every
one-vertex deletion S_min − v (v at depth ≥ 1). These deletions are the matched passing collars: same seam, same cells
except one. The state of a partial region uses the primal traces of G[S ∩ R_r] (6 colour pairs) plus a presence mask,
because the dual form needs a triangulated region.

## 0. Numbers

| exp | L | w | k0 | n (obstructing/passing) | FULL states (mixed) | rows 0,w (mixed) | row w alone | row 0 + height | heights all rows | height row 0 | classes with ≥ 2 distinct colourings |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L10_A | 10 | 2 | 5 | 327 (326/1) | 252 (0) | 252 (0) | 244 (0) | 225 (0) | 66 (0) | 1 (1) | 8, all pure |
| L10_B | 10 | 2 | 7 | 363 (214/149) | 305 (0) | 305 (0) | 290 (1) | 268 (7) | 82 (31) | 1 (1) | 8, all pure |
| L11_A | 11 | 2 | 6 | 351 (349/2) | 295 (0) | 295 (0) | 295 (0) | 273 (1) | 123 (2) | 1 (1) | 9, all pure |
| L11_B | 11 | 2 | 6 | 333 (308/25) | 304 (0) | 304 (0) | 300 (0) | 279 (1) | 121 (9) | 1 (1) | 2, all pure |
| L12_A | 12 | 2 | 6 | 501 (495/6) | 438 (0) | 438 (0) | 421 (0) | 412 (0) | 46 (5) | 1 (1) | 10, all pure |
| L12_B | 12 | 2 | 6 | 501 (493/8) | 429 (0) | 429 (0) | 421 (0) | 409 (0) | 51 (6) | 1 (1) | 14, all pure |
| L13_A | 13 | 3 | 9 | 357 (139/218) | 300 (0) | 300 (0) | 289 (1) | 261 (2) | 194 (1) | 1 (1) | 7, all pure |
| L13_B | 13 | 3 | 9 | 387 (149/238) | 339 (0) | 339 (0) | 339 (0) | 302 (0) | 222 (2) | 1 (1) | 4, all pure |
| L14_A | 14 | 3 | 7 | 501 (445/56) | 426 (0) | 426 (0) | 420 (0) | 406 (6) | 334 (5) | 1 (1) | 7, all pure |
| L14_B | 14 | 3 | 7 | 501 (441/60) | 428 (0) | 428 (0) | 421 (0) | 403 (6) | 331 (6) | 1 (1) | 6, all pure |
| L15_A | 15 | 3 | 7 | 501 (491/10) | 456 (0) | 456 (0) | 448 (0) | 422 (1) | 175 (4) | 1 (1) | 8, all pure |
| L15_B | 15 | 3 | 7 | 501 (493/8) | 439 (0) | 439 (0) | 426 (0) | 396 (0) | 194 (2) | 1 (1) | 7, all pure |
| L18_A | 18 | 4 | 10 | 501 (263/238) | 427 (0) | 427 (0) | 411 (2) | 374 (10) | 310 (13) | 1 (1) | 7, all pure |
| L18_B | 18 | 4 | 10 | 501 (282/219) | 428 (0) | 428 (0) | 412 (1) | 380 (8) | 316 (13) | 1 (1) | 9, all pure |

How to read the table: each cell is the number of distinct states, with the number of *mixed* classes in brackets. A mixed
class is a set of collars that share one state but have different outcomes. The last column counts the FULL classes that
contain at least two genuinely different colourings, and reports whether their outcomes agree ("pure").

Opus A/B: the minimal-collar part is done (§3). The population runs (`run.py opus_A|opus_B`, about 4 s per sample) had not
finished when this file was written, so there are no `pop_opus_*.json` and no Opus rows in the table.

## 1. Q1: identical state, different outcome?

- **Full state (every row, jointly aligned, with heights and parity): no such pair** in 6,126 tube collars. That is 0 mixed
  classes in all 14 experiments [M].
- This is guaranteed for the primal form [P]. Row w−1 is adjacent only to rows w−2, w−1 and w, so the collar SAT instance
  sees the fixed region at depth ≥ w only through three things: the row-w word, and for each colour pair, the partition of
  row-w vertices into components of G[rows ≥ w]. Row 0 enters only through its word. So the outcome is a function of
  (row-0 word, row-w word, 6-pair primal trace at row w), aligned with each other. The dual 3-Tait-pair trace at row w
  carries the same information. That equivalence is [M]: in every sample it separated exactly as the primal argument predicts.
- **Caveat: the separation is nearly trivial.** The FULL state is close to injective: 252–456 distinct states per 321–501
  samples. The only collisions between genuinely different colourings (2–14 classes per experiment) come almost entirely
  from the `below` mode, where rows 0..w are equal and only the deeper rows differ. All of those classes are pure.
- **Outer-boundary state (row-0 height + row-0 dual trace + parity): yes, it is missing a feature.** 0–10 mixed classes per
  experiment, 129 obstructing/passing pairs with identical row-0 state [M]. The diff, by the first jointly aligned prefix
  of rows where the two states differ:
  - row 1: 116 pairs;
  - row 2 or 3: 4 pairs;
  - only at row w: 9 pairs.

  Example (L13_A, w = 3). The two collars have identical rows 0–2 and identical trace prefixes 0..2. Row 3 is
  `3030312010101` in the obstructing collar and `1303012010103` in the passing one, with tau_H(row 3) = 2.33 vs 1.87.
  The missing feature is the data at depth w: its word, its Kempe connectivity through the deeper rows, and how that is
  aligned with the seam.
- **Height is not sufficient** at any level. Seam words with the same (|t|, tau_H) have both outcomes, so `height_row0` is
  mixed whenever the height-matched population exists (all 14). The heights of all rows are mixed too, in 13 of the 14
  experiments (2–31 classes).

## 2. Q2: which component is decisive?

- **The trace at row w, jointly aligned with row 0** (`trace_rows0,w`): 0 mixed classes everywhere [M], as the [P] argument
  predicts. The trace at row w canonicalised *alone* still has 1–2 mixed classes (L10_B, L13_A, L18_A/B). So the relative
  rotation and colour permutation between the seam word and row w is itself part of the feature.
- **The trace at row 0 is not decisive.** It is a trace of the given colouring, and that colouring includes the collar
  rows, which the SAT instance is free to recolour. Its information about the fixed data is indirect.
- **The intermediate rows 1..w−1 are irrelevant** to the outcome [P], since they are free. `collar`-mode samples always
  keep the outcome of `orig`. Here the collar is rigid in fact: resampling reproduced the original colouring.
- **Parity carries no information** [P]. An {α, β} dual chain alternates its two labels, so its parity is fixed by the
  labels of its two end ports, which are part of the trace. Checked on 244,746 chains with 0 exceptions.
  `FULL_noparity` gives exactly the same classes as `FULL`.
- **Height:** constant at row 0 within a fixed-seam population, and mixed when used alone (§1).

## 3. Minimal collars vs. their one-vertex deletions [M]

- All 16 minimal collars are UNSAT. All 321 one-vertex deletions (depth ≥ 1) are SAT, which confirms minimality.
- In 2–12 deletions per collar (87 of 321 in total), the deletion changes **no** Kempe connectivity among the remaining
  vertices on any row 0..w. The primal state differs only in the presence of v.
  - When v is free (depth 1..w−1), its colour is irrelevant. What flips the outcome is the extra freedom it gives in a recolouring.
  - When v is in row w, it is the colours it forbids on its free neighbours.

  So on *partial* regions, the Kempe trace of the given colouring is not a complete state: the vertex set and the forbidden
  colours on the free vertices matter. On full tube collars this is absorbed by the fixed tube geometry and the row-w word (§1).
- **Containment:** every population collar that contains a minimal pattern (same colours on its cells) is obstructing.
  That is 1,523 collars with 0 exceptions over 14 experiments. Note that the pattern cells lie in rows 0..w and include free
  cells, so containment is a restriction to pattern-compatible fixed data, not a monotonicity theorem [M].

## 4. Q3: distinct states per L

FULL states, counted as the union over sides A and B (tubes, plus height-matched samples). A and B share one height-matched
population at L = 12, 14, 15 and 18, so those samples are counted once.

| L | 10 | 11 | 12 | 13 | 14 | 15 | 18 |
|---|---|---|---|---|---|---|---|
| samples | 690 | 684 | 1002 | 744 | 1002 | 1002 | 1002 |
| distinct FULL states | 557 | 599 | 867 | 639 | 674 | 715 | 654 |

The counts do not saturate: 65–88% of samples have a new state. These are lower bounds only. The full state space per L is
far larger, and the outcome-relevant quotient (row 0, row w, row-w trace) is about as large.

## Caveats

- Reflection c → −c is not an automorphism of the sheared tube, whose diagonal is (k, i+1)–(k+1, i). It was included
  because the reviewer asked for it, and it created no collisions.
- Seeds come from Python's per-process `hash(exp)`, so populations are not bit-reproducible; `v1/` is an independent rerun
  with the same results.
- The height-matched search is random (90 s cap), so it found 1–30 words per experiment.
- The populations are random. An adversarial search for FULL-state collisions was not done.
