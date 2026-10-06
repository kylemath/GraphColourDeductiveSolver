# Lock counting: are locked classes equitable?

Long Table (Lock-Counting team), 5 October 2026. EXPLORATORY, post hoc, undeclared. Nothing here is evidence for a declared claim. Orders <= 18 only.

Setting: T has min degree 5 (`-m5`) or is 4-connected with degree >= 4 (`-c4m4`); x has degree 5; y is a neighbour with legal apex fan; G = T - xy. A class is locked if its Kempe class in G (whole-component swaps) has c(x) = c(y) in every member and no member with c(x) != c(y). Code reuses `tilley_apex.py`, `lock_anatomy.py`, `vhphi_explore.py` unchanged.

## 1. Data

Counts are over members (one canonical colouring each, colour permutations quotiented), the same convention as `tilley-separability.md` section 8. "Sizes" are the sorted colour-class sizes of the colouring of T - x.

| Family | Order | Graphs | Locked classes | Members | Sizes in T - x | Chains = full colour pairs | Full-pair complement forests |
|---|---|---|---|---|---|---|---|
| -m5 | 12, 14, 15, 16, 18 | 1,1,1,3,12 (order 13: none exist) | 0 | 0 | none | | |
| -m5 | 17 | 4 | 32 (10 on 17:0, 22 on 17:1) | 192 | (4,4,4,4): 192 | 164 of 192 | all 164 |
| -c4m4 | 10, 11, 12, 13 | 10, 25, 87, 313 | 0 | 0 | none | | |
| -c4m4 | 14 | 1,357 | 1 (graph 5, x=12, y=7) | 6 | (3,3,3,4): 6 | 6 of 6 | 6 of 6 |
| -c4m4 | 15 | 6,244 | 2 (graph 1, (x,y) = (9,14) and (14,9)) | 12 | (3,3,4,4): 12 | 12 of 12 | 12 of 12 |

Degrees at the 4-connected locks (ring in cyclic order around x):
- 14:5, x=12, y=7: deg y = 7, ring degrees (7,4,6,6,4). Two degree-4 ring vertices.
- 15:1, x=9, y=14: deg y = 5, ring degrees (6,6,4,5,5).
- 15:1, x=14, y=9: deg y = 5, ring degrees (5,4,6,6,5).
Each has one degree-4 ring vertex (15:1) or two (14:5). Neither is minimum degree 5.

**Plain statement.** At order 14 the sizes are (3,3,3,4) with 13 vertices in T - x, and at order 15 they are (3,3,4,4) with 14 vertices. Both are as balanced as 13 and 14 allow, so exact equitability cannot hold there and **near-equitability (sizes within 1) survives in all 18 members**. Sample is tiny: 3 locked classes on 2 graphs. The -m5 data has no lock outside 17:0 and 17:1. The 4-connected locks lie in a family that allows degree-4 vertices, so the two families do not independently confirm each other.

The forest column comes from `lockcount_forest.py` (section 3). Order-17 non-full members are the 28 with one non-forest complement pair (see section 3).

## 2. Commands

Run from `backgroundMaterial/planemap-structural/longtable/explore-vhphi/`. P is `/private/tmp/claude-501/-Users-fulkanjou-GraphColour/28402cc5-3e09-4c31-94e9-5ae923a5533c/scratchpad/plantri58/plantri`.

```
for n in 10 11 12 13 14 15; do $P -c4m4 $n -a | python3 lockcount_probe.py $n lockcount-c4-$n.json 14; done
for n in 12 14 15 16 17 18; do $P -m5 $n -a | python3 lockcount_probe.py $n lockcount-m5-$n.json 14; done
$P -m5 17 -a   | python3 lockcount_forest.py 17 0,1   > lockcount-forest-17.txt
$P -c4m4 14 -a | python3 lockcount_forest.py 14 5     > lockcount-forest-c4-14.txt
$P -c4m4 15 -a | python3 lockcount_forest.py 15 1     > lockcount-forest-c4-15.txt
```

