# job HCW13R2: Lean hC for the 45 swarm W13 round-2 C configurations (Studio, 6 Nov)

**Inputs:** 7dc38128 ext_handoff_nov3/w13r2/. extra_hcW13r2_ordered.tsv (a22b0076) and extra_hcW13r2.tsv (1437d398) match their
md5s. There are 45 rows, all with |X| = 1, interior, none rim-pinned. By ring: 12: 2, 13: 15, 14: 17, 15: 8, 16: 3. The D patterns
(pat_W13_D.out) are reference only; no hD was built.

**Split:** batch A = the 4 greedy-cover configs (extraA.tsv, ordered rows 1–4); batch B = the other 41 (extraB.tsv).

## Two engines (eng/verdicts.tsv; kc -t 600 -C -x X and cfast --fixed X; kc 07e79fae, cfast de59e72f)
**45 / 45 are C on both engines with the given X** (kc: adm=yes, leftover 0; cfast: C-REDUCIBLE, leftover 0). No config fails.

## Lean, batch A: the cover-4 (lean/; build ~/studio_lean_builds/rsst118_fb35d2d1/out_hcw13r2)
| module | exit | sorry | wall |
|---|---|---|---|
| CW2A: XRData ok, admissibleX, foldSafeX | 0 | 0 | 4 s |
| W2AV00: hC_0, b7_u567765._.55.... | 0 | 0 | 2,169 s |
| W2AV01: hC_1, b7_u5..5776_...55.5 | 0 | 0 | 341 s |
| W2AV02: hC_2, b7_u56.5776_5...5.5 | 0 | 0 | 256 s |
| W2AV03: hC_3, b7_u57575.._.5.65.. | 0 | 0 | 306 s |
| W2AVAll: hC_all (Fin 4) | 0 | 0 | 3 s |

Axioms: propext, Classical.choice and Quot.sound, plus native_decide aux. sorryAx appears 0 times.

## Lean, batch B (41): in progress
These are CW2B, W2BV00..40 and W2BVAll. The occurrence glue for both batches follows once Opus generates it from extraA.tsv and
extraB.tsv, with the same kc lines and names for the rfl.
