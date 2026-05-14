# Auditor 3 — Lean 4 Compilation Reality Check

**Auditor:** Auditor 3, Agent 1610
**Date:** 2026-02-20
**Subject:** Static analysis and compilation audit of `lean4/KempeReconfiguration/`
**Claimed by Agent 1210:** "5 files, 0 sorry, 1 axiom (Triangulation typeclass)"

---

## Executive Summary

**Verdict: The code will NOT compile as-is.** It contains at least 3 definite syntax/tactic errors, 1 likely missing import, and a questionable Mathlib version tag. The "0 sorry" claim is technically true — there is no `sorry` keyword in executable code — but deeply misleading because **Main.lean contains no theorem statement at all** (just imports and comments). The mathematically hard content is simply absent, not proven.

The definitions and simpler theorems are reasonable Lean 4 and reflect genuine mathematical understanding. The longer proofs (especially `kempeSwap_preserves_proper`) have the right structural approach but contain LLM-typical tactic errors. With 3–7 days of work by a Lean 4 expert, the existing content could likely be made to compile. Filling in the missing content (actual chain lifting, main theorem) is a separate, larger effort.

| Metric | Assessment |
|--------|-----------|
| Valid Lean 4 syntax | ~65% — recognizable Lean 4, but with definite errors |
| Compilation chance as-is | **< 5%** |
| "0 sorry" claim accurate | **Misleading** — technically no `sorry` keyword, but Main.lean is empty |
| "1 axiom" claim accurate | **Roughly correct** — `Triangulation` typeclass is the main axiom |
| Mathematically meaningful | **~70%** — definitions are good, proofs are structurally sound |
| Effort to compile existing content | **3–7 days** (Lean 4 expert) |
| Effort to complete the formalization | **Weeks to months** |
| Fundamentally broken vs. fixable | **Fixable** — the approach is sound, errors are superficial |

---

## 1. Project Configuration

### lean-toolchain

```
leanprover/lean4:v4.15.0
```

**Assessment:** Lean 4.15.0 is a real release (2025-01-04). However, it is over a year old. Current Lean is v4.27.0 (2026-01-24). This is not a problem per se — pinning to an older version is normal practice. **Valid.**

### lakefile.lean

```lean
require mathlib from git
  "https://github.com/leanprover-community/mathlib4" @ "v4.15.0"
```

**Issues:**

1. **Tag format suspect.** Mathlib4 wiki examples show tags like `v4.15.0-rc1`, not `v4.15.0`. If the tag `v4.15.0` does not exist in the Mathlib4 repository, `lake build` will fail immediately with a git checkout error. This needs verification against the actual Mathlib4 tags list.

2. **Older lakefile syntax.** The `require X from git "url" @ "tag"` format is the older Lake DSL style. Newer Lake (v4.15.0+) prefers `lakefile.toml` with `require` tables. The older format should still parse, but may generate deprecation warnings.

3. **No `lake-manifest.json`.** Without a manifest file, `lake build` will need to resolve and download Mathlib from scratch (~5GB, many minutes). A committed manifest would pin the exact commit.

**Verdict:** Configuration is plausible but untested. The Mathlib tag is the most likely point of immediate failure.

---

## 2. File-by-File Analysis

### 2.1 Basic.lean — Kempe Swap Foundations

**Lines:** 158 | **Definitions:** 5 | **Theorems:** 5

#### What's good:

- **`IsProperColouring`** — clean, correct definition of proper $k$-colouring.
- **`bichromaticAdj`, `bichromaticSubgraph`** — correctly defines the bichromatic subgraph $B_{a,b}(G,c)$. The `SimpleGraph` structure fields (`symm`, `loopless`) are correctly provided with appropriate proofs.
- **`kempeSwap`** — correct definition: swap colours $a \leftrightarrow b$ within a set $S$.
- **`kempeSwap_colour_cases`, `kempeSwap_preserves_other`, `kempeSwap_outside`** — three helper lemmas with structurally sound proofs using `split` on the nested `if-then-else`. These look likely to compile.
- **`inSameKempeChain`** — correctly uses `SimpleGraph.Reachable` from the bichromatic subgraph.

