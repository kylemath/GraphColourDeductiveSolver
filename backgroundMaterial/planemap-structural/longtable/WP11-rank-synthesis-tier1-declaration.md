# WP11 declaration (for review): rank synthesis, tier 1

Long Table, 4 October 2026. **For the math team's review. Nothing runs before their explicit go-ahead and the user's.** This answers the request in `2026-10-04-math-to-navigator-and-longtable-contact-complete.md`. Status words are the Proof Navigator's.

## Context

The math team's contact theorem (`four_color_of_empty_mass_region`, commits `1e4d990` and `a4a95dd`) reduces four-colourability, along this pathway, to the explicit hypothesis:

> every minimum-degree-five spherical triangulation T has a degree-five root r whose dead-end region is empty, for the mass rank R.

WP11 searches, within a declared finite family, for **alternative ranks** for which the same existential statement holds on the corpus. A surviving rank is a candidate replacement hypothesis. An infeasible tier is a certificate about **that tier only**.

## The model (fixed)

- **Graphs:** the existing Plantri minimum-degree-five triangulations. **Discovery uses orders 12–18 (22 graphs); the holdout is orders 19–20 (96 graphs), run once.** No orders beyond 20.
- **States:** at a root r, the proper four-colourings of T − r, taken up to global colour renaming. Features are colour-invariant (below), so this matches the math team's named-colour model state for state.
- **Moves:** exchange two colours on one whole bichromatic component, interior components included.
- **Macros:** at most two moves, with components recomputed after the first. Only the macro **endpoint** must decrease, and intermediate states may increase.
- **Targets:** states with p = 0 (at most three colours on B = N(r)).
- **Rank:** the lexicographic pair (p, s_w), where s_w = Σᵢ wᵢ·fᵢ. Targets are therefore below every non-target state.
- **Good_w(T, r):** every non-target state at r has a macro whose endpoint has a strictly smaller rank. By the math team's note, this is equivalent to an empty dead-end region for that rank in this model.

## Feature grammar G1 (frozen)

All features are non-negative integers computed in polynomial time from (T, r, c). All are **invariant under global colour permutation and under relabelling of T**: they are aggregates over unordered colour pairs, with no feature indexed by a named pair. ρ is the repeated boundary colour of c, and the singletons are the other three colours on B.

| Id | Feature | Definition |
|---|---|---|
| f1 | q | Σ over the six pairs and components K meeting B of \|K∖B\|² (the published mass) |
| f2 | lin | Σ over the same components of \|K∖B\| |
| f3 | L | The number of (singleton v, colour x ≠ c(v)) with v's {c(v),x}-component meeting B outside v. 0–9 |
| f4 | Lall | f3, counted over all five boundary vertices. 0–15 |
| f5 | links | The number of (pair, component) with \|K ∩ B\| ≥ 2 |
| f6 | shortLinks | The number of (pair, component) with \|K ∩ B\| ≥ 2 and \|K∖B\| = 0, i.e. links routed only through the boundary |
| f7 | repMass | f1 restricted to the three pairs containing ρ |
| f8 | hubToggles | The number of two-vertex bichromatic components containing a vertex outside N[r]. Lemma S bounds this by one per such vertex |

f1 to f7 are 0 at targets by convention, where ρ is undefined. f8 is defined everywhere.

## Tier 1 search space (frozen; finite)

| Sub-tier | Weights | Size |
|---|---|---|
| 1a | one feature, weight 1 | 8 |
| 1b | two features, weights in {1, 2, 3}² | 28 × 9 = 252 |
| 1c | any subset, weights in {0, 1}⁸, not all zero | 255 |

Each sub-tier is run completely; stopping at the first success is not allowed. Further tiers (larger weights, lexicographic triples, macro length 3) need a **new declaration**.

## Quantifiers (as requested)

- **Existential root, chosen before colourings.** For each w and each graph T, record whether ∃ r ∈ D(T) with Good_w(T, r). That is, ∀ T ∃ r ∀ non-target c ∃ macro decrease, with the root fixed before any colouring constraint is checked.
- **w passes discovery** if every discovery graph has such a root. It is **not** required that every root work. The all-roots statement is stronger and is reported separately.
- **Holdout:** each discovery survivor is evaluated once on orders 19–20, with no re-tuning.
- **A fitted root choice is not a selector.** The chosen roots are recorded as witnesses only. A uniform polynomial selector is a separate, unstarted obligation.

## Certificates (independently replayable)

Results are written as JSON, with input and checker hashes.

- **For a passing w**, per graph:
  - the chosen root r;
  - for every non-target state at r: the colouring, in the vertex order of T − r; its feature vector; and one witness macro, given as move 1 (colour pair, component vertex set), move 2 (same, or none), and the endpoint colouring with its feature vector.

  A replayer recomputes the components and features independently and checks legality and the lexicographic decrease.
- **For a failing w**, a witness graph T and, **for every** root r ∈ D(T): one stuck colouring at r, its feature vector, and the complete list of macro endpoints (each with move descriptions and feature vectors), none of them lower. A replayer recomputes the full macro neighbourhood and confirms there is no decrease.
- **For a whole tier:** the list of all w with their outcome and the pointer to each certificate.

**Infeasibility of a tier** means only that no w in that declared finite set, under this model and grammar, passes discovery. It says nothing about other features, larger weights, other macro lengths, or structural ranks in general.

## Implementation and replay

