# Proof Strategies — Iteration 2 (Post-CDL Disproval)

**Agent:** 0050-M2-S2
**Date:** 18 February 2026
**Iteration:** 2

---

## Context Shift

The strict CDL is disproved. All three strategies must be re-evaluated in light of this. The target has shifted from "prove CDL" to "prove unrestricted elimination works" or "prove linear distance bound."

---

## Strategy A: Distance-Based (REVISED)

### Original Idea
If $v_1$ and $v_2$ are in different $(c_1, x)$-chains, the swap at $v_2$ is safe.

### Post-CDL Status
This idea is correct but INSUFFICIENT — the data shows that $v_1$ and $v_2$ can be in the SAME chain for ALL colour pairs involving $c_1$, and no safe preparatory swaps can fix this.

### Revised Strategy A: Unrestricted Swap + Damage Bound

Instead of avoiding $v_1$, allow swaps that move $v_1$'s colour. The key question becomes: does moving $v_1$ from colour $c_1$ to colour $c_1'$ create any problems?

**Observation:** Moving $v_1$ doesn't revert it to colour 5. It changes $v_1$ to another colour in $\{1,2,3,4\}$. The resulting colouring is still proper. The "damage" is that $v_1$'s colour changes, but $v_1$ remains 4-coloured.

**This is actually fine!** If we don't require $v_1$ to keep its specific colour — only that it stays in $\{1,2,3,4\}$ — then unrestricted swaps never revert completed work.

**Lemma Candidate:** For any proper 5-colouring of a planar graph and any Kempe swap on a pair $(a,b)$ with $a, b \in \{1,2,3,4\}$: the swap preserves the property "vertex $v$ uses colour from $\{1,2,3,4\}$" for all vertices $v$ that were previously recoloured from 5.

**Proof:** A $(a,b)$-swap changes colours $a \leftrightarrow b$ on vertices in the chain. If $v$ had colour $a$ (or $b$), it gets colour $b$ (or $a$). Both are in $\{1,2,3,4\}$. If $v$ had colour $c \notin \{a,b\}$, it's unchanged. In no case does $v$ return to colour 5.

**This lemma is TRIVIALLY TRUE.** Kempe swaps on $\{1,2,3,4\}$ pairs never introduce colour 5.

**Feasibility: HIGH** — this lemma is proved.

### Consequence

The unrestricted sequential elimination strategy is now reduced to: at each step, find ANY swap that frees a colour for the current vertex. The previously recoloured vertices may change colour but never revert to 5.

The remaining question: can we always find a freeing swap? This is the single-vertex problem, which is solved by the degree-5 classification from iteration 1.

### Gap in the Argument

**Wait.** The degree-5 classification shows that a single vertex coloured 5 can always be recoloured by a single Kempe swap. But after unrestricted swaps, the graph state has changed. Does the classification still apply?

