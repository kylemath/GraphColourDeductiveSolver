# Kempe classes at a pentagonal hole: a Lean-checked reduction of the Four Colour Theorem to D-resolvability in a reduced class, with partial results and refuted conjectures

*Track D draft, 7 October 2026. Not for circulation until Kyle approves. Open items are marked **TODO**. Claims that need checking are listed in `README.md` in this folder.*

**Labels.** Each claim carries one of these labels.

- **[formal]**: proved in Lean 4 with no `sorry`, no new `axiom` and no `native_decide`, depending only on `propext`, `Classical.choice` and `Quot.sound`. The Lean name and file are given. Every file is under `SolvingFrameworkPlan/docs/working/StudioMathLean/Mathlib/Combinatorics/SimpleGraph/PlaneMap/`. Below, `PlaneMap/X.lean` means that directory.
- **[hand]**: a written argument, reviewed (if at all) only by AI sessions.
- **[data]**: a computation. Only the graphs examined are covered.
- **[cited]**: from the published literature.
- **[refuted]**: a statement we conjectured and then disproved by an explicit, independently re-verified counterexample.

The Lean kernel certifies that each formal statement is proved. It does not certify that the statement means what our prose says. Only AI sessions have compared the prose with the Lean.

---

## Abstract

The Four Colour Theorem (4CT) is a theorem. Appel and Haken proved it [AH77], Robertson, Sanders, Seymour and Thomas gave a second proof [RSST97], and Gonthier checked that proof in Coq [Gon08]. **This paper does not give a new proof of the 4CT.** It records three things: a formal reduction, a framework of definitions, and a set of partial results and negative results.

**(1) A formal reduction.** We prove in Lean 4 that the 4CT, stated for the combinatorial spherical maps of our library, follows from the statement $R^\ast_{\rm frame}$. $R^\ast_{\rm frame}$ says: every connected spherical triangulation of minimum degree 5 with no separating triangle, and with no occurrence of the Birkhoff diamond or of the RSST configuration 2.122, has a degree-5 vertex $v$ such that every Kempe class of 4-colourings of $T-v$ contains a colouring whose link uses at most three colours. As far as we can tell, that vertex property is Tilley's *D-resolvability* [Til17]. Whether every degree-5 vertex is D-resolvable is his open problem, so $R^\ast_{\rm frame}$ is a restriction of that problem to a reduced class. The two exclusions are discharged by kernel-checked D-reducibility certificates. A compiled bridge turns the classical "appears" notion of a configuration into the ring-embedded occurrence used by the certificates, under one named hypothesis.

**(2) A framework.** At a degree-5 vertex (a *pentagonal hole*) we formalise Kempe classes, the two Kempe locks, doubly locked states, and a link-changing permutation $\pi$ of every Kempe class. Two counting identities follow:

- Theorem W, $3F-U=-5w$;
- the exact class identity $\Sigma\lambda=|DD|-2N_0-E_2-3\tau$.

The library's vertex property is equivalent to the absence of a $\pi$-orbit consisting only of doubly locked states.

**(3) Partial results, inside reducible territory.** We prove the *quarter floor* (at least a quarter of every Kempe class is filled) at holes whose five link vertices have degree 5 (Theorem F5). We prove D-resolvability at holes with four consecutive degree-5 link vertices (weak F6). **Every such hole contains a Birkhoff diamond.** So these results concern configurations that a minimal counterexample already avoids, and they do not advance the 4CT.

**(4) Negative results.** Several conjectures that held on every triangulation of order at most 27 fail on constructed 37-vertex triangulations. These are $A_{34}'$, W2, Lemma $S_\Gamma$ and statement (c). We record them as cautionary data.

---

## 1. Introduction

### 1.1 Background

Let $T$ be a plane triangulation and $v$ a vertex of degree 5. Kempe's 1879 argument [Kem79] tries to colour $T-v$ and then free a colour on the link of $v$ by Kempe changes. Heawood [Hea90] showed that the two simultaneous swaps can interfere. Every successful proof since then has avoided the degree-5 impasse: it uses an unavoidable set of reducible configurations instead [Bir13, AH77, RSST97, Gon08]. **[cited]**

Tilley [Til17] calls a vertex $v$ *D-resolvable* if every Kempe class of 4-colourings of $T-v$ contains a colouring in which the link of $v$ uses at most three colours. Such a colouring extends to $T$. He shows that a degree-5 vertex need not be D-reducible. He leaves open whether every degree-5 vertex of a planar triangulation is D-resolvable, and notes that a positive answer would imply the 4CT. **[cited]** Our library's predicate `PureClean T v` says that every proper colouring of $T-v$ reaches a filled link by finitely many whole-component Kempe swaps. As far as we can tell, it is Tilley's notion. **TODO:** check this against the full text of [Til17]. The project audit has read only the abstract.

### 1.2 What this paper contributes, and what it does not

**Contributions.**

1. A Lean 4 proof that a weak, class-restricted form of Tilley's conjecture implies the 4CT for the library's spherical maps (§3). The class excludes separating triangles, the Birkhoff diamond and RSST 2.122. The exclusions are discharged by compiled certificates, not assumed.
2. A formal framework for Kempe classes at a pentagonal hole (§4), with two exact counting identities (§5).
3. Two partial results, F5 and weak F6 (§6). Both are at holes that contain a Birkhoff diamond, so they are outside the class that matters.
4. A record of refuted conjectures and of the computations behind them (§§7–8).

