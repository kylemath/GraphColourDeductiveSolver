# Referee report, second round: "Kempe chains around a degree-five vertex: a mod-4 parity formula and a parity law"

Revised draft of 9 Oct 2026 (`main.tex`, commit c678cb2c). Report of 9 Oct 2026, by an AI referee session that wrote none of the note, its Lean code, the first referee report or the literature check.
- **Read:** `main.tex`, `RefereeReport.md`, `LiteratureCheck.md`, `README.md`; `QuarterBitDynamics.lean`; the census engine `Census33/src/c33_eng.c`.
- **Sources checked directly:** Kittell 1935 (scanned pages 407–413, read in full); Kauffman 2005 (arXiv math/0112266, full text); Baldridge–Kauffman–McCarty (arXiv 2607.22398v1, HTML); Mohar–Salas (arXiv 0901.1010v2, HTML); Mohar 2006 (author's reprint, §5).
- **Code:** my own, written for this round. It imports nothing from the project and is not in the repository. All runs used at most 2 processes under `nice -n 10`.

## 1. Verdict

**Minor revision.**
- The repaired converse of Proposition 2 is correct. I checked it line by line and tested it on 1.83M fresh unfilled states, including about 241,000 where T[U] contains a cycle, with 0 failures.
- The new period-15 / multiple-of-30 remark is true. It is consistent with the census and with Lean. However, it does not need the law, and the note should say so (N2).
- One sentence added in answer to first-round item M3 is **false**: "other unfilled states can have N = 6". On the sphere, N ≥ 8 holds at every unfilled state (N1).
- The prior-work paragraph is accurate where I could check it against the sources. It needs three small additions so that it does not undersell nearby work (N4).
- All first-round items were addressed (§5). Only M3's fix introduced an error.

## 2. New items, by severity

### N1. Error (introduced by the M3 fix): "Eight is the minimum of N only among DL states …; other unfilled states can have N = 6 [computed¹]" (§2, after Definition 1)
This is false on the sphere. Proof, using only Proposition 2. Let c be unfilled.
- If L1 holds, then x0 ∉ K_αδ(x2), so there are at least 2 αδ-chains and at least 1 βγ-chain.
- If L1 fails, then x1 and x3 lie in different βγ-chains, so there are at least 2 βγ-chains and at least 1 αδ-chain.
- So the pairs {αδ, βγ} contribute at least 3. In the same way (L2, x4) the pairs {αγ, βδ} contribute at least 3. Together with αβ ≥ 1 and γδ ≥ 1 this gives **N ≥ 8 at every unfilled state**.

**Data.** On fresh random spheres the minimum of N over unfilled non-DL states was 8. There were 48,000+ sampled states in two runs (seeds 5 and 6; 150 + 400 graphs, 20% of states sampled for N), with 0 below 8. The first report asserted N = 6 in M3 but gave no count. The value is presumably an off-sphere figure: on the torus, Proposition 2 fails and N < 8 occurs.

**Fix:**
- delete "only among DL states" and the N = 6 clause;
- state "N ≥ 8 at every unfilled state [hand], by the argument of Proposition 4; equality at a DL state iff rigid";
- the abstract's "(eight chains, the minimum for doubly locked colourings)" is then true but understated, and can say "the minimum for unfilled colourings".

### N2. Overstated dependence: "Along a π-cycle of DL states N alternates in parity, so such a cycle has even length; as π acts on link colours with period 15, its length is a multiple of 30 [hand]" (after Corollary 7)
**The statement is correct. I verified it.**
- π acts on the link word by swapping positions j+2 and j+3 and moving the frame by 3.
- All 120 unfilled link words have π-orbit of length **exactly** 15. The argument needs "exactly 15", not just "π¹⁵ = id", so the note should say "every link word has orbit length exactly 15".
- Then π^L c = c forces 15 | L, and evenness gives 30 | L.

**But the law is not needed.**
- The library already has the **compiled** theorem `allDL_cycle_length_dvd_ten` (and `_recol`) in `QuarterBitDynamics.lean`, from commit 4d257b72 of 7 Oct. It is built by `check.sh` and so lies within audit J14's 91-module rebuild.
- That theorem proves 10 | L for every all-DL π-cycle, and 10 | L also for cycles up to colour renaming. It works from the outer-vertex bits (bitF of order 10), with no chain counts. The project noted "absolute colourings: 30" on 6 Oct (`NightF6Status.md`).
- So 15 | L (link) and 10 | L (Lean) already give 30 | L, and "even length" is not new information from the law.
- `LiteratureCheck.md` row (iv) says the even length is "a genuine consequence of the law, not of local periodicity". That is wrong: second-ring periodicity gives it.

**Consistency with the census.**
- The census engine keys states by colour-class partitions (`canon()` in `c33_eng.c`), so its "length 20" counts cycles up to renaming.
- After 5 π-steps the link word returns up to a renaming τ of order 3, and this holds for all 120 words.
- So a cycle of length 20 up to renaming has absolute length 20·3 = **60**. That is consistent with 30 | L and with Lean's 10 | 20.
- The README's "no conflict" is right. Note that the VH∃ paper (`VHE-paper/main.tex` l.345) says "all of length 20" without "up to renaming", and should add it.

**Fix:** cite `allDL_cycle_length_dvd_ten` [compiled], and say that, with the link period, it gives 30 | L independently of the law. The remark can stay as a consistency check of the law.

### N3. Minor overclaim: abstract "Apart from one local identity and the link-free half of one lemma, every result fails on the torus"; §5 "Every other result fails on the torus"
Lemma 12 (Fisk mod 4) and Lemma 13 (Kempe invariance of cw mod 4) are stated for every closed oriented surface, and they hold there (Mohar–Salas, Lemma 3.1 and Cor. 3.3). **Fix:** say "every other result of Section 3".

### N4. Prior work: accurate, but three additions are needed for fairness
I checked every new claim against the source.
- **Kittell 1935. Confirmed.**
  - Impasse: ring DBABC, with two intersecting Kempe chains from A to C and to D.
  - Eight named chains and nine operations; ζ is the "left-hand tangent chain", the BC chain touching the ring in the adjacent B and C.
  - Under B = α, A = β, C = γ, D = δ (ring D,B,A,B,C ↔ x4,x0,x1,x2,x3), ζ swaps K_αγ(x2), which is π. Kittell says left and right are arbitrary; mirrored, it is η. Suggest adding "(or η, by mirror symmetry)".
  - Kittell: "ζ and η have periods of fifteen". Confirmed.
  - On Errera's map, α, β, γ, δ, ζ, η are possible "in any combinations or raised to any power", while ε (end tangent chain) gives a non-impasse colouring (his Fig. 8). Confirmed.
  - "N ≥ 8 implicit in the eight chains" is fair: the eight chains are distinct by Proposition 2.
- **Kauffman 2005. Confirmed.**
  - §3 proves Spencer-Brown's Parity Lemma for planar cubic graphs.
  - It says a result of Tutte, cited as *On the four-color conjecture* (PLMS) and so Tutte 1948, implies the lemma.
  - It says the lemma fails for the Petersen graph with one edge deleted.
  - **Correction:** the parity pass is in §5 (five transformations A–E; A, C, D "complex", B and E simple), not "Secs. 4–5".
  - **Addition:** §4 contains a closer relative that the note does not mention. At a 1-deficient prime formation the curve count is 5 or 4, according as the two contextual curves have the same or different colours. Since "four and five have different parity", a simple operation on a contextual curve that touches the deficiency is forced to change the factorisation. This is a parity-of-curve-count argument at a hole, at an edge rather than a pentagon, and the note should cite it as the nearest published antecedent of Theorem 8 and the law.
- **BKM 2026 (arXiv 2607.22398). Confirmed with three caveats.**
  - The parity pass loops on a planar graph: "twelve complete cycles, or sixty steps".
  - Its remark is confirmed: "Certain steps in the algorithm switch the parity of the number of alternating color paths". It cites both Kauffman 2005 and Spencer-Brown's MS, not only unpublished work, so the note's "its exact statement is in unpublished work" should say "partly in [Kauffman 2005, Sec. 5] and partly unpublished".
  - (a) BKM call configuration 𝒞 "the edge coloring version of the famous Kempe chain problem". "Heawood's interlocked chains" is the note's gloss, so attribute it as such.
  - (b) BKM themselves connect Spencer-Brown's **parity mills** φ₁, φ₂ to Kittell: the mills "are based on moves from the impasse group". The mills are shown only in figures, so I could not tell whether one of them iterates ζ (= π). The note should mention the mills and say this was not determined. This is the one place where an overlap with "N-parity along π" could hide.
  - (c) Questions 5.1–5.2 ask whether non-symmetric plane graphs exist in which every pentagonal face, or at least two non-polar pentagonal faces, **admit** a looping 1-deficient colouring. The note's "the parity pass loops at every non-polar pentagonal face" should say "admits a looping colouring". The comparison with LPC ("no implication either way") is fair.
- **Mohar 2006, §5. Confirmed.** It reports that Tutte "observed that this is Kempe invariant": the parity of the degree.
- **Mohar–Salas 2009. Confirmed.**
  - Lemma 3.1 is Tutte's parity formula for the degree on closed orientable surfaces.
  - Cor. 3.3 is the Kempe invariance of the degree parity.
  - Neither discusses holes or boundaries.
  - Both are stated for simplicial triangulations. The note applies Lemma 13 to the multigraph T°, which is covered by the note's own proof of Lemma 12. Say so in one clause.

**"What is new" verdict:** fair and suitably hedged, given N4(b) and the explicit Fisk/Mohar 1985 caveat. None of the sources I read contains the hole terms of Theorem 5, lock parity in odd-degree form, the law or rigid isolation.

### N5. Wording of the repaired proof (G1)
The proof is correct (§3). Small points:
- define e₀ := e_m for the corner at u₀;
- add one clause for e_i = e_{i+1} (a leaf u_i): the list is then all the other neighbours, which is non-empty;
- update the sentence after the proof: "the walk above is the referee's repair, checked by a second referee (RefereeReport2.md) [hand]".

### N6. Housekeeping
- The LaTeX comment at ll. 233–235 says the disclosure "still says 'this paper'", but the text now says "this note" (commit 70a2eed5). README item 1 likewise says the disclosure was "left unchanged". Bring both up to date.
- README "Claims still unreviewed" item 4 can be closed, and item 8 can cite N2.

## 3. The repaired converse of Proposition 2: line-by-line check

The argument for L2, with Q = K_βδ(x1), x4 ∉ Q and U = Q ∪ {v}:
1. **T[U] is connected and v is a leaf.** U-neighbours of v: x0 and x2 are α, x3 is γ, x4 ∉ Q, so only x1. Correct.
2. **x4 lies in the face R at v's corner.** vx4 meets T[U] only at v, and a leaf has one corner. Correct.
3. **∂R is one closed walk.** True for a connected plane graph. The walk starts and ends with vx1 and passes v once. Correct (0 failures of "v not once").
4. **Corner lists lie outside U.** The neighbours strictly between consecutive T[U]-edges at u_i are not in U, because the subgraph is induced. Correct.
5. **Lists are non-empty.** If e_i ≠ e_{i+1} were consecutive in T, the face between them is a triangle with all three vertices, and hence all three edges, in the induced T[U]. It is then a face of T[U] on the R side, so equal to R, but it contains no vertex while R contains x4. If e_i = e_{i+1}, the list is deg − 1 ≥ 2 vertices. Correct; the second case is implicit (N5).
6. **Adjacency within a corner.** Consecutive rotation neighbours are adjacent, since faces are triangles. Correct.
7. **Gluing.** The last entry w at u_i spans the face (u_i, w, u_{i+1}), which at u_{i+1} is the first face after e_{i+1}. Correct.
8. **Colours.** Non-U neighbours of Q are α or γ (a β or δ neighbour would be in Q). x4 (δ) has no Q-neighbour, so it occurs only at v's corner. Correct.
9. **Cut at x4.** This leaves an α/γ walk x0, …, x2, x3 in T − v, so x0 ∈ K_αγ(x2). Correct.

The L1 case (Q = K_βγ(x1), x3 ∉ Q; the walk x4, x0, …, x2 is α/δ) goes through the same way.

**Test (`walk.py`).** The test builds exactly this walk from the rotation system and checks every step above separately:
- v is a leaf; the walk closes; v occurs once; v's corner is (x2, x3, x4, x0);
- no corner list is empty; no entry is in U; within-corner adjacency; gluing between corners;
- colours; x4 (resp. x3) occurs exactly once;
- the cut walk is a walk with the stated colours and ends;
- an independent BFS agrees.

It also checks both directions of Proposition 2 at every unfilled state.

**Population.** Random sphere triangulations, n = 9–40, built by stacking and then 6n random flips. Up to three degree-5 vertices per graph, and 400 random Kempe exchanges from a backtracking colouring. Two seeds, 1,500 graphs each.

| quantity | seed 11 | seed 22 |
|---|---|---|
| unfilled states | 912,532 | 920,097 |
| ¬L2, T[U] has a cycle | 58,438 | 59,482 |
| ¬L2, T[U] a tree | 351,043 | 354,318 |
| ¬L1, T[U] has a cycle | 60,487 | 62,940 |
| ¬L1, T[U] a tree | 351,471 | 351,986 |
| total cyclomatic number of T[U] over cyclic cases | 150,361 | 154,326 |
| longest boundary walk (corners) | 46 | 48 |
| **failures (any check, incl. Prop. 2 both ways)** | **0** | **0** |

**Sensitivity.** Two mutants were caught at once:
- dropping the first entry of each non-v corner list: thousands of "empty corner" and "gluing" failures;
- taking Q as the αβ-chain instead of the βδ-chain: "v not leaf".

## 4. Remark on period 15 / 30 (summary of N2)

| check | result |
|---|---|
| π-orbit length of each of the 120 unfilled link words | 15 for all 120 |
| orbit length up to colour renaming | 5 for all 120; the renaming after 5 steps has order 3 |
| census "length 20" (canonical keys, so up to renaming) | absolute length 60; 30 \| 60 ✓; Lean `_recol` 10 \| 20 ✓ |
| Lean `allDL_cycle_length_dvd_ten` (10 \| L, compiled, outer bits) | consistent; with 15 \| L it already gives 30 \| L without the law |

## 5. First-round items: status

| item | status |
|---|---|
| E1 (mod-4 overclaim) | **Fixed.** Title, abstract and the sentence after Theorem 5 all say that N is determined mod 2. |
| G1 (Prop. 2 converse) | **Fixed and correct** (§3). Wording nits in N5. |
| G2 ("each result fails off the sphere") | **Fixed** for (∗), the link-free half of Lemma W, Prop. 4 and Thm 8, with data. Residual: Lemmas 12–13 (N3). |
| G3 (population of 282/544) | **Fixed.** Populations x0 ∉ K and x0 ∈ K are separated. |
| G4 (π beyond its definition) | **Fixed.** The extension `piMove` is introduced before "permutes each Kempe class". |
| M1 (n = 22, "none at order 20") | **Fixed.** "261,093 greedy reductions … not an exhaustive search". |
| M2 (stale census) | **Fixed.** Orders 22–34; NR 8 at order 33, stays 8 at order 34. |
| M3 ("minimum number of chains") | **Fixed in the abstract, but the added §2 sentence is false** (N1). |
| M4 ("the law alone") | **Fixed.** |
| M5 (notation, labels) | **Fixed.** κ(p,q); cw vs cw_S, cw_{T°}; one label per lemma; loopless surfaces; §3 exception; `StarHyp`. |
| M6 (review markers) | **Fixed.** Prop. 2's marker can now be updated (N5). |

I did not re-derive the unchanged proofs (Theorem 3 (∗), Theorem 5, Lemma W, the law). The first report checked them, and nothing in them changed except notation. I did re-read Lemma 12's proof, including the multigraph case, and found it correct.
