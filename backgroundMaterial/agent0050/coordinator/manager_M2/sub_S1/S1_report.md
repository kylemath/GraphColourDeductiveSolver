# Sub-subagent 0050-M2-S1 Report

**Agent:** 0050-M2-S1
**Task:** Non-Crossing Theorems A & B
**Manager:** 0050-M2
**Status:** Complete

---

## Work Product

Rigorous proofs of Theorems A (Non-Interleaving) and B (Confinement).

- **`theorem_A_proof.md`**: Full proof using Jordan Curve Theorem. Handles edge cases (consecutive neighbours, chain cycles, boundary connections). Verified computationally at 1,848 vertex-checks with 0 violations.

- **`theorem_B_proof.md`**: Full proof of invariance of $(a,b)$-subgraph under swaps on disjoint colour pairs. Includes corollary on nested regions and analysis of limitations.

## Acceptance Criteria Check

- [x] `test_theorem_A_precise` — Statement handles boundary cases, vertex-in-chain subtlety, and consecutive-neighbour case
- [x] `test_theorem_B_precise` — Statement covers nested regions (corollary proved)
- [x] `test_consistency_with_computation` — Predictions match M1-S3's 1,848 vertex checks

## Key Insight for Downstream Work

The proof of Theorem A crucially requires $v$ to be EXTERNAL to the chains. This was independently discovered by M1-S3 when their initial verifier (checking at all vertices) produced false positives. The theoretical and computational teams converged on the same understanding.

## Self-Assessment

**Craftsperson says:** Both proofs are complete, rigorous, and handle edge cases. Theorem A's proof via JCT is clean and standard. Theorem B's invariance argument is straightforward but powerful.

**Skeptic says:** Theorem A only constrains configurations at external vertices. For the proof strategy (Colour Elimination Lemma), we also need to understand chain behaviour at vertices IN the chains. This is not addressed.

**Mover says:** The foundational theorems are solid. Moving to the case classification and elimination lemma where the real difficulty lies.

---

*0050-M2-S1 — 18 February 2026*