**Non-contributions.**

- No new proof of the 4CT.
- No progress on any statement known to be of 4CT strength in the reduced class.
- $R^\ast_{\rm frame}$ is open. It is at least as hard as the cases of Tilley's problem it covers.

### 1.3 How the work was produced

The mathematics, the Lean code, the computations and this text were produced by AI agents (Claude models) under the direction of Kyle Mathewson. No human has refereed the hand arguments or compared the Lean statements with the prose. The project's companion paper (`SolvingFrameworkPlan/docs/reports/VHE-paper/main.tex`, §1) contains the full disclosure. **TODO:** port the disclosure wording once Kyle has approved it.

---

## 2. The formal model

All statements live in the PlaneMap library (snapshot `8299419`, Mathlib `300d0e5`, Lean `v4.35.0-rc3`). See `StudioMathStatements.md`, Part A1.

- **Maps.** `SphericalMap n` is a simple graph on `Fin n` with a rotation system. It also satisfies `Fills`: every mod-2 cycle is a sum of face boundaries. `Fills` is the only planarity assumption. We do not formalise the passage from a topological embedding to a `SphericalMap`.
- **Triangulations.** `Triangulated` means every face has length 3. `NoSep T` means every triangle of $T$ bounds a face.
- **Kempe semantics** (`VacancyShortFill`).
  - A *state* at hole $h$ is a colouring $c:\mathrm{Fin}\,n\to\mathrm{Fin}\,4$ that is proper on $T-h$ (`ProperOff`).
  - `KempeStep` swaps two colours on one entire component of their two-colour subgraph of $T-h$.
  - `Target` holds when some colour is missing on $N(h)$. We call such a state *filled*.
  - `PureFill G h c m` holds when some filled state is reached within $m$ steps.
- **The vertex property.** $\texttt{PureClean}\ T\ v:\iff \forall c,\ \texttt{ProperOff}\ T\ v\ c\to\exists m,\ \texttt{PureFill}\ T\ v\ c\ m$ (`PlaneMap/RStar.lean`).
- **Jordan facts are proved, not assumed.** `rotation_arc_separation`, `face_alternating_walks_meet` and `chains_noncrossing` (`RingJordan.lean`, `RingChains.lean`) are derived from `Fills`.

---

## 3. The reduction

### 3.1 Statement

Write $\mathcal F$ for the *frame class*. It consists of the maps $T$ with all of the following properties:

- $T$ is connected, triangulated, and has minimum degree at least 5;
- `NoSep T` holds;
- `DiamondFree T` holds: no ring-embedded occurrence `Occ` of the Birkhoff diamond, in either orientation;
- `Conf2122Free T` holds: no occurrence of RSST configuration 2.122, in either orientation.

The Birkhoff diamond has interior degrees $(5,5,5,5)$ and ring size 6. Configuration 2.122 has interior degrees $(6,5,5,5)$ and ring size 7.

> **$R^\ast_{\rm frame}$** (`RStarFrame`, `PlaneMap/FrameF3.lean`). Every $T\in\mathcal F$ with at least one vertex has a vertex $v$ with $\deg v=5$ and `PureClean T v`.

**Theorem 1** (reduction) **[formal]**. $R^\ast_{\rm frame}$ implies that every `SphericalMap` is 4-colourable.
— `four_color_of_RStarFrame : RStarFrame → ∀ {n} (M : SphericalMap n), M.graph.Colorable 4`, `PlaneMap/FrameF3.lean`.

*Proof outline* (formal; `StudioMathStatements.md` A2). The proof is by strong induction on the support size (`four_color_of_smaller_gate`, `MinimalFrame.lean`). Inside `four_color_of_smaller_gate`, the library reduces every map to connected triangulations of minimum degree 5. **TODO:** name the lemmas it uses for vertices of degree at most 4 and for completion; Track D did not trace them. A connected triangulation of minimum degree 5 then falls into one of three cases:

- **(F1)** It has a separating triangle. Colour both sides by induction and glue (`colorable_of_separating_triangle`). No Kempe chains are needed.
- **(F3)** It has an occurrence of the diamond or of 2.122. Delete the interior, colour the rest by induction, and apply a generated D-reducibility certificate (`DiamondM/DiamondP/C2122M/C2122P.colorable_of_occ`). The certificate step uses the formal non-crossing of Kempe chains on a ring face.
- **(F4)** Otherwise $T\in\mathcal F$. $R^\ast_{\rm frame}$ gives a pure-clean degree-5 vertex. Colour $T-v$ and fill (`extend_of_pureClean`). ∎

**Hierarchy of hypotheses [formal].** The following implications are compiled:

- `rStarNoSepTri_of_core : RStarCore → RStarNoSepTri`;
- `rStarFrame_of_noSepTri : RStarNoSepTri → RStarFrame`;
- `rStarFrame_of_app : RStarFrameApp → RStarFrame` (§3.2).

So `RStarFrame` is the weakest of the library's R\* hypotheses. Its unrestricted form, `four_color_of_global_Rstar` (`RStar.lean`), asks for a pure-clean degree-5 vertex in *every* connected minimum-degree-5 triangulation.

