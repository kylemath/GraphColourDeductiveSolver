# Math attack on statement (N)

Math-team research worker, 5 October 2026. Long-horizon attack on statement (N) of `creative-intel-2026-10-05/d1-hand-attack.md` §7. Exploratory, undeclared; no declared experiment was run, no one else's file was edited, nothing was committed. Labels as in `START-HERE.md` §5: [hand], [computed], [open]. Status words stay with the Navigator.

**(N).** In a rigid triply locked state c of a minimum-degree-5 triangulation T, ν_γ c is separable for the fan at u0, or ν_β c is separable for the fan at u2.

Notation is that of `d1-hand-attack.md`: ring word D α D β γ on u0..u4; V_i, n_i, exc_i; pair subgraph [p,q] of T−x; K2 = component of u2 in [D,γ], K0 = component of u0 in [D,β]; c′ = ν_γ c (swap K2), c″ = ν_β c (swap K0); X = K2∩V_D, Y = K2∩V_γ, X0 = K0∩V_D, Y0 = K0∩V_β. In c′ the colours D, γ are exchanged on K2, so D′ = (V_D∖X)∪Y and γ′ = (V_γ∖Y)∪X.

## 0. Result

| Task | Outcome |
|---|---|
| (a) proof by a second/third-order Jordan or counting lemma | **No proof found.** New exact first-order information (§2): a duality lemma, an exact first-order criterion for the unlock of c′ and c″, and a necessary condition for (N) to fail in terms of the unique tree paths P13, P14. The counting identities are consistent with failure of (N) (§4). |
| (b) both neighbours cannot be locked | **No contradiction found** from I1/I2 plus Jordan. A conditional degree-excess relation (§2.5) and the computed S3-structure of the locked classes (§3) are the only new constraints. |
| (c) why a proof must be global | Partial. (N) alone is not shown to imply 4CT; D1 does. Weaker provable local statements are listed in §5. |
| (d) structural counterexample search | **Not done by construction** (needs a disc generator, §6). Lemma tests on 17:0 and 17:1 only (plantri available), §3. |

The one thing that is new and complete is §2.1–2.3: a proof that (N) holds unless **both** P14 meets K2∩V_γ **and** P13 meets K0∩V_β, and that this is the only way a first-order escape can fail. Everything else is bookkeeping that shows where a proof would have to go.

## 1. What was read and what is assumed

START-HERE, `d1-hand-attack.md`, `tilley-separability.md`, `lock-counting.md`, `MathCreativeCatchUpReview.md`. Legality of the fans at u0 and u2 is assumed as in the source (automatic if T is 4-connected). "Rigid" means all three chains full, equivalently (Prop 3 there) all six pair subgraphs of T−x are forests with component vector (1,2,2,1,1,1) for (Dα, Dβ, Dγ, αβ, αγ, βγ). In a rigid state [α,β] and [α,γ] are spanning trees on V_α∪V_β, V_α∪V_γ, so the paths P13 (u1 to u3 in [α,β]) and P14 (u1 to u4 in [α,γ]) exist and are **unique** [hand].

## 2. Hand results

### 2.1 Lemma D (duality for a pair subgraph) [hand]

Let c be a proper 4-colouring of T−x, x of degree 5 with ring u0..u4, and let a, b be ring vertices coloured p, q respectively, p≠q. Let {r,s} be the other two colours. Then a and b lie in different components of [p,q] (in T−x) **iff** there are ring vertices s′, t′ with colours in {r,s}, joined by a path R in [r,s], such that a and b lie in different arcs of the ring minus {s′,t′}.

*Proof.* (⇐) Γ = x s′ R t′ x is a simple closed curve; a, b are not on Γ (their colours differ from those of R, and they are not x), and the edges xa, xb leave x on opposite sides of Γ. A [p,q]-path from a to b avoids the vertices of Γ and hence cannot cross it. (⇒) Let K be the [p,q]-component of a, U the union of the closed triangular faces of T having a vertex in K. U is connected, a is interior to U, and b ∉ U (a face containing b and a vertex of K would put an edge between b and K, forcing b ∈ K). An edge of ∂U lies in a face f ∈ U and a face f′ ∉ U; if one endpoint were in K, f′ would contain it, so both endpoints are outside K. Take f = uvw with w ∈ K: neither u nor v is coloured in {p,q} unless it is x, because it is adjacent to w. So every edge of ∂U is an [r,s]-edge or an edge xv with v a ring vertex of colour in {r,s}. a and b lie in different faces of the plane graph ∂U, so some simple cycle C ⊂ ∂U separates them (a minimal cut of the dual). If C avoids x, then x, and with it every ring vertex not on C, lies on one side, so C does not separate a from b. Hence C passes through x, uses two edges xs′, xt′, and the rest is an [r,s]-path R. The separation of a, b by C is the separation of the ring arcs. ∎

