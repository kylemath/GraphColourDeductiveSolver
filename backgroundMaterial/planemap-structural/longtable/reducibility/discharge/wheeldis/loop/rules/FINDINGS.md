# What must a rule see to get past 5/17 at d = 7? (16 Oct 2026, exploratory, LP-only, no new D/C verdicts)

## 0. Pre-registration (written 07:50 UTC, before any computation in loop/rules)
- Classes: (c) transfer 5->u depends on u's whole arrangement (link + s word) and the sender slot; pairs of big
  neighbours of one 5 must agree on their overlap. Also a two-7 cluster pattern ("both 7s of a shared sender loaded").
- Guess: the 5/17 certificate's pairs of 7s (the two 7s of 66677 / 55767 / outer 7s of 55777) are mirror images over
  the whole union of their arrangements, so (c) alone stays at 5/17; it drops only when the two-7 cluster is forbidden.
- Plan changes if: (c) already drops below 5/17 with no new patterns (information alone helps), or forbidding the
  two-7 clusters still leaves t > 0 from another self-mirror closed structure (then the class needs reducibility, not info).

## 1. Reproduction
- `wlp3r.py` (= `wlp3.py`, paths moved here), no patterns: **t* = 1/2** (`wlp3_val0.txt`), as wlp3_v28val0.
- A6 certificate rechecked in exact rationals: 6/17·55667 + 1/17·55767 + 2/17·55777 + 2/17·66677 against
  2/17·R1 + 4/17·R2 (R1 = d7 link 5567576 s 5755556, R2 = link 5576576 s 5756656); all rooted words balance, so
  t ≥ 5/17. The full D-only rerun (`A6r.log`) was stopped at iter 56 (t = 2/7, rising); 5/17 is from out/wlp2_A6.txt.

## 2. Binding structure at d = 7: the pairs are mirror images, not merely equal words
- R1 senders: w0 lone 55667; w1 = 55767 (bigs u, s1); w4 = 55777 (u middle, outer w3, w5).
- R2 senders: w0 lone 55667; w1 = 55777 (u outer; middle w2, outer s1); w4 = 66677 (bigs u, w5, adjacent).
- The dual needs: both 7s of each 66677 = R2 at the same slot; both 7s of each 55767 = R1 at the same slot; outer
  7s of each 55777 = R2, middle = R1. `rules_c.py` finds each such situation consistent (letters agree on all shared
  coordinates), i.e. the union of the two arrangements is invariant under swapping the two 7s. Example: R2's 66677
  at w4 sits on edge u–w5 (common nbrs w4, w6); read from w5 it is R2 at the same slot (w3↔s4, w0↔s5).
- So the unseparated 7s are mirror images: **no rule whose information lies in the union of the two arrangements
  can separate them**, not only rooted-word rules.
- Big–big edges are balanced too: R1 has two R2 big neighbours, R2 has one R1 and one R2 (mirror), and
  2·μ(R1) = 1·μ(R2) = 4/17, so 7→7 transfers (class (b), depending on both arrangements) cancel in the dual sum.
  `rules_b.py` (class (c) + antisymmetric z on every big–big edge, receiver rows over all consistent neighbour
  arrangements) on the pool {R1, R2}: **t_low = 5/17** in tie and free modes (`b_A6cert.txt`; lower bound).

## 3. Class (c) LPs (`rules_c2.py`; y(A, j) per receiver arrangement A and sender slot j)
Rows: receiver rows = pool arrangements; sender rows = every situation whose big neighbours all have a view in the
pool, pairwise consistent on shared coordinates (lazy). A relaxation of the full class-(c) LP, so a **lower bound**,
sound up to realizability of the situations (letter agreement is necessary, not sufficient). Upper bounds for (c)
come only from rooted words (c ⊇ rooted). Modes: tie = rooted-word rule on the same rows; free = (c); nomir = drop
situations where two bigs carry the same (arrangement, slot); noLL = drop situations with ≥ 2 "loaded" bigs
(arrangement with a lone sender), i.e. pretend every such two-7 cluster is reducible.

| pool (d = 7 only) | tie | free (c) | nomir | noLL | status |
|---|---|---|---|---|---|
| A6 certificate {R1, R2} | 5/17 | **5/17** | 0 | 0 | lower bound; with A6's 5/17 upper bound ⇒ **t*(c) = t*(b) = 5/17** |
| HARD d=7 rows (5,098) | 11/39 ≈ 0.282 | **1/5** | 1/5 | — | lower bound; no ring ≤ 16 B-free D verdict can remove these rows |
| HARD d=7 + {R1, R2} | 5/17 | 5/17 | 1/5 | **1/6** | lower bound |
| hardlp certificates alone (noC, allC, d7only) | 0 | 0 | 0 | 0 | not closed (partners missing) |
Only 2,264 of 21,049 HARD slots have all partner views in the pool, so these floors are probably low. Patterns: those
the pools were generated under (§6.1 D-only set). The B-fixed D list (out/def_*.out, hash names) was **not** used.

## 4. Reading
1. Against the 5/17 certificate **information is worthless**: it is carried by mirror-symmetric two-7 situations
   in a closed R1:R2 = 1:2 structure: (b), (c) stay at 5/17 (LP), (a) too by the mirror argument. The obstruction
   is that R1, R2 are not reducible, not the rule class (this corrects README §6.1's reading for this certificate).
   Caveats: realizability of the 3 mirror situations (letter agreement; R2|R2 by hand), A6's D-only patterns.
2. Once only HARD arrangements are left, information does help: class (c) cuts the floor from 11/39 to 1/5 on the
   same rows (it separates non-mirror equal-word pairs, e.g. 55767 between A42 and A1402, both link 5567576).
3. But (c) keeps a floor ≥ 1/5 (≥ 1/6 even with every "two loaded 7s share a 5" situation declared reducible).
   The residual certificate is full 7s whose senders have 2–4 big neighbours (links 5656757, 5567557; senders
   57777, 55777, 56677). So Job 28's B-fixed loop (reducibility) is the lever; rule richness alone cannot close.

## 5. Next probe
- `whotested.py`: R1 (= A42) is HARD (4 B-free sets, rings 10–12, not D, no cfast C-candidate). R2 has only 2 of
  its 4 B-free sets in the registry (rings 9, 13; not D, no C-candidate): one pair and the triple were never tested.
  Cheapest move: dfast those two, then the B-fixed sets of R1, R2 and of the (c) 1/5 certificate (A1402 5567576/
  5655757, A1308 5567557/6657776, A2581 5656757/6595755) first in Job 28's queue; re-run rules_c2 on each new
  certificate to see whether it is again mirror-closed (then rule richness is irrelevant again).
- Replace the pool by on-demand partner generation (sep3 + slot-consistency filter) so the (c) number is an
  optimum, not a pool floor; build the mirror union R2|R2 (across 66677) as a graph and run dfast on it.
Files: `wlp3r.py`, `sep3`, `rules_c.py`, `rules_c2.py`, `rules_b.py`, `whotested.py`, `wlp3_val0.txt`, `c2_*.txt`/`.log`, `pool_*.txt`.
