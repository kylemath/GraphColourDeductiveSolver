# Families among the reducible configurations and rule parts (FAM-1, 11 Nov 2026)

Light, read-only analysis, one engine (this thread's own Python, about 3 CPU-min). Nothing here is a proof claim. The outside team's files were used as data only.

**Inputs**
- Configurations: `swarm/outside/beat_633/data/pool_configs.json` (md5 079eccb5). Entries 0..632 are RSST's 633 configurations with full rotations and degrees: 249 D, 333 C, 51 C_merge. Entries 633+ (3,462 other reducible configs: nl51, PATS44, windows) were used only as a reference set.
- Rule parts: `swarm/outside/beat_633_588/synth_rules_588.txt` (50b1cf1b), the outside team's 604 parts at SCALE 60.
- Neighbourhoods: `beat_633/data/stage1_ext_profile.jsonl` (972cb6fe). This file lists the leaves (hub degree d, link word) that have exactly one RSST killer, capped at 400 per configuration (309 configurations hit the cap, 83 have none).

Code is in `code/` and outputs in `results/`. Rerun with `python3 code/run12.py 20 N1POOLN2`, then `code/step3.py`, `code/step4.py` and `code/step5probe.py`, all run from a folder that holds `data/` copies of the three inputs.

## Bottom line

1. **The configuration families are real.** On every edit type they beat both random baselines by many standard deviations. The 633 configurations use only 155 embedded interior shapes (140 up to mirror image). The baselines have the same sizes, degrees and ring sizes.
2. **The families are mostly families of degree variants on a shared core.** They are not families that share a reason for reducibility. Neighbours in a family usually differ in reducibility kind (D vs C) and cover different, adjacent neighbourhoods.
3. **The rule parts have some structure, but not "a handful of schemas".** The 604 parts are exactly mirror-closed (303 classes). One-slot edits, retargeting and generic-slot lifts reduce them to 172 schemas (the null gives 300 ± 2). The largest schema has only 8 parts.
4. **Step 5 (a family-level reducibility argument) is not supported by these data, so I did not start it.** The cheapest next test is listed at the end.

## Step 1: configuration edit graph

Configurations are compared by a canonical code of the embedded interior graph (interior rotation, BFS from every directed edge, minimum taken, automorphisms kept) plus the degree vector. Edit types are counted separately:

- `deg1`: same shape, one vertex's degree differs by 1.
- `degk`: same shape, one vertex's degree differs by more than 1.
- `add0`: B minus one vertex is A exactly, with all degrees kept (containment).
- `add1`: B minus one vertex has A's shape, with one degree different.
- `mirror`: A is the mirror image of B.

Results for RSST 633, oriented (unoriented in brackets):

| metric | RSST |
|---|---|
| distinct interior shapes | 155 (140) |
| `deg1` edges | 334 (351) |
| `degk` edges | 8 |
| `add0` (containment) | **0** (as minimality requires) |
| `add1` edges | 1,078 (1,320) |
| families under degree edits only | 327, of which 243 are singletons; largest 31 |
| components under all edits | 47 (24); largest 581 (605) |

**Mirror images:** 63 configurations are mirror-symmetric. The other 570 have a distinct mirror twin, and **none of those twins is in the set**, because RSST lists one configuration per mirror pair. This is consistent with the swarm's 07:14Z ROT finding (4,398 leaves killed only by a mirrored copy). Any rotation-respecting matcher must add the 570 mirrors explicitly.

The largest degree families (all members have the same m):

| size | m | D / C / C_merge | top hub degrees of their forced leaves | examples |
|---|---|---|---|---|
| 31 | 8 | 10 / 20 / 1 | 7: 58%, 8: 42% | 2.1551966, 2.745566, 2.1609562 |
| 25 | 7 | 8 / 16 / 1 | 7: 59%, 8: 41% | 2.1325166, 2.504366, 122.22086 |
| 21 | 8 | 7 / 14 / 0 | 7, 8, 9 | 126.1325166, 126.504126 |
| 18 | 8 | 7 / 11 / 0 | 7: 100% | 482.431, 486.428, 196.428 |
| 14 | 7 | 6 / 8 / 0 | 7: 98% | 2.25866, 122.431, 126.191 |

The full list (25 families of size 4 or more) is in `results/res3.json`.

## Step 2: null baselines (20 replicates each, mean ± sd)

- **N1, shape kept:** each configuration keeps its shape, and its degree multiset is shuffled over its vertices (only feasible placements).
- **N2, random shape:** an induced disc patch of the same m from a random triangulated torus (degrees 5 to 11, 40k random flips), accepted only if its boundary walk matches. That also matches ring size, since ring = Σdeg − 6m + 6 + L. The paired configuration's degree multiset is then placed feasibly.
- **POOL (reference only, not a null):** m-matched draws without replacement from the other 3,462 pool configurations.

| metric (oriented) | RSST | N1 | N2 | POOL |
|---|---|---|---|---|
| shapes | 155 | 155 | 288.6 ± 5.6 | 205.5 ± 2.8 |
| `deg1` edges | **334** | 53.1 ± 3.7 | 12.1 ± 2.3 | 180.1 ± 7.7 |
| `add0` containment | **0** | 27.8 ± 5.6 | 16.7 ± 3.4 | 47.6 ± 5.8 |
| `add1` edges | **1,078** | 272 ± 16 | 147 ± 13 | 841 ± 26 |
| degree families | **327** | 580.0 ± 3.5 | 620.4 ± 2.4 | 451.8 ± 7.5 |
| largest degree family | **31** | 5.7 ± 0.6 | 3.0 ± 0.3 | 12.7 ± 1.8 |
| components, all edits | **47** | 355 ± 14 | 482 ± 11 | 119 ± 10 |

The RSST set is far more clustered than N1 or N2. N1 shows that the clustering is not only shared shapes: degree vectors cluster too.

Caveat: `add1` (delete a vertex and change one degree) is a loose edit. It joins nearly everything into one component even in POOL, and partly in the nulls. The tight, meaningful families are the degree families. The POOL reference is itself generated by edits, which is why it is clustered too.

## Step 3: which configurations cover which neighbourhoods

A neighbourhood type is (hub degree, link word). The table compares the forced-leaf types of pairs of configurations.

| pairs | n | mean Jaccard | share ≥1 type | same dominant hub degree |
|---|---|---|---|---|
| `deg1` neighbours | 334 | **0.058** | 19.5% | **88%** |
| `add1` neighbours | 1,078 | 0.039 | 12.1% | 76% |
| same degree family | 1,810 | 0.017 | 7.3% | 61% |
| random pairs | 20,000 | 0.004 | 2.2% | 41% |
| random, same m and ring | 18,968 | 0.006 | 2.6% | 42% |

Family neighbours work in the same hub degree and share types about 10 times more often than random pairs. Still, about 80% of neighbour pairs share no forced neighbourhood at all. The families **tile** neighbouring link words; they do not cover the same ones. This test is limited because the profile is capped at 400 forced leaves per configuration.

## Step 4: rule schemas (the outside team's 604 parts)

- **Mirror:** the set is exactly mirror-closed. The map is spoke i → 2t − i, the hat comes from the next slot, and fans travel with the spoke, reversed (t = 2). All 604 images are in the set. That gives 303 classes, 8 of them self-symmetric. RSST's 71 give 37 classes.
- **Templates by tag:** 71 `drule` (RSST, weight 6 at SCALE 60, hubs 5 to 8); 493 `SP_` (300 at weight 3, 193 at weight 6, hubs 7 and 8); 40 `ST` (20 `STm_` at −6, 20 `STp_` at +6, hubs 5 to 7). Each −6 part is a rotation of a +6 part, so it is one local picture read from two targets. **The 40 ST parts are 10 objects** (two endpoints × mirror).
- **Schema edits:** `slot1` (same template, hub and weight, one slot differs, mod mirror): 74; `retarget` (same slots up to rotation): 82; `lift` (drop one generic 5..9/5..9 slot to get a hub−1 part): 9.

| set | parts | mirror classes | schemas | singletons | largest | null schemas |
|---|---|---|---|---|---|---|
| all 604 | 604 | 303 | **172** | 97 | 8 | 299.9 ± 1.8 |
| RSST 71 | 71 | 37 | 30 | 23 | 2 | 34.3 ± 2.1 |
| SP 493 | 493 | 246 | 132 | 74 | 8 | 246 |
| ST 40 | 40 | 20 | 10 | 0 | 2 | 19.4 ± 0.7 |

Null: each part keeps its template, hub, weight and target slot. Every other slot is redrawn from that position's empirical distribution, and the result is mirror-closed again.

Reading: exact reproduction needs about 170 parameterised schemas. Dropping to the 14 coarse classes (template × hub × weight) is only possible if every part's slot values stay free parameters, which is not compression. A "handful of schemas" would need a looser schema language, for example interval-valued slots learned to cover several parts. Such a language must be checked against the engine, because it would change what the parts do.

## Probe toward step 5 (no reducibility runs)

- Over the 342 degree-edit pairs, by reducibility kind: C–D 133, C–C 104, D–D 55, C_merge–D 26, C–C_merge 16, C_merge–C_merge 8. **One degree change flips D↔C in 39% of pairs.**
- C–C neighbours with interior contractions use the same aligned contraction set X in 58 of 81 pairs. The 20 C members of the 31-family use 6 different X.
- So the strongest family has no single reducibility mode. A family-level theorem would have to cover D and C members with several contractions. Nothing here points to one structural reason, so step 5 was not started.

**Cheapest next test:** in the 31-family, try its most common aligned X on every member with `kc -C2` + `cfast`, using about 31 short runs through cpuslot. If one X works for every member, that family is the place to look for a structural argument. If it fails, families are bookkeeping only.

## Addendum, 12 Nov: embedding, factor and cluster analysis of the parts (code/embed.py)

Each of the 303 mirror classes is encoded as a raw 124-dimensional vector: hub degree, weight, and for each slot offset −3..+3 from the target, the allowed spoke degrees, the allowed hat degrees and the fan degree counts. I then ran PCA and k-means on these vectors. The null is 10 slot-redrawn sets, as in step 4.

| measure | real | null |
|---|---|---|
| variance on PC1 / PCs 1-3 | 0.141 / 0.317 | 0.132 / 0.265 |
| PCs needed for 90% of variance | 30 | 33.9 ± 0.3 |
| median nearest-neighbour distance | 2.36 | 3.38 ± 0.04 |
| silhouette at k = 5 / 10 / 20 / 40 | 0.12 / 0.13 / 0.16 / 0.19 | 0.08 / 0.08 / 0.07 / 0.07 |

- **Clusters:** the real set clusters more than the null, but the clusters are weak (a silhouette of 0.2 is low). The clusters recover the templates: RSST's parts form one cluster and the tunnel parts another. The SP parts split by which neighbour positions are pinned.
- **Factors:** there is no low-dimensional factor structure. The parts need 30 components for 90% of the variance, against 34 for random parts. The top components read as "the target's hat is a big vertex" (PC1) and "the next spoke is a 5" (PC2).
- **Conclusion:** describing the parts by how they look gives only a mild gain over random. A better test would describe each part by what it does: the charge it moves on each neighbourhood of the world.

## Addendum 2, 12 Nov: the parts described by what they do (code/behav.py, behav_an.py, behav_int.py)

**Method.** For every receiver neighbourhood I computed the expected charge each part moves into the receiver. A neighbourhood here is a receiver degree d plus its link word, taken up to rotation and mirror. Degrees 5 to 8 are exhaustive (25,395 classes at d = 8); degrees 9, 10 and 11 use 15,000 sampled classes each, for 78,172 neighbourhood classes in all. Unknown second-ring degrees are uniform on 5..9+.

The matcher is a port of the outside team's `fit_part`/`Window2Ball` (verify_compact_4ct.py). Run against their own code it gives 0 mismatches on 1.48M fit tests (`code/validate.py`).

Mirror pairs are averaged into one column per mirror class, which gives 305 classes. A part and its mirror do the same job on mirrored neighbourhoods, so after averaging they are identical. The neighbourhoods are then pooled at four coarser levels. The null is 3 slot-scrambled, mirror-closed rule sets, evaluated the same way.

| neighbourhood grouping | groups | factors for 90% (real / null) | factors for 99% | behaviour groups at cosine ≥ 0.999 / 0.99 / 0.9 (real; null) |
|---|---|---|---|---|
| link class (rotation + mirror) | 78,172 | **100** / 176 | 155 / 243 | 236 / 225 / 191 (292 / 285 / 275) |
| link degree multiset | 3,640 | 39 / 65 | 90 / 134 | 228 / 202 / 131 (280 / 266 / 203) |
| where the 5s sit (5 vs not-5 pattern) | 286 | 15 / 20 | 29 / 36 | 146 / 107 / 62 (209 / 168 / 80) |
| receiver degree only | 7 | 3 / 3 | 3 / 3 | 26 / 13 / 7 (32 / 15 / 7) |

**Reading**

- **Lower-dimensional behaviour.** Behaviour lives in a clearly lower-dimensional space than random rules: 100 factors instead of 176 on exact neighbourhoods. This gap is much larger than the shape-only gap (30 vs 34).
- **Duplicate behaviours.** About 70 mirror classes duplicate another class's behaviour (cosine ≥ 0.999); 63 of them are SP parts. The largest groups are 4 to 6 SP parts at hub 7, often a weight-3 and a weight-6 version. 290 of the 305 vectors are distinct exactly, so most duplicates are the same direction at a different magnitude.
- **Named factors at the "where the 5s sit" level.** Factor 1 (18%): charge into a 7 with one 5 neighbour. Factor 2 (16%): into a 7 with two adjacent 5s. Factors 3-4 (11% each): RSST's own rules, a 5 paying its 8+ neighbours, against a 7 with two 5s spaced apart. So the 493 SP parts mostly repair degree-7 receivers next to 5s.
- **Coarse grouping and its limit.** Grouping by where the 5s sit collapses the behaviour to 62 groups at cosine 0.9 (null 80). That grouping is still not a proof object: a rule set must work on every exact neighbourhood, not on averages.
- **Merge candidates, not proven merges.** Equal link-class behaviour does not imply equal behaviour on every full 2-ball, so the duplicate groups are only candidates. Each merge (one part with the summed weight) has to be rechecked on the engine.
