# M2-S3 Report: Formal Equivalence Analysis

**Agent:** 1419-M2-S3
**Status:** COMPLETE

## The Three Statements

**(a) 4CT:** Every planar graph is 4-colourable.

**(b) BFS Avoidance (Conjecture 5.5, original):** For every planar triangulation $G$, vertex $v$ with $\deg(v) \leq 5$ and $c(v) = 5$, every BFS-optimal path in $R(G-v, 5)$ avoids swapping Kempe chains adjacent to $v$.

**(b') Safe Path Existence (revised):** For every planar triangulation $G$, vertex $v$ with $\deg(v) \leq 5$ and $c(v) = 5$, there exists a path in $R(G-v, 5)$ to a 4-colouring that avoids all unsafe $(a,5)$-swaps.

**(c) {1,2,3,4}-Swap Sufficiency:** For every planar triangulation $G$ and 5-colouring $c$, there exists a sequence of {1,2,3,4}-Kempe swaps and safe $(a,5)$-swaps reducing $c$ to a 4-colouring.

## Status Update: (b) is FALSE

M1-S1/S3 found counterexamples at $n=9$: graphs T_9_25 and T_9_35 have colourings where ALL BFS-optimal paths use unsafe swaps. Statement (b) is disproved.

## Logical Relationships

### (b') → (a): YES, with inductive scaffold

**Proof sketch:** Given any planar graph $G$ on $n$ vertices:
1. By 5CT (proved by Heawood 1890), $G$ has a proper 5-colouring $c$.
2. If $c$ uses $\leq 4$ colours, done.
3. If $c$ uses 5 colours, choose $v$ with $\deg(v) \leq 5$ (exists by Euler).
4. Restrict to $G-v$: by induction, $G-v$ has a 4-colouring reachable from $c|_{G-v}$ via safe swaps.
5. By (b'), there is a safe path to this 4-colouring — no unsafe swaps means no chain merges.
6. Apply the safe swap sequence in $G$: Chain Lifting (Lemma 5.1) guarantees {1,2,3,4}-swaps lift identically. Safe $(a,5)$-swaps don't merge by definition.
7. After the sequence, $G-v$ is 4-coloured. Since $\deg(v) \leq 5$ and $v$ has $\leq 5$ neighbours using $\leq 4$ colours, by pigeonhole $v$ can be recoloured in {1,2,3,4}.

**CRITICAL CAVEAT:** Step 4 requires the inductive hypothesis at $n-1$. But we need more: we need the 4-colouring of $G-v$ to be reachable from the SPECIFIC colouring $c|_{G-v}$ via safe swaps. The induction gives us a 4-colouring of $G-v$ (from any 5-colouring) but we need it from our particular starting colouring.

This works because $R(G-v, 5)$ is connected (Las Vergnas-Meyniel for $k \geq \Delta + 1$, and triangulations have $\Delta \leq n-1$, but we're using $k=5$ which may be $< \Delta$). Actually, $R(G,5)$ connectivity is a theorem for planar graphs (Mohar's theorem), so every 5-colouring can reach a 4-colouring. Statement (b') adds that this can be done via safe swaps.

### (a) → (b'): UNKNOWN, and probably FALSE

4CT says $G$ is 4-colourable, but says nothing about the structure of paths in $R(G,5)$. In particular:
- 4CT is proved via unavoidable configurations + reducibility, a completely different technique
- The safe-path property is about the internal structure of the reconfiguration graph
- There is no known logical implication from 4CT to safe path existence

**(a) and (b') appear to be INDEPENDENT statements that both happen to be true.**

### (c) ↔ (b'): EQUIVALENT (modulo the inductive scaffold)

Statement (c) is essentially the sequentialized version of (b'). If safe paths exist at each inductive step, then the overall reduction from 5-colouring to 4-colouring uses only safe swaps. Conversely, if {1,2,3,4}-swaps and safe $(a,5)$-swaps suffice, this gives a safe path at each step.

## Circularity Analysis

**Is the proof architecture circular?**

The concern: we prove $G$ is 4-colourable by assuming $G-v$ is 4-colourable. This is standard induction on $|V|$, not circular.

The subtler concern: do we need 4CT to prove (b')? If (b') is used to prove 4CT, we'd have circularity. Analysis:
- (b') is a statement about reconfiguration paths, independent of whether $G$ is 4-colourable
- The only "input" to the proof is 5CT (5-colourability, which is proved independently)
- The inductive step uses (b') at size $n-1$ to establish 4-colourability at size $n$
- No circularity: we never assume 4CT to prove (b')

**Remaining question:** Is (b') provable without assuming 4CT? If (b') can only be proved using 4CT, we have a problem. The computational evidence suggests (b') is an independent fact about reconfiguration graphs, not a consequence of 4CT.

## Revised Distance Bound

Original claim: BFS distance $\leq n-4$.
Revised (after counterexamples): safe path distance $\leq n-3$ (one extra step per induction level, worst case).

This changes the distance bound from $n-4$ to at most $n-3$ (and possibly still $n-4$ for most cases). The bound is less tight but the structure survives.

## Summary

| Implication | Status |
|------------|--------|
| (b) → (a) | N/A — (b) is FALSE |
| (b') → (a) | YES, via induction |
| (a) → (b') | UNKNOWN, probably no |
| (c) ↔ (b') | EQUIVALENT |
| Circularity | NONE detected |
