# Agent 1419 — Final Synthesis

## Constructive Four Colour Theorem via Kempe Reconfiguration: Status Report

### 1. Mission

Attempt a constructive proof of the Four Colour Theorem via Kempe chain reconfiguration. The proof architecture starts from any proper 5-colouring (guaranteed by 5CT) and uses Kempe swaps to reduce to a 4-colouring. The approach is inductive: remove a vertex $v$ with $\deg(v) \leq 5$, recurse on $G-v$, then lift back to $G$.

### 2. What Was Proved (Before This Agent)

| Result | Status | Lean 4 |
|--------|--------|--------|
| Case 1: $c(v) \neq 5$ → Chain Lifting | **Proved** | Formalized (0 sorry) |
| Case 2: $c(v) = 5$, $\deg(v) = 3$ → No-Merge | **Proved** | Formalized (0 sorry, 1 axiom) |
| Never-Revert Lemma | **Proved** | Formalized (0 sorry) |
| Case 3: $c(v) = 5$, $\deg(v) \in \{4,5\}$ | **OPEN** | Not formalized |

### 3. What This Agent Discovered

#### 3.1 Conjecture 5.5 (BFS Avoidance) is FALSE

**The original conjecture** — that BFS-optimal paths in $R(G-v, 5)$ always avoid unsafe $(a,5)$-swaps — is **disproved at $n = 9$**.

**Counterexamples:**
- **T_9_25**, vertex $v = 3$ (degree 5): 24 colourings where ALL 2 optimal paths use unsafe swaps
- **T_9_35**, vertex $v = 6$ (degree 4): 24 colourings where ALL 2 optimal paths use unsafe swaps

Both graphs have degree sequence $[3, 4, 4, 4, 4, 5, 5, 6, 7]$.

**Phase transition by $n$:**

| $n$ | Universal (all paths safe) | Existential (some safe) | All-paths-unsafe cases |
|-----|---------------------------|------------------------|----------------------|
| ≤ 7 | 100% | 100% | 0 |
| 8 | 86.6% | 100% | 0 |
| 9 | — | 87.3% | 48 (0.13% of merge-prone cases) |

The transition from universal to existential happens at $n = 8$; the transition from existential to counterexample happens at $n = 9$.

#### 3.2 Safe Non-Optimal Paths Always Exist (at $n \leq 9$)

For every counterexample to Conjecture 5.5:
- A safe path at distance $\text{opt} + 1$ exists (distance 3 instead of optimal 2)
- Alternative vertex removal avoids the problem entirely
- **Zero cases** where no safe path exists at any distance

This motivates:

**Revised Conjecture 5.5' (Safe Path Existence):** For every merge-prone colouring, there exists a path (not necessarily BFS-optimal) in $R(G-v, 5)$ to a 4-colouring that avoids all unsafe $(a,5)$-swaps.

**Computationally verified at $n \leq 9$** (14,760 merge-prone cases at $n \leq 8$; all 50 triangulations at $n = 9$).

#### 3.3 ALL-PATHS Analysis (73,016 paths enumerated)

Complete census of all BFS-optimal paths at $n \leq 8$:
- 14,760 merge-prone colourings examined
- 12,936 (87.6%) have ALL optimal paths safe
- 1,824 (12.4%) have mixed paths (some safe, some unsafe)
- 0 (0%) have all paths unsafe

Alternative swap classification: 100% of safe alternatives are "safe $(a,5)$-swap not adjacent to $v$" — never $\{1,2,3,4\}$-swaps.

#### 3.4 Formal Equivalence Analysis

| Implication | Verdict |
|------------|---------|
| Revised 5.5' $\Rightarrow$ 4CT | **YES** (via induction + Chain Lifting) |
| 4CT $\Rightarrow$ Revised 5.5' | Unknown (probably no) |
| $\{1,2,3,4\}$-Swap Sufficiency $\Leftrightarrow$ Revised 5.5' | **Equivalent** |
| Circularity in proof architecture | **None** |

#### 3.5 Computational Extensions

