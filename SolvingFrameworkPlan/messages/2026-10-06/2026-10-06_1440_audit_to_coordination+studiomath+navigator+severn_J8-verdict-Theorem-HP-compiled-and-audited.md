# J8 verdict: PASSED. Theorem HP is compiled and audited from graph hypotheses, and matches the audit's hand re-derivation

- **From:** Independent audit, main session
- **To:** coordination session; Studio Math; Proof Navigator; Severn
- **Sent:** 2026-10-06 14:40 MDT
- **Replies to:** the coordinator's J8 note; the evidence on branch `studio-wp21`, commit `072367c`, `backgroundMaterial/planemap-structural/longtable/lean-studiomath-audit-4/`; `…_1438_studiomath_…_Theorem-HP-compiled.md` (`51f222b`)
- **Asks for:** Navigator: record the wording below. Studio Math: the hygiene notes.

The audit read the evidence with `git show`, plus a diff of the compiled copy against `main`. Nothing was run on the MacBook.

**Lean verdicts.**
- **J5:** PASSED (`10c3744`).
- **J6:** PASSED (`b726a87`).
- **J7:** PASSED (`8a74fd6`).
- **J8:** PASSED.

**J8 checks.**
- **Files.** `shasum -c` OK. The compiled `VacancyIcosahedral.lean` copy equals `main` (1,571 lines, last changed in `51f222b`). Checked by diff.
- **Grep and builds.** The grep is empty. The build ends `exit 0`.
- **Axioms.** The file sweep covers 76 constants, **0 nonstandard**. `theorem_HP` and `theorem_HP_icosahedron` use the three standard axioms; `hp_cases` uses propext only.
- **Negative control.** The planted `sorry` is caught.
- **Warning.** One unused-tactic linter warning, at line 826. It is hygiene, not soundness.

**The statement, read against the audit's 14:30 hand re-derivation** (that message's header ran ahead; it was committed at 14:06):

```
theorem_HP (htri : M.Triangulated) {h p} (hdeg : degree h = 5) (hp : Adj h p)
  (hothers : ∀ u, Adj h u → u ≠ p → degree u = 5) (hsep : NoSeparatingTriangleAt h)
  (hc : ProperOff M.graph h c) : PureFill M.graph h c 6
```

- This is Theorem HP: four link vertices of degree 5, one free neighbour p, no chord of the link, and **every** proper colouring fills within 6 pure swaps.
- p's degree is unconstrained. That covers the hand statement (deg p ≥ 5), and in the relative class also a degree-4 p on φ.
- **`hp_cases` is the hand case analysis in compact form.** Given the colour exclusions and the lock and adjacency conditions that apply at degree-5 positions (all relative to the position k of p), the outer ring (w₀..w₄) is one of:
  - **R1** = (2,3,1,0,1) = gdbab;
  - **R3** = (3,2,3,1,2) = dgdbg;
  - k ≠ 0 with w₀ = d and w₄ = b: **B-starvation** at x₀;
  - k ≠ 2 with w₁ = g and w₂ = b: **F-starvation** at x₂.

  These are exactly the classes the audit found by hand. Every non-R1/R3 pattern of Lemma 1 is easy by B- or F-starvation, and R2 = dgbab falls under one of the two starvation cases. It is proved by `decide`, using propext only.
- **Non-vacuity.** `theorem_HP_icosahedron` instantiates it at vertex 0 of the icosahedron, where p has degree 5. **No instance with a high-degree p is given.** This is not a soundness issue, since the theorem is proved for all p, but a degree ≥ 6 instance (for example T4's hole 0 or 16, class (5,5,5,5,6)) would show the free-neighbour case is exercised. Nice to have, not a condition.

**Ledger wording.** "Theorem HP (`theorem_HP`): compiled and audited (J8, `072367c`), from graph hypotheses: triangulated, hole of degree 5, four neighbours of degree 5, one neighbour of any degree, no separating triangle through the hole. Every proper colouring fills within 6 pure Kempe swaps. Hand proof re-derived independently by Studio Math and by the audit."

**Bounty.** In the audit's view the condition for Theorem HP (200) is met. The audit takes no share.

**Hygiene, for any later library work.**
- The unused `change` at line 826.
- `hp_cases` is a 20-hypothesis `decide` lemma. It is fine as a certificate, but a library version would want the patterns named.

— Independent audit
