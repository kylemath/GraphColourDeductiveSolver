# Image Generation Prompts — Four Colour Theorem Proof Plans

Three self-contained prompts for generating whiteboard infographic images. Each follows the same visual language and constraints. Paste each prompt individually into the image generator.

---

## Shared Style Constraints (included in each prompt below)

These constraints are already embedded in each prompt — this section is for reference only.

- **Format:** Landscape orientation, high resolution (at minimum 1920×1080 equivalent)
- **Style:** Clean whiteboard infographic — off-white/cream background (#F5F0E8), hand-drawn-feeling but precise mathematical diagrams, dark ink (#1A1A2E) for text and lines, accent colours for emphasis
- **Typography:** Bold sans-serif headers, clean serif or monospace for math notation, handwritten-style annotations
- **Layout:** Multiple sub-panels arranged in a clear reading order (top-to-bottom, left-to-right), connected by arrows showing flow
- **Colour palette:** Dark navy ink (#1A1A2E), teal (#2EC4B6), coral (#E71D36), amber (#FF9F1C), soft blue (#4361EE), muted green (#3A7D44), light grey for secondary elements
- **Mathematical notation:** Rendered clearly, not as LaTeX code — actual symbols (Σ, χ, ∀, ≤, etc.)
- **No photorealism.** This is a diagram/infographic, not a photograph.

---

## PROMPT 1: Plan 1 — Refined Discharging + SAT + Proof Mining

```
Create a detailed landscape whiteboard infographic titled "PLAN 1: REFINED DISCHARGING + SAT OPTIMIZATION + PROOF MINING" showing a complete step-by-step proof strategy for the Four Colour Theorem.

STYLE: Clean whiteboard/chalkboard infographic on an off-white cream background (#F5F0E8). Dark navy ink (#1A1A2E) for text and lines. Accent colours: teal (#2EC4B6), coral (#E71D36), amber (#FF9F1C). Bold sans-serif headers, clean mathematical notation with actual symbols (not LaTeX). Hand-drawn-feeling but precise diagrams. No photorealism — this is a technical infographic.

HEADER BANNER: Across the top, a bold banner reading "PLAN 1: REFINED DISCHARGING + SAT + PROOF MINING" with subtitle "Priority: CRITICAL — 6-12 months — Highest Confidence Path" in teal. A small "Four Colour Theorem" badge in the top-right corner.

The infographic has 8 SUB-PANELS arranged in a flowing layout with arrows connecting them:

SUB-PANEL A — "THE CORE EQUATION" (top-left, small)
Show the charge assignment formula on a small planar graph diagram:
- A triangulated planar graph with ~8 vertices
- Each vertex labelled with its charge: c(v) = 6 - deg(v)
- Vertices of degree 5 labelled "+1", degree 6 labelled "0", degree 7 labelled "-1"
- Curved arrows showing charge being redistributed between vertices
- Below: the equation Σ c(v) = 12 in large clear text
- Caption: "Euler's formula guarantees total positive charge = 12"

SUB-PANEL B — "THE UNAVOIDABLE SET" (top-center)
Show a visual representation of configurations shrinking:
- LEFT SIDE: A large grid/mosaic of ~30 small hexagonal graph configurations (representing 633), labelled "RSST 1997: N = 633"
- An arrow pointing RIGHT
- RIGHT SIDE: A much smaller cluster of ~6-8 configurations, labelled "TARGET: N ≤ 50"
- Between them: "32 rules → optimized rules" and "SAT/SMT search"
- The shrinking is dramatic and visually clear
- Below: a horizontal bar showing the Pareto frontier — x-axis "Configuration Count N" (633 down to 50), y-axis "Rule Complexity" — with dots for Appel-Haken (487 rules, 1476 configs), RSST (32 rules, 633 configs), and a target zone (≤64 rules, ≤50 configs)

SUB-PANEL C — "CONFIGURATION RING" (top-right, medium)
Show a single configuration with its boundary ring:
- An octagonal ring of 8 vertices (r₁ through r₈) connected in a cycle
- Interior vertices and edges forming a small triangulated graph inside the ring
- The ring vertices are coloured with 4 colours (red, blue, green, yellow)
- Annotation: "D-reducible if ALL 4^|R| boundary colourings extend inward"
- Show a small Kempe chain (bichromatic path) highlighted in two colours inside the configuration
- Caption: "Each configuration: verify 4-colouring extends from ring to interior via Kempe swaps"

SUB-PANEL D — "PHASE 1: INFRASTRUCTURE" (middle-left)
A checklist-style panel with three items, each with an icon:
1. Python/Rust icon → "Flexible Discharging Framework: input rules → compute unavoidable set → test reducibility"
2. Coq logo icon → "Instrument Gonthier's 60,000-line Coq proof: extract 633 reducibility traces"
3. Lean 4 icon → "Build shared Lean 4 libraries: planar graphs, Kempe chains, Five Colour Theorem"
Timeline bar: "Months 1-2"

SUB-PANEL E — "PHASE 2: SAT SEARCH" (middle-center, prominent)
Show a SAT solver optimization loop:
- A circuit/logic gate icon labelled "CaDiCaL / Kissat"
- Input arrow: "Candidate discharging rules"
- Processing: "Encode as Boolean SAT → Solve → Extract unavoidable set → Check reducibility"
- Output arrow: "Minimum N found"
- A progress timeline below: Month 2: "N=633 (reproduce)", Month 3: "N≤400", Month 4: "N≤200", Month 5: "N≤100?"
- Each milestone in a circle getting smaller (representing fewer configurations)
- Parallel branch: "CLUSTER ANALYSIS" — show 633 dots being grouped into ~5 colour-coded clusters, with label "Do the 633 checks share common argument patterns?"

SUB-PANEL F — "PHASE 3: PROOF CONSTRUCTION" (middle-right)
Show the assembly of a proof document:
- A stack of pages icon, with sections labelled:
  - "Preliminaries (5 pp): Euler, Kempe, 5CT"
  - "Discharging (5-10 pp): Optimized rules → unavoidable set"
  - "Reducibility (10-30 pp): Parameterized lemma families"
  - "Appendix: Individual 1-page arguments"
- Total: "≤ 50 pages" circled in teal
- Arrow pointing to a computer screen icon showing "theorem four_colour : ∀ G, IsPlanar G → Colorable 4 G" — the Lean 4 formalization
- Caption: "Human-readable proof + machine-verified"

SUB-PANEL G — "PHASE 4: REFINE & PUBLISH" (bottom-right, small)
Three icons in a row:
1. SAT solver icon → "Push N even lower"
2. AI/brain icon → "LLM-assisted proof compression"
3. Paper/publication icon → "Technical paper + Mathlib contribution"

SUB-PANEL H — "SUCCESS CRITERIA" (bottom strip across full width)
Four medal icons in a row (Bronze, Silver, Gold, Platinum):
- Bronze: "N ≤ 500, reproduce RSST" (Very High feasibility)
- Silver: "N ≤ 200, 3+ config clusters" (High)
- Gold: "N ≤ 50, parameterized lemmas cover 80%" (Medium-High)
- Platinum: "Complete human-readable proof + Lean 4" (Medium)

CONNECTING ARROWS: Large flowing arrows connect the panels in order: A→B→C forms the mathematical foundation row; D→E→F forms the execution row; G and H are the conclusion row. The overall flow is top-to-bottom, left-to-right.

FOOTER: Small text "Graph Colour Project — Plan 1 — February 2026" and "Key insight: No lower bound on minimum N is known. Modern SAT solvers have never been applied to this optimization."
```

---

## PROMPT 2: Plan 2 — Kempe Swap Game + Topological Non-Crossing

```
Create a detailed landscape whiteboard infographic titled "PLAN 2: KEMPE SWAP GAME + TOPOLOGICAL NON-CROSSING" showing a complete step-by-step proof strategy for the Four Colour Theorem.

STYLE: Clean whiteboard/chalkboard infographic on an off-white cream background (#F5F0E8). Dark navy ink (#1A1A2E) for text and lines. Accent colours: coral (#E71D36), amber (#FF9F1C), purple (#7B2D8E), soft blue (#4361EE). Bold sans-serif headers, clean mathematical notation with actual symbols. Hand-drawn-feeling but precise diagrams. No photorealism — this is a technical infographic.

HEADER BANNER: Bold banner "PLAN 2: KEMPE SWAP GAME + TOPOLOGICAL NON-CROSSING" with subtitle "Priority: HIGH — 6-18 months — Most Promising Novel Strategy" in coral. Small "Four Colour Theorem" badge top-right.

The infographic has 9 SUB-PANELS arranged in a flowing layout:

SUB-PANEL A — "THE CORE IDEA" (top-left, prominent)
A visual comparison showing WHY 5CT is easy and 4CT is hard:
- LEFT: "5 COLOURS — ONE SWAP ALWAYS WORKS"
  - A degree-5 vertex v in the center with 5 neighbours w₁...w₅ arranged in a pentagon
  - Each neighbour coloured differently (5 distinct colours: red, blue, green, yellow, purple)
  - A thick bichromatic Kempe chain (red-green) highlighted, connecting w₁ to w₃
  - An arrow showing the swap succeeds
  - Checkmark icon
- RIGHT: "4 COLOURS — SWAPS CAN INTERFERE"
  - Same degree-5 vertex v, but now two neighbours share a colour (red)
  - Two Kempe chains shown, with a collision/interference symbol (X) where they interact
  - Question mark icon
- Between them: "The gap between 5CT and 4CT is exactly the interference problem"

SUB-PANEL B — "THE NON-CROSSING CONSTRAINT" (top-center, large and prominent)
The key mathematical insight, shown as a planar diagram:
- A degree-5 vertex v in the center of a planar embedding
- 5 neighbours w₁...w₅ in cyclic order around v
- A thick coloured Kempe chain (red-blue, drawn as a curving path) connecting w₁ to w₃, forming a Jordan curve
- The chain visually divides the plane into TWO REGIONS
- w₂ is clearly shown TRAPPED in the interior region (highlighted with a light tint)
- w₄ and w₅ are in the exterior region
- A dotted line from w₂ showing its Kempe chain CANNOT cross the w₁-w₃ chain
- Label: "Jordan Curve Theorem: Kempe chains for disjoint colour pairs CANNOT CROSS in a planar graph"
- Annotation: "This constraint is barely exploited in existing proofs — Agent 1221 calls it 'the central underexploited mathematical structure'"

SUB-PANEL C — "THE RECONFIGURATION GRAPH" (top-right)
Show the conceptual structure:
- A small graph where each NODE represents a proper colouring (shown as a tiny coloured graph icon)
- EDGES connect colourings that differ by one Kempe swap
- Show two levels:
  - R(G, 5): "All 5-colourings connected (Las Vergnas-Meyniel 1981)" — highlighted as connected
  - R(G, 4): "Connected? OPEN QUESTION" — shown with a question mark
- A path highlighted from a 5-coloring node down to a 4-coloring node, with labels "Kempe swap → Kempe swap → ... → 4-colouring!"
- Caption: "4CT ⟺ every 5-colouring can reach a 4-colouring via Kempe swaps"

SUB-PANEL D — "PHASE 1: COMPUTATIONAL VERIFICATION" (middle-left)
A computation pipeline:
- Icon: "plantri" tool → generates all planar triangulations
- Table showing scale:
  - n ≤ 12: thousands (minutes) ✓
  - n ≤ 15: hundreds of thousands (hours)
  - n ≤ 18: tens of millions (days)
  - n ≤ 20: billions (HPC)
- For each triangulation: "Enumerate all 5-colourings → BFS on reconfiguration graph → Find path to 4-colouring"
- BIG LABEL: "Kill criterion: ANY counterexample found → strategy is dead (but significant negative result)"
- Timeline bar: "Months 1-4"

SUB-PANEL E — "PHASE 2: TOPOLOGICAL ANALYSIS" (middle-center, important)
Two theorem boxes stacked:
- "THEOREM A (Non-Interleaving): If K_ab chain from wᵢ reaches wₖ, then K_cd chain from wⱼ stays within the arc — no crossing"
  - Small diagram showing chains respecting each other's regions
- "THEOREM B (Confinement): If K_ab separates wⱼ from wₗ, no swaps on other colours can reconnect them"
  - Small diagram showing confinement
- Below: "CASE CLASSIFICATION: Enumerate ALL topologically distinct Kempe patterns at degree-5 vertices under non-crossing. Target: ≤ 20 patterns, each individually analyzed."
- Timeline bar: "Months 3-8"

SUB-PANEL F — "PHASE 3: COLOUR ELIMINATION" (middle-right)
The core lemma shown step-by-step:
- Start: A planar graph with a proper 5-colouring (5 colours shown, one colour — purple — used sparingly)
- Step 1: "Choose the least-used colour (say purple, k vertices)"
- Step 2: "For each purple vertex vᵢ: examine neighbourhood → apply Kempe swaps → recolour to {1,2,3,4}"
- Step 3: "Non-crossing constraint limits which swaps can fail"
- End: Same graph, now with only 4 colours. Purple eliminated.
- KEY LEMMA box: "∃ ordering v₁,...,v_k such that each vᵢ can be recoloured using swaps not affecting earlier vertices"
- Caption: "If true → constructive proof of 4CT"
- Timeline bar: "Months 6-12"

SUB-PANEL G — "FISK HOMOLOGY" (bottom-left, smaller)
Algebraic structure panel:
- "4-colourings mod Kempe swaps form a group ≅ Z₂^g"
- Show the group structure as a small lattice/cube diagram
- "Fisk (1977): This algebraic structure constrains the reconfiguration landscape"
- "5-colouring reducible ⟺ its Fisk class intersects the set of 4-colourings"

SUB-PANEL H — "PHASE 4: SYNTHESIS + FALLBACK" (bottom-center)
Two paths shown:
- SUCCESS PATH (teal): "5CT start → Non-crossing constrains → Case analysis resolves → Colour elimination proves 4CT → Lean 4 formalization"
- FALLBACK PATH (amber): "Non-crossing theorems (publishable) + Computational verification n≤20 (publishable) + Fisk analysis (publishable) + Feeds Plan 1 reducibility proofs"

SUB-PANEL I — "SUCCESS CRITERIA" (bottom strip)
Four medal icons:
- Bronze: "5→4 verified for all n ≤ 15" (Very High)
- Silver: "Non-crossing Theorems A & B proved" (High)
- Gold: "Complete degree-5 case classification" (Medium-High)
- Platinum: "Colour Elimination Lemma → 4CT" (Medium)

CONNECTING ARROWS: A→B→C is the mathematical insight row (the "why"). D→E→F is the execution row (the "how"). G and H form the synthesis row. The central flow is: Understand non-crossing (B) → Verify computationally (D) → Classify cases (E) → Eliminate colour (F) → Prove 4CT.

FOOTER: "Graph Colour Project — Plan 2 — February 2026" and "Key insight: The Jordan Curve Theorem constrains HOW Kempe chains interfere. This topological constraint is the most underexploited structure in the problem."
```

---

## PROMPT 3: Plan 3 — TQFT / Penrose Evaluation + Sheaf Cohomology

```
Create a detailed landscape whiteboard infographic titled "PLAN 3: TQFT / PENROSE EVALUATION + SHEAF COHOMOLOGY" showing a complete step-by-step proof strategy for the Four Colour Theorem.

STYLE: Clean whiteboard/chalkboard infographic on an off-white cream background (#F5F0E8). Dark navy ink (#1A1A2E) for text and lines. Accent colours: deep blue (#4361EE), violet (#7B2D8E), teal (#2EC4B6), gold (#D4AF37). Bold sans-serif headers, clean mathematical notation with actual symbols. Hand-drawn-feeling but precise diagrams. No photorealism — this is a technical infographic.

HEADER BANNER: Bold banner "PLAN 3: TQFT / PENROSE EVALUATION + SHEAF COHOMOLOGY" with subtitle "Priority: MEDIUM — 1-3 years — Highest Mathematical Ceiling" in deep blue. Small "Four Colour Theorem" badge top-right.

The infographic has 10 SUB-PANELS arranged in a flowing layout:

SUB-PANEL A — "KAUFFMAN'S REFORMULATION" (top-left, prominent)
The key equivalence, shown visually:
- LEFT SIDE: A planar map with regions coloured in 4 colours (red, blue, green, yellow). Label: "4CT: Every planar map is 4-colourable"
- EQUALS SIGN (large, dramatic)
- RIGHT SIDE: A planar cubic graph (every vertex has degree 3) with edges labelled 1, 2, 3 in three distinct colours. At each vertex, show the ε_{ijk} symbol (Levi-Civita). Label: "Pen(G) > 0: Penrose evaluation is nonzero for all bridgeless planar cubic graphs"
- Below: "Kauffman (1990): These are EQUIVALENT. This is a proven theorem, not a conjecture."
- The formula: Pen(G) = Σ (over valid labellings) Π |ε_{ijk}| = # of proper edge-3-colourings

SUB-PANEL B — "THE TQFT CONNECTION" (top-center)
Show the quantum topology framework:
- A bracket notation diagram: |ψ_G⟩ in a large ket symbol
- Arrow to inner product: ⟨ψ_G|ψ_G⟩ = Pen(G) ≥ 0
- Label: "By UNITARITY of the modular tensor category, the Penrose evaluation is an inner product — automatically non-negative"
- Below: "4CT ⟺ |ψ_G⟩ ≠ 0 for bridgeless planar cubic G"
- Small icon showing the Turaev-Viro state sum connection
- Show the quantum group notation: U_q(sl_2) at q = e^{iπ/3}
- Caption: "The Penrose evaluation is a specialization of the Turaev-Viro TQFT invariant"

SUB-PANEL C — "THE SHEAF APPROACH" (top-right)
Show the sheaf cohomology formulation:
- A small graph with vector spaces (drawn as small boxes labelled "R⁴") sitting above each vertex
- Arrows (restriction maps) going from vertex stalks to edge stalks
- Labels: "Vertex stalk F(v) = R⁴ (colour space)" and "Edge stalk F(e): pairs of different colours"
- Below: "Global sections Γ(G, F₄) = proper 4-colourings"
- The key equation in a box: "H¹(G, F₄) = 0 for planar G → 4-colourings EXIST"
- Analogy note: "Like Kodaira vanishing in algebraic geometry: positivity → H¹ = 0 → global sections exist"

SUB-PANEL D — "FOUR INDEPENDENT PATHS" (below the top row, spanning full width)
A horizontal flow showing 4 parallel proof attempts, all converging to "4CT PROVED":
- PATH 2A: "Unitarity argument" — ⟨ψ|ψ⟩ > 0 via faithful Temperley-Lieb representation
- PATH 2B: "Kuperberg web basis" — positivity of web basis coefficients for planar diagrams
- PATH 2C: "Sheaf vanishing theorem" — H¹ = 0 via planar positivity condition (Mayer-Vietoris on separators)
- PATH 2D: "Chromatic homology positivity" — P(G,k) = Σ(-1)^i k^j dim H^{i,j} → positive at k=4
- All four paths have arrows converging to a central node: "ANY ONE SUCCEEDING PROVES 4CT"
- Each path has a small icon: quantum symbol, spider web, sheaf diagram, chain complex

SUB-PANEL E — "PHASE 1: COMPUTATIONAL FOUNDATIONS" (middle-left)
Four computation tasks shown as a grid:
- "1A: Penrose evaluation" — icon of cubic graph with edge labels → "Compute for all bridgeless planar cubic graphs n ≤ 30. Verify ALL positive."
- "1B: 6j-symbols" — icon of quantum group symbol → "Compute signs and magnitudes. Do they prevent cancellation?"
- "1C: Sheaf cohomology" — icon of graph with stalks → "Compute H⁰, H¹ for small planar graphs. Is H¹ always 0?"
- "1D: Chromatic homology" — icon of chain complex → "Compute H^{i,j}(G) at k=4. Concentration in even degrees?"
- Timeline bar: "Months 1-4"
- Kill criteria in red: "H¹ ≠ 0 for some planar G (kills sheaf path)" and "6j signs alternate with no pattern (weakens TQFT path)"

SUB-PANEL F — "PHASE 2: THEORETICAL ANALYSIS" (middle-center, large)
Four proof attempts shown as branching paths from Phase 1:
- 2A UNITARITY: "Express Pen(G) = ⟨ψ|ψ⟩ → Show |ψ⟩ ≠ 0 for planar inputs → Faithfulness of Temperley-Lieb representation"
- 2B WEB BASIS: "Express Pen(G) in Kuperberg basis → Verify non-negative coefficients from planarity → Bridgeless → strictly positive"
- 2C SHEAF: "Define 'planar-positive' sheaves → Show F₄ is planar-positive → Prove vanishing: positive sheaves have H¹ = 0"
- 2D HOMOLOGY: "Study categorified deletion-contraction → Long exact sequence degenerates at k=4 → Import Khovanov techniques"
- Timeline bar: "Months 4-12"
- Each path is colour-coded (blue, violet, teal, gold)

SUB-PANEL G — "THE PENROSE EVALUATION VISUALIZED" (middle-right)
A detailed diagram of the Penrose evaluation on a specific small cubic graph:
- Draw a prism graph (or similar small planar cubic graph) with ~6 vertices
- Show one valid edge-3-colouring: edges labelled 1, 2, 3 with three distinct colours
- At each vertex, the three incident edges have all three labels → checkmark
- Show a second INVALID labelling: two edges at a vertex share a label → X
- Pen(G) = (number of valid labellings) shown as a count
- Caption: "Valid labelling = Tait colouring = 4-face-colouring. Petersen graph has ZERO (non-planar). Planar graphs always have some — that's the 4CT."

SUB-PANEL H — "PHASE 3: SYNTHESIS" (bottom-left)
Two proof assembly panels:
- "TQFT PROOF (if 2A or 2B succeeds):"
  1. "4CT ⟺ Pen(G) > 0 [Kauffman]"
  2. "Pen(G) = ⟨ψ_G|ψ_G⟩ [TQFT inner product]"
  3. "|ψ_G⟩ ≠ 0 [faithfulness on planar diagrams]"
  4. "Pen(G) = ||ψ_G||² > 0 [unitarity] ∎"
- "SHEAF PROOF (if 2C succeeds):"
  1. "Define F₄ on G [colouring sheaf]"
  2. "H¹(G, F₄) = 0 [vanishing theorem]"
  3. "χ(F₄) > 0 [Euler characteristic]"
  4. "H⁰ ≠ 0 → 4-colourings exist ∎"
- Timeline: "Months 12-24"

SUB-PANEL I — "PHASE 4: EXTENSIONS" (bottom-center)
Three extension icons:
- Globe icon: "Higher genus → Heawood conjecture: χ(G) ≤ ⌊(7+√(1+48g))/2⌋"
- Quantum icon: "Quantum chromatic number χ_q(G) for planar graphs"
- Physics icon: "Spin foams, Potts model, topological phases"
- Caption: "TQFT framework naturally extends beyond the plane"

SUB-PANEL J — "SUCCESS CRITERIA" (bottom strip)
Four medal icons:
- Bronze: "Pen(G) > 0 verified for all n ≤ 30" (Very High)
- Silver: "6j sign structure identified; H¹ = 0 for n ≤ 14" (High)
- Gold: "4CT proved via TQFT unitarity OR sheaf vanishing" (Medium-Low)
- Platinum: "Extended to Heawood conjecture via higher-genus TQFT" (Low)

CONNECTING ARROWS: A establishes the reformulation. B and C show the two main approaches (TQFT and Sheaf). D shows four independent paths. E is computation, F is theory, G is visualization, H is assembly, I is extensions. The flow: Reformulate (A) → Understand the framework (B,C) → Four parallel paths (D) → Compute (E) → Theorize (F) → Assemble (H) → Extend (I).

FOOTER: "Graph Colour Project — Plan 3 — February 2026" and "Key insight: Kauffman already proved 4CT ⟺ Pen(G) > 0. The reformulation exists. We only need to prove non-vanishing. Four independent paths — any one suffices."
```

---

## Usage Notes

1. Each prompt is fully self-contained — paste one at a time
2. The prompts share the same visual language (cream background, same colour palette, same typography rules) so the three images form a coherent series
3. Each image should be landscape orientation, detailed enough to read all text and notation
4. The sub-panels are the core content — ensure all are legible
5. Mathematical notation should use actual symbols (Σ, χ, ∀, ≤, ε, ψ, H¹) not LaTeX source
6. The connecting arrows between sub-panels are important for showing the logical flow of each plan
