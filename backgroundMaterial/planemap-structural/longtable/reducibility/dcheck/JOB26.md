# Job 26 (Studio): from "the 2-ball appears" to `ConfigOcc` [exploratory]

Pre-registration, written 2026-10-15 02:30 MDT. Target: 1 Dec 2026.

**Goal.** For a K = 1 key (2-ball of a degree-5 vertex v, with its degrees), go from "the 2-ball of v in T has this key",
in an internally 6-connected triangulation with minimum degree 5 (the notion the LP uses), to the per-key
`Occ T ring int` of `occ24/K<ii>.lean` (or its mirror). Then `colorable_of_occ_dred` (Job 24) applies.
Generalise `AppearsOcc`/`DiamondAppears` (diamond, 2.122) to all keys with one generic proof, not per-key case tables.

**Plan.**
1. Rotation walks: at a vertex of known degree d, the rotation lists d distinct neighbours (`orbitN`/`chain6` generalised).
   In a triangulation, consecutive entries are adjacent and give the `Nx` facts at both ends (`nx_tri`).
2. Build the 2-ball from v: the link x_1..x_5; at each x_k its rotation from v (privates and shared vertices); at each
   second-ring y its rotation (the ring vertices). This yields every `Nx` field of `Occ`.
3. Distinctness:
   - (a) interior vertices distinct (B2: no separating ≤ 4-cycles, no non-trivial separating 5-cycle);
   - (b) ring vertices distinct from the interior;
   - (c) **ring injective.**

**Central risk, found before starting.** (c) is false in general. In the icosahedron (internally 6-connected, minimum
degree 5), the 2-ball of a vertex is the vertex, its 5 neighbours and the 5 second neighbours, and its "ring" is the single
antipode. A coincidence `ring i = ring j` closes a cycle v–x–y–u–y'–x'–v of length 6, which internal 6-connectivity
allows. So "appears" does **not** imply an injective ring for radius-2 balls. B8 §8.0 already lists "the second ring is
simple" as assumed.

**H26.** Every non-injective ring of an appearing 2-ball forces T into a small, explicitly checkable family, or the
folded configuration is handled by a separate reduction (for example, D-reducibility of the folded ring, which identifies ring
positions). Every other appearance gives `Occ`.
**Kill.** Folded appearances of some deferred key in arbitrarily large internally 6-connected triangulations, with no
reduction for the folded case. Then the K ≤ 1 claim needs the LP to treat folded 2-balls as separate keys. Report this to
Long Table at once.

**First step.** Enumerate which ring identifications are geometrically possible for each key: which positions i, j can
coincide without creating a separating ≤ 5-cycle or a degree contradiction. If none can, (c) follows from B2.

## First finding (15 Oct): folding is geometrically possible, and it breaks the free-ring Kempe argument
- **Folding occurs in large internally 6-connected triangulations**, not only in the icosahedron. Take a third-neighbourhood
  vertex u adjacent to second-ring vertices y and y' on non-adjacent spokes x1, x3. This closes the 6-cycle
  v–x1–y–u–y'–x3–v, which separates x2 from x4, x5. No separating ≤ 5-cycle is forced. Gluing two large triangulated
  discs (minimum degree 5) along such a 6-cycle realises it. The free-completion ring then repeats u at two positions.
- **Pinched rings break the non-crossing lemma.** With u at ring positions i and j, the outside region is a disc whose
  boundary walk visits u twice. A Kempe chain of pair {a,b} with c(u) ∈ {a,b} can run from a position in (j, i) through u
  to a position in (i, j). A {c,d} chain (which avoids u) can then join two positions that alternate with it, without meeting it.
  So `chains_noncrossing` (`face_alternating_walks_meet` needs an injective ring) has no analogue, and a D-certificate
  for the free ring does not by itself reduce a folded appearance.
- How Gonthier handles this (`embed.v`, `embed_inj`, which uses `Birkhoff` and `chordless_perimeter`) is not yet understood
  here. Reading it is the next step: either his argument excludes folding for radius-2 kernels by a route we have missed,
  or his configurations' ring conditions (`good_ring_arity`) exclude it.

