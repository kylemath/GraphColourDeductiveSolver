# Vacancy D-reducibility: joint-outside refinement and the 2-ball family

Math worker, 6 October 2026. Label: **[computed, exploratory]**, plus [hand] where marked. Not committed. `vdred.py` and `verify.py` are unchanged.

The run stopped early on the Math lead's instruction (13:01): the battery was low, so no further code was run. Total CPU used was about 6 min of the 10-min cap; 200 s of that went to one aborted run (section 5).

New files in this directory: `vdred_joint.py`, `verify_joint.py`, `outside_sampler.py`, `joint_witnessed.py`, `joint_targeted.py`, `family.py`. Logs: `joint_run_log.txt`, `verify_joint_log.txt`, `joint_witnessed_log.txt`, `joint_targeted_log.txt`, `family_log.txt`.

## 1. What joint realisability really constrains

**(a) The suggested premise is false [hand].** The suggested premise was that "two splits' matchings determine the third". Counterexample: take the 4-ring coloured 0,α,β,γ.
- M_α and M_γ are forced: each has only two transitional edges.
- M_β has two possible matchings, one for each diagonal chord of the outer square.
- Both are realised by one-chord outsides.

So M_β is not determined by the other two.

**(b) Every triple is realised on small rings [computed].** `outside_sampler.py` generates random triangulated outer discs with boundary 0..m−1. It starts from a wheel and applies random stackings, unstackings and interior flips; outer chords are allowed. For each disc it enumerates all 4-colourings and records the triple of Tait matchings. Every recorded triple is witnessed by an explicit outside, so it is certainly realisable.

| m | triples realised / all non-crossing triples | pairs realised / all pairs |
|---|---|---|
| 4 | 10/10 | 23/23 |
| 5 | 40/40 | 80/80 |
| 6 | **295/295** (up to 9 interior vertices) | 470/470 |
| 7 | 1923/1925 (2000 discs, up to 11 interior vertices) | 2413/2415 |

The ring-7 count was still rising when sampling stopped.

**Conjecture J.** For every proper ring colouring, the three matchings are independent: every triple of non-crossing perfect matchings is realised by some outside. It is proved by witnesses only for m ≤ 6.

If J holds for a ring length, then restricting the adversary to jointly realisable triples changes nothing at that length: the original `vdred.py` adversary is already exact on outside patterns.

**(c) A refinement that holds regardless of J [hand].** Suppose a swapped θ-component C contains no ring vertex. Then C is a whole component of T − v lying inside K − R. The ring colouring and the outside colouring do not change, so **all three matchings survive**. `vdred.py` forgets the other two splits' matchings after every swap; that is safe but loses information.

## 2. vdred_joint.py (built, run and verified)

**State.** Knowledge is a partial triple K = (K₁, K₂, K₃), each entry unknown or a matching. One real outside is fixed throughout.

**Rules.**
- **Reveal.** The adversary chooses M_θ so that K + M_θ lies in an allowed triple for the current ring colouring. Allowed sets:
  - `full`: every triple is allowed. This is a sound superset of the realisable triples.
  - `witnessed`: only sampled realised triples are allowed. This is a subset, so only a NOT-reducible verdict transfers to the exact game.
- **Swap.** M_θ is always kept. If C is ring-free, all knowledge is kept; otherwise only M_θ is kept.
- **Splits.** Switching splits no longer erases knowledge.

**Soundness [hand].**
- Every known entry is always the true matching of the fixed real outside.
- The `full` adversary may choose anything the real outside does.
- So the soundness argument of README §2 carries over unchanged.
- Since knowledge only restricts the adversary, V_joint ≤ V_vdred on every state.

**Verification (`verify_joint.py 6`)** [computed]: 26 explicit triangulations, all with **0 violations of check A and 0 of check B**:
- T4 and 6 flipped completions;
- A₃ and 6;
- A₄ and 6;
- pentakis and 1.

**Results with the `full` adversary (sound):**

| 2-ball | vdred | vdred_joint |
|---|---|---|
| T4 (5,5,6,6,5), ring 7 | reducible, depth 7 | reducible, depth 7; two states improve from 4 to 3 swaps |
| icosahedral (5⁵), ring 5 | reducible, depth 3 | reducible, depth 3 (unchanged) |
| **pentakis (6⁵), ring 10** | 370 lost | **still NOT reducible: 370 lost, 180 won in 1 swap** (18,870 decision nodes, 2.3 s) |

**Exact joint game for (6⁵).** It equals the `full` game wherever Conjecture J holds. **If J holds at m = 10, the (6⁵) 2-ball is not vacancy-D-reducible under any joint-outside refinement with this knowledge structure.**

