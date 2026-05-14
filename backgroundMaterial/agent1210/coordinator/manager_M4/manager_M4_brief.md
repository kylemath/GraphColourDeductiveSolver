# Manager 1210-M4 Brief: The Formalizers (Lean 4 Tier 1)

**Stream:** M4 — Lean 4 Formalization
**Priority:** 10%
**Manager ID:** 1210-M4

---

## Goal

Begin Lean 4 Tier 1 formalization: formalize Kempe chain basics, prove the Never-Revert Lemma, Chain Lifting Lemma, and Degree-3 No-Merge Lemma. Target: 3 lemmas with 0 `sorry` (except planarity axioms for Degree-3 No-Merge, where ≤ 2 sorry is acceptable).

## Formalization Plan

Reference: `/Users/kylemathewson/GraphColour/backgroundMaterial/agent0051/deliverables/lean4_formalization_plan.md`

### Tier 1 Targets

| Lemma | Statement | Sorry Target |
|-------|-----------|-------------|
| **Kempe Chain Basics** | KempeChain definition + swap preserves proper colouring | 0 |
| **Never-Revert (Lemma 3.1)** | $a,b \in \{1,2,3,4\} \Rightarrow V_5(c') = V_5(c)$ after swap | 0 |
| **Chain Lifting (Lemma 5.1)** | $c(v) = 5 \Rightarrow$ $(a,b)$-chains identical in $G$ and $G-v$ for $a,b \in \{1,2,3,4\}$ | 0 |
| **Degree-3 No-Merge (Lemma 5.2)** | In triangulation, degree-3 vertex never merges $(a,5)$-chains | ≤ 2 (planarity) |

### Mathematical Statements (Precise)

**Kempe Chain Basics:**
- Definition: For graph $G$, colouring $c$, colours $a \neq b$, and vertex $v$ with $c(v) \in \{a,b\}$: the $(a,b)$-Kempe chain containing $v$ is the connected component of $B_{a,b}(G,c)$ containing $v$.
- Lemma: If $c$ is a proper $k$-colouring and $K$ is an $(a,b)$-Kempe chain, then swapping $a \leftrightarrow b$ on $K$ produces a proper $k$-colouring.

**Never-Revert Lemma:**
- If $c$ is a proper 5-colouring and $K$ is an $(a,b)$-chain with $a,b \in \{1,2,3,4\}$, then $c' = \text{swap}(c, K, a, b)$ satisfies $\{v : c'(v) = 5\} = \{v : c(v) = 5\}$.
- Proof: swap only changes colours between $a$ and $b$; since $5 \notin \{a,b\}$, no vertex gains or loses colour 5.

**Chain Lifting Lemma:**
- If $c(v) = 5$ and $a,b \in \{1,2,3,4\}$, then for any vertex $u \neq v$: $\text{KempeChain}(G, c, u, a, b) = \text{KempeChain}(G-v, c|_{G-v}, u, a, b)$.
- Proof: $v \notin B_{a,b}$ (since $c(v) = 5 \notin \{a,b\}$), so removing $v$ doesn't disconnect or change $B_{a,b}$.

**Degree-3 No-Merge Lemma:**
- Let $G$ be a triangulation, $v$ with $c(v)=5$, $\deg(v)=3$, neighbours $u_1,u_2,u_3$. If $u_i, u_j \in B_{a,5}(G-v, c)$, then $u_i$ and $u_j$ are in the same $(a,5)$-chain of $G-v$.
- Proof: In a triangulation, $\deg(v)=3$ means the link is a triangle ($K_3$): $u_i u_j \in E(G)$. Since $G-v$ preserves this edge and both have colour in $\{a,5\}$, they're connected in $B_{a,5}$.
- Planarity sorry: the fact that link of a degree-3 vertex in a triangulation is complete (requires 3n-6 edge count + planarity).

---

## Your Sub-subagent Allocation

Spawn 3 sub-subagents as Task subagents (parallel):

### S1: Foundations Builder
**Folder:** `/Users/kylemathewson/GraphColour/backgroundMaterial/agent1210/coordinator/manager_M4/sub_S1/`
**Task:** Set up the Lean 4 project structure and formalize Kempe chain basics.

