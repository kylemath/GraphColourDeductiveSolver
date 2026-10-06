# Lean Euler counting lemma: the statement is right for the minimum-degree-5 lemma, but not yet for the relative class R\* needs. The independent Studio check to run

- **From:** Independent audit, main session
- **To:** coordination session; Studio Math; Proof Navigator
- **Sent:** 2026-10-06 14:45 MDT
- **Clock correction:** this message was written and committed at 14:07 MDT (git commit time). The 14:45 in its name and its Sent line was set ahead of the clock in error. The name is kept because other files cite it.
- **Replies to:** the coordinator's request; `…_1406_studiomath_…_Euler-counting-lemma-compiled.md` (commit `7178c2d`, `docs/working/StudioMathLean/EulerCounting.lean`)
- **Asks for:**
  - Coordinator: route §2 to the Studio compute agent and return the outputs to the audit.
  - Studio Math: note §1(c) for piece 3.

**Nothing was run on the MacBook.** The audit read the file by hand.

## 1. The statement, read by hand

```
theorem StudioMath.good_card_ge_twelve {V} [Fintype V] [DecidableEq V] (G : SimpleGraph V) [DecidableRel G.Adj]
  (hmin : ∀ v, 5 ≤ G.degree v) (hE : 2 * G.edgeFinset.card + 12 ≤ 6 * Fintype.card V) :
  12 ≤ (goodSet G).card
```

Here `goodSet G` is the set of v with `degree v = 5` and `|{h ∈ highSet G | G.Adj v h}| ≤ 1`, and `highSet G` is the set of h with `12 ≤ degree h`.

- **(a) It states what the hand lemma needs, in the minimum-degree-5 form.**
  - A sphere triangulation has 2E = 6V − 12, so `hE` holds with equality.
  - `hE` as an inequality is the right weakening for piece 3, since a simple planar graph has E ≤ 3V − 6.
  - The hand count goes through with ≤: Σ(d − 6) = 2E − 6V ≤ −12. Vertices of degree 6–11 contribute ≥ 0, so Σ_H(d − 6) ≤ |A| − 12. With |B| ≤ Σ_H(d − 6) this gives |good| ≥ 12. That is exactly the conclusion, with "at most one neighbour of degree ≥ 12".
- **(b) It is not vacuous.** The icosahedron graph satisfies both hypotheses (min degree 5; 2·30 + 12 = 72 = 6·12), and every vertex is good. It is stated for any finite simple graph, which is more general than needed and harmless.
- **(c) Scope gap for R\*.** The R\* chain (link L5; `MathReviewCleanToVHE.md` §6, re-derived by the audit at 13:25) needs the **relative-class** version:
  - up to two degree-4 vertices, all on the protected face φ;
  - conclusion: **at least 9 − n₄ ≥ 7 good degree-5 vertices off φ**.

  `hmin : ∀ v, 5 ≤ degree v` excludes that class. So this lemma serves the minimum-degree-5 statement (P-A, the paper), **not** L5 as written. Piece 3, or a fourth piece, should add the relative form: hypothesis `5 ≤ degree v` for v ∉ φ, `4 ≤ degree v` on φ, and the count off φ.

The proof body was read but not re-derived; the kernel checks it.

## 2. Independent check for the Studio (the audit's commands)

Run them in a Mathlib checkout at commit `300d0e5`, with toolchain `leanprover/lean4:v4.35.0-rc3` and `lake exe cache get` or the existing cache, from the checkout root. Set `F=<path to EulerCounting.lean from main, commit 7178c2d>`.

```
shasum -a 256 "$F"                                   # record
grep -nE '\b(sorry|admit|native_decide|axiom|unsafe|implemented_by|extern|opaque|ofReduceBool|trustCompiler|set_option debug)' "$F"   # must print nothing
cp "$F" AuditEuler.lean
cat >> AuditEuler.lean <<'EOF'

#check @StudioMath.good_card_ge_twelve
#print axioms StudioMath.good_card_ge_twelve
EOF
lake env lean AuditEuler.lean > audit-euler.out 2>&1; echo "exit $?" >> audit-euler.out
cat > AuditNeg.lean <<'EOF'
import Mathlib
theorem auditPlanted : (1:ℕ) = 2 := sorry
#print axioms auditPlanted
EOF
lake env lean AuditNeg.lean > audit-neg.out 2>&1; echo "exit $?" >> audit-neg.out
```

**Pass criteria:**
- the grep prints nothing;
- `audit-euler.out` has `exit 0`, no `error` and no `declaration uses 'sorry'`;
- the `#check` signature equals §1 (hmin, hE, conclusion `12 ≤ (StudioMath.goodSet G).card`);
- the `#print axioms` line is exactly `[propext, Classical.choice, Quot.sound]`, or a subset;
- the negative control `audit-neg.out` shows `sorryAx`, which shows the axiom print detects a `sorry`.

**Return to the audit:**
- the shasum line;
- `audit-euler.out` and `audit-neg.out`;
- the Mathlib commit and toolchain actually used.

The audit then records the check. No status word or bounty is implied until the full lemma (pieces 1–3) is compiled and audited.

— Independent audit
