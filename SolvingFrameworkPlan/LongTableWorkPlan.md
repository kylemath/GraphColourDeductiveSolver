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

**Execution awaits the user's release.** Nothing below starts before then, and acceptance is never inferred from silence. *(Released 4 October; see progress below.)*

## Progress, 4 October evening

### Work packages

| WP | State | Evidence |
|---|---|---|
| WP1 invariance argument | Written; awaiting the math team's quantifier review. The empirical check agrees: in all 118 graphs, failing roots form unions of automorphism orbits. | `longtable/InvarianceNote.md`, `automorphisms.json` |
| WP2 regression fixtures | All 32 checks pass. The graph-36 permutation runs show (σ, β) changing outcome under relabelling while mass-macro results do not. | `regressions.json`, report 1 |
| WP3 adversary | Built. It consumes the published mass table and reproduces the anchor-rule failure. | `adversary.py`, report 2 |
| WP4 candidate sets | S0, S1+ and S1− each contain a failing root in some tested graph, so their every-member guarantees fail. No graph has every root failing. Discovery on orders 12–18 found no simple local-degree rule worth freezing. S2 is not specified. **Orders 19–20 are untouched.** | report 2 |
| WP4b broadening (two predeclared rounds) | Eight alternative ranks shrink discovery failures to the single orbit {4, 6} of order 17, graph 0; none reaches zero, so none advanced. Two rank variants (rep and Lonly) are refuted outright. | `broaden-discovery*.json`, report 3 |
| WP5 completion review | Done. The math team prefers the direct coefficient proof; `FaceCorner.lean` now gives faces of length ≥ 3 at minimum degree two. | `EdgeInsertionReview.md` |
| WP6 errata | Done for the documents and both plays. | — |
| Root 4 versus root 8 | Done, and replicated by the math team (`MathLongTableResponse3.md`). | `compare-roots.json`, report 3 |
| Trap demo | Published at `docs/trap/` and linked from the site. | `trap_demo_data.py` |

### What the trap taught us

1. **The failure is a basin, not a plateau.** Escaping the trap at root 4 takes three swaps, with R climbing +20 first. Root 8's stuck states escape in two swaps with a climb of at most +4.
2. **The trap is the tidiest state nearby.** It is the minimum of every tested cheap score over its whole two-swap neighbourhood, so reweighting a monotone "tidiness" score cannot help. Crediting boundary-linking chains (q − k·links) also changed nothing.
3. **Its boundary is fully locked.** Each singleton is chained to another boundary vertex in all three of its pairs, and the repeated colour is chained through a singleton. The math team's pair profile adds detail: at root 4 the three pairs of singleton colours (12, 13, 23) each contribute 36, from one chain of exterior mass 6 joining two singletons. Root 8's colouring has the same σ and the same q, but a different profile, and it descends in one swap.
4. **New: avoidance is exact at this fixture.** At each failing root (4, 6, 9, 14) of order 17, graph 0, every colouring except the trap itself descends to a target along a strictly decreasing two-swap path that never enters the trap. For example, 53 of 54 colourings descend at root 4. So at this fixture, "the recursion never hands over this one colouring" is exactly the missing condition. This is finite evidence, not a certificate: the condition still has to be named, checkable, preserved by deletion and reconstruction, and not a restatement of extendibility.

### Our answers to the math team's three questions

- **Q2, the joint rank-and-set gate:** we **accept** it. Freeze the rank and the equivariant candidate set together, require zero bad members in discovery (orders 12–18), and use orders 19–20 once for the frozen pair. We will not amend the screening protocol or reuse holdout results.
- **Q1, isolating one interaction:** taken up as WP7 below.
- **Q3, the precise Jordan lemma on repeated face walks:** taken up as WP10 below. We accept that `alternating_walks_intersect` does not apply directly, since it is a centred-star theorem. We also adopt their termination measure: the number of missing vertex pairs, bounded by choose(s, 2).

## Next work packages (proposed, in order)

### WP7: the singleton-chain interaction (answers Q1)

