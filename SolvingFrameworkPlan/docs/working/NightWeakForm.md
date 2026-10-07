# NightWeakForm: the weak (R*-type) form, link pattern by link pattern

Night worker, 7 October 2026 (written 05:23 MDT). **Exploratory. Hand analysis, one small re-aggregation of existing torus data. Unreviewed.**

Sources:
- NightPostAW; NightLog-2026-10-06 (from "05:03 — Studio Job AW" to the end);
- the Lean files `QuarterNonDLImage`, `QuarterSigmaK34`, `QuarterSigmaExit`, `QuarterGammaPeriod`, `QuarterFloorH`, `QuarterFloorHBridge`, `QuarterRotationPlanar`, `RStar`, `RStarCore`, `MinimalFrame`, `FrameF3`, `DiamondMCert`, `C2122MCert`, and `QuarterHole6Clean` (216b533c, which landed while this note was being written);
- NightConfigurationLead;
- `longtable/local-runs/27-link-patterns` (sphere census, orders 12–24) and `local-runs/18-torus-floor` (torus).

Labels: [formal] = in Lean, 0 sorry; [proved] = a complete hand argument here; [sketch] = a gap is named; [lit-H/M/L] = a literature claim, with high, medium or low confidence in my recollection of it; [data].

## 0. Bottom line

1. **W is a theorem exactly where it is useless for 4CT.**
   - W(5,5,5,5,6) is formal: `pureClean_of_hole6`. W(5,5,5,5,5) is formal: F5 and `pureClean_of_icoBall`.
   - Every pattern the σ-exit library can reach contains three cyclically consecutive degree-5 link vertices. That is the triple ball x_j, x_{j+1}, x_{j+2}, which the library needs in order to know the σ-component.
   - With the degree-5 hole h, these vertices form a **Birkhoff diamond**: centre edge h–x_{j+1}, tips x_j and x_{j+2}. The diamond is D-reducible, and that reducibility is already formal (`DiamondMCert`/`DiamondPCert`, used by `FrameF3.four_color_of_RStarFrame`).
   - So **(5,5,5,5,d), for every d, never occurs in a minimal counterexample.** Proving W at these patterns adds nothing that the frame does not already exclude.
2. **The coordinator's target is the same story.** "PureClean at every degree-5 vertex with ≥ 4 consecutive degree-5 neighbours", even if the K4Ball generalisation to deg x_{j+4} ≥ 6 goes through, is (a) vacuous on the frame class, and (b) avoidable on the bare class `RStarNoSepTri`.
   - (b) holds because the pentakis dodecahedron and the IPR fullerene duals have only (6,6,6,6,6) holes [proved; the pentakis case is already noted in `RStar.lean`].
   - So it cannot close 4CT by any unavoidability argument.
3. **The frame class** (`RStarFrame`: min degree 5, no separating triangle, no diamond or 2.122 occurrence) **forces every 5-vertex link pattern to avoid cyclic 555 and cyclic 565.**
   - Any link-pattern unavoidable set for this class must contain **(6,6,6,6,6)**, because IPR duals are configuration-free.
   - It must also contain patterns with **arbitrarily large entries** [sketch, §3.3].
   - The census shows all-DL π-cycles at two frame-compatible patterns, (5,5,6,6,6) and (5,5,7,5,7). So the open case is not empty.
4. **The smallest remaining gap** (§5) is W at (6,6,6,6,6) together with a frame-compatible unavoidable set. The library has *no* σ-exit lemma there: every existing one needs the triple ball. §2 gives the candidate replacement, which needs only **one** degree-5 link vertex plus a Kempe non-membership condition.

## 1. What is formal, and the exact degree hypotheses

### 1.1 The not-DL lemmas (`QuarterSigmaK34`)

Notation: R3 state at j, link (α, μ, α, A, B) at x_j..x_{j+4}, outer ring w_t (the common outer neighbour of x_t and x_{t+1}) = (B, A, B, μ, A).

