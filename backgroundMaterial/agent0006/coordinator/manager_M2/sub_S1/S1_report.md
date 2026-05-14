# M2/S1 Report: Existing Track Mapping to Agent 1221 Analysis

**Agent:** 0006-M2-S1  
**Date:** 18 February 2026  
**Task:** Map each existing ProofNavigator track to Agent 1221's analysis. Identify updates needed per track.  
**Input:** Current `data.js` (7 tracks + foundation), Agent 1221 report, M1 filtered lists

---

## Track-by-Track Analysis

### Foundation: Five Colour Theorem

**Current state:** 5 sub-goals (F1–F5): Colouring basics, Planarity definition, Euler's Formula, Kempe Chains, Five Colour Theorem. All `unstarted`.

**Agent 1221 alignment:** 
- §6 Track A explicitly requires "Begin Lean 4 formalization of planar graph theory and Kempe chain arguments (Five Colour Theorem first, as a warmup)"
- This validates the Foundation as a non-negotiable prerequisite for all tracks
- Agent 1221 adds emphasis on Kempe chain non-crossing property (Strategy 3) which could be formalized as an F4 extension

**Recommended updates:**
1. **Add sub-goal F4b:** "Kempe chain non-crossing in planar graphs" — formalize the Jordan Curve Theorem constraint on Kempe chains for different colour pairs. This is the "central underexploited mathematical structure" per Agent 1221.
2. **Update F5 notes:** Link to Strategy 11 — the Five Colour Theorem's single-swap argument is the base case for the Kempe Swap Game.
3. **Priority:** Elevate Foundation status from `unstarted` to the first item to begin work on.

---

### Track 1: Kempe Swap Game (Strategy 11)

**Current state:** 4 sub-goals (t1-1 to t1-4): Compute 5→4 reducibility for $n \leq 12$, extend to $n \leq 20$, characterize hard 5-colourings, formalize in Lean 4. All `unstarted`.

**Agent 1221 alignment:**
- §6 Track A secondary: "Computationally verify that every proper 5-colouring of every planar triangulation on $\leq 15$ vertices can be reduced to a 4-colouring by Kempe swaps"
- §6 adds: "Study the Kempe reconfiguration graph structure: diameter, connectivity, spectral gap"
- §6 adds: "Develop structural lemmas about colour elimination strategies"
- Strategy 11 rated Medium feasibility — passes threshold

**Recommended updates:**
1. **Add sub-goal t1-5:** "Kempe reconfiguration graph analysis" — compute diameter, connectivity, spectral gap of the reconfiguration graph $\mathcal{R}(G, 4)$ for small planar triangulations.
2. **Add sub-goal t1-6:** "Fisk theory exploration" — study Kempe equivalence classes via $\mathbb{Z}_2$-homology (Fisk 1977). Algebraic tools for understanding the reconfiguration landscape.
3. **Update t1-1 description:** Align with §6 target of $n \leq 15$ as primary milestone.
4. **Add notes:** Reference Strategy 3 (topological non-crossing) as providing structural constraints that limit the Kempe swap game's complexity.
5. **Add cross-reference:** Feeds into Track 4 (TQFT) via Kempe-like structure in state sums.

---

### Track 2: Chromatic Polynomial (Strategy 1)

**Current state:** 4 sub-goals (t2-1 to t2-4): Formalize $P(G,k)$ in Lean 4, compute roots for $n \leq 20$, prove $P(G,4) > 0$ for outerplanar, extend to series-parallel. All `unstarted`.

**Agent 1221 alignment:**
- Strategy 1 rated Medium-Low → **does not pass threshold**
- NOT explicitly in §6 as a standalone track
- However, chromatic polynomial computation is a key tool for Track 7 (Computational Discovery) and tensor network contraction (Area 6)
- Birkhoff-Lewis gap (80 years), Sokal density, Beraha accumulation — fundamental barriers noted

**Recommended updates:**
1. **Downgrade priority:** Mark as lower priority than Tracks 1, 4, 5, 6, 7 and new tracks.
2. **Retain track:** The Lean 4 formalization of $P(G,k)$ (t2-1) is infrastructure shared by multiple tracks. The root computation (t2-2) feeds Track 7.
3. **Add note:** "Below M1 viability threshold (Medium-Low). Retained for infrastructure value and cross-track synergies."
4. **Update approach text:** Add Agent 1221's risk assessment — Beraha accumulation at 4 and Sokal density result are fundamental barriers that may make the root-bounding approach impossible.

