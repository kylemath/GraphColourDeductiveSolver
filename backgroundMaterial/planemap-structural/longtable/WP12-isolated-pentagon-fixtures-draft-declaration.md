# WP12 draft declaration (unreleased): isolated degree-five roots on named symmetric fixtures

Long Table, 4 October 2026. **Draft for the math team's review and the user's decision. Nothing has run.** It concerns graphs beyond order 20, which are outside every current release. Status words are the Proof Navigator's.

## Why: a coverage gap in the corpus

The fact comes from the replayed WP11 discovery data (orders 12–18; graph structure only).

- Classify each degree-five root by the degrees of its five neighbours as (number of degree 5, number of degree 6, number of degree ≥ 7).
- In all 279 discovery roots, **every root has at least two degree-five neighbours.** The types seen are (5,0,0), (4,1,0), (4,0,1), (3,2,0), (3,1,1), (3,0,2), (2,3,0) and (2,2,1).
- Under lin, all 247 roots outside type (2,3,0) are good; type (2,3,0) has 30 good and 2 bad (order 17, graph 0, roots 4 and 6). Under q, the bad roots fall in types (2,3,0), (3,2,0) and (5,0,0).

The root type **(0,5,0)**, a degree-five vertex all of whose neighbours have degree six, does not occur. Among large minimum-degree-five triangulations with degrees 5 and 6 only, it is the generic type: once the twelve degree-five vertices are isolated, it is the only type. A rank or receiver condition fitted through order 20 has therefore never met the regime that dominates at scale. A local-degree receiver condition such as "at most two degree-six neighbours" has no member there.

(The counts of these types on orders 19–20 are graph-only facts. They will be added after the WP11 validation output is frozen, so that file is not touched mid-run.)

## Fixtures (named, symmetric, finite)

| id | graph | order | degree-five roots | root type |
|---|---|---|---|---|
| F32 | pentakis dodecahedron (dual of the truncated icosahedron C60) | 32 | 12, all in one automorphism orbit | (0,5,0) |
| F42 | geodesic icosahedron, class (2,0) (dual of the chamfered dodecahedron) | 42 | 12, all in one orbit | (0,5,0) |

The rotation systems will be built by a committed script and validated as simple spherical triangulations by `mass_core.validate_triangulation`. The orbit claim will be checked from the computed automorphism group, as in `automorphisms.py`. Since all roots lie in one orbit, **the existential and all-roots statements coincide** on each fixture: one root decides both.

## Test (frozen before any run)

- **Ranks:** q, the published mass rank (Gate D's rank), plus the WP11 discovery existential-survivor list frozen at digest `ef80b32e…`. If the WP11 validation pass has completed and been replayed by then, the list is restricted to its validated survivors. No new vectors and no tuning.
- **Model:** unchanged from WP11 (two-swap macros, whole active components, endpoint decrease, p = 0 targets).
- **Output:** the WP11 indexed-certificate format, one table per fixture at one root, with the automorphism-orbit certificate.
- **Reported facts:** for each rank, good or bad at the fixture root, with a stuck-state witness when bad.

## Expected cost (not measured; measuring needs the release)

The deletion graph has 31 or 41 vertices. The number of colouring orbits is unknown; it could exceed 10⁵ on F32 and 10⁶ on F42, with about 100–250 endpoints per hard state. The current pure-Python producer may need hours for F32 and may be impractical for F42 without a faster enumerator. If F42 proves infeasible, F32 alone is the declared minimum; this will be reported, not tuned around.

## What it can and cannot show

- **A bad root for q on F32 or F42** would be an existential counterexample to the Gate-D hypothesis for the mass rank on that graph, and similarly for any survivor. This is the sharp adversarial use.
- **A good root** is one more fixture, not evidence of universality.
- Whatever the outcome, there is no claim about other large triangulations.

## Needed before any run

- The math team's review of the fixtures, quantifiers and output format.
- **An explicit release by the user,** since this is beyond order 20.
- The WP11 validation outcome, which fixes the survivor list used here.
