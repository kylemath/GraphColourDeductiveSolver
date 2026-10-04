# Long Table work plan: adversary and structural candidate sets

4 October 2026. Our accepted share of the revision-39 plan: **the adversary** and **structural candidate-set proposals**. The corpus implementation, quantifier review, support transport and filling proofs belong to the scale-up team. The evidence and status ledger belongs to the navigator group. We do not rerun the census.

## Ground rules

- Python standard library only, in the style of the existing `backgroundMaterial/planemap-structural/*.py` scripts.
- **Inputs:**
  - The Plantri corpus `triangulations-min5-{12..20}.txt`, with line hashes checked against `search-results.json`.
  - Published result files.
  - Recomputation is allowed only for a single named graph, for regression or debugging.
- **Outputs:** JSON with a `scope` line stating what is *not* established, input hashes, and full witnesses: the colouring, the root, every successor rank.
- Every proposal uses the checklist: class, move, invariant, measure, input family, coverage, witness.
- No status words. We report results; the navigator group assigns status.
- Commit only our own files.

## WP1: Adversary (`adversary.py`)

Purpose: rule in, first failing graph out, reported with a replayable witness.

1. **Corpus loader.** Read every order file, check each line against the recorded input hashes, and parse the rotation format used by `component-mass.py`.
2. **Rule interface.** A rule is a function `candidates(rotation) -> set of roots`, plus a named check per root. The checks are:
   - the (σ, β) robust game, reused from `bit-search.py`;
   - mass-macro descent at macro length 1 and length 2.
3. **Classification,** per correction 2 of the review:
   - (i) the root fails;
   - (ii) the candidate set contains a failing root, so the selector fails;
   - (iii) every degree-five root fails, which is a kill witness for MMD-exists.
4. **Regression gate,** which must pass before any new result is reported:
   - Smallest-label exterior root with (σ, β): reproduce the order-20, graph-36, root-8 failure, 5 of 55 losing.
   - Graph 36: reproduce that only root 8 loses (σ, β) among the 8 eligible roots.
   - Graph 36, root 8, mass-macro length 1: exactly 3 stuck orbits, the first at rank (1,190).
   - Length 2: no stuck orbits.
   - Icosahedron: every root passes trivially.
5. **Consume, don't recompute.** Once the corpus team publishes per-root mass-macro results, the adversary reads them. Until then it computes per-graph results only for regression fixtures.

**Done when:** all regression cases are reproduced from the corpus files alone, and one command evaluates any candidate set over the corpus.

## WP2: Structural candidate sets

Purpose: nonempty, isomorphism-equivariant sets S(T) ⊆ D(T), with deterministic tie-breaking, that contain only passing roots.

1. **Check suggestion (a) first.**
   - Relabel each of the 118 graphs by a random permutation and permute colours.
   - Confirm that the mass-macro pass set maps to itself on a sample of graphs that includes graph 36.
   - Compute automorphism orbits of D(T) and confirm each pass set is a union of orbits.
   - If this fails, report it to both teams before proposing any candidate set.
2. **Describe the pass sets,** once the corpus table exists. For each graph record:
   - |D(T)|, the pass set, and how many orbits it spans;
   - simple structural data per root: degree-5 neighbour count, the second-ring degree multiset, distances to other degree-5 vertices, and charge after a fixed discharging rule.

   This is description, not fitting. Any rule found here must then be tested on graphs not used to find it, such as orders 21 and up if they are generated.
3. **Proposals,** each stated in symbols with a one-line proof that it is nonempty:
   - **S0:** all of D(T). This is the baseline, and it fails exactly when MMD-exists fails.
   - **S1:** arg max or arg min of the number of degree-5 neighbours over D(T).
   - **S2:** the degree-5 vertices that receive positive final charge under a stated discharging rule. Nonemptiness follows from total charge 12.
   - **S3+:** whatever WP2.2 suggests, with the rule written down before it is evaluated.
4. **Report,** for each proposal: the first failing graph with its witness, or "passes the corpus through order 20". Include the cost of computing the set. Passing is evidence, not coverage.

**Done when:** at least S0–S2 are evaluated against the corpus pass sets, with witnesses or pass statements filed for the ledger.

## WP3: Housekeeping on our own documents

- Add an errata note to [LongTableJointReply.md](LongTableJointReply.md):
  - rename D2 to mass-macro descent;
  - point to the revision-39 corrections;
  - mark §5 as superseded by the corrected statement.
- Revise the plays, keeping their fiction labelled:
  - remove the Catalan-42 claim;
  - take interior swaps off the "DEAD" list;
  - change "only live shape" to "one live shape";
  - change "label-invariant" to "structural candidate set";
  - add a note that root 8 passes the tested mass macro.
- Offer, but do not insist on, a second reading of revision 39's quantifiers.

## Order of work and dependencies

1. WP3 errata (immediate).
2. WP1 steps 1–4, which need only files already on record.
3. WP2.1, the invariance check, using the WP1 tooling.
4. **Wait** for the corpus team's per-root mass-macro table.
5. WP2.2–2.4.
6. Report findings to both teams as one file, and play revisions at any point.

## Stop rules

- If MMD-exists is killed by the corpus (a class (iii) graph): stop WP2. Send the witness, and help inspect it for a structural move lemma. Do not lengthen the macro.
- If WP2.1 finds pass sets that are not invariant: stop, and report before going further.