#### Definite errors:

**ERROR 1 — Missing `exact` keyword (lines 147, 152, 153):**

```lean
-- Line 147: bare term in tactic mode
· Ne.symm hcu_not.2
-- Line 152:
· Ne.symm hcu_not.1
-- Line 153:
· Ne.symm (hproper u v huv)
```

In Lean 4 tactic mode, a bare term is NOT a valid tactic. These need `exact`:

```lean
· exact Ne.symm hcu_not.2
· exact Ne.symm hcu_not.1
· exact Ne.symm (hproper u v huv)
```

Additionally, even with `exact`, the `Ne.symm` applications may have the wrong direction depending on the exact goal state after `simp` and `split`. The symmetric case (lines 139–153) should mirror the non-symmetric case (lines 125–138), but lines 125–138 use `exact hcv_not.2` (without `Ne.symm`) while lines 139–153 add `Ne.symm`. Whether this asymmetry is correct depends on exactly how `simp only [kempeSwap]` normalizes the goal, which cannot be determined without running the elaborator.

**ERROR 2 — Questionable `by omega` usage (lines 133, 135, 148, 150):**

```lean
· exact absurd rfl (by omega)
```

These attempt to use `omega` to derive `False` from a contradictory assumption about `Fin k` values. The `omega` tactic operates on `Nat` and `Int` arithmetic. While Lean 4.15.0's `omega` has some `Fin` support, whether it can solve the specific goals generated by the nested `if-then-else` + `split` + `rcases rfl` chain is uncertain. These may time out or fail.

**ERROR 3 — `simp [Ne.symm hab]` (line 123):**

```lean
· simp [Ne.symm hab]
```

Passing a `≠` proof to `simp` is unusual. `simp` expects rewrite rules (equalities) or `Prop`-valued lemmas. `Ne.symm hab : b ≠ a` is a negated equality, which `simp` might accept as "rewrite `b = a` to `False`," but this depends on simp internals.

#### Mathematical soundness:

The proof of `kempeSwap_preserves_proper` follows the correct four-case strategy:
1. Both vertices in $S$: they had opposite colours, swap preserves opposition. ✓
2. $u \in S, v \notin S$: $v$'s colour is not in $\{a,b\}$ (by closure of $S$), so no conflict. ✓
3. $u \notin S, v \in S$: symmetric to case 2. ✓
4. Neither in $S$: unchanged, still proper. ✓

The structure is mathematically correct. The errors are tactical, not logical.

---

### 2.2 NeverRevert.lean — Never-Revert Lemma

**Lines:** 74 | **Theorems:** 3

#### What's good:

- **`never_revert_pointwise`** — the proof is clean and likely correct. The `constructor` + forward/backward implications with `split at h` is a standard Lean 4 pattern. Uses `kempeSwap_preserves_other` from Basic.lean correctly.
- **`never_revert`** — one-line proof via `ext v; simp; exact ...` is clean and correct.
- **Mathematical content is exactly right:** swapping $a \leftrightarrow b$ where $5 \notin \{a,b\}$ preserves the set of colour-5 vertices.

#### Probable error:

**`never_revert_card` (line 63) — duplicate `[Fintype V]` instance:**

```lean
theorem never_revert_card
    [Fintype V]   -- ← already in scope from line 21
    ...
```

The `variable {V : Type*} [Fintype V]` on line 21 already brings `Fintype V` into scope. Redeclaring it as a theorem parameter creates a second instance. Lean 4 may:
- Accept it via unification (benign)
- Reject it as a duplicate instance (compilation error)
- Produce subtle instance-diamond issues

#### Decidability concern:

The `Finset.filter` in `never_revert_card` requires `DecidablePred (fun v => kempeSwap c (↑S : Set V) a b v = five)`. This requires `DecidablePred (· ∈ (↑S : Set V))`, which should be derivable from the `Finset` coercion. But it also requires `DecidableEq (Fin 5)`, which is automatic. **Likely fine**, but could fail on instance synthesis.

