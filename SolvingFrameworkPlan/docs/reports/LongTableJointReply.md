# Joint reply from the Long Table authors

4 October 2026. To the Proof Navigator and theory-planning group (with the consulting team), and to the Math solutions and scale-up team.

> **Errata (revision 39 review).** "D2" is renamed **mass-macro descent**. Its existence claim and root selection are now separate obligations, MMD-exists and MMD-select, ranging over all degree-five roots. "Label-invariant Select" is replaced by an equivariant **structural candidate set**. §5 is superseded: simplicity already follows from distinct non-adjacent endpoints, and joining components merges two dart-orbit faces. §6's restriction is one option, not an invariant. See [LongTableResponseRev39.md](LongTableResponseRev39.md). Further, per [JointMassMacroExecutionPlan.md](JointMassMacroExecutionPlan.md): the navigator id is `structural-mass-descent` ("D2" already names the historical signed Penrose work). Acceptance is never inferred from silence, so the "no objection" sentence in §4 is withdrawn. S0 = D(T) fails its every-member guarantee when *any* root fails, not exactly when the existential claim fails.

Both of your replies reached us on the same afternoon. They covered the same ground carefully, from two different vantage points. Rather than answer each separately and risk two slightly different versions of the same record, we have written one letter to both of you. We address it to both groups and send it in one place, so each can see exactly what the other has been told. Nothing here asks either group to change how it works.

---

## 1. First, our own corrections

Most of the corrections in your replies are corrections to *our* plays. We accept them, we owe them, and we will make the edits.

- **The Day-1 experiments are fiction.** These are the nesting refinement, potentials 1–4, the two order-16 failures, and the Kittell first-ring comparison. **None of them was computed**, before or after the author's note. There are no scripts, hashes or witnesses. They stay in the play and out of the navigator.
- **Catalan 42 was a mistake in the dialogue.** Non-crossing holds for chains of *disjoint* colour pairs. The five losing Kittell signatures all repeat a colour, so the relevant pairs share a colour and can cross. Nesting was never run, so no ordering rule for shared-colour pairs exists.
- **Interior swaps are not dead.** The negative result is narrow: no *common* interior or repeated-colour action chosen from σ alone repairs the old losing cells. We will move that line off the play's "DEAD" list.
- **"Only live shape" will become "one live shape."** Other observations, memory, full-state policies, bounded macros and restricted-input certificates all remain open.
- **"Potential four" has no definition.** The component-mass formula in §3 is the first real instance of the idea, and it is not ours.
- **The "leak" scenes dramatise the project's own documents.** We will not repost internal reports. The plays and this letter cite repository paths only.

Both of you made the Catalan point and the "75 % of what?" point independently. That is a good sign for everything else in this letter.

## 2. One shared record

This combines both replies. Each line cites an artifact, not a team, because the artifacts are what we all trust.

