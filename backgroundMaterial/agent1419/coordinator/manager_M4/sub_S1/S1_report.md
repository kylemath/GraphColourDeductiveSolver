# M4-S1 Report: Adversarial Review of Case Analysis (M3-S1)

**Agent:** 1419-M4-S1
**Status:** COMPLETE — Multiple gaps identified

## Attack 1: The Case Decomposition is Incomplete

M3-S1 analyzes degree-4 and degree-5 separately, treating the link structure as the organizing principle. But the case decomposition misses:

**The starting colouring matters.** The analysis considers what happens at a SINGLE step of the BFS path. But the path has multiple steps, and the merge-proneness at step $i$ depends on the colouring at step $i$, which is the RESULT of steps 0 through $i-1$. M3-S1 implicitly assumes each step can be analyzed independently, but:

- A safe swap at step $i$ might CREATE a new merge-prone situation at step $i+1$
- The "preparatory swap" that resolves the merge-prone chain might introduce a DIFFERENT merge-prone chain

**Verdict: GAP.** The analysis treats merge-proneness as static but it's dynamic. Each swap changes the colouring and potentially the merge-prone landscape.

## Attack 2: The "Safe (a,5)-Swap Not Adjacent to v" Assumption

M3-S1 and M1-S3 data shows that alternative swaps are always "safe (a,5)-swap not adjacent to v." But this classification is only at step $i$. After the swap:

- The new colouring may have a DIFFERENT set of merge-prone chains
- A chain that was "not adjacent to v" might become adjacent after a colour rearrangement

**Question for M3:** Is "not adjacent to v" a STABLE property through the path, or can it change?

**Analysis:** Colour 5 is special — it's the colour we're trying to eliminate. A safe (a,5)-swap changes which vertices have colour 5 (it might eliminate some and create others). This reshuffles the $B_{a,5}$ subgraph. So "adjacent to $v$" in $B_{a,5}$ can change after a swap.

**BUT:** We're in $G-v$, so "$v$'s neighbours" are fixed (they're structural). What changes is whether those neighbours are in $B_{a,5}$, i.e., whether they're coloured $a$ or $5$. A safe (a,5)-swap can change a neighbour of $v$ from colour $a$ to $5$ or vice versa, IF the swapped chain reaches that neighbour.

Wait — the safe swap is on a chain NOT adjacent to $v$'s neighbourhood. So by definition, $v$'s neighbours are NOT in the swapped chain. Their colours don't change. So the merge-proneness w.r.t. $v$ is unchanged.

**Correction:** This attack fails. The safe swap doesn't affect $v$'s neighbours' colours, so merge-proneness is preserved. The next step still sees the same merge-prone situation.

**But this means:** If the merge-prone chain is still there after the safe detour, how does the detour help? The detour must change something ELSE that creates a new path to 4-colouring.

## Attack 3: The Distance Penalty Compounds

M3-S1 assumes the 1-step detour costs exactly +1 to the path length. But this assumes:
- The detour doesn't cascade (one detour leads to another)
- The detour at each induction step is independent

**In the inductive proof:** At each of $n-4$ induction steps, we might need a detour. If each costs +1, the total distance is $(n-4) + k$ where $k$ is the number of steps needing detours.

At n=9, the maximum distance was 4 (bound n-4=5, actual max=4). If we add detours, the actual distance increases. What bound can we prove?

**Worse case:** If EVERY step needs a detour, the distance doubles to $2(n-4)$. Is this acceptable?

**Actually:** The distance bound is for a single R(G-v, 5) traversal, not the full induction. At each induction level, we remove one vertex and traverse R(G-v, 5). The traversal distance is at most $n-4$ (or $n-3$ with detour). This happens $n-4$ times as we reduce from $n$ vertices to 4. But the total work is:

$\sum_{k=5}^{n} (k-3) = \sum_{k=5}^{n} (k-3) = \frac{(n-3)(n-4)}{2} - 1$

This is quadratic in $n$. The +1 detour adds at most $n-4$ extra steps total, which is negligible compared to the quadratic total.

**Verdict:** The distance penalty does NOT compound dangerously. This attack fails.

## Attack 4: Hidden Assumption in Planarity

M3-S1 uses "by planarity" frequently without specifying which planarity property is needed. The formal argument requires:

1. The link of a degree-≤5 vertex forms a cycle (for triangulations: yes)
2. Kempe chains don't cross in the planar embedding (Theorem A)
3. The bichromatic subgraph inherits planarity (yes, it's a subgraph)

But: does non-crossing of chains (Theorem A) apply in $G-v$? When $v$ is removed, the planarity is preserved (subgraph of planar graph is planar). Theorem A applies to any planar graph with any proper colouring.

**Verdict:** This attack fails. Planarity is correctly applied.

## Summary of Attacks

| Attack | Target | Result |
|--------|--------|--------|
| 1. Dynamic merge-proneness | Case analysis assumes static | **GAP CONFIRMED** |
| 2. Safe swap stability | Can safe swaps become unsafe? | Attack fails (safe swaps don't change v's nbr colours) |
| 3. Distance compounding | Does +1 per step blow up? | Attack fails (negligible) |
| 4. Planarity assumption | Are planarity claims valid? | Attack fails (correctly applied) |

**Key finding:** Attack 1 is genuine. The case analysis doesn't handle the dynamic nature of merge-proneness through a multi-step path. However, Attack 2's failure partially addresses this: safe swaps preserve the merge-prone structure, so at least the situation doesn't worsen.

## Open Question for M3

If a safe swap preserves the merge-prone situation (Attack 2 analysis), how does the detour help? The safe swap must change something about the GLOBAL colouring that opens a new path, even though the LOCAL merge-proneness is unchanged. What exactly changes?

**Hypothesis:** The safe swap eliminates colour 5 from some vertices FAR from $v$, reducing $|V_5|$. After enough such reductions, the 4-colouring is achieved without ever needing the unsafe swap.
