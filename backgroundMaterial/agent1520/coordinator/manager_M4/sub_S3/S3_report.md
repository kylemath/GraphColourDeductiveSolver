# S3 Report: Kuperberg Web Basis Analysis

**Agent:** 1520-M4-S3 (Web Basis Analysis)  
**Date:** 2026-02-20  
**Status:** COMPLETE — KEY DISCOVERY

---

## Summary

Analyzed the Penrose evaluation through the lens of the Kuperberg web basis for $\mathfrak{sl}_3$ invariant tensors. **Key discovery: for all planar cubic graphs tested, the signed Penrose evaluation equals the unsigned count — every Tait colouring contributes +1 to the signed tensor contraction.** For the non-planar $K_{3,3}$, sign cancellation occurs (signed = 0, unsigned = 12). This is a structural consequence of planarity, not a new proof strategy.

---

## Background

### The Signed vs Unsigned Penrose Evaluation

The Penrose evaluation involves the Levi-Civita tensor $\epsilon_{abc}$ at each vertex. Two related quantities:

1. **Signed:** $\text{Pen}(G) = \sum_\ell \prod_{v} \epsilon_{\ell(e_1), \ell(e_2), \ell(e_3)}$ — each vertex contributes $\pm 1$
2. **Unsigned:** $|\text{Pen}|(G) = \sum_\ell \prod_{v} |\epsilon_{\ell(e_1), \ell(e_2), \ell(e_3)}|$ — each vertex contributes $+1$

The unsigned count equals the number of Tait colourings. The signed version depends on the ordering of edges at each vertex.

### Kuperberg Web Basis

Kuperberg's (1996) rank-2 spider for $\mathfrak{sl}_3$ provides a positive basis for $\text{Inv}(V^{\otimes k} \otimes (V^*)^{\otimes l})$. Web basis elements are represented by non-crossing planar diagrams. For closed tensor networks (graphs with no boundary), the invariant space is 1-dimensional, so the web basis question becomes about intermediate decompositions.

---

## Results

### Signed vs Unsigned Evaluation

| Graph | Planar | Signed | Unsigned | Equal? |
|---|---|---|---|---|
| K4 | ✓ | 6 | 6 | **YES** |
| Prism | ✓ | 6 | 6 | **YES** |
| Cube | ✓ | 24 | 24 | **YES** |
| Prism $C_4$ | ✓ | 24 | 24 | **YES** |
| Prism $C_5$ | ✓ | 30 | 30 | **YES** |
| $K_{3,3}$ | ✗ | 0 | 12 | **NO** |
| Petersen | ✗ | 0 | 0 | YES (both 0) |

**For all planar graphs: Signed = Unsigned.** Every Tait colouring of a planar graph contributes $+1$ in the signed evaluation.

**For $K_{3,3}$: Signed ≠ Unsigned.** The 12 Tait colourings split into 6 with sign +1 and 6 with sign −1, perfectly canceling.

### Partial Contraction Analysis

We tracked the state (number of positive/negative coefficient terms) as vertices are contracted one by one.

**K4 (planar):**
| Step | Vertex | Positive | Negative | Total |
|---|---|---|---|---|
| 0 | 0 | 3 | 3 | 6 |
| 1 | 1 | 6 | 6 | 12 |
| 2 | 2 | 3 | 3 | 6 |
| 3 | 3 | **6** | **0** | **6** |

Negative coefficients appear at every intermediate step until the final contraction, where they all cancel out, leaving only positive terms.

**Cube (planar):**
| Step | Vertex | Positive | Negative | Total |
|---|---|---|---|---|
| 0 | 0 | 3 | 3 | 6 |
| 1 | 1 | 6 | 6 | 12 |
| 2 | 2 | 12 | 12 | 24 |
| 3 | 3 | 0 | 18 | 18 |
| 4 | 4 | 18 | 18 | 36 |
| 5 | 5 | 6 | 24 | 30 |
| 6 | 6 | 12 | 12 | 24 |
| 7 | 7 | **24** | **0** | **24** |

At step 3, ALL 18 terms are negative. Yet the final result is entirely positive. The sign cancellation is extremely non-local.

