# Step (c), decomposition: chordless hierarchies. Results from a 90-minute probe

22 Oct 2026. Code: `hier.py` (top-down splitter, exhaustive splitter, generators, separating-cycle counts), `grow.py` (lopsided growth), `e1_hier.py` (test suite, writes `e1_hier_L40.jsonl` and `e1_L40.log`), and the scratch tests `t1.py`–`t5.py` (`t3.py` is the hexagon test). Labels: [P] proved here, [M] measured, [C] conjecture. "Chordless" means the boundary is induced **in G**, which is stricter than `lev.chords`, since that only counts chords inside the disc.

## Numbers first

| test | result |
|---|---|
| Flat hexagonal patches (BFS balls in the 6-regular part of ico20), radius 1, 2, 3, 4: 7, 19, 37, 61 vertices. All are chordless discs. | **No split into two chordless discs exists** [M]. Radius 1–2: exhaustive over all 2^18 partitions. Radius 3–4: Lemma 1 below leaves only face peels, and all of them were tested: 0 valid. At radius 6 (127 vertices), 12 face peels are valid. |
| Top-down harmonic splitter, leaf bound L = 12, ico10 (n = 1,002) | 103 of 106 splits were bad. Once one chord appears it persists in the descendants. |
| Same splitter with reflex-aware transitions (Lemma 1), L = 40. Maps: ico5, ico10, flip10 (degrees 5–9), drum30_10 (two hubs of degree 30), glue5_5_5 (nested separating triangles), BASE_defect_ico17 (n = 2,892), ico20 (n = 4,002) | **Fully chordless hierarchy found in 0 of 13 runs.** Primary failures (a chordless node with no chordless split found): 2–9 per map at n ≤ 1,002, 22–25 on defect_ico17, 38 on ico20. Bad splits carried 1–35 chords; most carried 1–3. Max leaf size reached 34–136, and up to 288 on glue, because nodes with no disc split were left as leaves. One ico20 run crashed (no evaluable candidate). BASE_rand22 had not finished. |
| Lopsided growth (one disc absorbing faces, diamonds or partial wheels) | Stuck at step 1 on ico5 and ico10 (2 of 2 seeds each). Seeded with a face or a 7-vertex wheel, no candidate piece extends the seed to a chordless disc. |
| Earlier data (`levelling/chordsplit.jsonl`): the 19 chordful clusters on which re-levelling failed, cut along all chords | In 19 of 19, every chordless piece is 1-level (up to 56 pieces each). |

Nothing reached 10k vertices with a chordless hierarchy. The failure is structural, not a matter of scale; see below.

## What the obstruction is

**Lemma 1 (transition lemma) [P].** Let U be a chordless disc with boundary C, and U = A ⊔ B with A and B chordless discs whose boundaries both have length ≥ 4. Then A∩C and B∩C are complementary arcs. At each of the two transition edges ab of C (a ∈ A, b ∈ B), let z be the apex of the U-face on ab.
- If z ∈ A, then d_U(b) ≥ 5 and d_U(a) ≥ 4.
- Symmetrically, if z ∈ B, then d_U(a) ≥ 5 and d_U(b) ≥ 4.

*Proof.* A boundary vertex of a chordless disc X with |∂X| ≥ 4 has X-degree ≥ 3; X-degree 2 would make its two neighbours adjacent, which is a chord. If z ∈ A, then b loses a and z, and a loses b. ∎

The arcs are complementary because a second arc of A∩C would disconnect B.

**Gauss–Bonnet identity [P].** For a near-triangulated disc, Σ_{v∈C}(4 − d_U(v)) + Σ_{v interior}(6 − d(v)) = 6. Call a boundary vertex with d_U ≥ 5 *reflex*.

**Corollary [P].** Suppose U is chordless and has no reflex boundary vertex, i.e. it is *convex*. Then the only possible splits peel off a disc bounded by a triangle. If G has no separating triangle, that disc is a single face. Flat hexagons of radius 1–4 admit no valid face peel either, so they are **dead ends** [M].