> **Update, 4 October, late.** The math team released WP7 with a correction: Π alone cannot separate states with the same σ. WP7 was declared (`longtable/WP7-declaration.md`, commit `880c323`) and tested on discovery (`longtable/WP7-results.md`):
> - **Exact statements:** locality (Lemma 7.1), re-partition (Lemma 7.2), and Kempe's full-lock lemma (Lemma 7.4).
> - **Conjecture 7.3, mass dominance, is refuted** by the order-17, graph-3 short-circuit traps.
> - **Next:** the dynamic re-partition question below. Meanwhile, breadcrumb descent (the user's idea, swept by the math team) passes all 1,586 roots with at most 4 warnings. Its warning bound is the main open obligation.

**Statement first, then test.** Define the *singleton triangle* Π(c): for every pair {x, y} of singleton colours on B, the {x, y}-component containing the x-singleton also contains the y-singleton. A conjectured mechanism to test:
- when Π holds, every swap of a chain that touches the repeated colour merges mass into those three linking chains, which raises q;
- this is why the first step out is uphill.

**Test.**
- Count Π across all non-target states at the 279 discovery roots, comparing two-swap-stuck states, one-swap-stuck states and the rest.
- Report whether Π, possibly with the repeated-colour chain condition, separates the trap from root 8's same-σ, same-q colouring.

**Deliverable:** a stated interaction lemma *with quantifiers*, or a counterexample state that refutes the mechanism. Target distance stays diagnostic only.

> **Update, 4 October (evening, later):**
> - **WP7b:** H-A and H-B refuted; H-C survives but is not distinctive.
> - **WP7c:** injective pattern charging refuted, by the twins at order 17, graph 3.
> - **WP7d:** the fixture structure.
>   - It has five pits of trap and twin, ten connectors at R 1873, ten spurs at R 1866, and stabiliser order 10.
>   - The toggles are two-vertex chains at the opposite hub, and they never combine.
>   - C7d has no kill in 39 runs, with an exact maximum fibre of 3.
> - **WP7e:** Lemma S (one toggle per hub) is proved by hand for every vertex of degree ≥ 5 outside N[r]. It is sent to the math team for checking and possible Lean work.
> - **Next, pending joint agreement:** targeted search for C7d failure with distant hubs.
> - The WP7 Lean lemmas 7.1, 7.2 and 7.4 compile (Proof Navigator revision 45).

### WP8: a joint rank-and-set candidate (only if WP7 suggests one)

- Freeze the rank and an equivariant candidate set together.
- Discovery gate: zero bad members on orders 12–18.
- Then evaluate on orders 19–20 exactly once.
- Hand any survivor to the math team for the official sweep.

### WP9: from avoidance to a certificate

1. **Is the trap ever produced?** Run a concrete, fully specified recursive colouring (degree-≤4 extension plus two-swap descent at a fixed good-root rule) on the corpus graphs, and record whether it ever hands a trap colouring to a failing root. This gives evidence about what the recursion produces; it is not a proof.
2. **Name a candidate.** Look for a checkable property P that excludes all four trap states at order 17, graph 0 (and later traps), implies that a two-swap descent exists, and could plausibly be reproduced on reconstruction. Candidate shapes include "Π fails" and "some singleton is free in some pair after one swap".
3. **Report or stop.** Report P with its preservation obligation stated, or stop if every natural P is just a restatement of extendibility.

### WP10: the Jordan lemma statement for chord availability (answers Q3)

State the lemma for a face of length ≥ 4 in a connected, full-support spherical map, covering:
- choosing corners when the face walk repeats vertices;
- extracting a simple cycle from the face walk plus a hypothetical diagonal;
- why that cycle separates the two ends of the other diagonal, using the proved even-set/Jordan separation result rather than the star theorem.

**Deliverable:** a statement for the math team to formalise or reject.

### Not planned

- Longer macros.
- New observation games.
- Orders beyond 20 (pending joint agreement).
- Any status words; the navigator assigns those.

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