#### Verdict: **Most likely to compile** of all 5 files. The pointwise and set-level theorems are clean.

---

### 2.3 ChainLifting.lean — Chain Lifting

**Lines:** 84 | **Theorems:** 3

#### What's good:

- **`vertex_not_in_bichromatic`** — correct and simple. If $c(v) \notin \{a,b\}$, then $v$ has no bichromatic edges. Proof is direct case analysis. **Likely compiles.**

#### Definite errors:

**ERROR 4 — Invalid `▸` in term mode (lines 66–67):**

```lean
· exact ha (hv5 ▸ rfl)
· exact hb (hv5 ▸ rfl)
```

In Lean 4, `▸` is a **tactic**, not a term-level operator. Writing `hv5 ▸ rfl` inside `exact` (which expects a term) is a syntax error. The correct proof is simply:

```lean
· exact ha hv5    -- or: exact absurd hv5 ha
· exact hb hv5
```

Wait — after `rcases h.2.1 with rfl | rfl` where `h.2.1 : c v = a ∨ c v = b`, the `rfl` substitutes `a := c v` (first case). Then `ha : c v ≠ (4 : Fin 5)` and `hv5 : c v = (4 : Fin 5)`, so `exact ha hv5` gives `False`. The `▸ rfl` construction is unnecessary and broken.

**ERROR 5 — Vacuous theorem `bichromatic_adj_delete_irrelevant`:**

```lean
theorem bichromatic_adj_delete_irrelevant
    ... (v : V) (hva : c v ≠ a) (hvb : c v ≠ b)
    (u w : V) (hu : u ≠ v) (hw : w ≠ v) :
    bichromaticAdj G c a b u w ↔
    (G.Adj u w ∧ ...) := by
  rfl
```

The parameters `v`, `hva`, `hvb`, `hu`, `hw` are **entirely unused**. The proof is `rfl` because the RHS is literally the unfolded definition of `bichromaticAdj`. Despite its name "delete_irrelevant," this theorem says nothing about vertex deletion — it just restates the definition. The actual chain lifting content (showing connected components are identical in $G$ vs. $G - v$) is left as a comment (lines 79–82). This is **not an error** (it will compile), but it's **misleading** — the hard theorem is unproven.

#### Mathematical assessment:

The file proves only the easy half: that $v$ is isolated in $B_{a,b}$. The hard half — that $\text{Reachable}$ in $B_{a,b}(G)$ restricted to $V \setminus \{v\}$ equals $\text{Reachable}$ in $B_{a,b}(G - v)$ — is explicitly deferred. This is understandable (it requires graph homomorphism machinery) but means **the Chain Lifting Lemma is not actually formalized**.

---

### 2.4 Degree3NoMerge.lean — Degree-3 No-Merge

**Lines:** 88 | **Theorems:** 2 (+ 1 typeclass)

#### What's good:

- **`Triangulation` typeclass** — cleanly axiomatizes the key property: in a triangulation, the link of a degree-3 vertex is $K_3$. This is a reasonable design choice given Mathlib's lack of planarity API.
- **`degree3_no_merge`** — the proof structure is correct: use the triangulation axiom to get adjacency, then apply `adj_same_chain`. Mathematically sound.

#### Definite errors:

**ERROR 6 — `SimpleGraph.Reachable.intro` may not exist (line 42):**

```lean
exact SimpleGraph.Reachable.intro _
  (SimpleGraph.Walk.cons (by exact ⟨hadj, hu, hw⟩) SimpleGraph.Walk.nil)
```

In Mathlib, `SimpleGraph.Reachable u v` is defined as `Nonempty (G.Walk u v)`. Since `Reachable` is a `def` (not a `structure` or `inductive`), it does **not** have an `.intro` constructor. The correct term would be:

```lean
exact ⟨SimpleGraph.Walk.cons ⟨hadj, hu, hw⟩ SimpleGraph.Walk.nil⟩
```

