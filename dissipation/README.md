# Dissipation and rule-family work (11 to 13 Nov 2026)

What was made and tried in the cloud thread "families" and on the Mac Studio, in one place. Everything here is
exploratory measurement by one tool unless a line says otherwise. None of it is a proof claim, and none of it
touches the stopped proof jobs.

## What we asked and what we found

| Question | Where | Result |
| --- | --- | --- |
| Are the reducible configurations and rule parts organised in families? | `families/REPORT.md` | Structure is real (far above null baselines) but bookkeeping-level: no shared reducibility reason. |
| Can the rules be described by what they do (behaviour embedding, mirror/odd-even groups)? | `families/REPORT.md` addenda 1 and 2 | 305 mirror classes need about 100 factors (null: 176); about 70 behaviour duplicates. |
| Can the 604 added parts be compacted? | `families/FABLE_IDEAS.md` | 89% of the 493 added push parts fit one law: a 7 or 8 left at exactly +6 forwards it. Exact merging gives 497 parts instead of 604. Receiver choice unexplained. |
| Are near rules single swaps, and is there a smaller set of operations? | `families/OPERATIONS_IDEAS.md` | Only 51 of 307 tree branches in the 588 proof are 1 or 2 nodes apart; recurring swaps are complement case splits ("6 versus 7 or more"). |
| Can a small integer attention step imitate the outside team's receiver choice? | `stage0/RESULT.md` | 76% exact held out, pass line 95%: not met. With all rule kinds and random data: RSST push 96%, tunnels 95%, added pushes 75%. Needs about 10,000 weights, so learnable but not compact. |
| Can a multi-round dissipation network trained from scratch reach zero on the degree 5/6/7 world? | `RESULT_STAGE1.md`, spec in `SPEC.md` | No. Exact leftover charge 0.200 (first run), 0.087 (hats, forwarding, tunnels), 0.083 (round one alone with kite pushes); existing families reach about 0.006 to 0.007. The attention did almost nothing; the obstruction is structural. |

Proposed next, not run: a "lift test" (does the fractional world behind a failed solve survive one ring further out?)
and a "type alphabet" search (vertex type from its own ring, one sender-by-receiver table). Evidence for the second
is `stage0/alphabet_test.py`: on RSST rules the edge amount is fixed by the two end rings in all but 0.01% of repeated cases.

## Folder map

| Path | What it is |
| --- | --- |
| `SPEC.md` | The brief for the network experiment (model, world, pass and fail lines, ground rules) |
| `RESULT_STAGE1.md` | Every Stage 1 run on the Mac Studio with numbers, diagnosis and compute |
| `stage0/` | Imitation experiments (code and `RESULT.md`) |
| `stage1/` | Network code, exact evaluator, soundness tests, best parameter sets and logs from the Mac Studio |
| `families/` | Family and behaviour analysis: `REPORT.md`, `FABLE_IDEAS.md`, `OPERATIONS_IDEAS.md`, `code/` |
| `families/atlas_page/` | The Discharging Rule Atlas: its own `README.md`, a self-contained `rule-atlas.html` copy of the published page, and the page sources (`assemble.py`, `body3.html`, `css.txt`); the builder is `families/code/build_atlas.py` |
| `w16/` | Copy of the W16 zero-Euler code, data and report that defined the 5/6/7 world |
| `families_code/` | Early copies of `behav.py`, `parts.py`, `mir.py` used by the Stage 0 scripts |

## Published artifacts (these live on claude.ai, not in git)

- Rule Atlas, with four proofs, the family tree and the template page: https://claude.ai/artifact/CZnurqSukekcNnbzCaqtyn
- Proposal "Learned charge dissipation" with the Stage 0 and Stage 1 results: https://claude.ai/artifact/K7kVZV2BdxaqriaGcywmgW

## Not in the repository

- Large caches from the Mac run (48 to 200 MB each); the `stage1/build_cache*.py` scripts rebuild them.
- The Atlas data file (`atlas4.json`, 7 MB) and the rule database (`rules.sqlite`); rebuild with `families/code/build_atlas.py` and `builddb.py`, or take them from the project files `swarm/families/db/`.
- The outside team's 588-part rule file as a separate file: `stage0/gen.py` and `gen_all.py` need it. Note that `families/atlas_page/rule-atlas.html` embeds those rule parts as page data (the "Outside team 588" proof), and the earlier pass of the outside team's work is already on main under `backgroundMaterial/.../out/job_OUTSIDE2/`.