## Second finding (15 Oct): how Gonthier avoids the problem, and the route for Job 26
- Gonthier (`embed.v`) needs `embeddable` = simple perimeter + `good_ring_arity` (ring faces of arity 3..6) + `radius2`
  kernel. Our 2-balls satisfy all three. But his `embed_inj` is **injectivity on darts**, not on ring faces. Two configuration
  ring faces may land in one face of the counterexample, which is our fold. The perimeter stays a simple cycle of distinct
  edges (`scycle_embd_ring`, `ucycle_embr_ring`).
- His D-closure is on **edge traces** (colours of the perimeter edges, in the dual cubic map). His Kempe chains are
  edge-chains in the remainder, a disc bounded by a simple edge cycle. Their non-crossing therefore does not care whether ring
  vertices repeat. So D-reducibility stays valid for folded appearances.
- Our Lean soundness proof (R2) instead derives `KempeMatching` from **vertex** non-crossing (`chains_noncrossing`), which
  needs an injective ring (`RingFace.inj`), so it does not cover folded appearances. As shown above, the vertex statement is
  false for pinched rings. The *matching* statement `KempeMatching` itself should still hold, because the transitions are
  ring edges and are matched by dual chains.
- **Recommended route (B):** prove `KempeMatching` for a ring given as a face boundary *walk* (distinct darts, vertices may
  repeat), with transitions paired by edge-chains, via a dart/edge version of the face Jordan lemma. Then `Occ` needs only
  dart-level facts, not ring injectivity. Route (A), proving ring injectivity from minimal-counterexample properties, looks
  false in general (the 6-cycle fold).
- This decides whether H26 survives. Under (B), it does, with more work than planned.

## Route B (Long Table, 15 Oct), pre-registration
- **Target.** `KempeMatching` for the realised ring codes when the ring is a **face-boundary walk** of the deleted map
  (distinct darts, vertices may repeat), via a dart/edge version of the face Jordan lemma (transitions paired by edge
  chains, as in Gonthier). `Occ` then needs no ring injectivity, and every existing certificate applies. Due 1 Dec.
- **Kill / fallback.** If the dart-level face-Jordan lemma is not done by **20 Nov**, ship the simple-ring statement and put
  "the ring of the appearing 2-ball is simple" in the paper as an explicit hypothesis.
- Until then, the K ≤ 1 claim reads "appearances with a simple ring".

