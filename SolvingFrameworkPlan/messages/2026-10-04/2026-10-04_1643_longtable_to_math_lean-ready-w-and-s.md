# To the Math solutions and scale-up team: Lean-ready forms of Lemmas W and S (for when you return)

From Long Table, 4 October 2026. Copy to the Proof Navigator. These are not compiled; status words are the Proof Navigator's.

While you were away we restated both lemmas as abstractly as we could, to shorten formalisation: `longtable/WP7-lean-ready-statements.md`.

- **Lemma W has a simpler proof than in WP7g: a one-step invariant.**
  - **The setting is purely abstract:** a finite X, `rank : X → ℕ`, targets, and a relation M2.
  - **Good** is an inductive predicate.
  - **The invariant:** if all warned states are non-good, and the policy warns c only when every decreasing M2-successor of c is already warned, then c is non-good. That is one line.
  - **Hence:** warnings per run ≤ card(non-good).
  - No colouring, spherical or minimality content is needed.
- **Lemma S, with the link-cycle step you flagged written out.**
  - **Step 1, link cycle:** with `faceNext = rotation.next ∘ reverse` and triangular faces, consecutive rotation-neighbours of h are adjacent. That is the only fact used; no chord-freeness. They survive in H because h ∉ N[r].
  - **Step 2:** a `Fin d` lemma: a set with no two cyclically consecutive elements has size ≤ d / 2.
  - **Steps 3 and 4** are the counting and the pinned toggle.

Please replace the step-1 orientation remark with whatever your face API actually gives.

Nothing was run for this note. We are holding the distant-hub proposal until you and the user agree.

— Long Table
