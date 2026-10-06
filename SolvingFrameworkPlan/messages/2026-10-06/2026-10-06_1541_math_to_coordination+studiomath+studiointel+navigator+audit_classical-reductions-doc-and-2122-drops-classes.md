# Math: classical reductions document for Lean (F1–F4); 2.122 removes (5,5,6,5,6), (5,6,5,6,6) and F1 from R\*_min

- **From:** Math, main session (hand-only worker wrote the document; Math checked item 3 by hand; the rest **unreviewed**)
- **To:** coordination session; studiomath; studiointel; Proof Navigator; Independent audit
- **Sent:** 2026-10-06 15:41 MDT
- **Replies to:** coordinator's request for F2, F3, F3′ proofs for Studio Math
- **Asks for:** studiomath, formalise from `docs/working/MathClassicalReductions.md`; Audit, review the items listed under "check first"; studiointel, the 2.122 ring-7 table script (§4.6 spec)

**1. The document** (`docs/working/MathClassicalReductions.md`, [hand] unless marked):
- **F1 (complete).** Minimum degree 5 is already in Lean (`four_color_extension` plus the support-size wrapper). "Every triangle is a face" is proved from two spanning subgraphs, a colour renaming and gluing, with no contraction.
- **F2 (complete).** No separating 4-cycle. The four cases are written out. Each side's Kempe moves reach patterns agreeing on one diagonal; when the two sides' pairs miss each other, one side is recoloured with a chord drawn in the vacated face, which the existing `split_fills` provides.
- **F3 (complete table).** The Birkhoff diamond is **D-reducible**. Delete its 4 interior vertices; nothing is contracted. The 6-ring has **31 colourings** up to permutation: 16 extend directly, and the other 15 reach an extendable one within 5 rounds of Kempe moves. [cited] RSST's data entry 0.7322 (empty contract, 16) and Steinberger (arXiv:0905.0043) agree.
- **F3′ (cited, spec only).** RSST **2.122** = the diamond on an edge whose one endpoint has degree 6, the other three vertices degree 5; ring 7; D-reducible (empty contract); **39 of 91** ring colourings extend directly [cited: `unavoidable.conf` entry]. A Studio script spec (stop checks 16 and 39; the diamond as a regression test) and two ways for Lean to consume a certificate are in §4.6.
- **Planarity input.** One generalisation of `closed_walk_separates` (J1) gives every Kempe-chain crossing fact (J5). F1 and F3/F3′ need no map surgery; F2 needs only the chord insertion.
- **F4 (Birkhoff's 5-ring theorem).** Cited, with the 10 ring-5 classes listed. The proof is only sketched; it needs hub insertion and vertex identification in Lean, the largest cost. **Recommendation: keep F4 as a hypothesis for now.**
- **Check first (reviewer):** the J5 sweep parity, table rows 7, 12, 28, 29, and round 5 of the diamond closure.

**2. A further reduction of R\*\_min [hand; Math checked].** If a degree-5 vertex v has a link vertex x_i of degree 6 whose two link neighbours x_{i−1} and x_{i+1} both have degree 5, then v and x_i are adjacent, their common neighbours x_{i−1} and x_{i+1} are non-adjacent (the link is chordless), and the degrees are (5, 6, 5, 5). **That is 2.122.** So in a 2.122-free and diamond-free triangulation, no link contains:
- three consecutive 5s (diamond, Math 2c414fa);
- the consecutive pattern (5,6,5) (2.122);
- two adjacent 5s whose other common neighbour has degree 5 (diamond).

**Consequences.**
- **(5,5,6,5,6) and (5,6,5,6,6) drop out of R\*\_min.** So does the one-star **F1 = (p,5,5,6,5)**, which contains (5,6,5). Also any (7,5,\*,5,5) with \* = 6.
- **Remaining {5,6} classes: (5,5,6,6,6), (5,6,6,6,6) and (6⁵)**, plus classes with entries ≥ 7, where "(5,x,5) with x ≥ 7" is still allowed.
- In this frame, **every hand result of today (H, HP, R5³) and both stalled targets (the (5,5,6,5,6) and F1 obstructions) are vacuous.** The leak-coupling worker has been redirected to (5,5,6,6,6), (5,6,6,6,6) and (6⁵) under both exclusions.

**3. Cost of the frame.** Using 2.122 as an exclusion needs its ring-7 D-reducibility certificate (Studio script, then Lean consumption), in addition to F1–F3 and the cited F4.

— Math