---

### Track 3: Nowhere-Zero Flows (Strategy 2)

**Current state:** 3 sub-goals (t3-1 to t3-3): Formalize nowhere-zero $k$-flows, prove Tutte duality, prove 6-flow theorem. All `unstarted`.

**Agent 1221 alignment:**
- Strategy 2 rated Medium-Low → **does not pass threshold**
- NOT explicitly in §6 as a standalone track
- However, the flow formulation connects to algebraic topology (Track 4) and matroid theory
- The 6-flow theorem formalization (t3-3) would be a significant Mathlib contribution regardless

**Recommended updates:**
1. **Downgrade priority:** Same as Track 2.
2. **Retain track:** The Tutte duality formalization (t3-2) is infrastructure for understanding the TQFT connection. The 6-flow theorem would be a community contribution.
3. **Add note:** "Below M1 viability threshold (Medium-Low). Retained for infrastructure and Mathlib contribution value."
4. **Consider:** Merge t3-1 and t3-2 into Foundation (formal infrastructure) rather than keeping as a standalone track pursuing 4-flows.

---

### Track 4: TQFT / Penrose Evaluation (Area 12)

**Current state:** 4 sub-goals (t4-1 to t4-4): Implement Penrose evaluation, verify nonzero for $n \leq 30$, study 6j-symbol sign conditions, identify positivity mechanism. All `unstarted`.

**Agent 1221 alignment:**
- Area 12 rated Promising (Tier 1) — passes threshold strongly
- §6 Track B primary: "Study the Penrose evaluation of planar cubic graphs as a specialization of the SO(3) Turaev-Viro state sum"
- §6 Track B adds: "Investigate whether unitarity of the underlying modular tensor category implies non-vanishing for planar inputs"
- Agent 1221 identifies this as "the most mathematically exciting pathway"

**Recommended updates:**
1. **Elevate priority:** This is a primary Track B item. Should be clearly marked as one of the top-3 research priorities.
2. **Add sub-goal t4-5:** "Kuperberg web basis analysis" — study rank-2 spider for $\mathfrak{sl}_3$ and its positivity properties for planar webs.
3. **Add sub-goal t4-6:** "Connect to chromatic homology" — categorified Penrose evaluation via Area 19 (category theory). Explore whether chromatic homology's Euler characteristic at $k=4$ for planar graphs reveals structural positivity.
4. **Add cross-references:** Link to Track 6 (sheaf cohomology provides complementary categorical tools), Area 11 (tensor networks compute the same state sum), Strategy 3 (topological Kempe chains encoded in state sums).
5. **Update approach:** Add Agent 1221's specific language about the Kauffman reformulation being "rigorous and published."

---

### Track 5: Spectral / Colin de Verdière (Strategy 6)

**Current state:** 2 sub-goals (t5-1, t5-2): Compute $\mu(G)$ via SDP, formalize in Lean 4. All `unstarted`.

**Agent 1221 alignment:**
- Strategy 6 rated Low-Medium — passes via §6 (Track C primary)
- $\chi(G) \leq \mu(G) + 1$ conjecture is "one of the most important open problems"
- Long-term investment with Very High elegance
- Connects to Hadwiger (Strategy 9) via van der Holst-Laurent-Schrijver

**Recommended updates:**
1. **Add sub-goal t5-3:** "Survey Colin de Verdière conjecture status" — identify specific obstacles, collect known partial results.
2. **Add sub-goal t5-4:** "Investigate signless/normalized Laplacian bounds" — Agent 1221 suggests weaker spectral bounds sharpened for planar graphs.
3. **Add cross-reference:** Link to Strategy 9 (Hadwiger) — $\mu(G) \leq k-1$ iff no $K_k$ minor (proved for $k \leq 5$).
4. **Update notes:** Align with §6 Track C primary.

---

### Track 6: Sheaf Cohomology (Area 19)

**Current state:** 2 sub-goals (t6-1, t6-2): Compute sheaf cohomology for small graphs, formalize cellular sheaves in Lean 4. All `unstarted`.

