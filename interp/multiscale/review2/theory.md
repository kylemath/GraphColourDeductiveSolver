# Desk check of the second outside review (claims 1–7)

22 Oct 2026, 40-minute box. Ratings: **correct** / **correct with caveat** / **wrong**. Notation and the height convention are those of `../levelling/RESULTS.md`. Heights live on **vertices**, with increments ±e_{c(u)⊕c(v)}. So h(x) ≡ c(x) + const (mod 2Λ), under Λ/2Λ ≅ Z2². The c* construction is being tested elsewhere and is not covered here. The scratch scripts (`tv.py`, `tx.py`, `q.py`) were run outside the project folder and their outputs are quoted below.

**1. Crater vs 4-coloured hole: first half correct, second half wrong as stated.** e_a+e_b+e_c = 0, so a w = ±2 crater has zero monodromy. That concedes review1 §1. The topological sentence does not parse: the link's image runs *through* the vertices of ∂Δ³, so it has no class in π₁(∂Δ³ ∖ vertices). The correct obstruction is not homotopical: v extends iff its link misses some colour. Worse, 4 colours on the link do not force nonzero monodromy. Over all proper 6-cycle links with alternating face signs, |t| ∈ {0, 2√3} when the link uses 4 colours and t = 0 otherwise (`q.py`). Example: link 0,1,0,2,3,2 gives +e1−e1+e2−e1+e1−e2 = 0. Our F3 bound R ≥ d(v, odd) − 2 needs nonzero monodromy (`tilt_aware.md` F3), so it covers only the 2√3 holes. Holes are in any case not level leaves.

**2. Two-vortex lemma: algebra correct; the explanation of the 42 is wrong.** r_a∘r_b(x) = x + 2(a−b), and h ≡ c mod 2Λ holds in our vertex convention. So c(u) ≠ c(v) ⇒ t ∉ 4Λ ⇒ |t| ≥ 2 ⇒ τ ≥ 1. In general, t ≡ 2Σ_o c(o) (mod 4Λ) for any even set of vortices. On level colourings (|t| ≤ 2) this gives **t = 0 ⇔ the XOR of the vortex colours is 0**. This held in 84/84 level colourings of the 42 E1 balls with n ≤ 200 (`tx.py`, 2 to 76 vortices).

The proposed explanation of the 42 still fails, for two reasons:
- **Wrong population.** The 42 t=0-infeasible balls are not all two-vortex caps. Only 11 have two vortices; 10 have six, and the rest have 12 to 148. The 13 feasible balls have 4, 8, 12, 26, 36, … vortices, and **none** has two. So "the 13 are the caps with c(u) = c(v)" is a category error.
- **No forcing of the colours.** In 9 of the 11 two-vortex balls (2 large ones unfinished), a proper colouring with c(u) = c(v) exists. It then has |t| = 4 or 8, and no *level* colouring has c(u) = c(v) (`tv.py`). The lemma therefore restates "t = 0 is infeasible" as "c(u) ≠ c(v) in every level colouring". It does not derive it.

The actual cause is the geometric Z3 class f(t) = χ ≠ 0 of the Eulerian annulus around the pair (closing Lemma 1, round3 §1). χ is fixed by the positions of the poles mod the 3-sublattice.

**3. Citations: correct with caveat.** Izmestiev, Kusner, Rote, Springborn and Sullivan, arXiv 1207.3605, do prove that there is no 5,7-triangulation of the torus (exactly two exceptional vertices, of degrees 5 and 7). That is a multi-author paper giving *geometric re-proofs* of a result they call known; the original is Jendrol'–Jucovič (1972), as review1 C noted. Mohar–Salas (arXiv 0901.1010, J. Phys. A 2009) prove that deg mod 12 is a Kempe invariant for **3-colourable** triangulations of closed oriented surfaces. They apply it to T(3L,3M) with **3 ≤ L ≤ M** to get at least two Kempe classes. The quote holds once those two qualifiers are added.

