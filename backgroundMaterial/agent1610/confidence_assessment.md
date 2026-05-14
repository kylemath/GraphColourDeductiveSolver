# Agent 1610 — Confidence Assessment: Independent Audit Results

**Date:** 2026-02-20
**Purpose:** Determine what we actually know vs. what agents have claimed

---

## The Four Auditors

| Auditor | Task | Key Finding |
|---------|------|-------------|
| 1 (Code Review) | Read and bug-check critical scripts | Core infra solid; path enumeration caps could inflate CE count |
| 2 (Independent Replication) | Write new code from scratch, replicate | Consistent with claims at n≤8; exact MTL claim not fully tested at n=9 |
| 3 (Lean 4 Compile) | Assess Lean 4 code reality | Valid skeleton with real errors; "0 sorry" misleading; 3-7 days to compile |
| 4 (Adversarial Breaker) | Try to break the MTL Lemma | **Claims counterexamples — but likely tested the wrong property** |

---

## Critical Finding: Auditor 4's "Counterexamples" Are Probably Not What They Seem

Auditor 4 claims to have found "thousands of counterexamples" to the MTL Lemma, starting at n=5. This sounds like it kills the entire approach. But there is a critical distinction:

**The agents' MTL claim (EXISTENTIAL):** There EXISTS a 4-colouring c* of G-v, reachable by Kempe swaps from the starting 5-colouring, such that c* has a free colour for v.

**What Auditor 4 appears to have tested (UNIVERSAL/ALL):** For ALL 4-colourings of G-v, does a free colour for v exist?

These are vastly different claims. Of course most 4-colourings of G-v use all 4 colours on v's neighbours — that's expected. The MTL claim is that among the 4-colourings REACHABLE BY BFS from the specific starting 5-colouring, at least one leaves a free colour.

Auditor 4's key assertion — "every such 4-colouring is trivially reachable (0 swaps from the starting colouring)" — is almost certainly wrong. A 4-colouring of G-v is NOT directly reachable from a 5-colouring of G-v. The 5-colouring has colour-5 vertices that must be eliminated via Kempe swaps. The BFS process of eliminating colour 5 constrains WHICH 4-colourings are reached.

**However, this confusion is itself a major finding.** It reveals:
1. The precise statement of the MTL Lemma is subtle and easy to misinterpret
2. Four different agents (plus our auditor) may all be testing slightly different things
3. We cannot be confident in the MTL result without being extremely precise about what was tested

---

## Per-Auditor Results

### Auditor 1: Code Review — "Core is solid, quantitative claims inflated"

- **Core infrastructure** (kempe_ops, triangulation_db, reconfiguration_graph): **HIGH confidence (93-95%)**. No bugs found. Proper colouring checks, Kempe swaps, BFS all look correct.
- **Counterexample verification** (verify_counterexamples): **MEDIUM confidence (70%)**. Path enumeration caps at 1000-10000 but callers treat budget exhaustion as "no safe path exists." The 48 counterexample count could include false positives.
- **MTL check** (merge_tolerant_check): **MEDIUM-HIGH confidence (75%)**. Logic is correct, but inherits uncertainty from CE identification.
- **Safe path search**: **HIGH confidence (90%)**. Exhaustive enumeration, no sampling.
- **Overall MTL confidence: 62%**

### Auditor 2: Independent Replication — "Consistent but incomplete"

- Generated all 73 triangulations at n=4 through n=9 correctly (counts match known values)
- 57.9% of ALL 4-colourings fail MTL — expected, since the claim is about BFS-reachable ones only
- BFS reachability checks at n≤8: 168 checks, 0 unreachable. Every problematic starting state can reach a "good" 4-colouring.
- Could NOT fully replicate the exact BFS-endpoint MTL check at n=9 (computational cost)
- **No contradictions found, but exact claim not independently verified**
- **Overall MTL confidence: 75%**

### Auditor 3: Lean 4 Reality Check — "Valid skeleton, significant repair needed"

- Code is recognizable Lean 4 (not gibberish) but has 8-12 specific errors
- Syntax issues: missing `exact` keywords, invalid `▸ rfl` in term mode, hallucinated constructors
- "0 sorry" is technically true but **deeply misleading**: Main.lean is empty, hard content absent
- Honest accounting: "0 sorry in 4 partial lemma files, 0 main theorem attempted"
- Definitions and theorem statements are mathematically meaningful
- **Estimated 3-7 days to get compiling** (with Lean 4 expertise)
- **Confidence in mathematical meaningfulness: 65%**

### Auditor 4: Adversarial Breaker — "Found counterexamples to wrong claim"

- Found that most 4-colourings of G-v DO assign all 4 colours to v's neighbours
- Claims this breaks MTL — but likely tested the universal version, not the existential one
- The key error: treating any 4-colouring of G-v as "reachable in 0 swaps" from a 5-colouring
- **The actual MTL claim (existential, BFS-endpoint-specific) was likely NOT tested**
- **Confidence that MTL is false: probably too high (100% claimed, actual evidence for the right claim: ~30%)**

---

## Synthesis: What We Actually Know

### HIGH CONFIDENCE (≥85%)

- The core Kempe chain infrastructure (swap operations, proper colouring checks, bichromatic components) is correctly implemented
- Planar triangulation generation matches known counts
- The Five Colour Theorem approach (inductive removal + Kempe reduction) is a valid proof architecture
- Surface Tension Rigidity Conjecture is false (solid code, exact computation)
- The Lean 4 code is a valid skeleton that could be repaired, not gibberish

### MEDIUM CONFIDENCE (50-75%)

- {1,2,3,4}-Swap Sufficiency is false at n=9 (code review found path enumeration cap issue; could be false positives)
- The MTL Lemma holds for BFS endpoints at n≤9 (Auditor 1: 62%, Auditor 2: 75%, not fully independently replicated)
- Safe paths with bounded detour exist through n=10 (code looks solid per Auditor 1: 90%)

### LOW CONFIDENCE (≤40%)

- The MTL Lemma is true for ALL n (no one has tested beyond n=10, and the precise claim is subtle)
- The Lean 4 code compiles or is close to compiling (3-7 days minimum, errors throughout)
- The degree-5 "healing" mechanism is a real phenomenon (not independently tested, mechanism not understood)
- "One lemma away from proving 4CT" (the lemma is unproved, the precise statement may not even be right)

---

## What Would Maximally Increase Confidence

1. **Resolve the Auditor 4 discrepancy.** Write a PRECISE test: for the exact starting 5-colouring, run BFS to the nearest 4-colouring in the reconfiguration graph, check whether THAT SPECIFIC 4-colouring has a free colour. Not all 4-colourings. Not any reachable 4-colouring. The BFS endpoint.

2. **Fix the path enumeration cap.** Auditor 1 found that verify_counterexamples treats budget exhaustion as "no safe path." Run with unlimited budget at n=9 to get the true count of counterexamples.

3. **Independent BFS-endpoint MTL check at n=9.** Auditor 2 couldn't complete this. Either optimize the code or use targeted sampling on the 48 claimed counterexamples.

4. **Compile one Lean file.** Even getting Basic.lean to compile against Mathlib would demonstrate that the formalization is real, not aspirational.

---

*Agent 1610 — Graph Colour Project*
*2026-02-20*
