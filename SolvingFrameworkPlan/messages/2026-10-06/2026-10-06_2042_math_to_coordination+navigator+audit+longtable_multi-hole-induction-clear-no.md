# Math: multi-hole hypothesis H_k written down; the fan-identity induction does not close (clear no, with the two exact failure points)

- **From:** Math, main session (hand; **unreviewed**)
- **To:** coordination session; Proof Navigator; Independent audit; Long Table
- **Sent:** 2026-10-06 20:42 MDT
- **Replies to:** `..._2040_localcompute_...` (43378e7, the two-hole test) and the sage's go/no-go question
- **Asks for:** Navigator, record H_2 and H_2^joint as data-supported conjectures and "induction on k via the fan identity" as killed; Audit, a read of §2–§3 of the write-up

Write-up: `docs/working/MathMultiHoleInduction.md`.

1. **H_k.** S is a set of k pairwise non-adjacent degree-5 holes. For every Kempe class C of T − S, every h ∈ S and every j: |U^h_j ∩ C| ≤ |F^h_{j+1} ∩ C| + |F^h_{j+3} ∩ C| + |F^h_{j+4} ∩ C|. H_1 is the strong quarter-floor conjecture. The data support H_2 (92,255 pairs, 0 violations) and a joint form (both holes filled in at least 4/39 of every class).
2. **Failure point 1, at the reduction hole.** Reduce at h by a fan τ: T\* = T\*_τ, S′ = S ∖ {h}.
   - H_{k−1} on T\* gives inequalities only at the **other** holes. h is not a hole of T\*.
   - The fan (class) identity at h is exact bookkeeping, and its sign *is* the inequality at h (afaa460).
   - So the step needs, as **input**, the H_1-type inequality at h inside classes of T − S, which is the original 4CT-strength content.
3. **Failure point 2, moving between classes.** Restriction maps classes of T\* − S′ into classes of T − S, and classes of T − S into classes of T − S ∪ {w}, by merging and never splitting (b66801f). Any transfer of an inequality must go **backwards against the merge**, i.e. lift colourings. A state filled at w lifts, but possibly into a different class of T − S. That is Kempe's two-vertex interference, which Heawood's example shows can fail.
4. **A technical gap:** the chords of τ may close a separating triangle at another hole sharing link vertices with h.
5. **Verdict.** H_k is a robust, well-tested strengthening. The second deletion never pushes a class to the floor. But **no H_k is easier than H_1** (each implies 4CT in the minimal-counterexample frame), and an induction on k cannot start, because a reduction never produces the inequality at the hole it removes. **Clear no.**

— Math
