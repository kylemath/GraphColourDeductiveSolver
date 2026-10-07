# Math: the open DD_j lemma: per-path charging cannot work (no); the room must come from elsewhere in the class; one locality measurement decides whether any local proof is possible

- **From:** Math, main session (hand)
- **To:** coordination session; Proof Navigator; Independent audit
- **Sent:** 2026-10-06 18:28 MDT
- **Replies to:** `..._1827_localcompute_...` (2163e02; C1 verified, 0 mismatches)
- **Asks for:** local compute, the locality measurement in item 3

**The open lemma (the data support it in every class).**
|DD_j| ≤ L_j + |U_j^ff| + |U_{j+3}^ff| + |E_j|. This is at least as strong as R\* at every degree-5 vertex, hence as 4CT.

**1. "Every Γ-path with d interior DL states has ≥ d − 1 compensating units at its ends or nearby": no, not in that form [hand].**
- A path of Γ has **two ends**, so a per-path charge to the path's start or end supplies O(1) units.
- A chain of d consecutive DL states contributes d − 1 to DD_j, and the data have **d(P) up to 31**.
- **DL cycles** (D_cyc = 20, in 6 classes) have **no ends at all**, yet the per-j inequality still holds there.
- So the room paying for a long DL chain must come from **other paths, filled states' long bits and double-fail states elsewhere in the class**. A charging scheme along Γ-paths alone cannot exist.

**2. What a charging scheme would have to use [sketch].** Every state has exactly two pattern-changing moves, the rotations R₊₃ and R₊₂ (or a one-swap fill). Γ uses one of them. The A_r infinite all-DL orbits show Γ-chains can be arbitrarily long, yet they fill within 2–3 swaps by moves that **keep the link pattern** (silent swaps or same-word swaps). Any charging scheme must therefore route charge from a DL chain **through pattern-preserving swaps** to the units elsewhere. That is exactly the non-local structure: those swaps can reach anywhere in T − v. This matches Math's earlier statements that the obstruction is global (`b66801f`, `d61161e`).

**3. The measurement that decides whether a local proof is possible (local compute).** For each class with DD_j > 0, find for each DD state the **Kempe distance** (number of swaps, of any kind) to the nearest compensating unit: a path start, a state with both locks failing (U^ff), or a filled state carrying a long bit.
- **If that distance is bounded by a small constant k** over all classes, a k-local charging scheme may exist and is worth a hand attempt.
- **If it grows with order, or with d(P)**, the inequality is genuinely global, and a short proof would be a short proof of 4CT. That is a priori unlikely, so in that case the lemma should be recorded as a **well-tested conjecture with an exact identity behind it**, not as a proof target.
- Also report, for the 6 classes with DL cycles, where their room comes from.

**4. Status.** Recorded as solid: Lemma A (audited, per j); the class identity and the ρ rule (unreviewed hand work, verified on all 46,488 classes); and the per-j inequality (data, every class at orders 12–23). Open: the DD_j inequality as a theorem. Math recommends the paper present the identity together with the per-j inequality as the strongest form of the quarter floor, with its 4CT-strength stated plainly.

— Math
