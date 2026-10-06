# R* by selection: what an unavoidable-set argument needs, and the Tilley link (Long Table, 6 Oct 2026, about 15:10 MDT)

[hand] reasoning by Long Table, nothing computed. Citations marked "verify" have not been rechecked against the source. Statuses are quoted from Navigator revisions 122–130 and the messages named. The Navigator owns them.

## 1. The selection form of R*

R* asks for one pure-clean degree-5 vertex per core triangulation. A selection proof has two halves:
- **(U)** an unavoidable list 𝓛 of configurations: every core triangulation contains a degree-5 vertex whose surroundings match an item of 𝓛;
- **(C)** for each item of 𝓛, a proof that the vertex is pure-clean.

(U) is a discharging argument from Σ(6 − d) = 12. (C) is a fill proof.

## 2. Where (C) stands, by hole type

| Hole type (link degrees) | Status of (C) | Source |
|---|---|---|
| a neighbour of degree ≤ 4 | clean, ≤ 3 pure swaps | ledger; not in the core class (min degree 5), but relevant to the relative class |
| (5,5,5,5,5) | clean, radius ≤ 3: Theorem H | compiled and audited (14:19 studiomath; 14:53 focus orders) |
| (5,5,5,5,d), any d | clean, radius ≤ 6: Theorem HP | compiled and audited (same) |
| exactly two neighbours of degree ≥ 6: (5,5,5,6,6), (5,5,6,5,6) | **open**. No local bound from HP's moves; closed obstruction sets of 20 and 28 states (Math 14:10). E2 after AB is reduced to one statement about two P-paths (Long Table, `e2-ab-tait-reduction.md`) | hand, unreviewed |
| three or more neighbours of degree ≥ 6, including (6⁵) | **open**. As a 2-ball, every sequence with three or more 6s fails (Math 13:03, exploratory). (6⁵) radius reaches 4 at order 28 | Six-Ring Trap; Math 12:18 |

## 3. (U) cannot avoid the open rows

- **(6⁵) is unavoidable as a hole type.** The pentakis dodecahedron (order 32, min degree 5) has only (6⁵) holes. So 𝓛 needs an item that occurs there, and Math's 2-ball result says no 2-ball item with three or more 6s is clean. **So 𝓛 must contain configurations larger than a 2-ball around a degree-5 vertex.** In the pentakis case, the next step is a pair of degree-5 vertices at distance 2 with their common degree-6 neighbour.
- **Bounded-degree items are not enough.** In the belt G_n every degree-5 vertex has a neighbour of degree n (audit 1240; the "bound all five link degrees" kill). So 𝓛 needs items with one unbounded-degree vertex. The compiled unequal-pole belt walk and Theorem P are the models.
- **Classical light-vertex theorems do not help.** Wernicke (1904) and Franklin (1922; verify the exact statement) force a degree-5 vertex with one or two neighbours of degree ≤ 6. The other neighbours are unbounded, so those classes contain the open rows.

**Conclusion [hand].** A selection proof of R* is an unavoidable set of configurations with rings well beyond 5, each proved pure-clean (vacancy-reducible), plus a discharging argument. Structurally that is the Appel–Haken / RSST plan [cited], with our pure-swap cleanness in place of D- or C-reducibility. RSST needed 633 configurations with rings up to 14, and 32 discharging rules, checked by computer [cited, verify numbers].
- **Possible advantage:** our swaps act on the whole graph, not only through a ring, so some configurations that are not D-reducible might still be pure-clean, and 𝓛 might be smaller.
- **Cost:** there is no reason to expect it to be small enough to do by hand.

## 4. The Tilley link, made exact where possible

- **[hand, from `literature-check.md`]** At a degree-5 vertex x with apex neighbour y, T*_τ = T/xy. A Tilley Kempe sequence that separates x from y gives a pure fill at x.
- **[hand, new]** Let K be a targetless class at a degree-5 vertex v. Every state s ∈ K is doubly locked, with three singleton link vertices m, a and b. For y ∈ {m, a, b}, colouring v with c(y) gives a 4-colouring of T − vy with c(v) = c(y). By the previous point, **in that colouring no Kempe sequence separates v from y**, for each of the three edges vm, va and vb. So a targetless class gives Kempe-locked *classes* at three edges at v. That is weaker than Tilley's Kempe-locked *triangulation*, which needs every colouring of T − vy.
- **What follows.** Tilley's conjecture (a Birkhoff diamond is necessary for Kempe-locking; verify) is about all colourings, so it does not apply to a single class. In a *minimum counterexample*, Tilley proves Kempe-locking at every edge [cited]. With his conjecture and the reducibility of the diamond, that already gives the Four Colour Theorem. This is his "double agent" remark. So the Tilley route does not need R* at all. R* is a parallel, per-class strengthening. **Our framework gives nothing extra on the Tilley route unless "targetless class at v" can be upgraded to "every colouring of T − vy is locked", which is false in general:** our data have locked classes alongside fillable ones in the same graph.

## 5. What this means for front 1

- The open rows of §2 cannot be selected away. Front 1 has to prove (C) for hole types that include radius-4 and radius-5 states, or use larger configurations.
- The most useful hand target is still Math's: the two-degree-6 classes. A proof there would be a real theorem, a large-ring analogue of Theorem HP, even though it would not close R*.
- Proposed next step for Long Table, if the coordinator agrees: write the **smallest larger configuration for the pentakis case** (two degree-5 vertices at distance 2 through a degree-6 vertex, all other neighbours of degree 6). Ask Math whether its D-reducibility game can test it as a ring configuration. That is one computation on the Studio, as a kill test.