[computed] Lemma D was tested on all colourings of T−x at every degree-5 vertex, all pairs of ring vertices with different colours: `plantri -m5` orders 12 (1 graph), 14, 15, 16 (3), 17 (2: 17:0, 17:1), 18 (12); 0 mismatches over 12 810 (order 17) and 132 860 (order 18) tests, with 22 024 disconnected cases at order 18. Script `dual.py`. Order 18 is a spent order (START-HERE §5) and was used only as a lemma test.

### 2.2 First-order criterion for the unlock of c′ and c″ [hand]

By Prop 1 of `d1-hand-attack.md`, at the apex u0 of c′ the chains {D,α}, {D,γ} are automatic (u0 is adjacent to u1 and u4) and only {D,β} can be broken: it is broken iff u3 and u0 lie in different components of [β,D′]. The ring word of c′ is D α γ β γ. The complementary pair of {β,D′} is {α,γ′}; its ring vertices are u1 (α), u2 (γ), u4 (γ). The ring pairs that separate u3 from u0 are {u1,u4} and {u2,u4}. By Lemma D:

> **Cor 1.** c′ is first-order unlocked at u0 (and then separable for the fan at u0 by one G-swap) **iff** u4 ~ u1 or u4 ~ u2 in [α,γ′].

Symmetrically (c″ has ring word β α D β γ, apex u2, only {D,γ} can break, complement {α,β″}, ring vertices u0 (β), u1 (α), u3 (β), separating pairs {u0,u3}, {u1,u3}):

> **Cor 1′.** c″ is first-order unlocked at u2 iff u1 ~ u3 or u0 ~ u3 in [α,β″].

### 2.3 Necessary condition for (N) to fail [hand]

[α,γ′] ⊇ [α,γ] minus Y. If P14 contains no vertex of Y then P14 is still a path of [α,γ′] from u1 to u4, so by Cor 1 c′ is separable at u0. Likewise, if P13 contains no vertex of Y0 = K0∩V_β then u1 ~ u3 in [α,β″] and c″ is separable at u2 (Cor 1′). Hence:

> **Prop N1.** (N) holds unless **both** P14 ∩ Y ≠ ∅ **and** P13 ∩ Y0 ≠ ∅. A counterexample to (N) also needs u4 ≁ u2 in [α,γ′] and u0 ≁ u3 in [α,β″], and all deeper locks.

This is a clean, checkable necessary condition. [computed] The necessary condition holds in all four rigid states on 17:1 (as it must, since both neighbours stay first-order locked): the hit is a single γ-vertex of P14 in K2 (vertices 2, 10, 11, 0 for x=5 states 0,1 and x=15 states 0,1) and a single β-vertex of P13 in K0 (9, 11, 4, 2).

In the data the picture is a pinch: P13 and P14 share the α-vertices a, a′ (e.g. x=5: 8 and 3) and between them P14 makes an excursion 8–2–3 through the γ-vertex of K2 while P13 makes an excursion 8–9–3 through the β-vertex of K0; the two excursions with a, a′ form a 4-cycle α β α γ. I could not turn this into a proof that the pinch is forced or impossible: Jordan with C13 = x u1 P13 u3 x puts K2 strictly inside C13 and the γ-hit inside it, but [D,γ] and [α,γ] share their γ-vertices, so C14 does not obstruct K2.

### 2.4 The V_α-fixed sub-class is 2-regular-like [hand]

Let Λ(c) be the set of colourings reachable from c by swapping components of the pairs **not containing α** in T−x. For every member V_α is the same set and r_α = 1, so exc_α and n_α are unchanged, and by I2 κ_α = (n−1)+1−3n_α−exc_α is unchanged (= 3 for the rigid c). Hence for every member

  Σ over the three α-free pairs of (comps − cyc) = 8 − κ_α = 5.

If the three α-free pair subgraphs of a member are forests, their component counts sum to 5 and are (2,2,1) or (3,1,1) in some order. Swapping one component of a pair with k components gives, up to renaming of colours, k distinct neighbours if k ≥ 3, one if k = 2, none if k = 1. So the member has 2 or 3 neighbours in Λ, and exactly 2 in the (2,2,1) case. The same holds for each of the three fans' classes with α replaced by the apex colour, whenever the class is generated by pair swaps avoiding that colour (chain swaps at full chains are renamings). This is what makes the fan classes of rigid states small cycles (§3).

### 2.5 A degree-excess relation, conditional on the type II form of c′ [hand, conditional]

