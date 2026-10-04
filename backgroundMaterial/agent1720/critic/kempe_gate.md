# Gate: K4, K5, K6

**Date:** 2 October 2026
**Meeting:** critic with the main planning team
**Reports:** `K4_report.md`, `K5_report.md`, `K6_report.md`
**Checked against:** `K4_results.json`, `K5_verify.json`, `K5_partC_raw.json`, `K6_cache_n4_11.json`, `K6_named.json`

## Accepted as computations, not theorems

| Claim | Witness in the files |
|---|---|
| \(s_1 \le d+1\) on triangulations \(n=6,\ldots,10\) | `K4_s1_gt_d+1` empty; \(s_1-d \in \{0,1\}\) |
| A K1-safe 4-colouring of \(G-v\) need not 4-colour \(G\) | \(T_{6,0}\), vertex 0, colouring \(0{:}5,1{:}1,2{:}2,3{:}3,4{:}4,5{:}2\), \(d=s_1=0\), \(d_2=s_2=2\) |
| \(\mathcal{R}(G,5)\) connected and every class contains a 4-colouring, triangulations \(n\le 11\) | Part A summaries, `all_connected` and `all_classes_contain_le4` |
| Non-strict monotone reduction, same range | `monotone_failures` \(= 0\); `max_plateau` is \(0,1,2,3,3,4,4,5\) |
| KC5, triangulations \(n\le 11\), icosahedron, Errera's 12 degree-5 vertices | `n_bad_classes` \(= 0\); Errera max distance to a fix is \(3\) |

Given Meyniel (1978), the sentence "every proper 5-colouring of a planar graph Kempe-reduces to a 4-colouring" is a reformulation of the Four Colour Theorem. The citation is accepted. The proof of Meyniel is not in this repository, so the reformulation stays conditional on that paper.

## Killed

The strict monotone statement (a swap that decreases the size of colour 5 whenever that size is positive). Witness: \(T_{5,0}\), colouring \((1,2,3,5,4)\), first swap of colours \((3,4)\) on \(\{2\}\) leaves the size equal to 1.

## Refused

- Marking any of these universal. \(n=11\) was not run for K4. Kittell's triangulation was not checked: the stored graph is not planar and has the wrong number of edges.
- Treating Errera as a kill of KC5. It kills Kempe's two-swap procedure. On the stored Errera graph, KC5 holds.
- Marking Track 1 proved or killed. The root sentence is a reformulation, conditional on Meyniel.

## Still open, and not a new theorem

On the same K4 run, \(s_2 \le d_2+1\) at every stored orbit through \(n=10\) (at \(n=10\) the gap \(s_2-d_2\) is \(0\) or \(1\)). That is the target that actually extends to a 4-colouring of \(G\). It is a finite observation. The next run must write a new file and must not overwrite `K4_results.json`.
