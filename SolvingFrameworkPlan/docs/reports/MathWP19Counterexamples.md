# Two order-24 counterexamples

Math, 5 October 2026. These are extracted from the completed, independently reproduced WP19 P3 phase, not a further search. Graph indices, vertices and fan indices are zero-based. Full certificates and both graph records are in `longtable/audit/wp19-counterexamples.json`; compact independently reconstructed paths and layers are in `wp19-named-kills-results.json`. The complete phase is archived losslessly with its raw digest in `longtable/wp19/WP19-verified-output-manifest.json`.

## 24:6406: every choice needs a three-move allowance

This graph has 14 degree-five vertices, eight degree-six vertices and two degree-seven vertices (1 and 21). Every one of its 70 legal vertex/fan pairs has an admitted start whose mixed fill distance exceeds two. The complete pair maxima are:

| Maximum mixed fill distance L | Pairs |
| --- | ---: |
| 3 | 58 |
| 4 | 12 |

Consequently its exact best-choice value is **m=3**. This kills C1 (m≤2 at every order≥18) and C3 (m≥3 implies all degrees 5/6). U∃ still holds on the graph.

At vertex 0, fan 0, the 134 admitted starts have distances 0/1/2/3 in counts 22/81/28/3, respectively. One worst start is

```
[4,0,1,2,1,3,2,3,2,3,2,0,1,3,0,1,0,1,0,3,1,3,2,2]
```

Here 4 denotes the hole. A three-Kempe path is K(1,3,seed 2), K(0,1,seed 1), K(0,3,seed 1), with global canonical relabelling after each move. Saved lower witnesses cover all 70 pairs, not just this exhibited start. The package checker verifies them; Math's complete replay also reconstructs all families and maxima.

ASCII rotation and SHA-256:

```
24 bcdef,afghijc,abjkld,aclmne,adnof,aeogb,bfopqh,bgqri,bhrsj,biskc,cjstul,ckuvmd,dlvwn,dmwoe,enwpgf,gowvq,gpvxrh,hqxtsi,irtkj,ksrxu,ktxvl,luxqpwm,mvpon,qvutr
47cb6dc88b4225dfafce0bfec21f30265c8865ad54ecc0df8d387212938d136b
```

## 24:7228: a slide saves two Kempe swaps

At vertex 17, fan 0, the link is [7,16,23,18,8] and the added chords are 7–23 and 7–18. This admitted start has **exact ℓ=3 and κ=5**:

```
[0,1,2,3,1,2,0,3,2,3,1,2,3,0,3,2,1,4,1,0,2,1,3,0]
```

A mixed filling path is slide to 8, K(1,2,seed 1), K(0,1,seed 0). A pure Kempe filling path at the original hole is K(1,2,seed 1), K(0,2,seed 0), K(0,3,seed 0), K(2,3,seed 2), K(0,3,seed 0). Both use canonical colour labels after each move; every component is recomputed in the current deletion.

The independent breadth-first layers are:

| Depth | New mixed states | Mixed targets | New Kempe-only states | Kempe targets |
| --- | ---: | ---: | ---: | ---: |
| 0 | 1 | 0 | 1 | 0 |
| 1 | 7 | 0 | 4 | 0 |
| 2 | 27 | 0 | 8 | 0 |
| 3 | 82 | 1 | 10 | 0 |
| 4 | — | — | 13 | 0 |
| 5 | — | — | 26 | 6 |

Thus κ−ℓ=2, killing M2's proposed allowance of one extra Kempe swap. The saved kill alone certifies κ≥5; the explicit pure path and independent reconstruction establish equality. This graph nevertheless has **m=1** and U∃ holds: the best pair can be easy even though another pair has a difficult individual start.

ASCII rotation and SHA-256:

```
24 bcdef,afghijc,abjkd,ackle,adlmf,aemnogb,bfopqh,bgqri,bhrstj,bitkc,cjtld,dktme,eltunf,fmuvo,fnvpg,govwxq,gpxrh,hqxsi,irxwt,iswumlkj,mtwvn,nuwpo,pvutsx,pwsrq
a031bc58029463df7662cfeafb89aba76915f4706c13cebd29e89fefadfb6cde
```

Neither example refutes VH∃ or U∃. M1's four-move allowance and C2's m≤3 passed the completed WP19 phases; their universal statements remain open. M3 is independently settled by the hand proof in `MathShortFillTheorem.md` and is consistent with these examples.
