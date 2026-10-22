# Rule fits: simplest discharging rule vs t (s54, Opus, 21 Oct 2026)

**Status: partial (work in progress).** Registry A97, the s53 flag set (`xon apexcls filt16 hat5 consall l3q lqcap=3 l3qV=7,8`,
`rpatN3`, `exname_rm128`), engine `s54/eng` (copy of `s51/eng` plus `pmodel.py`; md5s in `s54/eng/md5*.txt`).
Reference: `s53/run_A97/sol_q53A97.json`, t = 0.098789365409, upperR2 FEASIBLE, about 7,000 free weights.

## Method

- **Model class.** Each family's weight is `w[key] = sum_f theta_f * phi_f(key)`, with generic features built from the raw
  key letters only (`s54/feats.py`). The models are `D` (constant per receiver letter), `add` (one term per letter at
  each key position, positions paired under the key's reflection), `addD` (the same per D), `pair` (add + adjacent-pair
  terms), `full` (one weight per key), `zero` (family off) and `free` (the original columns).
- **Parametric LP (`pm=fam:model,...`).** Every row coefficient on a key is spread onto that family's theta columns, and
  solveR2's separation runs unchanged on the rule the thetas define. Each family's bounds (>= 0; x and lq <= 3) are rows
  over its **whole key universe**: y 942, g 393, h 18,683, x 70,875, r 153, lq 40. The written sol stores the model
  evaluated on the whole universe, so upperR2 checks exactly that rule.
- Warm pool: `s51/eng/rows_q53A97.txt` (21,241 receiver rows). "pool t" is the LP over the pool only (`nosep`), a
  lower bound for that model. A **verified** t is a separation run to convergence followed by upperR2 FEASIBLE.

## 1. Regress and round (least squares on the reference weights)

Fits over the family's universe (absent key = 0), `s54/fits_ls.txt`. The fits are poor (y: R^2 <= 0.68 even with 135
pair features; h: R^2 <= 0.55), so rounding them is hopeless. The parametric LP is the main route.

| family | model | rank | R^2 | max abs error |
|---|---|---|---|---|
| y | D | 3 | 0.29 | 0.56 |
| y | add | 11 | 0.53 | 0.43 |
| y | pair | 63 | 0.64 | 0.43 |
| y | pairD | 135 | 0.68 | 0.44 |
| g | add | 8 | 0.83 | 0.14 |
| g | pair | 26 | 0.93 | 0.12 |
| h | addD | 42 | 0.46 | 0.29 |
| h | pair | 78 | 0.55 | 0.26 |
| x | side | 133 | 0.02 | 0.13 |
| r | side | 17 | 0.63 | 0.13 |

## 2. Which families matter (pool t; y free unless stated, other families free)

| change | pool t |
|---|---|
| none (all free) | 0.089202 |
| r (hat channel) = 0 | 0.089202 (r is not needed) |
| x = 0 | 0.113400 |
| x per (from, to) degree only (9 params) | 0.111111 |
| lq = 0 | 0.111111 |
| g = h = 0 (no 6-relay) | 0.142857 = 1/7 |
| everything but y = 0 | 0.200000 |
| g additive, h additive per D | 0.134986 |
| g pair, h pair | 0.134986 |
| y per D only (3 params) | 0.183544 |
| y add / addD / pair / pairD | 0.117877 / 0.111240 / 0.092770 / 0.090342 |

## 3. Verified rules (separation to convergence, then upperR2)

| rule | free params | verified t | upperR2 |
|---|---|---|---|
| y per D, all else 0 | 3 (1 distinct value) | 2/3 = 0.666667 | FEASIBLE |
| y additive (D + flank letter + far letter), all else 0 | 11 | 0.413989 | FEASIBLE |
| y pair, all else 0 | 63 | 0.296703 | FEASIBLE |
| y pair + x per (from, to) + lq const | 63 + 9 + 2 | 0.282737 | FEASIBLE |
| y free (one weight per key), all else 0 | 942 | 7/27 = 0.259259 | FEASIBLE |
| reference sol_q53A97 | ~7,000 | 0.098789 | FEASIBLE |

The simplest rule so far: **"a 5 sends 1/3 to each neighbour of degree >= 7"** (t = 2/3).

## 4. All families together: lasso path and forward selection (in progress)

- **Lasso path** (`s54/lpath.sh`): one LP over the pool with every family on a generic dictionary (y: D, addD, pairD,
  full; g: const, add, pair, full; h: D, addD, pair, full; x: FT, side, sideFT; r: const, type, side, full; lq: const,
  full; about 22,000 features) and objective t + lambda * sum |theta|. Its support is then **refit** (lambda = 0) with
  separation to convergence, and upperR2 checks the refit.
- **Forward selection** (`pm=...:sel`, column generation): start from nothing; at each converged LP price every
  dictionary feature exactly from the duals, try the 24 best as new columns, keep the one that lowers t most, separate
  again. Snapshots `s54/runs/S1*/sol_*_sNNN.json`.

| rule (all families) | nonzero params | verified t | upperR2 |
|---|---|---|---|
| selection: y const | 1 | 2/3 | (converged LP; = the y-per-D rule) |
| selection: + flank 6 | 2 | 1/2 | converged LP |
| selection: + flank 5 | 3 | 5/11 = 0.454545 | converged LP |
| selection: + flank-far pair 6-6 | 4 | 10/23 = 0.434783 | converged LP |
| selection: + pair 5-5 | 5 | 19/44 = 0.431818 | converged LP |
| selection: + pair 5-6 | 6 | 7/17 = 0.411765 | converged LP |
| lasso 0.3 refit (y only) | 14 | 2/5 = 0.400000 | FEASIBLE |
| lasso 0.1 refit | 27 | 0.305482 | FEASIBLE |
| lasso 0.03 refit | 86 | 0.189687 | FEASIBLE |
| lasso 0.01 refit | 137 | 0.158213 | FEASIBLE |
| lasso 0.01 refit, second pass (pool + refit rows) | 159 | 0.152003 | FEASIBLE |
| lasso 0.003 refit | 436 | 0.145762 | FEASIBLE |
| lasso 0.001 refit | 366 | 0.137847 | FEASIBLE |

Finding so far: the 6-relay (g, h) is what takes t below 1/7, and it needs only 3 to 7 h features
("6 -> big: per first link nbr 5 / 6 followed by a 5, per small apex beside a first link nbr 5"), but g then needs
key-level corrections. Forward selection stalls at 7/17 with 6 y features, because the relay needs g and h columns
together; a lasso block step over the candidate pool is being added for that.