Not run: `-c4m4 16` (started, killed for time, partial output deleted). `-m5 13` has no graphs and `-m5 < 12` is not accepted by plantri.

## 3. Forest lemma and counting

Notation. c is a member colouring of a locked class with c(x) = c(y) = 1. V_i are the colour classes of T - x with sizes n_i, so V_1 contains y; m = n - 1 - n_1. Everything below is in G = T - xy (a triangulation with one quadrilateral face x,a,y,b). T - x has n - 1 vertices and 3n - 11 edges. e_ij counts edges between V_i and V_j in T - x. S_1 = sum of degrees in T - x over V_1 = e_12 + e_13 + e_14, since V_1 is independent. E_234 = e_23 + e_24 + e_34, so S_1 + E_234 = 3n - 11.

**Lemma F [hand]** (full chains give forests). Suppose for some k in {2,3,4} the {1,k}-chain through x and y equals V_1 u V_k u {x}. Let {j,l} = {2,3,4} minus {k}. Then G[V_j u V_l] is a forest.
Proof. Suppose it has a cycle C. C is a cycle in G alternating colours j and l, so it has even length >= 4. Take an edge uv of C and the face of G on one chosen side of it. This face is not the quadrilateral, since every edge of the quadrilateral is incident to x or y. So it is a triangle uvw. The triangle is properly 4-coloured and has colours j and l on u and v, so w has colour 1 or k (w may be x, which has colour 1). Hence w is a vertex of the chain, and w is not on C. It lies strictly on the chosen side of C, since a face at an edge of C lies in the closed disc on its own side and w is not on C. Applying this to both sides of uv gives chain vertices strictly on both sides of C. The chain is connected in G and avoids all vertices of C (colours 1 and k). By the Jordan curve theorem any path between the two sides meets C. Contradiction. QED

This uses only the single chain {1,k}. If all three chains are full, as in 164 + 6 + 12 members, the three pairs {3,4}, {2,4}, {2,3} induce forests. Data agree: all 182 full members satisfy it. In the 28 non-full members on order 17, exactly one of the three complement pairs fails to be a forest (the failing pair is not forced by anything I proved). That matches Lemma F in contrapositive form and is unproved as a statement about all locks.

**Consequences [hand, assuming all three chains full].** Forests give e_jl <= n_j + n_l - 1, so E_234 <= 2m - 3. Then:
- S_1 = 3n - 11 - E_234 >= n + 2 n_1 - 6.
- S_1 <= 2(n - 1) - 4 = 2n - 6, since the edges of T - x between V_1 and the rest form a planar bipartite graph. This holds for every 4-colouring, with no lock.
- Min degree 5: ring vertices in V_1 are only y (the other four neighbours of x are in G coloured differently from x), and ring vertices have degree >= 4 in T - x. So S_1 >= 5 n_1 - 1.
- Upper counting from degrees: sum over V_2,V_3,V_4 of degrees = 2 E_234 + S_1 >= 5m - 5, giving S_1 <= n + 5 n_1 - 12.

