# D3b — Signed Tait counts on duals, $n\le 8$

**Group:** D3b, manager M-Duality
**Date:** 2 October 2026
**Status:** finite check already stored in `D3_results.json`. Read only; the enumerator was not run again.

## 1. Definitions

Implemented in `compute/flows/a1720_alon_tarsi.py`. For a cached triangulation $T$, `dual_rotation` builds the plane dual $T^*$ from `networkx.check_planarity`. Colours are $\{0,1,2\}$ (`colours` in the JSON). A Tait colouring $\varphi$ is a proper edge colouring. `colouring_sign` and `permutation_sign` set

$$\operatorname{sign}(\varphi)=\prod_v \operatorname{sgn}(c_0,c_1,c_2),$$

the product over vertices of $T^*$ of the sign of the three colours in the planar rotation at $v$. The JSON field `definition` states: `sign(phi) = product over vertices v of sgn(colours of the three edges of phi in the planar rotation at v); signed count = sum_phi sign(phi)`. `tally` returns the positive and negative counts. The Tait count is their sum and the signed count is their difference.

## 2. Statement

**Computed.** For every cached triangulation on $n$ vertices with $4\le n\le 8$ ($1+1+2+5+14=23$ graphs), every Tait colouring of the plane dual has one sign, and the absolute value of the signed count equals the Tait count.

The common sign depends on the graph. It is $+1$ for every such dual of even order and $-1$ for every such dual of odd order. There is no single sign for all of these colourings.

## 3. Evidence

Read with `/Users/fulkanjou/GraphColour/.venv/bin/python` from `backgroundMaterial/agent1720/groups/D3_results.json`. No recount. The stored `command` is `/Users/fulkanjou/GraphColour/.venv/bin/python compute/flows/a1720_alon_tarsi.py 8`. The stored `elapsed_seconds` is $0.104$.

`checks`: `matches_d1_tait` true, `rotation_reversal_checks` true, `every_colouring_same_sign_within_its_graph` true, `one_sign_across_all_colourings` false. `signs_seen` is $[-1,1]$. `mixed_sign_graphs` is `[]`.

`per_n`, each with `all_same_sign_within_each_graph` true and `abs_signed_equals_tait` true:

| $n$ | `count` | `common_signs` | `tait_min`–`tait_max` | `signed_min`–`signed_max` | `elapsed_seconds` |
|---|---|---|---|---|---|
| 4 | 1 | $[1]$ | $6$–$6$ | $6$–$6$ | $0.069$ |
| 5 | 1 | $[-1]$ | $6$–$6$ | $-6$–$-6$ | $0.001$ |
| 6 | 2 | $[1]$ | $6$–$24$ | $6$–$24$ | $0.005$ |
| 7 | 5 | $[-1]$ | $6$–$30$ | $-30$–$-6$ | $0.005$ |
| 8 | 14 | $[1]$ | $6$–$72$ | $6$–$72$ | $0.017$ |

On the $17$ graphs with `common_sign` $1$, `signed` equals `tait`. On the $6$ graphs with `common_sign` $-1$, `signed` equals $-$`tait`. Sanity: `K4_tait` $6$, `K4_signed` $6$, `K4_positive` $6$, `K4_negative` $0$.

Ellingham and Goddyn, *List edge colourings of some 1-factorable multigraphs*, Combinatorica (1996), https://doi.org/10.1007/bf01261320: planar cubic 3-edge-colourable graphs are 3-edge-choosable, which is a consequence of 4-colourability plus equal signs, not a proof of non-vanishing.

## 4. Result

**Computed** on the cached triangulations of orders $4$ through $8$. Each dual is monochromatic in sign, and $|\mathrm{signed}|=\#\mathrm{Tait}$. **Literature-settled** for the choosability corollary above. That corollary does not prove the signed count is nonzero.

## 5. Kill criterion

A cached dual with $n\le 8$ whose Tait colourings use both signs, or with $|\mathrm{signed}|\ne\#\mathrm{Tait}$. Not met: `mixed_sign_graphs` is empty and every `abs_signed_equals_tait` entry is true.

## 6. Not proved

The check stops at $n=8$. It does not cover every planar cubic graph. `one_sign_across_all_colourings` is false, so the sign is not constant across this set. `signed` equals `tait` only for `common_sign` $1$. Non-vanishing on these $23$ duals is the already computed Tait count. Extending that existence statement to every bridgeless planar cubic graph is Tait's reformulation of the Four Colour Theorem.

## 7. Feasibility

**High** for the same finite check at $n=9,10,11$: the script and the triangulation cache already exist, and the stored $n=8$ block took $0.017$s. **Low** for a proof that the signed count is nonzero on every bridgeless planar cubic graph without using the Four Colour Theorem.

## 8. Next steps

Leave `D3_results.json` as the record of $n\le 8$. A later call of `compute/flows/a1720_alon_tarsi.py` with upper order $11$ would test the same two predicates on the rest of the cache. That run would still be a finite check. This report does not start it.