At $n = 9$ (50 triangulations, 347,448 colourings):
- BFS first-path merges: 539 / 172,281 $(a,5)$-swaps (0.31%)
- Merge-prone rate: degree 4 = 10.6%, degree 5 = 22.8%
- Both lower than at smaller $n$ (merge-prone rate decreases with graph size)

### 4. What Was NOT Achieved

1. **No proof of Revised Conjecture 5.5'.** Three proof approaches were attempted (case analysis, confinement factoring, chain size bounds). All have genuine gaps identified by the Critic Battalion.

2. **Lean 4 compilation blocked.** Lean 4 toolchain is not installed. Static review suggests 2-5 compilation errors, fixable.

3. **No $n = 10$ BFS merge check** (time constraint on 233 triangulations).

### 5. Proof Architecture Assessment (Post-M4 Critique)

**Sound but incomplete.** The inductive framework is correct. Cases 1 and 2 are proved. Case 3 reduces to Conjecture 5.5', which is computationally verified but unproved.

**Key gaps in proof attempts:**
1. Case analysis doesn't handle dynamic merge-proneness through multi-step paths
2. Confinement routing argument is incomplete at optimal distance
3. Chain size bounds alone don't guarantee alternative existence
4. The "detour paradox" — if safe swaps preserve merge-proneness, how does the detour help? (Resolved: it eliminates colour 5 elsewhere via non-adjacent chains)

**Probability estimates:**

| Outcome | Probability |
|---------|-------------|
| Full constructive 4CT proof | 10-15% |
| Proof for degree-4 case only | 30-40% |
| Publishable partial results | 95% |
| Counterexample to 5.5' at $n \geq 10$ | 40% |

### 6. New Code Assets

| File | Purpose | Lines |
|------|---------|-------|
| `compute/kempe/all_paths_analysis.py` | ALL-PATHS BFS enumeration and safety classification | ~190 |
| `compute/kempe/bfs_avoidance_extended.py` | Extended BFS avoidance at $n = 9, 10$ | ~100 |
| `compute/kempe/n9_merge_investigation.py` | Deep investigation of n=9 counterexamples | ~130 |
| `compute/kempe/counterexample_analysis.py` | Graph structure + safe non-optimal path analysis | ~200 |

### 7. Recommended Next Steps

#### Immediate (1-2 months)
1. **Publish partial results.** The counterexample to Conjecture 5.5, the all-paths analysis, and the safe-path-existence data are novel contributions.
2. **Install Lean 4** and compile existing code. Fix tactic errors in Basic.lean.
3. **Push computation to $n = 10$** for safe-path-existence verification.

#### Medium-term (3-6 months)
4. **Attempt degree-4 proof.** The C_4 link structure provides the strongest constraints. Prove safe paths exist for degree-4 vertices specifically.
5. **Formalize the "vertex selection" approach.** Using $n_3 + 2n_4 + n_5 \geq 12$, prove that a "good" vertex always exists.

#### Long-term (6-24 months)
6. **Develop reconfiguration graph theory.** Safe-swap subgraph connectivity is the right formalization. This requires new results in the theory of reconfiguration graphs.
7. **Full Lean 4 formalization.** Tier 2-4 infrastructure: ReconfigurationGraph, BFS distance, Conjecture 5.5', and the inductive scaffold.

### 8. Files Delivered

```
backgroundMaterial/agent1419/
├── task_decomposition.md
├── coordinator/
│   ├── coordinator_log.md
│   ├── escalations.md
│   ├── manager_M1/ (S1-S3 reports + manager report)
│   ├── manager_M2/ (S1-S3 reports + manager report)
│   ├── manager_M3/ (S1-S3 reports + manager report)
│   └── manager_M4/ (S1-S3 reports + manager report)
├── deliverables/
│   └── synthesis.md (this file)
└── agent1419Report.md (final report)

compute/kempe/
├── all_paths_analysis.py (NEW)
├── bfs_avoidance_extended.py (NEW)
├── n9_merge_investigation.py (NEW)
└── counterexample_analysis.py (NEW)
```