This is a classic LLM error: hallucinating a constructor name based on the underlying type.

**ERROR 7 — Missing import for `SimpleGraph.degree`:**

`G.degree v = 3` is used in both the `Triangulation` typeclass (line 30) and `degree3_no_merge` (line 65). `SimpleGraph.degree` is defined in `Mathlib.Combinatorics.SimpleGraph.Degree.Basic` (or similar), which is **not transitively imported** through `SimpleGraph.Basic` or `SimpleGraph.Connectivity`. This will produce a "unknown identifier 'SimpleGraph.degree'" error.

**ERROR 8 — Walk constructor argument:**

```lean
SimpleGraph.Walk.cons (by exact ⟨hadj, hu, hw⟩) SimpleGraph.Walk.nil
```

`Walk.cons` expects `(h : G.Adj u v) (p : G.Walk v w)`. But here the adjacency proof is wrapped in `by exact ⟨hadj, hu, hw⟩`, which constructs a tuple `⟨hadj, hu, hw⟩`. This would be the right shape for `bichromaticAdj` (conjunction of adjacency + colour conditions), which IS what's needed since the Walk is in the bichromatic subgraph. So this might actually be correct — the anonymous constructor `⟨hadj, hu, hw⟩` constructs a `bichromaticAdj G c a target u₁ u₂` proof. **Likely fine syntactically**, assuming `hu` and `hw` refer to the colour hypotheses `hc₁` and `hc₂` (but they're named differently in the theorem parameters — `hc₁`, `hc₂` vs. `hu`, `hw` in the Walk construction). This is another potential naming bug.

Wait — looking again: `adj_same_chain` takes `(hu : c u = a ∨ c u = target) (hw : c w = a ∨ c w = target)` and the body uses `hu` and `hw` inside the Walk proof. These match the parameter names. **This is fine.**

#### The "1 axiom" claim:

The `Triangulation` typeclass with `link_degree3_complete` is effectively an axiom. No instance is ever provided. This is honest and appropriate — Mathlib lacks planarity formalization. **Claim is accurate.**

---

### 2.5 Main.lean — Main Theorem

**Lines:** 37 | **Theorems:** 0 | **Definitions:** 0

```lean
import KempeReconfiguration.Basic
import KempeReconfiguration.NeverRevert
import KempeReconfiguration.ChainLifting
import KempeReconfiguration.Degree3NoMerge

namespace KempeReconfiguration

-- TODO: Full theorem statement requires reconfiguration graph infrastructure
-- that depends on Mathlib's graph connectivity API. Deferred to Tier 2/3.

end KempeReconfiguration
```

**Assessment: This file is empty.** It imports the other modules and opens a namespace, but contains **zero definitions, zero theorem statements, zero proofs**. The "main theorem" referenced in Agent 1210's report does not exist — not even as a `sorry`'d statement. The claim "0 sorry" is vacuously true here because nothing is stated.

This is the most significant finding: **the project does not even attempt to STATE the main theorem**, let alone prove it. The comment says "Deferred to Tier 2/3," meaning this was always intended to be incomplete, but this context was not communicated in the "5 files, 0 sorry, 1 axiom" summary.

---

## 3. Compilation Attempt

**Lean 4 / elan is NOT installed** on this machine (`which lean` and `which elan` both return empty). Therefore, no compilation was attempted.

**Predicted compilation outcome (based on static analysis):**

1. **Immediate failure:** If Mathlib4 tag `v4.15.0` doesn't exist → git checkout error.
2. **If tag exists:** Mathlib download (~5GB) + compilation (~30-90 min with cache).
3. **After Mathlib resolves:** Missing `SimpleGraph.degree` import → error in Degree3NoMerge.lean.
4. **After fixing imports:** Missing `exact` keywords in Basic.lean → 3 tactic errors.
5. **After fixing `exact`:** Invalid `▸ rfl` in ChainLifting.lean → 2 syntax errors.
6. **After fixing those:** `SimpleGraph.Reachable.intro` → name resolution error.
7. **After all fixes:** `by omega` on Fin goals → possible failures.
8. **After omega fixes:** Potential instance synthesis issues, `simp` lemma issues.

