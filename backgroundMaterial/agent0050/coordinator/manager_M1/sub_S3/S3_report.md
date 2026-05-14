# Sub-subagent 0050-M1-S3 Report

**Agent:** 0050-M1-S3
**Task:** Non-Crossing Verifier + Fisk Homology
**Manager:** 0050-M1
**Status:** Complete

---

## Work Product

### 1. Non-Crossing Verifier (`noncrossing_verifier.py`)

Verifies the non-interleaving property (Theorem A) at vertices external to the chains. The key insight: the local cyclic-order check is valid ONLY at vertices not in either bichromatic subgraph. For 5-colourings, vertices coloured 5 satisfy this condition.

**Results:**

| Graph | 5-colourings with colour 5 | Vertices checked | Violations |
|-------|---------------------------|-----------------|------------|
| $K_4$ | 96 | 96 | 0 |
| Bipyramid | 216 | 240 | 0 |
| $T_{6,0}$ | 456 | 576 | 0 |
| Octahedron | 684 | 936 | 0 |
| **Total** | **1,452** | **1,848** | **0** |

**Non-crossing property confirmed at all 1,848 tested vertices.** Consistent with Theorem A.

### 2. Fisk Homology (`fisk_homology.py`)

Computes the equivalence classes of 4-colourings under single Kempe chain swaps (Fisk group).

**Results:**

| Graph | 4-colourings | Fisk classes | Structure |
|-------|-------------|-------------|-----------|
| $K_4$ | 24 | 1 | Trivial ($\mathbb{Z}_2^0$) |
| Bipyramid | 24 | 1 | Trivial |
| $T_{6,0}$ | 24 | 1 | Trivial |
| Octahedron | 96 | 1 | Trivial |

**All 4-colourings are Kempe-equivalent** for all tested sphere triangulations. Confirms Fisk (1977) for genus 0.

### Important Methodological Note

Initial implementation attempted to verify non-crossing at ALL vertices for 4-colourings. This produced false positives because: at a vertex $v$ coloured $a$, the $(a,b)$-chains include $v$, and the chain "passes through" the center of $v$'s neighbourhood. This doesn't create a topological barrier, so the local interleaving check gives spurious violations.

**Fix:** Only check at vertices whose colour is NOT in any chain pair — i.e., vertices coloured 5 in a 5-colouring. This correctly implements the Theorem A scenario.

## Files

| File | Description |
|------|-------------|
| `noncrossing_verifier.py` | Non-crossing verification with chain classification |
| `fisk_homology.py` | Fisk group computation via union-find |
| `S3_report.md` | This report |

## Acceptance Criteria Check

- [x] `test_disjoint_chains_noncrossing` — PASS: 1,848 vertex checks, 0 violations
- [x] `test_fisk_group` — PASS: all triangulations have 1 Fisk class (consistent with $\mathbb{Z}_2^0$ for sphere)

## Challenge to M2

1. **Theorem A is confirmed** for $n \leq 6$. M2's proof must hold for ALL $n$.
2. **The local check methodology**: M2 should note that non-crossing is only checkable at external vertices. This has implications for how Theorem A should be stated.
3. **Fisk single-class**: all 4-colourings are equivalent, confirming $\mathcal{R}(T,4)$ connectivity. But this relies on 4CT being true (the colourings exist). Can M2 prove connectivity WITHOUT assuming 4CT?

## Self-Assessment

**Craftsperson says:** The verifier correctly implements Theorem A's scenario, and the Fisk computation is clean. The methodological correction (external-only checks) is an important insight.

**Skeptic says:** The false positive incident revealed a subtlety that M2 should address in their proof: the non-crossing property at a vertex is meaningful only for external vertices. Also, we haven't tested $n \geq 7$.

**Mover says:** Both tools work, tests pass, and the data supports Plan 2. The false positive was caught and fixed. Shipping with confidence.

---

*0050-M1-S3 — 18 February 2026*
