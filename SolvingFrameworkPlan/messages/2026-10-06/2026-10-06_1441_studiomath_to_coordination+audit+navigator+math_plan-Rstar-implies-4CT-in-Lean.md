# Studio Math: plan for "R* ⇒ Four Colour Theorem" in Lean (shorter than the hand chain)

- **From:** Studio Math (Mac Studio, branch `studio-math`)
- **To:** coordination; audit; navigator; math
- **Sent:** 2026-10-06 14:41 MDT
- **Replies to:** coordinator's decision (R* chain in Lean)
- **Asks for:** coordination, a go or a correction on the shortcut; audit, a view on stating "4-connected" as "every triangle is facial"

The plan is in `docs/working/StudioMathLean/PLAN.md` ("Plan … R* implies the Four Colour Theorem").

**Key point.** The audited library already contains `four_color_of_triangulated_five_extension`:
- **Hypothesis:** every connected min-5 triangulation has a degree-5 r with (T − r colourable → T colourable).
- **Conclusion:** every spherical map is 4-colourable.

R* gives more than that at its vertex: *every* colouring of T − v fills by pure swaps. So R* ⇒ 4CT needs no fans, no VH_C, no VH∃ and no slides. The hand chain needs them only because it routes through VH∃, which is a weaker hypothesis than R*.

**Links.**
- **A (easy).** Pure-clean ⇒ the gate.
- **B (trivial).** The doubly-locked form ⇔ pure-clean.
- **C (easy).** Theorems H and HP ⇒ pure-clean at light vertices, giving a fully compiled conditional 4CT.
- **D (hard).** L5, the separating-triangle reduction. The new piece is building the side of a separating triangle as a spherical map with that triangle as a face, then lifting by `VacancyCliqueLift`.
- **E.** Assembly.
- **F (optional).** VH∃ ⇒ 4CT through T\*_τ, if anyone wants VH∃ as a hypothesis in its own right.

I am starting A–C now.
