# NightG66: DL runs at all-6 holes

Night worker, 7 October 2026 (written 05:38–05:55 MDT). **Exploratory. Hand analysis plus a small 2-ball enumeration (scratchpad script, not committed). Unreviewed.**

Sources:
- NightWeakForm (G66, §2 candidate lemmas X4/X3, frame-class pattern facts); NightPostAW; NightLog-2026-10-06 from "05:03 — Studio Job AW" to the end;
- Lean: `QuarterPi`, `QuarterRotation` (`rot3`, `rot3_values`), `QuarterLemmaP`, `QuarterGammaPeriod`, `QuarterHole6Clean`, `QuarterNonDLImage`, `QuarterWinding`, `QuarterPairDuality`, `QuarterStepChange`, `NoFrozen`, `FrameF3`, `RStarCore`;
- `QuarterHole66` (a10f4971, landed while this note was being written). It formalises the facts of §1.2 below. Where my hand derivation and that file overlap they agree, and the file is the ground truth.

Labels: [formal] = in Lean, 0 sorry; [proved] = a complete hand argument here; [computed] = the 2-ball enumeration of §1.4; [sketch]; [data]; [lit-L] = a literature recollection with low confidence.

## 0. Bottom line

1. **There is a universal (pattern-free) DL dynamics on the five w-vertices, and it is a signed rotation of period 10** [proved; checked by enumeration at 7 patterns].
   - Write a DL state's outer w-colours as five bits.
   - On every DD step, at every link pattern, the bits move by F(b) = (¬b₃, b₄, ¬b₀, b₁, ¬b₂).
   - F⁵ is the complement and F¹⁰ = id.
   - This one map explains `gamma_period_ten`, the R1/R3 alternation at (5,5,5,5,6), and the new R1→R1 and R2→R2 steps at (6,6,6,6,6).
2. **The link degrees act only as 2-clauses on the w-word.**
   - Each degree-5 link vertex x_t contributes a ring edge w_{t−1}w_t, and so a forbidden pair of bits.
   - At (5,5,5,5,5) and (5,5,5,5,6) only the 2-orbit {R3: BABμA, R1: ABμαμ} survives. That is the formal Γ-cycle.
   - At (6,6,6,6,6) there are no w–w edges. **All 32 w-words, i.e. all four F-orbits (10, 10, 10, 2), survive.**
3. **The 2-ball says nothing at an all-6 hole** [computed, sound over-approximation with the Jordan exclusions at the hole].
   - There are 74 DL-feasible ring colourings per repeat index.
   - Every one of them has a DL-feasible successor and lies on a local cycle.
   - None of them has a σ-image that is certified non-DL, in any branch of the non-local memberships.
   - At (5,5,5,5,5) and (5,5,5,5,6) the same model empties the core (it reproduces the formal W). At (5,5,6,6,6), 59 nodes survive.
4. **The NightWeakForm candidate X4(6)/X3(6) is vacuous** [proved].
   - At a degree-6 link vertex x_{j+3} (resp. x_{j+4}), σc always keeps an α-neighbour there.
   - So σc always has all four lock ends.
   - At an all-6 hole a non-DL σ-image can only come from a lock chain cut **outside the 2-ball**.
5. **The Theorem W sign question.**
   - In the Lean convention Σλ = 5·windingSum, so an all-DL class has winding **+N/5**. The task statement's −N/5 is the opposite sign convention.
   - "Planarity forces class winding ≤ 0" is *literally* the quarter floor (`quarterFloor_iff_lam`), and the floor ⇒ R\* ⇒ 4CT. So it is not easy, and it is not an Euler fact.
   - It breaks at the per-cycle level: all-DL π-cycles (positive winding) exist on the sphere at (5,5,6,6,6), (5,5,7,5,7) and the AW (5,5,5,5,6) graphs. So any sign constraint is class-level.
   - The "winding" is the lifted rotation number of the repeat index around the link. It is not the homology class of a curve, and the Euler identities (six-pair, dualities) hold identically along DL runs.
