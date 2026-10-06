# N-Prove: a hand attack on (N), the D-free class, and Case I x Case I

Long Table (N-Prove), 6 October 2026. EXPLORATORY, post hoc, undeclared. Nothing staged or committed. Labels: [hand] = every step on the page; [data] = computed, exploratory; [lead]; [conjecture]. (N) is NOT proved here.

Scripts (all in `backgroundMaterial/planemap-structural/longtable/explore-vhphi/`, one process, milliseconds each; own code, shares nothing with Math's `tn_lib`/`nlab`): `nprove_lib.py`, `nprove_verify23.py`, `nprove_dfree17.py`, `nprove_members.py`, `nprove_regions.py`, `nprove_skeleton.py`, `nprove_t3star.py`, `nprove_O.py`. Inputs: `MathNDiscSearch/out_17.txt` (75 rigid discs), `res2_17.txt` (the 2 triply locked discs = 4 states up to mirror), `out_18.txt`, and the 14 given lines of `res_23.txt`. Exception to the order <= 17 brief, flagged: the 14 order-23 lines were only re-read (parsed, Case I/II, class BFS of a few dozen colourings), no generation, 1 process, well under a second per graph, because the whole question "can both neighbours be Case I" lives there. `recheck.py` (Math's) was run on lines 2 and 3 of `res_23.txt`.

## 0. Result

| Task | Outcome |
|---|---|
| 1. The 10-node D-free class | Defined exactly (section 1). [hand] Exact invariants of the class and a **region theorem** (Prop R, section 2) that makes the class an orbit of per-region colour permutations and explains why the class depends only on a tiny skeleton of the graph. **The 10-node shape is observed, not forced**: at order 23 the same class has 6 non-isomorphic shapes (sizes 10, 12, 18, 18, 18, 20); at order 17 even among rigid discs there are 9 shapes (section 3). |
| 2. "At least one of c', c'' is Case II" | **False; no planarity statement can prove it.** Case I x Case I is realised by two genuine triangulations (section 4). The right target is the uniform statement T3* (section 5), which covers Case I and II together; it is [data] 32 of 32, [open] in general. (O) is not needed for anything proved here; it is **not** a consequence of rigidity (fails on 7 of 75 rigid discs at n=17), section 6. |
| 3. Realisability of Case I x Case I | **Realised.** Order 23, discs 2 and 3 of `res_23.txt`: sphere triangulations, min degree 5, **no separating triangle** (so 4-connected), rigid, triply locked, both neighbours Case I; (N) still holds on them, both neighbours separable. No simple planarity or degree argument excludes the configuration. |

## 1. The D-free Kempe class, defined

Take a rigid triply locked c and c' = nu_gamma c (the case c'' is the mirror image). The ring word of c' is D alpha gamma beta gamma on u0..u4, apex u0, colour D. Call D' the colour class of u0 in c': V_D' = (V_D minus X) union Y (notation of MathNAttack). Define