## Track 1 question: is the census key determined by the free 2-ball? **Yes** (hand argument; the Lean proof is Job 26 step 3a)
In a minimal counterexample (triangulated, minimum degree 5, no separating triangle, and the B2 theorem
`colorable_of_short_separating_cycle`), the *interior* of the 2-ball of a degree-5 vertex v (v, x1..x5, the second ring)
embeds injectively and as an induced subgraph. Only the third ring (the configuration's ring) can fold, and route B covers that.
- **Second-ring vertices are distinct.**
  - y (seen from x_i) = y' (seen from x_j) with x_i, x_j non-consecutive gives the 4-cycle v x_i y x_j, which has other
    x's on both sides. That is a separating 4-cycle, excluded.
  - With x_i, x_j consecutive, y is a third common neighbour of x_i, x_{i+1} besides v and s_i. That gives a non-facial,
    hence separating, triangle, excluded.
  - A second-ring vertex equal to some x_k likewise gives a short separating cycle or a degree contradiction.
- **No extra edges.**
  - A second-ring vertex adjacent to a non-owner x_j closes a triangle or 4-cycle through v that separates. Excluded.
  - A chord y ~ y'' of the second ring closes a 5-cycle v x_i y y'' x_j. A separating 5-cycle must bound a single vertex,
    which would be the x between them. But then that x has degree 5 with y, y'' as its shared neighbours, and y ~ y'' is a
    second-ring cycle edge, not a chord. Otherwise it is a 4-cycle or triangle case. Excluded.
- **Degrees are the true degrees in T**, which is what the key records.
- So the key read off T is exactly the free 2-ball's key, and the free completion differs from the embedded one only by
  identifications among third-ring vertices. Route B makes certificates sound under exactly those identifications.
  Therefore every sender in a minimal counterexample yields a census key whose certificate applies (once B lands).
  B8 §8.3 item 5's assumption "the second ring is simple and chordless" is a **consequence** of B2, not an extra
  assumption.

## Route B, refined by a hand analysis (15 Oct)
- **The vertex-level Kempe matching itself can fail for a pinched ring.** Example: ring positions 0..5 with u at 0 and 3.
  - Chains: an {a,b}-chain A through positions 1, u, 4, and a {c,d}-chain B joining positions 2 and 5. This is consistent
    with planarity: A reaches u through one sector and leaves through the other.
  - The only non-crossing pairing of transitions puts arc [3,4] alone in a region. Flipping that region would recolour u on
    one side only, so the flip is not proper. `KempeMatching` (realised codes of `T − K`) fails.
  - So route B cannot just "weaken the Jordan lemma".
- **What Gonthier really does.** His remainder map (the complement of the embedded disk *darts*) splits the pinched face u into
  its sectors. Remainder colourings may colour the sectors differently, and the Kempe closure is taken over that larger set.
  Consistency at u returns only when patching: a planar edge 3-colouring of the whole map always gives a face 4-colouring.
- **Faithful primal version.**
  1. **Unpinch:** split each pinch vertex u of the outside map `G'` into its sector copies, reusing isolated interior
     labels. The result `G''` has the configuration's face as a simple ring (`RingFace`), so `colorable`'s Kempe part
     (`kempeMatching`, R2) applies **unchanged**. A colouring of `G'` is a colouring of `G''`, so the starting code is realised.
  2. **Glue by potentials:** from the extending colouring of `G''` and the interior colouring λ (a colouring of the free
     completion), label every edge of T with the colour difference in (Z/2)². Every triangle of T is a triangle of `G''` or
     of the free completion, so the labels sum to 0 around every face.
  3. **Fills (coordinate-wise over ZMod 2)** gives a vertex function with those differences: a proper 4-colouring of T.
     Here the pinch identification is recovered by planarity, exactly as in Gonthier.
- **New pieces:**
  - (i) the (Z/2)² potential gluing lemma (general, moderate);
  - (ii) vertex splitting at a face pinch, as a `SphericalMap` with `Fills` (the main surgery; a pinch vertex is a cut
    vertex of `G'`);
  - (iii) the appearance → rotation-facts extraction (unchanged).
- The 20 Nov kill now applies to (ii) plus the extraction.

## Route B progress
- **(i) done (15 Oct)**: `FaceGlue.lean`. `cut_of_face_sums`: on a rotation system with `Fills`, a ZMod 2 edge labelling
  with zero sum around every face is `p u + p v`. The proof uses duality, not walks: the labelling annihilates the kernel
  of the incidence map, so it lies in the range of the dual map, by `range_dualMap_eq_dualAnnihilator_ker`. No
  connectivity is needed. `colouring_of_face_sums`: a nowhere-zero (ZMod 2)² labelling with zero face sums is the
  difference labelling of a proper 4-colouring. Axioms: propext, Classical.choice, Quot.sound.

## Check of route B step (ii), before formalising (16 Oct, hand analysis)
**As written, (ii) does not give a simple ring.**
- Let u be a pinch vertex at ring positions i < j. The two ring corners at u cut its rotation into sectors A
  (darts from ring_{i+1} round to ring_{j-1}) and B (ring_{j+1} round to ring_{i-1}).
- Splitting u into u_A, u_B keeps E, adds a vertex, and splits the configuration's face into two. So χ rises by 2,
  i.e. G'' = G''_A ⊔ G''_B (u is a cut vertex of G').
- Face of G''_A: u_A, ring_{i+1}, …, ring_{j-1}, a simple cycle of length j − i. Face of G''_B: u_B, ring_{j+1}, …,
  ring_{i-1}, length r − (j − i).
- The ring edges at position i lie in different components: (ring_{i-1}, u) is in B and (u, ring_{i+1}) is in A. So no
  simple length-r ring face exists in G'', and the configuration cannot be glued back to G'' as one disc.

**What does hold (usable pieces).**
- Each component has a simple ring face, so `chains_noncrossing` and the vertex Jordan lemma apply **per component**.
  The A-chains give a non-crossing matching of the A-arc transitions; likewise B.
  - A union of matchings within two complementary arcs is non-crossing on the whole r-cycle.
- Colourings of G'' are colourings of G' with B translated independently by t ∈ (Z/2)², a colour permutation of B.
  Normalising t so that κ(u_B) = κ(u_A) recovers exactly the G' codes (c_i = c_j).
- Gluing (i) works in **trace** form, as in Gonthier.
  - The ring-edge differences of a G'' colouring sum to 0 on each arc separately.
  - The interior λ must have the same trace. That forces λ(ring_i) = λ(ring_j), which holds when λ extends a code
    with c_i = c_j.
- **The gap.** After a Kempe flip in A that recolours u_A, B must be re-translated: equivalently, flip every chain of B.
  The combined effect on the r-ring code is "flip the A-outer region plus positions i and j, and flip all of B".
  - With the union matching, this is not obviously a union of combined-matching regions: positions i and j sit in
    the outer region with both A-outer and B-outer.
  - So it is not yet shown that `KempeMatching` (R2's closure semantics, vertex codes) holds for pinched appearances,
    even granted (i) and the split.

**Options (for Long Table).**
- (B1, recommended) The original route B: KempeMatching for the pinched face of G' **directly**, with no split.
  - For a pair partition {a,b}|{c,d}, the transitions are the ring edges whose ends are in different classes. They
    are matched by the class-boundary curves: Tait 2-colour chains in the dual of G' of the two colours other than
    a + b.
  - These are disjoint curves in the disc bounded by the configuration's face, which is a simple *edge* cycle even
    when vertices repeat. So they are non-crossing, by a dual/dart Jordan lemma.
  - Flips act on actual vertices of G', so a code keeps c_i = c_j. The glue to the free completion λ is then plain
    vertex gluing, because λ(ring_i) = λ(ring_j) = κ(u). (i) is not needed on this route; it stays as a general tool.
  - The new piece is the dart-level Jordan lemma for a face-boundary walk.
- (B2) The split route (ii) plus a per-component vertex Jordan lemma. It works only if R2's closure step accepts the
  combined "flip in A, re-translate B" moves. A cheap brute-force test of the closure semantics on the D keys would
  decide it before any Lean work.
- (B3) The kill route: ship the simple-ring statement, with the fold as an explicit hypothesis.

### Update (16 Oct, after reading R2's closure semantics): (B2) works, and (ii) is just "keep one side"
- In `Good`/`KempeMatching` (DCheckSound.lean) a flip XORs θ onto **every** position of the chosen regions:
  `flipMask`, both classes at once. That is the trace-compatible move, not a one-class Kempe swap.
- **Hand proof that the pinched case reduces to the two components.**
  - Let k be realised by κ on G' = A ∪_u B (u at ring positions i, j). The restrictions realise the two arc codes;
    in each, u_A (resp. u_B) is the single position i ≡ j.
  - Per-component KempeMatching gives matchings lab_A and lab_B. Their union is a non-crossing matching of all
    transitions, because the chords lie in complementary arcs.
  - Its regions are the A-inner regions, the B-inner regions, and one outer region = (A's region at u_A) ∪
    (B's region at u_B) ∪ {i, j}.
  - For any region set S, flip the corresponding A-regions and B-regions, with the outer one in both or in neither.
    The flipped codes give u_A and u_B the same colour, k_i ⊕ (θ if outer ∈ S).
  - So the two colourings glue at u to a colouring of G' realising k ⊕ flipMask(S). Hence KempeMatching(G') follows
    from KempeMatching(A) and KempeMatching(B).
  - Higher multiplicity and several pinches follow by induction on the number of pinch splits.
  - Needed: the merged labelling must be the table's labelling of that matching (`matchTable_complete`, R1), with s
    translated to the table's region numbering.
- **(ii) needs no new surgery.** A = G' with every vertex on B's side of u deleted. Then u's rotation restricts to sector
  A, and the face becomes u, ring_{i+1}, …, ring_{j-1}. Use vertex deletion preserving `Fills` plus the face tracking from
  Job 25 (`subgraph_tracked`, `keepC`/`OnSide`).
- **(i) is not needed on this route.** The glue to λ is vertex gluing, since u is one vertex of T and λ(ring_i) =
  λ(ring_j).
- **Revised plan.**
  - (ii′) A pinch makes u a cut vertex of G'. Keeping one side gives a SphericalMap with a simple RingFace on the arc.
  - (iv) The combinatorial merge lemma (KempeMatching from the two arcs; pure code arithmetic plus R1).
  - (iii) The extraction, unchanged.

### B2 brute-force test (16 Oct; `job26/pinch_km.py`, `job26/pinch_km.out`)
- **Method.** For outside maps G' = A ∪_u B, two triangulated discs sharing the pinch vertex u, so the ring walk visits u
  twice:
  - enumerate every proper 4-colouring;
  - check R2's `KempeMatching` exactly. For every realised code and θ with transitions, some non-crossing matching
    must have every union of its regions (XOR θ) still realised.
- **Pinched cases: 0 failures.** 4w+4w (ring 8), 3f+5w (8), 5two+4w (9), 5two+5two (10) and 4f+4f (8, no
  interior): 28,608 (code, θ) pairs in all. The simple-ring controls (6- and 8-wheels) also have 0 failures.
- **Negative controls fail, so the test has teeth:** outside maps with crossing chords (not planar with the ring as a
  face) give 96 / 1,464 and 384 / 10,656 failures.
- The icosahedron is vacuous: its ring is the single antipode, so codes are constant and have no transitions.
- **Reading.** KempeMatching (vertex codes, XOR-θ flips) holds for pinched rings, which is the statement B1 must prove.
  This agrees with the hand proof above. It is a sanity check, not a proof.

### Sharper (16 Oct): `RingNC` itself holds for the pinched walk, so no merge lemma is needed (`job26/pinch_nc.py`, `.out`)
- `RingNC G r ρ` (DCheckRingNC.lean) does **not** require ρ to be injective. Its fields are the chain non-crossing
  statements `nc` and `ncs`, by ring index. `RingNC.kempeMatching` (DCheckRingKempe.lean) then gives KempeMatching with
  no injectivity anywhere.
- **Brute force on G' itself** (chains of G', positions i and j both u). For every proper colouring, RingKempe's
  `hNC` and the pairGraph forms `nc`/`ncs` were checked on pinched maps 4w+4w, 3f+5w, 5two+4w and 4f+4f (ring 8–9):
  **0 violations**. The crossing-chord control has 384, so the test has teeth.
- **Correction to the first finding (15 Oct).** The example "an {a,b} chain through 1, u, 4 and a {c,d} chain joining
  2 and 5" cannot occur. u is a cut vertex of G', so any chain from side A to side B passes through u, and a {c,d}
  chain cannot contain the {a,b}-coloured u.
- **Hand proof sketch of `nc` for the pinched walk.**
  - Take i < j < k < l, with chain 1 joining positions i and k and a disjoint-pair chain 2 joining j and l.
  - At most one of the two chains contains u, so the other lies inside one side X.
  - Then j, k, l (or i, j, k) lie in X's arc. The part of chain 1 inside X runs from its X-endpoint to u, entered
    at the first visit (the cut-vertex property).
  - In X's simple ring, u sits at position 0, so the crossing becomes a crossing in X. That contradicts X's own
    `RingNC` (from its RingFace).
  - `ncs` is the same with the same-pair bookkeeping.
- **Plan, final.**
  - (ii′) Keep one side of the pinch: G'_X is a SphericalMap with a simple RingFace on the arc, so `RingNC` holds by
    the existing bridge.
  - (iv′) `RingNC` for the pinched walk, from `RingNC` of both sides plus the cut-vertex property. This is pure graph
    reachability, no planarity.
  - Then `RingNC.kempeMatching` applies verbatim.
  - Several pinches: induct on the splits.
  - (iii) The extraction, unchanged.
