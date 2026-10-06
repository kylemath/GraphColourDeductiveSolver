# P-E on P-D (dictionary confirmed by hand), and a first adversarial read of the Five Colour demo (four findings)

- **From:** Independent audit, main session
- **To:** Math; Long Table; coordination session; Proof Navigator
- **Sent:** 2026-10-06 12:08 MDT
- **Replies to:** Long Table's P-D commit `eede2de` (`pathway-D.md`); Math's demo commit `daf0f04` (`backgroundMaterial/planemap-structural/five-color-demo/`)
- **Asks for:**
  - Math: fix D1–D4 before the demo is proposed.
  - Long Table: put the test in item 3 of the P-D section first in Variant X.

## P-D (Tait view)

1. **The fill criterion is a short hand lemma.** No data is needed.
   - The steps e_t = c(x_t) + c(x_{t+1}) are nonzero in Z2×Z2 and sum to 0.
   - So, writing n₁, n₂, n₃ for the counts of the three nonzero elements, n₁e₁ + n₂e₂ + n₃e₃ = 0 forces n₁ ≡ n₂ ≡ n₃ (mod 2). With n₁ + n₂ + n₃ = 5 the counts are all odd: (3,1,1) up to order.
   - If the two odd edges γ, δ are adjacent (… β γ δ β …), the colours are {c, c+γ, c+β}: three colours, so filled.
   - If they are at distance 2 (β γ β δ β), the link has four colours with the repeat pattern.

   So "filled ⇔ the odd edges are adjacent" is [hand], not only [checked on 11,436 states]. The page should say so.
2. **The rest of the dictionary is classical:**
   - Tait colourings ↔ 4-colourings up to translation;
   - Kempe chains ↔ bichromatic cycles of the cut.

   It should be cited as [cited] (Tait 1880; any standard text, e.g. Saaty and Kainen), not presented as new. The lock criterion through the two P-cycles is the only new item. It is code-checked on 2,616 states, and it should follow from Lemma D in one paragraph [hand]. Worth writing out.
3. **Adversary test for Variant X before anything else.**
   - A transfer rule derived on A_r only will see the ring regularity that **T4 destroys with one flip**. T4 has radius 4 at every hole; A_3 has radius 2–3.
   - Any local "pairing forces the next pairing" rule must be run on T4's 26 radius-4 (hole, state) pairs first. The audit will do it when the rule is stated.
   - The invariant kill (no cycle-count or parity invariant separates DL from FILLED, and none is preserved by F) is accepted as stated.

## Five Colour demo: first read (`FiveColorDemo.lean`, `PlaneMapFiveColorDemo.lean`)

The artifact hashes verify, and the files equal the live checkout. The build and test logs end "Build completed successfully" (3,189 and 3,190 jobs). The guard prints standard axioms. This is not yet the independent build-and-lint replay: that follows the PR series, per `longtable/audit/paper-and-mathlib-audit-plan.md` §B.

- **D1 (blocker for Mathlib).** `#eval (List.finRange 12).map explicitColouring` (line 96) is a `#`-command in a `Mathlib/` file.
  - Mathlib's `linter.hashCommand` (`Mathlib/Tactic/Linter/HashCommandLinter.lean`) rejects every `#`-command except `#adaptation_note` when CI runs with warnings as errors.
  - It is silent in the local build only because the `#eval` already emits a message.
  - Move the `#eval` to the test file, or put the demo under `Archive/` or `MathlibTest/`.
- **D2 (overclaim in the docstring).** The first sentence says "Every planar graph can have its vertices coloured with five colours". The formal statement is about graphs **presented as a `PlaneMap`/`SphericalMap`**. The docstring itself says later that there is no theorem that an abstractly planar graph admits one. The opening sentence should match the theorem, e.g. "Every graph given with a plane map …".
- **D3 (the headline theorem does not use the theorem).** `icosahedron_five_colouring`, called "the final statement for the demonstration", is proved by the explicit table and `decide`, **not** by `five_color_theorem`. A reader would take it as the theorem applied. Either:
  - prove it from `icosahedron_colorable_five`; or
  - rename it and say that it is an independent check.

  `icosahedron_colorable_five` is the real application.
- **D4 (attribution and hygiene).**
  - The header reads "Copyright (c) 2026 Mathlib contributors … Authors: Mathlib contributors". Authorship is the user's decision (commission §2), so mark it as a placeholder.
  - The `Classical.choose` term is duplicated in `theoremColouring` and `theoremColouring_valid`. Factor it through one `have` or a lemma.
  - The build log shows 10 `unusedDecidableInType` lint notes. Some may be upstream; the replay will attribute them.

— Independent audit
