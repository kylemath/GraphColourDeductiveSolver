# Audit response and research postscript to the two plays

4 October 2026. This note accompanies the play; it does not rewrite its dialogue.

## What is now verified

One fresh dependency-ordered rebuild passed all 41 custom Lean sources and tests, including `DegreeFiveOutside` and its guarded axiom tests. The overlay excluded 493 cached custom artifacts. Every source hash agrees with `PlaneMapFourColorAudit.sha256` and was unchanged after compilation. The [audit manifest](../backgroundMaterial/planemap-structural/lean-source-audit.json) records each module and source hash; [compiler output](../backgroundMaterial/planemap-structural/lean-source-audit-output.txt) records the test diagnostics. This supersedes the earlier split 39-plus-2 rebuild description.

The final API `SphericalMap.finiteFourColorExtend` in `Mathlib/Combinatorics/SimpleGraph/PlaneMap/FiniteFourExtension.lean` takes a spherical map, executable adjacency, a vertex of degree at most four, and a proper deletion colouring. It finds its cyclic neighbour enumeration and obtains separation internally. Additional enumeration and separation arguments occur in lower-level helpers, not in this final API. The real remaining execution gap is the full degree-four spherical swap fixture, followed by executable deletion-carrier construction and recursive low-degree selection. No complete general solver is claimed.

## What the dialogue does and does not establish

The author's note identifies the project's own records as the technical source. The HTML supplies no independent evidence of an information leak.

The play's distinction between a cheap formula and an enumerated target-distance table is sound. A formula with a polynomial range only bounds solver work once a legal decreasing move exists at every required non-target state and that move can be found at bounded cost. A finite backtest can falsify such a formula; passing it cannot establish coverage.

The Catalan number 42 counts noncrossing partitions of five marked points. It does not count arbitrary interior component arrangements, nesting depths, or future Kempe actions. The existing observation already records the six boundary partitions. Bounded additional nesting data needs its own definition and sufficiency theorem. Colour pairs sharing a colour also share vertices, so the separation argument for disjoint colour pairs does not automatically apply to every pair of chains. A bounded number of observations alone neither gives a decreasing rank nor guarantees a common successful action for all represented states.

Likewise, total curvature 12 for a connected spherical triangulation supplies low-degree candidates, not roots with a Kempe progress theorem. The proved availability of six exterior degree-five roots makes selection possible but leaves goodness open. Since graph degrees stay fixed under Kempe swaps, a degree-charge formula alone is constant during recolouring. It needs additional state-dependent data to guide descent. Raw local indistinguishability only falsifies a selection rule that uses that specified local information; it cannot rule out every global root rule.

The statement that a potential is at least target distance needs a normalization: a nonnegative integer rank which decreases by at least one along selected moves bounds the length of that selected trajectory and therefore the shortest target distance. An arbitrary real-valued potential or unencoded lexicographic pair does not have that numeric implication.

## The next experiment

Use order 20, graph 36, root 8 as the primary adversarial fixture. Kittell and the icosahedron remain regression fixtures. The former is already repaired by the fixed exterior bit in the root-aware finite game; the latter reaches a target in at most one swap at every root.

Specify each proposed formula before reading target-distance tables. Name its graph class, allowable component swaps, proper-colouring invariant, integer range, and move-selection rule. Enumerate all 198 concrete colouring orbits of this fixture only to check that every non-target state has a decreasing move. Save a full colouring and all successor ranks for a local-minimum witness. Do not present another computed attractor as a structural formula.

If a formula survives, test it across the existing 118-graph corpus, then prove its decrease and range uniformly. If it fails, restrict or discard that formula explicitly. A failure is not a counterexample to four-colourability or to every Kempe class containing an extendible colouring.

## First formula: falsified on the primary fixture

We instantiated the potential proposal with `p = max(0, distinct boundary colours − 3)` and `q = Σ |K \ B|²`, summing over all six colour pairs and their components which meet the boundary. This is a formula on the concrete colouring, independent of target-distance tables. Component traversal evaluates it in linear graph time for the fixed six pairs; `q ≤ 6n²`. Compare `(p,q)` lexicographically. Proper colouring is the invariant; moves swap one whole bichromatic component, including components missing the boundary.

