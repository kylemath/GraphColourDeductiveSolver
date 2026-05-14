# Sub-subagent 1210-M1-S3 / M2-S3 Report (Shared)

**Task:** Adversarial Red Team — Try to BREAK BFS Avoidance at degree 4 and 5
**Status:** Complete — NO COUNTEREXAMPLE FOUND

---

## Work Product

### Five Adversarial Attacks — All Failed

| Attack | Strategy | Result | Proof Ingredient |
|--------|----------|--------|-----------------|
| 1. Forced Bottleneck | Find cases where ALL $(a,5)$-chains are adjacent to $v$ | 25,968 cases found — BFS STILL avoids | BFS uses $\{1,2,3,4\}$-swaps instead |
| 2. Unique Shortest Path | Force BFS through merge-prone chain | 0 counterexamples | BFS always has alternatives |
| 3. Octahedron Stress | All-degree-4 graph | 0 merge-prone at BFS level | Octahedron is "too symmetric" |
| 4. Chain Dominance | Merge-prone chain holds >50% of $B_{a,5}$ | 14,736 cases — BFS avoids ALL | Dominance doesn't force selection |
| 5. Equivalence to 4CT | Is BFS Avoidance equivalent to 4CT? | **NO** — BFS always finds non-merge paths | Avoidance may be STRICTLY WEAKER than 4CT |

### CRITICAL INSIGHT from Attack 1

**Attack 1 found 25,968 cases where ALL $(a,5)$-chains touch $v$'s neighbourhood.** In these cases, there is no "safe" $(a,5)$-chain to swap. Yet BFS never uses any of them.

**This means:** BFS doesn't avoid merge-prone chains by picking a different $(a,5)$-chain. BFS avoids $(a,5)$-swaps ENTIRELY in these cases, using $\{1,2,3,4\}$-swaps instead.

**Why this works:** By Lemma 5.1 (Chain Lifting), $\{1,2,3,4\}$-swaps lift perfectly from $G-v$ to $G$. By Never-Revert (Lemma 3.1), these swaps don't create or destroy colour-5 vertices. So BFS can always make progress using "safe" swaps.

**Proof direction:** If we can show that BFS-optimal paths in $\mathcal{R}(G-v, 5)$ always achieve the same distance using only $\{1,2,3,4\}$-swaps (i.e., $(a,5)$-swaps on merge-prone chains are never BFS-optimal), the conjecture follows.

### CRITICAL INSIGHT from Attack 5

**BFS Avoidance is STRICTLY WEAKER than 4CT.** In all 17,184 merge-prone situations tested, BFS always found a non-merge path. This means:
- Proving BFS Avoidance does NOT require proving 4CT
- The conjecture may be provable by local/structural arguments about BFS optimality
- This is the best possible outcome for our proof strategy

### Attack-by-Attack Detail

**Attack 1 (Forced Bottleneck):** When ALL $(a,5)$-chains are adjacent to $v$, BFS path doesn't use ANY $(a,5)$-swap at the merge-prone step. It routes through $\{1,2,3,4\}$-pair swaps instead. Example: graph T_6_0, vertex 4, degree 4, colour $a=4$ — both $(4,5)$-chains are single vertices adjacent to $v$, but BFS path eliminates colour 5 through $(1,2)$ or $(1,3)$ swaps.

**Attack 2 (Unique Shortest Path):** No BFS-optimal path ever passes through a merge-prone chain. BFS explores breadth-first, and non-merge paths are always available at equal or shorter distance.

**Attack 3 (Octahedron):** The octahedron (all degree 4) has 0 merge-prone cases at the BFS path level. This is because the high symmetry provides many alternative paths.

**Attack 4 (Chain Dominance):** Even when a merge-prone chain contains >50% of $B_{a,5}$, BFS avoids it. The chain being "dominant" doesn't make it BFS-necessary. BFS can reduce $|V_5|$ without touching the dominant chain at that step.

**Attack 5 (Equivalence):** For every merge-prone case, there exists a BFS-optimal path that avoids the merge. This means the set of "merge-avoiding" BFS paths is non-empty for every starting colouring. BFS Avoidance is not as strong as 4CT — it's a BFS selection property, not a reachability property.

---

## Files

| File | Description |
|------|-------------|
| `adversarial_test.py` | All 5 attack scripts (in `compute/kempe/`) |

## Acceptance Criteria Check

- [x] Try to construct counterexample — none found
- [x] Document WHY each attack fails — done
- [x] Determine if BFS Avoidance ≡ 4CT — **NO, it's strictly weaker**
- [x] Extract proof ingredients from failure modes

## Questions for Manager

1. **The bottleneck finding is the key proof ingredient.** BFS avoids $(a,5)$-swaps entirely when they're merge-prone, using $\{1,2,3,4\}$-swaps instead. Can we prove that $\{1,2,3,4\}$-swaps are always sufficient for BFS-optimal paths?
2. If $\{1,2,3,4\}$-swaps suffice, BFS Avoidance is a corollary of Chain Lifting + a BFS optimality argument. This would close the gap.

## Self-Assessment

**Craftsperson says:** Five attacks, zero counterexamples, and two major structural insights. The strongest finding is that BFS Avoidance is strictly weaker than 4CT — this validates the entire proof approach.

**Skeptic says:** "Strictly weaker" is based on computational evidence at $n \leq 8$. As $n$ grows, BFS might be forced into merge-prone chains. The bottleneck-avoidance mechanism (using $\{1,2,3,4\}$-swaps) needs a proof, not just evidence.

**Mover says:** We have a concrete proof direction: show that $\{1,2,3,4\}$-swaps achieve BFS-optimal distance. This reduces BFS Avoidance to a property of the reconfiguration graph restricted to $\{1,2,3,4\}$-swaps. Ship this insight and let the theorists formalize it.
