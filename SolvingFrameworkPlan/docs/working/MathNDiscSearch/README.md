# MathNDiscSearch (exploratory tool, not a declared experiment)

[computed, exploratory, post hoc] Math-team worker, 5 October 2026. Implements the disc generator of `MathNAttack.md` §6: rigid triply locked states of a min-degree-5 triangulation are built directly as acyclic 4-coloured discs T-x with ring word D a D b g, **without enumerating triangulations**, then statement (N) is tested on every state that survives. It can only produce a counterexample candidate or a no-find report. No universal claim is made.

## Files
- `disc_gen.cpp` (`g++ -O2 -o disc_gen disc_gen.cpp`): `./disc_gen N [maxout] [cpu_seconds]`. Grows the disc inward from the 5-ring by an advancing front (stack of simple cycles; each step puts a triangle on a front edge, apex = new vertex or an existing vertex of the same front cycle). Pruning: proper colour; per-pair union-find rejects any cycle (all six pairs forests); class sizes fixed by a target (nD,na,nb,ng) running over all tuples with exc_i = N-4-3n_i (alpha: N-3-3n_alpha) >= 0 (Prop 3); class excess lower bound <= exc_i; closed vertices need degree >= 5 (ring: >= 4 in the disc); closed pair components cannot merge, so closed + (open>0) <= target comps (1,2,2,1,1,1); ring chords forbidden (legality). Final test: comps vector exactly (1,2,2,1,1,1). Output lines `DISC sizes ; colours ; edges`. Up to reflection of the disc (graph-level), ring labelled. Not canonical beyond that, so an isomorphism class can occur several times (other ring placements, other x).
- `test_N.py FILE`: for each disc re-verifies the structure, tests locks at fans u1,u3,u4 by BFS over the full Kempe class in G = T-xy (cap 200 000 colourings), and for locked states builds nu_gamma c, nu_beta c and tests separability at u0, u2. Prints `N-holds`, `CAND` (candidate counterexample), or `N-UNDECIDED(trunc)`.
- `recheck.py -f FILE` (or the line as arguments): independent re-check of one line, shares no code with `test_N.py`. Certifies sphere triangulation (vertex links are cycles, Euler), min degree 5, no ring chord, proper colouring, six forests with (1,2,2,1,1,1), full classes of the three fans (must not separate) and full classes of both neighbours; prints `N HOLDS` or `N FAILS (counterexample certificate ...)`. A counterexample candidate is only reportable after `recheck.py` agrees and it has been looked at by hand.
- `out_N.txt`, `err_N.txt`: raw generator output and per-size logs; `res_23.txt` test output for N=23 (all 14 locked states, with full disc lines for recheck).

## Results [computed, exploratory, post hoc]
| N | discs with the forced structure | locked at all three fans | (N) | CPU (generator) |
|---|---|---|---|---|
| 12, 14 | 0 | - | - | 0 |
| 16 | 0 | - | - | <1 s |
| 17 | 75 | 2 (sizes 4,4,4,4) | holds, both neighbours separable, classes of fans size 6 (matches the hexagon of MathNAttack §3) | <1 s |
| 18 | 74 | 0 | vacuous | <1 s |
| 19 | 170 | 0 | vacuous | 1 s |
| 20 | 1565 | 0 | vacuous | 4 s |
| 21 | 5146 | 0 | vacuous | 16 s |
| 22 | 15840 | 0 | vacuous | 114 s |
| 23 | 78005 | 14 (sizes (5,6,5,6) x2, (5,6,6,5) x2, (6,4,6,6) x6, (6,6,4,6) x2, (6,6,6,4) x2) | holds in all 14 (at least one neighbour separable, in fact both); first nonvacuous test above 17; three of them re-checked by `recheck.py` | 533 s (complete, no timeout) |

Reading: at orders 19 to 22 the rigid pair structure is plentiful (170 to 15840 labelled discs) but none is triply locked, so (N) is vacuous there; at N=23 14 triply locked discs appear and (N) holds on all of them (both neighbours separable, Kempe classes of size 13 to 42). The two order-17 discs are the 17:1 states of the source (the source counts 4 states, mirror images and the two choices of x; the generator identifies reflections). The agreement with the source at 12 to 18 (no locked state at 12, 14, 15, 16, 18) is a consistency check of the generator, not a proof of its exhaustiveness. Exhaustiveness at N >= 19 is untested against an independent census (no plantri binary was found on this machine).

## Limits and honest caveats
- Exhaustive only if the front construction is complete for planar triangulated discs with simple front cycles and the pruning is sound; both are argued, not verified against plantri at N >= 19.
- The size-target loop and the exc formulas rely on Prop 3 of `d1-hand-attack.md` (hand proof, not machine-checked here).
- Generation is exponential: N=22 took 114 s CPU, the ratio per order is about 7, N=23 finished in 533 CPU s (just under budget); test_N.py on it took a further about 2 min. N=24 would need roughly an hour of CPU and was not run. N >= 24 needs more than 10 CPU minutes by a large factor and was not run.
- Discs with separating triangles are allowed (T need not be 4-connected); only ring chords are excluded.
- No counterexample to (N) was found. This is a no-find report only.
