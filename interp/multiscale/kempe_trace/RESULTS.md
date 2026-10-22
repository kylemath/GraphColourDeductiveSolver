# Kempe traces of coloured discs: signatures, collar normalisation, run caps

22 Oct 2026, ~100 min box. Library `kt.py` (traces, non-crossing, signature), `collar.py` (CaDiCaL collar SAT), `minbad.py` (shrinker). Labels: [P] proved, [M] measured (SAT/CSP exact per instance), [C] conjecture. Collar convention (REPORT's): width w = rows at depth 0..w-1; the boundary word is kept, so the free vertices are those at depth 1..w-1.

## 0. Numbers

| what | result |
|---|---|
| Non-crossing | holds in all 16 + 40 + 2,000+ discs/annuli computed (Opus halves, round3 hard pkls, random tubes). 0 violations. [M] |
| Total blocks (6 pairs) on a full disc | **exactly L+3** in every disc tested: Opus A, B (21 = 18+3); 10 round3 full discs with L = 113, 130 (116, 133). Fails on annuli / band-only colourings (24–34 at L = 18). [M], [C] identity |
| Opus A / B signature (L = 18, W_band = 4) | 21 blocks, **0 / 3 singletons**, cyclic nesting depth 2, max span 10 / 8; 15 of 21 blocks have size 2–4 |
| Easy closings, same sphere, random level words (W_band = 0–1, 7 closings) | 21 blocks, **9–14 singletons**, depth 1–2, max span 12–16 (one near-wrapping block per pair) |
| Round3 hard (R = 3, L = 113–130, full colourings) | 116–133 blocks, 58–80 singletons (≈ 0.55 L), depth 2–3, max span 79–118 |
| Tube counterexample halves (annulus depth w*) | blocks 13–24 (> L+3 allowed on an annulus), singletons 4–10, depth 1–2, max span 5–10 |
| Collar rigidity, Opus (enumeration, exhaustive) | for w = 2, 3, 4 the collar has **exactly 1** proper colouring (18, 36, 54 free vertices). Traces cannot change. [M] |
| Window target k (every block inside k consecutive seam positions), Opus A | current 11; min k = 11, 11, 11, 10, 10 for w = 2..6. B: 9 at all w ≤ 6 |
| Exact-trace target: reproduce a random "easy" A′ (same seam word, W_band(A′,B) = 1) on Opus A | w ≤ 4 impossible (rigid); **w = 5: 2 of 5; w = 6: 5 of 5**. After normalisation W_band(A_norm, B) = 1, 1, 1, 1, **3** |
| Tubes: min window k vs collar w (A side) | L=10: 6,6,6→4 (w=2,3,4,5); L=13 (w*=3): 10,10,7,6,5 (w=2..6); L=18 (w*=4): 11,11,11,10,6,4 (w=2..7). k is frozen for w ≤ w*, moves only once the depth-w* row is free |
| Run cap (seam runs ≤ 3) vs none, random tubes, D = 8, 40 per L, L = 8–24 | identical: depth max 2 at every L ≥ 10 (mean 1.0 → 1.9), max span L−2, blocks ≥ L+3. **No measurable effect of the cap** [M] |
| L = 13 k0 = 2 collar failure (bicolour) | with seam rows fixed only 2 a′ and 12 b′ exist; 24 pairs, 2 fail, all 14 rows have distinct signatures; the signature pair separates pass/fail with 0 mixed classes, but trivially (population too small) |
| Minimal obstructing collars (add-on) | 16 cases → **15 distinct** canonical obstructions (L=18 A and B coincide: b is a rotation of a). Sizes 19–22 (w*=2), 28–46 (w*=3), 41 (L=18 tube), 59 / 65 (Opus A / B). All lie in rows 0..w* |

## 1. Definitions and the identity [P]/[M]

Trace of pair {x,y}: components of G[S][{x,y}] that meet ∂S, each recorded as its set of boundary positions. Non-crossing follows from planarity (two disjoint connected sets in a disc cannot interleave on the boundary); confirmed everywhere. Cyclic nesting depth = min over cut points of the linear interval-nesting depth. The identity Σ_pairs #blocks = L+3 held on all 12 full discs (vortices present: round3 halves hold 6 poles each), and only there; it is presumably an Euler count [C], and it means the number of blocks carries no information: the signature is in the block sizes (singletons) and the nesting.

## 2. Signature of the hard halves [M]

Hard halves have few singletons and many blocks of size 2–4 with span ≈ L/2 (Opus A: 0 singletons; the round3 R = 3 halves are not distinguishable from easy ones by this: 0.55 L singletons, which is the random value). Easy halves have ≈ 0.6 L singletons and one long block per pair. The cone collisions of the Opus pair show up as the three size-3 blocks per pair (positions 2-3-4, 11-12-13, 9-15-16 for {0,1}). So for the tube family the signature is a clean discriminator; for the random icosphere R = 3 cases it is not.

## 3. Collar normalisation [M]

- **Width ≤ w\* changes nothing.** On the Opus halves the collar is rigid: given the seam word and the depth-4 row (30)³(20)³(10)³, rows 1–3 are forced (cone lemma), 1 colouring. On the tubes the min window k is frozen for every w ≤ w*: the obstruction (the cones) sits exactly in rows 0..w*, and the minimal obstructions confirm it (all 15 live in rows 0..w*, 19–65 vertices).
- **Width w\*+1 or w\*+2 works at L = 18.** Once the depth-4 row is free, Opus A can be recoloured to have exactly the traces of a random easy A′ with the same seam word (w = 6 in 5/5 trials, w = 5 in 2/5), and in 4 of 5 cases the normalised A then closes against the untouched Opus B with W_band = 1 (was 4). One case gave W_band = 3: equal traces do not imply equal closing radius, so traces are not a complete boundary datum for extension.
- **Scaling.** The width needed is w* + 1 to w* + 2, and w* grows like L/3.5 (REPORT). So collar normalisation does not give a bounded width on the tube family; it reproduces the band-filling scaling. The window target is the wrong normal form anyway: easy halves have *long* blocks.

## 4. Run cap and trace complexity [M, weak]

Random seam rows with runs ≤ 3 and random seam rows with a run > 3 give statistically identical traces at every L from 8 to 24 (depth ≤ 2, spans L−2). This supports Valour's point that the cap does not constrain the traces, but it also shows that *random* interiors never produce nesting depth > 2; an adversarial SAT search for depth 3 (`t4_adv.py`) did not finish in the box. The L = 13 k0 = 2 test is degenerate: with seam rows fixed there are only 2 × 12 candidate pairs, each row has its own signature, so the signature separates pass from fail but cannot be told apart from the identity map.

## Not done
Per-row signatures with Dvořák–Lidický parity and composition under one-vertex attachment (only the block-size parities of the L = 13 rows were recorded, `t5_l13.log`); adversarial nesting-depth search; regeneration of easy round3 closings at L ≈ 100 (replaced by easy closings on the same L = 18 sphere).

Files: `t1_sphere.py/.json`, `t2_tubes.py` (+`t2_tubes.log`), `t3_collar.py` (`t3_sphere.log`), `t3_enum.py/.json`, `t3_t2cheap.py/.json`, `t3_tubes.py/.json`, `t4_cap.py/.json`, `t5_l13.py/.json`, `run_minbad.py`, `minimal_bad/*.json` (+`index.json`), `minbad.log`. Note: `t2_tubes.log` sphere trials predate the at-most-one fix in `sat_colour` (seam words there may not be level); the random-word closings in `t3_t2cheap.log` are the corrected ones.