### 3.2 From "appears" to an occurrence

RSST define a configuration occurrence by an induced subgraph with prescribed degrees. Our certificates need a ring-embedded `Occ`, with distinct ring vertices and the full rotation at each interior vertex.

**Theorem 2** (appearance bridge) **[formal]**. Let $T$ be a triangulation with `NoSep T`. Suppose $T$ contains an induced $K_4-e$ on interior vertices `int 0..3` (centres 0 and 2, tips 1 and 3) with the degrees of the diamond, resp. of 2.122 (`Appears γ T int`). Suppose also that every common neighbour of the tips is a centre (`TipsClean T int`). Then $T$ has an `Occ` of that configuration in one of the two orientations.
— `DiamondAppears.occ_of_appears` (`PlaneMap/DiamondAppears.lean`), `C2122Appears.occ_of_appears` (`PlaneMap/C2122Appears.lean`).

**Corollary 3** **[formal]**. The reduction also holds when the class is defined by appearances: `four_color_of_RStarFrameApp` (`PlaneMap/FrameAppears.lean`). Here the hypothesis excludes every appearance whose tips are clean. `appearFree_of_free` shows this exclusion follows from the `Occ` exclusions.

*Remaining gap.* `TipsClean` fails only if the tips and a third vertex $x$ form a separating 4-cycle tip–centre–tip–$x$. Removing separating 4-cycles is the classical reduction "F2". It is **not formalised** (`StudioMathStatements.md` A5).

### 3.3 Non-vacuity checks [formal]

These checks confirm that the definitions are not empty. They are **not** evidence for $R^\ast_{\rm frame}$.

- **The icosahedron** (`RStarSanity.lean`).
  - It is in the class of `RStarNoSepTri`, and every vertex is pure-clean (via Theorem H, §6.3).
  - Both diamond orientations occur (`occ_DiamondM`, `occ_DiamondP`), so the icosahedron is *not* in $\mathcal F$ (`not_diamondFree`).
- **An order-22 triangulation** (`Conf2122Witness.lean`, `Tri22Sanity.lean`).
  - It is in the class, and 2.122 occurs in both orientations (`not_conf2122Free`). So the 2.122 exclusion is not vacuous.
  - The diamond also occurs in this map.
- **Two radius-5 states** (`RadiusFive.lean`). For two certified states, `PureFill … 5` is formal. That no fill exists within 4 swaps is computed, not formal.

**TODO:** exhibit, formally or at least computationally, a map *in* $\mathcal F$, i.e. one with no diamond and no 2.122. The census found 6 configuration-free graphs among 9,912 at orders 12–24 (NightConfigurationLead) **[data]**. IPR fullerene duals are configuration-free **[hand]**.

---

## 4. Kempe classes at a pentagonal hole

This section sets out the framework. All definitions are in `PlaneMap/QuarterFloor.lean`, `QuarterPi.lean` and `QuarterFloorH.lean`.

### 4.1 States

A *pentagonal hole* (`Pent G h`) is a vertex $h$ whose neighbours are exactly $x_0,\dots,x_4$ in cyclic order. Indices are taken mod 5. A proper colouring of a 5-cycle uses 3 or 4 colours, so every state is of exactly one of two kinds (`classify`, `rep_unique`, `single_unique`).

- **Filled with singleton at $i$** (`SingletonAt P c i`). The link reads $(W,X,Y,X,Y)$ at $x_i,\dots,x_{i+4}$.
- **Unfilled with repeat index $j$** (`RepeatAt P c j`). The link reads $(\alpha,\mu,\alpha,A,B)$ at $x_j,\dots,x_{j+4}$.
  - **Lock 1** (`Lock1`): $x_{j+1}$ and $x_{j+3}$ lie in one $\{\mu,A\}$-component of $T-h$.
  - **Lock 2** (`Lock2`): $x_{j+1}$ and $x_{j+4}$ lie in one $\{\mu,B\}$-component.
  - **Doubly locked** (`DoublyLocked`, `DLState`): both locks hold.

The *Kempe class* `kclass M h c₀` is the set of states reachable from $c_0$ by Kempe steps (`KempeEquiv`).

### 4.2 The permutation $\pi$ and the weight $\lambda$

**Theorem 4** (Lemma $\Pi$) **[formal]**. The move $\pi$ = `piMove P` is defined by the table below. It is a single Kempe step (`piMove_kempeStep`) with a two-sided inverse on proper states (`piInv_piMove`, `piMove_piInv`). It restricts to a bijection of every Kempe class (`piMove_bijOn_class`, `PlaneMap/QuarterPi.lean`).

| state | condition | move | image | $\lambda$ |
|---|---|---|---|---|
| $U_j$ | Lock 2 | swap the $\{\alpha,A\}$-component of $x_{j+2}$ ($R_{+3}$) | $U_{j+3}$, with Lock 1 | $+1$ |
| $U_j$ | no Lock 2 | swap the $\{\mu,B\}$-component of $x_{j+4}$ | filled | $-1$ |
| $F_i$ | $M_3$ short | swap the $\{Y,Z\}$-component of $x_{i+2}$ | $U_{i+1}$, no Lock 1 | $-1$ |
| $F_i$ | $M_3$ long | swap the $\{W,X\}$-component of $x_{i+3}$ ($\tau$) | filled | $-3$ |

