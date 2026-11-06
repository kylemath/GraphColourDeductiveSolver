| group | side | rules | justified (keep pool) | found by Studio hint | found only by full-pool search | not justified in keep pool | of which justified by a non-keep config | of which exname-held only | not justified in any pool |
|---|---|---|---|---|---|---|---|---|---|
| d7_w6 | - | 2,437 | 1,693 | 1,513 | 180 | 744 | 136 | 0 | 608 |
| d8_w6 | - | 1,738 | 1,122 | 1,112 | 10 | 616 | 98 | 0 | 518 |
| d9_w6 | - | 463 | 87 | 87 | 0 | 376 | 68 | 0 | 308 |
| d7_w7 | +1 | 1,440 | 1,040 | 923 | 117 | 400 | 25 | 0 | 375 |
| d7_w7 | -1 | 1,440 | 1,040 | 923 | 117 | 400 | 25 | 0 | 375 |
| d8_w7 | +1 | 904 | 731 | 712 | 19 | 173 | 2 | 0 | 171 |
| d8_w7 | -1 | 904 | 731 | 712 | 19 | 173 | 2 | 0 | 171 |
| **total** | | 9,326 | 6,444 | 5,982 | 462 | 2,882 | 356 | 0 | 2,526 |

Reason for not justified in the keep pool (Studio DERIVE justifiers re-tested in the true 2-ball):

| group | side | faceset_only | no_embedding_true_2ball | no_studio_justifier | BUG |
|---|---|---|---|---|---|
| d7_w6 | - | 46 | 698 | 0 | 0 |
| d8_w6 | - | 134 | 482 | 0 | 0 |
| d9_w6 | - | 10 | 366 | 0 | 0 |
| d7_w7 | +1 | 19 | 381 | 0 | 0 |
| d7_w7 | -1 | 19 | 381 | 0 | 0 |
| d8_w7 | +1 | 23 | 150 | 0 | 0 |
| d8_w7 | -1 | 23 | 150 | 0 | 0 |

w7 rules by where they can fire (7-side: c >= 7 or ap >= 7 possible; <=6 side: c <= 6 and ap <= 6 possible):

| group | side | fire 7-sides only: J / NJ | fire <=6 sides only: J / NJ | fire both: J / NJ |
|---|---|---|---|---|
| d7_w7 | +1 | 261 / 85 | 778 / 313 | 1 / 2 |
| d7_w7 | -1 | 261 / 85 | 778 / 313 | 1 / 2 |
| d8_w7 | +1 | 108 / 27 | 623 / 146 | 0 / 0 |
| d8_w7 | -1 | 108 / 27 | 623 / 146 | 0 / 0 |

filtered file rules_studio_keep95p131f_W18strict.json: 6444 rules, md5 c67fa1d1ba6739dea8d522713d9de622, mirror-consistent True
filtered file rules_studio_keep95p131f_W18withnonkeep.json: 6800 rules, md5 daa453d45dcae3617fac76d8616b7859, mirror-consistent True
