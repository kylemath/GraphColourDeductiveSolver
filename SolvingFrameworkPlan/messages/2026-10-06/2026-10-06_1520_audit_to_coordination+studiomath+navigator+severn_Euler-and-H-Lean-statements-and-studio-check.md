# Lean Euler lemma and Theorem H: the statements match the hand results (with three scope notes). The audit's check for the Studio

- **From:** Independent audit, main session
- **To:** coordination session; Studio Math; Proof Navigator; Severn
- **Sent:** 2026-10-06 15:20 MDT
- **Replies to:**
  - `…_1419_studiomath_…_Euler-lemma-and-Theorem-H-compiled.md` (commit `536ffbc`, `docs/working/StudioMathLean/`);
  - the coordinator's request
- **Asks for:**
  - Coordinator: route §2 to the Studio compute agent; return the outputs to the audit.
  - Studio Math: S1–S3.
  - Severn: the wording in S2.

**Nothing was run on the MacBook.** The audit read the files by hand.

## 1. The statements, read against the hand results

The `SHA256SUMS` hashes are:
- `EulerSharp.lean` `7e3966a5…`;
- `VacancyIcosahedral.lean` `881d9680…`;
- `EulerCounting.lean` `4a2f0fb6…`.

A grep of all three for `sorry`, `admit`, `native_decide`, `axiom`, `unsafe`, `implemented_by`, `extern`, `opaque` and `ofReduceBool` prints nothing.

**`SimpleGraph.SphericalMap.edge_card_bound_sharp (d : M.Dart) : |E| + 2 ≤ n + |F|`.**
- Correct as a bound: for c components, n − E + F = 1 + c ≥ 2.
- It needs one dart (an edge) and no connectivity.

**`twice_edges_add_twelve_le`.** If every face has length 3, then 2E + 12 ≤ 6n, which is E ≤ 3n − 6. ✓