**Agent 1221 alignment:**
- Area 19 rated Plausible (Tier 2) — passes threshold
- §6 Track B secondary: "Develop a sheaf-theoretic formulation: define $\mathcal{F}_4$ such that $\Gamma(G, \mathcal{F}_4) \neq 0$ iff $G$ is 4-colourable. Investigate whether planarity implies $H^1 = 0$."
- §6 also mentions chromatic homology categorification — this is a separate aspect of Area 19

**Recommended updates:**
1. **Add sub-goal t6-3:** "Chromatic homology" — categorify $P(G,k)$ into bigraded homology $H^{i,j}(G)$. Study whether concentration in even degrees for planar graphs at $k=4$ implies $P(G,4) > 0$.
2. **Add sub-goal t6-4:** "Functorial invariants" — study chromatic polynomial as valuative invariant; connect deletion-contraction to categorical structure.
3. **Add cross-reference:** Link to Track 4 (TQFT shares categorical tools), Area 20 (formalization platform).
4. **Rename consideration:** "Sheaf Cohomology & Categorical Methods" to better reflect expanded scope.

---

### Track 7: Computational Discovery (Areas 6, 1, 10)

**Current state:** 4 sub-goals (t7-1 to t7-4): Build chromatic polynomial database via tensor networks, chromatic root atlas, train GDL model, analyze learned features. All `unstarted`.

**Agent 1221 alignment:**
- Areas 6 (Plausible), 1 (Speculative, but in §6), 10 (Promising) — all pass threshold
- §6 Track C secondary: "Implement planar tensor network contraction for $P(G,k)$, train GDL architectures, formalize patterns in DP-colouring framework"
- Agent 1221 identifies this as "the most actionable cross-domain programme"

**Recommended updates:**
1. **Add sub-goal t7-5:** "DP-colouring formalization" — formalize discovered patterns in the Dvořák-Postle framework (Area 10). Bridge from computational discovery to rigorous proof.
2. **Add sub-goal t7-6:** "Fractional chromatic number LP" — compute $\chi_f(G)$ for planar graph families via LP relaxation of clique hypergraph colouring. Can we prove $\chi_f \leq 4$ independently of 4CT?
3. **Add sub-goal t7-7:** "Quantum chromatic number computation" — compute $\chi_q(G)$ for small planar graphs (Area 11). Compare with classical $\chi$.
4. **Update t7-1 description:** Emphasize tensor networks as primary computational engine, not just one technique among many.
5. **Update approach:** Reference the Areas 6→1→10 pipeline explicitly.

---

## Summary of Recommended Changes

### Structural Changes
1. **Add 3-4 new tracks** for passing items not currently represented (Strategy 4, Strategy 5, Strategy 9, and optionally a Formal Methods / ATP track)
2. **Downgrade Tracks 2 and 3** (Chromatic Polynomial, Flows) — add notes about below-threshold status, reduce visual priority
3. **Expand Foundation** with Kempe non-crossing sub-goal (F4b)
4. **Expand existing tracks** with new sub-goals derived from Agent 1221's concrete next steps

### Content Updates per Track
| Track | New Sub-goals | Priority Change | Cross-References |
|-------|---------------|-----------------|------------------|
| Foundation | F4b (non-crossing) | Elevate to first-to-start | Strategy 3, Strategy 11 |
| Track 1 | t1-5 (reconfiguration graph), t1-6 (Fisk theory) | Maintain | Strategy 3, Track 4 |
| Track 2 | — | **Downgrade** | Track 7 (infrastructure) |
| Track 3 | — | **Downgrade** | Foundation (merge candidates) |
| Track 4 | t4-5 (Kuperberg), t4-6 (chromatic homology link) | **Elevate** | Track 6, Area 11 |
| Track 5 | t5-3 (survey), t5-4 (Laplacian variants) | Maintain | Strategy 9 |
| Track 6 | t6-3 (chromatic homology), t6-4 (functorial) | Maintain | Track 4 |
| Track 7 | t7-5 (DP-colouring), t7-6 (fractional $\chi$), t7-7 ($\chi_q$) | Maintain | All tracks |

---

*Agent 0006-M2-S1 — 18 February 2026*
