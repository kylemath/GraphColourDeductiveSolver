# SCOPE-A5v: how much of LPC can an A5v-type local Jordan fact reach?

Long Table (scope lead), 13 Oct 2026, about 90 minutes, written up by 13:06 (clock). Exploratory. Labels:
**[data]** = computed here (scripts in this folder); **[hand]** = argument written here, not reviewed;
**[conjecture]**. Other tracks' files were read only (TrackH `th_engine`, TrackT `tt_lib`, axioms `ax_lib`).
Compute: at most 3 processes, `nice -n 10`, each run under 15 minutes, on AC power.

## 0. Verdict

1. **A5v in primal language is "π is defined": x_j ∉ K_{αA}(x_{j+2}) (¬inA).** [hand] At a DL state the
   far end of v's M-edge is the triangle (x_{j+2}, x_{j+3}, w) across the link edge x_{j+2}x_{j+3}. The
   Tait loops X and Y lie in the interfaces E(K, J) and E(K0, J). That triangle is on X's side unless
   x_{j+2} is P2-linked to x_j (inA) or to x_{j+1}, and the second is impossible for a vertex colouring.
   The proof (Lemma F, §2) uses only the corner structure of a cellular embedding. **No Jordan curve
   theorem is used.** All of the Jordan content sits in "¬inA", the D2 half of the hole duality.
2. **The dictionary is exact on sphere data** [data]. Primal and Tait forms agree at **323,186 / 323,186**
   sphere DL states: plantri24 every 20th graph, the 25 Census33 all-DL-cycle holes, and C30#0 h0/h16.
3. **Off the sphere, A5v is "liftable + ¬inA", not a surface fact** [data]. On the Tait duals of RP²,
   torus and Klein-bottle triangulations (420 holes), A5v fails at 5,659 DL-good matchings:
   - Every failure has x_{j+2} P2-face-linked to x_j or to x_{j+1}, as Lemma F predicts (0 exceptions).
   - At the 27,953 integrable (genuinely primal) states it fails **exactly at D2 violators**: 220 failures
     on torus/Klein, all with inA; 0 failures among the 27,351 states with ¬inA.
   - The other 5,439 failures are at non-integrable Tait colourings.

   This corrects Run 1's reading of A5v as a "local Jordan fact" true on RP²/Klein. It held on Run 1's
   six seed holes only because those states lift and have ¬inA.
4. **Task 3 answer: no.** The known frozen objects are two disjoint kinds of fake:
   - *Cubic fakes* (TrackU T1, 939 orbits) have no primal near v, and they violate A5v at every state.
   - *Primal fakes* (TrackH, TrackJ) have no dual surface. They satisfy A5v-primal at every state,
     necessarily, because π is defined along a π-cycle (TrackH Lemma H0).

   So **"law + lock parity + A5v ⇒ no frozen class" is false.** The 43 TrackJ rung-d graphs each carry a
   frozen 20-state class on which all of the following hold:
   - the chain-parity law (860/860 steps);
   - lock parity P1–P3 and D1/D2 at every state;
   - A5v-primal at every state (non-vacuous at 844/860);
   - every edge lies in a triangle, H3 holds, and the graph is 4-colourable.

   What these graphs violate is **surface structure**: at least 57 edges of G − h are not in exactly two
   triangles, and at least 27 vertex links are not cycles. That is the "dual exists" property, which the
   cubic abstraction has built in.
5. **Scope map (§6).**
   - A5v cannot reach the rest of LPC.
   - Its whole role is to make the cubic abstraction locally liftable at v, so that T1-v (law + A5v ⇒ no
     R-cycle) is a meaningful stand-in for NRC.
   - NRC closes near-rigid LPC only. The open part of LPC, the "mixed higher chain counts", has no
     matching-form (cubic) formulation without face data. In the primal form, every hole-local fact,
     A5v included, holds on the known frozen classes.
   - The planar input that is still missing is non-local: the law plus genuine surface or genus-0
     structure.