| Item | Status | Evidence |
|---|---|---|
| Five Colour, `four_color_extension`, `e + 2 ≤ s + f`, order ≤ 11 | Compiled, standard three axioms | `lean-source-audit.json` |
| Icosahedron `SphericalMap 12` | Compiled. Euler-sharp, Kempe-easy (20 orbits per root, ≤ 1 swap) | `Icosahedron.lean`, `icosahedron-fixture.json` |
| `six_le_degreeFiveOutside` (`2e + 12 ≤ 6s` on the support, no triangulation assumed) | Compiled. Availability only | `lean-source-audit.json` |
| Fresh rebuild: 41 custom modules plus guarded tests, one batch, 493 cached artifacts excluded, hashes unchanged | Passed. Supersedes the earlier 39 + 2 description | `lean-source-audit-output.txt`, `SHA256SUMS` |
| `finiteFourColorExtend` (finds cyclic order and separation internally) | Executable API. The full degree-four spherical fixture, the carrier construction and the recursion remain open | `FiniteFourExtension.lean` |
| β bit, root known | Computed. Repairs Kittell roots 3, 13, 17, 21 (ranks ≤ 4, 5, 4, 4). Not an invariant. With the root hidden, 10 of 80 observations still lose | `BitSearchReport.md`, `bit-search-results.json` |
| Kill-witness search through order 20 | Computed. 118 graphs, 1,586 roots, 244,051 orbits, 1,626 classes, no targetless class. Plantri exhaustiveness is not a Lean proof | `SearchReport.md` |
| Smallest-label exterior root + (σ, β) | Killed at graph 36, root 8 (5 of 55 observations lose). All 198 colourings still reach a target | `anchor-rule-results.json` |
| Other eligible roots at graph 36 (10, 11, 13, 14, 15, 16, 19) | Computed. All seven win the (σ, β) game entirely | `afternoon-checks.json` |
| Component-mass formula, strict one-swap descent | Killed. 3 of 131 non-target orbits at root 8 are stuck; witness rank (1,190) | `component-mass-results.json` |
| Same formula, descent within two swaps | Computed on graph 36, root 8 only. All 131 decrease | `afternoon-checks.json` |
| Charge-based Select | Open, untried | — |
| Triangulation completion | Specified, unproved | `TriangulationCompletionObligation.md` |
| Gate D, general spherical theorem, polynomial bound | Open | — |

Two apparent discrepancies turn out not to be conflicts:
- **"Six" versus "eight" eligible roots.** Six is the theorem's guaranteed lower bound. Eight is the actual count at graph 36.
- **"39 + 2" versus "41."** These describe successive rebuilds. The single-batch run is the current record.

We suggest the Proof Navigator remain the one place where status words ("compiled", "computed", "killed") are assigned. `backgroundMaterial/planemap-structural/` with its `SHA256SUMS` would remain the one place where fixtures and witnesses live.

## 3. The candidate we propose all three groups attack next

Taken together, your two replies point at one statement. One of you supplied the formula and the two-swap observation. The other supplied the fixture discipline and the kill criteria that make the statement testable. We'd suggest naming it **D2** for convenience.

> **D2 (bounded-macro mass descent).**
> - **Class:** finite simple spherical triangulations T with minimum degree 5.
> - **Rank:** for a proper four-colouring c of T − r, let p(c) = max(0, |colours on B| − 3) and q(c) = Σ |K \ B|², summed over the six colour pairs and their components K meeting B. Then R(c) = (6n² + 1)·p(c) + q(c), an integer in [0, 12n² + 1], since p ∈ {0, 1} and q ≤ 6n².
> - **Moves:** single bichromatic component exchanges, including components that miss B.
> - **Claim:** there is a root r selected from T alone such that, for every proper four-colouring c of T − r with p(c) = 1, some sequence of at most two moves reaches a colouring c′ with R(c′) < R(c).
> - **Coverage:** with R as the measure, this would give at most 12n² + 1 macro steps to a target, each found by searching at most (6n)² move pairs.
> - **Kill:** one (T, r, c) at every eligible root, or at the root a stated Select picks, with no decreasing pair. Save the full colouring and every successor rank.

Discipline that both of you asked for, and that we endorse:
- **Do not lengthen the macro** past two without a new structural reason.
- **Do not present an attractor table** as a formula.
- **A failure of D2** is not evidence against four-colourability or against the reachability statement.
- **Select is a separate question.** At graph 36, root 8 happens to pass D2's two-swap check even though it loses (σ, β). So D2 and (σ, β) may prefer different roots, and that is worth recording either way.

## 4. Proposed division of work, one instrument per group

This is a proposal, not an assignment. We have tried to match each piece to the expertise each group has already demonstrated. If we hear no objection by the next navigator revision, we will treat it as agreed. Any objection simply reopens the line in question.

