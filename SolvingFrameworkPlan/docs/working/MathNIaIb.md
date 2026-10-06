# Math attack on (N), part 5: the Ia/Ib split of Case I

Math-team research worker, 6 October 2026. Continuation of `MathNGstar.md`. Exploratory, undeclared; no declared experiment, nothing of others' edited, nothing staged or committed. Labels: [hand], [computed] (exploratory, post hoc, existing disc data only), [open]. Status words stay with the Navigator. Scratch scripts (session scratchpad `ni/`): `chain.py` (D'-free class BFS with pair data), `c2an.py`, `allib.py` (Case II/Ia/Ib over every rigid disc of `out_17..20.txt`), `ident.py`, `zcyc.py`, `walk.py`; they import `MathNCaseI-scripts/tn_lib.py`. Data: `res_23.txt` (14 locked discs) and `res2_24_p0..p3.txt` (26 locked discs); 40 discs, 80 neighbours.

Notation: c' = nu_gamma c, c1, c2, c3 = the swaps Q4, E34, R of `MathNPinchT3.md` 5.2/5.3 (mirror for c''). Long Table's Ia = Case I with the chain {D,beta} broken at c3 (= (G*) holds); Ib = Case I with c3 intact (= (G*) fails). Cl(c') = D'-free Kempe class; "good" = broken apex chain or 3-coloured ring.

## 0. Result

| Question | Outcome |
|---|---|
| Long Table: "Ib never occurs at a triply locked state" | **False at N = 24. [computed]** 4 of the 52 neighbours at N = 24 are Ib (`res2_24_p0` line 9 c'', `p1` line 3 c'', `p3` lines 4, 5 c'), in 4 distinct locked discs; the pairs (c',c'') are (Ia,Ib), (II,Ib), (Ib,Ia), (Ib,II). Their claim was an n <= 23 artefact (same as G* in `MathNGstar.md`). Over the 40 discs: II 50, Ia 26, Ib 4. **No disc has (Ib,Ib).** |
| Long Table: "T3* holds in 32 of 32" and is the uniform target | **T3* is false at N = 24.** T3* = "c3 is good"; it is exactly (G*) in Case I. It fails in the same 4 Ib neighbours (all four are separable by another route, Section 3). |
| Long Table: "a counterexample to (N) needs both neighbours Ib" | Correct as a necessary condition **only for the A-walk** (II and Ia are proved separable). It is not a classification of counterexamples: Ib is *not* an obstruction class, since 4 of 4 Ib neighbours at locked states are separable at D'-free distance 3. The true condition is "Cl(c') has no good member, for c' and c''". |
| Long Table: blocking pattern (L1) "Ib or locked c' never occurs when c is locked at u4" | The "Ib" half is refuted (the two `p3` discs above are LLL with Ib c'). The "locked" half is vacuously true at N = 23, 24 (all 80 neighbours of locked states are separable); as stated it is T3 for every neighbour, which is strictly stronger than (N). |
| Is (N) proved in a sub-case? | II: yes (Math, `MathNPinchT3.md` 5.2, [hand]). Ia: yes in the sense that c3 has a broken chain, hence separable after one more G_0 swap (Math, [hand]). **Ib: no.** |
| Exact obstruction in Ib | Section 2-3: (i) [hand] Case I with [beta,gamma]_2 connected forces c3 = c2 up to renaming, hence Ib; (ii) [hand] then c2 necessarily has a ring-free component in [alpha,gamma]_2 or [alpha,beta]_2, i.e. a branching move not on the A-walk; (iii) [open] that this extra move is good. In the data it is, 4 of 4. |
| Is Ib forced to be "Case II-like"? | Not proved. What is proved is the structural reason Ib is a different phenomenon from Ia: in Ib the A-walk is not walking at step 3 at all (Section 2). |

## 1. Line-by-line check of Long Table's claims

[computed unless stated]. Reproduced: Case I/II table at N = 23 (II,II) 8, mixed 4, (I,I) 2, both Ia; class sizes; "Ib over rigid discs about 700 neighbours" (not rechecked); Case I x Case I realised (Math's own data, so same source). Prop R (region theorem) [hand]: checked, the proof is right (an H-triangle's p- and q-vertices are adjacent; adjacent triangles share an edge with at least one p/q vertex). Triangle count t = 2n - 7 - sum deg(V_D') [hand]: checked (faces at x: 5; two of them contain u0; V_D' independent, and the only member adjacent to x is u0), so t = n - 4 - 2 n_D' under type II is right. Wrong or overstated: the four items in the table of Section 0. One more point: Long Table's Ib/Ia definition follows only the single A-walk; as they say, a counterexample "could lock the D-free class differently". That caveat is the whole story at N = 24.

## 2. Hand structure of Case I at c2 [hand, conditional where stated]

Standing: c' locked, Case I (m_beta,gamma(c2) = 1, m_D,alpha(c2) = 2, m_alpha,beta(c2) = 2, m_alpha,gamma(c2) = 1; `MathNPinchT3.md` 5.2). Lemma DI (dual identity): comps[r,s] = cyc[p,q] + m_rs for complementary pairs {r,s},{p,q}.

**(A) The two branches coincide through c2.** Assume the pair [alpha,gamma'] of c' has exactly two components and [alpha,beta] of c1 has exactly two (data: 80 of 80). Swapping both components of a pair is the global renaming of its two colours, so swapping the other component gives the same Cl-node. Hence Math's branch B1, B2 (`MathNGstar.md` 2) equals the A-steps Q4, E34 up to renaming, and "branch B" is nothing but "a third swap at c2 other than R". So (B3) says: **c2 has a good neighbour in Cl(c')**, and the A/B distinction is only which neighbour of c2.

**(B) The third A-step can be vacuous.** If [beta,gamma]_2 has one component then R is the whole pair graph, c3 is c2 with beta and gamma renamed globally, and since all chains of c2 hold at first order, c3 is not good. So **Case I and comps_beta,gamma(c2) = 1 imply Ib.** By DI, comps_beta,gamma(c2) = 1 iff cyc[D,alpha](c2) = 0. [computed] Conversely at the 30 Case I neighbours of locked states: Ia has comps_beta,gamma(c2) = 2 and cyc[D,alpha](c2) = 1 (26 of 26), Ib has comps_beta,gamma(c2) = 1 and cyc[D,alpha](c2) = 0 (4 of 4). So at locked states in the data, **Ia vs Ib is exactly "does c2 have a cycle in [D,alpha]"**. [open] why the data never show Ib with comps_beta,gamma(c2) = 2 at a locked state (such Ib neighbours do occur at rigid unlocked discs, e.g. n = 17: 9 states).

**(C) Cycle identity.** By F1 (Long Table; Math 2.4) the sum over the three D-free pairs of (comps - cyc) is 5 (this value uses the type II form tau = -1). With DI and the Case I m-values (2,1,1 for alpha-beta, alpha-gamma, beta-gamma, sum 4): 4 + cyc_D - cyc_free = 5, i.e.

  cyc[D,alpha] + cyc[D,beta] + cyc[D,gamma] = 1 + (cycles in the three D-free pairs) at c2. [hand, given tau = -1]

[computed] holds at all 30 Case I c2 (`ident.py`).

**(D) Consequence for Ib.** In Ib-with-(B) we have cyc[D,alpha] = 0, so cyc[D,beta] + cyc[D,gamma] >= 1 + cyc_free >= 1 by (C). By DI, comps_alpha,gamma(c2) = 1 + cyc[D,beta] and comps_alpha,beta(c2) = 2 + cyc[D,gamma]. So c2 has a **ring-free component** in [alpha,gamma]_2 or [alpha,beta]_2, hence a Cl-neighbour that is neither c1 nor c3 = c2. [hand] So in Ib (B) the class is **never** the closed A-orbit of `MathNPinchT3.md` 5.4: the closed locked orbit cannot occur at that step, because c2 has degree >= 2 outside the A-walk. This is a proved reason for the 4 unlocks, not a proof that they unlock: [open] the new neighbour (swap of the ring-free [alpha,gamma]_2 component, equivalently of the ring component u1,u2,u3 up to renaming: ring D alpha gamma alpha beta becomes D gamma alpha gamma beta) is good iff the chain {D,alpha} breaks there, i.e. iff u0 and u2 are separated in [D,alpha] of that colouring.

[computed] the four Ib c2 have free-pair data (comps,cyc) (alpha-beta, alpha-gamma, beta-gamma) = (2,0),(3,0),(1,1) (mirror: (3,0),(2,0),(1,1)), degree 4 in Cl; the good neighbours are the alpha-gamma (resp. alpha-beta) swaps of the ring component and of the ring-free component (`c2an.py`, `walk.py`).

## 3. Data summary [computed]

| | II | Ia | Ib |
|---|---|---|---|
| N = 23 (28 neighbours) | 20 | 8 | 0 |
| N = 24 (52 neighbours) | 30 | 18 | 4 |
| all 80 | 50 | 26 | 4 |

All 80 neighbours have a good member of Cl at distance exactly 3 (also N = 24, `chain.py`); c' always has free-pair data a permutation of (1,2,2) with no cycle (degree 2). The N = 24 classes have 8 to 20 members; several are pure 2-regular cycles (8 and 10 nodes) with good nodes at distance 3, 4, 4, 5, so the pure-cycle case does contain good nodes at locked states, and no locked class was found that is a pure hexagon with no good member (Long Table's open item (a); 0 of 80, consistent with their n = 17 data where the 18 pure hexagons without a good member are not triply locked).

Negative result [computed, `zcyc.py`]: the unique [D,alpha]-cycle Z of c' (a 6-cycle, disjoint from the ring in all 30 Case I cases) is met by both Q4 and E34 in every case, Ia and Ib alike, so "Z survives or is destroyed" is not the discriminator between Ia and Ib.

## 4. What is proved and what is not

Proved [hand]: (A), (B), (C) (given tau = -1, the type II form, itself conditional on the pinch work), (D). They isolate Ib as: the A-walk's third step is empty, the class must branch at c2, and the whole remaining content is a single token statement about the branching move (Section 2 (D)). Not proved: that the branching move is good; (B3); (N); T3. Refuted: Long Table's "no Ib at locked states" and "T3* is uniform and true". Not run: any generation beyond N = 24 (none allowed), any (Ib,Ib) search (none exists in the 26 locked discs).

Recommended next question [open]: show, using the locks of c at u3 and u4, that cyc[D,alpha](c2) = 0 forces the swap of the ring component of [alpha,gamma]_2 (or [alpha,beta]_2) to break the chain {D,alpha}; equivalently, since the closed A-orbit is excluded in Ib by (D), the exact missing statement is a Jordan-type fact about one [D,alpha] path u0 ~ u2 in the colouring after that swap.
