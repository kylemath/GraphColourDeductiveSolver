# Sub-subagent 1210-M3-S3 Report

**Task:** Explore alternative proof architectures that bypass chain lifting entirely
**Status:** Complete

---

## Work Product

### Three Candidate Architectures Analyzed

---

### Candidate 1: Direct BFS Diameter Bound via Expansion

**Idea:** If $\mathcal{R}(G,5)$ is a good expander (high algebraic connectivity $\lambda_2$), then $\text{diam}(\mathcal{R}(G,5)) = O(\log |\mathcal{R}|/\lambda_2)$, giving a polynomial bound on BFS distance without any chain lifting argument.

**Evidence:**
- $\lambda_2 \geq 2.0$ observed for all $n \leq 8$ (from Agent 0051's spectral analysis)
- For connected $d$-regular graphs, $\text{diam} \leq \lceil \log(n) / \log(d/\lambda_2) \rceil$

**Analysis:**
- **Pro:** Completely bypasses chain lifting and BFS Avoidance. Would give a polynomial constructive 4CT.
- **Con:** The bound would be $O(n^2)$ or $O(n \log n)$, not the $O(n)$ bound we currently pursue. Weaker result.
- **Con:** Proving $\lambda_2 \geq c > 0$ universally requires understanding the global structure of $\mathcal{R}(G,5)$ for arbitrary planar graphs. This is a separate hard problem.
- **Con:** Mathlib has limited spectral graph theory support.

**Feasibility:** Medium-Low. The approach is clean but requires proving a universal spectral gap, which is likely as hard as the BFS Avoidance problem.

---

### Candidate 2: Greedy Algorithm with Temporary Detours

**Idea:** The $|V_5|$ descent approach fails because 23-33% of colourings don't admit a single-swap descent. But what about 2-step or 3-step lookahead? Could a greedy-with-detour algorithm always find a path?

**Evidence:**
- Single-swap descent: 70-77% success rate
- 2-step descent from resistant colourings: ~67% additional success (from Agent 0051)
- BFS always succeeds (by Las Vergnas-Meyniel), so paths exist

**Analysis:**
- **Pro:** Would give a constructive algorithm without needing BFS optimality.
- **Con:** Even 2-step lookahead doesn't reach 100%. Need arbitrary lookahead.
- **Con:** Arbitrary lookahead is essentially BFS, which brings us back to the original problem.
- **Con:** The $|V_5|$ metric is the wrong potential function. BFS doesn't minimize $|V_5|$ at each step — it minimizes distance to a 4-colouring, which sometimes INCREASES $|V_5|$.
- **Key insight from Agent 0051:** Any proof must allow non-monotone $|V_5|$ steps. The inductive lift approach naturally accommodates this.

**Feasibility:** Low. The $|V_5|$ descent approach is fundamentally limited and has been ruled out by prior work.

---

### Candidate 3: Las Vergnas-Meyniel Connectivity (Direct Diameter Bound)

**Idea:** Las Vergnas and Meyniel (1981) proved $\mathcal{R}(G,5)$ is connected for any planar graph. Their proof technique might already contain the ingredients for a diameter bound.

**Evidence:**
- Their proof uses the fact that any proper 5-colouring can be transformed to any other via Kempe swaps
- Key technique: they exploit the existence of a vertex of degree $\leq 5$ (Euler's formula) and induct
- This is essentially the SAME structure as our proof — their connectivity proof IS an inductive chain-lifting argument

**Analysis:**
- **Pro:** The connection is deep. Our proof is a quantitative refinement of LVM's qualitative connectivity proof.
- **Pro:** LVM's proof works for ALL colourings, not just BFS-optimal paths. This suggests the key property is about the reconfiguration graph itself, not about BFS.
- **Con:** LVM's proof gives no distance bound (only connectivity). Extracting a bound requires exactly the chain-lifting analysis we're already doing.
- **Key insight:** LVM's proof implicitly uses the fact that $\{1,2,3,4\}$-swaps can accomplish reductions without touching colour 5. This is precisely our Chain Lifting Lemma + Never-Revert Lemma. The remaining gap ($(a,5)$-swap avoidance) is what LVM's proof also implicitly avoids — they don't quantify how many steps it takes.

**Feasibility:** Medium. The most promising alternative, but it reduces to the same problem we already face. The insight is that LVM's proof strategy and ours are isomorphic — proving BFS Avoidance IS the quantitative version of LVM's connectivity proof.

---

### Synthesis: A NEW Proof Direction

The adversarial Red Team (M1-S3/M2-S3) discovered that BFS avoids merge-prone chains by using $\{1,2,3,4\}$-swaps exclusively in critical regions. Combined with the LVM analysis, this suggests:

**Candidate 4 (NEW): {1,2,3,4}-Swap Sufficiency**

**Claim:** For any planar graph $G$, vertex $v$ with $c(v)=5$, and BFS-optimal path $P$ in $\mathcal{R}(G-v, 5)$, there exists a BFS-optimal path $P'$ of the same length that uses only $\{1,2,3,4\}$-swaps at steps where the original path would use a merge-prone $(a,5)$-swap.

**If true:** This immediately implies BFS Avoidance (Conjecture 5.5), because $\{1,2,3,4\}$-swaps lift perfectly by Lemma 5.1.

**Key question:** Can we prove that replacing a merge-prone $(a,5)$-swap with a sequence of $\{1,2,3,4\}$-swaps achieves the same progress toward 4-colouring without increasing the path length?

**Feasibility:** Medium-High. This is the most promising direction because:
1. It directly leverages the Chain Lifting Lemma (proved)
2. It's supported by the computational evidence (BFS always has alternatives)
3. It's a local property of the reconfiguration graph (may be provable by case analysis on the degree-4/5 link structure)

---

## Summary Table

| Candidate | Approach | Feasibility | Bound Type | Status |
|-----------|----------|-------------|-----------|--------|
| 1 | Spectral gap | Medium-Low | $O(n^2)$ | Separate hard problem |
| 2 | Greedy + detour | Low | N/A | Ruled out by prior work |
| 3 | LVM direct | Medium | Same gap | Isomorphic to current approach |
| **4 (NEW)** | **{1,2,3,4}-sufficiency** | **Medium-High** | **$O(n)$** | **Most promising** |

---

## Files

| File | Description |
|------|-------------|
| This report | Feasibility analysis |

## Acceptance Criteria Check

- [x] Analyze 3+ alternative architectures
- [x] Rate feasibility
- [x] Identify most promising direction
- [x] Concrete next steps

## Self-Assessment

**Craftsperson says:** The synthesis of adversarial results with LVM analysis yielded a genuinely new proof direction ($\{1,2,3,4\}$-swap sufficiency). This wasn't in the original brief.

**Skeptic says:** "Medium-High feasibility" is still speculative. The hard part is proving that removing one $(a,5)$-swap from a BFS path can be compensated without increasing length. This requires understanding the fine structure of shortest paths in $\mathcal{R}(G-v, 5)$.

**Mover says:** Candidate 4 is the clear winner. Recommend M1 and M2 pivot to testing and proving $\{1,2,3,4\}$-swap sufficiency.