The pair data of the non-rigid locked members (`d1-hand-attack.md` §8) read, in the roles D′ = γ′ (doubled), M′ = β, L′ = D, R′ = α of c′: comps (2,2,2,1,1,1) for (D′L′, D′M′, D′R′, L′M′, M′R′, L′R′) and exactly one cycle, in [L′,R′] = [D,α]. Call this **type II form**. It is not proved for c′; in the data it holds (§3). If c′ has it, I1 and I2 give κ′_{γ′}=6, κ′_β=4, κ′_D=3, κ′_α=3 and

  exc′_{γ′} = n−5−3n′_{γ′},  exc′_D = n−3−3n′_D,

with n′_{γ′} = n_γ − |Y| + |X| and exc′_{γ′} = exc_γ − exc(Y) + exc(X). Combining with exc_γ = n−4−3n_γ for the rigid c:

  **exc(Y) − exc(X) = 1 − 3(|Y| − |X|)**, where exc(S) = Σ_{v∈S}(deg_T v − 5).

Both cases d = |Y|−|X| ≤ 0 (exc(Y) ≥ 1) and d ≥ 1 (exc(X) ≥ 3d−1 ≥ 2) give a vertex of degree ≥ 6 in K2. The same holds for K0 and c″ (exc(Y0) − exc(X0) = 1 − 3(|Y0|−|X0|)). [computed] all four rigid states satisfy this relation exactly, with |X|=|Y| and the single excess vertex in Y (resp. Y0). So **if both neighbours were locked and of type II, K2 and K0 would each have to carry a vertex of degree ≥ 6**; at n=17 the excess budget (1,2,1,1) is then fully used (γ and β each have excess 1, all in Y and Y0). This is a constraint, not a contradiction: for n ≥ 19 the budget has slack.

## 3. Computed observations (17:0, 17:1 only; exploratory, post hoc)

Scripts are in `docs/working/MathNAttack-scripts/` (`nlab.py` library and enumerator; others import it). plantri at the path recorded in `lock-counting.md` §2. Only the two graphs 17:0, 17:1 were used, plus Lemma D tests.

1. **Rigid triply locked states.** On 17:1 only: x=5 (2 states) and x=15 (2 states), matching the 4 of `d1-hand-attack.md`. None on 17:0. All have ring degrees (5,6,5,5,5), sizes (4,4,4,4), (|K2|,|K0|) ∈ {(2,4),(4,2)}. Both neighbours of every one are separable (8 of 8), as in the source. `nlab.py`.
2. **Hexagon.** For the rigid state at x=5, each of the three fan classes in G has exactly 6 canonical colourings and its swap graph is a 6-cycle (nodes 0..5; rigid states A=0 and B=5 antipodal, the other four non-rigid; edge swap sizes 4, 2/6, 2/6, 4, 2/6, 2/6). The two rigid states of x=5 lie in the same fan-u1 class. This is the 2-regular behaviour predicted by §2.4 with all pairs forests; the cycle has the shape of the Cayley graph of S3 for two transpositions. `cg.py`, `cls.py`.
3. **Structure of c′, c″.** Component and cyclomatic data of c′ (and c″) are type II form in all 4 states: (Dβ,βγ,αβ,Dγ,Dα,αγ) = (1,2,1,2,(1,1),2) for c′. `cp.py`.
4. **Excess relation of §2.5** holds in all 8 neighbour cases. `exc.py`.
5. **First-order locks.** In all 8 neighbours the unlocking fan is first-order locked (no u4~u1, u4~u2 path); the unlock needs the 4 G_0-swaps found by BFS. Every shortest unlock sequence has the **same shape in all four states, for both neighbours**: swap 1 is the Jordan-split component of [α,γ′] (the one containing u4, equivalently its complement containing u1, u2; for c″ the split component of [α,β″]); swap 2 is a component of [β,γ′] (sizes 4 and 2/6, containing u1 or u3,u4); swap 3 is a [D,β]- or [β,α]-component (sizes 2,3,6), after which a chain is broken; swap 4 separates. After swap 1 the apex u0 has become the *middle* singleton of the ring word. 16 shortest paths per neighbour, `up2.py`.
6. **The two hit conditions of §2.3** hold in all 4 states (hit vertices listed there).
7. **Not in the data:** a state where c′ and c″ are both locked.

## 4. Why I1/I2, Jordan and counting do not close (N) [hand]

For c′ = ν_γ c the following are all consistent with c′ being triply locked: Prop 6 (a cycle in [α,γ′] or [α,D′]); Prop 2 applied to c′, which only forces u4 ≁ u1, u2 in [α,γ′] and u2 ≁ u4, u0 in [D′,γ′]; the invariants κ′_α = 3, δ′_{αβ} = 1, δ′_{Dγ} = 2; and the excess relation of §2.5, which at n ≥ 19 has slack. The identities give only the two sums δ′_{αD′}+δ′_{αγ′} = 2 and δ′_{βD′}+δ′_{βγ′} = 3, never the individual counts, so the type II form cannot be derived from counting alone; it needs geometry of how a swap of K2 changes the trees [α,D] and [α,γ] (c′ has [α,D′] = ([α,D] minus X) ∪ ([α,γ] restricted to α∪Y), a forest plus new edges). No lower bound on any δ′ appears. The unlock lies at Kempe distance 4 in G_0 (§3 item 5), so a proof by Jordan has to see 3 preparatory swaps; the pattern of §3 item 5 is the natural target:

