# Solving Proof Strategy: An Automated Framework for Iterative 4CT Proof Discovery

**Project:** Graph Colouring — Four Colour Theorem  
**Date:** 17 February 2026  
**Author:** Agent 1221  
**Classification:** Architectural Plan — Skeptical & Realistic

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [State of the Art: What Actually Exists Today](#2-state-of-the-art-what-actually-exists-today)
3. [What "Success" Looks Like — Defining the Win Conditions](#3-what-success-looks-like--defining-the-win-conditions)
4. [The Test Harness: Verifiable Checkpoints](#4-the-test-harness-verifiable-checkpoints)
5. [Architecture: The Proof Discovery Framework](#5-architecture-the-proof-discovery-framework)
6. [Agent Swarm Design](#6-agent-swarm-design)
7. [Proof Strategy Pipelines](#7-proof-strategy-pipelines)
8. [Branching, Checkpointing, and State Management](#8-branching-checkpointing-and-state-management)
9. [Skeptic's Reality Check](#9-skeptics-reality-check)
10. [Implementation Roadmap](#10-implementation-roadmap)
11. [Appendix A: Existing Tools and Versions](#appendix-a-existing-tools-and-versions)
12. [Appendix B: The Proof Dependency Graph](#appendix-b-the-proof-dependency-graph)

---

## 1. Executive Summary

This document lays out a **realistic but ambitious** plan for building an automated framework to iteratively discover, test, verify, and refine proofs (or proof components) of the Four Colour Theorem. The central philosophy is:

> **The proof assistant is the arbiter. Everything else is heuristic.**

No matter how clever our AI agents, search heuristics, or human intuitions are, the only thing that counts is a proof that compiles in a formal verification system (Lean 4 or Coq). This means our framework is fundamentally a **generate-and-test loop** wrapped around a proof checker, with increasingly sophisticated generators.

### What this plan covers:
- How to set up Lean 4 with the right libraries and test infrastructure
- What specific formal statements constitute "success" at each stage
- How to decompose the 4CT proof into independently testable subgoals
- How to run parallel agent swarms exploring different proof strategies
- How to manage branching proof attempts with checkpointing
- What's realistic today vs. what's aspirational

### What this plan does NOT claim:
- That we will find a new proof of the 4CT (we might, or we might merely formalize the known one differently)
- That AI can currently replace mathematicians for this problem (it cannot — see Section 9)
- That any specific timeline is guaranteed

---

## 2. State of the Art: What Actually Exists Today

### 2.1 Proof Assistants

| System | Status | 4CT Relevance |
|--------|--------|---------------|
| **Coq** (now Rocq) | Mature, ~30 years old | The 4CT is fully formalized (Gonthier, 2005). ~60,000 lines. Maintained at `rocq-community/fourcolor` on GitHub. Uses SSReflect and hypermap-based combinatorial planarity. |
| **Lean 4** | Rapidly growing, ~5 years old | Mathlib4 has `SimpleGraph.Coloring`, `SimpleGraph.Colorable`, `chromaticNumber`. **No planarity formalization yet.** No 4CT. Mathlib TODO explicitly lists "planar graphs" as future work. |
| **Isabelle/HOL** | Mature | Has graph theory but no 4CT formalization. |

**Honest assessment:** Lean 4 is where the momentum is (AI tools, community, growth), but it's missing critical infrastructure for 4CT. Coq has the proof but the ecosystem is less AI-friendly. The pragmatic path is: use Lean 4 for new work, reference Coq for structural guidance.

### 2.2 AI-Guided Proof Search Tools

| Tool | What It Does | Maturity | Relevance |
|------|-------------|----------|-----------|
| **AlphaProof** (DeepMind, 2024-2025) | RL-based formal proof search in Lean. Solved 4/6 IMO 2024 problems at silver medal level. Uses test-time RL, generating millions of problem variants. | Research prototype; not publicly available. | The gold standard for what's possible, but we can't use it directly. Proves the approach works. |
| **APOLLO** (2025) | Multi-agent LLM framework for Lean 4. Agents analyze, fix syntax, isolate failing sublemmas, invoke LLMs. 84.9% on miniF2F with <100 samples. | Open research; code available. | Directly usable architecture. Best model for our agent swarm design. |
| **BFS-Prover-V2** (2025) | Planner-enhanced multi-agent: a reasoning model decomposes theorems into subgoals, parallel provers collaborate via shared cache. 95% on miniF2F. | Research; OpenReview 2025. | The hierarchical decomposition + shared cache is exactly what we need. |
| **LeanDojo v2 / ReProver** (2025) | Python library for extracting proof data from Lean repos + ByT5-based tactic generation. LeanDojo v2 is the current recommended version. | Actively maintained, open source. | Our primary interface layer between AI and Lean. |
| **Lean-Auto** (2025) | First general-purpose ATP integration for Lean 4. Translates Lean goals to ATP format with guaranteed soundness. Beats existing tools on Mathlib4 benchmarks. | Published, available. | Critical for automating routine subgoals. |
| **LeanCopilot** | Runs LLMs natively inside Lean 4 for tactic suggestions. | Available. | Useful for interactive exploration. |
| **ImProver** (2025) | Agent-based proof optimization — rewrites proofs for length/readability while maintaining correctness. | Research. | Useful for proof compression after discovery. |

### 2.3 SAT/SMT Integration

| Tool | What It Does | Relevance |
|------|-------------|-----------|
| **LeanSAT** (archived 2024, superseded by `bv_decide`) | SAT reasoning in Lean 4 via LRAT proof certificates. Now integrated into Lean's core as `bv_decide` tactic. | Directly relevant for reducibility verification. |
| **Hadwiger-Nelson in Lean 4** (Nesterov, 2025) | Proved a 510-vertex graph is not 4-colorable using LeanSAT + external CaDiCaL solver. Parses graph → CNF → SAT solve → LRAT certificate → Lean verification. | **Template for our reducibility checker.** Exactly the pattern we need. |
| **PBLean** (2026) | Pseudo-Boolean proof certificates for Lean 4. Supports cutting-plane proofs beyond what resolution can handle. | May be useful for more sophisticated reducibility arguments. |
| **CaDiCaL / Kissat** | State-of-the-art SAT solvers. | Backend for any SAT-based proof component. |

### 2.4 The Existing Coq 4CT Proof

The `rocq-community/fourcolor` repository contains Gonthier's proof. Key structural components:

```
fourcolor/theories/
├── hypermap.v          # Combinatorial hypermap theory (replaces topological planarity)
├── colormap.v          # Map coloring definitions
├── coloring.v          # Graph coloring theory
├── chromogram.v        # Chromatic analysis
├── discharge.v         # The 32 discharging rules
├── reducible.v         # Reducibility checker
├── unavoidable.v       # The 633 unavoidable configurations
├── kempe.v             # Kempe chain theory
├── birkhoff.v          # Birkhoff reducibility
├── four_color.v        # The final theorem statement
└── ... (~170 files total)
```

**Critical insight:** The proof's structure is modular. The discharging rules, the unavoidable set, and the reducibility checker are separate components. We can target each independently.

---

## 3. What "Success" Looks Like — Defining the Win Conditions

This is the most important section. Before building anything, we need machine-checkable definitions of success at every level.

### 3.1 The Ultimate Goal (Level 5)

```lean
-- THE WIN CONDITION: This compiles in Lean 4.
theorem four_color_theorem :
    ∀ (G : SimpleGraph V) [Fintype V] [DecidableRel G.Adj],
    G.IsPlanar → G.Colorable 4 := by
  sorry -- This is what we're trying to fill in.
```

**Honest assessment:** Getting here from scratch in Lean 4 is a multi-year project. Gonthier's Coq proof took ~5 years with a dedicated team. Even with modern tools, a full Lean 4 formalization is 1-3 years of serious effort.

### 3.2 Progressive Win Conditions (Levels 0-4)

We define a ladder of increasingly difficult milestones, each of which is independently valuable and machine-verifiable:

#### Level 0: Infrastructure (No mathematical content)
```lean
-- Can we even talk about planar graphs in Lean 4?
-- SUCCESS: These definitions compile and are usable.
def SimpleGraph.IsPlanar (G : SimpleGraph V) : Prop := sorry
def SimpleGraph.PlanarEmbedding (G : SimpleGraph V) : Type := sorry
```

**What this tests:** That we have a working formalization of planarity. Currently missing from Mathlib.

#### Level 1: The Five Colour Theorem
```lean
-- SUCCESS: This compiles.
theorem five_color_theorem :
    ∀ (G : SimpleGraph V) [Fintype V] [DecidableRel G.Adj],
    G.IsPlanar → G.Colorable 5 := by
  -- Proof via induction + single Kempe chain swap
  sorry
```

**Why this matters:** The Five Colour Theorem is provable by elementary induction with a single Kempe chain argument. It's the "warm-up" that tests all the infrastructure (planarity, colouring, Kempe chains, Euler's formula) without the hard part. If we can't do this, we can't do 4CT.

#### Level 2: Kempe Chain Machinery
```lean
-- SUCCESS: Kempe chains are formalized and their key properties are proved.
def KempeChain (G : SimpleGraph V) (c : G.Coloring (Fin k))
    (v : V) (a b : Fin k) : Set V := sorry

theorem kempe_swap_valid :
    ∀ (G : SimpleGraph V) (c : G.Coloring (Fin k)) (chain : Set V),
    IsKempeChain G c chain a b →
    (swapKempe c chain a b).IsProper := by sorry

theorem kempe_chain_planar_noncrossing :
    ∀ (G : SimpleGraph V) [G.IsPlanar],
    -- Kempe chains for disjoint colour pairs don't cross
    sorry := by sorry
```

**Why this matters:** Kempe chains are the core mechanism for every known proof approach. Formalizing them — including the planar non-crossing property — is essential infrastructure.

#### Level 3: Single Configuration Reducibility
```lean
-- SUCCESS: We can formally verify that ONE specific configuration is reducible.
theorem birkhoff_diamond_reducible :
    ∀ (G : SimpleGraph V) [G.IsPlanar],
    ContainsConfiguration G birkhoff_diamond →
    ¬ IsMinimalCounterexample G := by sorry
```

**Why this matters:** If we can verify a single reducibility proof formally, we can do them all. This is the "proof of concept" for the entire framework.

#### Level 4: Unavoidable Set + Batch Reducibility
```lean
-- SUCCESS: A set of configurations is unavoidable AND all are reducible.
-- (This is essentially the 4CT, modulo the choice of unavoidable set size.)
theorem unavoidable_set_exists :
    ∃ (S : Finset Configuration),
    (∀ G, G.IsPlanar → ∃ c ∈ S, ContainsConfiguration G c) ∧
    (∀ c ∈ S, IsReducible c) := by sorry
```

#### Level 5: The Full Theorem
Stated in 3.1 above.

### 3.3 Machine-Checkable Test Suite

Every milestone is a `.lean` file that either compiles or doesn't. There is no ambiguity.

```
tests/
├── Level0_Planarity.lean          # Does IsPlanar compile? Can we check K5/K33?
├── Level1_FiveColorTheorem.lean   # Does the 5CT proof compile?
├── Level2_KempeChains.lean        # Do Kempe chain properties compile?
├── Level3_SingleReducibility.lean # Does one reducibility proof compile?
├── Level4_UnavoidableSet.lean     # Does the batch check compile?
├── Level5_FourColorTheorem.lean   # THE final test
├── Sanity_K4_is_4colorable.lean   # Trivial: K4 needs exactly 4 colours
├── Sanity_K5_not_planar.lean      # Trivial: K5 is not planar
├── Sanity_Petersen_3colorable.lean # Petersen graph is 3-chromatic
└── Integration_USStateMap.lean    # Can we 4-colour 49 states formally?
```

**The CI pipeline is the proof checker.** Every push to the repo runs `lake build` on all test files. Green = progress. Red = broken.

---

## 4. The Test Harness: Verifiable Checkpoints

### 4.1 Design Principles

1. **Binary pass/fail.** Every test is a Lean file that compiles or doesn't. No "partial credit."
2. **Monotonic progress.** Once a test passes, it should never regress (barring upstream Mathlib changes).
3. **Independent subgoals.** Tests can be worked on in parallel by different agents.
4. **`sorry`-counting.** We track the total number of `sorry` (unproved) lemmas. Success = zero `sorry`s in a given level's test file.
5. **Proof term size.** We track the size of proof terms. Smaller is better (more likely to represent genuine insight).

### 4.2 The `sorry` Dashboard

```
┌─────────────────────────────────────┬──────────┬──────────┬────────┐
│ Test File                           │ Sorries  │ Status   │ Trend  │
├─────────────────────────────────────┼──────────┼──────────┼────────┤
│ Level0_Planarity.lean               │ 5        │ PARTIAL  │ ↓ (was 12) │
│ Level1_FiveColorTheorem.lean        │ 8        │ PARTIAL  │ ↓ (was 15) │
│ Level2_KempeChains.lean             │ 11       │ PARTIAL  │ new    │
│ Level3_SingleReducibility.lean      │ 3        │ PARTIAL  │ new    │
│ Level4_UnavoidableSet.lean          │ 634      │ BLOCKED  │ —      │
│ Level5_FourColorTheorem.lean        │ 1        │ BLOCKED  │ —      │
│ Sanity_K4_is_4colorable.lean        │ 0        │ ✓ PASS   │ —      │
│ Sanity_K5_not_planar.lean           │ 0        │ ✓ PASS   │ —      │
├─────────────────────────────────────┼──────────┼──────────┼────────┤
│ TOTAL                               │ 662      │          │        │
└─────────────────────────────────────┴──────────┴──────────┴────────┘
```

Each `sorry` is a concrete, named subgoal. This is what agents work on.

### 4.3 Formal Pre-Conditions and Post-Conditions for Each Level

| Level | Pre-Conditions | Post-Conditions (pass criteria) |
|-------|---------------|-------------------------------|
| 0 | Lean 4 + Mathlib4 installed | `IsPlanar`, `PlanarEmbedding` defined; K4 is planar, K5 is not; Euler's formula proved for planar graphs |
| 1 | Level 0 passes | Five Colour Theorem compiles with 0 sorries; proof uses induction + Kempe swap |
| 2 | Level 0 passes | Kempe chain definition, swap validity, and planar non-crossing all proved |
| 3 | Levels 0 + 2 pass | At least 1 configuration proved reducible with 0 sorries |
| 4 | Levels 0 + 2 + 3 pass | Unavoidable set proved + all members shown reducible |
| 5 | Level 4 passes | Full 4CT statement proved with 0 sorries |

---

## 5. Architecture: The Proof Discovery Framework

### 5.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     ORCHESTRATOR (Manager Agent)                │
│  - Tracks sorry dashboard                                       │
│  - Assigns subgoals to worker agents                            │
│  - Manages branching and checkpointing                          │
│  - Decides when to prune dead-end branches                      │
└──────────────┬──────────────────────────────────────────────────┘
               │
    ┌──────────┴──────────┐
    │                     │
    ▼                     ▼
┌────────────┐    ┌────────────────┐
│  GENERATOR │    │   VERIFIER     │
│   LAYER    │    │    LAYER       │
│            │    │                │
│ - LLM      │    │ - Lean 4       │
│   agents   │───▶│   compiler     │
│ - ATP      │    │ - lake build   │
│   solvers  │    │ - sorry count  │
│ - SAT      │    │ - LRAT certs   │
│   solvers  │    │                │
│ - Human    │    │ BINARY: ✓ or ✗ │
│   input    │    └────────────────┘
└────────────┘           │
                         │ feedback
                         ▼
               ┌──────────────────┐
               │   STATE MANAGER  │
               │                  │
               │ - Git branches   │
               │ - Checkpoints    │
               │ - sorry DB       │
               │ - Proof tree     │
               └──────────────────┘
```

### 5.2 The Generate-Verify Loop

Every proof attempt follows this loop:

```
1. ORCHESTRATOR selects a sorry (open subgoal)
2. ORCHESTRATOR assigns it to a GENERATOR agent
3. GENERATOR produces candidate tactic/proof term
4. VERIFIER runs `lake build` on the modified file
5. IF compiles: commit to branch, update sorry dashboard
   IF fails: extract error message, feed back to GENERATOR
6. GOTO 1
```

The key insight: **the verifier is infallible.** Lean's type checker is the ground truth. The generators are fallible heuristics. The framework's job is to make the generators fail fast and iterate quickly.

### 5.3 Technology Stack

```
┌─────────────────────────────────────────────────┐
│ Layer 4: Orchestration                          │
│   Python (or similar) process manager           │
│   Git-based state management                    │
│   Dashboard / monitoring                        │
├─────────────────────────────────────────────────┤
│ Layer 3: AI Generators                          │
│   LLM agents (Claude, GPT-4, Gemini)           │
│   APOLLO-style multi-agent pipeline             │
│   ReProver/LeanDojo v2 tactic generation        │
│   LeanCopilot in-process suggestions            │
├─────────────────────────────────────────────────┤
│ Layer 2: Classical Solvers                      │
│   Lean-Auto (ATP integration)                   │
│   bv_decide / LeanSAT (SAT reasoning)          │
│   CaDiCaL / Kissat (external SAT solvers)       │
│   PBLean (pseudo-Boolean reasoning)             │
│   omega, simp, decide, norm_num (Lean tactics)  │
├─────────────────────────────────────────────────┤
│ Layer 1: Formal Verification                    │
│   Lean 4 compiler + type checker                │
│   Mathlib4 library                              │
│   Custom 4CT library (our code)                 │
├─────────────────────────────────────────────────┤
│ Layer 0: Infrastructure                         │
│   Git repositories                              │
│   CI/CD (GitHub Actions or similar)             │
│   Container orchestration (Docker/K8s)          │
│   GPU compute (for LLM inference)               │
└─────────────────────────────────────────────────┘
```

---

## 6. Agent Swarm Design

### 6.1 Agent Types

We define five agent roles, inspired by the APOLLO and BFS-Prover-V2 architectures:

#### Agent Type 1: Planner
- **Role:** Takes a `sorry` and decomposes it into sub-lemmas.
- **Input:** A Lean proof state (the goal and local context).
- **Output:** A `have` / `suffices` / `calc` skeleton with multiple smaller `sorry`s.
- **Model:** Strong reasoning LLM (Claude, GPT-4, or Gemini 2 Pro).
- **Why:** The 4CT proof has deep dependency trees. Breaking goals into subgoals is the highest-leverage activity.

#### Agent Type 2: Tactic Generator
- **Role:** Fills a single `sorry` with a tactic proof.
- **Input:** A Lean proof state (narrow goal).
- **Output:** A sequence of tactics (e.g., `intro h; apply foo; exact bar`).
- **Model:** ReProver (fine-tuned ByT5) or LeanCopilot.
- **Why:** Most subgoals, once properly decomposed, are individually tractable.

#### Agent Type 3: SAT Worker
- **Role:** Handles computational verification tasks (reducibility checks, specific graph properties).
- **Input:** A graph configuration + property to verify.
- **Output:** An LRAT proof certificate that Lean can consume via `bv_decide` or native SAT.
- **Model:** CaDiCaL / Kissat solver.
- **Why:** Reducibility of each configuration is a finite computation. SAT solvers are the right tool.

#### Agent Type 4: Repair Agent
- **Role:** Takes a failed proof attempt + Lean error message and fixes it.
- **Input:** Broken `.lean` file + compiler error.
- **Output:** Fixed `.lean` file.
- **Model:** LLM with Lean error parsing (APOLLO-style).
- **Why:** Most LLM-generated proofs have syntax/type errors. Rapid repair is essential for iteration speed.

#### Agent Type 5: Explorer
- **Role:** Tries unconventional proof strategies. Proposes new lemmas, definitions, or approaches.
- **Input:** The current proof tree + sorry list + history of failed attempts.
- **Output:** New `.lean` files with alternative proof skeletons.
- **Model:** Strong reasoning LLM with long context.
- **Why:** Avoid getting stuck. The explorer generates "lateral moves" when the main strategies stall.

### 6.2 Agent Communication

Agents communicate through the **shared proof state** (the Git repository). There is no direct agent-to-agent messaging. This is deliberate:

1. All state is in `.lean` files → always verifiable
2. No "telephone game" where agent A tells agent B something incorrect
3. The orchestrator reads the repo state and assigns work

### 6.3 Parallelism Model

```
ORCHESTRATOR
    │
    ├── Branch: strategy/discharging
    │     ├── Planner Agent → decompose discharging proof
    │     ├── Tactic Agent 1 → work on discharge rule 1
    │     ├── Tactic Agent 2 → work on discharge rule 2
    │     └── SAT Worker → verify configuration reducibility
    │
    ├── Branch: strategy/kempe-topological
    │     ├── Planner Agent → decompose Kempe non-crossing proof
    │     ├── Tactic Agent 3 → work on Jordan Curve consequence
    │     └── Explorer Agent → try sheaf-theoretic formulation
    │
    ├── Branch: strategy/five-color-first
    │     ├── Planner Agent → decompose 5CT proof
    │     ├── Tactic Agent 4 → Euler formula subgoal
    │     └── Tactic Agent 5 → induction step
    │
    └── Branch: strategy/sat-reducibility
          ├── SAT Worker Pool (8 workers) → batch-verify 633 configs
          └── Repair Agent → fix LRAT integration issues
```

**Key constraint:** Multiple branches can run in parallel, but within a branch, work is sequential (each sorry depends on the proof state created by resolving prior sorries).

---

## 7. Proof Strategy Pipelines

Each pipeline is a sequence of concrete tasks targeting a specific proof approach.

### 7.1 Pipeline A: Port and Modernize (Conservative)

**Goal:** Reproduce the RSST proof in Lean 4, learning from Gonthier's Coq.

| Step | Task | Tests | Dependencies |
|------|------|-------|-------------|
| A1 | Define hypermaps in Lean 4 (following Gonthier's `hypermap.v`) | Level 0 planarity tests pass | Mathlib SimpleGraph |
| A2 | Formalize Euler's formula for hypermaps | Euler formula test | A1 |
| A3 | Formalize Kempe chain theory | Level 2 tests pass | A1 |
| A4 | Formalize the 32 RSST discharging rules | Discharging test passes | A2 |
| A5 | Build reducibility checker as Lean `decide` procedure | Level 3 (single config) passes | A3 |
| A6 | Batch-verify all 633 configurations | Level 4 passes | A5 |
| A7 | Connect discharging + unavoidability + reducibility | Level 5 passes | A4, A6 |

**Estimated effort:** 12-24 months with heavy automation.  
**Risk:** This is "just" a port. High certainty of eventual success, but limited novelty.

### 7.2 Pipeline B: SAT-Boosted Reducibility (Hybrid)

**Goal:** Use modern SAT solvers to verify reducibility, reducing the Lean proof burden.

| Step | Task | Tests | Dependencies |
|------|------|-------|-------------|
| B1 | Encode each of 633 RSST configurations as a graph in Lean | Config encoding test | Level 0 |
| B2 | For each config: reduce 4-colorability to CNF | CNF generation test | B1 |
| B3 | For each config: run CaDiCaL, produce LRAT certificate | SAT solve completes | B2 |
| B4 | For each config: verify LRAT certificate in Lean via `bv_decide` | Level 3/4 tests pass | B3 |
| B5 | Prove unavoidability via discharging (traditional proof) | Discharging test | Level 0 |
| B6 | Connect unavoidability + SAT-verified reducibility | Level 5 passes | B4, B5 |

**Estimated effort:** 6-12 months (SAT verification is fast; discharging proof is the bottleneck).  
**Risk:** The LRAT certificate approach is proven (Hadwiger-Nelson project did exactly this for graph non-colorability). The main risk is that the discharging proof (B5) requires substantial manual formalization.

**This is the recommended first pipeline.** It has the highest ratio of leverage (SAT does the heavy lifting for reducibility) to effort (we only need to formalize the discharging argument ourselves).

### 7.3 Pipeline C: Shrink the Unavoidable Set (Novel)

**Goal:** Use SAT solvers to find better discharging rules, shrinking 633 configs.

| Step | Task | Tests | Dependencies |
|------|------|-------|-------------|
| C1 | Implement discharging rule search in Python (not Lean) | Rule search produces valid rules | None |
| C2 | For each candidate rule set: compute implied unavoidable set | Unavoidable set test | C1 |
| C3 | For each configuration in set: SAT-verify reducibility | All configs reducible | C2 |
| C4 | Find minimum-size unavoidable set of reducible configs | N_min found | C1-C3 loop |
| C5 | Formalize the best rule set found in Lean 4 | Discharging test passes | C4, Level 0 |
| C6 | SAT-verify all configs in the minimized set in Lean | Level 4 passes | C4, Pipeline B |

**Estimated effort:** 3-6 months for the search (Python), + Pipeline B effort for formalization.  
**Risk:** The minimum N might still be large (>100). We don't know until we search. But even reducing from 633 to 200 would be a publishable result.

### 7.4 Pipeline D: Novel Proof Exploration (Speculative)

**Goal:** Let AI agents explore non-standard proof strategies.

| Step | Task | Tests | Dependencies |
|------|------|-------|-------------|
| D1 | Formalize chromatic polynomial basics in Lean | P(G,k) definition compiles | Level 0 |
| D2 | Prove P(K4, 4) > 0 (trivial test case) | Sanity test passes | D1 |
| D3 | Let Explorer agents try to prove P(G,4) > 0 for planar G | Any partial result | D2 |
| D4 | Formalize nowhere-zero flow basics | Flow definition compiles | Level 0 |
| D5 | Let Explorer agents try flow-based 4CT | Any partial result | D4 |
| D6 | Formalize Colin de Verdiere's invariant | mu(G) definition compiles | Level 0 |
| D7 | Let Explorer agents try spectral approach | Any partial result | D6 |

**Estimated effort:** Ongoing / open-ended.  
**Risk:** High probability of failure for any individual approach. But the framework makes failure cheap — a failed attempt is just a branch that never merges.

---

## 8. Branching, Checkpointing, and State Management

### 8.1 Git-Based Proof State

The entire proof state lives in a Git repository. Every proof attempt is a branch.

```
main                    # Stable: only proven (sorry-free) lemmas
├── infra/planarity     # Working: planarity definitions
├── infra/kempe         # Working: Kempe chain formalization
├── strategy/pipeline-a # Working: conservative port
│   ├── a/discharging   # Sub-branch: discharging rules
│   └── a/reducibility  # Sub-branch: reducibility checker
├── strategy/pipeline-b # Working: SAT-boosted approach
│   └── b/config-batch  # Sub-branch: batch SAT verification
├── strategy/pipeline-c # Working: minimized unavoidable set
│   └── c/search-round-7 # Sub-branch: search iteration 7
├── strategy/pipeline-d # Experimental: novel approaches
│   ├── d/chromatic-poly # Sub-branch: algebraic approach
│   └── d/flow-based    # Sub-branch: flow approach (abandoned)
└── graveyard/          # Tag: abandoned branches (for reference)
```

### 8.2 Checkpoint Protocol

A **checkpoint** is a Git tag on a branch where:
1. `lake build` succeeds (no compilation errors)
2. The sorry count is recorded
3. A machine-readable manifest lists all remaining sorries

```yaml
# checkpoint-manifest.yaml
checkpoint: pipeline-b-v12
date: 2026-03-15
branch: strategy/pipeline-b
lean_version: 4.16.0
mathlib_version: 2026-03-10
sorry_count: 47
sorries:
  - file: FourColor/Discharge/Rule7.lean
    line: 142
    goal: "∀ v, deg(v) ≥ 7 → finalCharge v ≥ 0"
    difficulty: medium
    assigned_to: tactic-agent-3
    attempts: 5
    last_error: "unknown identifier 'Finset.sum_nonneg'"
  - file: FourColor/Reduce/Config23.lean
    line: 88
    goal: "isReducible config_23"
    difficulty: mechanical
    assigned_to: sat-worker-pool
    attempts: 0
    status: queued
  # ... 45 more
```

### 8.3 Branch Lifecycle

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  CREATE   │───▶│  ACTIVE   │───▶│  REVIEW   │───▶│  MERGED   │
│           │    │           │    │           │    │ (to main) │
└──────────┘    └─────┬─────┘    └──────────┘    └──────────┘
                      │
                      │ sorry count stagnant
                      │ for > 2 weeks
                      ▼
                ┌──────────┐
                │  STALLED  │──── human review ───▶ RESUME or ABANDON
                └──────────┘
```

**Merge criteria:** A branch merges to `main` when:
- `lake build` succeeds
- Zero `sorry`s in the merged files
- No regressions in existing tests
- At least one new test file passes

### 8.4 Dealing with Upstream Changes

Mathlib4 updates frequently. Our strategy:
- Pin to a specific Mathlib version per checkpoint
- Monthly rebase onto latest Mathlib
- CI runs on both pinned and latest versions
- If latest breaks, we stay pinned until fixed

---

## 9. Skeptic's Reality Check

This section is deliberately pessimistic. Read it before getting excited.

### 9.1 What AI Can Actually Do Today (February 2026)

| Claim | Reality |
|-------|---------|
| "AI can prove theorems" | AI can prove **simple** theorems. AlphaProof solved IMO problems — impressive, but these are single-page proofs with well-defined problem types. The 4CT proof is 60,000 lines of deeply interdependent formal mathematics. |
| "LLMs understand math" | LLMs are **very good at pattern matching** on proof states and can generate plausible tactics. They do not "understand" why a proof works. They hallucinate tactics that don't exist, confuse similar-sounding lemma names, and cannot plan more than ~5 steps ahead reliably. |
| "We can just port the Coq proof" | Porting 60,000 lines of Coq to Lean 4 is not "just" anything. The type theories differ. SSReflect idioms don't translate directly. Gonthier's hypermap formalization has no Lean analogue. Estimated: 12-24 person-months of expert work. |
| "SAT solvers can verify everything" | SAT solvers can verify **finite combinatorial properties**. The reducibility of each configuration is finite and SAT-verifiable. The discharging argument is NOT — it's an infinite argument ("for ALL planar graphs...") that requires a proper mathematical proof. |
| "Agent swarms will solve it" | Agent swarms accelerate search but don't change what's findable. If a proof doesn't exist (e.g., a spectral approach), no amount of search will find it. Swarms help with **coverage** (trying many approaches) and **speed** (filling in routine steps), not with **insight**. |

### 9.2 What Will Actually Be Hard

1. **Planarity formalization.** There is no planarity definition in Lean 4 Mathlib. Gonthier invented hypermap-based combinatorial planarity specifically for the 4CT. Someone has to either port this or develop a new approach. This is a significant research-engineering project in itself.

2. **The discharging proof.** This is a traditional mathematical argument that requires human-level insight to formalize. It involves case analysis on local vertex configurations, and the 32 RSST rules interact in subtle ways. AI may help fill in steps, but a human will need to provide the proof structure.

3. **Connecting the pieces.** Even if we have formalized planarity, Kempe chains, discharging, and SAT-verified reducibility, connecting them into a coherent proof requires understanding the global proof architecture. This is currently a human task.

4. **Lean/Mathlib API churn.** Mathlib4 is a moving target. Definitions change, lemma names change, API conventions evolve. A multi-month project will need to adapt repeatedly.

### 9.3 What Might Realistically Happen

**Optimistic scenario (18 months):**
- Level 0-1 (planarity + 5CT) formalized in Lean 4
- Pipeline B (SAT-boosted reducibility) verified for all 633 configurations
- Discharging argument partially formalized, ~50 sorries remaining
- Pipeline C produces a reduced unavoidable set of ~200-400 configurations
- Total: A near-complete Lean 4 proof with human-assisted completion plausible

**Realistic scenario (18 months):**
- Level 0-1 formalized with some gaps
- Pipeline B verified for ~100 configurations
- Discharging argument sketched with ~200 sorries
- Pipeline C finds some rule set improvements but no dramatic reduction
- Total: A solid framework with substantial work remaining

**Pessimistic scenario (18 months):**
- Level 0 partially done (planarity is harder than expected)
- Pipeline B blocked on LRAT integration issues
- No progress on discharging
- Total: Good infrastructure, minimal proof content

### 9.4 The Honest Value Proposition

Even in the pessimistic scenario, the framework has value:
- A reusable Lean 4 graph theory library with planarity support
- A template for SAT-verified combinatorial proofs in Lean
- A tested agent orchestration system for formal proof search
- Documentation of what works and what doesn't, saving future teams months

---

## 10. Implementation Roadmap

### Phase 0: Environment Setup (Week 1-2)

| Task | Tool | Output |
|------|------|--------|
| Install Lean 4 + Mathlib4 | elan, lake | Working build environment |
| Set up Git repo with CI | GitHub Actions | `lake build` runs on every push |
| Create test file scaffolding | Manual | `tests/Level0_Planarity.lean` through `Level5_FourColorTheorem.lean` with all-sorry skeletons |
| Set up sorry-counting script | Python/shell | Dashboard showing sorry count per file |
| Install LeanDojo v2 | pip | Python ↔ Lean interface working |
| Install CaDiCaL | cargo/make | SAT solver producing LRAT certificates |
| Create virtual environment | venv | Isolated Python deps for orchestration layer |

### Phase 1: Foundations (Weeks 3-8)

| Task | Agent | Test |
|------|-------|------|
| Define `IsPlanar` (combinatorial, via Kuratowski) | Human + LLM | K4 planar, K5 not |
| Prove Euler's formula for planar graphs | Human + LLM | $V - E + F = 2$ test |
| Prove $E \leq 3V - 6$ | LLM tactic agent | Edge bound test |
| Prove existence of vertex with $\deg \leq 5$ | LLM tactic agent | Low-degree test |
| Define Kempe chains | Human | Type-checks |
| Prove Kempe swap preserves proper coloring | LLM tactic agent | Level 2 test |
| **Milestone: Level 0 passes** | | |

### Phase 2: Five Colour Theorem (Weeks 9-14)

| Task | Agent | Test |
|------|-------|------|
| Formalize induction on vertex count | Human + Planner | Proof skeleton compiles |
| Handle $\deg(v) \leq 4$ case | LLM tactic agent | Compiles |
| Handle $\deg(v) = 5$ case with Kempe swap | Human + LLM | Compiles |
| **Milestone: Level 1 passes (Five Colour Theorem in Lean 4)** | | |

This milestone is independently publishable and validates the entire infrastructure.

### Phase 3: SAT Pipeline (Weeks 10-20, parallel with Phase 2)

| Task | Agent | Test |
|------|-------|------|
| Encode 633 RSST configurations as Lean graph objects | Codegen script | All 633 parse correctly |
| Write Lean ↔ DIMACS CNF translation for colorability | Human + LLM | Round-trip test on small graphs |
| Run CaDiCaL on all 633 configs, collect LRAT certificates | SAT Worker pool | All 633 UNSAT (= reducible) |
| Write LRAT ↔ Lean `bv_decide` bridge | Human | Single config verified in Lean |
| Batch-verify all 633 certificates in Lean | SAT Worker pool | Level 4 partial pass |
| **Milestone: All 633 configurations SAT-verified in Lean** | | |

### Phase 4: Discharging (Weeks 15-30)

| Task | Agent | Test |
|------|-------|------|
| Formalize charge assignment $c(v) = 6 - \deg(v)$ | LLM | Definition compiles |
| Prove total charge = 12 for triangulations | LLM tactic agent | Compiles |
| Formalize each of 32 RSST discharging rules | Human + LLM (iterative) | Each rule compiles |
| Prove charge conservation under each rule | LLM tactic agent | Compiles |
| Prove unavoidability: after discharging, positive-charge vertices contain a configuration from the set | Human-heavy | Level 4 unavoidability test |
| **Milestone: Level 4 passes (unavoidable + reducible)** | | |

### Phase 5: Assembly (Weeks 28-36)

| Task | Agent | Test |
|------|-------|------|
| Connect: "minimal counterexample" → "contains unavoidable config" → "config is reducible" → "contradiction" | Human + Planner | Level 5 passes |
| **Milestone: Four Colour Theorem proved in Lean 4** | | |

### Phase X: Novel Exploration (Ongoing, parallel)

| Task | Agent | Test |
|------|-------|------|
| Pipeline C: Search for smaller unavoidable sets | Python + SAT | N_min decreases |
| Pipeline D: Algebraic/flow/spectral approaches | Explorer agents | Any new sorry-free lemma |
| Proof optimization: compress, simplify, humanize | ImProver-style agent | Proof size decreases |

### Timeline Summary

```
Week:  1    4    8    12   16   20   24   28   32   36
       |====|====|====|====|====|====|====|====|====|
       ▼    ▼              ▼                   ▼
       ENV  L0   L1        SAT ALL 633         L5?
       SETUP PASS PASS      VERIFIED           ASSEMBLY
                                               
       ├─── Phase 1 ──┤
            ├──── Phase 2 ─────┤
            ├────── Phase 3 (parallel) ────────┤
                        ├──── Phase 4 ─────────────────┤
                                          ├─ Phase 5 ──┤
       ├──────────── Phase X (ongoing) ────────────────┤
```

---

## Appendix A: Existing Tools and Versions

### Lean 4 Ecosystem (as of February 2026)

| Tool | Version/Date | Purpose | URL |
|------|-------------|---------|-----|
| Lean 4 | 4.x (latest stable) | Proof assistant core | github.com/leanprover/lean4 |
| Mathlib4 | Rolling (pin per checkpoint) | Math library | github.com/leanprover-community/mathlib4 |
| LeanDojo v2 | Dec 2025 release | ML ↔ Lean interface | github.com/lean-dojo |
| ReProver | v2 (Lean 4 only) | Tactic generation model | github.com/lean-dojo/reprover |
| Lean-Auto | 2025 release | ATP integration | Link in paper |
| LeanCopilot | Current | In-process LLM suggestions | github.com/lean-dojo/LeanCopilot |
| `bv_decide` | Built into Lean 4 | SAT reasoning (successor to LeanSAT) | Built-in |
| PBLean | Feb 2026 | Pseudo-Boolean certificates | arxiv.org/abs/2602.08692 |
| elan | Current | Lean toolchain manager | github.com/leanprover/elan |
| lake | Built into Lean 4 | Build system | Built-in |

### SAT Solvers

| Solver | Purpose | Notes |
|--------|---------|-------|
| CaDiCaL | Primary SAT solver | Produces LRAT proofs; SAT Competition winner |
| Kissat | Alternative SAT solver | Faster on some instance types |

### AI Proof Tools (reference only — not all publicly available)

| Tool | Status | Notes |
|------|--------|-------|
| AlphaProof | Not public | DeepMind; demonstrates what's possible |
| APOLLO | Research code | Multi-agent Lean framework |
| BFS-Prover-V2 | Research | Planner + parallel provers |
| ImProver | Research | Proof optimization |

### Existing Coq 4CT Proof

| Repository | URL |
|------------|-----|
| rocq-community/fourcolor | github.com/rocq-community/fourcolor |
| ~170 theory files, ~60,000 lines | Compiles with modern Coq/Rocq |

---

## Appendix B: The Proof Dependency Graph

The 4CT proof has a clear dependency structure. Understanding this is critical for parallelizing work.

```
                    ┌─────────────────┐
                    │  4CT (Level 5)  │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
     ┌────────────┐  ┌────────────┐  ┌────────────┐
     │ Discharging│  │Unavoidable │  │Reducibility│
     │  (32 rules)│  │  Set (N    │  │  (N checks)│
     │            │  │  configs)  │  │            │
     └─────┬──────┘  └─────┬──────┘  └─────┬──────┘
           │               │               │
           │          ┌────┘               │
           │          │                    │
           ▼          ▼                    ▼
     ┌──────────┐  ┌──────────┐     ┌──────────┐
     │ Euler's  │  │  Charge  │     │  Kempe   │
     │ Formula  │  │Assignment│     │  Chains  │
     └────┬─────┘  └────┬─────┘     └────┬─────┘
          │              │               │
          └──────────────┼───────────────┘
                         │
                         ▼
                  ┌──────────────┐
                  │  Planarity   │
                  │  Definition  │
                  └──────────────┘
                         │
                         ▼
                  ┌──────────────┐
                  │  SimpleGraph │
                  │  (Mathlib)   │
                  └──────────────┘
```

**Parallelizable work:**
- Discharging formalization and SAT reducibility verification can run in parallel (they share dependencies on planarity and Kempe chains but not on each other).
- All 633 (or N) SAT verifications are embarrassingly parallel.
- Pipeline C (search for smaller unavoidable sets) can run independently of Lean formalization.
- Pipeline D (novel approaches) is entirely independent.

**Sequential bottlenecks:**
- Planarity must come first. Everything depends on it.
- Kempe chain theory must precede both reducibility and the 5CT.
- The final assembly (Level 5) requires all prior levels.

---

## Final Note

This framework is designed to be **honest about what it can and cannot do**. It cannot conjure mathematical insight from computation. What it CAN do is:

1. **Make verification instant.** Every candidate proof step is checked in seconds.
2. **Make failure cheap.** A failed approach costs compute time, not human months.
3. **Make progress visible.** The sorry dashboard shows exactly where we are.
4. **Make parallelism possible.** Independent subgoals can be attacked simultaneously.
5. **Make the ground truth unambiguous.** Lean's type checker is the final arbiter.

The best-case outcome is a new Lean 4 formalization of the Four Colour Theorem — potentially with a smaller unavoidable set than RSST, discovered by SAT search. The worst-case outcome is a well-tested framework for formal proof engineering with reusable graph theory infrastructure.

Both outcomes are worth pursuing.

---

*Agent 1221 — SolvingFrameworkPlan*  
*17 February 2026*
