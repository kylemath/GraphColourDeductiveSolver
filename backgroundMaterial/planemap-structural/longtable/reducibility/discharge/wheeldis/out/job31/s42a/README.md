# s42a on A78: solutions and the lower-bound certificate

This is the Opus lane's s42a run on registry A78 (main b6dc7610), with the 128 ring-merge cpat names held out (`loop/opus/P_own_lp/s40f/exname_rm128.txt`). The rules are l3q (RSST rule 9) and rpatN3 (the 2026 set, used as a map and proved D on our two engines). The engine is `loop/opus/P_own_lp/s39o/eng` and the spec is `loop/opus/P_own_lp/s39o/RELAY_SPEC_s39o.md` (§39.6) plus `s40f/RELAY_SPEC_s40f.md`.

Studio confirmed both bounds on its own engine (9bc9b2b2, `loop/studio/opus_check/s42a_verdict.md`):
**44/421 = 0.104513 <= t* <= 0.109439356774**. Quote the upper as that float; 80/731 is not feasible.

| file | what it is |
|---|---|
| `sol_q42aA78.json` | The upper solution (keeppen, converged). upperR2 FEASIBLE at 0.109439356774. This is the actual rule set (sender amounts). |
| `sol_q42aA78L.json` | The nosep primal solution that goes with the lower certificate (t = 0.104513...). It is not a valid rule set on the full registry. |
| `cert_q42aA78L.json` | The lower certificate (155 dual rows). lowerR2 VALID at exactly 44/421, and no column is priced at a cap. |

## Schema

**Solution JSON** (both `sol_*.json` files): a dict.
- `t`: the LP value (float). `model`: the receiver model string (`"R6x2"`).
- Boolean keys switch families on or off: `apex`, `xon`, `apexcls`, `l3q`, `hat5`, `zh`, `q7`, `v6`, `face5`, `hatrr`, `big2`, `l6r`, `zrflag`.
- List-valued families are `[[key, amount], ...]`, with the key a tuple of ints:
  - `g`: 5 to big, one-sided wedge. `h`: 5 to big with second ring, key `[d, ...]` = big degree, then the neighbour word.
  - `r`: the relay columns of RELAY_SPEC_s39o.
  - `lq` and `lQ`: the l3q pair, keyed `[centre letter, a, mask]`, see RELAY_SPEC_s21.
  - The rest (`z`, `zr`, `q`, `v`, `f`, `rr`, `D`, `z6`, `Z6`, `V`) are empty in this run.
- `y`: a dict `"d|word"` → amount, the base 5→d charge by link word.
- `x`: a dict of excess-penalty column id → value. These are keeppen/nosep slack columns, capped at 3, and are not discharging amounts.

**Certificate JSON** (`cert_q42aA78L.json`): a list of `{"w": dual weight, "row": label}`, where `label[0]` is the row type:
- `["senderR2", word, pattern]`: a sender-side row.
- `["receiverR2", d, link, second_ring]`: the receiver row for a degree-d vertex with link word `link` and second-ring word `second_ring`.
- `["cons2", ...]` and `["mrowR2"/"mrowL", ...]`: conservation and mask rows.

lowerR2 re-derives every row's coefficients from its label, so the certificate needs nothing beyond the labels and weights. To check it, run `python3 pcheck.py lowerR2 <flags> cert=cert_q42aA78L.json` in the engine directory, with the flags in `loop/opus/P_own_lp/s42a/run_A78/` (see `binders.log` and the run scripts).

These files contain no Team B material.
