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
