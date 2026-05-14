# M2/S2 Report: Integration Plan — New data.js Nodes

**Agent:** 0006-M2-S2  
**Date:** 18 February 2026  
**Task:** Design new `data.js` nodes for items passing threshold. Write the complete integration plan for the ProofNavigator web application.  
**Input:** M1 filtered lists, M2/S1 track mapping, current `data.js` structure

---

## Integration Plan Overview

The ProofNavigator currently has 7 tracks + Foundation. After applying the viability threshold, we need to:

1. **Add 4 new tracks** (Tracks 8–11) for major passing items not currently represented
2. **Update 5 existing tracks** with new sub-goals from Agent 1221's analysis
3. **Add 1 new Foundation sub-goal** (F4b)
4. **Downgrade 2 existing tracks** (Tracks 2, 3) in priority status
5. **Update root node** metadata to reflect 11-track structure

### Final Track Structure

| Track | Name | Source | §6 Alignment | Priority |
|-------|------|--------|--------------|----------|
| Foundation | Five Colour Theorem | Infrastructure | Prerequisite | **Critical** |
| Track 1 | Kempe Swap Game | Strategy 11 | Track A secondary | **High** |
| Track 2 | Chromatic Polynomial | Strategy 1 | — (below threshold) | **Low** |
| Track 3 | Nowhere-Zero Flows | Strategy 2 | — (below threshold) | **Low** |
| Track 4 | TQFT / Penrose | Area 12 | Track B primary | **High** |
| Track 5 | Spectral / Colin de Verdière | Strategy 6 | Track C primary | Medium |
| Track 6 | Sheaf Cohomology & Categorical Methods | Area 19 | Track B secondary | Medium |
| Track 7 | Computational Discovery | Areas 6, 1, 10 | Track C secondary | **High** |
| **Track 8** | **Refined Discharging** | **Strategy 4** | **Track A primary** | **Critical** |
| **Track 9** | **Proof Mining** | **Strategy 5** | **Track A support** | **High** |
| **Track 10** | **Hadwiger Conjecture** | **Strategy 9** | **Track C primary** | Medium |
| **Track 11** | **Formal Methods & ATP** | **Area 20 + Area 16** | **Track A infrastructure** | **High** |

---

## New data.js Nodes

### Track 8: Refined Discharging (Strategy 4)

```javascript
{
  id: "track8",
  title: "Track 8: Refined Discharging",
  statement: "Find discharging rules that shrink the unavoidable set from 633 to ≤50 human-checkable configurations.",
  status: "unstarted",
  approach: "RSST used 32 rules / 633 configs. Modern SAT/SMT can systematically search for optimal rules. No lower bound on N is known. If N < 50, each reducibility check fits on one page — yielding a mostly deductive proof. Agent 1221's highest-feasibility strategy.",
  killCriteria: "Proven lower bound N ≥ 200 for any discharging-based proof. OR SAT search finds no improvement over 633 after 3 months of compute.",
  files: [],
  notes: [
    { time: "2026-02-18T00:00:00Z", text: "Created from Agent 1221 Strategy 4. §6 Track A primary." }
  ],
  evidence: "",
  expanded: false,
  children: [
    {
      id: "t8-1",
      title: "Build flexible discharging framework",
      statement: "Software system: input discharging rules → compute unavoidable set → test each config for reducibility.",
      status: "unstarted",
      approach: "Python prototype, then Rust for performance. Decouple from RSST's specific rules.",
      killCriteria: "",
      files: ["compute/discharging/framework.py"],
      notes: [],
      evidence: "",
      expanded: false,
      children: []
    },
    {
      id: "t8-2",
      title: "SAT/SMT search for optimal rules",
      statement: "Encode discharging as CSP: given target N, find rules making exactly N configs unavoidable, all reducible.",
      status: "unstarted",
      approach: "CaDiCaL or Kissat SAT solver. Start with N=500, binary search downward.",
      killCriteria: "No improvement over 633 after 4 weeks",
      files: ["compute/discharging/sat_search.py"],
      notes: [],
      evidence: "",
      expanded: false,
      children: []
    },
    {
      id: "t8-3",
      title: "Study theoretical minimum N",
      statement: "Is there an information-theoretic or structural lower bound on unavoidable set size?",
      status: "unstarted",
      approach: "Literature survey + attempted proofs. Does every unavoidable set need ring size ≥ r for some r > 6?",
      killCriteria: "Proven lower bound N ≥ 200",
      files: [],
      notes: [],
      evidence: "",
      expanded: false,
      children: []
    },
    {
      id: "t8-4",
      title: "Human-friendly reducibility proofs",
      statement: "For each config in the reduced unavoidable set, write simplest possible Kempe chain argument.",
      status: "unstarted",
      approach: "Target: each argument fits on 1 page. Uses Kempe non-crossing (Strategy 3) to simplify.",
      killCriteria: "Any config requires > 10 pages",
      files: [],
      notes: [],
      evidence: "",
      expanded: false,
      children: []
    }
  ]
}
```