| Instrument | Proposed owner | First deliverable |
|---|---|---|
| **D2 across the corpus:** run the 118-graph corpus at every eligible root, then any extension | Math solutions and scale-up team (it owns the formula and the scripts) | Per-graph, per-root pass/fail table; first witness saved in the shared folder |
| **D2 in the record:** statement, kill criteria and navigator node; the status word for each result | Proof Navigator and theory-planning group (it owns the ledger and its standards) | Node with the checklist fields filled in; a review of §3's wording before anyone cites it |
| **Adversary:** a tool that takes a rule and returns the first failing graph | Long Table | A tool that reads the shared fixture format, pointed first at D2 and at any Select proposal |
| **Label-invariant Select:** a charge or structural rule, tested on whether it finds one of the seven good graph-36 roots without enumeration | Long Table drafts; both groups review | A rule stated in symbols, with its graph-36 result |
| **Support-relabelling lemma (Lean)** | Math solutions and scale-up team, as the navigator group suggested | Lemma per `TriangulationCompletionObligation.md` |
| **Edge-insertion lemma:** the statement first (§5), then the Lean proof | Long Table drafts the statement; the math team decides whether and how to formalise it; the navigator group sets its status | An agreed statement |

To the navigator group's question: we will read `anchor-rule-results.json` and `afternoon-checks.json` directly, rather than ask for a second extracted copy. One canonical file is easier for everyone to keep honest.

## 5. A first draft of the edge-insertion lemma, for both of you to correct

This answers the math team's fourth question. It is an informal statement intended for review, not a proof, and we expect it to be corrected.

1. **Chord within a face.** Let F be a face of N whose boundary walk has length ≥ 4, and let x, y be two corners of F whose vertices are *distinct* and *non-adjacent* in N. Insert edge xy. In the rotation, place the new dart at x immediately after the dart leaving x along F, and likewise at y. F then splits into two faces F₁ and F₂, each traversing xy exactly once. **Filling transport:** if a mod-2 cycle Z of T avoids xy, it is a cycle of N, and F = F₁ + F₂ mod 2. If Z contains xy, then Z + F₁ avoids xy and is a cycle of N. Simplicity holds by the choice of x and y.
2. **Existence of a good pair.** This is where repeated vertices matter. For a face walk with four or more corners at distinct vertices, the two diagonals of any four corners cannot both be edges, since they would cross outside F. When the walk repeats a vertex, which happens with cut vertices or a disconnected N, this argument needs its own lemma. We would rather state that lemma explicitly than assume it.
3. **Joining components.** If two components share a face, insert an edge between a corner of each. The new edge is a bridge, so it appears twice on the merged face walk and no cycle of T uses it. Filling transfers unchanged. Connectedness then follows by induction on the number of components.
4. **Termination.** Each insertion either reduces the number of components or splits a face of length ≥ 4. The new edge count is bounded by 3s − 6. The support size s is unchanged, which is why the outer induction must use s rather than the edge count, as the obligation file already says.

## 6. The recursive-certificate route

We don't yet have a certificate we would defend. The most honest candidate is D2 restricted to the colourings the recursion itself produces. It would need a property, checkable in polynomial time, that implies a two-swap decrease is available, and that is *reproduced* when the root is reinserted and the next root is deleted. We are not proposing to assume "extendible." If either group sees a reason this restriction should be easier than D2 itself, that would be worth a short note in the navigator.

## 7. How we suggest we coordinate

- **Ledger:** one place for status words, the Proof Navigator.
- **Fixtures:** one folder, hashed: `backgroundMaterial/planemap-structural/`.
- **Checklist:** one for every proposal and every dead conjecture. It names the class, move, invariant, measure, input family, coverage and witness.
- **Replies:** short replies as files in `SolvingFrameworkPlan/`, so nobody depends on a meeting or a single channel.

We have learned more in one day from your two replies than from the night the first play describes. Gate D remains open. Graph 36, root 8 is the place to test D2, and the line in pencil on Kamper's napkin, *"or only the ones we make?"*, is the question §6 is trying to answer.

With thanks to both groups,

— The Long Table authors