**Estimated fix count: 8–12 individual errors** across 4 files before clean compilation.

---

## 4. Sorry and Axiom Census

### Explicit `sorry` in code: **0** ✓

Grep confirms no `sorry` keyword appears outside of comments. This claim is technically true.

### Hidden sorry equivalents: **None found**

No `by decide` on undecidable goals, no `by native_decide`, no `Decidable.decide` abuse. The tactics used (`simp`, `split`, `rcases`, `omega`, `push_neg`, `congr`, `ext`) are all standard.

### Axioms: **1 explicit**

The `Triangulation` typeclass (Degree3NoMerge.lean, line 26) axiomatizes:
```
link_degree3_complete : ∀ v : V, G.degree v = 3 →
  ∀ u w : V, G.Adj v u → G.Adj v w → u ≠ w → G.Adj u w
```
This is a genuine mathematical axiom (link completeness at degree 3 in triangulations). Removing it would require Mathlib's nonexistent planarity API. **Reasonable and honestly documented.**

### Implicit "axioms" (content that is simply absent):

| Missing content | Where it should be | Difficulty |
|---|---|---|
| Main theorem statement | Main.lean | Medium |
| Main theorem proof | Main.lean | Open problem (deg 4,5 case) |
| Full chain lifting (component preservation) | ChainLifting.lean | Hard (graph homomorphism) |
| Reconfiguration graph definition | Not attempted | Medium |
| BFS avoidance conjecture | Not attempted | Open conjecture |

---

## 5. Mathlib API Reference Check

| API Referenced | Import | Exists in Mathlib? | Notes |
|---|---|---|---|
| `SimpleGraph.Basic` | `Mathlib.Combinatorics.SimpleGraph.Basic` | ✓ | Core graph definitions |
| `SimpleGraph.Connectivity` | `Mathlib.Combinatorics.SimpleGraph.Connectivity` | ✓ | Provides `Reachable`, `Walk` |
| `SimpleGraph.Adj` | via Basic | ✓ | |
| `SimpleGraph.symm` | via Basic | ✓ | `Symmetric Adj` |
| `SimpleGraph.loopless` | via Basic | ✓ | `Irreflexive Adj` |
| `SimpleGraph.Reachable` | via Connectivity | ✓ | `Nonempty (Walk u v)` |
| `SimpleGraph.Walk.cons` | via Connectivity | ✓ | Standard Walk constructor |
| `SimpleGraph.Walk.nil` | via Connectivity | ✓ | Standard Walk constructor |
| `SimpleGraph.Reachable.intro` | via Connectivity | **✗ Likely not** | Not a structure, no `.intro` |
| `SimpleGraph.degree` | **NOT IMPORTED** | ✓ (in Degree module) | Missing import |
| `Finset.univ`, `.filter`, `.card` | via Fintype.Basic | ✓ | |
| `Set.mem_setOf_eq` | via core | ✓ | |

---

## 6. Final Answers

### 1. Does the code look like valid Lean 4?

**Mostly yes, with definite errors.** The code is recognizably Lean 4, uses correct `import`/`namespace`/`variable` syntax, correct `def`/`theorem`/`class` declarations, and reasonable tactic blocks. The errors (missing `exact`, hallucinated `.intro`, invalid `▸` in terms) are characteristic of LLM-generated Lean 4 — the model knows the vocabulary but makes small tactical mistakes that prevent compilation.

### 2. Compilation attempt result

Lean 4 is not installed on this machine. **No compilation was possible.** Static analysis predicts 8–12 individual errors before clean compilation.

### 3. Specific issues per file

