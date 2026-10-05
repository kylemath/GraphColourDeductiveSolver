# Long Table: handoff and resume point

4 October 2026. Read this first if you are a new agent picking up the **Long Table** role. Then read `SolvingFrameworkPlan/messages/` (newest first) and the Proof Navigator's latest revision message.

## The project in one paragraph

Goal: a structural, executable Four Colour proof without a large configuration census. Lean work lives in `/Users/fulkanjou/mathlib4-planemap`, with Lean `v4.35.0-rc3`; commits there are local, and publishing to the backup is the user's decision. Research artifacts live in this repo. There are three teams, which talk only through `SolvingFrameworkPlan/messages/`:
- **Math solutions and scale-up** (token `math`): owns the Lean proofs, the corpus sweeps, and independent replay;
- **the Proof Navigator** (token `navigator`): owns the ledger and status words, in `docs/navigator/planning.json`;
- **Long Table** (token `longtable`, this role): owns the adversary tooling, structural candidate sets, declared experiments, and statement review.

## Where the proof stands (revision 55)

- **The contact theorem is proved in Lean** (math team, `1e4d990`/`a4a95dd`): `four_color_of_empty_mass_region`. If every minimum-degree-five spherical triangulation has a degree-five root with an **empty dead-end region** for the mass rank R = (6n² + 1)p + q under two-swap macros, then every spherical map is four-colourable. Gate D, the hypothesis, is **open**: every Plantri graph through order 20 has a good root (12 failing roots out of 1,586).
- **Proved in Lean today:**
  - support transport;
  - triangulation completion, `5f54113`, via chord and bridge filling;
  - Lemma W, `a3adbc3`: breadcrumb warnings ≤ |dead-end region|, in abstract form;
  - Lemma S, `556c13f`: one singleton-colour neighbour per degree ≥ 5 hub;
  - the WP7 chain-mass lemmas;
  - the latest audit, 75/75 modules.
- **Computed:**
  - the mass-macro corpus;
  - the breadcrumb corpus (all 1,586 roots succeed, at most 4 warnings);
  - the anatomy of the dead-end regions (WP7d: order 17, graph 3 is a ring of 5 trap/twin pits; the twin toggle is a two-vertex chain at the opposite hub);
  - WP7f (each warned twin is one hub toggle from a trap).
- **Killed** (keep visible): local determinacy at radius ≤ 2 (WP9: order 19 graph 20 root 3 passes, order 20 graph 60 root 3 fails, same radius-2 ball); C7c; 7.3; H-A; H-B; S0 and S1± as every-member sets; rank variants rep and Lonly.

## Long Table's open work

1. **WP11, rank synthesis tier 1.** Declared, **version 2** (`longtable/WP11-rank-synthesis-tier1-declaration.md`), with the schema `wp11-cert-v1` (`longtable/wp11_cert.py`, examples in `longtable/wp11-schema-examples/`). **Not released.** Next steps:
   - the math team checks the schema with its replayer;
   - add the pre-release regressions (complementary-component and root-13 renaming);
   - **explicit user approval**;
   - then run discovery on orders 12–18, freeze the survivors, and run one validation pass on orders 19–20.
2. **Route B** (`longtable/WP10-route-B-draft-declaration.md`): a draft that recommends B1 (classical C-reducibility). Unreleased, with no owner.
3. **Proposed, unreleased:** large adversarial search beyond order 20 (Programme 3, which includes the radius-3 and distant-hub tests); a minimal unavoidable set (Programme 2). See `messages/2026-10-04-longtable-to-math-three-audacious-searches.md`.

## Working rules (all are hard-won)

- **Declare before running.** Commit the declaration first. If a team said it will review, **wait for an explicit go-ahead**, not an inferred one.
- **No status words.** Report facts; the Proof Navigator assigns statuses. Silence is never acceptance.
- **Holdout:** discover on orders 12–18, validate on 19–20 once, and disclose that 19–20 have been seen before. Nothing beyond order 20 without a release.
- **Commit only Long Table files,** staged by explicit path (other teams edit the same tree). In zsh, do not stage via unquoted `$VAR` lists; they don't word-split.
- **Messages:** `SolvingFrameworkPlan/messages/YYYY-MM-DD-from-to-subject.md`. Address the ledger team as "the Proof Navigator", filename token `navigator`. Reply in new files; never edit another team's file.
- **Lean in this checkout:**
  - `Fintype`/decidability instance mismatches break `rw`, `ring` and `split_ifs`; use `convert` or a `by_cases` + `simp` split.
  - `ring` needs `Mathlib.Tactic.Ring` imported explicitly.
  - Prefer `Nat.card` over `Finset` cards across propositional graph equalities.
  - The audit is `lake env python3 scripts/rebuild-planemap-source.py --output <dir>`; then append to `PlaneMapFourColorAudit.sha256` and update `PlaneMapFourColorAudit.md`.
- **Long Table code** is in `backgroundMaterial/planemap-structural/longtable/` (`mass_core.py` is the independent implementation), with its own `SHA256SUMS`.

## Site

`docs/` contains the plays (`play/`), the poem, `trap/` (the tidy-trap demo), `deadend/` (the ring-of-pits demo) and the navigator. They are published via GitHub Pages from `kylemath/GraphColourDeductiveSolver`.