> **T3 (target third-order statement) [open].** In a rigid triply locked state, in the G_0-class of c′ (x coloured D, apex u0), there is a sequence of three swaps, namely the Jordan-split [α,γ′]-component, a split [β,γ′]-component, and one more, ending in a state with u3 ≁ u0 in [β,D].

I could not prove T3, nor find a reason why the first two swaps are always available beyond Prop 2 (which gives the split) and the 2-regularity of §2.4 (which says the class has 2 such moves, namely the two split pairs). The third swap exists in the data because the [β,D] or [β,α] pair of the state reached has a component that contains u0 and u4 (or is ring-free) and whose swap breaks u3~u0; I have no general reason for it.

## 5. What is and is not local

**Provable locally [hand]:**
- Prop N1: first-order escape iff P14 misses K2∩V_γ (sufficient), plus the exact criterion of Cor 1/1′.
- §2.4: the V_α-fixed class of a rigid state has at most 3 and, in the forest (2,2,1) case, exactly 2 neighbours per member, so it is a union of cycles.
- §2.5: conditional degree-≥6 requirement for K2 and K0.
- (N) is vacuous for n = 12, 14, 15 (no rigid triply locked state, Prop 3 table).

**Why a proof needs global input.** The reduction of D1 to (N) is only for the rigid case; D1 for all minimum-degree-5 T implies 4CT (`d1-hand-attack.md` §9). It does **not** follow that (N) alone implies 4CT: the hypothetical minimum counterexample need not contain a rigid triply locked state, because rigidity forces every colouring in the class to have all four classes ≤ (n−4)/3 (resp. (n−3)/3 for α), which has slack for n ≥ 19 but is a strong condition on the colouring. So (N) is not *known* to be equivalent to anything hard; I know no hand proof and no reason it is false. The reason it resists is that the swaps in the unlock path (sizes 2, 4, 6 out of 8-vertex pair subgraphs) are components of spanning trees of the whole colour classes: any argument must control entire pair subgraphs, which is what the "locked" hypothesis grants only at first order (the chains) and not at the depth the unlock needs. This is an explanation of the obstacle, not a theorem.

**Weaker statements still provable or plausible:**
1. (N) restricted to states where P14 misses K2∩V_γ or P13 misses K0∩V_β: proved (Prop N1).
2. Both neighbours unlocking at first order is not needed by any data; first-order locks of c′, c″ hold in all computed cases [computed]; a hand proof of "c′ is first-order locked at u0 in every rigid state" would be worthwhile only if it fails, since a failure gives (N).
3. A conditional theorem: if the type II form holds for c′ and c″ and both are locked, then K2 and K0 each have a vertex of degree ≥ 6, and for n = 17 these are exactly the unique degree-6 vertices of V_γ and V_β. This is consistent with the data, so it is no refutation.

## 6. What was not done

- **No counterexample search by construction.** A direct search needs a generator of triangulated discs with ring word D α D β γ and the six-forest structure, grown from the ring, with the size caps (n_i ≤ (n−4)/3, n_α ≤ (n−3)/3) as pruning; n = 19, 20 are the first orders with slack. A hand design: grow T−x by adding a vertex in the boundary face, with a union-find per colour pair rejecting any cycle; I did not implement it. The census orders 19–24 were not run.
- No attempt to prove the type II form of c′ in general (§4) or the pinch structure of §2.3.
- Orders 17 only for the computed items, and the item "all 8 neighbours unlock" is the source's data, rechecked here for the four rigid states.

## 7. Next steps worth Math's time

1. Prove or refute **the pinch**: in a rigid triply locked state the unique paths P13, P14 share α-vertices a, a′ with excursions through K0 and K2. A proof that it is forced would reduce failure of (N) to a statement about a 4-cycle α β α γ and its interior.
2. Prove the **type II form** of c′ (one cycle in [D,α], comps (2,2,2,1,1,1)) from the tree description of §2.5; with it §2.5 is unconditional.
3. T3.
4. Write the generator of §6 and test (N) at n = 19–22 on rigid states constructed directly; this does not need a census.

Files: this page; `docs/working/MathNAttack-scripts/` (nlab.py, cp.py, cls.py, cg.py, up.py, up2.py, hexa.py, reg.py, dual.py, exc.py). Nothing staged or committed.