The [reproducible script](../backgroundMaterial/planemap-structural/component-mass.py) enumerates the 198 proper colouring orbits of graph 36 at root 8, verifies properness, move closure and reversibility, and checks every legal successor. Of 131 non-target orbits, three have no strict decreasing move. The [full witness](../backgroundMaterial/planemap-structural/component-mass-results.json) includes all three colourings and every move at the first witness. Its rank is `(1,190)`; successor ranks are only `(1,190)`, `(1,206)`, `(1,207)`, `(1,211)`, and `(1,228)`. An independent rerun reproduced the entire report. Thus this formula with strict single-swap descent is killed. It says nothing against macro moves, another formula, or the full quantified candidate. This formula is our concrete instantiation, not a theorem asserted by the dialogue.

Two research constraints in the play are optional: the canonical candidate allows polynomial-size state information, and enumerating a fixed four-swap macro has at most `(6n)^4` action sequences. Such enumeration may be costly and needs a coverage theorem, but is polynomial for fixed macro length. A bad root refutes a specified root rule; refuting existential root selection needs bad deletion-colouring witnesses at every eligible root.

General Four Colour, a polynomial solver bound, and triangulation completion remain unproved. The new rebuild strengthens verification of the foundations; it does not cross Gate D.

## Update after The Afternoon Call

The sequel correctly distinguishes confidence in a reachability statement from confidence in a structural proof or a polynomial solver. It acknowledges that the icosahedron is easy, that root availability does not prove goodness, and that a failed labelled selection rule does not exclude every structural rule. Its recursive-certificate proposal and triangulation-completion obligations remain relevant.

The author's note explicitly labels the nesting refinement, potential experiments including order-sixteen failures, and first-ring degree comparisons as invented. They are not independent replications and do not update empirical confidence. Their definitions and witnesses would be needed before inserting them as computed or killed findings in the navigator. “Only live shape” is too strong: failure of a particular observation also leaves alternative observations, memory and bounded macros open.

An independent replay answers the sequel's exterior-root question. There are eight eligible roots outside anchor 0's star in graph 36: `8,10,11,13,14,15,16,19`. Only root 8 loses the fixed sigma-plus-beta robust game. The other seven win entirely; the replay exactly matches the existing corpus. This rechecks existing evidence, not a new graph census. A selector must still recognize good roots without enumerating all colourings. Relabelling sensitivity also occurs in the fixed bit and boundary normalization, beyond smallest-label root choice alone.

A new bounded-macro check finds a decreasing two-swap sequence at each of our three component-mass local minima. Hence every non-target orbit of graph 36/root 8 decreases the same formula within two swaps. The [report](../backgroundMaterial/planemap-structural/afternoon-checks.json) stores the intermediate states and ranks; the [program](../backgroundMaterial/planemap-structural/afternoon-checks.py) replays both the exterior roots and this check without external Python packages. This does not reverse the strict single-swap failure. It motivates a precisely stated bounded-macro coverage candidate, whose uniform proof is absent. A fixed two-swap search and the integer rank `(6n²+1)p+q` would have polynomial cost/range if that coverage lemma held.

My qualitative judgments: targetless classes are less plausible in the searched finite range, but universal reachability is unproved. There is no new reachability evidence in the fictional afternoon experiments. Strict one-swap component-mass descent is false; its two-swap variant deserves a broader test. Full-state formulae and explicit recursive certificates remain viable research shapes with low confidence in a completed structural proof. No calibrated numerical probability of success follows from these tests, and polynomial complexity remains a separate obligation.

The [direct model-to-model response](AfternoonAgentResponse.md) gives the root table, the bounded-macro result, current judgments, and four questions about an explicit potential, topological information, a preserved certificate and edge-insertion filling. It is a handoff document; no external message has been sent.
