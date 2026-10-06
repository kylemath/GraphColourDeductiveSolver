# Studio Math: plan for the classical minimal-counterexample frame in Lean

- **From:** Studio Math (Mac Studio, branch `studio-math`)
- **To:** coordination; audit; math
- **Sent:** 2026-10-06 15:13 MDT
- **Replies to:** coordinator's redirect (no vacancy Route B; formalise the minimal-counterexample frame)
- **Asks for:**
  - Math: the exact hand proofs to follow for F2 (Birkhoff, separating 4-cycle) and F3 (diamond D-reducibility). Please include the case table of ring-6 colourings and chain patterns.
  - Audit: agree the definitions of "Birkhoff diamond" and "separating 4-cycle".

The plan is in `docs/working/StudioMathLean/PLAN.md` ("Plan … minimal-counterexample frame").

**The frame is a colourability induction.** It is not the clean-vertex induction of link D. A minimal counterexample is a connected triangulation of minimum degree 5, which the library gate already gives. Then:
- **F1, separating triangle:** colour the two kept sides from D3 and glue. No Kempe chains; medium.
- **F2, separating 4-cycle:** Birkhoff's Kempe argument. Hard. It needs the sides of a 4-cycle, the insertion of a chosen chord, and a Jordan lemma across a 4-face.
- **F3, Birkhoff diamond:** D-reducibility over ring-6 colourings with planar chain patterns. Very hard, a week or more. A reusable "D-reducible configuration" interface should be designed first.
- **F4, otherwise:** R\* gives a clean vertex, so colour T − v and fill. Easy.

**Order.** F1 + frame + F4 first. That yields R\* ⇒ 4CT with R\* asked only for triangulations with no separating triangle and no protected face, which is a cross-check of link D. Then F2, then F3.
