# Dissipation network, Stage 1: result (13 Nov 2026, Mac Studio)

**Verdict: FAIL at Stage 1.** The exact maximum final charge after hardening is **12 charge units = 1/5 in t units**
(one engine: this code's integer evaluator, labelled [P] one engine). The best un-hardened point is the rational LP value
**115/11 ≈ 10.4545 units ≈ 0.1742 t-units** (HiGHS float, [M]). Both are far above the LP families' floor in this world
(0.0058 to 0.0072 t-units), and far above 0. Since round 1 already rounds to integer units, anything above 0 is at least
1/60 = 0.0167 t-units, so with integer amounts the only outcome below the LP floor would have been a pass.

Unit conversion: t-units = charge units / 60 (a 5 starts with 60, the LP's t is the largest final charge in units of a 5's charge).

## World and row set

- **7-rows:** `w16/data/world_567_7_std.pkl` (md5 `a83ab2f3bb07b45ea190f34f11908de5`, 114,091 labels), the W16 world of 5 Nov 2026:
  every admissible degree-7 neighbourhood (link w + hats s) with all letters in {5,6,7} on the **Studio-full stack**
  (keep95p131f rules, l3q V7/V8 tables, rpatN3, the A111 C patterns, RBIG; the stack W16 loaded through `st21_w10.py`, md5 fa40e97f).
  **110,087 rows.** I did **not** rebuild this from the Studio's engine. The W10 harness that `load21.py` needs
  (`/tmp/swarm-W10` and `/tmp/swarm-W16`: `sol_zero.json`, `args_k95f.txt`, its working directory) is no longer on this machine.
  /tmp was wiped on the 10 Nov reboot. So the kill mask is the 5 Nov Studio-full one. Later kills (B5 and others) could only excuse more rows.
- **5-rows / 6-rows:** wheel-level kills only, R5 / R6 / FANS copied verbatim from spec 4.4 as written in `st21_w10.py`
  (SPEC_R5, SPEC_R6, SPEC_FANS, plus three consecutive 5s in a 6-link). This gives **24 admissible 5-links**, identical to W16's sender
  words, and **61 admissible 6-links** (W16's 60 cons2 words plus 666666). Fewer kills than the full stack, so this is conservative.
- **Excused 7-rows:** 765 rows (those where no admissible degree-7 row of some 7-neighbour fits what the row shows of it). Such a row
  cannot occur in a kill-free map. 109,322 live 7-rows remain.

## Model as run

- Round 1: every u of degree 5 or 6 pushes `P[deg u, deg v, {x,y}, n5(u)]` to each neighbour v of degree ≥ 6. Here {x,y} is the unordered
  pair of degrees of the two common neighbours (mirror shared), and n5(u) is the count of 5s around u (unbucketed, 0..6). That gives 168
  table entries.
- Round 2: every 7 with c1 > θ sends c1 − θ to its **degree-7** neighbours. The split is equal over the slots whose integer score is within
  margin m of the best (hardened shares 1, 1/2, 1/3, …). Scores are integer weights over 559 mirror-symmetric bits of the slot's context
  as seen in the sender's own row: ring neighbours, hats, outer link vertices and far hats, pooled over the two sides, with all pairs of
  the 16 base bits and one-hot side types.
- Design choices I made (not fixed by the brief): forward targets are 7s only, with no forwarding into 6s. No round 3.
  The attention has **no fans and no c1(v) thresholds**: those would read past the sender's row and widen the reach again.
- Charge conservation is by construction. The torus self-test below checks it.

## How the wider reach was handled (conservative bound, sound)

The final charge of a 7 X is min(c1(X), θ) + Σ fwd(u → X) over its 7-neighbours u. fwd(u → X) depends on u's own row, one ring further out.
I bound it from above by the **maximum over every admissible 7-row of u, in all 14 orientations, that agrees with what X's row shows of u**.
That covers u's link neighbours beside X, u's link vertices two away (X's hats), u's hats beside X (X's link vertices two away), and u's
hat across (w_{i±1}, s) when that w_{i±1} is a 5. There are 1,422 distinct views over 741,624 (row, slot, orientation) entries.

The other unknowns are maximised in the same way:
- The hidden letter of each link 6 is maximised over the letters that keep that 6-link admissible.
- A 6's incoming pushes are maximised over the admissible links of the pushing 5 or 6.

**Torus self-test** (`test_torus.py`): on 30 random 5/6/7 torus triangulations, with 6 random integer parameter sets each, I simulated the
network on the map. The true final charge never exceeds the row bound (9,234 vertex checks), and total charge is conserved. As a control,
a deliberately wrong view (two fields swapped) is caught.

## Training, hardening, pruning

- Inner solver: with the shares fixed and each row's own term fixed (θ or c1; both are upper bounds of min(c1, θ)), the bound is
  convex piecewise-linear in (P, θ). So the best amounts are an **exact LP**: about 127k constraints after dedupe, about 1,640 variables,
  2 s with HiGHS.
- Descent: PyTorch, Adam on a log-sum-exp smooth max (β 0.2 → 10) with softmax attention (τ 1 → 0.05) and L1 on P and W.
  Runs: 300 steps, and three seeds of 4,000 steps. Best soft max: 10.54.
- Hardening: weights quantised to 2, 3 or 4 bits by magnitude, margins 0 to 4, LP re-solve over a θ grid. **Every setting gives 115/11.**
  Pruning by rounded magnitude removed **all** attention weights with no loss: uniform splitting is as good as anything found.
  Control: 20 random integer attentions give a minimum of 115/11 and a median of 10.49.
- Snap P to multiples of 3 and θ to an integer, then integer coordinate descent on the exact evaluator: 15 → **12** units.

| setting | max final (charge units) | t-units |
|---|---|---|
| round 1 only (LP, no forward) | 11.6418 [M] | 0.1940 |
| uniform forward, best θ (LP) | 115/11 = 10.4545 [M] | 0.1742 |
| trained attention, any bits or margin (LP) | 10.4545 [M] | 0.1742 |
| fixed θ = −60 / −20 / 0 / 5, uniform | 27.10 / 15.53 / 11.88 / 11.02 [M] | |
| **hardened, exact integers** | **12 [P]** | **1/5** |

**Hardened network:** θ = 10, margin 0, **36 non-zero push entries** (multiples of 3, listed in `stage1/result_stage1.json`),
**0 attention weights**, so 37 non-zero parameters including θ.

**Binding rows at 12:** 7-row 5556776 / 5776567 (c1 = 12); 5-links 55757 and 56776; 6-links 556676, 565667, 565767, 565777, 566677 and 567567.

## Why it fails (diagnosis)

- The 5-rows, the 6-rows and the 94 rows of 7s with no 7-neighbour can all be brought to 0 together (LP t = 0). The obstruction comes
  entirely from forwarding 7s.
- At the 115/11 optimum, the binding incoming forwards come from neighbour rows such as 5556676 / 5776677: a 7 with three 5s that has
  **exactly one 7-neighbour**. Its whole surplus must go to that one receiver, whatever the attention says. A receiver whose view admits
  such a neighbour has to budget the worst case on every 7-slot.
- That decoupled worst case is the tightest bound available from the receiver's 2-ball. The unknown fans of different neighbours do not
  share vertices, so enumerating a wider ball would only help through kills that span three rings. So in this model, with 2-ball receiver
  rows, attention cannot act on the binding rows. The brief's mechanism ("forward your surplus") does not lower the bound below the
  round-1 level here.
- Separately, the spec's round-1 table (no hats) is much weaker than the LP families: 0.194 t-units against base 0.028.

## Hardware, speedups, wall time

- Apple M4 Max, 16 cores, 128 GB, with PyTorch 2.6 (MPS available) and NumPy/SciPy. Nothing installed.
- MPS was **8× slower** than CPU for this model (0.47 s against 0.06 s per step; the scatter-max is the slow part), so training ran on
  CPU with 4 threads.
- Speedups used:
  - dedupe of attention contexts (370,812 slots → 2,716 contexts);
  - dedupe of LP rows (110k → 59–75k) and of forward constraints by (view, share, candidate sets);
  - segment-max over sorted views (`np.maximum.reduceat`);
  - integer evaluation in units of 1/420, so shares 1/k are exact;
  - few-bit weights ranked by magnitude for pruning;
  - the exact LP in place of descent for the amounts;
  - early stopping in the polish.
- Not used: bit-packed uint64 features. The full exact evaluation already takes 18 ms.
- Wall time about 1.5 h in all, with compute about 25 min: training 4 × ~4 min, hardening 11 min, diagnostics about 5 min. At most
  4–5 cores were busy and the machine stayed usable. No existing job, queue or file was touched.

## Not done / could not do

- I did not rebuild the 7-row kill mask with the current Studio stack (harness missing, see above).
- No round 3, and no forwarding into 6s.
- No unrolling or two-engine check, since nothing passed.

## Files (`dissipation/stage1/`)

| purpose | files |
|---|---|
| row set | `rows.py` |
| index structures and exact integer evaluator | `net.py` |
| torus soundness test | `test_torus.py` |
| inner LP | `lp.py` |
| soft model and descent | `train.py`, `run_train*.py` |
| hardening, pruning and polish | `harden.py`, `run_harden.py` |
| baselines and diagnostics | `baseline.py`, `sweep_theta.py`, `diag1-5.py` |
| final exact evaluation | `final_eval.py` → `result_stage1.json` |
| hardened parameters | `hard_s0_300.pkl` |
| logs | `logs/` |

The 48 MB index cache (`cache_B.pkl`) is not committed; `build_cache.py` rebuilds it in 4 s.