* H = T - x - V_D' (the induced graph on the other three classes),
* Cl(c') = the set of proper 4-colourings of T - x reachable from c' by swapping single components of the three pair subgraphs [p,q] of T - x with p, q different from the colour D of u0, taken up to renaming of the three colours other than D. Nodes: canonical colourings; edges: one swap.

Equivalently Cl(c') is the 3-colour Kempe class of the induced 3-colouring of H, and it is the part of the G-class of c' at the fan u0 (G = T - x u0, x coloured D) that never touches V_D'. A member is *good* if it is 3-coloured on the ring or some chain {D,k} at u0 is broken (then one more G-swap separates). By Lemma D, "the chain {D,k} is broken" is a statement about the complementary pair of {D,k}, which is a pair of colours different from D, so goodness is a property of the 3-colouring of H only.

## 2. What is forced [hand]

**F1 (invariants).** For every member of Cl(c'): V_D' is the same set, the colours of the ring vertices of V_D' are unchanged (only u0), so n_D', r_D', exc_D' are constant. By I2, kappa_D' = (n-1) + r_D' - 3 n_D' - exc_D' is constant, and by I1 the sum over the three D-free pairs of delta = comps - cyc equals 8 - kappa_D', also constant. With Theorem G (MathNPinchT3; in the data tau = -1, kappa_D' = 3) the value is **5** for every member. [The invariance is unconditional; the value 5 uses the type II form, which is proved only up to tau = -1.]

**F2 (degrees).** Swapping a component of a pair with k components gives k different colourings up to renaming if k >= 3, one if k = 2 (swapping either component gives the same state up to the global transposition), none if k = 1. If the three D-free pair graphs of a member are forests, the component counts sum to 5, hence are (1,2,2) (degree 2) or (1,1,3) (degree 3). Cycles raise the counts: comps = delta + cyc. So a member of degree > 2 has a cycle in a D-free pair or a pair with 3 or more components.

**Prop R (regions).** Call an *H-triangle* a face of T with no vertex in V_D' union {x}, a *region* a class of H-triangles under sharing an edge, a *loose* vertex or edge one lying in no H-triangle. Let K be a component of a D-free pair [p,q] of any member, R a region. Then either all p- and q-coloured vertices of R lie in K or none do. Consequently the swap of K acts on R as the global transposition (p q) of its colours, and the colouring of R is determined by the colours of one triangle (S3-torsor).

*Proof.* An H-triangle has one vertex of each of the three colours. Its p-vertex and q-vertex are adjacent, hence in the same component of [p,q]; so a triangle with one vertex in K has all its p/q vertices in K. Two triangles sharing an edge share two vertices of different colours, at least one of which is coloured p or q; so if all p/q vertices of one triangle are in K, the shared one is, and the other triangle has a vertex in K. Connectivity of the region gives the claim. For the last sentence: the third vertex of an adjacent triangle is forced. QED

**Consequences [hand].** (i) The region decomposition depends only on (T, V_D'), not on the 3-colouring, so it is constant on the class. (ii) Cl(c') is the set of reachable assignments (permutation of each region, colours of loose vertices), at most 6^(r-1) times loose choices; the coupling through shared vertices and loose edges is what makes the actual classes tiny. (iii) The number of H-triangles is t = 2n - 7 - sum over V_D' of deg_T. Proof: each face has at most one vertex of the independent set V_D'; faces at x number 5, faces at u0 number deg u0, and 2 faces contain both x and u0 (u0 is the only V_D' vertex adjacent to x); so the faces touching V_D' union {x} number 5 + sum deg - 2, and t = (2n-4) - 3 - sum deg. With exc_D' = n - 3 - 3 n_D' (type II form, tau = -1) this is **t = n - 4 - 2 n_D'**. [data] Prop R and (iii) hold in all 150 classes of the 75 rigid discs at n = 17 (script `nprove_regions.py`: PropR ok 150 of 150, including the locked ones).

So H is "mostly holes": at n = 17 only 5 triangles for 12 vertices.

## 3. The 10-node class: why identical in the 8 cases, and is it forced?

**[data] n = 17, the 4 triply locked states (x2 mirror = 8 cases).** Skeleton of H (`nprove_skeleton.py`): n_D' = 4, t = 5, 4 regions of vertex sizes (3,3,3,4) (three single triangles, one pair of triangles sharing an edge), a single vertex shared by two regions, 5 loose edges, 12 vertices, 19 edges. The same skeleton (up to mirror) in c' and c'' of both discs. The class: 10 nodes, 11 edges, two hexagons sharing an edge, degrees (2^8, 3^2); the three-component members are exactly the two endpoints of the shared edge, each with a cycle in a D-free pair (comps (2,2,2), delta sum 5 by F1; `nprove_members.py`: members 3 and 6 for disc 0 c'), every other member has comps (1,2,2); first good member at distance 3 in all 8 cases, all good members in the second hexagon.

So the identical class in the 8 cases is explained by the identical skeleton; the skeleton in turn is a [data] fact about the two discs (at n = 17, n_D' = 4 and t = 5 are forced by F1, F2, (iii), but the arrangement of 5 triangles into regions (3,3,3,4) is observed). The 8 cases are really 2 discs times {c', c''}, up to mirror: 4 independent cases, not 8.

**It is not forced by rigidity.** [data, order <= 17] Over all 75 rigid discs at n = 17 (150 classes) the D-free class has **9 isomorphism types**: sizes 1 (40 cases), 2 (26), 3 (24), 4 (22+2), 6 (18, a pure hexagon with **no good member at all**), 7 (4), 8 (6), 10 (8). The 10-node class occurs also in 4 rigid but not triply locked cases. So the shape is neither a consequence of rigidity nor, evidently, of the lock alone.

**It is not forced by the triple lock.** [data, the 14 given order-23 lines] The same class has 6 shapes (`nprove_dfree17.py`): 10 nodes/11 edges, 12/14, 20/37, 18/31, 18/29 (twice, different degree sequences). Math's earlier statement that the 10-node class is not universal beyond 17 is confirmed with independent code. In all 28 order-23 classes the first good member is at distance exactly 3, as at n = 17 (32 of 32 over both orders).

**Hexagon mechanism [hand, partly].** On a member with comps (1,2,2) and forests, F2 gives degree 2 and the walk is deterministic, so a maximal run of such members is a path or a cycle; the six-cycles are S3 orbits (two non-commuting transpositions, Prop R: regions carry S3). The fan classes of c itself (alpha-free at u1, beta-free at u3, gamma-free at u4) are hexagons of size 6 at n = 17 and at n = 23 ([data], `recheck.py` output). Two facts are open: (a) why a pure hexagon of c' (no free-pair cycle) cannot occur once c is locked at all three fans (it occurs for 18 rigid but not triply locked classes at n = 17, so the other two fan locks must be used); (b) why some member of Cl(c') has a free-pair cycle (the branch point). By Lemma DI, cyc[D,k] = comps[a,b] - m_ab for the complementary free pair {a,b}, so a cycle in a D-pair of c' (type II) is the same datum as an extra ring-free free-pair component; moving it into a free pair is exactly what the branching members do, but I found no argument that the class must contain one.

## 4. Task 2/3: Case I x Case I is realised

[data, own code `nprove_verify23.py`, reproducing Math's table exactly] Discs 2 and 3 of `res_23.txt`: sizes (5,6,5,6) and (5,6,6,5); (|K2|,|K0|) = (4,4) in both; c' and c'' both Case I. Certificates computed from the edge lists: every vertex link is one cycle, m = 3n - 6, minimum degree 5, **zero separating triangles** (3-cliques minus faces), proper colouring, comps (1,2,2,1,1,1), fan classes of u1, u3, u4 of size 6 (not separating), and `recheck.py` prints `N HOLDS` (class sizes 15 and 20 for disc 2, 15 and 15 for disc 3). These are legal 4-connected minimum-degree-5 triangulations of order 23 realising the abstract configuration.

Hence **no planarity/degree argument can exclude both-Case-I**, and the conjecture "exactly/at least one of c', c'' is Case II" (MathNPinchT3 section 7) is false (Math's note already says so; this is an independent re-derivation of the certificate). Pattern in the data: the Case I neighbours have (|Q|,|E|,|R|) in {(4,6,6),(4,7,9),(5,9,7),(6,9,8),(7,9,9)} and the Case II ones have |E| <= 7 and |R| arbitrary; no size or pinch statistic separates them (Math reports the same for X, Y, tau, (O)). I propose no classification.

## 5. The statement that should be attacked: T3* (uniform)

In Case II the third swap is "the [beta,gamma]-component of u4" and in Case I it is "the [beta,gamma]-component through u2, u4"; but u4 lies in that component in both cases. So both cases are the same operation:

> **T3\*** (c' locked at the unlock level). Let c1 = swap of the [alpha,gamma']-component of u4 in c'; c2 = swap of the [alpha,beta]-component of u4 in c1 (it contains u3 because u3u4 is an edge); c3 = swap of the [beta,gamma]-component of u4 in c2. Then c3 is good (3-coloured ring in Case II; chain {D,beta} broken in Case I, equivalently u1 ~ u3 or u4 in [alpha,gamma]_3, Math's (G*)).

Reading: c3 is c' after three successive Kempe chains **rooted at the single vertex u4** along the colour pair sequence (alpha gamma), (alpha beta), (beta gamma): u4 is walked gamma -> alpha -> beta -> gamma. [data] T3* holds in 32 of 32 neighbours (`nprove_t3star.py`: 4 at n = 17 up to mirror, 28 at n = 23), ring colours 3 (Case II) or 4 with broken chain (Case I). T3* implies (N) for c' alone, with no use of c''. Whether T3* follows from the hypothesis "all members of Cl(c') are locked" cannot be settled by token counting (Math's closed locked orbit). What my region theorem adds is that the statement lives on the skeleton of H with t = n - 4 - 2 n_D' triangles; for the locked data t is 5 (n = 17), 9 or 7 (n = 23), i.e. the problem is about a very sparse 3-coloured planar graph, but I did not find a mechanism forcing a good member.

**Dead ends tried (so they are not repeated).**
1. Using chirality: in a 3-coloured triangulated region the signs of adjacent triangles alternate (mirror across an edge), so the orientation field is fixed up to a global flip per region and the Kempe swap flips whole regions; this is exactly Prop R, nothing more. It gives no inequality.
2. Planarity of the lens/fill and of Z13, Z14: the Case I x Case I discs have the same pinch, Lambda = a rhombus, X cap X0 empty, tau = -1 as the Case II ones (Math), and the mirror symmetry argument (c' <-> c'') cannot separate a symmetric hypothesis from itself.
3. Counting (I1, I2, Lemma DI, Lemma M): closed locked orbit c1 -> c2 -> c3 -> c4 ~ c1 (MathNPinchT3 5.4) and F1 above (the free-pair delta sum is constant 5) do not exclude a pure hexagon of c' (which does occur at n = 17 for non-triply-locked rigid states).

## 6. Where (O) is needed; can it be derived?

* (O) is used only in Theorem P (the pinch: a Y-hit of P14 gives a Y0-hit of P13 between the same shared alpha-vertices). The hand theorem "(N) holds unless both c', c'' are Case I" (Case II is an explicit three-swap sequence) and everything in sections 1-5 above do not use (O).
* [data] (O) holds on 14 of 14 order-23 locked discs, on 74 of 74 rigid discs at n = 18 (none triply locked), but on only **68 of 75** rigid discs at n = 17 (`nprove_O.py`); the 2 triply locked ones are among the 68. So (O) does not follow from rigidity (first-order lock, forests, Jordan, counting). If it is derivable at all it needs the full lock at some fan; I have no derivation. [lead] the bipartite plane graph [alpha,beta] union [alpha,gamma] (alpha against beta and gamma, n_alpha faces of length >= 4, each beta-gamma edge a chord of a quadrilateral face) is the natural arena for an order argument; not pursued.

## 7. Proved vs observed on the four rigid states of 17:1

Proved [hand]: F1, F2, Prop R, the triangle count t, the reduction of the third swap to the single operation T3*. Observed only: the skeleton (4 regions 3,3,3,4), the 10-node class, hexagon A pure, distance 3 to the first good member, T3* (32/32), the (O) pattern, Case I x II mix. Not proved: (N); T3*; the type II form (tau = -1) behind the value 5 and t = n - 4 - 2 n_D'; (O); the existence of a branching (free-pair-cycle) member; the claim that every locked class has a good member at distance 3.