6. **No pattern-free mechanism can kill all-DL π-cycles,** because they exist on the sphere at (5,5,6,6,6) and (5,5,7,5,7).
   - At an all-6 hole the 2-ball contributes nothing (items 3–4).
   - So a proof of G66 must use **non-local** structure: a 3-ball or larger, chain geometry, or the frame class globally. Or it must be **class-level**, not orbit-level.
   - §4 gives the conjecture ladder and the exact Studio tests.

## 1. Setup and what is forced

### 1.1 The all-6 hole

- h has degree 5, with link x_0..x_4, all of degree 6.
- x_t has neighbours h, x_{t−1}, x_{t+1}, w_{t−1}, m_t, w_t, with the outer ones in rotation order.
- w_t is the third vertex of the face x_t x_{t+1} w_t. m_t is x_t's inserted vertex.
- The second ring is the 10-cycle … w_{t−1} m_t w_t m_{t+1} … (`Hole66`, [formal setup]).
- I assume the 15 vertices are distinct and the ring has no chords. Chords only add constraints, so all "nothing is forced" statements below survive them.

DL state at j: link (α, μ, α, A, B) at x_j..x_{j+4}.
- Lock1: a {μ,A}-chain x_{j+1} → x_{j+3}.
- Lock2: a {μ,B}-chain x_{j+1} → x_{j+4}.
- π = R₊₃ swaps the **{α, A}-component K of x_{j+2}**. K contains x_{j+3} and misses x_j (`rot3Def_of_lock2`, Jordan).
- The new link is (α, B, α, μ, A) at x_{j+3}..x_{j+2}, so the repeat index moves **j ↦ j+3 at every pattern**. The renaming is α′ = α, μ′ = B, A′ = μ, B′ = A.

Properness alone gives [formal, `ring66_dom`]:
- w_j, w_{j+1} ∈ {A,B};
- w_{j+2} ∈ {μ,B};
- w_{j+3} ∈ {α,μ};
- w_{j+4} ∈ {μ,A}.

The lock ends give [formal, `ring66_of_dl`]:
- (w_j, m_{j+1}, w_{j+1}) ∈ {(A,B,A), (B,A,B), (A,α,B), (B,α,A)};
- μ ∈ {w_{j+2}, m_{j+3}, w_{j+3}};
- μ ∈ {w_{j+3}, m_{j+4}, w_{j+4}}.

### 1.2 The type of the image: exact, at every pattern [proved; formal at Hole66 as `image_type66`]

- w_{j+1} is adjacent to x_{j+2} ∈ K, and w_{j+3} is adjacent to x_{j+3} ∈ K. So both are recoloured iff their colour is α or A.
- Hence type(πc) at j+3 is:
  - **R1** if w_{j+3} = μ;
  - **R3** if w_{j+3} = α and w_{j+1} = B;
  - **R2** if w_{j+3} = α and w_{j+1} = A.
- The proof uses only the two faces at x_{j+2}x_{j+1} and x_{j+3}x_{j+4}, so it is pattern-free.
- `r3_step` is the case w_{j+3} = μ.
- `r1_ring` (Hole6) is the statement that degree-5 ring edges force (w_{j+1}, w_{j+3}) = (B, α) after R1. At an all-6 hole nothing forces it.
- Transition sets at all-6: R3 → R1; R2 → {R2, R3}; R1 → {R1, R2, R3}. These match `dd_step66`.
- **So tk_step's (type, k) ↦ (flip, k+2) fails at (6,6,6,6,6).** It is also meaningless there: k is defined relative to the unique degree-6 vertex, and the all-6 hole is rotation-symmetric.

### 1.3 The w-word map F (the real analogue of tk_step) [proved]

Encode the w-colours of a DL state at j by the bits

  b₀ = [w_j = A], b₁ = [w_{j+1} = A], b₂ = [w_{j+2} = μ], b₃ = [w_{j+3} = α], b₄ = [w_{j+4} = μ].