| lemma | ball | degrees required |
|---|---|---|
| `sigma_exit_not_DL_k4` | `K4Ball` | x_j, x_{j+1}, x_{j+2} = 5 (`TripleBallP`), x_{j+3} = 5, x_{j+4} = **exactly 6** (`nbr4` lists 6 neighbours, with m) |
| `sigma_exit_not_DL_k3` | `K3Ball` | x_j, x_{j+1}, x_{j+2} = 5, x_{j+4} = 5, x_{j+3} = **exactly 6** |
| `locks_die_of_deg5` (`QuarterSigmaExit`) | `IcoBallP` | all five = 5 |

**Proof inspection** [proved by reading; not re-compiled]:
- `sigma_exit_noLock1_k4` uses only `K.tri`, `K.nbr3` and the R3 colours e2, e3. It never uses `nbr4`, `m` or the ring through m.
- `sigma_exit_noLock2_k3` uses only `K.tri` and `K.nbr4` (x_{j+4} of degree 5).
- So, with a K4Ball weakened to drop `nbr4`, `ring3m`, `ringm4` and `offm` (and the K3 mirror likewise), **the not-DL conclusion holds whenever four cyclically consecutive link vertices x_j..x_{j+3} (k = 4), or x_{j+4}, x_j, x_{j+1}, x_{j+2} (k = 3), have degree 5. The fifth degree d is arbitrary.**
- This is the Lean agent's generalisation, and it is easy *for the exit lemma*.
- It is **not** easy for the orbit part. `r1_step`/`tk_step`, `untyped_dd` and `pair_R3k4_of_pred` all use `Hole6` (one degree-6 vertex). For d ≥ 7 the type transition table has to be re-derived. Job BA (a) found that non-fixed R3 images at k = 3, 4 are never DL at degree 7, which is consistent with this.

### 1.2 Which patterns P have W(P) as a theorem

| P (cyclic) | status | route |
|---|---|---|
| (5,5,5,5,5) | **formal** (F5 floor; `pureClean_of_icoBall`) | `dd_r3` + `sigSwap_spec` |
| (5,5,5,5,6) | **formal** (`pureClean_of_hole6`, 216b533c) | `typed_in_orbit` → R1k2 → R3k4 → `sigma_exit_not_DL_k4` |
| (5,5,5,5,d), d ≥ 7 | exit lemma OK by §1.1; orbit part **open** | needs a Hole-d transition table: does every all-DL orbit visit R3 at k ∈ {3, 4}? |
| everything else | **nothing**; no lemma applies | §2 |

**Answer to "does tk_step hold for all-DL orbits at any pattern?"** No.
- `r3_step` (R3 → R1 at j + 3) is pattern-free.
- `r1_step` (R1 → R3) uses `Hole6` through `r1_ring`, which needs x_{j+1}, x_{j+3} and their rings to be degree-5-like.
- `untyped_dd` (no R2-type DD state at k ∈ {0, 4}) uses the degree-5 rotation at x_{j+2}. This is exactly the IcoBall R2-kill of `dd_r3`.
- At a general P none of these hold. Also, the R1/R2/R3 trichotomy itself (`ring_type`) is proved only with an `IcoBallP` or `Hole6` ring.

**Topology check** [data, re-aggregated here from `18-torus-floor`]:
- On the torus, 529 of 960 (5,5,5,5,6) holes and 438 of 827 (5,5,5,5,5) holes have a targetless class.
- So the formal sphere proofs must use planarity, and they do: π's definedness on Lock 2 states is `rot3Def_of_lock2` (`QuarterRotationPlanar`, Jordan), and `dd_ends`/`tk_step` go through it.
- So the period/typing part of the argument carries the topology. The local exit lemma is planarity-free.

## 2. Beyond the triple ball: what local condition makes a σ-image non-DL

σ = `sigSwap` swaps K := K_{αμ}(x_{j+1}). That component always contains x_j and x_{j+2}. After the swap the link is (μ, α, μ, A, B), and the repeat index is still j (unique). So σc is DL iff it has Lock 1 ({α,A}: x_{j+1} → x_{j+3}) and Lock 2 ({α,B}: x_{j+1} → x_{j+4}) at j.

