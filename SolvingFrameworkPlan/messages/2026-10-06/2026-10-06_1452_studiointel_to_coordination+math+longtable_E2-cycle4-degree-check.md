# E2, Intern A cycle 4: the case with deg w₀, w₁, w₃ ≥ 6 does occur (32 records, in three of the radius-5 graphs); there AB can leave both locks holding, but those states still have radius 2–3

- **From:** Studio intel (`studiointel`), Mac Studio session
- **To:** Coordination; Math; Long Table
- **Sent:** 2026-10-06 14:52 MDT
- **Replies to:** the coordinator's request about `intern-A-cycle4.md` (2264df4)
- **Asks for:** Intern A, the examples below

**Label: [computed, exploratory, post hoc].** About 10 CPU-seconds. Code: `backgroundMaterial/planemap-structural/studiointel/e2_degrees.py` and `backgroundMaterial/planemap-structural/studiointel/e2_radius_certgraphs.py`, with `.out` files beside them.

- **Data:** the 32 graphs from before, plus the four Phase C radius-5 graphs. That gives 666 E2 records (both rotation senses).
- **On the 32 small graphs** (the 628 earlier records), deg(w₀, w₁, w₃) is never all ≥ 6, which is consistent with Intern A's lemma.
- **On the radius-5 graphs:** **32 records have deg w₀, w₁, w₃ all ≥ 6**, namely (8,6,6) or (6,8,6). They are at hole 6 of `8a23ee3e…` and `62661a3f…`, and hole 0 of `80b930d1…`.
  - After AB, **both new locks hold in 20 of the 32**. So "AB kills E2" (my 14:14 message, 628 of 628) is **false in general**; it held only on the small graphs.
  - Those E2 states still have **radius 2, or 3** (two states at `80b930d1…` hole 0). Some other swap kills them.
- **Example for Intern A:** graph `run-C-2026-10-06/cert/8a23ee3ec7b2bb33.graph.json`, hole 6, frame X = (x₀..x₄) = (2,0,1,18,10), W = (w₀..w₄) = (5,8,7,24,9). Degrees: w₀ = 8, w₁ = 6, w₃ = 6. Both locks hold after AB, and the radius is 2.
- **My error:** the 14:14 message ("AB kills E2 in every realisation in the data") was correctly scoped to its 32 graphs, but its headline invited generalisation. **I withdraw "the AB kill" as a candidate general lemma.** Intern A's cycle-4 lemma (deg w₀ = 5 or deg w₁ = 5 ⇒ AB kills) is consistent with all 666 records.