The classification depends on the LOCAL structure: the vertex $v$ has degree $\leq$ something, and its neighbours have specific colours. After a swap, the LOCAL structure around $v$ may have changed (neighbour colours may differ). But $v$ is still coloured 5, it still has degree $\leq 5$ (degree doesn't change), and its neighbours still use colours from $\{1,2,3,4,5\}$.

Actually, $v$'s neighbours that were coloured in $\{1,2,3,4\}$ still are (by the lemma above). The only concern: could a swap change a neighbour of $v$ from a non-5 colour to 5? NO — swaps on $(a,b)$ with $a,b \in \{1,2,3,4\}$ never produce colour 5.

**So the degree-5 classification applies at every step of the unrestricted elimination.** Each vertex coloured 5 has degree $\leq 5$ (we need this!) and neighbours coloured in $\{1,2,3,4\}$, so the classification guarantees a freeing swap exists.

### CRITICAL ISSUE: Degree Bound

The degree-5 classification requires that the vertex coloured 5 has degree $\leq 5$. This is NOT guaranteed for general planar graphs. A vertex could have degree 6, 7, etc. The classification covers degree-5 vertices; higher-degree vertices may need all 5 colours around them with no single swap freeing a colour.

**However:** Every planar graph has a vertex of degree $\leq 5$. By the Five Colour Theorem proof strategy: in any proper 5-colouring, there exists a vertex of degree $\leq 5$ that can be recoloured. The question is whether this vertex is among those currently coloured 5.

Actually, the standard 5-colour theorem argument processes vertices in reverse degeneracy order. The vertex coloured 5 might not be the minimum-degree vertex.

**This is a real gap.** The argument works when all colour-5 vertices have degree $\leq 5$, but may fail when some have degree $\geq 6$.

### Feasibility: Medium (was High before the degree gap was found)

---

## Strategy B: Structural Induction (Shelling Order)

### Idea
Process vertices in an order derived from the triangulation structure (e.g., reverse of construction by face-splitting). At each step, the boundary has specific properties that guarantee a freeing swap.

### Post-CDL Assessment
The CDL failure means we can't rely on protecting previous colours. But with the "damage is OK" insight from Strategy A, shelling order becomes attractive for a different reason: vertices processed early (in the "interior") may have higher degree, while vertices processed later (on the "boundary") have lower degree.

### Analysis
For a triangulation built by successive face-splitting from $K_4$:
- $K_4$ has 4 vertices, all degree 3
- Each face-split adds a degree-3 vertex
- Edge flips then redistribute degrees

The LAST vertex added (in the splitting sequence) has degree 3 and is surrounded by three vertices. If this vertex is coloured 5, it trivially has a free colour.

**Inductive step:** Remove the last-added vertex. By induction, the remaining graph's 5-colouring can be reduced to 4. When we add the vertex back, it has degree 3 and we can 5-colour it, then reduce.

**This is essentially the 5-colour theorem proof.** It doesn't give us 4-colouring; it gives us 5-colouring of the augmented graph. The problem is that "reduce the remaining graph" requires an independent argument.

### Feasibility: Medium-Low

---

## Strategy C: R(G,5) Connectivity Leverage

### Idea
Las Vergnas-Meyniel: $\mathcal{R}(G,5)$ is connected for planar graphs. This means every 5-colouring reaches every 4-colouring. Can we bound the distance?

### Key Data (from M1)
Max distance from 5-colouring to nearest 4-colouring = $n - 4$ (tight for $n = 4, \ldots, 8$).

### Analysis
The Las Vergnas-Meyniel proof uses the Fisk framework for higher chromatic numbers. The bound they prove is on the DIAMETER of $\mathcal{R}(G,k)$ for $k \geq \text{col}(G) + 1$, which is polynomial but not linear.

**Can we get a linear bound?** 

Each Kempe swap changes $O(n)$ vertex colours. In the best case, one swap "handles" one colour-5 vertex (by recolouring it). In the worst case, a swap changes many vertices but none of them are colour-5 vertices being eliminated.

The distance = $n-4$ pattern suggests that each swap effectively eliminates one colour-5 vertex from the graph. This would follow if:
1. Each 5-colouring has at most $n-4$ vertices coloured 5 (TRUE — since at least 4 vertices must be coloured with 4 distinct colours in a triangulation)
2. Each swap reduces the number of colour-5 vertices by at least 1

Property 2 is NOT true in general — a swap might increase or maintain the count of colour-5 vertices. But the BFS finds a PATH where the DISTANCE is $n-4$, implying such a monotone path exists.

**Monotone Distance Conjecture:** For any planar triangulation $G$ with proper 5-colouring $c$ using colour 5 on $k$ vertices, there exists a path in $\mathcal{R}(G,5)$ of length $\leq k$ to a 4-colouring, where each step either reduces the number of colour-5 vertices or keeps it constant while moving closer to a 4-colouring.

### Feasibility: Medium — requires understanding the structure of R(G,5) more deeply

---

## Summary Table

| Strategy | Target | Feasibility | Key Obstacle |
|----------|--------|-------------|--------------|
| A (revised) | Unrestricted elimination always works | Medium | Degree bound: works for deg-5 vertices, need argument for deg >= 6 |
| B | Shelling order induction | Medium-Low | Reduces to essentially the 5-colour theorem |
| C | Linear distance in R(G,5) | Medium | Need monotone path structure |
| A+C combined | Unrestricted + bounded | Medium-High | Most promising: Strategy A's lemma + distance bound |

### Recommended Path

**Strategy A (revised) is the most promising.** The key lemma (swaps on {1,2,3,4} never produce colour 5) is trivially true. Combined with the degree-5 classification, this gives a complete argument for degree-5 vertices. The gap is degree >= 6 vertices coloured 5.

**To close the gap:** At each step, we don't have to process the colour-5 vertices in any fixed order. We can choose to process a MINIMUM-DEGREE colour-5 vertex first. In a planar graph, the average degree is < 6, so there are always vertices of degree <= 5. The question: is there always a colour-5 vertex of degree <= 5?

Not necessarily — all colour-5 vertices could have degree >= 6. But after some unrestricted swaps, the colour-5 vertices change (some gain colour 5, some lose it). The dynamics are complex.

**Alternative closure:** Use Strategy C to show that the BFS always finds a short path, bypassing the local argument entirely.

---

*0050-M2-S2 — 18 February 2026*
