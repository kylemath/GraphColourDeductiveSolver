# M3-S1 Report: Case Analysis for Safe Path Existence

**Agent:** 1419-M3-S1
**Status:** COMPLETE — Proof sketch with identified gaps

## Approach

For each colour-type at a degree-4/5 vertex $v$ with $c(v) = 5$, prove that when BFS encounters a merge-prone $(a,5)$-chain, a safe alternative swap always exists.

## Degree-4 Case Analysis

In a triangulation, a degree-4 vertex $v$ has link $C_4$: neighbours $u_1$-$u_2$-$u_3$-$u_4$-$u_1$.

### Key structural constraint (Merge Geometry)
For $(a,5)$-merge to occur at degree 4: $v$ has 2+ neighbours in $B_{a,5}(G-v)$ belonging to distinct chains. Since the link is $C_4$, adjacent neighbours share an edge and MUST be in the same chain. Therefore only **opposite pairs** $(u_1, u_3)$ or $(u_2, u_4)$ can be in different chains.

This means: at most ONE colour $a$ can be merge-prone at any degree-4 vertex (because only one pair of opposite neighbours can be non-adjacent in $B_{a,5}$, and there are only 4 colours to distribute among 4 neighbours).

### Degree-4 colour types (neighbours of $v$, $c(v) = 5$):

