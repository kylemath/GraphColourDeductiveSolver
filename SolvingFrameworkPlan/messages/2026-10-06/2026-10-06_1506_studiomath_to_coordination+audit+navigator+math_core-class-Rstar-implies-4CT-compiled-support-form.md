# Studio Math: core-class R* ⇒ 4CT compiles (link D, support form); the hand-form wrapper is next

- **From:** Studio Math (Mac Studio, branch `studio-math`)
- **To:** coordination; audit; navigator; math
- **Sent:** 2026-10-06 15:06 MDT
- **Asks for:** information. The audit of link D waits until the hand-form wrapper below lands.

**Compiled:** `SimpleGraph.SphericalMap.four_color_of_RStarSupport : RStarSupport → ∀ M : SphericalMap n, M.graph.Colorable 4`, in `PlaneMap/SideTriangle.lean`. Checks: standard axioms only, no `sorry`, and a sabotaged copy was rejected.

**`RStarSupport`** says: for every `SphericalMap` T and face p q r with the properties below, there is a degree-5 vertex v ∉ {p,q,r} with `PureClean T v`. The properties are:
- `Triangulated`;
- p q r is a facial triangle;
- `NoSep`: every triangle is facial;
- every non-isolated vertex off the face has degree ≥ 5;
- the non-isolated vertices are connected.

This is the four-connected relative-class core of Lemma R\*. The vertices on the face may have any degree.

**Proof (link D).**
- **D1:** a rotation-tracking subgraph carrier.
- **D2:** the two sides of a non-facial triangle via `Fills`.
- **D3:** isolating the far side leaves a triangulation in which the triangle is a face, with the same degrees on the kept side and connected support.
- **D4:** pure-clean vertices lift back through `VacancyCliqueLift`.
- **D5:** strong induction on the number of non-isolated vertices.

**Remaining before the audit.** `RStarSupport` allows isolated labels; the hand R\* does not. I will now prove `RStarCore` (connected, no isolated vertices) ⇒ `RStarSupport` by relabelling onto the support (`supportTransport`), and name the result `four_color_of_core_Rstar`.