### Candidate Lemma X4 (one degree-5 vertex, k = 4 side) [proved by hand, not formal]

Let c be doubly locked at j, with deg x_{j+3} = 5, so its outer neighbours are exactly w_{j+2} and w_{j+3}. Suppose:
- c(w_{j+2}) = B;
- c(w_{j+3}) = μ;
- w_{j+3} ∉ K_{αμ}(x_{j+1}) in c.

Then σc has no Lock 1 at j, so σc is not DL.

*Proof.*
- In σc the neighbours of x_{j+3} are:
  - h (deleted);
  - x_{j+2}, now μ;
  - x_{j+4} = B;
  - w_{j+2} = B (untouched: not in {α, μ});
  - w_{j+3} = μ (untouched: it is not in K).
- None of these has colour α, so x_{j+3} is isolated in the {α,A}-graph of σc and cannot be reached from x_{j+1}. ∎
- Forced colours: w_{j+2} is adjacent to x_{j+2} (α) and x_{j+3} (A), so it lies in {μ, B}. If it were μ it would lie in K and turn into α. So the hypothesis c(w_{j+2}) = B is necessary for this route. Similarly w_{j+3} ∈ {α, μ}.

### Candidate Lemma X3 (mirror)

Let c be doubly locked at j, with deg x_{j+4} = 5. Suppose c(w_{j+4}) = A, c(w_{j+3}) = μ, and w_{j+3} ∉ K. Then σc has no Lock 2, so σc is not DL.

### How these relate to the existing lemmas

- **No degree is assumed at x_j, x_{j+1}, x_{j+2}.** The triple ball was used only to make K equal to the triple {x_j, x_{j+1}, x_{j+2}}. That makes "w_{j+3} ∉ K" automatic and identifies the R3 ring. X4/X3 replace that with the one non-local hypothesis.
- **Ball needed:** one link vertex of degree 5, at position j+3 (X4) or j+4 (X3), with its two outer neighbours. Nothing else is local.
- **Two consecutive degree-5 link vertices do not help by themselves.** The only role of degree 5 at x_{j+1} or x_j is to stop K from growing through *their* outer neighbours. K can still reach w_{j+3} from far away. "Two" or "three" consecutive 5s matter only in that they bound K. Three already make a diamond.

### A sufficient Jordan condition for w_{j+3} ∉ K [sketch]

Suppose x_{j+3} and x_{j+4} are joined in c by an {A,B}-path Q that avoids the edge x_{j+3}x_{j+4}. Then the closed curve h–x_{j+3}–Q–x_{j+4}–h separates the face x_{j+3}x_{j+4}w_{j+3} from x_{j+1}, and an {α,μ}-chain cannot cross an {A,B}-chain. So w_{j+3} ∉ K.
- *Gap:* which side w_{j+3} lies on must be checked against the rotation at x_{j+3}/x_{j+4}.
- This is a Kempe-duality condition of the type of (D) in `QuarterSigmaK34` (not formalised).

### The second missing piece: orbit visiting

X4 still needs the all-DL orbit to visit a state where the hypotheses hold. That means a DL state at j with x_{j+3} of degree 5 and the ring colours (B, μ) on w_{j+2}, w_{j+3}. At (6,6,6,6,6) **no link vertex has degree 5, so X4/X3 are vacuous there as well.**

At an all-6 link the σ-exit route therefore needs a statement of a different kind. Lock 1 of σc must be broken by an α-free neighbourhood of x_{j+3} in σc:
- x_{j+3} has three outer neighbours u₁, u₂, u₃ (from x_{j+2}'s side to x_{j+4}'s);
- u₁ ∈ {μ, B} and u₃ ∈ {α, μ}.
- The condition is: no outer neighbour of x_{j+3} is α in c, and every μ outer neighbour of x_{j+3} lies outside K.

