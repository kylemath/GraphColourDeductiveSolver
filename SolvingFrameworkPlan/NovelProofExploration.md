# Novel Proof Exploration: A Pipeline D-Only Strategy

**Project:** Graph Colouring — Four Colour Theorem  
**Date:** 17 February 2026  
**Author:** Agent 1221  
**Follows:** `SolvingProofStrategy.md` (Pipeline D refocus)  
**Philosophy:** New proof or nothing. But prove something small and real first.

---

## Table of Contents

1. [Strategic Decision](#1-strategic-decision)
2. [The Verifiable Foundation: Earn the Right to Explore](#2-the-verifiable-foundation-earn-the-right-to-explore)
3. [The Seven Exploration Tracks](#3-the-seven-exploration-tracks)
4. [Track Details](#4-track-details)
5. [What "Progress" Means for Speculative Work](#5-what-progress-means-for-speculative-work)
6. [Computational Exploration Layer (Python)](#6-computational-exploration-layer-python)
7. [The Kill Criteria: When to Abandon a Track](#7-the-kill-criteria-when-to-abandon-a-track)
8. [Infrastructure and Tooling](#8-infrastructure-and-tooling)
9. [Honest Assessment of Each Track](#9-honest-assessment-of-each-track)
10. [Implementation Order](#10-implementation-order)

---

## 1. Strategic Decision

We are explicitly **not** pursuing:
- Pipeline A (conservative Coq port)
- Pipeline B (SAT-boosted reducibility of the known 633 configs)
- Pipeline C (shrinking the unavoidable set within the existing proof framework)

These are engineering projects that reproduce known results. We want a **new proof** — one that reveals *why* four colours suffice, not one that repeats the brute-force check that they do.

This means we accept higher risk of total failure. The mitigation is:
1. **Prove something real first** — build a verifiable foundation so our tools and infrastructure are tested on problems we know have solutions.
2. **Run multiple tracks in parallel** — any single track will probably fail, but running seven gives reasonable odds that at least one yields new mathematical insight.
3. **Define kill criteria** — every track has explicit conditions under which we abandon it, so we don't sink unlimited time into dead ends.

---

## 2. The Verifiable Foundation: Earn the Right to Explore

Before exploring novel proof directions, we need to prove we can prove *anything* about graph colouring in our chosen toolchain. This is not the boring part — it's the necessary part. Without it, we're writing fiction, not mathematics.

### 2.1 The Foundation Milestone: Five Colour Theorem in Lean 4

The Five Colour Theorem (Heawood, 1890) is the natural foundation. It uses exactly the same machinery we'll need for novel 4CT approaches (planarity, Euler's formula, Kempe chains) but is provable by a clean induction with a single Kempe swap. No computer assistance required. No unavoidable sets. Pure deductive mathematics.

**Why this is the right foundation:**

| Property | 5CT | 4CT |
|----------|-----|-----|
| Planarity definition needed | Yes | Yes |
| Euler's formula needed | Yes | Yes |
| Kempe chains needed | Yes | Yes |
| Degree-5 vertex analysis | Yes (one swap) | Yes (swaps can interfere) |
| Computer verification needed | **No** | Yes (in known proofs) |
| Doable in Lean 4 today | **Yes** (hard but tractable) | Unknown |

If we can formalize the 5CT, we've built all the infrastructure for any novel 4CT attempt. If we can't, we have no business attempting the 4CT.

### 2.2 Foundation Steps (In Order)

Every step here produces a Lean 4 file that compiles. No `sorry` allowed at the end of each step.

#### Step F1: Graph Colouring Basics (Mathlib already has this)

Verify we can use Mathlib's existing `SimpleGraph.Coloring` and `SimpleGraph.Colorable`. Write test files:

```lean
-- Foundation/F1_ColoringBasics.lean
-- TEST: K4 is 4-colorable, C5 is 3-colorable, etc.
-- Uses only existing Mathlib. Must compile with 0 sorry.
```

**Effort:** Days. This is just learning the API.

#### Step F2: Planarity Definition

This is the hardest foundation step. Mathlib has no `IsPlanar`. We need one.

Two options:
- **Option A (Fast, Weaker):** Define planarity as `¬ (K5 ≤m G) ∧ ¬ (K33 ≤m G)` using Mathlib's graph minor machinery. This is the Wagner/Kuratowski characterization. It's correct but doesn't give us a planar embedding to work with.
- **Option B (Slow, Stronger):** Define a combinatorial planar embedding (rotation system or hypermap a la Gonthier). This gives us face structure, which some novel approaches need.

**Recommendation:** Start with Option A. It's enough for the 5CT and most novel approaches. Build Option B only if a track specifically requires face structure (the TQFT track will).

```lean
-- Foundation/F2_Planarity.lean
-- TEST: K4 is planar. K5 is not planar. K33 is not planar.
-- Petersen graph is not planar. Dodecahedron is planar.
```

**Effort:** 2-4 weeks. This is real formalization work.

#### Step F3: Euler's Formula and the Degree Bound

```lean
-- Foundation/F3_EulerFormula.lean
-- TEST: For planar G with V ≥ 3: E ≤ 3V - 6
-- TEST: Every planar graph has a vertex of degree ≤ 5
```

**Effort:** 1-2 weeks given F2.

#### Step F4: Kempe Chains

```lean
-- Foundation/F4_KempeChains.lean
-- TEST: Kempe chain swap preserves proper colouring
-- TEST: If v has deg ≤ 4, any (k≥5)-colouring of G-v extends to G
```

**Effort:** 1-2 weeks.

#### Step F5: Five Colour Theorem

```lean
-- Foundation/F5_FiveColorTheorem.lean
theorem five_color_theorem :
    ∀ (G : SimpleGraph V) [Fintype V] [DecidableRel G.Adj],
    G.IsPlanar → G.Colorable 5 := by
  -- Induction on |V|, remove min-degree vertex,
  -- 4 cases trivial, deg-5 case uses one Kempe swap
  <proof>
```

**Effort:** 2-4 weeks given F1-F4.

**Total foundation effort:** 8-14 weeks. This is non-negotiable. It produces:
- A working planarity definition in Lean 4
- Euler's formula formalized
- Kempe chain machinery formalized
- The Five Colour Theorem — a genuine, independently publishable result in Lean 4

### 2.3 Why the Foundation Validates the Framework

After Step F5, we know:
- Our planarity definition works and is usable in proofs
- Our Kempe chain machinery works and is usable in proofs
- Lean 4 + Mathlib can handle this level of graph theory
- Our agent tooling (LeanDojo, tactic generation, etc.) works on real problems
- We have a concrete proof artifact to point at

From here, every exploration track starts by extending this foundation in a different direction.

---

## 3. The Seven Exploration Tracks

Each track is an independent attempt at a novel 4CT proof via a different mathematical avenue. They share the foundation from Section 2 but diverge from there.

```
                     ┌──────────────────┐
                     │  FOUNDATION (5CT)│
                     │  F1-F5 complete  │
                     └────────┬─────────┘
                              │
     ┌────────┬───────┬───────┼───────┬───────┬────────┐
     │        │       │       │       │       │        │
     ▼        ▼       ▼       ▼       ▼       ▼        ▼
  ┌──────┐┌──────┐┌──────┐┌──────┐┌──────┐┌──────┐┌──────┐
  │Track ││Track ││Track ││Track ││Track ││Track ││Track │
  │  1   ││  2   ││  3   ││  4   ││  5   ││  6   ││  7   │
  │Kempe ││Chrom.││Flows ││TQFT/ ││Spect-││Sheaf ││Compu-│
  │Swap  ││Poly  ││      ││Penr. ││ral   ││Cohom.││tation│
  │Game  ││      ││      ││      ││      ││      ││-al   │
  └──────┘└──────┘└──────┘└──────┘└──────┘└──────┘└──────┘
```

| Track | Approach | Verifiable Artifact | Elegance | Feasibility |
|-------|----------|--------------------| ---------|-------------|
| 1 | Kempe Swap Game | Computational: can every 5-colouring be reduced to 4 by swaps? | Medium-High | **Medium** |
| 2 | Chromatic Polynomial | Prove $P(G,4) > 0$ for restricted planar families | High | Medium-Low |
| 3 | Nowhere-Zero Flows | Prove 4-flow for restricted planar families | High | Medium-Low |
| 4 | TQFT / Penrose Evaluation | Reformulate 4CT as state sum non-vanishing | **Very High** | Low-Medium |
| 5 | Spectral / Colin de Verdiere | Prove $\chi(G) \leq \mu(G)+1$ for planar graphs | **Very High** | Low-Medium |
| 6 | Sheaf Cohomology | Cohomological vanishing theorem for 4-colourability | **Very High** | Low |
| 7 | Computational Discovery | Use tensor networks / GDL to find patterns, then prove them | Medium | **Medium** |

---

## 4. Track Details

### 4.1 Track 1: The Kempe Swap Game

**The Idea:** Start with a 5-colouring (which exists by our 5CT foundation). Show that Kempe chain swaps can always eliminate one colour, reducing to a 4-colouring. This is a constructive approach — it would simultaneously prove 4CT and give an algorithm.

**Why it's promising:** This is the track closest to the classical proof but with a fundamentally different architecture. Instead of "minimal counterexample + unavoidable set + reducibility," it's "start with a valid colouring and improve it." The Five Colour Theorem already guarantees the starting point.

**Verifiable milestones:**

| Step | What to Prove | Formal/Computational | Kill if... |
|------|--------------|---------------------|------------|
| 1.1 | Define Kempe equivalence classes on colourings | Lean 4 definition | — |
| 1.2 | Prove: the 5-colouring Kempe graph of any planar graph on $\leq 12$ vertices is connected to a 4-colouring | Python computation, exhaustive | Any counterexample found |
| 1.3 | Extend computation to $n \leq 15, 18, 20$ | Python (parallelized) | Counterexample, or runtime > 1 week for $n=15$ |
| 1.4 | Characterize *which* 5-colourings are hardest to reduce | Python analysis | No pattern emerges after $n=18$ |
| 1.5 | If pattern found: formalize as Lean 4 lemma | Lean 4 proof | Formalization attempt stalls for > 4 weeks |
| 1.6 | Prove the full statement: every 5-colouring of a planar graph can be Kempe-reduced to a 4-colouring | Lean 4 proof (the dream) | — |

**Key question answered at step 1.3:** Is the Kempe reconfiguration space from 5-colourings to 4-colourings always connected for planar graphs? This is an **open problem in mathematics**. Answering it computationally for all planar graphs up to some $n$ is itself a publishable result, even without a proof.

**Tools:** Python + NetworkX for computation. Lean 4 for any formal results. No SAT needed initially — just enumeration.

### 4.2 Track 2: Chromatic Polynomial

**The Idea:** The 4CT is equivalent to $P(G, 4) > 0$ for all planar $G$. Prove this by algebraic means — analyzing the structure of the chromatic polynomial as a polynomial in $k$.

**Why it's interesting:** This would be a proof that doesn't mention colourings at all. It would work entirely in the polynomial ring. A "non-combinatorial proof of a combinatorial theorem."

**Verifiable milestones:**

| Step | What to Prove | Formal/Computational | Kill if... |
|------|--------------|---------------------|------------|
| 2.1 | Formalize $P(G,k)$ in Lean 4 via deletion-contraction | Lean 4 definition | — |
| 2.2 | Prove $P(G,k) = P(G-e,k) - P(G/e,k)$ formally | Lean 4 proof | — |
| 2.3 | Prove $P(K_n, k) = k(k-1)\cdots(k-n+1)$ | Lean 4 proof | — |
| 2.4 | Compute real roots of $P(G,k)$ for all planar triangulations $n \leq 20$ | Python (SageMath) | Roots found in $(3, 4)$ for some planar $G$ (this would be a major discovery but would dash this approach) |
| 2.5 | Prove $P(G,4) > 0$ for outerplanar graphs | Lean 4 proof | Proof attempt stalls > 6 weeks |
| 2.6 | Prove $P(G,4) > 0$ for series-parallel graphs | Lean 4 proof | Proof attempt stalls > 6 weeks |
| 2.7 | Prove $P(G,4) > 0$ for planar graphs of treewidth $\leq k$ (for increasing $k$) | Lean 4 proofs | $k$ stalls below 4 |
| 2.8 | Investigate stable polynomial / Borcea-Branden theory for $P(G,k)$ | Paper-based math | No positivity mechanism found |

**The incremental value:** Even if we never reach the full 4CT, proving $P(G,4) > 0$ for restricted planar families (outerplanar, series-parallel, bounded treewidth) would be new formalized results. Each is independently publishable.

### 4.3 Track 3: Nowhere-Zero Flows

**The Idea:** By Tutte duality, 4CT for planar graphs $\equiv$ every bridgeless planar graph has a nowhere-zero 4-flow. Prove the flow version directly.

**Verifiable milestones:**

| Step | What to Prove | Formal/Computational | Kill if... |
|------|--------------|---------------------|------------|
| 3.1 | Formalize nowhere-zero $k$-flows in Lean 4 | Lean 4 definition | — |
| 3.2 | Prove that Tutte duality relates colourings and flows for planar graphs | Lean 4 proof | — |
| 3.3 | Prove every bridgeless graph has a nowhere-zero 6-flow (Seymour's theorem) | Lean 4 proof | Stalls > 8 weeks (this is a known hard formalization) |
| 3.4 | Prove 4-flow for restricted planar families (3-edge-connected, 4-edge-connected) | Lean 4 proofs | No progress on restriction |
| 3.5 | Investigate circular flow numbers of planar graphs computationally | Python | — |
| 3.6 | Investigate group connectivity (Jaeger framework) for planar graphs | Paper math + Python | No structural insight after 3 months |

**The incremental value:** Formalizing Seymour's 6-flow theorem (step 3.3) in Lean 4 would itself be a notable contribution to Mathlib. Tutte duality formalized is also new.

### 4.4 Track 4: TQFT / Penrose Evaluation

**The Idea:** Kauffman (1990) showed that the 4CT is equivalent to the non-vanishing of the Penrose evaluation (an SO(3) state sum) for all bridgeless planar cubic graphs. This reformulates 4CT as a statement in topological quantum field theory. Prove non-vanishing by exploiting unitarity or positivity of the underlying modular tensor category.

**Why it's the most exciting:** This would be a *fundamentally new proof* — connecting a 170-year-old combinatorial problem to quantum topology. It would explain 4CT as a consequence of deep algebraic structure.

**Verifiable milestones:**

| Step | What to Prove | Formal/Computational | Kill if... |
|------|--------------|---------------------|------------|
| 4.1 | Define the Penrose evaluation for planar cubic graphs | Python (symbolic algebra) | — |
| 4.2 | Verify computationally: Penrose evaluation is nonzero for all bridgeless planar cubic graphs on $\leq 30$ vertices | Python (exhaustive) | Any zero found (would be a 4CT counterexample — extremely unlikely but must check) |
| 4.3 | Study the $6j$-symbols appearing in the planar evaluation; check sign conditions | Python (symbolic) | Signs are alternating with no clear positivity |
| 4.4 | Identify which modular tensor category structure (unitarity, sphericality) could force non-vanishing | Paper math | No candidate mechanism after 3 months |
| 4.5 | If mechanism found: formalize the state sum in Lean 4 | Lean 4 definition | — |
| 4.6 | Prove non-vanishing formally | Lean 4 proof | — |

**The honest risk:** This requires serious mathematical physics / quantum topology knowledge. The gap between "we have a reformulation" and "we can prove non-vanishing" is enormous. But the reformulation itself (4.1-4.2) is verifiable and educational.

**Requires:** Foundation Option B (planar embedding with face structure) for the full formalization. Computational work (4.1-4.3) needs only Python.

### 4.5 Track 5: Spectral / Colin de Verdiere

**The Idea:** Colin de Verdiere's invariant $\mu(G)$ satisfies $\mu(G) \leq 3$ for planar graphs. The conjecture $\chi(G) \leq \mu(G) + 1$ would immediately give $\chi(G) \leq 4$ for all planar graphs.

**Verifiable milestones:**

| Step | What to Prove | Formal/Computational | Kill if... |
|------|--------------|---------------------|------------|
| 5.1 | Define $\mu(G)$ in Lean 4 (matrix optimization with transversality conditions) | Lean 4 definition | — |
| 5.2 | Prove $\mu(K_n) = n - 1$ (known result) | Lean 4 proof | — |
| 5.3 | Prove $\mu(G) \leq 3 \Rightarrow G$ is planar (or the converse direction, which is easier) | Lean 4 proof | Stalls > 8 weeks |
| 5.4 | Computationally verify $\chi(G) \leq \mu(G) + 1$ for all graphs on $\leq 10$ vertices | Python (SageMath) | Counterexample found (would disprove the conjecture entirely) |
| 5.5 | Study the spectral structure of planar graphs via Laplacian eigenvalues | Python analysis | — |
| 5.6 | Attempt to prove $\chi(G) \leq \mu(G) + 1$ for planar $G$ | Paper math → Lean 4 | No viable proof strategy after 3 months |

**The honest risk:** The conjecture $\chi \leq \mu + 1$ is considered extremely hard. It's been open since 1990. We're unlikely to prove it. But characterizing $\mu(G)$ computationally for planar graphs and formalizing the known results ($\mu \leq 3 \Leftrightarrow$ planar) is independently valuable.

### 4.6 Track 6: Sheaf Cohomology

**The Idea:** Define a cellular sheaf $\mathcal{F}_4$ on a planar graph $G$ whose global sections are proper 4-colourings. Prove that planarity implies the vanishing of $H^1(G, \mathcal{F}_4)$, which guarantees global sections exist. A "cohomological proof of 4CT."

**Verifiable milestones:**

| Step | What to Prove | Formal/Computational | Kill if... |
|------|--------------|---------------------|------------|
| 6.1 | Define cellular sheaves on graphs in Lean 4 | Lean 4 definitions | — |
| 6.2 | Define the "colouring sheaf" $\mathcal{F}_k$ for $k$-colouring | Lean 4 definition | — |
| 6.3 | Prove: global sections of $\mathcal{F}_k$ = proper $k$-colourings | Lean 4 proof | — |
| 6.4 | Compute $H^0$ and $H^1$ of $\mathcal{F}_4$ for small planar graphs | Python (linear algebra over $\mathbb{F}_2$ or $\mathbb{Z}$) | $H^1 \neq 0$ for some planar $G$ at $k=4$ (would kill this approach) |
| 6.5 | If $H^1 = 0$ computationally: investigate why. Is there a vanishing theorem from planarity? | Paper math | No mechanism after 3 months |
| 6.6 | If mechanism found: formalize and prove | Lean 4 proof | — |

**The honest risk:** This is the most speculative track. Sheaf cohomology on graphs is a real subject (Ghrist, Hansen, Curry), but nobody has connected it to graph colouring in a way that yields the 4CT. The colouring sheaf needs to be defined carefully — the "stalks" (colour sets on vertices) and "restriction maps" (edge constraints) must be chosen so that the cohomological machinery applies. There is no guarantee such a sheaf exists with the right properties.

**The incremental value:** Formalizing cellular sheaves on graphs in Lean 4 would be new and useful infrastructure regardless of whether the 4CT application works out.

### 4.7 Track 7: Computational Discovery

**The Idea:** Use computational tools (tensor networks, symbolic algebra, GDL) to discover patterns in graph colouring that no human has noticed, then prove those patterns formally.

This is the "experimental mathematics" track. We're not trying to prove 4CT directly — we're trying to discover new lemmas or structural facts about planar graph colouring that might lead to a proof.

**Verifiable milestones:**

| Step | What to Do | Tool | Output |
|------|-----------|------|--------|
| 7.1 | Compute $P(G, k)$ for all planar triangulations $n \leq 25$ via tensor network contraction | Python + numpy | Database of chromatic polynomials |
| 7.2 | Analyze root distribution: plot all roots in $\mathbb{C}$, especially near $k = 4$ | Python + matplotlib | Root distribution atlas |
| 7.3 | Compute Kempe reconfiguration graphs for $k = 4, 5$ on planar graphs $n \leq 14$ | Python + NetworkX | Reconfiguration database |
| 7.4 | Train a GDL model (3-WL equivalent) to predict whether a Kempe chain swap sequence reduces a 5-colouring to 4-colouring | Python + PyTorch Geometric | Trained model + accuracy metrics |
| 7.5 | Analyze learned representations: what graph features does the model use? | Python (attribution analysis) | Feature importance report |
| 7.6 | If features found: formulate as conjectures | Markdown document | Conjecture list |
| 7.7 | For each conjecture: attempt formal proof | Lean 4 | Proved lemmas |

**The honest risk:** Computational discovery often produces patterns that are artefacts of the dataset, not genuine mathematical structure. Every "discovery" must be stress-tested against larger graphs before formalization is attempted.

**The unique value:** This track feeds the other tracks. A pattern discovered here might suggest a sheaf-theoretic structure (Track 6), a spectral bound (Track 5), or a Kempe swap strategy (Track 1). It's the intelligence-gathering operation.

---

## 5. What "Progress" Means for Speculative Work

For Pipelines A-C, progress is simple: sorry count goes down. For Pipeline D, we need different metrics.

### 5.1 Progress Indicators (Positive Signals)

| Signal | Meaning | Action |
|--------|---------|--------|
| Computation confirms conjecture for all $n \leq N$ | Pattern is likely real | Increase $N$; begin formalization |
| New Lean 4 lemma compiles for restricted class | Partial result on the ladder | Attempt to weaken restrictions |
| Two tracks converge on the same structure | Structure is probably important | Allocate more resources to shared structure |
| Failed proof attempt reveals specific obstruction | We understand *why* something is hard | Document obstruction; consider if another track avoids it |
| Formalized infrastructure (sheaves, flows, $\mu$) is reusable | We've built lasting tools | Continue regardless of 4CT outcome |

### 5.2 Non-Progress Indicators (Warning Signs)

| Signal | Meaning | Action |
|--------|---------|--------|
| Computation fails for $n = 8$ | Conjecture is probably false | Kill the specific conjecture; study why it fails |
| LLM generates plausible-looking proofs that all fail in Lean | The approach may not be formalizable | Step back; try smaller subgoal or different formalization |
| 6 weeks with no new compiled lemma | Track is stuck | Invoke kill criteria (Section 7) |
| Track requires mathematics nobody on the team understands | We've exceeded our competence | Seek collaboration or pivot |

### 5.3 The Publication Ladder

Even without proving 4CT, each track can produce publishable artifacts:

| Track | Publishable Even if 4CT Not Proved |
|-------|-------------------------------------|
| Foundation | "The Five Colour Theorem in Lean 4: A Formalization" |
| Track 1 | "Kempe Reconfiguration of 5-Colourings in Planar Graphs: Computational Evidence" |
| Track 2 | "Chromatic Polynomial Positivity for Bounded-Treewidth Planar Graphs" |
| Track 3 | "Seymour's 6-Flow Theorem in Lean 4" |
| Track 4 | "Computational Verification of the Penrose Evaluation for Small Cubic Graphs" |
| Track 5 | "Colin de Verdiere's Invariant: Formalization and Computation" |
| Track 6 | "Cellular Sheaves on Graphs: A Lean 4 Formalization" |
| Track 7 | "Machine Learning Structural Features of Planar Graph Colourings" |

Every one of these is independently valuable. The framework produces useful output even in total failure.

---

## 6. Computational Exploration Layer (Python)

Each track has a computational wing that runs in Python, *independent of Lean 4*. This is where hypotheses are generated and tested before formal verification is attempted. Think of it as the lab bench.

### 6.1 Shared Computational Infrastructure

```
compute/
├── graphs/
│   ├── planar_triangulations.py   # Generate all planar triangulations up to n
│   ├── graph_database.py          # SQLite DB of graphs with computed properties
│   └── generators.py              # Random planar graph generation
│
├── chromatic/
│   ├── chromatic_poly.py          # Deletion-contraction + tensor network
│   ├── root_finder.py             # Numerical root finding for P(G,k)
│   └── dsatur.py                  # DSATUR and SPARK implementation
│
├── kempe/
│   ├── kempe_chains.py            # Kempe chain identification + swap
│   ├── reconfiguration.py         # Build Kempe reconfiguration graph
│   └── reduction_search.py        # Search for 5→4 colour reduction paths
│
├── spectral/
│   ├── laplacian.py               # Graph Laplacian eigenvalues
│   ├── colin_de_verdiere.py       # μ(G) computation (SDP)
│   └── hoffman_bound.py           # Hoffman chromatic bound
│
├── topology/
│   ├── penrose_eval.py            # Penrose evaluation for cubic graphs
│   ├── state_sum.py               # Turaev-Viro state sum computation
│   └── sheaf_cohomology.py        # Cellular sheaf H^0, H^1 computation
│
├── flows/
│   ├── nowhere_zero.py            # Nowhere-zero flow enumeration
│   ├── circular_flow.py           # Circular flow number computation
│   └── tutte_polynomial.py        # Tutte polynomial computation
│
├── discovery/
│   ├── tensor_network.py          # Planar tensor network contraction
│   ├── gnn_coloring.py            # GDL model for coloring pattern discovery
│   └── pattern_mining.py          # Statistical analysis of graph features
│
└── tests/
    ├── test_all.py                # pytest suite — runs everything
    └── known_results.py           # Sanity checks against known values
```

### 6.2 The Computational Feedback Loop

```
        ┌───────────────────────┐
        │  Python Computation   │
        │  (generate hypothesis)│
        └───────────┬───────────┘
                    │
                    │ "Pattern X holds for all tested graphs"
                    ▼
        ┌───────────────────────┐
        │  Human/Agent Review   │
        │  (is this plausible?) │
        └───────────┬───────────┘
                    │
              ┌─────┴─────┐
              │           │
        Yes, try to      No, it's
        prove it         an artifact
              │           │
              ▼           ▼
        ┌──────────┐  ┌──────────┐
        │  Lean 4   │  │  Discard  │
        │  attempt  │  │  or test  │
        │           │  │  harder   │
        └─────┬─────┘  └──────────┘
              │
        ┌─────┴─────┐
        │           │
      Compiles    Fails
        │           │
        ▼           ▼
     PROVEN      Feed error
     (merge)     back to Python
                 (refine hypothesis)
```

### 6.3 Virtual Environment Setup

```bash
# All Python work runs in a venv (per user rule)
python3 -m venv .venv
source .venv/bin/activate
pip install networkx numpy scipy matplotlib sage torch torch-geometric pytest
```

---

## 7. The Kill Criteria: When to Abandon a Track

Every track has explicit kill conditions. These are commitments, not suggestions. When a kill condition is met, we stop investing in that track and redistribute effort.

| Track | Kill Condition | What It Means |
|-------|---------------|--------------|
| 1 (Kempe Swap) | A planar graph found where some 5-colouring cannot be Kempe-reduced to 4-colouring | The approach is provably impossible |
| 1 (Kempe Swap) | Computation for $n = 15$ takes > 2 weeks | Combinatorial explosion; can't gather enough evidence |
| 2 (Chromatic Poly) | Real root of $P(G, k)$ found in $(3, 4)$ for some planar $G$ | Root-bounding approach is dead |
| 2 (Chromatic Poly) | Cannot prove $P(G,4) > 0$ even for outerplanar graphs after 8 weeks | The formalization is intractable |
| 3 (Flows) | 6-flow formalization stalls for > 10 weeks | We lack the Lean infrastructure |
| 4 (TQFT) | Penrose evaluation is zero for some bridgeless planar cubic graph (= 4CT counterexample, not expected but must check) | Entire project is wrong (astronomically unlikely) |
| 4 (TQFT) | No candidate positivity mechanism after 3 months of study | We don't have the math |
| 5 (Spectral) | Counterexample to $\chi \leq \mu + 1$ found for any graph | The conjecture is false |
| 5 (Spectral) | $\mu(G)$ computation is too expensive for $n > 12$ | Can't gather enough evidence |
| 6 (Sheaf) | $H^1(G, \mathcal{F}_4) \neq 0$ for some planar $G$ at $k=4$ | The sheaf doesn't work as hoped |
| 6 (Sheaf) | Cannot define a coherent colouring sheaf after 6 weeks | The formalization is unclear |
| 7 (Computational) | GDL model accuracy below 80% on held-out planar graphs | No learnable structure |
| 7 (Computational) | All discovered patterns fail on $n > 20$ | Dataset artefacts, not mathematics |

**What happens when a track is killed:** The infrastructure built for that track (Lean definitions, Python tools, computed databases) is preserved and documented. Only the specific proof goal is abandoned. Infrastructure is never wasted.

---

## 8. Infrastructure and Tooling

### 8.1 Repository Structure

```
GraphColour/
├── SolvingFrameworkPlan/
│   ├── SolvingProofStrategy.md          # Original strategy doc
│   └── NovelProofExploration.md         # This document
│
├── lean4/                               # Lean 4 project root
│   ├── lakefile.lean                    # Build configuration
│   ├── FourColor/
│   │   ├── Foundation/                  # F1-F5: planarity, Euler, Kempe, 5CT
│   │   ├── Track1_KempeSwap/           # Track 1 formalization
│   │   ├── Track2_ChromaticPoly/       # Track 2 formalization
│   │   ├── Track3_Flows/              # Track 3 formalization
│   │   ├── Track4_TQFT/              # Track 4 formalization
│   │   ├── Track5_Spectral/          # Track 5 formalization
│   │   ├── Track6_Sheaf/             # Track 6 formalization
│   │   └── Track7_Discovery/         # Track 7: conjectures promoted to Lean
│   └── Tests/
│       ├── Sanity.lean               # K4 colorable, K5 not planar, etc.
│       └── Foundation.lean           # 5CT test
│
├── compute/                           # Python computational layer
│   ├── ... (as described in 6.1)
│   └── results/                      # Stored computation results
│       ├── chromatic_roots/          # Root distribution data
│       ├── kempe_reconfig/           # Reconfiguration graph data
│       └── penrose_evals/            # Penrose evaluation data
│
└── backgroundMaterial/               # Existing agent reports
    ├── agent1007ProblemSet.md
    ├── agent1012/
    └── agent1221/
```

### 8.2 CI Pipeline

```yaml
# .github/workflows/verify.yml (conceptual)
on: push
jobs:
  lean-build:
    steps:
      - uses: leanprover/lean-action@v1
      - run: lake build
      - run: python scripts/count_sorries.py > sorry_report.txt
      - run: python scripts/update_dashboard.py

  python-tests:
    steps:
      - run: python -m venv .venv && source .venv/bin/activate
      - run: pip install -r compute/requirements.txt
      - run: pytest compute/tests/
```

### 8.3 Minimum Viable Agent Setup

For initial work, we don't need a sophisticated agent swarm. We need:

1. **A human** who understands the mathematics and can write Lean 4 (or learn it).
2. **LeanCopilot** running in VS Code for tactic suggestions.
3. **A Python environment** for computational exploration.
4. **Git** for branching and checkpointing.

Agent swarms become useful once the foundation is complete and there are many independent sorries to fill. For the first 8-14 weeks, the bottleneck is mathematical understanding, not parallelism.

---

## 9. Honest Assessment of Each Track

### Probability of reaching a full novel 4CT proof:

| Track | P(full proof) | P(publishable partial result) | P(useful infrastructure) |
|-------|---------------|-------------------------------|-------------------------|
| 1 (Kempe Swap) | ~2% | ~40% | ~90% |
| 2 (Chromatic Poly) | ~1% | ~30% | ~80% |
| 3 (Flows) | ~1% | ~25% | ~80% |
| 4 (TQFT) | ~1% | ~20% | ~60% |
| 5 (Spectral) | <1% | ~15% | ~70% |
| 6 (Sheaf) | <1% | ~15% | ~70% |
| 7 (Computational) | <1% (itself) | ~50% (feeds others) | ~95% |

**Combined probability of at least one full novel proof: ~5-6%.** This is honest. The 4CT has resisted novel proof for 50 years. We are unlikely to be the ones who find it.

**Combined probability of at least one publishable result: ~85%.** This is the real expected value. We will almost certainly produce useful mathematics, formal infrastructure, and computational data, even if we don't prove the 4CT.

**The expected outcome is:** A Lean 4 formalization of the Five Colour Theorem, several formalized partial results (chromatic polynomial positivity for restricted classes, flow theory basics, spectral invariants), a computational database of Kempe reconfiguration graphs and chromatic polynomial roots, and possibly one genuinely new mathematical insight.

### What would change the odds:

- **A breakthrough in AI proof search** (AlphaProof-level system becoming public) would increase all probabilities by ~3-5x.
- **A new mathematical idea from a human collaborator** is the single highest-leverage event. The framework exists to test such ideas rapidly, not to replace them.
- **Discovering that two tracks converge** (e.g., the sheaf cohomology approach turns out to be equivalent to the TQFT approach) would be a signal that the shared structure is deep and worth pursuing.

---

## 10. Implementation Order

### Weeks 1-2: Environment Setup
- Install Lean 4 + Mathlib4 + LeanCopilot
- Set up Python venv with computation libraries
- Create repo structure
- Write `Sanity.lean` tests (K4 colorable, K5 not planar)

### Weeks 3-14: Foundation (F1-F5)
- This is the **non-negotiable** phase. Everything depends on it.
- Deliverable: Five Colour Theorem formalized in Lean 4.

### Weeks 6-14 (parallel with foundation): Computational Exploration
- Start Python work for Tracks 1, 2, 4, 5, 7 immediately.
- Computation doesn't need the Lean foundation; it only needs NetworkX and SageMath.
- Key early questions to answer:
  - Track 1: Are all 5-colourings of planar graphs on $n \leq 12$ Kempe-reducible to 4?
  - Track 2: What do chromatic roots of planar triangulations look like near $k = 4$?
  - Track 4: What does the Penrose evaluation look like for small cubic graphs?
  - Track 5: What is $\mu(G)$ for small planar graphs?

### Weeks 15-30: Track Exploration
- Foundation complete. Begin Lean 4 formalization on whichever tracks have the best computational evidence.
- Expected: 2-3 tracks will show promising patterns; the rest will hit kill conditions or stall.
- Focus resources on the survivors.

### Weeks 30+: Deep Pursuit
- By this point, we either have a promising direction or we don't.
- If yes: concentrated effort on formalizing the most viable approach.
- If no: publish the partial results and the infrastructure, and document what we learned for the next team.

---

## Final Word

This plan is deliberately structured so that *failure is productive*. The Five Colour Theorem in Lean 4 is valuable regardless of what happens after. The computational databases are useful to the research community regardless. The Lean 4 infrastructure for planarity, flows, sheaves, and spectral invariants fills genuine gaps in Mathlib.

The novel proof of the Four Colour Theorem, if it exists, will probably not come from brute-force search over tactic sequences. It will come from a mathematical idea — a connection between structures that nobody has noticed, or a reformulation that makes the hard part easy. The role of this framework is to make such ideas *testable in minutes instead of months*, so that when the right idea appears, we can recognize it immediately.

The framework doesn't generate insight. It accelerates it.

---

*Agent 1221 — SolvingFrameworkPlan*  
*17 February 2026*