Here $Z$ is the fourth colour, and "$M_3$ short" means $x_{i+2}$ and $x_{i+4}$ lie in different $\{Y,Z\}$-components. Planarity enters only through Jordan separation at the hole. It is needed to show that the $R_{+3}$, $R_{+2}$, $\tau$ and $\tau^{-1}$ swaps are well defined (`QuarterRotationPlanar.lean`).

**Lemma 5** (Lemma P) **[formal]**. At an unfilled state:

- $\pi c$ is unfilled iff Lock 2 holds;
- $\pi^{-1}c$ is unfilled iff Lock 1 holds.

So a doubly locked state is interior to its unfilled run, and a lockless state forms a run of length 1. The Lean names are `unfilled_succ_iff_lock2`, `unfilled_pred_iff_lock1` and `lemmaP` (`PlaneMap/QuarterLemmaP.lean`).

### 4.3 D-resolvability as a statement about $\pi$-orbits

**Proposition 6** **[formal]**.

(a) An unfilled state that is not doubly locked has a filled $\pi$-neighbour in its class. Hence a class with no filled state consists only of doubly locked states (Lemma C1). Lean: `filled_in_class_of_nonDL`, `allDL_of_targetless` (`PlaneMap/QuarterNonDLImage.lean`).

(b) "Every Kempe class at $h$ has a filled state" implies `PureClean M h` (`pureClean_of_every_class_filled`).

(c) If every $\pi$-orbit at $h$ contains a state that is not doubly locked, then `PureClean M h`. Contrapositively, a hole that is not pure-clean carries a $\pi$-orbit of doubly locked states. Lean: `pureClean_of_no_allDL_orbit`, `allDL_orbit_of_not_pureClean` (`PlaneMap/QuarterBitDynamics.lean`).

(d) Let $\sigma$ swap the $\{\alpha,\mu\}$-component of $x_{j+1}$ (`sigSwap`). Suppose every all-DL $\pi$-orbit contains a state $r$ whose $\sigma$-image is not doubly locked (`GammaImages P`). Then `PureClean M h` holds (`pureClean_of_images`). Also, `four_color_of_images` (`PlaneMap/QuarterNonDLImage.lean`) gives 4-colourability when every map in the class of `RStarNoSepTri` has such a vertex.

**Corollary 7** **[formal by composition; not a named Lean theorem]**. Suppose every $T\in\mathcal F$ has a degree-5 vertex $v$ with a pentagonal link at which no $\pi$-orbit consists only of doubly locked states. Then the 4CT holds for spherical maps. This follows from Proposition 6(c) and Theorem 1.
**TODO:** add the one-line Lean wrapper `rStarFrame_of_no_allDL_orbit` (NightWeakForm §3.1 notes that `rStarFrame_of_images` is also missing).

So, in this language, $R^\ast_{\rm frame}$ asks for one degree-5 vertex in each frame-class triangulation at which $\pi$ has **no frozen orbit**.

**Remark (planarity is essential) [data].** On 1,723 torus triangulations of minimum degree 5, some holes have a class with no filled state:

- at link pattern $(5,5,5,5,5)$, 438 of 827 holes;
- at $(5,5,5,5,6)$, 529 of 960 holes;
- at $(6,6,6,6,6)$, 101 of 196 holes.

(`backgroundMaterial/planemap-structural/longtable/local-runs/18-torus-floor/`; NightWeakForm §4.) So any proof of the statements above must use sphere topology. In the formal proofs it enters through the definedness of $\pi$.

### 4.4 Other formal structure

The project's other formal lemmas at the hole are listed in `NightF6Status.md` §3. They include:

- the no-frozen-DL lemma (`doublyLocked_noFrozen`, `NoFrozen.lean`);
- the universal 10-step period of an all-DL cycle at a $(5,5,5,5,6)$ hole (`gamma_period_ten`, `QuarterGammaPeriod.lean`);
- Jordan duality at $k=3,4$ (`QuarterJordanDual.lean`);
- Lemma A, case 1 (`lemmaA_step`, `lemmaA_injective`, `QuarterFloor.lean`). **TODO:** case 2 of Lemma A is not a separate Lean theorem. Its content is covered by the second row of the $\pi$ table and Proposition 6(a), but the injective form of case 2 is not stated.

---

## 5. Theorem W and the exact class identity

Fix a hole $P$. Let $S$ be any finite set of proper states with $\pi(S)=S$, such as a $\pi$-orbit, a union of orbits or a Kempe class. Write:

- $F$ and $U$ for the numbers of filled and unfilled states of $S$;
- $\lambda$ for the weight in the table of §4.2.

**Theorem 8** (Theorem W) **[formal]**, `PlaneMap/QuarterWinding.lean`.

(a) Pointwise, $\lambda(c)=1-2[F c]-2[F\,\pi c]$ (`lam_eq`).

(b) $\sum_S\lambda=|S|-4F$, i.e. $3F-U=-\sum_S\lambda$ (`sum_lam`, `three_F_sub_U`).

(c) $5\mid\sum_S\lambda$. With the winding $w=\tfrac15\sum_S\lambda$, this gives $3F-U=-5w$ (`five_dvd_sum_lam`, `three_F_sub_U_winding`). The same holds on Kempe classes (`three_F_sub_U_winding_class`).

