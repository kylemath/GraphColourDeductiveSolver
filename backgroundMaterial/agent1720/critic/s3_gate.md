# Gate: S3 D-reducibility

**Date:** 2 October 2026
**Report:** `backgroundMaterial/agent1720/groups/S3_report.md`
**Checked against:** `backgroundMaterial/agent1720/groups/S3_results.json`

## Accepted as a computation

Robertson–Sanders–Seymour–Thomas (1997) call a free completion D-reducible when the maximal consistent set of bad ring edge-colourings in $\{-1,0,1\}$ is empty.

| Configuration | Edge-colourings | Extend | Maximal consistent bad set | D-reducible |
|---|---|---|---|---|
| Birkhoff diamond, ring 6, four interior vertices of degree 5 | 729 | 96 | empty | yes |
| One degree-5 vertex, ring 5 | 243 | 30 | 30 | no |
| One degree-4 vertex, ring 4 | 81 | 15 | empty | yes |

Elapsed 0.0176s. Direct extension is weaker: 348 of 732 vertex 4-colourings of the diamond's ring do not extend. The file `compute/discharging/reducibility_checker.py` does not run this test. Its diamond is one interior vertex of degree 6.

## Not accepted

`S3b_results.json` records `degree5_vertex.d_reducible: true` and `failures: 0`, while its `claims` field says the opposite. The RSST count leaves 30 bad colourings on that ring. The S3b degree-5 flag is not accepted.

## Not proved

This is one configuration, not the 633, and not a discharging proof. The 1997 paper was not re-proved.