Consequences:
- **(c) cannot be proved greedily** in the form "every large chordless disc splits into two chordless discs": that statement is false [M].
- A hierarchy must avoid producing convex internal nodes larger than L. Every split also *consumes* reflex vertices at its two transitions. So the seams have to create new reflex vertices on both sides, which means they must zigzag.
- Harmonic level-set seams are nearly straight, and growth from a round seed makes round, convex discs. That is exactly why both constructors die.
- The difficulty is **flatness**: 6-regular patches of domes and internally 6-connected maps. Separating short cycles and high degrees are not the problem. Degree-7 vertices inside a disc make Σ_C(d_U − 4) more negative, i.e. more convex. Degree-5 vertices make it more reflex.

**Hypotheses on G.** Lemma 1 holds in any triangulation. The corollary's "only face peels" needs no separating triangles. A minimal counterexample is internally 6-connected: 5-connected, and its only separating 5-cycles are vertex links. That rules out separating 3- and 4-cycles. It does **not** help with the obstruction above, because flat hexagonal patches are internally 6-connected. On the obstructions the task listed:
- **Separating triangles** are harmless in principle: put the triangle-bounded disc in as one subtree. On glue5_5_5 they caused only 2 bad splits (1 chord each).
- **High-degree hubs:** a wheel W_d is a chordless disc with no split at all [P], since one side would be a set of rim vertices with no triangle. So a hub of degree d forces the smallest node containing it in its interior to come from a careful merge. Drum30_10 failed 4 times per run [M].

## Is (c) true? (calibrated)

- [C, about 55%] Every min-degree-5 triangulation has a chordless hierarchy with leaves of size O(1), but only with *designed* seams that keep reflex vertices on both sides.
- Leaves would need to hold at least whatever bounded dead ends cannot be avoided. Nothing tested here rules out leaves of size about 20–60.
- My constructors are not evidence against (c). They are evidence that (c) is a delicate *shape* condition. It is not a connectivity condition.
- [C, about 30%] Balanced chordless hierarchies with leaves ≤ 12 exist.

## Weakening (step 3)

**W1: cut along chords.** Allow merges whose union U has chords. Treat U as the tree of its chordless pockets glued at chord edges. Levelness is required only of each pocket. A 2-vertex seam (the chord) is connected, so one renaming fixes it.
- Existing evidence: 19 of 19 chordful failure clusters split into all-level pockets [M].
- **Not tested here:** I ran out of time before running merge/collar re-levelling (`lev.merge`, `relevel`) with W1, so whether R stays ≤ 1–2 is open.
- With W1, (c) becomes easy [P sketch]: any hierarchy of discs works, e.g. the Voronoi hierarchy already used.
- The cost moves into (a): a merge must now keep each pocket level, and pockets can be thin.

**W2: bounded chords per merge.** Observed bad splits carry 1–3 chords typically, at most 35. I would not adopt W2 without a seam design that bounds this.

## Proof ideas

1. [P] Lemma 1 and the Gauss–Bonnet identity: necessary local conditions at the transitions.
2. [C] **Reflex-budget induction.** Define a potential r(U) = number of reflex boundary vertices. Show that from r(U) ≥ 4 and |U| > L one can choose a zigzag seam such that both children have r ≥ 4.
   - In a flat region this is a lattice-path construction: a seam alternating its turning gives each side reflex vertices.
   - Curvature (degree-5/7 vertices) only shifts the budget by Σ(6 − d) over the interior.
   - This looks provable for bounded degree. Unbounded degree needs separate handling of hubs, e.g. a hub always sits on a zigzag of its own.
3. [C] **Top-down by induced cycles.** Choose the root split along an induced cycle that zigzags. Split each child along induced paths between reflex boundary vertices, keeping the induced path at distance ≥ 2 from C except near its ends, which prevents chords to C.
   - The failing cases here were seams running parallel to C at distance 1, and ears at transitions. Both are exactly what this rule forbids.

**Bottom line:** (c) in its literal form is not established. The naive constructors fail for an identified reason: convex chordless discs are dead ends (Lemma 1 and the hexagon data). The most promising routes are a reflex-budget zigzag construction [C], or switching to W1, where the merge step remains to be tested.