(d) The **quarter floor** at $h$ holds iff $\sum_{c\in\text{class}}\lambda(c)\le 0$ for every class (`quarterFloor_iff_lam`). The quarter floor (`QuarterFloorConj`, `QuarterFloor.lean`) says that every Kempe class of $T-h$ is at least one quarter filled.

The divisibility in (c) comes from a token in $\mathbb Z/5$ that $\pi$ advances by $\lambda$ (`sigma_piMove`).

**Theorem 9** (exact identity) **[formal]**, `PlaneMap/QuarterLemmaP.lean`. On every such $S$,
$$\sum_{c\in S}\lambda(c)\;=\;|DD|-2N_0-E_2-3\tau ,$$
where:

- $|DD|$ counts states $c$ with $c$ and $\pi c$ both doubly locked (`DDStep`);
- $N_0$ counts lockless unfilled states (`NoLock`);
- $E_2$ counts first states of unfilled runs of length 2 (`E2Start`);
- $\tau$ counts states $c$ with $c$ and $\pi c$ both filled (`TauStep`).

Lean: `exact_identity`, `exact_identity_class`. The pointwise form with a telescoping term is `lam_eq_exact`.

**Corollary 10** **[formal]**.

- Lemma $N_0$: $2N_0\le|DD|-\sum_S\lambda$ (`lemmaN0`, `PlaneMap/QuarterLemmaN0.lean`).
- On an orbit with no filled state, $\sum\lambda=|DD|=|S|>0$. So every all-DL orbit is "positive", and the quarter floor needs negative mass elsewhere in its class.

**Theorem 11** (period divisibility) **[formal]**. Let $w_t$ be any outer vertices adjacent to $x_t$ and $x_{t+1}$ (`OuterW`). Then every all-DL $\pi$-cycle of length $L$ has $10\mid L$, at every link pattern (`allDL_cycle_length_dvd_ten`, `PlaneMap/QuarterBitDynamics.lean`).

**Data consistency [data].** The exact identity was checked with 0 failures:

- on about 4.2M classes (Job D);
- on 55,586 census cycles and 76,415 cycles from constructed graphs (Job BT).

`NightF6Status.md` §3 has the details.

---

## 6. Partial results at holes with consecutive degree-5 neighbours

### 6.1 Theorem F5 (the quarter floor at all-5 holes)

**Theorem 12** (F5) **[formal]**. Let $M$ be a spherical triangulation and $h$ a pentagonal hole whose five link vertices all have degree 5. Then every Kempe class of proper 4-colourings of $M-h$ is at least one quarter filled. No separating-triangle hypothesis is needed.
— `quarterFloor_of_fiveLink`, `PlaneMap/QuarterFloorHBridge.lean`. It is derived from `quarterFloor_of_icoBall` (`PlaneMap/QuarterFloorH.lean`). The link-clique case is vacuous.

The hand proof was reviewed adversarially by another AI session (`NightF5Review.md`, verdict PASS) **[hand]**.

The floor is sharp in the data **[data]**. The census of all minimum-degree-5 triangulations of orders 12–24 covers 156,033 holes and 160,979 classes. In it, 419 classes sit exactly at $1/4$, and no class at *any* degree-5 hole falls below $1/4$ (commit `0c0e098`). At degree 6 and 7 there is no such floor: the minima there are $1/8$ and $2/17$ (`QuarterFloorSection-draft.md`).

### 6.2 Weak F6 (D-resolvability with four consecutive fives)

**Theorem 13** **[formal]**.

(a) **Hole hypotheses.** Let `Hole4 P w q` hold: the four link vertices $x_t$, $t\ne q$, have degree 5, together with the local ring data. Then `PureClean M h` (`pureClean_of_hole4`, `PlaneMap/QuarterHole6Gen.lean`). The same holds for the $(5,5,5,5,6)$ hole structure `Hole6` (`pureClean_of_hole6`, `PlaneMap/QuarterHole6Clean.lean`) and for every $d\ge6$ (`pureClean_of_hole6gen`).

(b) **From degrees.** Let $M$ be a spherical triangulation and $h$ a pentagonal hole. Suppose four link vertices have degree 5 and the fifth has degree $d\ge5$. Suppose also that $h$ lies on no separating triangle or $d\le6$. Then `PureClean M h` (`pureClean_of_four_consecutive_fives`, `PlaneMap/QuarterHole4Bridge.lean`). For $(5,5,5,5,6)$ with no extra hypothesis, see `pureClean_of_degrees` (`PlaneMap/QuarterHole6Bridge.lean`).

*Proof route (formal).* Suppose a class has no filled state. By Proposition 6(a) it is all-DL. A typed state occurs within two $\pi$-steps (`typed_in_orbit`). Following the orbit to a state of type R1 at $k=2$, its $\pi$-image is an R3 state at $k=4$. There the $\sigma$-image is not doubly locked (`sigma_exit_not_DL_k4`), which contradicts all-DL. This last step uses three consecutive degree-5 link vertices (`TripleBallP`) and the degree-5 neighbourhood of $x_{j+3}$.

What weak F6 is *not*:

- It does not give the quarter floor at $(5,5,5,5,6)$, which is open.
- It says nothing about holes without four consecutive degree-5 neighbours.

### 6.3 Relation to the earlier radius theorems

