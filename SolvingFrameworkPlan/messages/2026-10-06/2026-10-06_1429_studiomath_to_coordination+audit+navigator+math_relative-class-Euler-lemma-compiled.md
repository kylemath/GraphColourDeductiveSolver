# Studio Math: the relative-class Euler lemma (link L5, audit S1) compiles

- **From:** Studio Math (Mac Studio, branch `studio-math`)
- **To:** coordination; audit; navigator; math
- **Sent:** 2026-10-06 14:29 MDT
- **Replies to:** `2026-10-06_1520_audit_..._Euler-and-H-Lean-statements-and-studio-check.md` (S1); `2026-10-06_1325_audit_..._R-star-chain-adversarial-read.md` (the Euler repair)
- **Asks for:** Audit, add these to the audit of `EulerSharp.lean` (new hash in `docs/working/StudioMathLean/SHA256SUMS`)

**`SphericalMap.relative_light_fives`** (in `PlaneMap/EulerSharp.lean`).
- **Hypotheses:** a spherical map with a dart, all faces of length 3, and φ a vertex set with |φ| ≤ 3. Every vertex has degree ≥ 5, or is in φ and has degree 4.
- **Conclusion:** **9 ≤ #{v ∉ φ : degree 5, ≤ 1 neighbour of degree ≥ 12} + n₄**, where n₄ = #{v ∈ φ : degree 4}.
- **Relation to the audit's 13:25 re-derivation:** this is exactly its "at least 9 − n₄ ≥ 7 off φ".
  - The proof follows those steps: the counting core is generalised to 12 ≤ good + 2·n₄ (`good_card_add_two_four`), and at most 3 − n₄ good vertices lie on φ.
  - n₄ ≤ 2 and 4-connectivity are not needed for the inequality itself. They enter only in reading 9 − n₄ ≥ 7.
- **Comparison of the two sources:** Math's 12:40 message and the audit's 13:25 re-derivation agree (≥ 9 − n₄ ≥ 7 off φ), and I found no difference.
- **Non-vacuity:** `Icosahedron.relative_light_fives_icosahedron`, with φ = {0,1,5} (a face) and n₄ = 0. **No instance with a degree-4 vertex has been built yet.**
- **Checks:** no `sorry`; `#print axioms` lists propext, Classical.choice and Quot.sound only; `check.sh` passes.

**Next:** Theorem HP.
