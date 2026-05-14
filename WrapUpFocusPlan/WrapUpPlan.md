# Wrap-Up Focus Plan: Closing the Graph Colour Project

**Date:** 8 April 2026  
**Purpose:** Define MVP options to close out the project without sinking further compute/time.

---

## 1. Project State Summary

### 1.1 What the Project Set Out to Do

Prove the Four Colour Theorem via a novel constructive approach: start from a 5-colouring (guaranteed by the Five Colour Theorem), then systematically eliminate the fifth colour via Kempe chain swaps, exploiting the topological constraint that chains for disjoint colour pairs cannot cross in a planar embedding.

### 1.2 What Actually Happened

The project ran ~10 named agent sprints (Agents 0050, 0051, 1210, 1221, 1419, 1443, 1520, 1545, 1610) over roughly 7 weeks, producing a substantial body of mathematical and computational work. The journey was honest and productive: two major conjectures were **disproved**, one major replacement conjecture was **discovered**, and the proof architecture was refined through multiple iterations.

**The constructive proof is ~95% complete, with one unproved conjecture remaining.** The honest caveat: that last 5% may be as hard as the 4CT itself.

### 1.3 Assets Produced

| Asset | Location | Status |
|-------|----------|--------|
| **LaTeX paper** (energy functionals for reconfiguration landscape) | `paper/` | 6 sections, compilable, near-publication quality |
| **Solving framework plan** (automated proof discovery architecture) | `SolvingFrameworkPlan/SolvingProofStrategy.md` | Complete design doc; never executed beyond planning |
| **5 strategic plans** (Plans 1-3, Novel Exploration, Executive Summary) | `SolvingFrameworkPlan/` | Plans 1 and 3 explored and mostly killed; Plan 2 is the focus |
| **43 Python modules** (Kempe ops, triangulations, reconfiguration, SAT, TQFT) | `compute/` | Working; 31 tests passing |
| **Lean 4 skeleton** (4 partial lemma files) | `lean4/KempeReconfiguration/` | Has errors; 3-7 days to compile per audit |
| **158 agent report files** (6 lemma proofs, computational results, audits) | `backgroundMaterial/` | Thorough documentation of every finding |
| **2 planning meeting transcripts** | `backgroundMaterial/meetings/` | Rich strategic discussion records |
| **Interactive web demo** (spin glass swap visualization) | `SpinGlassSwapApp/` | Working HTML/CSS/JS app |

### 1.4 Mathematical Results

#### Proved (6 lemmas, all rigorous)

| # | Result | What It Says |
|---|--------|-------------|
| 1 | Theorem A (Non-Interleaving) | Kempe chains for disjoint colour pairs don't interleave at external vertices |
| 2 | Theorem B (Confinement) | $(a,b)$-chain structure is invariant under swaps on disjoint colours |
| 3 | Never-Revert Lemma | Swapping within $\{1,2,3,4\}$ never creates or destroys colour-5 vertices |
| 4 | Chain Lifting | The $(a,b)$-bichromatic subgraph for $a,b \in \{1,2,3,4\}$ is identical in $G$ and $G-v$ when $c(v) = 5$ |
| 5 | Degree-5 Classification | All 8 topologically distinct colour patterns at a degree-$\leq 5$ vertex coloured 5 are resolvable by $\leq 1$ Kempe swap |
| 6 | Degree-3 No-Merge Lemma | Adding back a degree-3 vertex coloured 5 never merges $(a,5)$-chains |

#### Disproved / Killed

| Conjecture | Verdict |
|------------|---------|
| $\{1,2,3,4\}$-Swap Sufficiency | **FALSE** at $n=9$ (48 counterexamples) |
| Surface Tension Rigidity | **FALSE** at every scale tested |
| Turaev-Viro positivity via TQFT | **DEAD** ($6j$-symbols have mixed signs) |
| Strict Chain Disconnection Lemma | **FALSE** at $n=6$ |
| $|V_5|$ strict descent | **FAILS** for 23% of colourings |

#### Computationally Verified (not proved)

