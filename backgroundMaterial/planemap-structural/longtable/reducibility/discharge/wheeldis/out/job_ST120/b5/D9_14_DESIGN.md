# ST-120 B5: design note for d = 9..14 (not built)

Studio, 10 Nov. What exists: `checkDegP_sound` (any d ≤ 30, any part list, any kill list), `hi_le_60_sub_4d`
(d ≥ 9 ⇒ hi ≤ 60 − 4d, by the slot relaxation + kernel `decide`), `B5_ge15`.

**Why the d5..8 checker does not scale as is.** `checkDeg` visits all 5^d link words (d = 14: 6.1·10^9) and pays
≈3 ms of root work per word in the interpreter. The DFS part is small at d ≥ 9 (spec §13 A.4: 3.9 M nodes at d9 with
symmetry, 1.6 M at d10, 0.3 M at d11, almost nothing above).

**Plan (reuses everything proved).**
1. *Link-level table c⁺(L_{i−2..i+2})* (3125 windows): generalise `slotView` so that the spokes and hats that are link
   letters (t = 1, n−1 spokes; t = 0, 1 hats) take the window's letters instead of codes; `slotCheck` per window by
   the same `dfs` with base −c⁺ (or a native_decide over the 3125-entry table). `entry_eq`/`hub_bound` carry over with
   σ unchanged on the remaining codes. Result: `hi W ≤ 60 − 10d + Σ_i c⁺(window_i)`.
2. *Link-word DFS* in the checker over L_0..L_{d−1}, pruning a partial word when 60 − 10d + Σ(c⁺ of the decided windows)
   + 6·(undecided hubs) ≤ 0 (valid by 1). Soundness: induction like `dfs_sound`, cover 5..9 at each letter.
3. At every surviving full word run the existing `checkLinkP` (symbolic instances, classes, kill requirements). The
   certificate is the same per-word line format, keyed by the surviving words in DFS order. u is a host with letter d
   (RSST interiors have degree ≤ 11, so it matters at d = 9..11; `hostLetter` already does this).
4. Optional: rotation canonicalisation on the T side (choose the link listing whose word is rotation-least; B4's
   `eval_sound` holds for every listing), ÷d on words. No reflection (would need mirror invariance of the parts).

Estimated size without symmetry: d9 ≈ 18 k·9 words, ≈ 70 M DFS nodes ⇒ ≈ 30 min interpreted at 26 µs/node; d10 ≈ 15 min;
d11..14 minutes. The max-plus/Karp potentials (spec §13) are then not needed in Lean: they are subsumed by step 1–2's
bound, and the kills make the per-word replay necessary at d9..12 anyway.

**N2 caveat.** `hi_le_60_sub_4d` and c⁺ are for the 71 parts. With N2 (spec §16) `slotCheck` must be re-run on the
extended part list (statement and proof are otherwise parametric once `rsstParts` is replaced); if c⁺ rises above 6
the d ≥ 15 threshold moves to d ≥ ⌈60/(10 − c⁺)⌉.