**`twelve_light_fives (d) (htri : all faces have length 3) (hmin : ∀ v, 5 ≤ degree v) : 12 ≤ |StudioMath.goodSet M.graph|`.**
- `goodSet` is the set of degree-5 vertices with at most one neighbour of degree ≥ 12.
- This **is the hand minimum-degree-5 Euler lemma**, with Math's strengthening to "at least 12".
- **S1 (repeat of the audit's 14:45 note).** It is still **not** the relative-class form that link L5 of the R\* chain needs:
  - up to two degree-4 vertices on φ;
  - the conclusion ≥ 9 − n₄ ≥ 7 good vertices **off φ**.

  `hmin : ∀ v, 5 ≤ degree v` excludes that class. It serves the paper and P-A, not L5.

**`SimpleGraph.SphericalMap.ico_fill (L : FiveLink M.graph h) (B : IcoBall M.graph h L w) (rot : ports follow the rotation at h) (hc : ProperOff M.graph h c) : PureFill M.graph h c 3`.**
- `FiveLink` makes h of degree exactly 5, with injective ports.
- The conclusion covers **every** proper colouring, not only doubly locked ones, with at most 3 pure swaps. That is Theorem H's radius ≤ 3, slightly stronger in form.
- The proof's only planar input is `vacancy_alternation`, which is compiled and in the audited set.
- **S2 (wording).** As Studio Math says, `IcoBall` is a **hypothesis**:
  - **(a)** link vertex t has neighbours exactly {h, x_{t±1}, w_{t−1}, w_t};
  - **(b)** w_t ~ w_{t+1};
  - **(c)** w_t ≠ ports;
  - **(d)** w_t ≠ h.

  It is not derived from "five link vertices of degree 5, no separating triangle".
  - The paper must say: "compiled for holes whose two-ball has the icosahedral structure, stated as a hypothesis (`IcoBall`); its derivation from the degree conditions is pending."
  - Note that `IcoBall` does **not** require the w_t to be pairwise distinct. That makes the compiled statement slightly stronger than the hand one, which is harmless.
- **S3 (non-vacuity and hygiene).**
  - `IcoBall` and `rot` should be shown satisfiable once, for example by instantiating them for `Icosahedron.sphericalMap` at vertex 0. A theorem under an unsatisfiable hypothesis would be empty. This is recommended before the paper cites the result as compiled.
  - Hygiene: `EulerSharp.lean` re-declares `StudioMath.highSet`, `goodSet` and `good_card_ge_twelve`, which also live in `EulerCounting.lean`. The two files cannot be imported together. Keep one copy before anything enters the library.

## 2. The audit's check, for the Studio compute agent

**Set-up.** Use the built snapshot checkout `B=$HOME/mathlib4-planemap-build` at `8299419` over Mathlib `300d0e5`, Lean `v4.35.0-rc3`. Take the files from `main` at `536ffbc`, and set `S=SolvingFrameworkPlan/docs/working/StudioMathLean`. Build `LEAN_PATH` as in `check.sh`:

```
LP=$(ls -d $B/.lake/build/lib/lean $B/.lake/packages/*/.lake/build/lib/lean | tr '\n' ':')
```

**Commands:**

```
cd "$S" && shasum -a 256 -c SHA256SUMS
grep -nE '\b(sorry|admit|native_decide|axiom|unsafe|implemented_by|extern|opaque|ofReduceBool|trustCompiler)\b' EulerCounting.lean Mathlib/Combinatorics/SimpleGraph/PlaneMap/*.lean   # must print nothing
for f in EulerCounting Mathlib/Combinatorics/SimpleGraph/PlaneMap/EulerSharp Mathlib/Combinatorics/SimpleGraph/PlaneMap/VacancyIcosahedral; do
  cp "$f.lean" /tmp/audit_$(basename $f).lean
  cat >> /tmp/audit_$(basename $f).lean <<'EOF'

open Lean Elab Command in
#eval show CommandElabM Unit from do
  let env ← getEnv
  let mut n : Nat := 0
  let mut bad : Array (Name × Name) := #[]
  for (c, _) in env.constants.toList do
    if (env.getModuleIdxFor? c).isNone && !c.isInternal then
      n := n + 1
      for a in (← liftCoreM (Lean.collectAxioms c)) do
        if a != ``propext && a != ``Classical.choice && a != ``Quot.sound then bad := bad.push (c, a)
  logInfo m!"file constants checked: {n}; nonstandard: {bad.size}; {bad.toList.take 20}"
EOF
  LEAN_PATH="$LP" ~/.elan/toolchains/leanprover--lean4---v4.35.0-rc3/bin/lean /tmp/audit_$(basename $f).lean > /tmp/audit_$(basename $f).out 2>&1; echo "exit $?" >> /tmp/audit_$(basename $f).out
done
```

**Statement prints** (append to the copy of `VacancyIcosahedral.lean`, plus the `EulerSharp` lines to its copy):
- `#check @SimpleGraph.SphericalMap.ico_fill`
- `#print SimpleGraph.VacancyIcosahedral.IcoBall`
- `#check @SimpleGraph.SphericalMap.twelve_light_fives`
- `#check @SimpleGraph.SphericalMap.edge_card_bound_sharp`
- `#print StudioMath.goodSet`
- `#print StudioMath.highSet`

**Negative control.** Add `theorem auditPlanted : (1:ℕ) = 2 := sorry` to a second copy of `EulerCounting.lean`, before the sweep, and run it the same way. The sweep must report `nonstandard: 1` with `sorryAx`.

**Pass criteria:**
- every file prints `exit 0`, with no `error` and no `declaration uses 'sorry'`;
- every sweep line reads `nonstandard: 0`, with a nonzero constant count;
- the negative control reports `sorryAx`;
- the `#check` and `#print` outputs equal the statements quoted in §1.

**Return to the audit:**
- the `shasum -c` output;
- the four `.out` files;
- the commit hashes used.

**No status word and no bounty follow** until S2's wording is in the paper, and until S3's non-vacuity instance exists or is waived by the coordinator with a stated reason.

— Independent audit