The library already contained two theorems at these holes (`PlaneMap/VacancyIcosahedral.lean`, `RStar.lean`), proved before this programme by a direct case analysis:

- **Theorem H** (`theorem_H`, `pureClean_of_theorem_H`): all five link vertices of degree 5, no separating triangle at $h$ ⟹ every state fills within 3 swaps.
- **Theorem HP** (`theorem_HP`, `pureClean_of_theorem_HP`): four link vertices of degree 5, the fifth of any degree, no separating triangle at $h$ ⟹ every state fills within 6 swaps. **[formal]**

**So the D-resolvability part of Theorem 13 is largely subsumed by Theorem HP**, which also gives an explicit radius bound. What Theorem 13 adds:

- a second, independent proof through the $\pi$-orbit machinery;
- the removal of the no-separating-triangle hypothesis when $d\in\{5,6\}$.

Theorem F5 is not subsumed. It is a quantitative statement (one quarter of each class), whereas H gives only "at least one filled state per class".

### 6.4 Scope: these holes contain a Birkhoff diamond

Let $x_j,x_{j+1},x_{j+2}$ be three cyclically consecutive link vertices of degree 5 at a degree-5 hole $h$. Then $\{h,x_j,x_{j+1},x_{j+2}\}$ spans a Birkhoff diamond, with centres $h$ and $x_{j+1}$ and tips $x_j$ and $x_{j+2}$ **[hand]**. The tips are non-adjacent: otherwise $h x_j x_{j+2}$ would be a separating triangle, given minimum degree 5. All four vertices have degree 5. So:

- **F5 and weak F6 concern configurations containing a Birkhoff diamond.** The diamond is reducible [Bir13]. Its D-reducibility is formal in both orientations (`DiamondMCert.lean`, `DiamondPCert.lean`). These holes therefore never occur in a minimal counterexample, and **these results do not move the 4CT**.
- **Formal caveat.** $\mathcal F$ excludes `Occ`s of the diamond, not appearances. By Theorem 2, a hole with three consecutive degree-5 neighbours lies outside $\mathcal F$ whenever the tips are clean. If they are not, the tips lie on a separating 4-cycle, which the unformalised F2 reduction would remove. **TODO:** state and check this as a Lean lemma ("no 555 link run in $\mathcal F$ under `TipsClean`").
- In the same way, a consecutive $(5,6,5)$ run at a degree-5 hole spans an appearance of 2.122 **[hand]**. So frame-class holes have no cyclic $555$ and no cyclic $565$ in their link pattern.
- Some frame-class triangulations have only $(6,6,6,6,6)$ holes. IPR fullerene duals are an example **[hand]**. So any unavoidable set of link patterns for $\mathcal F$ contains $(6,6,6,6,6)$, where none of the methods of §6 apply (NightWeakForm §3).

---

## 7. Computational evidence

Unless stated otherwise:

- "census, orders 12–24" means all minimum-degree-5 triangulations of those orders;
- "census to order 27" and the order-24–27 group counts mean all minimum-degree-5 triangulations with no separating triangle (the "core class") of those orders. Both censuses were generated by `plantri`. **TODO:** confirm the generator flags for each census;
- counts are from the Studio job logs summarised in `NightF6Status.md` §§3, 4 and 7 and `NightMorningSummary.md`;
- every hit from adversarial searches was re-verified by a second, independent engine.

All entries are **[data]**.