**$K_{3,3}$ (non-planar):**
| Step | Vertex | Positive | Negative | Total |
|---|---|---|---|---|
| 0 | 0 | 3 | 3 | 6 |
| 1 | 1 | 18 | 18 | 36 |
| 2 | 2 | 108 | 108 | 216 |
| 3 | 3 | 24 | 24 | 48 |
| 4 | 4 | 6 | 6 | 12 |
| 5 | 5 | 6 | 6 | 12 |

For $K_{3,3}$, the positive/negative balance persists to the end — the signed evaluation is 0. Note: the unsigned evaluation gives 12 (the 12 Tait colourings), but they cancel in the signed version.

**Petersen (non-planar):**
The state becomes empty (0 terms) after step 8, confirming no Tait colourings exist at all.

### Edge Cut Decomposition (Cube)

Cut the cube along the 4 "equatorial" edges connecting the two faces:
- Both parts have **all-negative** coefficients (15 each)
- This means the natural tensor decomposition at a planar edge cut does NOT have non-negative coefficients

---

## Key Mathematical Interpretation

### Why Signed = Unsigned for Planar Graphs

This is a **consequence of planarity**, not a discovery. For a planar graph with a fixed planar embedding:

1. The embedding determines a cyclic ordering of edges at each vertex
2. This cyclic ordering defines a canonical $\epsilon$-orientation
3. For every Tait colouring, the product $\prod_v \epsilon_{\ell(e_1), \ell(e_2), \ell(e_3)} = +1$

This follows because a planar graph is 2-cell embedded in $S^2$, and each face gives a consistent orientation constraint. The global consistency of orientations in a planar embedding guarantees all sign products are $+1$.

For $K_{3,3}$, planarity fails, so there's no consistent global orientation, and some colourings contribute $-1$.

### Why Intermediate Negativity Doesn't Kill the Approach

The partial contraction analysis uses an arbitrary vertex ordering. The negative intermediate coefficients reflect the fact that:
1. A generic linear vertex ordering of a planar graph is NOT compatible with the planar structure
2. The web basis positivity is about the PLANAR decomposition, not an arbitrary sequential one

**Critical insight:** If we decompose a planar tensor network along a PLANAR SEPARATOR (a Jordan curve cutting the plane into two regions), the Temperley-Lieb algebra guarantees that the inner product is non-negative. But our sequential vertex ordering doesn't respect planar separators.

### Web Basis Positivity: Refined Question

The correct question is not "are all intermediate coefficients non-negative?" but rather:

**"Does the Penrose tensor of a planar graph, decomposed along planar cuts, always have non-negative coefficients in the Kuperberg web basis?"**

Our edge cut experiment (cube) gave negative coefficients, but this was for a RAW tensor decomposition, not in the web basis. Converting to the web basis might absorb the negativity.

---

## Assessment

### What Works
- Signed = Unsigned for planar graphs is a rock-solid structural fact
- The Penrose evaluation is well-behaved computationally
- Non-planarity manifests as sign cancellation (K_{3,3}) or complete absence (Petersen)

### What Doesn't Work
- Naïve intermediate positivity (sequential vertex contraction) fails badly
- Raw edge cut decomposition produces negative coefficients
- The "web basis with non-negative coefficients" hypothesis needs the actual Kuperberg basis, not just the tensor entries

### What Remains to Test
- Implement actual Kuperberg web basis conversion (requires non-crossing matchings)
- Test planar separator decompositions (tree decomposition compatible with planarity)
- Relate to Temperley-Lieb algebra positivity for the D = 3 case

---

## Code

Implementation: `compute/topology/kuperberg_web.py`  
Raw output: `sub_S3/web_basis_raw.txt`

---

## Conclusion

The Kuperberg web basis approach has **mixed evidence:**
- **Positive:** Signed = unsigned for planar graphs confirms the structural foundation is sound
- **Negative:** Intermediate contractions and edge cuts produce negative coefficients, meaning naïve positivity fails
- **Open:** The actual web basis decomposition (non-crossing planar diagrams) has not been implemented — this is where positivity might live

**Feasibility rating:** MEDIUM-LOW for naïve web basis positivity, MEDIUM for refined planar-separator web basis approach.
