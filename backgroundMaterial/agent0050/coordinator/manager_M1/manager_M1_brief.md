# Task Brief — Manager 0050-M1 ("The Engineers")

**From:** Coordinator 0050-C
**To:** Manager 0050-M1
**Date:** 18 February 2026

---

## Mission

You lead the **Computational Verification Team** ("The Engineers") for Plan 2: Kempe Swap Game + Topological Non-Crossing. Your mission: **build the evidence base, find hard cases, and try to break the theorists' (M2) claims.**

You are in **direct competition** with Manager 0050-M2 ("The Mathematicians"). They are trying to prove general theorems. You are trying to find cases where those theorems fail, or where the approach hits walls. Whoever produces more impactful, tested results wins.

## Mathematical Context

**Plan 2 Core Question:** Starting from any proper 5-colouring of a planar graph (guaranteed by 5CT), can a sequence of Kempe chain swaps always eliminate one colour? If yes → constructive proof of 4CT.

Key objects:
- **Kempe chains**: maximal bichromatic connected subgraphs
- **Kempe swap**: swap colours $a \leftrightarrow b$ on a Kempe chain; preserves proper colouring
- **Non-crossing property**: in planar graphs, Kempe chains for disjoint colour pairs $\{a,b\}$ and $\{c,d\}$ cannot cross (Jordan Curve Theorem)
- **Reconfiguration graph** $\mathcal{R}(G,k)$: nodes = proper $k$-colourings, edges = single Kempe swaps
- $\mathcal{R}(G,5)$ is always connected for planar $G$ (Las Vergnas-Meyniel 1981)
- $\mathcal{R}(G,4)$ connectivity is OPEN — equivalent to 4CT
- Fisk (1977): 4-colourings mod Kempe swaps form group $\cong \mathbb{Z}_2^g$

## Your Team — 3 Sub-workers

You must spawn exactly 3 sub-workers as Task subagents. They compete with each other for quality. Launch S1 first (others depend on its infrastructure), then S2 and S3 in parallel.

### M1-S1: Triangulation Database + 5→4 Reduction Search

**Task:** Build Python modules to generate all planar triangulations up to $n$ vertices. For small $n$ ($\leq 8$ realistically), enumerate ALL proper 5-colourings. BFS the Kempe reconfiguration graph from each 5-colouring to find paths to 4-colourings.

**Deliverables:**
1. `triangulation_db.py` — generate planar triangulations (up to isomorphism) as networkx graphs with planar embeddings
2. `kempe_ops.py` — Kempe chain extraction, Kempe swap execution, proper colouring verification
3. `reduction_search.py` — BFS/DFS through Kempe swap sequences to find 5→4 recolouring paths
4. `S1_report.md` — results report

**Acceptance Criteria (TESTS — each must be a function in the code):**
- `test_triangle_is_3colorable`: $K_3$ has chromatic number 3
- `test_K4_is_4colorable`: $K_4$ needs exactly 4 colours
- `test_5col_to_4col_K4`: Every 5-colouring of $K_4$ can be Kempe-reduced to a 4-colouring
- `test_5col_to_4col_octahedron`: Same for the octahedron (6 vertices)
- `test_kempe_swap_preserves_coloring`: After any Kempe swap, the colouring is still proper

**Output Location:** `/Users/kylemathewson/GraphColour/backgroundMaterial/agent0050/coordinator/manager_M1/sub_S1/`
Also copy final Python files to: `/Users/kylemathewson/GraphColour/compute/kempe/`

### M1-S2: Reconfiguration Graph Analyzer

**Task:** Build $\mathcal{R}(T, k)$ for small triangulations: nodes = proper $k$-colourings, edges = single Kempe swaps. Compute structural properties.

**Deliverables:**
1. `reconfiguration_graph.py` — build R(T,k), compute diameter, connected components, basic statistics
2. `S2_report.md` — results for all tested triangulations

**Acceptance Criteria (TESTS):**
- `test_R5_connected`: $\mathcal{R}(T, 5)$ is connected for all $T$ on $n \leq 8$
- `test_R4_components`: Count connected components of $\mathcal{R}(T, 4)$ for all tested $T$
- `test_diameter_finite`: Diameter is finite for all tested cases

**Output Location:** `/Users/kylemathewson/GraphColour/backgroundMaterial/agent0050/coordinator/manager_M1/sub_S2/`
Also copy final Python files to: `/Users/kylemathewson/GraphColour/compute/kempe/`

**Dependency:** Uses `kempe_ops.py` and `triangulation_db.py` from S1.

### M1-S3: Non-Crossing Verifier + Fisk Homology

**Task:** For each proper 4-colouring of each small triangulation: verify that Kempe chains for disjoint colour pairs never cross in the planar embedding. Compute the Fisk group structure.

**Deliverables:**
1. `noncrossing_verifier.py` — verify non-crossing property using planar embeddings
2. `fisk_homology.py` — compute Fisk group (quotient of 4-colourings by Kempe swaps)
3. `S3_report.md` — results

**Acceptance Criteria (TESTS):**
- `test_disjoint_chains_noncrossing`: Verify for all 4-colourings of $T$ on $n \leq 8$
- `test_fisk_group_is_Z2`: Fisk group has $\mathbb{Z}_2^g$ structure for tested $T$ (for the sphere, $g=0$, so the group should be trivial)

**Output Location:** `/Users/kylemathewson/GraphColour/backgroundMaterial/agent0050/coordinator/manager_M1/sub_S3/`
Also copy final Python files to: `/Users/kylemathewson/GraphColour/compute/kempe/`

**Dependency:** Uses `kempe_ops.py` and `triangulation_db.py` from S1.

## Technical Constraints

- **Python virtual environment**: Use `python3 -m venv .venv && source .venv/bin/activate` at the project root (`/Users/kylemathewson/GraphColour/`)
- **Allowed dependencies**: standard library + `networkx` + `numpy` + `itertools` (install networkx and numpy via pip if needed)
- **Type hints and docstrings** on all functions
- **All tests must actually run and pass** — not just be defined

## Report Format

Write `manager_M1_report.md` in your folder (`/Users/kylemathewson/GraphColour/backgroundMaterial/agent0050/coordinator/manager_M1/`) following this structure:

```
# Manager 0050-M1 Report

**Agent:** 0050-M1
**Stream:** parallel — Computational Verification ("The Engineers")
**Coordinator:** 0050-C
**Status:** [Complete / In Progress / Blocked]

## Stream Summary
## Sub-subagent Status (table)
## Collected Outputs
## Integration Notes
## Competition Results (what we found that challenges M2)
## Issues Encountered
## Self-Assessment (Craftsperson/Skeptic/Mover)
```

## Competition Framing

Your team COMPETES against M2 ("The Mathematicians"). Specifically:
- If M2 claims Theorem A (non-interleaving), your S3's data must either **confirm or refute** it
- If M2 claims all degree-5 cases are resolvable, your S1 must **test this on real graphs**
- If M2 claims the Colour Elimination Lemma holds, your S1's BFS data must **show whether the ordering strategy actually works**
- **Hard cases you find** that M2 cannot explain are your strongest weapon

---

*Coordinator 0050-C — 18 February 2026*
