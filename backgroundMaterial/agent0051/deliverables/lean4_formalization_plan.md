# Lean 4 Formalization Plan — Agent 0051

**Date:** 18 February 2026

---

## Tier 1: Immediately Formalizable (No planarity needed)

### 1.1 Kempe Chain Basics
- **Definition:** `KempeChain G c a b v` — the connected component of `B_{a,b}(G,c)` containing `v`
- **Lemma:** Kempe swap produces a proper colouring
- **Dependencies:** `Mathlib.Combinatorics.SimpleGraph.Coloring`, `Mathlib.Combinatorics.SimpleGraph.Connectivity`
- **Effort:** 1-2 days
- **Sorry count target:** 0

### 1.2 Never-Revert Lemma
- **Statement:** `kempe_swap chain a b c → a ∈ {1,2,3,4} → b ∈ {1,2,3,4} → V₅(c') = V₅(c)`
- **Proof:** Definitional — swap only changes colours a ↔ b, neither equals 5
- **Dependencies:** 1.1
- **Effort:** 0.5 days
- **Sorry count target:** 0

### 1.3 Chain Lifting for {1,2,3,4} Pairs
- **Statement:** `c(v) = 5 → a,b ∈ {1,2,3,4} → KempeChain G c a b = KempeChain (G-v) c|_{G-v} a b`
- **Proof:** `v ∉ B_{a,b}` since `c(v) ∉ {a,b}`, so removing `v` doesn't affect `B_{a,b}`
- **Dependencies:** 1.1 + vertex deletion
- **Effort:** 1-2 days
- **Sorry count target:** 0

## Tier 2: Requires Mathlib Planarity Extensions

### 2.1 Degree-3 No-Merge Lemma
- **Statement:** In a triangulation, degree-3 neighbours form a triangle; all `B_{a,5}`-neighbours are in the same chain
- **Requires:** Triangulation definition (3n-6 edges + planarity), link structure
- **Key missing Mathlib component:** `PlanarEmbedding`, face structure
- **Effort:** 2-3 days (assuming Mathlib extensions exist)
- **Sorry count target:** ≤ 2 (planarity axioms)

### 2.2 Degree-5 Classification
- **Statement:** 8 types, all resolvable by ≤ 1 swap
- **Requires:** Jordan Curve Theorem (for non-interleaving), link cycle structure
- **Key missing Mathlib component:** JCT for combinatorial embeddings
- **Effort:** 3-5 days
- **Sorry count target:** ≤ 5 (planarity + JCT)

## Tier 3: Requires Gap Resolution

### 3.1 BFS Avoidance Conjecture
- **Statement:** BFS-optimal paths avoid merge-prone (a,5)-chains at degree-4/5 vertices
- **Requires:** Full formalization of reconfiguration graphs, BFS optimality
- **Status:** Unproved — cannot formalize without resolution
- **Sorry count target:** N/A

### 3.2 Full Constructive 4CT
- **Statement:** Every 5-colouring reaches a 4-colouring in ≤ n-4 Kempe swaps
- **Requires:** All of the above
- **Status:** Depends on 3.1
- **Sorry count target:** N/A

## Implementation Strategy

```
Phase 1 (Week 1):  Tier 1 → 3 lemmas, 0 sorry
Phase 2 (Week 2-3): Tier 2.1 (Degree-3) → may need sorry for planarity axioms
Phase 3 (Ongoing):  Tier 2.2 + Tier 3 → await Mathlib planarity + gap resolution
```

## Lean 4 Project Structure

```
lean4/KempeReconfiguration/
├── Basic.lean          -- Graph colouring, Kempe chain definitions
├── NeverRevert.lean    -- Lemma 3.1
├── ChainLifting.lean   -- Lemma 5.1
├── Degree3NoMerge.lean -- Lemma 5.2 (with planarity sorry)
├── Degree5Class.lean   -- Proposition 4.1 (with planarity sorry)
└── Main.lean           -- Statement of full theorem (with gap sorry)
```

## Feasibility Assessment

| Component | Feasibility | Confidence |
|-----------|------------|------------|
| Tier 1 | **High** | Very high — pure graph theory, well within Mathlib |
| Tier 2.1 | **Medium** | Medium — planarity gap in Mathlib is the bottleneck |
| Tier 2.2 | **Medium-Low** | Medium — JCT equivalent needed |
| Tier 3 | **Unknown** | Depends entirely on mathematical resolution |