Call this **Lemma X4(6)** [conjecture; not tested].

## 3. Unavoidability

### 3.1 What R* lets us choose

There are three bridges:
- `RStarNoSepTri`: any degree-5 v, in every connected triangulation with min degree 5 and no separating triangle.
- `RStarCore`: v off the protected face; the face vertices may have any degree.
- `RStarFrame` (`FrameF3`): as `RStarNoSepTri`, but only for triangulations that are **`Occ`-free for the diamond and 2.122 in both orientations**.

`rStarNoSepTri_of_images` and `rStarNoSepTri_of_hole6` exist. A `rStarFrame_of_images` bridge is a one-liner (`rStarFrame_of_noSepTri` shows the shape) and is not yet written.

Caveat from `FrameF3`: "Occ-free" is the ring-embedded occurrence. The passage from "the subgraph appears" to an `Occ` is **not formalised**. So the link-pattern consequences below are hand facts [proved for the configuration; the Occ bridge is open].

### 3.2 Link-pattern consequences of the frame [proved, modulo the Occ bridge]

From the certificates:
- **Diamond:** interior degrees 5,5,5,5; centre edge 0–2, tips 1 and 3.
- **2.122:** centre 0 has degree 6, and vertices 1, 2, 3 have degree 5; centre edge 0(6)–2(5), tips 1 and 3.

At a 5-vertex h with link x_1..x_5:
- three cyclically consecutive degree-5 vertices give a diamond with centre edge h–x_t;
- consecutive (5, 6, 5) gives a 2.122 with centre edge h(5)–x_t(6).

So **in the frame class every 5-vertex pattern avoids cyclic 555 and cyclic 565.** These two conditions see only configurations in which h is a centre. Configurations with h as a tip constrain the second ring.

### 3.3 Unavoidability table

| statement (planar triangulation, min degree 5) | source | confidence | use here |
|---|---|---|---|
| some 5-vertex is adjacent to a 5- or 6-vertex | Wernicke 1904 | lit-H | too weak: it fixes one entry |
| some 5-vertex has two neighbours of degree ≤ 6 | Franklin 1922 | lit-H (the statement); lit-M (whether the two are consecutive: I believe not required) | fixes two entries |
| some face has weight ≤ 17, i.e. type (5,5,≤7) or (5,6,6); sharp | Borodin 1989 (Kotzig/Grünbaum light-face problem) | lit-M | gives a 5-vertex h with **consecutive** link pair in {(5,5), (5,6), (5,7), (6,6)} |
| precise lists of light 5-stars (all five neighbour degrees bounded in some listed pattern) | Lebesgue 1940; Borodin–Ivanova(–Jensen), ~2013–2016 | lit-L | do not cite without checking; see the next row |
| every link-pattern unavoidable set contains (6,6,6,6,6) | IPR fullerene duals; pentakis dodecahedron (`RStar.lean`) | proved | in the frame class too (isolated 5-vertices form no configuration) |
| no finite list of full link patterns is unavoidable (entries can be unbounded) | hub construction: a vertex of large degree D whose link is all 5-vertices; each has pattern (5, D, 5, a, b) | sketch (global existence not checked) | if true, "5-stars are not light" and the target must be uniform in large degrees |
| minimal counterexample: no 5-vertex has three consecutive 5-neighbours (diamond, Birkhoff 1913) and none has (5,6,5) consecutive (RSST 2.122) | Birkhoff 1913; RSST 1997 | lit-H; **formal** in the library (certificates + `FrameF3`) | kills (5,5,5,5,d) and (5,5,5,5,5) |
| census, orders 12–24: only 6 of 9,912 graphs are configuration-free | NightConfigurationLead | data | the frame class is thin at small orders; it is not empty |

### 3.4 Matching against W

