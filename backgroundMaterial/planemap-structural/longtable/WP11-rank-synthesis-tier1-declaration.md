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