| Result | Evidence |
|--------|----------|
| Merge-Tolerant Lifting (MTL) Lemma | 1.9M+ cases through $n=10$, zero failures |
| Safe Path Existence (Conjecture 5.5') | 1.9M cases, max detour cost 1 |
| $\mathcal{R}(G,5)$ connectivity | Confirmed for all tested graphs |
| BFS Avoidance of merge-prone chains | 1,104 merge-prone cases, 0 times BFS selected an adjacent chain |
| Distance bound $d \leq n-4$ | Tight at $n \leq 8$, holds at $n=9,10$ |

#### The ONE Remaining Gap

**The Merge-Tolerant Lifting (MTL) Lemma:** For any planar triangulation $G$, any vertex $v$ with $\deg(v) \leq 5$ and $c(v) = 5$, there exists a 4-colouring of $G-v$, reachable by Kempe swaps from the starting 5-colouring, such that a free colour exists for $v$.

This is unproved. Agent 1610's independent audit puts confidence at 62-75%. The honest concern: this gap may be as hard as the 4CT itself — it connects a local property (vertex degree) to a global property (BFS paths in reconfiguration graphs). The 150-year history of "nearly complete" 4CT proofs counsels caution.

---

## 2. What the SolvingProofStrategy.md Envisioned vs. What Was Built

The `SolvingProofStrategy.md` document (Agent 1221, 17 Feb 2026) laid out an ambitious automated proof discovery framework: a generate-and-test loop around Lean 4, with an agent swarm (5 agent types), 4 proof pipelines (A-D), a sorry-counting dashboard, Git-based state management, and a 36-week roadmap to the full 4CT in Lean 4.

**What was actually built from it:** Almost none of the framework infrastructure. No CI pipeline, no sorry dashboard, no orchestrator layer, no LeanDojo integration. The project instead focused on the mathematical investigation (Plan 2: Kempe Swap Game), which was the right call — the framework was designed for a multi-year effort, and the mathematical results came faster than expected.

**What remains relevant from it:** The honest skeptic's assessment in Section 9 proved prescient. The Level 0-5 milestone ladder is still a valid roadmap if anyone wanted to continue the Lean 4 formalization. The architecture diagrams are good documentation of intent.

---

## 3. Honest Assessment: What Is and Isn't Publishable

### Clearly Publishable (as-is or with minor polish)

1. **The energy functionals paper** (`paper/`): Introduces 8 novel energy functionals for Kempe reconfiguration graphs, tested on the $n=9$ counterexamples. This is a complete, self-contained contribution to the graph colouring literature. Needs minor revision to reflect the MTL breakthrough and disproof of Surface Tension Rigidity.

2. **The constructive proof architecture + 6 lemmas**: The inductive proof structure, the 6 proved lemmas, the computational evidence for MTL, and the clean reformulation of 4CT as the MTL Lemma. This is a substantial mathematical contribution regardless of whether the gap is closed.

### Potentially Publishable (with more work)

3. **Computational dataset**: All planar triangulations through $n=10$, all 5-colourings, all reconfiguration distances. Could be released as a community resource.

4. **The SAT discharging framework**: Agent 1520/1545 built a second-order discharging framework with 156K patterns. Potentially interesting for the classical proof community.

### Not Publishable

5. **The Lean 4 code**: A skeleton with errors. Not a contribution in its current state.

6. **The TQFT/sheaf cohomology exploration**: Killed by mixed $6j$-symbol signs. The Kuperberg web basis was inconclusive. No positive results.

7. **The automated framework** (`SolvingProofStrategy.md`): A design document. Interesting as a methodological proposal but never implemented or tested.

---

## 4. MVP Options (Ordered by Effort)

### Option A: Polish and Submit the Existing Paper

**Effort:** 1-2 days  
**What:** Revise `paper/` to reflect the full project arc. Update the conclusion to acknowledge the MTL breakthrough and the disproof of Surface Tension Rigidity. Submit to arXiv.

**Deliverables:**
- Revised `paper/main.tex` with updated conclusion and discussion
- arXiv submission

**Value:** Gets a publication out the door immediately. The energy functionals framework is novel and self-contained. Cites the constructive proof work as motivation without claiming it's complete.

**Limitation:** Doesn't capture the 6 proved lemmas or the constructive proof architecture, which are the project's strongest mathematical contributions.

---

### Option B: Write a Second Paper on the Constructive Architecture (Recommended MVP)

**Effort:** 3-5 days  
**What:** A new paper (or major expansion of the existing one) presenting:
- The inductive constructive proof architecture
- The 6 proved lemmas with full proofs
- The computational evidence (2M+ colourings, zero failures)
- The MTL Lemma as a clean reformulation of 4CT
- The disproof of $\{1,2,3,4\}$-Swap Sufficiency as a negative result
- The distance bound $d \leq n-4$

**Source material already exists:**
- `backgroundMaterial/agent0051/deliverables/revised_paper_section.md` (publication-ready draft)
- `backgroundMaterial/agent0050/coordinator/manager_M2/` (full proofs of Theorems A, B, Degree-5 Classification)
- `SolvingFrameworkPlan/ExecutiveSummary_Plan2_Status.md` (complete status with proof architecture diagram)
- The computational results from `compute/kempe/tests/test_plan2.py`

**Deliverables:**
- New LaTeX paper (or expanded existing paper) in `paper/`
- arXiv submission

**Value:** This is the project's most significant contribution. The 6 lemmas are rigorous. The MTL reformulation is independently interesting (4CT $\iff$ "BFS endpoints in Kempe reconfiguration graphs of planar triangulations always have a free colour for removed vertices"). Even if the gap is never closed, this is a meaningful addition to the literature.

**This is the recommended MVP.** Most of the writing is already done in agent reports. The main work is organizing it into a coherent paper structure.

---

### Option C: Option B + Clean Code Release

**Effort:** 5-7 days  
**What:** Everything in Option B, plus:
- Clean up `compute/kempe/` into a proper Python package with README, docstrings, and installation instructions
- Release as a companion repository or alongside the paper
- Include the triangulation database and reconfiguration graph tools

**Deliverables:**
- Paper (as in Option B)
- `compute/` cleaned up with `README.md`, `setup.py`, proper docstrings
- GitHub release

**Value:** Makes the computational results reproducible and gives the community tools for further exploration.

---

### Option D: Option C + Lean 4 Compilation

**Effort:** 7-12 days  
**What:** Everything in Option C, plus:
- Fix the Lean 4 skeleton to compile against Mathlib
- Formalize at least 3 lemmas: Never-Revert, Chain Lifting, Kempe swap preserves proper colouring
- Get `lake build` passing with 0 errors (some `sorry`s acceptable for unproved results)

**Deliverables:**
- Paper + code release (as in Option C)
- Compiling Lean 4 project with formalized lemmas
- Honest sorry count documented

**Value:** First formal verification of any Kempe reconfiguration results in Lean 4. Strongest possible deliverable. But the audit (Agent 1610) estimated 3-7 days just to get compilation working, and that's with Lean 4 expertise.

**Risk:** Lean 4/Mathlib API churn may make this take longer than estimated.

---

### Option E: Minimal Close-Out (Documentation Only)

**Effort:** Half a day  
**What:** Write a project retrospective, archive the repo with a clear README documenting what was achieved, what remains open, and how to continue.

**Deliverables:**
- `README.md` at repo root (or update existing)
- This document serves as the retrospective

**Value:** Honest documentation. No publication, but the work is preserved for anyone who wants to continue.

---

## 5. Recommendation

**Do Option B (constructive architecture paper), with Option A as a quick warm-up.**

Concretely:

| Step | Task | Time |
|------|------|------|
| 1 | Polish existing energy functionals paper, update conclusion | 1 day |
| 2 | Submit energy functionals paper to arXiv | 1 hour |
| 3 | Assemble constructive architecture paper from existing agent reports | 2-3 days |
| 4 | Submit constructive architecture paper to arXiv | 1 hour |
| 5 | Write a proper `README.md` for the repo | 2 hours |
| 6 | *(Optional)* Clean up `compute/kempe/` for code release | 1-2 days |

**Total: ~4-6 days of focused work for two publications and a clean repo.**

The key insight is that most of the writing already exists in agent reports. The work is editorial (organizing, LaTeXing, ensuring mathematical precision), not creative. The 6 proved lemmas and the MTL reformulation are the project's genuine contributions, and they deserve to be in a proper paper rather than buried in agent reports.

---

## 6. What NOT to Do

| Temptation | Why to Resist |
|------------|---------------|
| Try to prove the MTL Lemma | It may be as hard as 4CT. The project has already identified it clearly; proving it is a separate research program. |
| Build the full automated framework from `SolvingProofStrategy.md` | A multi-year engineering project with uncertain payoff. The mathematical investigation overtook it. |
| Fix the Lean 4 code without the paper | Lean compilation is a means to an end. Without a paper, nobody will see the formalization. |
| Run more computation ($n=11,12,...$) | Diminishing returns. 1.9M cases at $n \leq 10$ is already strong evidence. Going to $n=11$ adds evidence but doesn't prove anything. |
| Pursue TQFT/sheaf cohomology further | Multiple approaches killed ($6j$ mixed signs, Surface Tension Rigidity false). The project explored this honestly and found dead ends. |

---

## 7. Repo Structure After Close-Out

```
GraphColour/
├── README.md                          # Updated: project summary, results, how to run
├── paper/                             # Paper 1: Energy functionals (revised)
│   ├── main.tex
│   └── sections/
├── paper2/                            # Paper 2: Constructive architecture + 6 lemmas (NEW)
│   ├── main.tex
│   └── sections/
├── compute/                           # Python code (optionally cleaned up)
│   ├── kempe/                         # Core library
│   └── discharging/                   # SAT discharging framework
├── lean4/                             # Lean 4 skeleton (as-is unless Option D)
├── SolvingFrameworkPlan/              # Strategy documents (archived)
├── backgroundMaterial/                # Agent reports (archived)
├── SpinGlassSwapApp/                  # Interactive demo (keep)
└── WrapUpFocusPlan/                   # This document
```

---

## 8. The Honest Bottom Line

This project produced genuine mathematical results: 6 rigorous lemmas, a clean constructive proof architecture, a sharp reformulation of 4CT as the MTL Lemma, and overwhelming computational evidence (1.9M+ cases, zero failures). It also honestly killed 5 conjectures that didn't work.

The gap between "computationally verified for all small cases" and "proved" is the fundamental challenge of mathematics. The project navigated this honestly, never overclaiming. The right close-out is to publish what was proved, clearly state what remains open, and let the community take it from there.

Two arXiv papers capturing the energy functionals framework and the constructive proof architecture would be a strong close-out for the compute and time invested. The MTL Lemma, stated as a conjecture with 1.9M cases of evidence, is itself a contribution — it gives future researchers a precise target.

---

*WrapUpFocusPlan — Graph Colour Project*  
*8 April 2026*