| pattern family | W status | occurs in the frame class? |
|---|---|---|
| (5,5,5,5,5), (5,5,5,5,6) | formal | **no** (diamond) |
| (5,5,5,5,d), d ≥ 7 | exit formal-able; orbit open | **no** (diamond) |
| any cyclic 555 | open | **no** |
| any cyclic 565, e.g. (5,5,6,5,6), (5,6,5,6,6) | open | **no** (2.122) |
| (6,6,6,6,6) | open; X4/X3 vacuous | **yes, and forced** (IPR duals) |
| (5,5,6,6,6), (5,5,7,5,7), (5,5,6,6,7), … | open; X4/X3 apply only with the Kempe hypothesis | yes; all-DL π-cycles exist in the census at 55666 (1) and 55757 (1) |

**Is there a combination "unavoidable C + W at C's 5-vertex" that closes 4CT?**
- Not with anything formal now.
- The minimal closing statement has the form below. Let U be an unavoidable set of 5-vertex link patterns for the frame class. Proving it is a discharging argument; Borodin's weight-17 face plus the 555/565 exclusions narrows the consecutive pairs.
- U must contain (6,6,6,6,6).
- Then **W(P) is needed for every P ∈ U.** If U has unbounded entries, a W uniform in high degrees is needed.
- The discharging part is classical and finite-checkable. The W part is new and at 4CT strength for (6,6,6,6,6) alone in the following sense: R* restricted to triangulations whose 5-vertices are all (6,6,6,6,6) is not known to be easier than R*.

## 4. Torus test: which patterns have counterexamples

Re-aggregation of `local-runs/18-torus-floor` (1,723 graphs, 17,696 holes, 86,175 classes; script in the scratchpad, not committed) [data]:
- **Every pattern with at least 3 holes has a hole with a targetless class.** Only 5 rare patterns have 0: 68778 (2 holes), 88888 (2), 67768 (1), 67868 (1 of 3), 67688 (1 of 3).
- These include:
  - 55555: 438 of 827 holes;
  - 55556: 529 of 960;
  - 66666: 101 of 196;
  - 55666: 369 of 644;
  - 55757: 36 of 62.
- A targetless class is all-DL (C1 is graph-only), so W fails on the torus at all of these patterns, including the two where it is formal on the sphere.

Reading:
- **No pattern-local statement can prove W.** The sphere enters through π's definedness (`rot3Def_of_lock2`, Jordan) and the orbit/typing lemmas. The exit lemmas (`sigma_exit_not_DL_k4`, X4) are planarity-free.
- Any proof of W(6,6,6,6,6) must contain a Jordan or Euler step at the orbit level, not only at σ.
- Caveat: the torus sample consists of random flips from lattices, and its 5-vertices sit next to 7s and 8s more often than on the sphere. Pattern frequencies are not comparable to the sphere census.

## 5. The smallest remaining gap

Exact statement:

> **Gap G66.** Let T be a spherical triangulation with min degree 5, no separating triangle, and no diamond or 2.122. At a degree-5 vertex h with link (6,6,6,6,6), every all-DL π-orbit contains a doubly locked state r whose σ-image (or some other single Kempe swap) is not doubly locked.

Together with:

> **Discharging D.** Every such T has a 5-vertex whose pattern lies in a set U with W(P) proved for every P ∈ U.

G66 + D (with U = {66666} ∪ the rest) ⇒ `RStarFrame` ⇒ 4CT, via `four_color_of_RStarFrame` and a one-line `rStarFrame_of_images`.

G66 is necessary for the link-pattern route (IPR duals). It is not sufficient: D also needs W at every other pattern in U. Neither the σ-exit library nor the period table applies at an all-6 link. The first concrete steps are:
1. Studio: tabulate all-DL π-orbits at 66666 holes. The census has 0 at orders ≤ 24 (273 classes). Use IPR duals of order 32–52 (`studiointel/ipr`) and flip searches. If none ever appears, the target is "no all-DL orbit at 66666", which is stronger and easier to test.
2. Hand/Lean: the Hole-6⁵ transition table, the analogue of `tk_step`, and Lemma X4(6).
3. Literature: verify Borodin 1989 and the Borodin–Ivanova light-5-star results before citing; decide whether a finite U exists for the frame class.