### Track 9: Proof Mining (Strategy 5)

```javascript
{
  id: "track9",
  title: "Track 9: Proof Mining",
  statement: "Extract structure from Gonthier's 60,000-line Coq proof. Collapse 633 reducibility checks into parameterized lemma families.",
  status: "unstarted",
  approach: "The 633 reducibility checks may cluster into a small number of parameterized templates. If 500 of 633 are 'essentially the same', collapsing them yields a much smaller effective proof. Complementary to Track 8 (fewer configs to mine). Agent 1221 Strategy 5.",
  killCriteria: "The 633 configurations are genuinely irreducibly diverse — each requires a qualitatively different argument. OR Coq proof cannot be compiled with modern tooling after 4 weeks of effort.",
  files: [],
  notes: [
    { time: "2026-02-18T00:00:00Z", text: "Created from Agent 1221 Strategy 5. §6 Track A support." }
  ],
  evidence: "",
  expanded: false,
  children: [
    {
      id: "t9-1",
      title: "Compile Gonthier's Coq proof",
      statement: "Obtain, compile, and understand the structure of the ~60,000 line proof.",
      status: "unstarted",
      approach: "Mathematical Components library maintains a version. May need porting to modern Coq.",
      killCriteria: "Cannot compile after 4 weeks",
      files: [],
      notes: [],
      evidence: "",
      expanded: false,
      children: []
    },
    {
      id: "t9-2",
      title: "Instrument reducibility checker",
      statement: "Modify Coq code to trace each check: which Kempe chains swapped, in what order, which boundary colourings are hard.",
      status: "unstarted",
      approach: "Add logging to the reducibility decision procedure.",
      killCriteria: "",
      files: [],
      notes: [],
      evidence: "",
      expanded: false,
      children: []
    },
    {
      id: "t9-3",
      title: "Cluster the 633 configurations",
      statement: "Apply clustering (k-means on trace features, graph similarity) to identify families of 'similar' configurations.",
      status: "unstarted",
      approach: "Python data science pipeline on instrumented traces.",
      killCriteria: "No meaningful clusters (all configs equally dissimilar)",
      files: ["compute/proofmining/cluster_configs.py"],
      notes: [],
      evidence: "",
      expanded: false,
      children: []
    },
    {
      id: "t9-4",
      title: "Write parameterized lemmas",
      statement: "For each cluster, write a single parameterized lemma covering all configs in the cluster.",
      status: "unstarted",
      approach: "Coq first (verify correctness), then translate to Lean 4.",
      killCriteria: "Largest cluster has < 10 configs (too fine-grained to help)",
      files: [],
      notes: [],
      evidence: "",
      expanded: false,
      children: []
    },
    {
      id: "t9-5",
      title: "LLM-assisted proof compression",
      statement: "Use LLMs to identify generalizations across reducibility arguments.",
      status: "unstarted",
      approach: "Fine-tune on the 4CT Coq proof corpus. Ask model to suggest unified arguments.",
      killCriteria: "LLM hallucinations outweigh useful suggestions",
      files: [],
      notes: [],
      evidence: "",
      expanded: false,
      children: []
    }
  ]
}
```

### Track 10: Hadwiger Conjecture (Strategy 9)

