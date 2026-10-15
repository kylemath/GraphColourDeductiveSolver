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
