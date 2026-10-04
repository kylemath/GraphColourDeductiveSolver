# Joint mass-macro execution plan

4 October 2026. Submission to the Proof Navigator, math and scale-up, and Long Table teams.

This consolidates the joint letter, the five mathematical corrections, the navigator's proposed revision 39, and Long Table's accepted subplan. The two navigator attachments are identical and represent one proposal. This document authorizes no experiment or implementation by itself: the user will circulate it before individual work starts. Only this Markdown plan is being saved now; no code, navigator board, status, proof, or fixture is changed.

## Objective and current boundary

The objective remains a structural constructive Four Colour proof without a large configuration census, followed by proved termination and a separately justified polynomial algorithm. Gate D is open. Finite searches are adversarial research tests, not a substitute proof.

The immediate attack is **mass-macro descent**, navigator id `structural-mass-descent`. Do not reuse `D2`, which already identifies the historical signed Penrose work. Keep earlier tracks and failures visible in the living tree.

The current board is revision 38. Revision 39 is a proposal for the navigator team to implement after review; it has not been applied by this document.

The checked foundation is unchanged: Five Colour, spherical degree-four extension, the eleven-vertex result, elimination certificates, the spherical icosahedron, and six exterior degree-five roots. The unified source rebuild passed all 41 custom modules and guarded tests with 493 cached custom artifacts excluded and unchanged source hashes. These are not downgraded by an open four-colour obligation.

Research evidence is also unchanged:

- The 118 triangulations through order 20 contain no targetless class among 1,626 tested Kempe classes at 1,586 roots. This is recorded computation, not uniform coverage.
- Strict one-swap component-mass descent is killed at graph 36/root 8: three stuck orbits among 131 non-target orbits.
- At that one root, every non-target orbit decreases the same formula within two swaps. The mass-macro corpus sweep has not been run.
- The smallest-label exterior root with `(sigma,beta)` is killed. At graph 36, the eight exterior degree-five roots are `8,10,11,13,14,15,16,19`; only 8 loses that observation game. Root 8 nevertheless passes the tested mass macro.
- Play experiments, nesting counts, potentials 1–4, and first-ring comparisons are fiction, not findings.

## Mathematical contract

Let T be a nonempty finite simple spherical triangulation with n vertices and minimum degree at least five. Define `D(T) = {r : degree_T(r)=5}`. For a proper four-colouring c of T minus r, put `B = neighbors_T(r)` and

```
p(c) = max(0, number of colours on B − 3)
q(c) = sum |K minus B|²
R(c) = (6n²+1) p(c) + q(c).
```

The sum runs over all six unordered colour pairs and every connected bichromatic component K meeting B. This is the existing formula, not a second rank. Since `p` is 0 or 1 and `q ≤ 6n²`, `0 ≤ R ≤ 12n²+1`. Stop as soon as `p=0`; terminal states need not have `q=0`.

A move exchanges the two colours on one entire bichromatic component, including components missing B. The candidate allows sequences of length **at most two**, recomputing legal components after the first swap. Intermediate ranks may increase. The final rank must strictly decrease. Proper colouring is preserved throughout.

Define `Good(T,r)` to mean: every proper deletion colouring with `p=1` admits such a decreasing sequence. The existential mathematical target is

```
for every T in the class, there exists r in D(T) such that Good(T,r).
```

The root is chosen before the colouring. Exterior roots of one anchor are a regression set, not the universal quantifier. A smaller candidate class or a root chosen after observing c must be recorded as a different statement.

Efficient selection is a separate obligation: a polynomial-time `Select(T)` returning a good root, or a polynomial-time nonempty structural set `S(T) ⊆ D(T)` whose **every member** is good, followed by deterministic tie-breaking. A single vertex cannot be selected equivariantly on every vertex-transitive graph. Equivariance therefore concerns the set; the tie-break may use labels without making the complete procedure equivariant.

If descent and selection are proved, strict integer decrease gives at most `12n²+1` macros. At a current colouring there are at most `3(n−1)` bichromatic components across the six pairs, so testing both one- and two-move sequences fits within the conservative `(6n)²` candidate bound. Component extraction, rank evaluation, reconstruction, completion and selection still require explicit cost accounting. This is a conditional local search bound, not a proved complexity theorem for the recursive solver.

## Failure classification: corrections to both subplans

Use four different conclusions:

| Observation | What it refutes |
|---|---|
| A colouring without a decreasing macro at one root | `Good(T,r)` for that root |
| A proposed set contains one failing root | The guarantee that every member of that set is good |
| The specified tie-break/Select actually returns a failing root | That particular selector |
| Every degree-five root has a failing colouring | The existential mass-macro claim |

**Correction to Long Table S0:** `S0(T)=D(T)` is a useful baseline, but its every-member guarantee fails when **any** root fails. It does not fail exactly when the existential claim fails; that requires every root to fail. Conversely, a candidate set containing a bad root does not automatically show that a fixed tie-break chooses it.

**Correction to S2:** total charge 12 proves some vertex receives positive charge only if redistribution conserves total charge. It does not prove that every positive receiver has degree five. A degree-five candidate-set proposal must prove that restriction, as well as nonemptiness and equivariance, before claiming a selector guarantee. S1 extrema are nonempty once `D(T)` is proved nonempty; the relevant Euler argument must be supplied.

No failure here refutes Four Colour or bare Kempe reachability. Do not lengthen the macro beyond two to improve the pass rate without a new structural argument and a separately stated candidate.

## Responsibilities and acceptance

| Team | Share | Acceptance recorded here |
|---|---|---|
| Navigator | Evidence, status words, revision 39, ledger reply and board regressions | Its reply specifies this scope; no census, adversary or Lean work |
| Math and scale-up | Corpus implementation, replayable witnesses, quantifier review, support transport and filling proofs | Proposed work our team offers; execution awaits the user's release |
| Long Table | Adversary tooling, structural candidate-set proposals and its own errata | Explicitly accepted in its supplied subplan |

Acceptance is never inferred from silence. Proposed new work and changes to another team's scope need an explicit response. Long Table may describe factual pass/fail outcomes; the navigator assigns board statuses. Each team commits only its own changes and avoids shared-file edits while another team owns an update.

## Work packages and dependency order

### 1. Ledger and statement review — navigator

Implement revision 39 without changing `docs/navigator/index.html`. Insert `structural-mass-descent` under `structural-gate-d` before moving the existing killed one-swap and computed two-swap nodes into it. Preserve their ids and statuses. Add the universal statement, the separate selection obligation, and the corrected failure classification above.

Create the proposed corpus, candidate-set, adversary, support-transport and edge-insertion nodes using the names in the navigator attachment. Keep `structural-mass-select`, `structural-mass-corpus`, `structural-candidate-set`, and `structural-rule-adversary` unstarted. Keep the general gate and the universal mass-macro node exploring. Edge insertion is exploring as a statement under review, not started Lean work. The recursive-certificate alternative remains exploring and is not the active theorem.

Record graph 36's observation-game results separately from mass descent. Preserve Five Colour, the icosahedron, the six-outside theorem, order eleven and the killed anchor rule. Add one journal entry recording the corrections and actual acceptance states. Save `MassMacroLedgerReply.md`.

Extend and run the existing navigator regression checks for parent placement, preserved statuses, new unstarted nodes and absence of `structural-d2`. Moves to the new mass parent must be the final effective moves for those ids. The board remains the sole status ledger.

### 2. Shared evidence contract and regressions — math plus Long Table

Use the existing `backgroundMaterial/planemap-structural/` folder and SHA256 manifest. Identify a graph by order, **zero-based** graph index, exact ASCII rotation and hash. Check whole-file hashes against the recorded census; compare each graph's ASCII record with its corresponding published record. Existing file-level hashes are not per-line hashes. If line hashes are added, specify newline/normalization conventions.

Results must include scope, input and checker hashes, formula version, macro bound, root, total proper colouring orbits, non-target count and pass/fail outcome. Failure witnesses contain a full colouring with vertex order, start rank, and all one-/two-step successor ranks. Store enough move/component information or a reproducible checker to certify completeness, rather than merely sampling successors. Empty colouring families must be identified explicitly; vacuous conditional descent is not an existence proof of a deletion colouring.

Long Table reproduces only named regression fixtures, using the standard library: graph 36's eight exterior roots; its three one-swap local minima and two-swap escapes; and the icosahedron. Other dependencies should be explicit. No second whole-corpus enumeration is needed for the adversary.

### 3. Mass-macro sweep — math and scale-up

After execution is released, run all 118 graphs at **every degree-five root**, not just exterior roots. Verify properness, colour-renaming quotient completeness, component moves and rank arithmetic. Report per-root outcomes and per-graph good-root sets.

On encountering a failing root, save its witness and continue through that graph's remaining roots to classify the existential claim. Stop and report immediately if every degree-five root fails. A corpus pass is computed evidence only. Do not extend to order 21 merely to avoid inspecting a failure; agree on an extension after the existing sweep is reviewed.