On a DD step:
- w_{j+1}, w_{j+2}, w_{j+3} are adjacent to x_{j+2} or x_{j+3} ∈ K, so they are swapped iff they are coloured α or A.
- w_j and w_{j+4} are adjacent to x_j ∉ K. They have no α colour, and an A-coloured one would put x_j in K. So they are untouched.

Reading the new word at j′ = j+3 (w′_{j′+i} = w_{j+3+i}) with the renaming gives

  **F(b₀,b₁,b₂,b₃,b₄) = (¬b₃, b₄, ¬b₀, b₁, ¬b₂).**

This is deterministic at every link pattern; only the m-vertices m_{j+1} and m_{j+4} can be non-local.

Consequences [proved]:
- Each bit visits every position once in 5 steps and is negated at 3 of them. So **F⁵ = complement**, F has no orbit of size 1 or 5, and **F¹⁰ = id**.
- The orbits on the 32 words have sizes 10, 10, 10 and 2. The word lists below give w_j..w_{j+4}, with type sequences:
  - (a) R3 R1 R1 R1 R3 R1 R2 R2 R3 R1: BBBμA ABμμμ AABμA ABBαμ BABμμ AAμαμ BABαA BBμαμ BAμμA ABμαA
  - (b) R3 R1 R1 R2 R3 R1 R2 R3 R1 R1: BBBμμ AAμμμ AABαA BBBαμ BAμμμ AAμαA BBBαA BBμμμ AAμμA ABBαA
  - (c) R3 R1 R1 R1 R1 R1 R2 R2 R2 R2: BBμμA ABμμA ABBμA ABBμμ AABμμ AABαμ BABαμ BAμαμ BAμαA BBμαA
  - (d) R3 R1: BABμA ABμαμ. This is the (5,5,5,5,6) Γ-cycle: R3 with w_{j+1} = A and w_{j+3} = μ, and R1 with r1_ring's (B, α).
