# Rule fits: simplest discharging rule vs t (s54, Opus, 21-22 Oct 2026)

Registry A97 with the s53 flag set (`xon apexcls filt16 hat5 consall l3q lqcap=3 l3qV=7,8`, `rpatN3`,
`exname=s40f/exname_rm128.txt`; RSST 2.126 and 8406.123 stay out). The engine is `s54/eng`: a copy of `s51/eng` plus
`pmodel.py`, with patches to `prelay2.py` (solveR2) and one exec line in `pcheck.py`. The md5s are in
`s54/eng/md5_s54.txt`; the s51 originals are in `md5_orig_s51.txt`. The reference is `s53/run_A97/sol_q53A97.json`:
t = 0.098789, upperR2 FEASIBLE, about 7,000 nonzero weights.

**Every "verified" t below is an upperR2 FEASIBLE result on the rule as written in its sol file.** Each modelled family
is evaluated on its whole key universe, so upperR2 checks exactly the stated rule.

## 0. Headline: complexity vs t (Pareto frontier, all verified)

| nonzero params | verified t | rule / source |
|---|---|---|
| 1 | 2/3 = 0.666667 | a 5 sends 1/3 to each 7+ neighbour (`runs/L_yD`, `S1_v1/s001`) |
| 2 | 1/2 | 1/4 + 1/4 per 6-flank (`S1_v1/s002`) |
| 3 | 5/11 = 0.454545 | `S1_v1/s003` |
| 4 | 10/23 = 0.434783 | `S1_v1/s004` |
| 5 | 19/44 = 0.431818 | `S1_v1/s005` |
| 6 | 7/17 = 0.411765 | `S1_v1/s006` |
| 14 | 2/5 = 0.400000 | lasso 0.3 refit, y only (`R_lasso05`) |
| 27 | 0.305482 | lasso 0.1 refit (`R_lasso1`) |
| 49 | 0.248278 | forward selection + lasso block (`S1b/s051`) |
| 62 | 0.192220 | forward selection (`S1b/s070`) |
| 78 | 0.182736 | forward selection; no 6-relay at all (`S1b/s087`) |
| 88 | 0.174850 | selection seeded from lasso 0.03 (`S2/s092`) |
| 114 | 0.158567 | `S2/s115` |
| 148 | 0.150937 | `S2/s148` |
| 366 | 0.137847 | lasso 0.001 refit (`R_lasso3`) |
| 395 | 0.135540 | magnitude-pruned refit (`R_q25`) |
| 428 | 0.129274 | `R_q2` |
| 457 | 0.125476 | `R_q15` |
| **465** | **0.124846 (<= 0.125)** | `R_q12`: smallest rule found under 1/8 |
| 543 | 0.123874 | `R_p2` |
| 774 | 0.122436 | `R_p3` |
| 1231 | 0.121874 | lasso 3e-4 refit (`R_lasso35`) |
| 1542 | 0.121104 | lasso 1e-4 refit (`R_lasso4`) |
| ~7,000 | 0.098789 | reference sol_q53A97 |

Not reached: t = 0.1059 and t = 0.0988. Every sparse model tried stays at t >= 0.1211, even with 1,542 parameters. The
last 0.022 needs the reference's per-key h and g tables (thousands of weights).

## 1. The simplest rules in words (all upperR2 FEASIBLE)

Terms: "big" means degree >= 7. A **flank** of a five v, seen from a big neighbour u, is one of the two common
neighbours of v and u. The **far** neighbours are v's other two neighbours. "Flank 5 next to far 6" means a flank of
degree 5 whose other neighbour on v's link has degree 6.

- **1 parameter, t = 2/3:** "A 5 sends 1/3 to each neighbour of degree >= 7."
- **2 parameters, t = 1/2 (the simplest non-trivial rule):** "A 5 sends 1/4 to each neighbour of degree >= 7, plus
  another 1/4 for each common neighbour of degree 6 that the two share."
- **3 parameters, t = 5/11:** "A 5 sends to each 7+ neighbour 6/55, plus 7/55 per shared neighbour of degree 5,
  plus 17/55 per shared neighbour of degree 6."
- **6 parameters, t = 7/17:** "A 5 sends to each 7+ neighbour 6/51, plus 3/51 per shared 5 and 14/51 per shared 6,
  plus 5/51 for each shared 5 whose next neighbour (around the 5) is a 5 or a 6, plus 2/51 for each shared 6 whose
  next neighbour is a 6."

Up to 6 parameters the best rules use only y (5 -> big) and ignore the receiver's degree. The first degree-dependent
and relay terms enter at the 49-parameter step.

### Rows that fail just beyond (upperR2 at t - 0.005; `s54/checks/ub_*.log`, digest from `s54/fails.py`)

Each excess is exactly 0.005, so these rows are tight at the rule's t.