The enumeration harness may be exponential. It tests a polynomially evaluable formula; it is not the proposed solver. An executable solver must generate macros from the current colouring without enumerating its entire colouring space.

### 4. Adversary and structural sets — Long Table

Build a loader and rule interface consuming published per-root results. Before the mass table exists, recompute only named regression graphs. A single command should classify a rule by the four outcomes above and point to the underlying witness.

Mass descent is invariant under graph relabelling and global colour permutation: these bijections preserve B, bichromatic components, component sizes and legal macros, hence preserve R and transport counterexamples. Write this argument first. Use permutation regressions to catch implementation errors. Exact automorphism-orbit checks are optional diagnostics; they must not become an unbounded prerequisite for the plan.

The label-sensitive `(sigma,beta)` game does not inherit this invariance automatically. State which check a candidate set targets.

Evaluate S0 and predeclared S1 extrema against mass pass sets. Specify S2's actual redistribution rules, conservation, equivariance and positive-receiver restriction before evaluation. Descriptive root statistics may suggest later proposals, but freeze a rule before testing it on graphs held out from its discovery. The corpus must not silently serve as both training and independent validation.

### 5. Completion bridge — math with Long Table statement review

Proceed beside the mass experiment after execution is released:

1. Transport the nonisolated support to `Fin s`, including rotation, filling, degrees and colouring restriction.
2. Define corner insertion using the actual `faceNext` convention.
3. Prove bridge insertion merges two face dart-orbits and preserves filling.
4. Prove chord insertion splits one face dart-orbit and preserves filling.
5. Prove eligible insertions exist until connected triangulation is reached, handling cut vertices and repeated face walks explicitly.

Distinct nonadjacent endpoints preserve graph simplicity. The remaining obligations are eligible corners, rotation updates and filling; simplicity does not await a diagonal-existence theorem.

For a bridge, an even cycle has zero coefficient on the new edge. A promising filling proof normalizes old face coefficients by a constant on one component so the two faces agree before merging; verify this algebra in the carrier. For a chord, prove the old face boundary equals the sum of the two new boundaries and handle cycles using the new edge by adding one new face boundary.

Each valid insertion increases the edge count, so a justified finite edge bound can organize completion termination. It does not establish insertion availability. Outer colouring induction uses support size, which completion preserves and deletion decreases. Adding edges does not preserve Kempe components; transport proper colourings by graph inclusion, not swap histories.

### 6. Structural explanation and certificate fallback — joint review

If the corpus kills mass-macro descent, stop structural-set fitting for that formula. Inspect the complete witness for a move mechanism or missing interaction. Preserve the failed candidate in the ledger; do not rename an attractor rank as a structural formula.

If it survives, identify a structural lemma explaining the decrease and test any explicit selector separately. A larger passing sweep does not supply that lemma.

The fallback is one possible restriction to induction-produced inputs, not the only restricted-input approach. It needs a named polynomially checkable certificate, a proof that it implies the required escape, and preservation under the actual deletion/completion/reconstruction steps. “Extendible” and “the recursion's outputs happen to pass” are not substitutes. No new boundary interface is required before that invariant is named.

## Our concrete contribution

The math and scale-up team offers to implement the exact mass-macro sweep and independent witness replay, review the quantifiers, prove support transport, and formalize filling-preserving insertion once its statements are agreed. The full spherical degree-four execution fixture and executable reconstruction remain useful parallel engineering work, but neither crosses Gate D. We will not modify the navigator on another team's behalf or duplicate Long Table's corpus-consuming adversary.

## Checkpoints and decision gates

1. **Agreement checkpoint:** teams explicitly accept their shares and the corrections to S0, candidate-set failure classification and S2. The navigator reviews revision 39.
2. **Regression checkpoint:** named fixtures reproduce and the shared report format is understood.
3. **Corpus checkpoint:** a replayable existential kill witness, or a complete finite pass/fail table with no mathematical status inflation.
4. **Mathematical checkpoint:** one explicit descent/selection lemma or one named preserved certificate. Without this, computation has not crossed the divide.
5. **Generalization checkpoint:** completion and support induction compose with the proved reduction; executable selection and full cost accounting are discharged separately.

Replies should be short files in `SolvingFrameworkPlan/`, citing the canonical fixtures. One joint report goes to both teams. Do not treat more green leaves, more experiments or more code as progress on the open universal lemma unless they supply the missing mathematical argument.
