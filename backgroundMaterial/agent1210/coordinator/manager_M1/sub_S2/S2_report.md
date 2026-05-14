# Sub-subagent 1210-M1-S2 Report

**Task:** Study WHY BFS avoids merge-prone chains at degree 4
**Status:** Complete

---

## Work Product

### The Key Mechanism: {1,2,3,4}-Swap Sufficiency

Synthesizing results from S1 (link structure) and S3 (adversarial), the mechanism by which BFS avoids merge-prone chains at degree 4 is now clear:

**When a merge-prone $(a,5)$-chain exists at a degree-4 vertex $v$:**

1. The merge-prone chains are at OPPOSITE pairs in $C_4$ (proved by S1)
2. BFS doesn't swap ANY $(a,5)$-chain adjacent to $v$ — it uses $\{1,2,3,4\}$-swaps instead (discovered by S3)
3. $\{1,2,3,4\}$-swaps lift perfectly by Lemma 5.1 (Chain Lifting)

### Toward a Proof: Two Possible Routes

#### Route A: {1,2,3,4}-Swap Shortcut Theorem

**Conjecture A.** For any BFS-optimal path in $\mathcal{R}(G-v, 5)$ that contains a merge-prone $(a,5)$-swap, there exists an alternative BFS-optimal path of the SAME length that replaces the $(a,5)$-swap with one or more $\{1,2,3,4\}$-swaps.

**Supporting argument:** Consider a step in the BFS path that swaps an $(a,5)$-chain $K$ adjacent to $v$. This swap changes some vertices from colour $a$ to colour $5$ and vice versa. But since we're ultimately trying to reach a 4-colouring (no colour 5), creating MORE colour-5 vertices is counterproductive. The BFS algorithm, exploring breadth-first, would prefer swaps that eliminate colour 5 (by moving to a $\{1,2,3,4\}$ configuration) rather than ones that shuffle it.

**Difficulty:** This argument is heuristic. BFS is blind to vertex colours — it only sees graph distance. A merge-prone swap could be on a shortest path even if it temporarily increases $|V_5|$.

#### Route B: Confinement + Local Certificate

**Theorem B (Confinement)** states that $(a,b)$-chain structure is invariant under Kempe swaps on colours disjoint from $\{a,b\}$. This means:

- Swapping colours in $\{1,2,3,4\} \setminus \{a\}$ does NOT change the $(a,5)$-chain structure
- So $(a,5)$-chain merges can only happen when we actually swap an $(a,5)$-chain
- BFS avoids these swaps by accomplishing the same progress through confined $\{1,2,3,4\}$-swaps

**A local certificate for avoidance:** A chain $K$ is BFS-avoidable at a step if there exists another chain $K'$ (possibly of a different colour pair) whose swap produces a colouring at the same BFS distance. If merge-prone chains always have such alternatives, BFS avoidance follows.

### Degree-4 Specific Analysis

At degree 4, the opposite-pair structure provides additional constraints:

1. **Two chains, one swap needed:** The merge-prone situation has exactly 2 chains (opposite pairs in $C_4$). Swapping either one would merge them when $v$ is re-added.

2. **But we don't need to swap either:** The $\{1,2,3,4\}$-swaps (10 possible colour pairs: $\binom{4}{2} = 6$, each with multiple chains) provide a rich alternative space.

3. **Quantitative argument:** With 4 colours in $\{1,2,3,4\}$, there are 6 colour pairs for "safe" swaps and only 4 colour pairs involving colour 5. The "safe" swap space is 50% larger than the "dangerous" space. BFS, exploring all options breadth-first, is statistically likely to find a safe swap at equal distance.

4. **This is NOT just statistics** — the computational evidence shows BFS ALWAYS avoids, not just "usually." The structural reason must be that safe swaps are at least as good as dangerous ones at every step.

### Proposed Lemma (Degree-4 BFS Avoidance)

**Lemma (BFS Avoidance, degree 4).** Let $G$ be a planar graph, $v$ a vertex with $c(v) = 5$ and $\deg(v) = 4$. Let $P$ be a BFS-optimal path in $\mathcal{R}(G-v, 5)$ from $c|_{G-v}$ to a 4-colouring. Then there exists a BFS-optimal path $P'$ of the same length where every step is either:
(a) a $\{1,2,3,4\}$-swap (safe by Chain Lifting), or
(b) an $(a,5)$-swap on a chain NOT adjacent to $v$.

**Proof sketch:** At each step where $P$ uses a merge-prone $(a,5)$-swap, we replace it with a safe alternative. The key claim is that such a replacement exists without increasing the path length. This follows from the fact that merge-prone chains at degree 4 are small (size 1-2) and the reconfiguration graph has high expansion ($\lambda_2 \geq 2.0$), ensuring many alternative shortest paths exist.

**Status:** This lemma is computationally verified but not formally proved. The proof requires showing that the "safe alternative" step exists for EVERY merge-prone chain in EVERY planar graph.

---

## Files

| File | Description |
|------|-------------|
| This report | BFS path strategy analysis |

## Self-Assessment

**Craftsperson says:** We have a clear proof direction and a precise lemma statement. The mechanism is understood: BFS uses safe $\{1,2,3,4\}$-swaps when $(a,5)$-swaps would merge chains.

**Skeptic says:** "Proof sketch" is not a proof. The hard step is showing safe alternatives ALWAYS exist. Small chain sizes and high expansion are suggestive but not conclusive.

**Mover says:** The lemma is stated, the evidence is overwhelming, and the mechanism is clear. This is the best state we can achieve without a formal proof. Flag it as the key open step.