- **Period of all-DL cycles** (colour-normalised states, as in Studio's `picyc`):
  - the repeat index forces L ≡ 0 (mod 5);
  - F¹⁰ = id with F⁵ ≠ id forces 2 | L.
  - Independently, `delta_rank_odd'` [formal] says ΣC changes by an odd amount on each DD step, which gives 2 | L again.
  - So **10 | L at every pattern**, matching Studio's L = 20.
- **Absolute colours** [proved]:
  - α is constant along a DL run, and (μ, A, B) ↦ (B, μ, A) is a 3-cycle.
  - So the swapped pairs cycle {α,A}, {α,μ}, {α,B}, and every lock chain lies in an α-free pair.
  - A Lean-level Γ-cycle (absolute colourings, `piPerm`) has length ≡ 0 (mod 30). A Studio L = 20 cycle lifts to 60.

**Degree-5 link vertices as clauses.** A ring edge w_{t−1}w_t (deg x_t = 5) forbids equal colours. Relative to j this gives:

| degree-5 link vertex | forbidden pattern |
|---|---|
| x_{j+1} | b₀ = b₁ |
| x_{j+2} | b₁ = b₂ = 0 |
| x_{j+3} | b₂ = 1, b₃ = 0 |
| x_{j+4} | b₃ = 0, b₄ = 1 |
| x_j | b₄ = 0, b₀ = 1 |

The degree-5 positions rotate by −3 relative to j each step. An all-DL orbit must keep every one of its 10 words clause-consistent. This is the whole mechanism of the formal (5,5,5,5,d) results. At all-6 no clause exists.

### 1.4 2-ball enumeration [computed]

Model:
- Enumerate proper colourings of the 15-vertex ball with the DL link fixed.
- Keep those with all four lock ends, the Jordan exclusions (Lock2 ⇒ x_{j+2} ≁ x_j in {α,A}; Lock1 ⇒ x_{j+2} ≁ x_j, x_{j+4} in {α,B}), and no closed local component that would contradict a lock.
- Successors: swap K. A local {α,A}-component of x_{j+2} that contains no ring vertex is exact. Otherwise branch the open ring components, which can only be m_{j+1} and m_{j+4}. Keep DL-feasible images.
- The core is the set of nodes with both a successor and a predecessor, iterated.
- σ is certified if σc is DL-infeasible in every branch.

Results:

| pattern | DL nodes (5 j's) | core | σ-certified in core | core avoiding certified | w-words on cycles |
|---|---|---|---|---|---|
| 55555 | 15 | 10 | 5 | **0** | 2 |
| 55556 | 23 | 10 | 2 | **0** | 2 |
| 55566 | 48 | 27 | 2 | 20 | 12 |
| 55666 | 95 | 67 | 2 | 59 | 22 |
| 55757 | 235 | 130 | 13 | 100 | 12 |
| 56566 | 108 | 63 | 2 | 56 | 22 |
| **66666** | **370 (74 per j)** | **370** | **0** | **370** | **32** |

Notes:
- F matched every computed transition at all 7 patterns.
- At 66666, 56 of the 74 words have one successor and 18 have two. The branching is m_{j+1} or m_{j+4} ∈ K, which is genuinely non-local.
- Adding the Jordan side condition (m_{j+1} can be in K only if w_j = B, and m_{j+4} only if w_{j+4} = μ) removes nothing, because it is already implied.
- Reading:
  - The model reproduces W(55555) and W(55556) from purely 2-ball facts plus Jordan at the hole. That matches how the Lean proofs work.
  - At (5,5,6,6,6), (5,5,7,5,7) and 66666 it certifies nothing, consistent with the census all-DL cycles at the first two.
  - The rotation-quotient graph at 66666 has SCCs of sizes 32, 21, 19 (period 10) and 2 (period 2). These are the F-orbits (a)–(c) refined by m-colours, and (d).

## 2. σ-exit at degree 6: X4(6) and X3(6) are vacuous [proved]

σ swaps K′ = K_{αμ}(x_{j+1}), which contains x_j and x_{j+2}. The link becomes (μ, α, μ, A, B) with repeat index j.

**Lemma X(6).** At a DL state at j with deg x_{j+3} = 6, x_{j+3} has an α-neighbour in σc. The same holds for x_{j+4} when deg x_{j+4} = 6.

Proof for x_{j+3}. Its outer path is w_{j+2} – m_{j+3} – w_{j+3}, with no colour A.
- If w_{j+2} = μ, it is adjacent to x_{j+2} ∈ K′, so it becomes α. Hence for no α-neighbour we need w_{j+2} = B.
- Then m_{j+3} ∈ {α, μ}, and w_{j+3} ∈ {α, μ} with w_{j+3} ≠ m_{j+3}. So one of them is α and the other μ, and they are adjacent.
- Adjacent α and μ vertices lie in the same {α,μ}-component. Either both are in K′ (the μ one becomes α) or both are out (the α one stays α).

Proof for x_{j+4}. Its outer path is w_{j+3} – m_{j+4} – w_{j+4}, with no colour B.
- w_{j+4} = μ would be absorbed via x_j, so w_{j+4} = A.
- m_{j+4} and w_{j+3} are then an adjacent {α, μ} pair, and the same argument applies. ∎

x_{j+1} keeps its A- and B-neighbours, since σ does not touch A or B. So **σc always has all four lock ends at an all-6 hole**, and a non-DL σ-image needs a chain cut outside the 2-ball.

At degree ≥ 7 the outer path can separate α from μ with B's (e.g. B, α, B, μ), so the route reopens, but only with non-local membership hypotheses. At degree 5 it is X4 of NightWeakForm.

The same parity argument should be run for σ′ and for the other α-pair swaps before Job BP's answer is read. I expect the same outcome for any swap whose seed is a link vertex, but have not checked it.

## 3. Candidate mechanisms and where each breaks

| # | mechanism | status | where it breaks |
|---|---|---|---|
| M1 | Six-pair identity Σr = ΣC − 8 and the six dualities (formal, pattern-free); bound component counts along DL runs | true, used | Identities hold at every DL state. Each DD step changes ΣC by an odd amount (`delta_rank_odd'`), which gives only 2 \| L. C(αA) and C(μB) are invariant on an {α,A}-step, and no other monotone quantity exists (NightClosedSets: 14 descents fail). Pattern-free, so it cannot exclude the all-DL cycles that exist at (5,5,6,6,6). |
| M2 | Sign of the Theorem W winding forced by planarity | = quarter floor | Σλ = 5·windingSum (Lean sign). An all-DL class has winding +N/5. "Winding ≤ 0 on the sphere" is `QuarterFloorConj` (`quarterFloor_iff_lam`) ⇒ R\* ⇒ 4CT. Per π-cycle the winding is +L/5 > 0 on Γ-cycles that exist on the sphere, so only class-level balancing can work. The winding is the lift of the ℤ/5 token (rotation of the repeat index; by §1.3 a ℤ/10 signed rotation of the w-word), not a curve's homology class, so Euler/orientation does not see it. |
| M3 | Closed DL run ⇒ frozen (torus-type) class | false as stated | `NoFrozen` is pointwise: every DL state on the sphere has C(αA), C(αB) ≥ 2. All-DL cycles on the sphere satisfy it at every state. What remains testable is whether **torus** targetless classes at 66666 always contain a state violating NoFrozen's conclusion (T5). |
| M4 | Pentagram crossing of lock chains [proved] | true, sphere-only | Q_n := the Lock2 chain at step n joins the diagonal {x_{j_n+1}, x_{j_n+4}} (the diagonal skipping x_{j_n}), with j_n = j₀ + 3n. Q_n shares an endpoint with Q_{n±1} and Q_{n±4}, and by Jordan meets Q_{n±2} and Q_{n±3}. Colours: Q_{n+2} ∩ Q_n consists of μ_n-vertices of Q_n not swapped at step n+1. This is satisfiable (census all-DL cycles on the sphere), so it is not a contradiction alone. It is the only sphere input found beyond `rot3Def`, and it is a candidate ingredient combined with degree data beyond the 2-ball. |
| M5 | Local (2-ball) σ-exit, X4(6) | vacuous | §2. |
| M6 | Fisk degree of the colouring of the disc T − star(h) into ∂Δ³ (Kempe behaviour of degree mod small numbers) [lit-L] | unexplored | Pattern-free, so by the argument for M1 it cannot kill all-DL π-cycles. It might constrain classes. Check the literature (Fisk; Mohar 2006, "Kempe equivalence of colorings") before spending time. |

**Structural conclusion.** Any proof of G66 must be one of:
- (i) non-local at the orbit level, with chain geometry beyond the 2-ball, for example M4 combined with degree-6 rings at radius 2–3;
- (ii) class-level, for example a counting or charge-back statement such as SigmaUnionC or B′ restricted to 66666;
- (iii) global use of the frame class.

The torus (101 of 196 66666 holes have targetless classes) shows that 3-ball data without Jordan cannot suffice. With Jordan, the 2-ball already fails (§1.4).

## 4. The conjecture and the tests

### 4.1 The ladder (strongest first)

- **G66⁰ (canary).** At every degree-5 vertex h with link (6,6,6,6,6), of every sphere triangulation of min degree 5 with no separating triangle (frame class first), there is **no all-DL π-cycle**. Census: 0 at orders ≤ 24 (273 classes). False on the torus.
- **G66^Γ (Lean plug-in).** `GammaImages P` at such h: every Γ-cycle has a state r with σr not DL. By §2 this needs a non-local cut. A weaker variant allows any single Kempe swap; by C1 that is equivalent to G66.
- **G66 (needed).** `PureClean T h` at every such h of every frame-class T: every Kempe class of T − h has a filled state. Together with discharging D (NightWeakForm §5), this gives `RStarFrame` ⇒ 4CT via `four_color_of_RStarFrame` and the unwritten one-line `rStarFrame_of_images`.
- **G66^IPR (necessary, weakest pattern-specific).** If every 5-vertex of a frame-class T has link (6,6,6,6,6) (IPR fullerene duals), some 5-vertex is PureClean. `RStarFrame` implies it.
- The weakest statement that implies R\* on the frame class is `RStarFrame` itself. G66 is the 66666 component of any link-pattern route to it.

### 4.2 Studio tests (Job BO is collecting run lengths and lock-death rules; BP the σ-analogue)

Data:
- every 66666 hole in the sphere census at orders ≤ 27;
- IPR fullerene duals at orders 32–80 (`studiointel/ipr`);
- an AW-protocol flip search with the hole star and all-6 link kept, objective the maximum DL-run length, with a frame-class variant that rejects flips creating a diamond, a 2.122 or a separating triangle.

Both orientations.

- **T1 (code check of §1.3, must be 100%).** On every DD step at any pattern, the w-bits move by F. The type of πc follows §1.2. Normalised all-DL cycle lengths are ≡ 0 mod 10. Any failure is a bug in this note or in the engine.
- **T2 (runs).** Collect at 66666:
  - the DL-run length distribution and maximum;
  - the w-orbit ((a)/(b)/(c)/(d)) and its phase at the run start and at the run end;
  - the number of all-DL π-cycles and their L.

  A sphere all-DL cycle kills G66⁰. Then run T4 on it.
- **T3 (lock-death rule).** At each run end (¬Lock2 at the last state), record:
  - the w-word;
  - m_{j+1}, m_{j+4};
  - the smallest radius r such that x_{j+4} and x_{j+2} are in different {μ′,B′}-components of the r-ball of h minus h, for πc.

  Prediction: no death is decided inside the 2-ball (r ≥ 3), since every 2-ball word has a DL successor. Report the distribution of r. A "lock-death rule" in terms of 2-ball colours alone would contradict §1.4 and should be treated as a census artefact.
- **T4 (σ-exits, Job BP).** For each DL state at 66666, record:
  - whether σc, σ′c and the other single swaps are DL;
  - which lock dies;
  - the cut radius.

  Prediction: lock ends are always present (Lemma X(6)), so every failure is a far cut. Then check GammaImages and PureClean on every class containing a Γ-cycle.
- **T5 (torus separation).** On the 101 torus 66666 holes with targetless classes, does every targetless class contain a DL state with C(αA) = 1 or C(αB) = 1 (impossible on the sphere by `NoFrozen`)? If yes, the sphere/torus gap is exactly NoFrozen-type, and the right target is a class-level statement "all-DL ⇒ some state with an α-pair graph connected". If no, the planarity input must be global (M4-type).
- **T6 (cheap, local).** Repeat the §1.4 model on the **3-ball** of an all-6 hole whose ring vertices also have degree 6 (hexagonal cone), and with one ring vertex of degree 5 (frame-allowed). Prediction: still no certification. If the 3-ball certifies anything, that is the first local lemma at 66666.

**Kill rules.**
- A sphere all-DL π-cycle at a 66666 hole kills G66⁰ only.
- A Γ-cycle whose σ-images are all DL kills G66^Γ (σ form).
- A 66666 class with no filled state on the sphere kills G66 and the link-pattern route through (6,6,6,6,6). It does not contradict 4CT.

### 4.3 Lean targets (cheap)

- `wword_step`: §1.3's F, at every pattern, from `rot3_values`, `rot3Def_of_lock2` and the five face adjacencies. Also `F⁵ = compl`.
- `x_fresh_alpha66`: Lemma X(6).
- `allDL_cycle_len_ten`: 10 ∣ L, from F and the repeat index. The absolute-colour version is 30 ∣ L.

## 5. Caveats

- The 2-ball model is an over-approximation: realisability of each word is not checked. "Nothing forced" claims are therefore safe; the 74-word count is an upper bound.
- The m-vertex branching treats m_{j+1} and m_{j+4} independently.
- The enumeration script is in the session scratchpad and is not committed. It has about 150 lines, and T1/T6 should re-implement it independently.
