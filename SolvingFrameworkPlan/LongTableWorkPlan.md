# Long Table work plan: adversary and structural candidate sets

4 October 2026, revised to conform to [JointMassMacroExecutionPlan.md](JointMassMacroExecutionPlan.md) (the joint plan). Where this plan and the joint plan differ, the joint plan governs.

**Our share,** explicitly accepted:
- adversary tooling;
- structural candidate-set proposals;
- our own errata;
- statement review for the completion bridge.

**Not ours:**
- the corpus sweep, quantifier review, support transport and filling proofs (math and scale-up);
- status words, revision 39 and the ledger (navigator).

**Execution awaits the user's release.** Nothing below starts before then, and acceptance is never inferred from silence.

## Ground rules

- **Naming:** navigator id `structural-mass-descent`, "mass-macro descent" in prose. Never "D2", which identifies the historical signed Penrose work.
- **The contract** is the joint plan's, verbatim:
  - p = max(0, #colours on B − 3);
  - q = Σ |K∖B|² over all six pairs and every component meeting B;
  - R = (6n²+1)p + q;
  - macros of at most two whole-component swaps, recomputing components after the first. Intermediate ranks may rise; the final rank must strictly fall. Stop at p = 0.
- **Graph identity:** order, zero-based graph index, exact ASCII rotation, and the hash of that ASCII. Whole-file hashes are checked against `search-results.json`. These are file hashes, not line hashes, and we will not invent a line-hash convention.
- **Every result file states:**
  - its scope;
  - input and checker hashes;
  - the formula version and macro bound;
  - the root;
  - total colouring orbits and the non-target count;
  - the outcome.
- **Every failure witness gives:**
  - the full colouring with its vertex order;
  - the start rank;
  - all one- and two-step successor ranks, with enough component and move data to certify completeness.
- **Empty colouring families** are reported explicitly, never as vacuous passes.
- **Tooling:** standard library only. Any other dependency is named.
- **Wording:** we report factual pass/fail outcomes, and the navigator assigns statuses.
- **Files:** we commit only our own files, and we do not edit shared files while another team owns an update.

## Failure classification (joint plan, used everywhere)

| Observation | Refutes |
|---|---|
| A colouring with no decreasing macro at root r | `Good(T, r)` |
| A proposed set S(T) contains one failing root | The every-member guarantee of that set |
| The stated tie-break/Select actually returns a failing root | That selector only |
| Every degree-five root has a failing colouring | The existential mass-macro claim |

None of these refutes Four Colour or bare Kempe reachability.

## WP1: Invariance argument (first, on paper)

Write a short proof that mass descent is invariant under graph relabelling and global colour permutation.
- Both bijections preserve B, bichromatic components and their sizes, the legal one- and two-swap macros, and therefore R.
- So Good(T, r) transports along isomorphisms, and counterexamples transport with it.
- Note explicitly that the label-sensitive (σ, β) game does **not** inherit this.

Deliverable: a section in our first report, for the math team's quantifier review. Exact automorphism-orbit computation is an optional diagnostic, not a prerequisite.

## WP2: Regression fixtures (named graphs only)

Reproduce only these fixtures, from the corpus files and published results:

1. Graph 36 (order 20, zero-based index 36): the eight exterior degree-five roots of anchor 0 are 8, 10, 11, 13, 14, 15, 16, 19. Only root 8 loses (σ, β), with 5 of 55 observations losing.
2. Graph 36, root 8, mass descent:
   - 198 orbits, of which 131 are non-target;
   - with one swap, exactly 3 stuck orbits, the first at rank (1,190) with successors (1,190), (1,206), (1,207), (1,211) and (1,228);
   - with two swaps, every non-target orbit decreases, matching the stored intermediate states in `afternoon-checks.json`.
3. The icosahedron: every root passes, with a target within one swap.

**Also:**
- **Permutation regressions:** randomly relabel the vertices and colours of graph 36, then confirm that the counts and outcomes at the image root are unchanged. This catches implementation errors; it does not prove anything.
- **No second whole-corpus enumeration.**

**Done when:** all named fixtures reproduce with hashes recorded, and the shared report format is confirmed with the math team. That is the joint plan's regression checkpoint.

## WP3: Adversary (`adversary.py`)

- **Loader:** reads the per-root mass-macro results the math team publishes, and the existing (σ, β) results, with file hashes checked. Until the mass table exists, it only recomputes the WP2 fixtures.
- **Rule interface:** a candidate set `S(rotation) -> set of roots`, an optional tie-break, and the named check it targets: mass descent or (σ, β). The two are never mixed silently.
- **Output:** one command classifies a rule into the four outcomes above. It gives the first failing graph per outcome, with a pointer to the underlying witness in the published files. It reports the cost of computing S separately.

**Done when:** it reproduces the known (σ, β) smallest-label failure at graph 36, root 8 from published results. After that, it classifies S0 and S1 against the mass table once that table exists.

## WP4: Structural candidate sets

Every proposal must state, before evaluation:
- its definition in symbols;
- a proof that it is nonempty;
- a proof of S(T) ⊆ D(T);
- a proof of equivariance;
- the tie-break;
- the check it targets.

- **Nonemptiness of D(T):** in a triangulation with minimum degree five, Euler gives Σ(6 − deg v) = 12. Only degree-five vertices contribute positively, so |D(T)| ≥ 12 + Σ_{deg v ≥ 7}(deg v − 6) ≥ 12. We will write this out in full.
- **S0 = D(T):** the baseline. Its every-member guarantee fails when *any* root fails. That is not the existential claim, which needs every root to fail. Its useful output is the per-graph fraction and the structure of the failing roots.
- **S1 (predeclared now):** S1⁺ = arg max and S1⁻ = arg min over D(T) of the number of degree-five neighbours. Both are nonempty because D(T) is, and equivariant because degree is.
- **S2 (deferred until fully specified):**
  - the actual redistribution rules;
  - a proof that total charge is conserved;
  - equivariance;
  - a proof that every positive receiver has degree five (charge 12 alone does not give this);
  - nonemptiness.

  S2 is not evaluated until all five are written down.
- **Holdout:**
  - Descriptive root statistics, such as second-ring degrees, distances between degree-five vertices and charge, are examined on orders 12–18 only.
  - Any rule they suggest is frozen in writing, then tested on orders 19–20.
  - S0 and S1 are declared before any mass results exist, so they may be evaluated on the whole corpus.
  - Extending past order 20 needs the joint agreement the plan requires.

## WP5: Completion statement review

Review the math team's statements as they are drafted:
- support transport to `Fin s`;
- corner insertion under the actual `faceNext` convention;
- bridge insertion merging two face dart-orbits;
- chord insertion splitting one face dart-orbit;
- existence of eligible insertions, including cut vertices and repeated face walks.

We will respond in short files and will not author Lean on that track.

## WP6: Our own errata

*The two document errata below were applied on 4 October, before release, because they correct our own wording. The play edits wait for release.*

- [LongTableJointReply.md](LongTableJointReply.md):
  - the D2 name is withdrawn in favour of `structural-mass-descent`;
  - the "no objection means agreed" sentence is withdrawn;
  - the S0 claim "fails exactly when MMD fails" is withdrawn.
- [LongTableResponseRev39.md](LongTableResponseRev39.md): its suggestion (a) is replaced by the WP1 proof obligation.
- The plays:
  - remove the Catalan-42 claim;
  - take interior swaps off "DEAD";
  - change "only live shape" to "one live shape";
  - change "label-invariant" to "structural candidate set";
  - add a note that root 8 passes the tested mass macro.

  They remain labelled fiction.

## Order of work

1. After release: WP6 (documents) and WP1 (invariance argument).
2. WP2 regressions. Then **regression checkpoint**: confirm the format with the math team.
3. WP3 adversary on the fixtures and published (σ, β) results.
4. **Wait** for the math team's mass-macro corpus table.
5. WP3 on mass results; WP4 S0/S1 evaluation; WP4 descriptive statistics on orders 12–18 only.
6. One joint report to both teams in `SolvingFrameworkPlan/`.

WP5 runs whenever the math team posts statements.

## Stop rules (joint plan §6)

- **Every degree-five root fails on some graph:** stop all candidate-set fitting for this formula. Help inspect the full witness for a move mechanism or missing interaction. Do not lengthen the macro or rename an attractor rank as a formula.
- **The corpus passes:** more sweeps are not progress. Our next useful output is a candidate structural lemma for the decrease, or a frozen selector with its own proof obligations.
- **A permutation regression changes an outcome:** treat it as an implementation bug, stop, and report before any further results.