```javascript
{
  id: "track10",
  title: "Track 10: Hadwiger Conjecture (k=5)",
  statement: "Prove Hadwiger for k=5 without using 4CT: every K5-minor-free graph is 4-colourable.",
  status: "unstarted",
  approach: "RST (1993) proved this USING 4CT. A 4CT-independent proof yields 4CT as corollary via a completely different route. Need to understand why K5-minor-free graphs decompose into 4-colourable pieces. Agent 1221 Strategy 9, §6 Track C primary.",
  killCriteria: "Proof shown to inherently require 4CT-strength result (circularity). OR RST proof analysis reveals no avoidable 4CT invocation after 3 months.",
  files: [],
  notes: [
    { time: "2026-02-18T00:00:00Z", text: "Created from Agent 1221 Strategy 9. §6 Track C primary. Very High elegance." }
  ],
  evidence: "",
  expanded: false,
  children: [
    {
      id: "t10-1",
      title: "Detailed study of RST proof",
      statement: "Read Robertson-Seymour-Thomas (1993) proof of Hadwiger k=5. Identify precisely where 4CT is invoked.",
      status: "unstarted",
      approach: "Paper math. Annotated reading of the original paper.",
      killCriteria: "",
      files: [],
      notes: [],
      evidence: "",
      expanded: false,
      children: []
    },
    {
      id: "t10-2",
      title: "Attempt 5CT substitution",
      statement: "Can the proof be restructured to use 5CT instead of 4CT? This gives a weaker but 4CT-independent result.",
      status: "unstarted",
      approach: "Modify the RST argument. See if K5-minor-free → 5-colourable follows without 4CT (known, but via Hadwiger framework).",
      killCriteria: "",
      files: [],
      notes: [],
      evidence: "",
      expanded: false,
      children: []
    },
    {
      id: "t10-3",
      title: "Refine decomposition",
      statement: "Can K5-minor-free decomposition yield pieces with extra structure (bounded treewidth) making 4-colouring easy without 4CT?",
      status: "unstarted",
      approach: "Graph structure theory. Investigate clique-sum decompositions.",
      killCriteria: "Pieces necessarily include arbitrary planar graphs (circularity)",
      files: [],
      notes: [],
      evidence: "",
      expanded: false,
      children: []
    }
  ]
}
```

### Track 11: Formal Methods & ATP (Area 20 + Area 16)

```javascript
{
  id: "track11",
  title: "Track 11: Formal Methods & ATP",
  statement: "Build shared Lean 4 / Mathlib infrastructure for all tracks. Deploy AI-guided proof search. SAT-based reducibility optimization.",
  status: "unstarted",
  approach: "Cross-cutting infrastructure track. Lean 4 formalization of planar graph theory, Kempe chains, discharging, reducibility — used by all other tracks. AI proof search (AlphaProof-style) for novel strategies. SAT solvers for Track 8. HoTT-inspired proof structures (Area 16). Agent 1221 Area 20, §6 Track A infrastructure.",
  killCriteria: "Lean 4 / Mathlib graph theory API insufficient for planar graph work after 6 weeks of effort.",
  files: [],
  notes: [
    { time: "2026-02-18T00:00:00Z", text: "Created from Agent 1221 Areas 20 + 16. Cross-cutting infrastructure." }
  ],
  evidence: "",
  expanded: false,
  children: [
    {
      id: "t11-1",
      title: "Lean 4 planar graph library",
      statement: "Formalize planar embeddings, faces, Euler's formula in Lean 4 using Mathlib.",
      status: "unstarted",
      approach: "Build on Mathlib SimpleGraph. Define PlanarEmbedding, prove Euler V-E+F=2.",
      killCriteria: "",
      files: ["lean4/FourColor/Infrastructure/PlanarGraph.lean"],
      notes: [],
      evidence: "",
      expanded: false,
      children: []
    },
    {
      id: "t11-2",
      title: "Lean 4 Kempe chain library",
      statement: "Formalize Kempe chains, swap validity, non-crossing in planar graphs.",
      status: "unstarted",
      approach: "Shared library used by Foundation (F4, F5), Track 1, Track 8.",
      killCriteria: "",
      files: ["lean4/FourColor/Infrastructure/KempeChain.lean"],
      notes: [],
      evidence: "",
      expanded: false,
      children: []
    },
    {
      id: "t11-3",
      title: "Lean 4 reducibility checker",
      statement: "Formalize D-reducibility testing for graph configurations.",
      status: "unstarted",
      approach: "Port from Gonthier's Coq. Use Lean 4 decision procedures.",
      killCriteria: "",
      files: ["lean4/FourColor/Infrastructure/Reducibility.lean"],
      notes: [],
      evidence: "",
      expanded: false,
      children: []
    },
    {
      id: "t11-4",
      title: "AI-guided proof exploration",
      statement: "Train neural proof search on Mathlib combinatorics. Direct at restricted 4CT cases.",
      status: "unstarted",
      approach: "LeanDojo or ReProver. Start with outerplanar, series-parallel, bounded treewidth.",
      killCriteria: "AI finds no novel proof strategies after 2 months",
      files: [],
      notes: [],
      evidence: "",
      expanded: false,
      children: []
    },
    {
      id: "t11-5",
      title: "HoTT exploration",
      statement: "Investigate HIT-based representation of planar graphs as cell complexes.",
      status: "unstarted",
      approach: "Cubical Agda or Lean 4 HoTT-inspired constructions. Does 2-cell structure enable new inductive arguments?",
      killCriteria: "No proof advantage over classical after 6 weeks",
      files: [],
      notes: [],
      evidence: "",
      expanded: false,
      children: []
    }
  ]
}
```