I tried to make this unconditional with a witnessed adversary. The witnesses were far too sparse:
- 500 random ring-10 discs gave 111,850 triples.
- Targeted sampling on the 360 ring colourings of the lost states covered only 1,613 of 135,380 possible triples.

In both runs the weakened adversary lost: the player won with depth 15 and depth 2 respectively. **Both runs are inconclusive** and say nothing about the exact game.

## 3. Family of 2-balls around a degree-5 vertex

**Structural fact [hand].** Assume:
- the link is induced (no separating triangle through v);
- no distance-2 vertex is adjacent to two non-consecutive link vertices.

Under these assumptions the boundary is a simple cycle and K (README §1 definition) is **determined by the cyclic link-degree sequence (d₁,…,d₅) up to rotation and reflection**. Ring length = Σd_i − 20, and |K − v| = 5 + ring length.

Adjacency among ring vertices other than consecutive ones lies outside K (it is part of O), so it does not create new configurations. Consequence: **a 2-ball result does not depend on the embedding.** The "one explicit embedding" caveat in README §4 does not apply to 2-balls with a simple ring. As a check, family-built (5,5,5,6,6) reproduces T4's result exactly.

**Count.** For link degrees in [5, D], with k = D − 4, the number of bracelets is (k⁵ + 5k³ + 4k)/10:

| D | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|
| configurations | 1 | 8 | 39 | 136 | 377 | 888 | **1855** |

Growth is about k⁵/10. Ring length runs up to 35 at D = 11.

**What the count misses:**
- Rings that are not simple: a distance-2 vertex adjacent to non-consecutive link vertices, which is excluded here and rejected by `ball_config`.
- A non-induced link: a separating triangle or quadrilateral through v.
- Link degree 4. Degree 3 is impossible with these rings.

These cases are absent in a 5-connected minimal counterexample without separating 4-cycles, but they are **not covered** here.

**Checker on all 8 configurations with link degrees in {5,6}** (`family.py`, 4.7 s):

| sequence | ring | vdred | vdred_joint (`full`, sound) |
|---|---|---|---|
| (5,5,5,5,5) | 5 | depth 3 | depth 3 |
| (5,5,5,5,6) | 6 | depth 6 | depth 6 |
| (5,5,5,6,6) = T4 | 7 | depth 7 | depth 7 |
| (5,5,6,5,6) | 7 | **28 lost** | **reducible, depth 14** |
| (5,5,6,6,6) | 8 | 59 lost | 56 lost |
| (5,6,5,6,6) | 8 | 56 lost | 48 lost |
| (5,6,6,6,6) | 9 | 135 lost | 135 lost |
| (6,6,6,6,6) | 10 | 370 lost | 370 lost |

**Reducible: 3 of 8 under vdred, 4 of 8 under vdred_joint.** Every configuration with three or more degree-6 neighbours fails. The new pass (5,5,6,5,6) depends only on the ring-free retention rule; it does not depend on Conjecture J. It has **not** been run through `verify_joint.py`, because no host triangulation for it has been built yet.

## 4. Untested, with the commands to run on the Mac Studio

All commands run from this directory with Python 3.9 and one core.

1. **Verify (5,5,6,5,6).**
   - Build a host triangulation containing that 2-ball. One way: flip outside the ring, starting from T4 or A₃; a new helper is needed for this.
   - Then run `verify.check(F, 0, cfg, vdred_joint.solve_joint(cfg), label)` on it and on about 10 flipped completions.
   - Expected: 0 violations of A and B. CPU < 30 s.
2. **Conjecture J at m = 7.** `python3 outside_sampler.py 7 14 6000`. Expected: 1925/1925 triples. CPU about 60 s.
3. **Conjecture J at m = 8.** `python3 outside_sampler.py 8 14 6000`. Expected: all triples realised, or a list of missing ones. CPU about 3–5 min.
4. **Witnessed adversary for (6⁵) at higher density.** `python3 joint_targeted.py 2000`. CPU about 40 min.
   - Expected: if the 370 states stay lost, (6⁵) is not reducible in the exact joint game, with no conjecture needed.
   - Likely still too sparse. A better generator would produce outsides with prescribed matchings (a constructive proof of J) rather than random discs.
5. **Larger rings.** {5,6,7} family members with ring 11–15: run `vdred_joint.solve_joint(family.config_from_degrees(s))`.
   - Node counts grow roughly ×8–10 per ring step: ring 11 takes about 20 s, ring 13 about 30 min, and ring 15 is infeasible in pure Python.
   - Output: reducible or lost counts for the 31 sequences outside {5,6}.
   - Pass `max_nodes` to abort cleanly.
6. **Avoid this command.** `joint_witnessed.py pentakis N F` with F ≥ 0 enumerates colourings of pentakis's own 26-vertex outside. It ran for more than 200 CPU-s and was killed. Use F = −1.
