/* Default proof tree data — initialized from 4CT project structure.
   This is loaded once on first visit; after that, localStorage is the source of truth.
   To reset, click the reset button in the header. */

const DEFAULT_TREE = {
  id: "4ct",
  title: "Four Colour Theorem",
  statement: "\u2200 planar G, \u03C7(G) \u2264 4",
  status: "exploring",
  approach: "Novel proof exploration via 7 parallel tracks. We seek a new deductive proof — not a reproduction of the Appel-Haken/RSST computer-assisted proof.",
  killCriteria: "",
  files: ["SolvingFrameworkPlan/docs/working/NovelProofExploration.md", "backgroundMaterial/agent1221/agent1221Report.md"],
  notes: [
    { time: "2026-02-17T12:00:00Z", text: "Project created. Agent 1221 report complete." },
    { time: "2026-02-17T13:00:00Z", text: "Strategy: Pipeline D only — novel proof or nothing." }
  ],
  evidence: "",
  expanded: true,
  children: [
    {
      id: "foundation",
      title: "Foundation: Five Colour Theorem",
      statement: "\u2200 planar G, \u03C7(G) \u2264 5",
      status: "unstarted",
      approach: "Prove the 5CT in Lean 4. This validates all infrastructure (planarity, Euler, Kempe chains) and is independently publishable. Non-negotiable prerequisite for all tracks.",
      killCriteria: "",
      files: [],
      notes: [],
      evidence: "",
      expanded: true,
      children: [
        {
          id: "f1",
          title: "F1: Colouring Basics",
          statement: "Use Mathlib SimpleGraph.Coloring API. Verify K4 is 4-colorable.",
          status: "unstarted",
          approach: "Learn the Mathlib API. Write sanity tests. No original math needed.",
          killCriteria: "",
          files: ["lean4/FourColor/Foundation/F1_ColoringBasics.lean"],
          notes: [],
          evidence: "",
          expanded: false,
          children: []
        },
        {
          id: "f2",
          title: "F2: Planarity Definition",
          statement: "Define IsPlanar via Kuratowski-Wagner: \u00AC(K5 \u2264m G) \u2227 \u00AC(K33 \u2264m G)",
          status: "unstarted",
          approach: "Option A (fast): define via forbidden minors. Option B (slow): combinatorial planar embedding. Start with A.",
          killCriteria: "Stalls for > 4 weeks. Seek help from Mathlib community.",
          files: ["lean4/FourColor/Foundation/F2_Planarity.lean"], plannedFiles: ["lean4/FourColor/Foundation/F2_Planarity.lean"],
          notes: [],
          evidence: "",
          expanded: false,
          children: []
        },
        {
          id: "f3",
          title: "F3: Euler's Formula",
          statement: "V - E + F = 2 for connected planar graphs. Corollary: E \u2264 3V - 6.",
          status: "unstarted",
          approach: "Prove from planarity definition. Derive: every planar graph has a vertex of degree \u2264 5.",
          killCriteria: "",
          files: ["lean4/FourColor/Foundation/F3_EulerFormula.lean"], plannedFiles: ["lean4/FourColor/Foundation/F3_EulerFormula.lean"],
          notes: [],
          evidence: "",
          expanded: false,
          children: []
        },
        {
          id: "f4",
          title: "F4: Kempe Chains",
          statement: "Kempe swap preserves proper colouring. Deg \u2264 4 case: colouring always extends.",
          status: "unstarted",
          approach: "Define Kempe chains as maximal bichromatic connected subgraphs. Prove swap validity.",
          killCriteria: "",
          files: ["lean4/FourColor/Foundation/F4_KempeChains.lean"],
          notes: [],
          evidence: "",
          expanded: false,
          children: []
        },
        {
          id: "f5",
          title: "F5: Five Colour Theorem",
          statement: "\u2200 (G : SimpleGraph V) [Fintype V], G.IsPlanar \u2192 G.Colorable 5",
          status: "unstarted",
          approach: "Induction on |V|. Remove min-degree vertex. Deg \u2264 4: trivial. Deg = 5: single Kempe swap.",
          killCriteria: "",
          files: ["lean4/FourColor/Foundation/F5_FiveColorTheorem.lean"], plannedFiles: ["lean4/FourColor/Foundation/F5_FiveColorTheorem.lean"],
          notes: [],
          evidence: "",
          expanded: false,
          children: []
        },
        {
          id: "f-spec-lean",
          title: "Spec: Lean Tier-1 obligations",
          statement: "Specify the Lean statements already justified by the Kempe lemmas (swap preserves a proper colouring, Never-Revert, Chain Lifting for colours in {1,2,3,4}), against lean4/KempeReconfiguration. This node records a specification, not a proof.",
          status: "in-progress",
          approach: "Agent 1701 task F2, manager M-Foundation. Specification accepted at the critic gate. Two obligations are closed in Lean source; Chain Lifting's chain-equality theorem is not.",
          killCriteria: "Critic gate rejects the specification as hot air.",
          files: ["backgroundMaterial/agent1701/tasks/F2.md", "backgroundMaterial/agent1701/groups/F2_spec.md", "lean4/KempeReconfiguration/"],
          notes: [{ "time": "2026-09-27T19:45:00Z", "text": "Issued by the main planning team. Not accepted until the critic gate." }, { "time": "2026-09-27T20:30:00Z", "text": "Critic gate accepted the specification. Not a proof of the Five Colour Theorem." }],
          evidence: "Spec accepted 2026-09-27. kempeSwap_preserves_proper (Basic.lean) and never_revert (NeverRevert.lean) are Lean proofs with no sorry tactic; they were not compiled in this wave. ChainLifting.lean proves isolation of colour 5 in the {1,2,3,4} bichromatic subgraph, not equality of chains in G and G-v. No Five Colour Theorem file is in the repo.",
          expanded: false,
          children: []
        }
      ]
    },
    {
      id: "track1",
      title: "Track 1: Kempe Swap Game",
      statement: "Every proper 5-colouring of a planar graph can be Kempe-reduced to a 4-colouring.",
      status: "unstarted",
      approach: "Start with a 5-colouring (guaranteed by 5CT). Show Kempe chain swaps can always eliminate one colour. Computational verification first, then formalize.",
      killCriteria: "A planar graph found where some 5-colouring cannot be Kempe-reduced to 4. OR computation for n=15 takes > 2 weeks.",
      files: [],
      notes: [],
      evidence: "",
      expanded: false,
      children: [
        { id: "t1-1", title: "Compute: 5\u21924 reducibility for n \u2264 12", statement: "Enumerate all 5-colourings of all planar triangulations n\u226412, verify each can be Kempe-reduced to 4.", status: "unstarted", approach: "Python + NetworkX exhaustive search.", killCriteria: "Any counterexample", files: ["compute/kempe/reduction_search.py"], notes: [], evidence: "", expanded: false, children: [] },
        { id: "t1-2", title: "Extend to n \u2264 15, 18, 20", statement: "Same computation, larger graphs.", status: "unstarted", approach: "Parallelized Python. May need HPC.", killCriteria: "Counterexample or runtime > 1 week for n=15", files: [], notes: [], evidence: "", expanded: false, children: [] },
        { id: "t1-3", title: "Characterize hard 5-colourings", statement: "Which 5-colourings require the most swaps to reduce?", status: "unstarted", approach: "Analyze computation data. Look for structural patterns.", killCriteria: "No pattern after n=18 data", files: [], notes: [], evidence: "", expanded: false, children: [] },
        { id: "t1-4", title: "Formalize in Lean 4", statement: "Prove the Kempe reduction property formally.", status: "unstarted", approach: "Depends on pattern found in t1-3.", killCriteria: "Stalls > 4 weeks", files: ["lean4/FourColor/Track1_KempeSwap/"], plannedFiles: ["lean4/FourColor/Track1_KempeSwap/"], notes: [], evidence: "", expanded: false, children: [] },
        { id: "t1-spec-d4", title: "Spec: BFS Avoidance at degree 4", statement: "Specify Conjecture 5.5 for a vertex v with c(v)=5 and deg(v)=4: definitions, exact claim, acceptance test for a future proof, cited evidence, and kill criterion. The conjecture is not claimed proved.", status: "in-progress", approach: "Agent 1701 task K1, manager M-Kempe. Specification accepted at the critic gate. The conjecture itself is not proved.", killCriteria: "A written counterexample: one planar graph, one proper 5-colouring, one degree-4 vertex coloured 5, and one shortest path that swaps an (a,5)-chain meeting a neighbour of v while v bridges at least two (a,5)-chains.", files: ["backgroundMaterial/agent1701/tasks/K1.md", "backgroundMaterial/agent1701/groups/K1_spec.md", "SolvingFrameworkPlan/docs/working/ExecutiveSummary_Plan2_Status.md"], notes: [{ "time": "2026-09-27T19:45:00Z", "text": "Issued by the main planning team. Not accepted until the critic gate." }, { "time": "2026-09-27T20:30:00Z", "text": "Critic gate accepted the specification. The conjecture is not proved and is not killed." }, { "time": "2026-09-27T21:40:00Z", "text": "The universal degree-4 statement met its kill criterion. The dead end is recorded on t1-conj-d4. This node remains the specification." }], evidence: "Spec accepted 2026-09-27. The universal statement is a dead end: on T_9_35, vertex 6, colouring (1,2,3,4,5,3,5,2,5), a length-2 shortest path swaps the (3,5)-chain {2,8}. See t1-conj-d4. The specification document is kept.", expanded: true, children: [] },
        { id: "t1-spec-d5", title: "Spec: BFS Avoidance at degree 5", statement: "Specify Conjecture 5.5 for deg(v)=5, and the observation that would reclassify the conjecture as a reformulation of the Four Colour Theorem rather than a shorter gap.", status: "in-progress", approach: "Agent 1701 task K2, manager M-Kempe. Specification accepted. Sequencing change: do not prove degree 4 first while the T_9,35 assertion is unverified.", killCriteria: "A written counterexample meeting the degree-5 kill test, or a proved reduction showing 4-colourability of an arbitrary triangulation is equivalent to this avoidance statement.", files: ["backgroundMaterial/agent1701/tasks/K2.md", "backgroundMaterial/agent1701/groups/K2_spec.md", "SolvingFrameworkPlan/docs/working/ExecutiveSummary_Plan2_Status.md"], notes: [{ "time": "2026-09-27T19:45:00Z", "text": "Issued by the main planning team. Not accepted until the critic gate." }, { "time": "2026-09-27T20:30:00Z", "text": "Critic gate accepted the specification. Observation R (equivalence with 4CT) is not established." }], evidence: "Spec accepted 2026-09-27. The universal degree-5 statement is a dead end on one colouring of T_9_25 at vertex 3; see t1-conj-d5. Observation R is not established. Track 1 is not killed.", expanded: false, children: [] },
        { id: "t1-witness-935", title: "Write the T_9,35 degree-4 witness", statement: "Exhibit the edge set of triangulation T_9,35 and one shortest path in R(G-v,5) at vertex 6 that meets the degree-4 kill criterion, or show that no such colouring exists.", status: "in-progress", approach: "Witness written and accepted by the critic. The universal conjecture is recorded as killed on t1-conj-d4, not on this node.", killCriteria: "The cited Agent 1419 assertion cannot be tied to a graph and a path, or the exhibited path fails the kill test in K1_spec.md.", files: ["backgroundMaterial/agent1701/tasks/W1.md", "backgroundMaterial/agent1701/groups/W_graph.md", "backgroundMaterial/agent1701/groups/W_path.md"], notes: [{ "time": "2026-09-27T20:30:00Z", "text": "Issued by the main planning team after the critic gate. Not complete." }, { "time": "2026-09-27T21:40:00Z", "text": "Critic accepted the witness. Edges of generate_triangulations(9)[35] match the JSON record. The length-2 path meets the kill test." }], evidence: "Accepted 2026-09-27. T_9_35 has 21 edges; vertex 6 has degree 4 and neighbours 0,1,2,5. Colouring 0:1, 1:2, 2:3, 3:4, 4:5, 5:3, 6:5, 7:2, 8:5. First step swaps (3,5)-chain {2,8} while neighbours 2 and 5 lie in distinct (3,5)-chains.", expanded: true, children: [] },
        { id: "t1-conj-d4", title: "Degree-4 universal BFS avoidance", statement: "Every shortest path in R(G-v,5) avoids unsafe (a,5)-swaps when c(v)=5 and deg(v)=4.", status: "killed", approach: "Killed by a written witness on one colouring. A weaker existence statement for stored colourings of this one graph is t1-weaker-935.", killCriteria: "Met. See evidence.", files: ["backgroundMaterial/agent1701/groups/W_path.md", "backgroundMaterial/agent1701/critic/witness_gate.md"], notes: [{ "time": "2026-09-27T21:40:00Z", "text": "Critic gate: dead end. This does not kill Track 1 or the Four Colour Theorem." }], evidence: "On T_9_35 = generate_triangulations(9)[35], vertex 6, one shortest path swaps {2,8}. Of 1440 proper 5-colourings with c(6)=5, the stored set S of 24 has every shortest path unsafe, and each of those 24 has a K1-safe path of length 3 (1.164s). Of the other 1416, zero have every shortest path unsafe (1.431s). These counts are computations on one triangulation, not a theorem.", expanded: false, children: [] },
        { id: "t1-conj-d5", title: "Degree-5 universal BFS avoidance", statement: "Every shortest path in R(G-v,5) avoids unsafe (a,5)-swaps when c(v)=5 and deg(v)=5.", status: "killed", approach: "Killed by a written witness on one colouring of T_9_25. Not a kill of Track 1.", killCriteria: "Met. See evidence.", files: ["backgroundMaterial/agent1701/groups/D5_witness.md", "backgroundMaterial/agent1701/groups/D5_classify.md"], notes: [{ "time": "2026-09-27T21:40:00Z", "text": "Critic gate: dead end on one colouring. The classification of all 1248 colourings is an accepted computation, not a theorem." }], evidence: "On T_9_25 = generate_triangulations(9)[25], vertex 3, one shortest path swaps the (4,5)-chain {4,5} while vertex 3 bridges {4,5} and {6,8}. Of 1248 proper 5-colourings with c(3)=5, 24 have every shortest path unsafe, and each of those 24 has a K1-safe path of length opt_dist+1 (6.536s). Another 120 have some unsafe shortest path and still have a safe shortest path.", expanded: false, children: [] },
        { id: "t1-weaker-935", title: "Spec: safe length-3 paths on stored T_9,35 colourings", statement: "For every colouring in the stored set S of 24 colourings of T_9_35 at vertex 6, a K1-safe path of length 3 exists in R(G-6,5). S is not all 1440 proper 5-colourings with c(6)=5.", status: "in-progress", approach: "Specification K3 accepted by the critic. The statement quantifies over S only. W5 separately classified the 1416 colourings outside S.", killCriteria: "One colouring in S with no K1-safe path of length 3.", files: ["backgroundMaterial/agent1701/groups/K3_weaker_spec.md", "backgroundMaterial/agent1701/groups/W3_batch.md", "backgroundMaterial/agent1701/groups/W5_classify.md"], notes: [{ "time": "2026-09-27T21:40:00Z", "text": "Critic accepted the specification and the W3 and W5 computations. Not a theorem about all planar graphs." }], evidence: "W3: 24/24 stored colourings have a K1-safe path of length 3, elapsed 1.164s. W4: 1440 proper 5-colourings with c(6)=5, 24 in S, 1416 outside, elapsed 1.057s. W5: of the 1416, 8 have one unsafe shortest path, 0 have every shortest path unsafe, and those 8 have a safe path of length opt_dist+1, elapsed 1.431s.", expanded: false, children: [] }
      ]
    },
    {
      id: "track2",
      title: "Track 2: Chromatic Polynomial",
      statement: "P(G, 4) > 0 for all planar G.",
      status: "unstarted",
      approach: "Prove the 4CT algebraically by analyzing the chromatic polynomial. Start with restricted planar families (outerplanar, series-parallel, bounded treewidth), build upward.",
      killCriteria: "Real root of P(G,k) found in (3,4) for some planar G (kills root-bounding approach). OR cannot prove even outerplanar case after 8 weeks.",
      files: [],
      notes: [],
      evidence: "",
      expanded: false,
      children: [
        { id: "t2-1", title: "Formalize P(G,k) in Lean 4", statement: "P(G,k) via deletion-contraction.", status: "unstarted", approach: "Define recursively. Prove P(G-e,k) - P(G/e,k) identity.", killCriteria: "", files: ["lean4/FourColor/Track2_ChromaticPoly/"], plannedFiles: ["lean4/FourColor/Track2_ChromaticPoly/"], notes: [], evidence: "", expanded: false, children: [] },
        { id: "t2-2", title: "Compute roots for planar triangulations n\u226420", statement: "Find all real roots of P(G,k) for small planar graphs.", status: "unstarted", approach: "SageMath symbolic computation.", killCriteria: "Root in (3,4) found", files: ["compute/chromatic/root_finder.py"], notes: [], evidence: "", expanded: false, children: [] },
        { id: "t2-3", title: "Prove P(G,4)>0 for outerplanar", statement: "Outerplanar graphs: P(G,4) > 0.", status: "unstarted", approach: "Outerplanar = treewidth \u2264 2. Should be tractable.", killCriteria: "Stalls > 6 weeks", files: [], notes: [], evidence: "", expanded: false, children: [] },
        { id: "t2-4", title: "Prove P(G,4)>0 for series-parallel", statement: "Series-parallel graphs: P(G,4) > 0.", status: "unstarted", approach: "Extend outerplanar result.", killCriteria: "Stalls > 6 weeks", files: [], notes: [], evidence: "", expanded: false, children: [] }
      ]
    },
    {
      id: "track3",
      title: "Track 3: Nowhere-Zero Flows",
      statement: "Every bridgeless planar graph has a nowhere-zero 4-flow.",
      status: "unstarted",
      approach: "Tutte duality: 4CT for planar \u2261 4-flow for bridgeless planar. Formalize flows and duality. Attempt 4-flow directly via modular linear algebra.",
      killCriteria: "6-flow formalization stalls > 10 weeks.",
      files: [],
      notes: [],
      evidence: "",
      expanded: false,
      children: [
        { id: "t3-1", title: "Formalize nowhere-zero k-flows", statement: "Orientation + edge labels in {1,...,k-1} satisfying Kirchhoff at each vertex mod k.", status: "unstarted", approach: "Define in Lean 4.", killCriteria: "", files: ["lean4/FourColor/Track3_Flows/"], plannedFiles: ["lean4/FourColor/Track3_Flows/"], notes: [], evidence: "", expanded: false, children: [] },
        { id: "t3-2", title: "Prove Tutte duality (planar)", statement: "G is k-colourable \u21D4 G* has nowhere-zero k-flow.", status: "unstarted", approach: "Requires planar dual construction.", killCriteria: "", files: [], notes: [], evidence: "", expanded: false, children: [] },
        { id: "t3-3", title: "Prove 6-flow theorem (Seymour)", statement: "Every bridgeless graph has a nowhere-zero 6-flow.", status: "unstarted", approach: "Would be a major Lean 4 / Mathlib contribution.", killCriteria: "Stalls > 10 weeks", files: [], notes: [], evidence: "", expanded: false, children: [] }
      ]
    },
    {
      id: "track4",
      title: "Track 4: TQFT / Penrose Evaluation",
      statement: "Penrose evaluation (SO(3) state sum) is nonzero for all bridgeless planar cubic graphs.",
      status: "unstarted",
      approach: "Kauffman (1990) reformulated 4CT as a state sum non-vanishing condition. Prove via unitarity / positivity of the modular tensor category. The most mathematically exciting track.",
      killCriteria: "Penrose eval = 0 for some bridgeless planar cubic graph (= 4CT counterexample, essentially impossible). OR no positivity mechanism after 3 months.",
      files: [],
      notes: [],
      evidence: "",
      expanded: false,
      children: [
        { id: "t4-1", title: "Implement Penrose evaluation", statement: "Compute the Penrose evaluation for planar cubic graphs.", status: "unstarted", approach: "Python symbolic algebra.", killCriteria: "", files: ["compute/topology/penrose_eval.py"], notes: [], evidence: "", expanded: false, children: [] },
        { id: "t4-2", title: "Verify nonzero for n \u2264 30", statement: "All bridgeless planar cubic graphs on \u226430 vertices.", status: "unstarted", approach: "Exhaustive computation.", killCriteria: "Zero found", files: [], notes: [], evidence: "", expanded: false, children: [] },
        { id: "t4-3", title: "Study 6j-symbol sign conditions", statement: "Do the 6j-symbols prevent cancellation?", status: "unstarted", approach: "Symbolic algebra + algebraic analysis.", killCriteria: "Signs alternate with no positivity", files: [], notes: [], evidence: "", expanded: false, children: [] },
        { id: "t4-4", title: "Identify positivity mechanism", statement: "Why is the state sum always positive for planar inputs?", status: "unstarted", approach: "Paper math. Modular tensor category structure.", killCriteria: "No mechanism after 3 months", files: [], notes: [], evidence: "", expanded: false, children: [] }
      ]
    },
    {
      id: "track5",
      title: "Track 5: Spectral / Colin de Verdi\u00e8re",
      statement: "\u03C7(G) \u2264 \u03BC(G) + 1 for planar graphs (which gives \u03C7 \u2264 4 since \u03BC \u2264 3).",
      status: "unstarted",
      approach: "Colin de Verdi\u00e8re\u2019s invariant \u03BC(G) \u2264 3 iff G is planar. The conjecture \u03C7 \u2264 \u03BC+1 would prove 4CT immediately.",
      killCriteria: "Counterexample to \u03C7 \u2264 \u03BC+1 for ANY graph. OR \u03BC computation too expensive for n > 12.",
      files: [],
      notes: [],
      evidence: "",
      expanded: false,
      children: [
        { id: "t5-1", title: "Compute \u03BC(G) for small planar graphs", statement: "SDP computation of Colin de Verdi\u00e8re invariant.", status: "unstarted", approach: "Python + CVXPY.", killCriteria: "Counterexample", files: ["compute/spectral/colin_de_verdiere.py"], notes: [], evidence: "", expanded: false, children: [] },
        { id: "t5-2", title: "Formalize \u03BC(G) in Lean 4", statement: "Define via matrix optimization with transversality.", status: "unstarted", approach: "Lean 4 definition.", killCriteria: "", files: ["lean4/FourColor/Track5_Spectral/"], plannedFiles: ["lean4/FourColor/Track5_Spectral/"], notes: [], evidence: "", expanded: false, children: [] }
      ]
    },
    {
      id: "track6",
      title: "Track 6: Sheaf Cohomology",
      statement: "Define sheaf F_4 on G s.t. \u0393(G, F_4) = proper 4-colourings. Prove H^1 = 0 for planar G.",
      status: "unstarted",
      approach: "Cohomological vanishing theorem for graph colourability. If planarity forces H^1(G, F_4) = 0, global sections (= 4-colourings) exist. Most speculative track.",
      killCriteria: "H^1 \u2260 0 for some planar G at k=4. OR cannot define coherent colouring sheaf after 6 weeks.",
      files: [],
      notes: [],
      evidence: "",
      expanded: false,
      children: [
        { id: "t6-1", title: "Compute sheaf cohomology for small graphs", statement: "H^0, H^1 of candidate colouring sheaves.", status: "unstarted", approach: "Python linear algebra.", killCriteria: "H^1 \u2260 0 for planar G", files: ["compute/topology/sheaf_cohomology.py"], notes: [], evidence: "", expanded: false, children: [] },
        { id: "t6-2", title: "Formalize cellular sheaves on graphs", statement: "Lean 4 formalization of sheaves on graphs.", status: "unstarted", approach: "New Lean 4 library. Would be useful to community.", killCriteria: "Stalls > 6 weeks", files: ["lean4/FourColor/Track6_Sheaf/"], plannedFiles: ["lean4/FourColor/Track6_Sheaf/"], notes: [], evidence: "", expanded: false, children: [] }
      ]
    },
    {
      id: "track7",
      title: "Track 7: Computational Discovery",
      statement: "Use tensor networks, GDL, and symbolic computation to discover new structural patterns.",
      status: "unstarted",
      approach: "Experimental math: compute, find patterns, conjecture, prove. Feeds all other tracks.",
      killCriteria: "GDL model accuracy < 80%. All patterns fail on n > 20.",
      files: [],
      notes: [],
      evidence: "",
      expanded: false,
      children: [
        { id: "t7-1", title: "Build chromatic polynomial database", statement: "P(G,k) for all planar triangulations n \u2264 25.", status: "unstarted", approach: "Tensor network contraction.", killCriteria: "", files: ["compute/discovery/tensor_network.py"], notes: [], evidence: "", expanded: false, children: [] },
        { id: "t7-2", title: "Chromatic root atlas", statement: "Plot all roots in C, especially near k=4.", status: "unstarted", approach: "Python + matplotlib.", killCriteria: "", files: ["compute/chromatic/root_finder.py"], notes: [], evidence: "", expanded: false, children: [] },
        { id: "t7-3", title: "Train GDL model", statement: "Predict Kempe reducibility from graph structure.", status: "unstarted", approach: "PyTorch Geometric. 3-WL architecture.", killCriteria: "Accuracy < 80%", files: ["compute/discovery/gnn_coloring.py"], notes: [], evidence: "", expanded: false, children: [] },
        { id: "t7-4", title: "Analyze learned features", statement: "What graph features does the model use?", status: "unstarted", approach: "Attribution analysis.", killCriteria: "No interpretable features", files: [], notes: [], evidence: "", expanded: false, children: [] }
      ]
    },
    {
      id: "audit-1701",
      title: "Reconcile navigator with the repo",
      statement: "For each proof-tree node, state whether a cited file exists and whether prior reports support a status other than unstarted. Recommendations are not applied until the critic gate.",
      status: "in-progress",
      approach: "Agent 1701 task F1, manager M-Foundation. Audit accepted. The gate left mathematical track statuses unchanged.",
      killCriteria: "Critic gate rejects the audit as unverifiable.",
      files: ["backgroundMaterial/agent1701/tasks/F1.md", "backgroundMaterial/agent1701/groups/F1_audit.md"],
      notes: [{ "time": "2026-09-27T19:45:00Z", "text": "Issued by the main planning team. Status changes to mathematical nodes wait on the critic gate." }, { "time": "2026-09-27T20:30:00Z", "text": "Critic gate accepted the audit and refused to mark track1, t1-1, or track4 in progress. Fifteen linked paths are missing. The six Plan 2 lemmas have argument files. The executive summary's near-complete-proof line was refused as hot air." }],
      evidence: "Audit accepted 2026-09-27. Fifteen unique linked paths are missing. Foundation and f5 stay unstarted: F5_FiveColorTheorem.lean is absent. Tracks 2, 3, 5, 6, and 7 stay unstarted. track4 stays unstarted at the gate even though compute/topology/penrose_eval.py exists: a Python file is not track progress.",
      expanded: false,
      children: []
    }
  ]
};