Long Table computes the features and runs the search with the `mass_core` code. **The math team, or a second implementation, replays every certificate** before any result is cited. Feature definitions are fixed here and will not change after the run starts.

## Expected cost and honest expectations

- **Cost:** the discovery range has about 6×10⁴ colouring orbits across 279 roots. Tier 1 totals 515 weight vectors, which should take minutes to hours in Python, since features and macro endpoints are precomputed once.
- **The published mass rank is close to 1a.** f1 alone, (p, q), passes discovery existentially; it already fails only at 6 roots, and never at all roots of a graph. So **tier 1 will trivially contain a survivor in the existential sense.** The informative outputs are therefore:
  1. which w also pass **every root** (the stronger, all-roots statement), giving a trap-free rank on the corpus;
  2. the full infeasibility map for the all-roots statement;
  3. holdout behaviour.

  We will report both quantifiers, keeping the existential one as primary, as requested.

---

## Version 2 amendments (after the math team's review; still not released)

This version responds to `2026-10-04-math-to-longtable-and-navigator-rank-synthesis-review.md`. Where they conflict, these amendments override the text above.

**Quantifiers.** The existential-root statement is **primary**; the all-roots statement is secondary. A surviving rank is its own conjecture. It is not new evidence for the original mass hypothesis, since (p, q) already survives existentially.

### 1. Certificates certify completeness, not only legality

The schema is `wp11-cert-v1`; see `wp11_cert.py` and the examples in `wp11-schema-examples/`.

- **Pass.** The certificate lists the chosen root, the full degree-five root set, and **every** canonical deletion-colouring state at that root, each with features, rank and, for non-targets, one witness macro. The replayer must independently:
  - enumerate the proper deletion colourings modulo global colour names and compare the exact state set;
  - derive the degree-five root set from the rotation;
  - recompute chain membership and properness after each move, with components recomputed between moves.
- **Two failure kinds, in separate fields:**
  - `all_roots_fail_witness`: one bad root, with one stuck colouring and its **complete** list of 1- and 2-move endpoints;
  - `existential_fail_witness`: **every** degree-five root, each with a stuck colouring and its complete endpoint list.

  The replayer recomputes every endpoint set independently and does not trust the supplied lists.
- **Registry and hashes:** graph ASCII and hash, producer hashes, and the frozen feature/weight registry, in every certificate.

### 2. What the colour quotient preserves

States **represent colour-permutation orbits**. The equivariance argument: a global colour permutation π maps each active {a,b}-component of c to the active {π(a),π(b)}-component of π∘c, and commutes with swapping it. It preserves p, every feature (all are aggregates over unordered pairs), and therefore the rank. The component recomputed after move 1 maps in the same way, so a macro and its decrease transport along π. Relabelling of T acts analogously (WP1, `InvarianceNote.md`).

**Moves are serialised in named-colour coordinates.** Move 1 acts on the listed start colouring; the intermediate is the raw named result; move 2 acts on that raw intermediate; the endpoint is raw, with its canonical form for identity. There is **no renaming between moves**.

**Regressions to add before release:** complementary-component and global-renaming checks, including the root-13 toggle case. The quotient-to-named-state bridge in Lean remains a formal obligation.

### 3. Feature counting, made precise

- **Active components.** A component is a connected component of the subgraph induced on vertices coloured a or b. Vertices of other colours are not part of it. f1, f2, f5, f6 and f7 count each active component once per unordered pair.
- **f6** counts a component that lies **entirely inside B** and has at least two boundary vertices. A component with a boundary-only path that also visits exterior vertices does not count.
- **f8** counts each two-vertex active component once per unordered pair, when at least one endpoint lies outside N[r], and once even when both do.
- **ρ:** at a non-target boundary, ρ is the uniquely repeated colour, and the singletons are the three singly occurring boundary vertices.
- **At targets:** f1 to f7 are 0 by convention, and f8 is still computed.

**Bounds**, with short proofs (components of one pair are disjoint and the boundary has 5 vertices):
- f1, f7 ≤ 6n² (per pair, Σ|K∖B|² ≤ (Σ|K|)² ≤ n²);
- f2 ≤ 6n;
- f3 ≤ 9;
- f4 ≤ 15;
- f5, f6 ≤ 12 (at most 2 components per pair meet B in ≥ 2 of the 5 vertices);
- f8 ≤ 3n (at most n/2 disjoint two-vertex components per pair).

With every weight ≤ 3, Q = 3(12n² + 9n + 48) bounds s_w, and the rank is represented by (Q + 1)p + s_w ≤ 2Q + 1. **This bounds the number of decreasing macros only conditionally on universal descent.** It says nothing about root selection or the cost of this search. The bounds will be checked in the implementation.

### 4. Validation and accounting

- **Orders 19–20 have been inspected in earlier research.** They are a fixed out-of-discovery validation pass, not unseen data. The **full survivor list is frozen before that pass**, and there is no re-tuning.
- **Duplicates:** the 515 sub-tier entries include duplicate and proportional vectors. Computation may be deduplicated, but the output preserves every declared sub-tier membership.
- **Infeasibility** is limited to this domain, quantifier and model. No broader conclusion follows.
- **If a rank survives,** the math team's plan applies: a generic ranked-macro contact wrapper, then formal bounds for that rank. It is never presented as a proof of the mass hypothesis.

**Release still requires** the math team's schema check and the user's explicit approval. Route B, the radius-3 and distant-hub searches, and orders beyond 20 remain unreleased.
