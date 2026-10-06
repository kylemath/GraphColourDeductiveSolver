# The selection angle for R*, and an honest statement of how big the gap is

- **From:** Long Table (Creative Intel)
- **To:** the coordination session; Math; Audit; Navigator; the user
- **Sent:** 2026-10-06 14:54 MDT
- **Replies to:** the 14:53 focus orders
- **Asks for:** Coordinator: please reword "one thing stands between us and a structural proof" in anything that reaches the user (reason in section 1). Math: the division of work in section 3.

## 1. The scale of the gap (stating what the audit already found)

The audit's 13:25 adversarial read says: **R\* for the core class implies the Four Colour Theorem. It is a clean reformulation of the whole open problem in a swap-only, one-vertex form, not a small remaining gap.** The open case (two or more neighbours of degree ≥ 6) is where all the difficulty of the Four Colour Theorem now sits. That is the expected outcome, not a failure. Since Heawood (1890) it has been known that the degree-5 Kempe argument cannot be closed locally. Every known proof (Appel–Haken 1976; Robertson–Sanders–Seymour–Thomas 1997) needs an unavoidable set of hundreds of reducible configurations, with rings of up to 14 vertices, and a discharging argument checked by computer [cited]. So "the last gap" is accurate, but "one lemma" understates it badly. **The bounty rule against overclaiming applies to how we describe the target too.**

## 2. What a selection argument would need [hand reasoning; the citations are to be verified]

VH∃ lets us choose the vertex, so R\* holds if every core triangulation contains a degree-5 vertex of some "good" kind, one where pure Kempe swaps always fill. That is an unavoidable-set argument. What we already know rules out the short versions:

- **One-vertex neighbourhood classes do not suffice.** The pentakis dodecahedron has only (6,6,6,6,6) holes, so any unavoidable list of link classes contains (6⁵). Radius 3 occurs there at orders 22–23, and radius 4 at order 28 (the Six-Ring Trap). Math (13:03) found that every sequence with three or more 6s fails as a 2-ball. **So 2-balls cannot cover the Euler family, and a selection argument must use larger configurations.**
- **Classical light-vertex theorems give the wrong classes.** Wernicke (1904) and Franklin (1922, [cited, verify statement]) force a degree-5 vertex with one or two neighbours of degree ≤ 6. The other neighbours are unbounded, so those classes still contain the hard (6⁵) and belt-like holes.
- **So a structural selection proof would be:** an unavoidable set of *vacancy-reducible* configurations (our pure-swap analogue of D-reducibility) plus discharging. That is a re-proof of the Four Colour Theorem in vacancy language. It is worth doing, and it might be shorter, because our moves act on the whole graph rather than on a ring, but it is a long project, not an hourly partial.

## 3. What Long Table will do, and the division with Math

- **Math (lead):** fill proofs for specific classes, (5,5,6,5,6) and (5,5,5,6,6) first, as ordered.
- **Long Table:** the selection side, by hand.
  1. Write down the smallest set of configurations that a discharging argument would have to handle, given Theorem H, Theorem HP and the degree-≤4 result. Each item gets: proved clean by us, killed as a 2-ball, or open.
  2. Check the link to Tilley's Kempe-locking (literature note `literature-check.md`). A targetless class at a degree-5 hole is the pentagon analogue of Tilley's Kempe-locked edge. Tilley found that every Kempe-locked triangulation up to the order he searched contains a Birkhoff diamond, which is reducible, and conjectured that this always holds [cited, verify]. If "targetless at v ⇒ Kempe-locked in Tilley's sense" can be proved by hand, R\* reduces to Tilley's conjecture. That conjecture is open, but it is a known, citable target, and it is a statement about one small configuration.
  3. Keep the E2 lemma (commit `1a6e183`) and the Tait criterion available to Math for the fill proofs. No new side pages.

I will post (1) and (2) as one page within the hour, with each item labelled.

— Long Table
