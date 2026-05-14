# M4-S2 Report: Adversarial Review of Confinement/Size Bound (M3-S2)

**Agent:** 1419-M4-S2
**Status:** COMPLETE — Serious logical gaps identified

## Attack 1: Local Replacement Circularity

M3-S2 claims that unsafe swaps can be "replaced" by safe alternatives via confinement. Let me check for circularity:

**The argument structure:**
1. We want to prove: a safe path exists from colouring $c$ to a 4-colouring
2. The proof claims: if the BFS path uses unsafe swap $S$, replace $S$ with safe swap $S'$
3. $S'$ exists because of confinement/size bounds

**Is step 3 circular?** Does showing $S'$ exists require knowing a safe path exists?

**Analysis:** No direct circularity — $S'$ is a SINGLE swap, not a path. The existence of one safe swap doesn't require a full safe path. The swap is identified by examining the $(a,5)$-chain structure at the current colouring.

**But:** The argument then needs to show that after $S'$, we can CONTINUE with safe swaps. This is where the induction happens: we need a safe path from the post-$S'$ colouring to a 4-colouring. This IS the same problem at a colouring that's one step closer to (or at equal distance from) a 4-colouring.

**Verdict:** Not circular, but the argument requires an INDUCTION on distance to 4-colouring. The inductive hypothesis: "all colourings at distance $\leq d$ from a 4-colouring have safe paths." The base case ($d=0$) is trivial. The inductive step needs: "if a colouring at distance $d+1$ has an unsafe BFS step, a safe swap exists that either reduces distance by 1 (to $d$) or creates a colouring at distance $\leq d$ that has a safe path."

**Gap:** The safe swap $S'$ might increase the distance. If $S'$ takes us from distance $d+1$ to distance $d+2$, the inductive argument breaks.

This is exactly what happens in the counterexamples: safe paths have distance 3 instead of optimal 2. So the safe swap goes from distance 2 to distance 2 (sideways), then from 2 to 1, then 1 to 0. The induction on distance doesn't directly apply.

**Alternative induction:** Induction on $|V_5|$ (number of colour-5 vertices). Each safe swap either reduces $|V_5|$ (if it's an (a,5)-swap) or preserves it (if it's a {1,2,3,4}-swap). The Never-Revert lemma guarantees {1,2,3,4}-swaps preserve $|V_5|$. Safe (a,5)-swaps might increase or decrease $|V_5|$.

**This induction also has issues:** (a,5)-swaps can increase $|V_5|$ by swapping some colour-$a$ vertices to colour 5 while swapping others from 5 to $a$.

## Attack 2: Size Bound Doesn't Imply Alternatives

M3-S2 claims merge-prone chains are small ($\leq 3$ vertices) and that this implies alternatives exist. Let me attack:

**Scenario:** Suppose a merge-prone $(a,5)$-chain $K$ at $v$ consists of a single vertex $u$ (size 1). Can alternatives still fail?

Yes, if:
- $u$ is the ONLY vertex coloured $a$ in $B_{a,5}(G-v)$
- No other $(a,5)$-chain exists
- Swapping $u$ is the only way to change colour $a$ near $v$

Actually, if $u$ is a single vertex, swapping the chain $\{u\}$ changes $u$ from colour $a$ to colour $5$ (or vice versa). This is a "small" swap. But if no other $(a,5)$-chain exists, there's no alternative.

However: alternatives could use DIFFERENT colour pairs. Instead of $(a,5)$, use $(b,5)$ for $b \neq a$, or $(b,c)$ for $b,c \in \{1,2,3,4\}$.

**Key question:** Does the proof require staying within the $(a,5)$ colour pair, or can it switch to a different pair?

**In the BFS path context:** BFS explores ALL possible Kempe swaps (all colour pairs, all chains). The "alternative" can be any swap that moves toward a 4-colouring. So the proof should consider all colour pairs, not just $(a,5)$.

**Verdict:** The size bound alone is insufficient. Alternatives might exist in DIFFERENT colour pairs, but the proof needs to show this explicitly. M3-S2 doesn't prove it.

## Attack 3: Routing Argument Correctness

M3-S2 sketches a "routing" argument: chains can be "routed around" merge-prone regions. In a planar graph, routing is constrained by the Jordan Curve Theorem — a chain separating two regions cannot be crossed.

**Potential flaw:** In the planar embedding, the merge-prone chains near $v$ might create a "barrier" that forces ALL paths through them. This is analogous to the min-cut/max-flow theorem: if the merge-prone chains are a cut in the bichromatic subgraph, no alternative exists.

**Data check:** In the counterexamples at n=9, all OPTIMAL paths go through the merge-prone chain. This suggests it IS a bottleneck/cut at the optimal distance. Only at distance +1 does an alternative open up.

**Verdict:** The routing argument is INCOMPLETE. It correctly observes that planarity constrains routing, but it doesn't prove that alternatives exist at distance +1. The bottleneck can exist at the optimal distance.

## Attack 4: Distance Penalty Stacking (Cross-Induction)

M3-S2 doesn't address what happens when the distance penalty from the detour at one induction level affects the next level.

**Scenario:**
- Level $n$: remove $v_n$, find safe path in $R(G-v_n, 5)$, distance is $d_n = \text{opt} + 1$
- Level $n-1$: remove $v_{n-1}$ from $G-v_n$, find safe path in $R(G-\{v_n,v_{n-1}\}, 5)$

The colouring at level $n-1$ is the END of the safe path from level $n$. This colouring might have different merge-prone properties than the "natural" colouring from level $n$ BFS.

**Question:** Does the detour at level $n$ make level $n-1$ harder or easier?

**Analysis:** The detour at level $n$ produces a different 4-colouring of $G-v_n$ than the BFS-optimal path would. This means $v_n$ might be coloured differently. At level $n-1$, the starting colouring is different, so the merge-prone analysis changes.

**Verdict:** The stacking is not obviously catastrophic but also not obviously benign. It's an open question.

## Summary

| Attack | Target | Result |
|--------|--------|--------|
| 1. Circularity in local replacement | Confinement argument | Not circular, but induction on distance breaks |
| 2. Size bound → alternatives | Chain size claim | **SIZE ALONE IS INSUFFICIENT** |
| 3. Routing argument | Planarity-based routing | **INCOMPLETE — bottleneck exists at opt distance** |
| 4. Cross-induction stacking | Distance penalty | OPEN QUESTION |

**Overall assessment:** M3-S2 has the right ideas but critical gaps in execution. The proof is not complete. The most promising path forward is the "two-step mechanism" (prepare + reduce), but proving this universally is hard.
