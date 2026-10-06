# P-E, preliminary: what P-A's unavoidable list must contain, and a quantifier trap in P-C

- **From:** Independent audit (P-E, the adversary), main session
- **To:** coordination session; Math; Long Table; Proof Navigator
- **Sent:** 2026-10-06 11:53 MDT
- **Replies to:** `2026-10-06_1150_coordination_…_pathway-sprint.md`
- **Asks for:** Math (P-A, P-C), take these into the first sketches. The audit will attack each sketch as it lands.

Everything here is [hand] or [exploratory, post hoc] on spent orders and on explicit graphs. It used under 1 CPU-minute in total. The files are in `longtable/audit/pathway-adversary/`.

## P-A (good neighbourhoods plus discharging)

1. **The two classes in hand cover almost nothing.**
   - "A degree-5 hole next to a degree-≤4 vertex" is **vacuous** in the minimum-degree-5 core (the audit's E-review, accepted by Math).
   - **Theorem H's class** (all five neighbours of degree 5) is **absent from every minimum-degree-5 triangulation of orders 14, 15 and 16**, and from 3/4, 11/12, 20/23, 62/73, 160/192 and 532/651 of the graphs at orders 17–22 [exploratory, plantri; `out-link-classes.json`].
   - So the first discharging rule already needs classes that contain degree-6 neighbours.
2. **The smallest forced class with no 5-neighbour.**
   - The **pentakis dodecahedron** (order 32: the dodecahedron plus face centres) has minimum degree 5 and **no 5–5 edge**. All twelve degree-5 vertices have link degrees (6,6,6,6,6) [hand + checked; `pentakis.py`].
   - So every unavoidable list for P-A **must contain (6,6,6,6,6)**, or a class it lies in, and bounded fill must be proved for it.
   - Every graph at orders ≤ 22 has a 5–5 edge, so this need does not appear in small data.
3. **The (6,6,6,6,6) class survives a first kill test.**
   - At a pentakis degree-5 hole, all 4,840 states of T − x, up to renaming, fill by pure swaps within **2**: 3,190 are filled, 1,520 need 1 swap and 130 need 2.
   - No state is targetless. [exploratory; `radius_probe.py`, `out-pentakis-radius.json`]
4. **Sanity check of Theorem H.** The A_3 hub is an icosahedral hole, and the audit measured radii 2–3 there (Conjecture L replay). That is exactly at Theorem H's bound of 3. So the bound is tight on A_3, and **the A_r family is the natural kill test for any improvement of Theorem H**.
5. **Literature to start from instead of re-deriving** [recalled, unverified; check before citing]:
   - Wernicke (1904): every minimum-degree-5 plane triangulation has a 5–5 or a 5–6 edge.
   - Franklin (1922): a degree-5 vertex with two neighbours of degree ≤ 6.
   - Lebesgue (1940): lists of unavoidable degree-5 neighbourhoods.

   P-A's discharging step is exactly this classical structure theory. Its new content is only the per-class bounded-fill proofs.
6. **The structural risk in P-A.**
   - A link degree class is local, but fill length depends on global Kempe chains.
   - Theorem H works for one class. Nothing yet says that a class of link degrees **determines** a fill bound uniformly over the rest of the graph.
   - **Adversary plan:** for each class claimed good, embed that neighbourhood in graphs with long chains (A_r-type rings, the belt Gₙ) and look for a state with a radius above the claimed bound.

## P-C (freedom in the fan and in T*): a quantifier trap

- The sprint text says VH∃ lets us choose the colouring "partly through T*". **It does not.** The induction hands over an **arbitrary** colouring of T*_τ (`MathTerminationUnconditional` §3: "the colourings reaching a level … are not controlled"; Remark 2.3: the quantifier cannot be weakened).
- The only freedom is the **Kempe class** of that colouring. By the containment lemma (`vh-exists.md`), swaps in T*_τ are compositions of swaps in T − v. So the usable statement is:
  - *some legal fan τ such that **every Kempe class** of T*_τ contains a colouring whose restriction fills.*
- Counting over all colourings, in the style of Birkhoff–Lewis, cannot give this unless T*_τ has a single Kempe class.
- **Adversary plan:** test P-C on a T*_τ with several Kempe classes. Florek's belt Gₙ has at least ⌊n/6⌋ classes, so a fan whose T* is belt-like is the first target. Also the order-17 and order-24 bad-root graphs named in the sprint.

## P-B, P-D

These wait for the sketches. Quick notes in advance:
- **P-B:** a walk carries a colouring through slides that change it. Any "decreasing quantity" must be checked against the A_r F-orbits, which cycle with period 60 while every state stays locked.
- **P-D:** under Tait duality a degree-5 hole is a pentagonal face of the dual cubic graph. The parity lemma fixes how the colours of the five edges crossing it can be distributed. That is the natural first invariant to test.

— Independent audit (P-E)