Since $v$ has 4 neighbours coloured from $\{1,2,3,4\}$ (they can't be 5 in a proper colouring... wait, they CAN be 5 — other neighbours of $v$ can be coloured 5 too).

Actually: in a proper 5-colouring, $v$'s neighbours can have ANY colours in $\{1,2,3,4,5\} \setminus \{5\}$... no, $v$ is coloured 5, so neighbours can be $1,2,3,4$ OR $5$ as long as they're not adjacent to $v$ with the same colour. But $c(v)=5$, so neighbours CANNOT be 5. They must be in $\{1,2,3,4\}$.

**Correction:** Neighbours of $v$ are coloured $\{1,2,3,4\}$ (since $c(v) = 5$ and the colouring is proper).

So the 4 neighbours use colours from $\{1,2,3,4\}$. For colour $a$ to be merge-prone, we need 2+ neighbours coloured $a$ (which are then in $B_{a,5}$). But wait — neighbours can also be coloured 5 in $B_{a,5}$... but we just said neighbours are in $\{1,2,3,4\}$.

**Key insight:** In $G-v$, neighbours of $v$ have their original colours ($\{1,2,3,4\}$). But $B_{a,5}(G-v)$ contains vertices coloured $a$ OR $5$. Vertices coloured 5 are elsewhere in the graph (not neighbours of $v$, since $v$ was the one coloured 5 and is removed).

Actually, OTHER vertices in $G-v$ can be coloured 5. The 5-colouring of $G$ uses colour 5 on vertices beyond just $v$.

So: neighbours of $v$ are coloured $\{1,2,3,4\}$, but they can be in $B_{a,5}(G-v)$ if they're coloured $a$. And those chains can extend through the rest of the graph (which may include colour-5 vertices).

### Merge-prone analysis at degree 4:

For colour $a$ to be merge-prone:
- At least 2 neighbours of $v$ are coloured $a$
- These neighbours are in distinct $(a,5)$-chains in $G-v$
- Only opposite pairs in $C_4$ can be in distinct chains

**Type 1: Two opposite neighbours have the same colour $a$**
- $c(u_1) = c(u_3) = a$, and they're in different $(a,5)$-chains in $G-v$
- Safe alternative: swap a DIFFERENT $(a,5)$-chain (one not adjacent to $v$)
- Alternative exists IF there's another $(a,5)$-chain in $G-v$ whose swap achieves the BFS target

**Type 2: Three or four neighbours coloured $a$**
- More than 2 neighbours coloured $a$
- All adjacent pairs are in the same chain (by C_4 link)
- For 3+ neighbours coloured $a$: at least 2 pairs are adjacent, so at most 2 chains
- Same argument: safe alternative exists if another chain is available

### Proof attempt for degree 4:

**Claim:** In $R(G-v, 5)$, if the BFS-optimal path at step $i$ would swap a merge-prone $(a,5)$-chain $K$ adjacent to $v$, then there exists an alternative swap at step $i$ that:
1. Also reaches a colouring at the same or one-greater distance from a 4-colouring
2. Is safe (either a $\{1,2,3,4\}$-swap or a safe $(a,5)$-swap)

**Proof sketch:**
- Let $K$ be the merge-prone chain. Swapping $K$ moves some vertices from colour $a$ to 5 and vice versa.
- Consider all $(a,5)$-chains in $G-v$. By planarity + non-crossing (Theorem A), these chains are non-interleaving around $v$.
- Since $K$ is merge-prone, it touches $v$'s neighbourhood at 2+ points in different chains.
- There must be at least one other $(a,5)$-chain $K'$ that:
  - Is not adjacent to $v$'s neighbourhood (safe)
  - Achieves a similar or smaller "colour reduction" effect

**GAP:** The existence of $K'$ with the right properties is not guaranteed. In the counterexample at n=9, all optimal paths lack such an alternative. The alternative exists at distance +1 but not at the optimal distance.

### Resolution of the gap:

The degree-4 case may actually work for OPTIMAL paths (counterexamples at n=9 are degree 5, and the degree-4 counterexamples involve the first BFS path but DO have safe optimal alternatives).

**Check:** Do the T_9_25 and T_9_35 counterexamples involve degree-4 or degree-5 vertices?
- T_9_25: v=3 is degree **5** (24 true counterexamples)
- T_9_25: v=5 is degree **4** (57 first-path merges, BUT safe optimal alternatives exist)
- T_9_35: v=6 is degree **4** (32 first-path merges, true counterexamples — 24 with all optimal paths unsafe)
- T_9_35: v=3 is degree **5** (6 first-path merges)

**Correction:** T_9_35 v=6 (degree 4) IS a true counterexample with all optimal paths unsafe!

So the degree-4 case is NOT clean. There exist degree-4 cases where all optimal paths are unsafe.

### Revised conclusion for degree 4:

The case analysis cannot prove safe OPTIMAL paths exist at degree 4. But it may prove safe NON-OPTIMAL paths exist. The key mechanism is:
1. The unsafe swap at step $i$ reduces distance by 1
2. A safe detour at step $i$ may increase distance by 1 (two steps instead of one)
3. Net effect: safe path of length opt+1

This is consistent with the computational data (counterexamples at distance 2, safe paths at distance 3).

## Degree-5 Case Analysis

The C_5 link is more permissive: non-adjacent pairs include $(u_1,u_3), (u_1,u_4), (u_2,u_4), (u_2,u_5), (u_3,u_5)$. This allows more merge-prone configurations and is where both counterexample vertices live.

The same approach applies but with weaker constraints. The non-crossing property (Theorem A) still constrains chain arrangements, but with 5 points on the cycle there are more possible interleaving patterns.

## Summary

| Case | Optimal path safe? | Non-optimal safe path exists? |
|------|-------------------|-------------------------------|
| deg 3 | YES (proved) | N/A |
| deg 4 | NO (CE at n=9) | YES (verified n≤9) |
| deg 5 | NO (CE at n=9) | YES (verified n≤9) |

**The proof must target non-optimal safe path existence, not optimal path safety.**

## Self-Assessment (Tripartite)

**Craftsperson:** The case analysis correctly identifies the structural constraints. The C_4 merge geometry is clean. The key insight — that safe alternatives exist at distance +1 — is consistent with all data.

**Skeptic:** The proof SKETCH is not a proof. The claim "safe non-optimal path exists" requires showing that the 1-step detour always works. What if at n=15, the detour costs 5 steps? What if the detour introduces NEW merge-prone situations at later steps? The induction step needs to handle the detour's side effects.

**Mover:** Degree 4 vs degree 5 is a distraction at this stage. Focus on the mechanism: why does a 1-step detour always suffice? Is this a property of the reconfiguration graph's structure (local connectivity) or a coincidence at small $n$?