---

## Updates to Existing Nodes

### Foundation: Add F4b

```javascript
{
  id: "f4b",
  title: "F4b: Kempe Non-Crossing (Planar)",
  statement: "In a planar graph, Kempe chains for non-overlapping colour pairs cannot cross (Jordan Curve Theorem). Formalize this constraint.",
  status: "unstarted",
  approach: "Agent 1221 identifies this as the 'central underexploited mathematical structure.' At degree-5 vertex v, if (a,b)-chain from w1 reaches w3, the (a,c)-chain from w2 is confined to one side.",
  killCriteria: "",
  files: ["lean4/FourColor/Foundation/F4b_KempeNonCrossing.lean"],
  notes: [
    { time: "2026-02-18T00:00:00Z", text: "Added from Agent 1221 Strategy 3 analysis. Cross-cutting: feeds Tracks 1, 4, 8." }
  ],
  evidence: "",
  expanded: false,
  children: []
}
```

### Track 1: Add t1-5 and t1-6

```javascript
{
  id: "t1-5",
  title: "Kempe reconfiguration graph analysis",
  statement: "Compute diameter, connectivity, spectral gap of R(G, 4) for planar triangulations n ≤ 15.",
  status: "unstarted",
  approach: "Build reconfiguration graph. Analyze structure. Does it have bounded diameter?",
  killCriteria: "Disconnected R(G,4) found (some 4-colourings not Kempe-equivalent)",
  files: ["compute/kempe/reconfiguration_graph.py"],
  notes: [],
  evidence: "",
  expanded: false,
  children: []
}
```

```javascript
{
  id: "t1-6",
  title: "Fisk theory of Kempe equivalence",
  statement: "Study Kempe equivalence classes via Z2-homology (Fisk 1977).",
  status: "unstarted",
  approach: "The algebraic structure of Kempe classes may constrain the reconfiguration landscape.",
  killCriteria: "",
  files: [],
  notes: [],
  evidence: "",
  expanded: false,
  children: []
}
```

### Track 4: Add t4-5 and t4-6

```javascript
{
  id: "t4-5",
  title: "Kuperberg web basis analysis",
  statement: "Study rank-2 spider for sl_3 and positivity properties for planar webs.",
  status: "unstarted",
  approach: "The Kuperberg basis provides explicit tools for the space of invariant tensors. Positivity here may imply Penrose non-vanishing.",
  killCriteria: "No positivity property for planar webs",
  files: [],
  notes: [],
  evidence: "",
  expanded: false,
  children: []
}
```

```javascript
{
  id: "t4-6",
  title: "Connect to chromatic homology (Area 19)",
  statement: "Categorified Penrose evaluation. Does chromatic homology at k=4 for planar graphs show structural positivity?",
  status: "unstarted",
  approach: "Bridge Track 4 (TQFT) and Track 6 (sheaf cohomology) via categorification.",
  killCriteria: "",
  files: [],
  notes: [],
  evidence: "",
  expanded: false,
  children: []
}
```

### Track 5: Add t5-3 and t5-4

```javascript
{
  id: "t5-3",
  title: "Survey Colin de Verdière conjecture",
  statement: "Catalogue known partial results and specific obstacles to χ ≤ μ+1.",
  status: "unstarted",
  approach: "Literature survey. Identify what's known for specific graph classes.",
  killCriteria: "",
  files: [],
  notes: [],
  evidence: "",
  expanded: false,
  children: []
}
```

```javascript
{
  id: "t5-4",
  title: "Alternate Laplacian bounds",
  statement: "Investigate signless and normalized Laplacian spectral bounds for planar graphs.",
  status: "unstarted",
  approach: "Can weaker spectral bounds be sharpened specifically for planar graphs?",
  killCriteria: "No improvement over existing bounds after 4 weeks",
  files: [],
  notes: [],
  evidence: "",
  expanded: false,
  children: []
}
```