**4. Hub: wrong.** The rim of W_d avoids the hub colour, so it is a proper 3-colouring of C_d. The walk could only drift if the rim labels alternated a,b,a,b, and a rim with those labels uses all 4 colours. So on a 3-coloured rim the alternating-sign walk stays bounded. Exhaustively for d = 4..12 (`q.py`), **every** proper rim colouring is level (τ ≤ 1, our definition). The shortest two-colour alternating run among them is 2, 3 or 4 (e.g. d = 6, rim 1,2,3,1,2,3), not d−3. Review1 G exhibited one level colouring per d; it did not say every level colouring looks like that. Levelness puts no constraint on a lone wheel. Whatever locks a hub has to come from outside the wheel.

**5. Plateau: the bound is right with a caveat; the mechanism is not justified.** 4τ + |t| = 6 is closing Lemma 2 (≤ 4) plus the base-point term |t_B| ≤ 2 (review1 B), so the bound is fine. Two problems:
- **Diameter vs. radius.** Since the renaming constant c is free, the pointwise offset is ≤ diam/2 = 3, not 6.
- **"2 units per layer" is only a lower bound.** Heights are 1-Lipschitz per edge, so a band of R layers per side absorbs at most about 2R units. That gives R ≥ M/2 − O(1). The matching upper bound would be a Lipschitz-extension lemma, and that is exactly what fails on the L=4 tube and at insertion width 4 at L=8.

Saturation also predicts the wrong shape of the data. If the offset typically saturated 6, R = 3 would become generic. Instead, at L = 572, R = 2 in 91% of closings and R = 3 in 8%. The better reading is that the ≤ 4 part saturates (P(R=1) → 0, mode R = 2), while the +2 base-point part is realised rarely (R = 3). This fits merge_proof/witness, where τ* removes the even-pocket excess.

**6. L = 4 vs L ≥ 5: the argument is wrong; the conclusion is half right.** Pigeonhole only excludes *globally* rainbow rows. The rigidity argument of round2 §3 needs only every 4 consecutive colours distinct. So the period-4 row (0,1,2,3)^{L/4} is frozen for every L ≡ 0 (mod 4): `q.py` finds 2 successors at L = 4 and 8, both shifts. It is excluded at L ≥ 8 only because |t| = L/2 > 2 makes it non-level. "Unlock within 1–2 rows" is also false: insertion width is k* = 2, 1, 2, **4**, 2, 2 for L = 5..10 (bandfill §2). The cause is hidden runs of 4 under the some-base-point level definition.

Correct statement:
- For L ≥ 5, no *level* row is frozen.
- Level rows are fillable with C(2), recolouring the level rows.
- With the level rows kept, they are fillable with k*(L) ≤ 4 for L ≤ 10. k* is conjectured to be ≤ 2 under τ* or a two-lap radius ≤ 1.5.
- Uniformity in L is not proved (bandfill §4).

**7. Fixes: (a) correct with caveat, (b) correct with caveat, (c) wrong.**
- **(a) Induced root split.** Our closing pipeline already uses induced seams (closing E1), and in an internally 6-connected map any vertex link is an induced cycle, so such a split exists. The caveat is that the chords that matter arise at intermediate merges, not at the root.
- **(b) Pocket bound S0.** Bounding the pockets crossed per merge by S0 bounds τ(P) ≤ S0 + 1 before re-levelling (merge_proof §1). It is a legitimate hierarchy constraint, but nobody has proved that hierarchies obeying it exist. The data do not need it: 57 crossed pockets still gave R ≤ 1, w ≤ 2.
- **(c) Coalescing pockets.** This **conflicts with Lemma M**. The first half, that chords with an endpoint inside the seam disappear and pockets fuse, is merge_proof §1 verbatim. But the fused monodromy t_P = a_P + P_π b_P is fixed by the vortices inside P. A vortex-free collar cannot change it, so any collar that "flattens" P must reach a vortex. The ico10 witness (merge_proof/witness) realises this: |t_P| = 2√3 under 23/24 renamings. It was cured only because its vortices sit at depth 1–2 (w* = 2). The fix needs the W2 sub-union condition (|t_Q| ≤ 2 for every connected sub-union of pockets). That condition is not preserved by W1 re-levelling (4/231 violations on flip10_1).

Sources: [IKRSS, arXiv 1207.3605](https://arxiv.org/abs/1207.3605v1); [Mohar–Salas, arXiv 0901.1010](https://arxiv.org/abs/0901.1010).
