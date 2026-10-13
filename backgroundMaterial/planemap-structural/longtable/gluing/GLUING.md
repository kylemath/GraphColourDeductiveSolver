# Gluing-lock search: frame graphs with a separating 5-cycle

Long Table, MacBook, 13 Oct 2026.

**Status: exploratory adversarial search (Track A style).** The hypotheses and the reporting rule were written down
before any glued graph was evaluated. Nothing here is evidence for a theorem.

## Why

1. **A hand fact, not reviewed (projection lemma, `../twinhole/README.md`).** Glue two triangulations along a
   common cycle C. Every Kempe chain of the result, cut down to one side, is a union of whole chains of that side.
   - So gluing never unlocks anything.
   - Along a 4- or 5-cycle, chains can also merge through the other side, and that adds locks.
2. **Census fact, checked here (`sepcyc.c`, `sep-*.txt`).** None of the 80,131 frame-class graphs at orders 22–33
   has a separating 4-cycle or a nontrivial separating 5-cycle (one with at least 2 vertices on each side).
   - So the census evidence for R\*, the quarter floor, lock parity and NRC comes **only from internally
     6-connected graphs**.
   - The frame class (minimum degree 5, no separating triangle, no Occ of the diamond or of RSST 2.122) does not
     exclude separating 5-cycles.
   - A minimal counterexample to 4CT has none (Birkhoff).
3. **Why it matters.** Gluing is the operation that can only add locks, and it produces exactly the frame graphs
   the census never saw.
   - If the floor or R\* fails on glued frame graphs, then the formal target `BudgetUnionPos ⇒ floor ⇒ R* ⇒ 4CT`
     is mis-scoped as stated. The frame class must then also assume internal 6-connectivity, which Birkhoff's
     theorem supplies classically, though not yet in Lean.
   - If they hold, the evidence base widens to a structurally different family.

## Construction (`glue.py`)

T = (A − u) ∪_C (B − u′):
- A and B are census frame graphs; u ∈ A and u′ ∈ B are degree-5 vertices;
- the link of u is identified with the link of u′, in reversed order, with a shift s ∈ 0..4.

Properties of T:
- order n_A + n_B − 6;
- the link C becomes a separating 5-cycle whose vertices have degree ≥ 6;
- every T is passed through TrackB's `frame` filter, and only frame-class graphs are evaluated.

## Evaluation

`picyc --full` (local-runs/27 engine, census-validated on p33.r0#713 h0) at every degree-5 hole of T.

## Hypotheses (stated before running)

- **H1 (floor).** At every degree-5 hole of every glued frame graph, every Kempe class has F/N ≥ 1/4.
- **H2 (R\*).** Every glued frame graph has a degree-5 hole at which every class contains a filled state.
- **H3 (lock parity / NRC proxies).** No all-DL π-cycle sits in a class without filled states, i.e. no frozen class
  at any hole.

## Reporting rule

- Any hole with a class of F/N < 1/4 is reported with the graph, hole and class signature, and re-checked by a
  second engine before any claim.
- The same applies to any frozen class.
- Otherwise, report the minimum F/N over all holes and graphs, and the fraction of floor-tight classes, against the
  census (order 33: 8,556 floor-tight holes in 979,741).

## Budget

- MacBook only, `nice -n 10`, at most 2 processes.
- Pilot first: the order-22 graph glued to itself.

## Results (13 Oct 2026)

Engine: `picyc --full`. It is census-validated: on p33.r0#713 h0 it reproduces S = 5787 and F = 2898 exactly. Every
glued graph passed TrackB's `frame` filter (minimum degree 5, no separating triangle, occfree) before evaluation.
Correction to the construction above: the order is n_A + n_B − 7, not − 6.

| round | glued frame graphs | order | holes evaluated | min class F/N | floor-tight holes | frozen classes | positive π-cycles |
|---|---|---|---|---|---|---|---|
| pilot: p22 × p22, every u′ and shift | 60 | 37 | 1,260 | 0.452 | 0 | 0 | 0 |
| tight seeds (p27#8475, p28#218651, p28#44900) × p22, every u and shift | 205 | 42–43 | 4,105 | **0.2500** | 139 (3.4%) | 0 | 8 (max w = +4) |
| round 2: a second p22 patch at distance 2–3 from each tight hole (tight holes only) | 65 | 57 | — | **0.2500** | 16 graphs | 0 | 0 |

Readings:
- **H1, H2 and H3 survive.** No hole has a class below 1/4, no class is frozen, and R\* holds in every graph
  evaluated in full. Engine consistency flags (`cls_bad`, `f5_bad`, `cyc_split`) are 0 everywhere.
- **Gluing does push toward the floor.** Floor-tight holes are 3.4% of holes after one gluing, against 0.9% in the
  order-33 census (8,556 of 979,741).
- **Positive-winding π-cycles appear after gluing (orders 42–43)**, but only in giant classes (140k–170k states)
  whose total winding is about −25,000 to −31,000. Floor pressure lives in small zero-winding classes, positive
  winding lives in giant negative classes, and gluing never brought the two together.
- **Equality classes after gluing** have (size, F) in {(8,2), (16,4), (32,8), (92,23)}.
  - This kills the guess "every equality class is a 4-state block times a cube of free chains" (92 = 4 × 23).
  - It agrees with the census sizes 12, 16 and 24.

**Bottom line.** The floor and R\* hold on the first frame graphs with nontrivial separating 5-cycles that anyone
has evaluated (330 graphs, orders 37–57). The census-only scope caveat (orders 22–33: internally 6-connected only)
is real, but this search did not exploit it.

**Not done.** Gluing along separating 4-cycles; B ≠ p22; gluing near the positive-cycle holes; the order-34 list
(Studio only).