| rule | tight senders (five's link word, which ends at t) | tight receivers (d, link) |
|---|---|---|
| 1 param, t = 2/3 | fives with exactly one big neighbour: 66667/8/9, 56676, 56667, 55696, ... (15 of 342 words) | d = 7, link 9557555 (five 5s around a 7) |
| 2 params, t = 1/2 | 56667/8/9 (one big flanked by 5 and 6), 55757, 55758, 55859, 55959 (two bigs flanked by 5s), 55667/8/9 (12 words) | d = 7, links 9565856, 9565855, 9565865 |
| 3 params, t = 5/11 | all-big fives 99999, 89999, 88888, 79999, ... (45 words) | d = 7, links 9655567, 9655568, 9655566, 9655569 |
| 6 params, t = 7/17 | 59999, 59899, 58999, 58959, ... (108 words) | d = 7, links 9565855, 9565755 |

## 2. Method

- **Model class.** A family's weight is `w[key] = sum_f theta_f * phi_f(key)`, where the features are generic indicators
  on the raw key letters, with positions paired under the key's reflection (`s54/feats.py`):
  - y: const, D, add (flank / far letters), addD, pair (flank-far, far-far, flank-flank), pairD, full;
  - g: const, add (spokes, hat / fan / apex classes), pair, full;
  - h: const, D, nf, add, addD, pair, full;
  - x: const, FT, add, side, sideFT;
  - r: const, type, side, full;
  - lq: const, full.
- **Parametric LP** (`pm=fam:model,...`, `s54/eng/pmodel.py`). Every row coefficient on a key is spread onto the theta
  columns, and solveR2's separation runs unchanged on the rule the thetas define. The bounds (>= 0; x and lq <= 3) are
  enforced on the **whole key universe** (y 942, g 393, h 18,683, x 70,875, r 153, lq 40 keys) by lazy rows (`lazyb`):
  rows for keys in use, plus any universe key whose value leaves its bounds. After each LP, the families are evaluated
  on the whole universe.
- **Sparse rules, three generic routes:**
  - **Forward selection** (`pm=...:sel`): column generation over the dictionary. Each feature is priced exactly from
    the duals; the 24 best are tried as warm-started new columns; pairs are tried next; at a plateau, a lasso block
    step runs over about 500 candidates. Separation then resumes.
  - **Lasso path** (objective t + lambda * sum |theta|) on the pool, followed by a **refit** (lambda = 0) with
    separation.
  - **Magnitude pruning** of a refit, followed by another refit.
- Warm pools: `s51/eng/rows_q53A97.txt`, then `s54/pool2.txt` (that file plus the receiver rows of the s54 runs).
- A decision-tree growth mode (`pm=...:tree`) was also built. It stalls because of LP degeneracy (the run reached
  t = 3/7 with 10 leaves), so it is not used in the table.

## 3. Regress and round (step 1): fails

Least squares over each family's universe (absent key = 0; `s54/fits_ls.txt`):

| family | models tried | best R^2 |
|---|---|---|
| y | D / add / pair / pairD | 0.29 / 0.53 / 0.64 / 0.68 (135 features) |
| g | add / pair | 0.83 / 0.93 |
| h | addD / pair | 0.46 / 0.55 |
| x | side | 0.02 |

The fitted values go negative on thousands of h and x keys. Rounding these fits is hopeless, so the parametric LP is
the main route.

## 4. Which families matter (pool LP, other families free; `s54/runs/n_*`)

| change | pool t |
|---|---|
| none (all free) | 0.0892 |
| r = 0 | 0.0892 (unchanged) |
| x = 0 | 0.1134 |
| x per (from, to) degree only | 0.1111 |
| lq = 0 | 0.1111 |
| g = h = 0 | 1/7 |
| all families but y = 0 | 1/5 |
| g, h additive or pair | 0.1350 (conservation makes simple h too rigid) |

Without the 6-relay (g, h), no rule beats 1/7. With y only, the optimum is 7/27 = 0.259259 using 942 weights (verified).
Fixed y-only models, verified: per D 2/3, add 0.413989 (11 features), pair 0.296703 (63); y pair + x per (from, to)
+ lq const gives 0.282737.

## 5. Notes

- Rationals: the small rules are LP vertices with exact small-denominator values (1/3; 1/4; 6/55, ...; x/51), so no
  rounding was needed.
- The sparse rules near t = 0.125 still carry about 250 h and 50 g key-level weights. The 6-relay is the
  incompressible part: conservation at every 6 for every apex word forces h to track g key by key.
- Files: scripts in `s54/` (`run1.sh`, `lpath.sh`, `prune*.sh`, `ucheck.sh`, `fit_ls.py`, `support.py`,
  `explain.py`, `fails.py`, `round_sol.py`). Runs are in `s54/runs/<tag>/` (`solve.log`, `upper.log`, sol JSON);
  supports are in `s54/sup/`; checks are in `s54/checks/`. `python3 s54/explain.py <sol>` prints any rule in words.
