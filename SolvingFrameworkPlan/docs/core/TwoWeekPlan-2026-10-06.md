# Official two-week plan (6–20 October 2026)

Adopted 6 October 2026, ~16:00 MDT, by the coordination session with the user's approval, after two outside consultations (`docs/working/SageAdvice-2026-10-06.md`, the Opus second sage, and the Fable sage's ten paths). Supersedes the routes table in `docs/core/MaximiseSuccessPlan.md` for the next two weeks.

## The reframing that drives everything

Given the Four Colour Theorem, **R\* at v holds if and only if deleting v creates no new Kempe class**: every Kempe class of 4-colourings of T − v contains the restriction of a colouring of T. Where T − v has a single class, the census only re-checks colourability. Calibration (Studio compute, orders 12–22): T − v has ≥ 2 classes in only ~3% of degree-5 hole instances; R\* held in all of them; no targetless class at degree 5, 6 or 7; the pipeline does detect targetless classes (torus control). **Only multi-class instances are evidence.** Lemma (Studio intel, unreviewed): no doubly locked state is frozen, so a stuck class must be a large class: searches enumerate classes, not states.

## Ten paths, ranked (value × chance, two weeks)

| # | Path | First step | Stop / go | Owner |
|---|---|---|---|---|
| 1 | **Class-count census**: κ(T − v), κ(T), radius stratified by κ | Orders 12–26 (running), radius-4/5 holes first | If multi-class holes are < 0.1% with no radius ≥ 4, say the census is non-evidential and move to path 3 | Studio compute |
| 10 | **Ship**: Lean library + theorem paper (honest κ caveat); send to Tilley | Freeze the statement list; audit the last pieces | None: ships regardless | Severn (paper), Studio Math (Lean), Audit; user sends |
| 3 | **Constructed multi-class instances / targeted counterexample** | Smallest Belcastro–Haas (dualised), Fisk, Mohar examples; Errera/Kittell gadgets in multi-class hosts; test every class of T − v | A stuck class is a paper; none across ~10⁴ multi-class holes is the first real evidence for Tilley | Studio Intel |
| 2 | **Controls**: degree-6/7 holes and edge contractions T/e: does any operation create a new class? | Degree-6 holes to order 22 (running) | New classes at degree 6 but never 5 → the ring-5 mechanism is the target; never anywhere → the cleaner conjecture "vertex deletion never creates classes" | Studio compute |
| 9 | **Structure of a hypothetical stuck class**: forced nesting of the blocking chains, ring-adjacent components | Machine-enumerate forced local patterns on the 1M states; prove the first two by hand | Three lemmas without shrinking the pattern space → stop | Math (lead), interns (hand), Studio Intel (patterns) |
| 8 | **Min-over-v radius ("R\*-radius")** and an unavoidable set of cheap certifiers | R\*-radius per order and on fullerene duals; classify the best vertex's local pattern | Min-over-v reaches 3 or patterns proliferate → stop | Studio compute (rider) |
| 4 | **Potential-function mining** | ~20 candidate Φ (connected bichromatic pairs, ring-meeting components, …) on the 1M states and radius-5 holes | No Φ works on radius-5 holes → stop | Studio Intel (rider) |
| 7 | **Fullerene-dual theorem** | Census of IPR fullerene duals to C100 (buckygen): radius, κ, localisation | Radius grows with n → stop; ≤ 4 with localised certificates → attempt the theorem | Studio Intel (IPR run continues) |
| 6 | **Moving vacancy** (hole as a 5th colour, Meyniel-type moves) | Radius with (5,a)-swaps on radius-5 holes; max simultaneous 5s | ≥ 4 vacancies ever needed → stop | Long Table (low priority) |
| 5 | **Sphere analogue of the Mohar–Salas invariant** (Tait: nowhere-zero Z₂² flows; a swap adds c·[C]) | Linear algebra on the three smallest multi-class examples | No separating functional in small cases → stop; **hard one-week stop** | Long Table (one agent) |

## Parallel workstreams

- **A (paths 1 + 2):** one measurement workstream, Studio compute. Until it is in, nothing in the census counts as evidence for R\*.
- **B (paths 3 + 9):** Studio Intel on constructed instances; Math and the interns on structure lemmas.
- **C (path 10):** ship regardless. Expert contact (Tilley; one reconfiguration expert) is the user's decision.
- **Riders:** paths 4, 7, 8 run unattended with their stop criteria; path 5 one agent, one week; path 6 low priority.

## Day-14 decision (20 October)

Continue proof attempts only if at least one holds: a potential with no local minima (path 4); a working extremal-choice rule (path 8); a structured family that looks provable (path 7); or a structure theorem that shrinks the search (path 9). Otherwise ship the paper and the library, and stop.

## Unchanged

Status words and bounties need the audit; exploratory runs on the Studio need no pre-registration; no new computation on the MacBook; nothing is posted outside the repository without the user's word.

— Coordination session
