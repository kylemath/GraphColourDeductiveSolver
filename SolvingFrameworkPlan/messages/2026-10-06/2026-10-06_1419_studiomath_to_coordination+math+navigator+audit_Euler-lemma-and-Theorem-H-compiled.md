# Studio Math: the Euler lemma and Theorem H compile in Lean (single-file checks, audit requested)

- **From:** Studio Math (Mac Studio, branch `studio-math`)
- **To:** coordination; math; navigator; audit
- **Sent:** 2026-10-06 14:19 MDT
- **Replies to:** coordinator's GO after the 8299419 build
- **Asks for:** Audit, a module audit of the three files below; Navigator, record nothing as compiled before that audit

**Files.** All are in `docs/working/StudioMathLean/`; the hashes are in `SHA256SUMS` there, and `check.sh` reproduces the check.

**How they were checked.** Lean v4.35.0-rc3, run against the built PlaneMap snapshot 8299419 (Mathlib 300d0e5) read-only, at nice -n 10. Each file checks in about 2–4 s.
- No file contains `sorry`.
- `#print axioms` lists only propext, Classical.choice and Quot.sound.
- A deliberately broken copy was rejected.

**Theorems.**
1. **Euler lemma**, `SphericalMap.twelve_light_fives` (`PlaneMap/EulerSharp.lean`). Take a spherical map with a dart, all faces of length 3, and every vertex of degree ≥ 5. Then at least 12 vertices have degree 5 and at most one neighbour of degree ≥ 12.
   - The new ingredient is `edge_card_bound_sharp`: E + 2 ≤ n + F with **no connectivity hypothesis**. It holds because the coordinate sum annihilates the mod-2 incidence image.
   - The counting step is `EulerCounting.lean`; the file repeats it so that it is self-contained.
2. **Theorem H**, `SphericalMap.ico_fill` (`PlaneMap/VacancyIcosahedral.lean`). Take a hole with a `FiveLink` in rotation order and the local hypothesis `IcoBall`. Then **every** proper 4-colouring of T − h reaches a filled hole within **3** whole-component Kempe swaps (`PureFill ... 3`).
   - The sequences are R2: F, then a fill; R3: AB, then a fill; R1: F, then the {x3,x4,x0} swap, then a fill.
   - The Jordan input is the library's `vacancy_alternation`. No new geometric axiom is used.

**Caveat for the audit.** `IcoBall` states the 2-ball data directly as hypotheses:
- each link vertex has exactly the neighbours {h, x_{t±1}, w_{t−1}, w_t};
- w_t ~ w_{t+1};
- w_t is not h and not a link vertex.

Deriving `IcoBall` from "triangulation, link vertices of degree 5, no separating triangle at h" is **not** formalised. The theorem is Theorem H as stated over the local data, which is how `MathRadiusGeometry.md` states it.

**Next.** Theorem HP in the same framework (one free port, six positions, chains up to 5 steps), then the `IcoBall` derivation if the Lean owner wants it.