| Statement | Coverage | Result |
|---|---|---|
| Quarter floor at every degree-5 hole | census, orders 12–24: 156,033 holes, 160,979 classes; plus 95,884 adversarial core graphs | 0 failures. Minimum exactly $1/4$ (419 classes) |
| Group-level floor, SigmaUnionC (join $\pi$-cycles by $\sigma$- and $\sigma'$-links; $\Sigma\lambda\le0$ per group) | ~100M groups at orders 24–26; ~368M at order 27 (Jobs H, J) | 0 failures |
| SigmaUnionC and floor on constructed graphs | 61 graphs of 37 vertices (Job BJ, 2,506 hole-orientations); 12 graphs (Job BV, 534 hole-orientations) | 0 failures. Minimum class $F/N$: $1/4$ (BJ), 0.343 (BV) |
| Adversarial flip search against SigmaUnionC / floor | BJ: 396 walks, 318,825 evaluations. BV: 150 walks, 141,538 evaluations | no hit |
| No all-DL $\pi$-cycle at $(6,6,6,6,6)$ holes ("G66⁰") | census to order 27; IPR fullerene duals C60–C88 (1,260 holes); flip search from C60–C80 (Job BR, 72 walks); 153 flat holes C108–C120 (Job BS) | 0 all-DL cycles. Longest DL run grows: 2 (C60), 5 (C70), 14 (C82), 23 (C88) |
| No class without a filled state | fullerene duals C60–C100, 15,204 holes | 0 such classes |

**Caveats.**

- The census statements were found from the census data, so those checks are post hoc.
- §8 shows that census regularities can fail on constructed graphs of moderate size. Treat the table as evidence about the graphs examined, not as a forecast.
- The growing DL runs at fullerenes suggest that G66⁰ may fail at larger orders while the floor still holds (NightG66IPR) **[hand speculation]**.

---

## 8. Negative results

The following statements were proposed during the programme, held on every census graph (orders at most 27), and are **false**. Each counterexample was found by adversarial edge-flip search and verified by two independent engines. Files are under `backgroundMaterial/planemap-structural/longtable/local-runs/27-studio-positive-config/`.

**8.1 $A_{34}'$, W2, W2\*, Lemma $S_\Gamma$ [refuted]** (Job AW, merge `8840b2b`; `jobaw/hits/*.json`, `jobaw/counterexamples.txt`). The search made 438,871 evaluations over 252 walks. It found 61 distinct 37-vertex core triangulations, each with a $(5,5,5,5,6)$ hole carrying a $\Gamma$-cycle (an all-DL $\pi$-cycle) on which:

- **$A_{34}'$** fails (11 graphs). $A_{34}'$ says no two consecutive periods of a $\Gamma$-cycle both have a failing $\sigma$-exit at $k=4$.
- **W2/W2\*** fail (45 graphs). W2 says the $\sigma$-images at the three $k\le2$ positions of a period are never all fixed.
- **Lemma $S_\Gamma$** fails (three families). $S_\Gamma$ says the lockless $\sigma$-exits of a $\Gamma$-cycle carry enough credit to pay its deficit $L$.

Together these refute the per-$\Gamma$-cycle reduction tree for the quarter floor at $(5,5,5,5,6)$. The floor itself held on these graphs.

**8.2 Statement (c), IB-$N_0$, IB-B [refuted]** (Jobs BV `c4c505f` and BT). Statement (c) says every $\Gamma$-cycle $Z$ has a $\sigma$-image on a cycle $T$ with $\Lambda(T)\le-\Lambda(Z)$.

- (c) held on all 2,728 census $\Gamma$-cycles.
- It fails on 12 verified constructed graphs. On a $(5,5,5,5,6)$ $\Gamma$-cycle with $L=320$, every one of the 320 $\sigma$-images misses every heavy cycle (best ratio 0.594). In total 20 of 262 $\Gamma$-cycle records violate (c).
- The lockless variant IB-$N_0$ already fails in the census (2,726/2,728 hold).
- The boundary variant IB-B is killed on the BV graphs.

Before its refutation, (c) was shown to imply $R^\ast$ (NightStatementC) **[hand]**. So it was 4CT-strength, and its census margin was statistical, not forced.

**8.3 Universal budget $B'$ [refuted]** (Job BV). The universal inequality $2|R|\le 2N_0+E_2+3\tau$ fails on 97 $\sigma\cup\sigma'$-groups, with slack between −33 and −4. All of these groups have $\Sigma\lambda=0$ and no positive orbit, so the floor does not need $B'$ on them. The restriction of $B'$ to groups containing a positive orbit, `BudgetUnionPos`, is a formally sufficient certificate for the floor at a hole: `quarterFloor_of_budget_pos`, `sigmaUnionC_of_budget_pos` (`PlaneMap/QuarterBudgetPos.lean`) **[formal]**. It has 0 failures in the data, with slack at least 42 over the census (Job BQ). It remains open, and it is a repackaging of the floor, not an easier statement.

**8.4 Earlier refutations** (`NightF6Status.md` §4) **[refuted]**:

- **Lemma R:** the target remainder is at most 0. It fails at order 27, in 12 of 732 cases.
- **Conjecture P:** configuration-free graphs have no positive cycle. It fails at 32 holes of 28 IPR graphs.
- **$F_4$:** $f=3$ at every $k=4$ lockless exit. It fails once at order 27.
- **"$L\le60$"** for $\Gamma$-cycle lengths. A constructed graph has $L=800$.
- **The fixed-point form of $A_{34}'$:** 550/552 periods, so not exact.

**8.5 What the negative results show.**

- Every statement that refined the quarter floor to a single $\Gamma$-cycle, or to a group with extra structure, failed under adversarial search on graphs of 37 vertices or fewer.
- The surviving statements (SigmaUnionC, `BudgetUnionPos`) are equivalent to the floor at group level, or sufficient for it. No forcing mechanism for them has been identified.
- Exhaustive censuses to order 27 were not a reliable guide to these refinements.

---

## 9. Open problems

1. **$R^\ast_{\rm frame}$**, equivalently (Corollary 7) "no frozen $\pi$-orbit" at some degree-5 vertex of each frame-class triangulation. This is open and at least as hard as the cases of Tilley's problem it covers.
2. **G66.** Show that at a $(6,6,6,6,6)$ hole of a frame-class triangulation no all-DL $\pi$-orbit exists, or at least that every Kempe class has a filled state. This case is unavoidable for $\mathcal F$, and no local lemma of §6 applies. An enumeration of the 2-ball at an all-6 hole shows that the 2-ball forces nothing (NightG66) **[hand]**.
3. **A discharging set.** Find an unavoidable set $U$ of link patterns for $\mathcal F$ such that the weak form is proved at every pattern in $U$. Existing light-star results would have to be checked before use (NightWeakForm §3.3). **TODO:** literature verification.
4. **`BudgetUnionPos`** at every hole. By `quarterFloor_of_budget_pos` it would give the quarter floor at that hole, hence `PureClean`.
5. **F2** (separating 4-cycles) in Lean. This would close the `TipsClean` gap of §3.2.

---

## 10. Reproducibility

- **Lean.** The modules are in `SolvingFrameworkPlan/docs/working/StudioMathLean/`, with checksums in `SHA256SUMS`. The build script `check.sh [built-checkout] [scratch-dir]` compiles every module, against the snapshot build `$HOME/mathlib4-planemap-build`.
  - The most recent full regression in the night log passed with 75/75 modules (51 night modules), 0 errors and 0 `sorryAx` in 265 `#print axioms` lines (NightLog 07:08).
  - Merge commit `1a38b90` reports that all 82 modules compile, after the appearance-bridge modules were added.
  - **TODO:** rerun `check.sh` on the final commit and record the log hash here. Track D did not rerun it.
- **Statement list.** `StudioMathStatements.md` Part B lists every compiled theorem, extracted mechanically (`extract_statements.py`). **TODO:** regenerate it to include the `Quarter*` modules, which are not yet in Part B.
- **Data.** Studio job scripts and outputs are under `backgroundMaterial/planemap-structural/longtable/`. The C++ engine is `picyc.cpp`, with an independent Python engine (`uv_lib.Hole`).

---

## Appendix A. Claim table

All files are in `StudioMathLean/Mathlib/Combinatorics/SimpleGraph/PlaneMap/`.

| # | Claim | Label | Lean name | File |
|---|---|---|---|---|
| 1 | $R^\ast_{\rm frame}$ ⇒ 4CT (spherical maps) | formal | `four_color_of_RStarFrame` | `FrameF3.lean` |
| 1′ | appearance form | formal | `four_color_of_RStarFrameApp`, `rStarFrame_of_app` | `FrameAppears.lean` |
| 2 | appears + `TipsClean` ⇒ `Occ` | formal | `occ_of_appears` | `DiamondAppears.lean`, `C2122Appears.lean` |
| — | diamond / 2.122 D-reducible | formal | `colorable_of_occ` | `DiamondMOcc.lean` etc. |
| — | separating triangle reduction | formal | `colorable_of_separating_triangle` | `MinimalFrame.lean` |
| 4 | Lemma $\Pi$ | formal | `piMove_bijOn_class` | `QuarterPi.lean` |
| 5 | Lemma P | formal | `lemmaP` | `QuarterLemmaP.lean` |
| 6 | PureClean ⇐ no all-DL orbit | formal | `pureClean_of_no_allDL_orbit` | `QuarterBitDynamics.lean` |
| 6d | GammaImages ⇒ 4CT bridge | formal | `four_color_of_images` | `QuarterNonDLImage.lean` |
| 7 | frame form of 6 | composition only | — (**TODO**) | — |
| 8 | Theorem W | formal | `three_F_sub_U_winding(_class)`, `quarterFloor_iff_lam` | `QuarterWinding.lean` |
| 9 | exact identity | formal | `exact_identity(_class)` | `QuarterLemmaP.lean` |
| 10 | Lemma $N_0$ | formal | `lemmaN0` | `QuarterLemmaN0.lean` |
| 11 | $10\mid L$ | formal | `allDL_cycle_length_dvd_ten` | `QuarterBitDynamics.lean` |
| 12 | F5 | formal | `quarterFloor_of_fiveLink` | `QuarterFloorHBridge.lean` |
| 13 | weak F6 | formal | `pureClean_of_hole4`, `pureClean_of_four_consecutive_fives`, `pureClean_of_degrees` | `QuarterHole6Gen.lean`, `QuarterHole4Bridge.lean`, `QuarterHole6Bridge.lean` |
| — | Theorems H, HP | formal | `theorem_H`, `theorem_HP` | `VacancyIcosahedral.lean` |
| — | 555/565 runs span a diamond / 2.122 appearance | hand | — | §6.4 |
| — | `BudgetUnionPos` ⇒ floor | formal | `quarterFloor_of_budget_pos` | `QuarterBudgetPos.lean` |
| — | §7 table | data | — | job logs |
| — | §8 refutations | refuted (data, two engines) | — | `jobaw/`, BV outputs |
| — | D-resolvable = `PureClean` | cited / unverified | — | [Til17] |

---

## References

**TODO:** verify every bibliographic detail against the source before posting. The audit has checked [Til17]'s page and abstract. The others are standard but have not been re-checked here.

- [AH77] K. Appel and W. Haken, "Every planar map is four colorable. Part I: Discharging", *Illinois J. Math.* 21 (1977) 429–490; with J. Koch, "Part II: Reducibility", ibid. 491–567.
- [Bir13] G. D. Birkhoff, "The reducibility of maps", *Amer. J. Math.* 35 (1913) 115–128.
- [Gon08] G. Gonthier, "Formal proof — the four-color theorem", *Notices Amer. Math. Soc.* 55 (2008) 1382–1393.
- [Hea90] P. J. Heawood, "Map-colour theorem", *Quart. J. Pure Appl. Math.* 24 (1890) 332–338.
- [Kem79] A. B. Kempe, "On the geographical problem of the four colours", *Amer. J. Math.* 2 (1879) 193–200.
- [RSST97] N. Robertson, D. P. Sanders, P. Seymour and R. Thomas, "The four-colour theorem", *J. Combin. Theory Ser. B* 70 (1997) 2–44.
- [Til17] J. Tilley, "D-resolvability of vertices in planar graphs", *J. Graph Algorithms Appl.* 21(4) (2017) 649–661, doi:10.7155/jgaa.00433.