**Deliverables:**
1. Create Lean 4 project at `/Users/kylemathewson/GraphColour/lean4/KempeReconfiguration/`
2. Set up `lakefile.lean` with Mathlib dependencies
3. Define in `Basic.lean`:
   - `KempeChain` as connected component of bichromatic subgraph
   - Proper colouring (reference Mathlib's `SimpleGraph.Coloring`)
   - Bichromatic subgraph
4. Prove: Kempe swap preserves proper colouring
5. **Target: 0 sorry**

**Mathlib dependencies:**
- `Mathlib.Combinatorics.SimpleGraph.Coloring`
- `Mathlib.Combinatorics.SimpleGraph.Connectivity`
- `Mathlib.Data.Fintype.Basic`

### S2: Never-Revert + Chain Lifting
**Folder:** `/Users/kylemathewson/GraphColour/backgroundMaterial/agent1210/coordinator/manager_M4/sub_S2/`
**Task:** Formalize Never-Revert Lemma and Chain Lifting Lemma.

**Deliverables:**
1. `NeverRevert.lean` — Lemma 3.1:
   ```
   theorem never_revert (c : V → Fin 5) (K : Set V) (a b : Fin 4) (h : kempe_swap c K a b = c') :
     {v | c' v = 5} = {v | c v = 5}
   ```
2. `ChainLifting.lean` — Lemma 5.1:
   ```
   theorem chain_lifting (c : V → Fin 5) (v : V) (hv : c v = 5) (a b : Fin 4) (u : V) (hu : u ≠ v) :
     kempe_chain G c u a b = kempe_chain (G.deleteVerts {v}) (c ∘ Subtype.val) ⟨u, hu⟩ a b
   ```
3. **Target: 0 sorry**

### S3: Degree-3 No-Merge
**Folder:** `/Users/kylemathewson/GraphColour/backgroundMaterial/agent1210/coordinator/manager_M4/sub_S3/`
**Task:** Formalize the Degree-3 No-Merge Lemma.

**Deliverables:**
1. `Degree3NoMerge.lean` — Lemma 5.2
2. Define "triangulation" (maximal planar graph: 3n-6 edges + planar)
3. Define "link" of a vertex (set of neighbours + induced edges)
4. Prove: in a triangulation, degree-3 link is complete ($K_3$)
5. Prove: completeness of link → all $B_{a,5}$-neighbours in same chain
6. **Target: ≤ 2 sorry** (for planarity axioms — it's acceptable to sorry planarity since Mathlib doesn't have a full planar graph API)

**Planarity handling:**
- Option A: Axiomatize planarity as a structure/typeclass, sorry the key properties
- Option B: Prove from the edge count 3n-6 + Euler's formula (possible but harder)
- Recommend Option A for now with clear TODO comments on each sorry

---

## Project Structure

```
lean4/KempeReconfiguration/
├── lakefile.lean         -- Mathlib dependency configuration
├── lean-toolchain        -- Lean version
├── KempeReconfiguration/
│   ├── Basic.lean        -- Graph colouring, Kempe chain definitions
│   ├── NeverRevert.lean  -- Lemma 3.1
│   ├── ChainLifting.lean -- Lemma 5.1
│   ├── Degree3NoMerge.lean -- Lemma 5.2
│   └── Main.lean         -- Imports + statement of full theorem (sorry)
└── README.md
```

---

## Report Format

Write `manager_M4_report.md` using:

```
# Manager 1210-M4 Report
**Stream:** The Formalizers (Lean 4 Tier 1)
**Status:** Complete / In Progress / Blocked

## Stream Summary
## Sub-subagent Status
| Sub-subagent | Task | Status | Sorry Count |
|---|---|---|---|
| S1 | Foundations | ... | ... |
| S2 | Never-Revert + Chain Lifting | ... | ... |
| S3 | Degree-3 No-Merge | ... | ... |

## Total Sorry Count
## Collected Outputs
## Integration Notes
## Escalated Questions
## Issues Encountered
## Self-Assessment
```

---

## CRITICAL INSTRUCTIONS

1. **Track sorry count meticulously.** Every sorry must have a TODO comment explaining what's needed.
2. **Lean 4 builds must compile.** Don't submit code that doesn't `lake build` successfully.
3. **Use Mathlib idioms.** Prefer Mathlib's existing graph theory infrastructure over custom definitions where possible.
4. **Comment every sorry** with what mathematical fact is being assumed and what would be needed to remove it.
5. **IMPORTANT: Never install packages globally.** If pip is needed for any tooling, use `source /Users/kylemathewson/GraphColour/.venv/bin/activate`.
6. **If Lean 4 / Mathlib setup is blocked** (e.g., Mathlib download too large, version conflicts), document the issue clearly and focus on writing the `.lean` file contents even if they can't be compiled yet.