What these give: n_1 >= 2 (from the first and last), n_1 <= (2n - 5)/5 (from the second and third; the same bound holds for any colour class that avoids x's other ring vertices, and for n_1 in any 4-colouring), and n_1 <= n/2. At n = 17 that is 2 <= n_1 <= 5, data 4. **None of this bounds n_2, n_3, n_4 below, and none forces balance.** A small class V_k has few edges, so its degree demand is also small, and the forests in the complements give only upper bounds. I found no inequality of the degree/planarity/Euler family that pushes the sizes together.

**Euler route [hand].** For the induced graph on V_2 u V_3 u V_4 inside T, Euler's formula with F_1 = 2n - 4 - S_1 triangular {2,3,4} faces and one face around each V_1 vertex reduces to the identity c = 1. It carries no information without the forest condition, which is Lemma F. With Lemma F it becomes the bound above.

**Data tightness.** For the full order-17 members (E_234, S_1) is (19,21) in 108 and (20,20) in 56 members, against the forest ceiling E_234 <= 2m - 3 = 21 when n_1 = 4. The slack is 1-2. At orders 14 and 15 the data are (E_234, S_1) = (15,16) and (15,19); I did not record n_1 per member, so I make no tightness claim there. The order-17 near-tightness is a possible lead (the complement forests are almost spanning trees), not pursued.

## 4. What is NOT shown

- Equitability or near-equitability is **not proved**. The only proved statements are Lemma F and the bounds on n_1 in its consequences, which hold only for locks whose chains are full, and the bounds that need no lock (planarity and min degree only).
- No lower bound on any n_i (i != 1) and no balance statement.
- The 28 non-full members at order 17 (chains not full pair-for-pair) are not covered by Lemma F; only data show the non-forest complement.
- Near-equitability at orders 14/15 rests on 3 locked classes of two graphs, in a family where x has degree-4 ring neighbours. It could be a coincidence of small sample.
- `-c4m4` order 16-18 and `-m5` beyond 17 locks: not checked (c4m4 16 was started and aborted). The 4-connected scan covers degree-5 x only.
- The locks being counted are those of the apex-fan pair; no connection to the pure-fill escapes (sections 7-8 of `tilley-separability.md`) is made here.

## 5. Files and SHA-256

Code (new, in `explore-vhphi/`): `lockcount_probe.py`, `lockcount_forest.py`. No existing file rewritten, nothing committed or staged.

```
6d911748c6233baaef5f900bddb6cda3930625dbe8d0f849ac743a88880c739a  lockcount_probe.py
9ab4b3693c11da959eb92e10f627d9730f1624a5ba242c338f55df056f70d0a4  lockcount_forest.py
ec8fadd9e9c280bc51c633cd421771452bc3020107cda4d8907350a9a5f1a00e  lockcount-c4-10.json
c2b80ad9e867d97d30b9658f261aa21f7b41736f0dab15d776c96b3d910a76d0  lockcount-c4-11.json
5d92f27d62c06f6edb146e91029ca89528bcdb2185faa809331ad601f37f875b  lockcount-c4-12.json
41c08650d85f37a1817ea81dab5591efbd689312db1323fa9eeeafd0d1a40093  lockcount-c4-13.json
04a111f31c8eb46362b48f1a2396c196ff00bf5a4cdbc996d2ae0ffcff04eae2  lockcount-c4-14.json
53225a84fd2a113e93b333113c8356279ca489ce39a229eb05dac378bc4b2c77  lockcount-c4-15.json
9df08d2ff8f32b9e1b9d31f30297a97fe2ad745c4eea233a92aea0bf6aa5437b  lockcount-m5-12.json
dfa66853de1b1193dd6a81e2660cea32144dd3823ceab112ad470ae683044d8d  lockcount-m5-14.json
4fce98b45198e6cd8ec865b52835914f3eb7332a3774c62b529d7bab1747c374  lockcount-m5-15.json
a5eddb1b090595c3bb10f75541ec7de2cda268e2f15208e5336a96ba10c3025e  lockcount-m5-16.json
b2cbd1810d06e937dc48c9f8b002f586eda646d5468f022e102fa56c9ddb81d0  lockcount-m5-17.json
5427f3defb3e3812278cf7456c9e9f07aa63e7054d74dacbe87a1d50a656d5fa  lockcount-m5-18.json
a2943183a1f0a84ca8db66a911546c8d18b725702b93fb7c39c04ee4a6872521  lockcount-forest-17.txt
213b9ca25ea8cf28c9deb54e093a153af739d58118b913241dc3f05064b47da3  lockcount-forest-c4-14.txt
6d1baf49d3680fe48fe2162690b7d55f4e1a5ab881b105146ba4c1e027dbf87c  lockcount-forest-c4-15.txt
```
