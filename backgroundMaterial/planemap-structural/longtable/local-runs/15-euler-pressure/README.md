# 15-euler-pressure [exploratory, no proof claimed]

Question: are doubly locked (DL) states closer to Euler saturation (bipartite planar: edges <= 2K-4) than other states?

## Definitions (exactly as computed; code in euler_features.py)
- G = T - v, v a degree-5 hole; state = proper 4-colouring of G up to renaming (kempe_py.Space). Link x0..x4 = cyclic rotation of v.
- Filled: link uses <= 3 colours. Otherwise alpha = repeated colour at x_j, x_{j+2}; m = x_{j+1}; a = x_{j+3}; b = x_{j+4}; mu, A, B = colours of m, a, b.
- DL: a in the {mu,A}-component of m AND b in the {mu,B}-component of m. Radius = dist_to_filled in the whole-component Kempe move graph (kempe_py).
- B_c = edges with exactly one end coloured c; K_c = its non-isolated vertices; slack_c = 2K_c - 4 - |E(B_c)|. sl_mu, sl_alpha, min_sl (min over 4 colours); mean_sl = mean over colours; sl_mu_rel = sl_mu / (2K_mu - 4).
- U = K1 u K2, K1 = {mu,A}-component of m, K2 = {mu,B}-component of m. Uv=|V(U)|, Ue = edges inside K1 plus edges inside K2, Urank = Ue - Uv + 1, Uslack = 2Uv - 4 - Ue.
- F = full mu-vs-{A,B} bipartite subgraph (all edges with colours {mu,A} or {mu,B}; isolated vertices dropped): Fv, Fe, Fslack = 2Fv - 4 - Fe.
- KY: for i in {alpha,A,B}, H = G[V_mu u V_i], ky_i = sum over components C of max(|C n V_i| - |C n V_mu|, -1); ky_tot = sum. Extras: pen_i = sum over colour-i vertices of max(2 - deg_H, 0); ky_min_c / ky_mean_c = ky_tot with each of the 4 colours as mu (min / mean), defined for filled states too.
- Groups (disjoint): filled; unfilled_nonDL; DL_r2 (radius 2); DL_r3p (radius >= 3). DL never has radius < 2 (asserted).
- Data: all degree-5 holes of every gentri graph at orders 12,14,16,17,18,19,20 ('main'), plus the order-22 F-cycle graph, hole 15 ('ext'; only 252 states, 1 class, 40 DL_r2 + 12 DL_r3p... see results.json). Orders 13, 15 have no core graphs in the files used.
  243,727 states total; main counts: filled 120,285; unfilled_nonDL 99,388; DL_r2 23,249; DL_r3p 553.

## Commands (pure Python, nice -n 10, 3 workers, total ~20 s)
    nice -n 10 python3 scan.py --orders 12 14 16 17 18 19 20 --workers 3 --out states-12-20.csv.gz
    nice -n 10 python3 fcycle22.py fcycle22-states.csv.gz
    (gzip -dc states-12-20.csv.gz; gzip -dc fcycle22-states.csv.gz | tail -n +2) | gzip > states-12-22.csv.gz
    nice -n 10 python3 analyze.py states-12-22.csv.gz results      # writes results.json (needs numpy; makes a .npy cache, delete it)
scan.py's floor tag / --floor-orders and hard.py's certificate part were not used (hard.py is only imported for build()).

## Results, scope main (orders 12-20): mean / min / max
| quantity | filled | unfilled non-DL | DL r2 | DL r3+ |
|---|---|---|---|---|
| min_sl | 6.21/2/9 | 6.29/2/9 | 6.52/2/9 | 7.55/5/9 |
| sl_mu | - | 9.55/4/18 | 8.06/4/15 | 8.18/5/13 |
| sl_alpha | - | 7.50/2/15 | 9.14/2/16 | 9.51/7/13 |
| Uslack | - | 4.90/0/8 | 6.68/4/9 | 6.79/5/8 |
| Uv (Urank) | - | 9.1 (1.2) | 12.9 (3.2) | 13.0 (3.2) |
| Fslack | - | 7.88/2/13 | 7.22/4/11 | 7.12/5/10 |
| ky_tot | - | 1.31/-4/10 | -0.44/-4/7 | -0.21/-3/3 |
| pen_tot | - | 6.79/0/21 | 3.57/0/15 | 3.98/0/10 |

Effect sizes vs unfilled non-DL (Cohen d; hole-matched mean difference, fraction of holes where DL mean is lower):
sl_mu -0.70 / -0.62 (-1.46, 91%); sl_alpha +0.76 / +0.99; Uslack +1.00 / +0.97 (DL has MORE slack; lower in 0.4% of holes); Fslack -0.46 / -0.50; ky_tot -0.90 / -0.75; pen_tot -1.09 / -0.90 (-3.2, 98% of holes); min_sl +0.19 / +0.99.

Saturation counts: DL states with slack 0 in U: 0 (min Uslack = 4); in F: 0 (min Fslack = 4); sl_mu = 0: 0; min_sl = 0: 0. (Non-DL unfilled: 4,883 states have Uslack 0 - small components, mostly trees/Urank 0; no state at all has Fslack or any B_c slack 0.) The same holds in scope ext (order 22 included). Full tables: results.json.

## Reading
Only sl_mu (about 1.5 lower) and the KY-type sums (ky_tot, pen_tot) are systematically smaller for DL states, and even there the minima are not extreme (sl_mu >= 4, ky_tot >= -4, same as non-DL). Slack in U and sl_alpha are LARGER for DL. No Euler saturation in any examined bipartite subgraph for any DL state. The sl_mu / pen effect may be partly a size effect (DL forces larger mu-components); not controlled for here.