### Track 6: Add t6-3 and t6-4

```javascript
{
  id: "t6-3",
  title: "Chromatic homology",
  statement: "Categorify P(G,k) into bigraded homology H^{i,j}(G). Study positivity for planar graphs at k=4.",
  status: "unstarted",
  approach: "Helme-Guizon and Rong (2005). Graded Euler characteristic recovers P(G,k). If concentrated in even degrees → P(G,4) > 0.",
  killCriteria: "Odd-degree terms dominate for some planar family",
  files: ["compute/topology/chromatic_homology.py"],
  notes: [],
  evidence: "",
  expanded: false,
  children: []
}
```

```javascript
{
  id: "t6-4",
  title: "Functorial colouring invariants",
  statement: "Study P(G,k) as valuative invariant. Connect deletion-contraction to categorical structure.",
  status: "unstarted",
  approach: "Category theory framework for graph homomorphisms and colouring.",
  killCriteria: "",
  files: [],
  notes: [],
  evidence: "",
  expanded: false,
  children: []
}
```

### Track 7: Add t7-5, t7-6, t7-7

```javascript
{
  id: "t7-5",
  title: "DP-colouring formalization",
  statement: "Formalize discovered computational patterns in the Dvořák-Postle DP-colouring framework.",
  status: "unstarted",
  approach: "Bridge from pattern discovery to rigorous proof. Area 10 (Hypergraph Theory).",
  killCriteria: "Patterns don't survive formalization",
  files: [],
  notes: [],
  evidence: "",
  expanded: false,
  children: []
}
```

```javascript
{
  id: "t7-6",
  title: "Fractional chromatic number LP",
  statement: "Compute χ_f(G) for planar graph families. Can we prove χ_f ≤ 4 independently of 4CT?",
  status: "unstarted",
  approach: "LP relaxation of clique hypergraph colouring. Explicit dual formulation for planar triangulations.",
  killCriteria: "",
  files: ["compute/discovery/fractional_chi.py"],
  notes: [],
  evidence: "",
  expanded: false,
  children: []
}
```

```javascript
{
  id: "t7-7",
  title: "Quantum chromatic number",
  statement: "Compute χ_q(G) for small planar graphs. Compare with classical χ.",
  status: "unstarted",
  approach: "Area 11 (Quantum Information). Operator system methods.",
  killCriteria: "",
  files: ["compute/discovery/quantum_chi.py"],
  notes: [],
  evidence: "",
  expanded: false,
  children: []
}
```

### Root Node Update

Update the root node's `approach` field:
```javascript
approach: "Novel proof exploration via 11 parallel tracks (4 new from Agent 1221 analysis). Organized by Agent 1221's three-track research programme: Track A (near-term: discharging, proof mining, Kempe swap, ATP), Track B (medium-term: TQFT, sheaf cohomology), Track C (long-term: Hadwiger, spectral, computational discovery). We seek a new deductive proof — not a reproduction of the Appel-Haken/RSST computer-assisted proof."
```

---

## Integration Priority Order

For implementation in `data.js`:

1. **Track 8 (Refined Discharging)** — new, Critical priority
2. **Track 11 (Formal Methods & ATP)** — new, High priority (infrastructure)
3. **Track 9 (Proof Mining)** — new, High priority
4. **Track 10 (Hadwiger)** — new, Medium priority
5. **Foundation F4b** — new sub-goal
6. **Track 1 updates** — t1-5, t1-6
7. **Track 4 updates** — t4-5, t4-6
8. **Track 5 updates** — t5-3, t5-4
9. **Track 6 updates** — t6-3, t6-4
10. **Track 7 updates** — t7-5, t7-6, t7-7
11. **Tracks 2 & 3 notes** — add below-threshold annotation

---

## Discrete Geometry (Area 18) Integration Note

Area 18 passes threshold (Plausible) but does not warrant a full dedicated track. Its key contribution — circle packing as canonical geometric embedding — is best integrated as:
- A sub-goal under Track 1 (Kempe chains in circle-packed graphs) or
- A sub-goal under Foundation (geometric representation of planarity)

Recommend adding a note to Track 1 or Foundation referencing circle packing, rather than creating Track 12.

---

*Agent 0006-M2-S2 — 18 February 2026*
