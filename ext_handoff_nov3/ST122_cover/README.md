# Stage B cover test: the 633 RSST configurations against kill families u and r

Opus, 10 Nov 2026, about 16:45Z. This is the cover test only; no LP was run. It used one CPU slot.

## Answer

**1. Config-level cover.**
- 307 of the 633 configurations contain a kill of family u (both sides, K3l5u and K3gB5u, agree).
- Family r gives the same 307. The five kills added since r (P17-P20) cover no configuration at this level.

**2. Every cover is the configuration itself.**
- The witness kill always has exactly the configuration's interior vertices, with the same degrees.
- 300 witnesses are window copies in our A97 registry (s33z/reg_A97: k3x_C_A97 168, k3x_D_A97 131, pairs_D7 1).
- The other 7 are wheels in the engine's R5 / R6 tables.
- So family u holds no smaller kill inside any RSST configuration. "Covered" means "already in our registry under a window name", and it saves Lean work only where our copy is in Lean.

**3. The Studio's 403 still to prove** (`queue403_*.tsv`):

| verdict | covered by u | our copy already in Lean | count | file |
|---|---|---|---|---|
| C2cons | yes | the witness window has an hC theorem (JCOV `lean_membership.tsv`, keep_lean_C) | **168** | can_leave |
| D2 | yes / no (1 / 20) | isomorphic to an entry of `job_HDC502/D_todo.tsv` (HDC502 hD, 370/370 built) | **21** | can_leave |
| C2cons | no | isomorphic to an entry of a HA5 hC job input | 2 | check |
| D2 | yes | no (k3x_D_A97 window or wheel, no hD) | 127 | stays |
| D2 / C2cons | no | no | 50 / 35 | stays |

So **189 of the 403 can leave the queue, 2 need a check, and 212 stay.**

Why ST-113 missed these 189:
- For the 168 C entries, ST-113 required our X to equal RSST's C2cons X. Our copies use our own X, and any valid contraction proves the configuration C-reducible.
- For the 21 D entries, ST-113 matched literals byte for byte, and these 21 are numbered differently in HDC502. Here the kc graphs were matched up to isomorphism, ring cycle kept and mirror allowed.

**4. Uncovered configs in the 403: 107** (70 D2, 37 C2cons).
- 22 of them have a Lean copy by isomorphism: 20 in HDC502 and 2 in HA5.
- The 20 HDC502 ones are kill-table configurations. Family u holds them through its kill tables, which this label-level test does not read.

## State-level counts (only where per-state data exists)

**d7/d8 domain sets** (W6r `fp_{A,B,C,T}.json`, K3gB5n domains; `sets_*` columns, `statecount/sc_{u,r}_sets.tsv`):
- 98 configurations kill a positive group.
- Family u, read at the group's own centre, rejects the row of every group for 4 of them: 128.1324802, 126.490802, 126.8406 and 128.442806.
- For the first three, the rejections come from P17-P20, and family r leaves those groups alive. Family r rejects 128.442806's groups too.

**Full-world none-config states** (Studio RSST-1SHOT `NEEDS_NONE.tsv.gz`, d6/d7/d8; `fw_*` columns, `statecount/sc_{u,r}_needsnone.tsv`):
- There are 223,743 (none config, state) lines. Family u leaves 25,570 of them not rejected.
- 9 none configurations have every one of their states rejected by u: 7566.128 (9,498 states), 7696.442802, 7566.9723, 209.1324802, 142.1324806, 7562.460920, 7562.1310580, 7562.1307280 and 126.687602.
- 16 none configurations have every one of their sole states rejected.
- These are candidates for W6r's exhaustive re-check, not results. The listed states are DFS leaves reduced by the RSST engines' own dominance argument, and that argument has not been re-proved for our kills.
- The d9/d10 none states (31,139 / 409) are not in NEEDS_NONE and were not tested.

## Method (`code/cover.py`)

**Placement test.** For every interior vertex z of degree d ≥ 7 of a configuration C:
- C fixes some letters of z's row label and leaves the others unknown:
  - link letters w_i and apex letters s_i, with letters 5..9 and 9 = degree 9 or more, as the engine reads them;
  - an unknown letter is a ring vertex of C, or an apex that C does not draw.
- z is killed if every completion of the unknown letters is inadmissible under the engine's own `admissible()` semantics: a pattern of the family under any rotation or reflection, R5 at a link 5, R6 at a link 6 for every private, or RBIG.
- The search is a depth-first search over completions with a cap of 20,000 nodes. No placement reached the cap.

**Wheel test.** For an interior vertex of degree 5 or 6, every completion of its wheel must be R5 (resp. R6).

**Soundness.** C is covered if some vertex is killed. Then every triangulation containing C contains a family-u kill. The test is not complete: it never looks at vertices outside C.

**Pattern lists.**
- u: `fam_args/u/patterns_K3l5u.tsv` (aeb3ac1e) and `patterns_K3gB5u.tsv` (fb93859f).
- r: `inputs/patterns_K3l5r.tsv` and `patterns_K3gB5r.tsv`, made with `fam_args/u/mkfamlist.py` from args a44799f9 / b0ce409f.
- The engine counts match: r has D 18154 / C 712 and D 18244 / C 781.

**Wheels.** The block in eng_p8/pcheck.py is exec'd verbatim: 24 R5, 31 R6, 7 fans, 104 RBIG.

**Configurations.** unavoidable.conf 26aeba66, matched by name and order to rsst_verdicts b6f7a314, with 0 mismatches.

## Checks

- **Engine cross-check** (`code/chk_engine.py`, `logs/log_chk_*.txt`). The real engine (eng_p8 pcheck `load_patterns` + `admissible`) was run on each family's args.
  - It ran on 818 uncovered completions found by the DFS (all must be admissible) and on 969 random completions of killed placements (all must be rejected).
  - Result: 1,787 / 1,787 agree, for each of the four families.
- **Sides.** K3l5x and K3gB5x give identical cover columns for both u and r.
- **Witness size.** Every pattern witness has exactly as many specified vertices as C has interior vertices, so it is C. No witness reads a vertex of degree 10 or more as the letter 9.

## Caveats

- **Lean evidence comes from listings on origin/main e82a49aa**, copied into `lean/`.
  - The 168 rest on JCOV `lean_membership.tsv`, which names an hC theorem for each.
  - The 21 rest on ST-113's statement that HDC502 is 370/370 built.
  - The Studio should confirm module status, and whether occurrence glue exists for these entries under our names.
- **Isomorphism ignores orientation.** It treats mirror images as the same configuration. Reducibility does not depend on orientation; whether the occurrence glue does is a question for the Studio.
- **Kill tables are not read** (U7/U8/U9, kill6, l3q), so config-level cover is a lower bound.

## Files

| file | what it holds |
|---|---|
| `cover_table.tsv` | One row per configuration: verdict, queue, cover u / r, witness and its vertex label, Lean evidence, set and needs-none counts, an alive label for uncovered configs |
| `queue403_can_leave.tsv`, `queue403_check.tsv`, `queue403_stays.tsv` | The 403 split three ways |
| `summary.tsv` | The cross-tab |
| `witness_patterns.tsv` | Witness per covered configuration |
| `statecount/` | sc_{u,r}_sets.tsv and sc_{u,r}_needsnone.tsv |
| `lean/` | leaniso.tsv, lean_listing.tsv, and the main listings used |
| `code/` | cover.py, statecount.py, mktable.py, finalize.py, leaniso.py, chk_engine.py |
| `inputs/` | The r pattern lists |
| `logs/` | Run logs, engine cross-checks, and the DFS leaves (`cover_*.tsv.leaves`) |
