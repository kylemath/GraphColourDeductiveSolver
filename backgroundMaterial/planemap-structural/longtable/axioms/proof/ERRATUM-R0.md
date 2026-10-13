# Erratum: Conjecture R0 is false (13 Oct 2026)

Conjecture R0 (PROOF-ATTEMPT-1.md §2, R0-ATTEMPT-1.md) says that a simple plane graph has no closed walk of the
perfect-matching digraph D through a Hamiltonian arc. Here D has an arc M → M′ when M and M′ are disjoint and
k(M′) = k(M) − 2. The conjecture is **false**.

## Counterexample

**Found by** Studio Job 5 (`axioms/studio/dcyc.cpp`, census scan). The witness is
`axioms/studio/out/R0_counterexample_p27_4710_h14.json`, in the Studio's commit.

**The graph:** the Tait dual of the order-27 census frame triangulation p27#4710 (`Census29/out/frame-27.txt`),
taken at its degree-5 hole 14. The dual has n = 46 vertices and is plane by construction.

**What it contains:** D has a cyclic strongly connected component of size 10, girth 10, with 2 Hamiltonian arcs.

**Independent check (MacBook, `r0_counterexample_check.py`):** own perfect-matching enumeration; same numbers as
the Studio's three codes:

| quantity | value |
|---|---|
| perfect matchings | 1,336 |
| arcs | 631 |
| Hamiltonian arcs | 123 |
| cyclic SCCs | 1, of size 10 |
| Hamiltonian arcs inside it | 2 |

## Why it does not touch NRC

At 7 of the 10 states, E − M_t is **disconnected** (2–3 components), so it is not a DL figure-eight. The cycle is
therefore not a Q-run or a near-rigid π-cycle. R0 dropped the connectivity of E − M, and R0-ATTEMPT-1's type lemma
had already noted that R0 differs from NRC exactly by extra cycles in Q_t. NRC stands: the census has NRcyc = 0 at
every hole up to order 34, and the planar windows with figure-eight connectivity are UNSAT up to n = 24.

## What survives

- Lemma E (the Tait sign sum moves by 4 mod 8 per step in the plane, so L ≡ 0 mod 10) still holds; it was proved
  for D-steps in the plane.
- The census statement "D is acyclic for planar Hamiltonian normal forms with n ≤ 20" is consistent: the smallest
  hit so far has n = 46.
- **Corrected target R0c** (≈ NRC-M through a Hamiltonian state): no closed D-walk that is a Q-cycle (E − M_t a
  connected DL figure-eight at every state) and contains a Hamiltonian arc. The Studio scan now classifies cycles
  by this criterion.

**Lesson:** a stripped-down conjecture must be checked on real census graphs before effort goes into proving it.
The SAT normal-form searches only reached n ≤ 26, below the smallest census counterexample (n = 46).
