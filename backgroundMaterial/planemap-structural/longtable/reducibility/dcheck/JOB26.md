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