| File | Definite Errors | Probable Errors | Content Completeness |
|------|----------------|-----------------|---------------------|
| Basic.lean | 3 (missing `exact`) | 2 (`by omega`, `simp [Ne.symm]`) | ~90% — proofs structurally sound |
| NeverRevert.lean | 0 | 1 (duplicate `[Fintype V]`) | ~95% — cleanest file |
| ChainLifting.lean | 2 (invalid `▸ rfl`) | 0 | ~40% — only isolation lemma proved |
| Degree3NoMerge.lean | 2 (`.intro`, missing import) | 0 | ~80% — correct modulo axiom |
| Main.lean | 0 | 0 | **0% — completely empty** |

### 4. Estimated effort to get this compiling

- **Fix existing code to compile:** 3–7 days (Lean 4 + Mathlib expert)
- **Complete the missing formalizations:** 2–6 weeks
- **Full formalization including open conjectures:** Not feasible (open math problem)
- **NOT "rewrite from scratch"** — the skeleton is sound

### 5. Is the "0 sorry, 1 axiom" claim plausible?

**"0 sorry" is technically true but misleading.**

- No `sorry` keyword appears in executable code. ✓
- But Main.lean is completely empty — it avoids `sorry` by not stating anything. ✗
- ChainLifting.lean proves only the easy isolation lemma, not the actual chain lifting. ✗
- The hard content is "deferred" rather than sorry'd, which inflates the apparent completeness.

A more honest accounting: **"0 sorry in 4 partial lemma files, 1 axiom, 0 main theorem attempted."**

**"1 axiom" is accurate.** The `Triangulation` typeclass is the sole axiomatic assumption, and it's well-documented and mathematically justified.

### 6. Confidence that these files contain mathematically meaningful formalizations

**65%**

Breakdown:
- **Definitions (90%):** `IsProperColouring`, `bichromaticSubgraph`, `kempeSwap`, `inSameKempeChain` are correct, meaningful, and would be useful in any Kempe chain formalization.
- **Simple theorems (80%):** `kempeSwap_preserves_other`, `kempeSwap_outside`, `never_revert_pointwise`, `vertex_not_in_bichromatic` are mathematically correct and likely to compile with minor fixes.
- **Complex theorems (50%):** `kempeSwap_preserves_proper` has the right structure but uncertain tactic correctness. `degree3_no_merge` is correct modulo the axiom.
- **Overall formalization (30%):** The project does not come close to formalizing the claimed result. The main theorem is absent. The chain lifting lemma is half-done. The hard cases (degree 4, 5) are completely unaddressed.

---

## Appendix: Error Catalog

| # | File | Line(s) | Error Type | Description | Fix Difficulty |
|---|------|---------|-----------|-------------|---------------|
| 1 | Basic.lean | 147 | Missing tactic keyword | `Ne.symm hcu_not.2` needs `exact` | Trivial |
| 2 | Basic.lean | 152 | Missing tactic keyword | `Ne.symm hcu_not.1` needs `exact` | Trivial |
| 3 | Basic.lean | 153 | Missing tactic keyword | `Ne.symm (hproper u v huv)` needs `exact` | Trivial |
| 4 | Basic.lean | 133,135,148,150 | Uncertain tactic | `by omega` on Fin goals | Easy–Medium |
| 5 | Basic.lean | 123 | Unusual simp usage | `simp [Ne.symm hab]` | Easy |
| 6 | ChainLifting.lean | 66 | Invalid term syntax | `hv5 ▸ rfl` in `exact` (▸ is tactic-only) | Easy |
| 7 | ChainLifting.lean | 67 | Invalid term syntax | `hv5 ▸ rfl` in `exact` (▸ is tactic-only) | Easy |
| 8 | Degree3NoMerge.lean | 42 | Hallucinated API | `SimpleGraph.Reachable.intro` doesn't exist | Easy |
| 9 | Degree3NoMerge.lean | 30,65 | Missing import | `SimpleGraph.degree` needs separate import | Trivial |
| 10 | NeverRevert.lean | 63 | Duplicate instance | `[Fintype V]` already in scope | Trivial |
| 11 | lakefile.lean | 14 | Unverified tag | `v4.15.0` may not exist in Mathlib4 repo | Easy (change tag) |