## 1. Dictionary: Tait (matching form) ↔ primal (Kempe chains) [hand]

Frame j, rim (α, μ, α, A, B) at x_j…x_{j+4}. Colours are elements of Z₂², and the Tait colour of a dual
edge is c(u) + c(w). Then 1 = α+μ = A+B (partition P1), 2 = α+A = μ+B (P2), 3 = α+B = μ+A (P3). The v-edges
e_i = f_{j+i} carry the colours (1,1,2,1,3), and k = j + 2.

| Tait object (TrackS / axioms) | primal object (any graph with a hole) |
|---|---|
| v, f_i | the hole h (pentagon face) and the link edge x_i x_{i+1} |
| M_t = colour 2 | P2(c) = E(αA) ∪ E(μB) |
| M_{t−1} = colour 3 | P3(c) = P2(π⁻¹c) (TrackJ J2) |
| Q = E − M_t (F13) | P2-cross edges = ⊔ over (αA-comp C, μB-comp C′) of the interface E(C, C′). Each {1,3}-cycle lies in a single interface (a cubic vertex is a triangle with two vertices in one class, which are P2-adjacent). On the sphere each nonempty interface is exactly one cycle |
| X (even v-loop, through f_{k±1}) | inside E(K, J), with K = K_{αA}(x_{j+2}) ∋ x_{j+3} and J = K_{μB}(x_{j+1}) ∋ x_{j+4} (Lock 2) |
| Y (odd v-loop, through f_{k±2}) | inside E(K0, J), with K0 = K_{αA}(x_j). TrackS S5: Y = δK0 when P2 = (2,1) |
| Q connected (DL-good) | on the sphere ⇔ P2 = (#αA, #μB) = (2,1) |
| v's M-edge f_k | the link edge x_{j+2}x_{j+3}, the only P2 edge of the link, which lies inside K |
| far end p of f_k | the triangle (x_{j+2}, x_{j+3}, w), with w ∈ {μ, B} |
| π: M_{t+1} = M_{t−1} Δ Y_t | π = swap K. In Tait form, switch the curve system C = δK (TrackS S1), which is X plus the cycles of δK not through v |
| parity form \|M ∩ E(X,Y)\| odd | the P2 edges inside J whose two triangles have apexes in K and in K0 |

## 2. A5v-primal: statement and proofs

**Definition (A5v-P; any graph G, hole h, no embedding).** At a DL state c with frame j:

  A5v-P(c): the P2-component of x_{j+2} contains neither x_j nor x_{j+1}.

For a vertex colouring this is exactly **x_j ∉ K_{αA}(x_{j+2})**, i.e. ¬inA, i.e. "π(c) is defined". The
x_{j+1} clause is automatic, since x_{j+1} has colour μ and K contains only α and A.

**Generalisations to every N (Q may have extra cycles Z).** Let p be the far end of f_k.
- **A5v-w:** p ∉ Y. This is the right generalisation: true on the sphere at every DL state.
- **A5v-π:** M_{t+1}(p) = M_{t−1}(p), i.e. p lies on the curve system that π switches. It is defined from
  the dynamics alone. When Q is connected it equals A5v. [hand]: by S1, p ∈ C ⇔ the colour-3 edge of c at
  p is the colour-2 edge of π(c) at p.
- **A5v-s:** p ∈ X. **This is not a valid generalisation.** On the sphere it fails at N ≥ 10 states
  whenever the apex w lies in a μB-component J′ ≠ J that K encloses: 24% of sphere DL states, and 26 of
  the 500 Census33 cycle states. Then p lies on a cycle Z ⊆ δK not through v.

In primal terms, given a triangle across x_{j+2}x_{j+3}:
- A5v-w ⇔ A5v-P;
- A5v-π always holds, because x_{j+2}, x_{j+3} ∈ K and w ∉ K;
- A5v-s ⇔ w ∈ J, provided E(K, J) is a single curve (true on the sphere).

**Lemma F (faces; any cellular embedding of the cubic graph on any surface, integrable or not)** [hand].
Call the faces (= primal vertices) P2-linked if they are joined by a chain of faces, consecutive ones
sharing a colour-2 edge. Suppose the P2-face-component of x_{j+2} contains neither x_j nor x_{j+1}. Then
the far end p of f_k is not on Y.

*Proof.*
- At a cubic vertex q with Q-edges a, b and colour-2 edge c, the three faces are: the face in the
  corner (a, b), and the two faces on either side of c. The last two share c, so they are P2-linked.
- So, walking along a Q-trail, the face on each local side changes only to a P2-linked face. All
  side-faces of one trail therefore lie in at most two P2-face-components, one per local side; a
  one-sided trail gives a single component.
- Y leaves v by e_0, with faces x_j and x_{j+1} beside it, and returns by e_4, with faces x_{j+4} and x_j
  beside it. So every side-face of Y lies in comp(x_j) ∪ comp(x_{j+1}).
- The faces at p are x_{j+2}, x_{j+3} (the two sides of e_2 = f_k) and one more face. x_{j+2} is a
  side-face of the trail through p.
- If p ∈ Y, then comp(x_{j+2}) ∈ {comp(x_j), comp(x_{j+1})}. ∎

**Corollary (sphere, and any surface at a lifted state)** [hand]. Let c be a vertex 4-colouring at a DL
state with ¬inA. Then:
- comp(x_{j+2}) = K;
- K does not contain x_{j+1}, which has the wrong colour class;
- K does not contain x_j, by ¬inA.

So A5v-w holds, and A5v holds whenever Q is connected. On the sphere, ¬inA holds at every DL state (D2:
Jordan, or Theorem P plus planarity), which gives A5v at every sphere DL state. Along any all-DL π-cycle,
in any graph, ¬inA is automatic (π is defined; H0). **Run 1's Jordan argument is therefore not needed:
the Jordan input is exactly D2.**

**Corollary (cubic fakes)** [hand]. If a matching-form state violates A5v, then in **every** cellular
embedding the face x_{j+2} is P2-linked to x_j or to x_{j+1}. Such a state is never the Tait dual of a
primal state at which π is defined, on any surface. So the T1 orbits, which violate A5v at every state,
are not matching forms of primal π-cycles on any surface.

## 3. Consistency with the Tait version [data]

Script: `a5v_primal.py`. It uses the primal engine TrackH `th_engine` and builds the Tait dual with TrackT
`tait_dual`. The connected case is checked with the independent axioms engine `ax_lib` (`dl`,
`fig8_axioms`); the general location of p is computed with a separate trail walk.

| data | holes | DL states | primal ↔ Tait (A5v-P ↔ p∉Y; w∈J ↔ p∈X) | p on X / Z / Y | ax_lib A5v (Q connected) | A5v-π | inA |
|---|---|---|---|---|---|---|---|
| C30#0 h0, h16 (Q-cycle, word 3232…) | 2 | 60 | 60 / 60 | 60 / 0 / 0 | 60 / 60 | 60 / 60 | 0 |
| plantri24, every 20th graph (`out/sphere_plantri24_s20.txt`) | 5,618 | 302,541 | 302,541 / 302,541 | 229,317 / 73,224 / **0** | 114,305 / 114,305 | 302,541 | 0 |
| Census33, all 25 all-DL-cycle holes (`out/census33_a5v.txt`) | 25 | 20,585 (500 on cycles) | 20,585 / 20,585 | 16,156 / 4,429 / **0** (cycle states: 474 / 26 / 0) | 4,748 / 4,748 | 20,585 | 0 |

Census33 cycles: the chain-parity law has 0 violations in 500 steps. Most cycle states have N ≥ 10 (the
N-words in the log).

**Off the sphere: Lemma F and liftability** (`facelemma` and `surfpm` modes). These runs use every DL-good
perfect matching of the Tait dual, as in Run 1's `sphere_check`, so they include Tait colourings that do
not come from a vertex colouring.

| data | holes | DL-good matchings | integrable: ¬inA (A5v ok / fail) | integrable: inA (A5v ok / fail) | non-integrable A5v failures | failures with x_{j+2} ~ x_j / ~ x_{j+1} | Lemma F violations |
|---|---|---|---|---|---|---|---|
| TrackH test beds (7 RP² + 4 sphere; `out/facelemma_testbeds.txt`) | 170 | 31,584 | 15,912 / **0** | none | 1,060 | 0 / 1,060 | 0 of 24,506 |
| TrackJ RP² graphs, every 25th (`out/facelemma_rp2_s25.txt`) | 132 | 22,086 | 6,660 integrable, A5v failures among them **0** | (not split) | 1,164 | 0 / 1,164 | 0 of 15,057 |
| TrackJ torus/Klein graphs, every 6th (`out/facelemma_torusklein_s6.txt`) | 118 | 58,484 | 5,527 / **0** | 382 / **220** | 3,215 | 1,459 / 2,713 (some both) | 0 of 26,244 |

Reading [data]:
- **Lemma F has no exception.**
- At genuinely primal (integrable) states, A5v fails **only** at D2 violators (inA). Off the sphere these
  exist at DL-good states, 602 of them on torus/Klein.
- Every other failure is a Tait colouring that is not a vertex colouring: x_{j+2} is P2-face-linked to
  x_{j+1} through a one-sided route.
- Run 1's 1,672 RP²/Klein states contained neither kind.

So A5v = (liftable at v) ∧ ¬inA, as the dictionary predicts.

## 4. Test table: every frozen or cycle object on disk [data]

"A5v-P" counts states where it holds / states; "vac" = states with no triangle across x_{j+2}x_{j+3}.
"Surface defects" = edges of G − h not in exactly two triangles (one for link edges) / vertices whose link
is not a cycle. LP = lock parity P1–P3, i.e. odd K_{αA}, K_{αB}, K_{αμ} counts. Logs are in `out/general_*.txt`.

| object | world | classes / states | filled in class | N | law viol / steps | LP | D1, D2 | A5v | surface defects |
|---|---|---|---|---|---|---|---|---|---|
| TrackU T1 orbits (Run 1: n22, coll_t1, walks, t1_first) | cubic | 939 orbits | n/a | (1212 words) | 0 | n/a | n/a | **fails at every state** | (dual exists, no primal) |
| TrackH `lp_general_min` (n = 28, χ = 5) | primal | 1 / 10, rigid | **0** | 8 | 10 / 10 | 10/10 | 10/10 | A5v-P 10/10 (vac 0), w ∈ J 10/10 | 66 / 27 |
| TrackH `lpc_general_min` (n = 21) | primal | 1 / 10, rigid | **0** | 8 | 10 / 10 | fails | 10/10 | 10/10 (vac 2) | 37 / 20 |
| TrackH `lpc_general_40` (n = 28) | primal | 1 / 40 (two 20-cycles) | **0** | **10 at all 40**; P2 ∈ {(2,1),(2,2),(3,1)} | 40 / 40 | fails | 40/40 | 40/40 (vac 8) | 71 / 27 |
| TrackH `lp_general_cex` / `lpc_general_cex` (unminimised) | primal | 1 / 10 each | **0** | 8 | 10 / 10 each | holds / fails | all | 10/10 each | 66 / 27 and 70 / 27 |
| TrackH `cex_free` / `cf_ball_cex` | primal | 12 / 11 (10 on the cycle, plus violators) | 0 | 8–9 | 8 / 10 each | fails / holds on the cycle | all on the cycle | 10/10 each | 80 / 29 and 57 / 25 |
| **TrackJ rung d** (43 graphs, n = 34–38) | primal | 43 / 860 | **0** | 8,9 alternating | **0 / 860** | **860/860** | 860/860 | **860/860 (vac 16)**, w ∈ J 860/860 | ≥ 57 / ≥ 27 (excess 27–33) |
| TrackP law R-cycles (193 graphs, all `ex_*`) | primal | 1,930 cycle states | 16 filled-free classes, all with violators | 8,9 | 0 / 1,930 | not all | all | 1,930/1,930 (vac 316) | ≥ 43 / ≥ 24 |
| TrackQ e = 1 law cycle (n = 29) | primal | 10 | > 0 | 8,9 | 0 / 10 | – | all | 10/10 | – |
| C30#0 h0/h16 Q-cycle (sphere) | both | 100-state class, 20-cycle | 40 | 9,10 | 0 / 20 | yes | yes | 20/20, p ∈ X | 0 / 0 |
| Census33 all-DL cycles (sphere, 25) | both | 500 cycle states | > 0 | mostly ≥ 10 | 0 / 500 | yes | yes | A5v-w 500/500; p ∈ X 474/500 | 0 / 0 |
| TrackF §8–9 off-sphere all-DL classes | both | 2,772 violator-free cycle classes | **all > 0** (no frozen class exists) | – | – | – | – | at cycle states π is defined, so A5v holds (Lemma F; tables in §3) | 0 / 0 |

TrackJ "rung d" has every edge of G − h in at least one triangle and H3 at every state, and G is
4-colourable (TrackJ README). Here, all 43 classes were re-checked by `th_engine`: class size 20, 0 filled.

## 5. Decision (task 3)

**Does every known frozen class contain a state violating A5v or its generalisation? No.**
- Every frozen class in the primal abstraction satisfies A5v-P = A5v-w at every state. This is forced:
  π is defined along an all-DL π-cycle (H0).
- Every frozen object in the cubic abstraction (T1) violates A5v at every state.
- No frozen class is known on any surface (TrackF §8–9, five surfaces, 1.1M evaluations).

So the two abstractions fail in complementary ways. Cubic fakes lack a primal near v, which A5v detects.
Primal fakes lack a dual surface, which A5v cannot see.

**The candidate "law + lock parity + A5v ⇒ no frozen class" is false as a statement about graphs with a
hole.** The 43 TrackJ rung-d classes satisfy all three, plus D, triangles, H3 and 4-colourability.
- It survives only in the cubic abstraction, where it is open beyond n = 22 for R-cycles (T1-v).
- Even there, it cannot be stated for general LPC from matching data. At N ≥ 10 states Q is usually
  disconnected, so the state is not determined by M (TrackS S3d). No Census33 cycle is a Q-cycle, and at
  most 13 of 20 states on a cycle have Q connected (TrackS §2.2).
- At such states the π-switch C = δK is not determined by Tait data, because it needs faces.

Plausibility as a 4CT-strength statement: **low as stated; and as a planar input, A5v is empty.** Lemma F
shows A5v is implied by "faces + ¬inA", so in any setting with faces it adds nothing to D2.

**What extra fact the frozen classes violate.**
- TrackH 28-vertex class: the chain-parity law (rigid → rigid at 10/10 steps), H3, and surface structure.
- TrackJ rung-d classes: among everything checked, **only surface structure** (law, LP, D, A5v,
  triangles and H3 all hold).

So the next "Jordan-type" fact needed is not at v. It is that G − h is a triangulated surface, i.e. the
dual exists, together with the law, which is the sphere-only input. Both are non-local.

## 6. Map: NRC, LPC and A5v

| piece | status | what closes it | does A5v help? |
|---|---|---|---|
| rigid LPC (classes of rigid states only) | **formal** (RI, `ChainF.lean`) | chain-parity law | no (not needed) |
| near-rigid LPC (all class states DL on π-cycles with N ≤ 9) | open; equivalent on the sphere to NRC (TrackJ J5) | NRC. Route: T1-v in the cubic world + TrackS S3 + the law ⇒ NRC | **yes, as the liftability axiom that makes the cubic search faithful.** T1-v is UNSAT for n ≤ 22 (Run 2). Its planar content is the law plus cubic (surface) structure, not A5v |
| mixed higher chain counts (frozen classes with some all-DL cycle states at N ≥ 10) | open; the only LPC case not covered by NRC. Every known sphere all-DL cycle is of this type (25 at order 33, 98 at order 34), always in classes with filled states | needs a class-level argument (Kempe moves beyond π: σ-exits, TrackH §3) | **no.** In primal form, A5v-P holds on all known frozen classes, including the N = 10 class `lpc_general_40`. In cubic form the dynamics is not defined without faces |
| LPC off the sphere | no counterexample (TrackF) | – | A5v holds at every lifted state with ¬inA, which includes every π-cycle state (Lemma F + H0); no content |

**What NRC (if proved) closes:** exactly the near-rigid shapes. These include every rigid or 8/9 shape
found in general graphs (TrackH rigid 10-cycles, TrackJ 8/9 20-cycles, TrackP/Q law cycles), all of
which would be impossible on the sphere. It says nothing about classes whose cycles visit N ≥ 10.

**What remains of LPC:** the mixed case. There, primal frozen fakes exist even with N = 10 at every
state (`lpc_general_40`; it fails the law and LP, so it is not yet a full analogue). The useful next
question for that case is the TrackJ-style ladder at N ≥ 10:
- does a primal frozen class with law + LP + D exist that has states at N ≥ 10?
- if so, which local surface condition kills it?

**Recommendations.**
1. **Sharp falsification test of T1-v from the primal side.** Search primal law R-cycles (TrackJ/TrackP
   engines) in graphs whose G − h is a triangulated *pseudo-surface*: every edge in exactly two triangles
   (one for link edges), vertex links unions of cycles.
   - Any hit dualises to a cubic law R-cycle that satisfies A5v, by Lemma F plus H0, and so refutes T1-v.
   - TrackH §7's pinch attempts were not aimed at this.
   - A null with power would be evidence that surface structure plus the law, not A5v, is the planar
     content.
2. **For a T1-v proof:** A5v is "¬inA seen from the dual". A proof should look for the face-free shadow
   of P2-face-components, i.e. which faces x_{j+2} is linked to, and not for a Jordan curve at v.
3. **Do not spend effort on A5v for the mixed (N ≥ 10) case.** Spend it on the class-level non-local
   input (law, σ-exits, surface structure).
4. Correct the axioms README Run 1 phrase "holds on RP²/Klein … local Jordan fact". In this run A5v
   failed at 5,659 off-sphere DL-good states: 220 integrable torus/Klein states with inA, and 5,439
   non-integrable states.

## 7. Files

| file | content |
|---|---|
| `a5v_primal.py` | primal A5v-P / strong / switch checks per DL state (via TrackH `th_engine`); Tait dual cross-check (TrackT `tait_dual` + axioms `ax_lib`); modes `one`, `batch`, `census33`, `general`, `surfpm`, `facelemma`; local surface-defect statistics |
| `census33_dlc_holes.json`, `out/census33_cycle_graphs.txt` | the 25 Census33 all-DL-cycle holes and their graphs (extracted from `Census33/out/frame-33.txt`) |
| `out/sphere_plantri24_s20.txt`, `out/census33_a5v.txt` | sphere consistency runs (§3) |
| `out/facelemma_*.txt` | Lemma F and liftability off the sphere (§3) |
| `out/general_trackH.txt`, `out/general_trackJ_rung_d.txt`, `out/general_trackP.txt`, `out/general_trackQ_e1.txt` | per-graph test rows (§4): `python3 a5v_primal.py general <file> 1 cyc` |
| `out/trackP_all.jsonl` | concatenation of TrackP `out/ex_*.jsonl` (input copy) |
