# Track I: rigid isolation is a theorem on the sphere [hand, unreviewed]

Studio, 8 Oct 2026. Nothing outside `TrackI/` was changed and nothing is committed. TrackH and TrackF engines were imported read-only.

Labels:
- **[hand, unreviewed]**: hand proof, not yet independently reviewed.
- **[data]**: computation.

Compute: at most 2 worker processes, all under `nice -n 10`, about 1.5 h wall time in total.

## 0. Bottom line

1. **Rigid isolation (RI) is proved** [hand, unreviewed]: on a triangulated sphere, if c is a rigid DL state at a degree-5 hole, then π(c) is not rigid. The proof is in `RigidIsolation.md`.
2. **RI is a special case of a more general parity law (Theorem 6)** [hand, unreviewed].
   - Let N(s) be the total number of Kempe chains of s (components of the six pair graphs of T − h). For every DL state c at a degree-5 hole of a triangulated sphere:
     **N(π(c)) − N(c) ≡ [π(c) is DL] (mod 2).**
   - Rigid ⇔ N = 8, which is the minimum for a DL state. So a rigid c with a rigid π(c) would give 0 ≡ 1.
   - Along every all-DL π-cycle on the sphere, N alternates in parity.
3. **The mechanism** is a switching-parity lemma: Lemma 5, built on the planar Lemma R. On the sphere, band surgery on a closed curve always changes the number of curves by exactly ±1. Switching colours 1 ↔ 3 on the boundary of K_{αA}(x_{j+2}) therefore changes k(H) + k(F12) by a parity that is fixed by the pairing at v alone.
   - Planarity is used in exactly four places: Jordan for the v-loops, regions = chains, locks = pairings, and "the far side of X is a disc".
4. **Checks** [data] (§3): 0 failures in every case.
   - Lemma 5 / Theorem 6 hold at **580,161 DL states** of real sphere triangulations (24-vertex, frame class 22–28, fullerene duals, Census29 cycle graphs), and at all 170,126 DL instances of the planar chord model up to N = 13.
   - The Tait translation agrees with the vertex engine on every rigid image.
5. **The proof visibly breaks off the sphere** [data].
   - On RP², Lemma 5 fails at 35% of DL states.
   - At all 36 RP² rigid → rigid steps, every Tait quantity looks spherical: pairings of DL type, all k = 1, X separating. The single failing step is (P-ii): the outer side of X is a Möbius band, and the outer F12 end-matching is **crossing** in 36/36 cases (outer H matching in 33/36).
   - Lemma R is false for crossing matchings (already at 4 points).
   - In TrackH's general-graph counterexamples N is constant along the π-cycle: N = 8 in the two rigid ones, N = 10 in the non-rigid 40-state one. So Theorem 6 fails at every step there.
6. **Toward LPC.**
   - Theorem 6 excludes every Kempe class on the sphere whose π-cycles keep N constant. That covers all three TrackH counterexample shapes, the non-rigid 40-state class included.
   - It does **not** exclude a closed all-DL class in which N alternates. Every sphere all-DL π-cycle in the data alternates (24/24), and those cycles sit in classes that have filled states.
   - The next naive strengthening, "no all-DL π-cycle contains a rigid state", is **false** (11 rigid states on 6 of 23 sphere cycles).
   - What remains is in §4.

## 1. Restatement (Tait / chord language)

**Construction.**
- Dualise T and contract the pentagon h\* to a vertex v. This gives a plane graph G with v of degree 5 and every other vertex cubic.
- Faces of G are the vertices of T − h. The edge e_t at v is dual to the link edge x_t x_{t+1}.
- The colouring c gives the Tait colouring "edge ↦ c(u) + c(w) ∈ ℤ₂² − 0", with colour 1 = α+μ, 2 = α+A, 3 = α+B. At v the colours are (1, 1, 2, 1, 3) on e₀ … e₄.
- **H = M₂ ∪ M₃** (the {2,3} edges; v-degree 2), **F12 = M₁ ∪ M₂** and **F13 = M₁ ∪ M₃** (v-degree 4).

**Dictionary (sphere).**
- #αμ + #AB = 1 + k(H), #αA + #μB = 2 + k(F13), #αB + #μA = 2 + k(F12). Hence N = 5 + k(H) + k(F12) + k(F13).
- Lock1 ⇔ F12 pairs (e₀e₃)(e₁e₂). Lock2 ⇔ F13 pairs (e₁e₃)(e₀e₄).
- **Rigid ⇔ H, F12 and F13 are all connected**:
  - H is a Hamiltonian cycle through v;
  - F12 and F13 are figure-eights at v with the DL pairings.
- **X** is the F13-loop through e₁, e₃, and **Y** the F13-loop through e₀, e₄. For rigid c, F13 = X ∪ Y.

**π in Tait form.**
- π switches 1 ↔ 3 on C = ∂(region of K_{αA}(x_{j+2})). For rigid c, C = X.
- In π(c)'s own frame: H′ = F12 Δ C (= H Δ Y when C = X and F13 = X ∪ Y), F12′ = F13, and F13′ = H Δ C.
- π(c) always keeps Lock1, and π(c) is DL ⇔ H Δ C pairs (e₁e₄)(e₂e₃).

**RI in chord language.** Draw H as a circle, with the colour-1 edges as non-crossing chords inside and outside it. It is impossible that all three of the following hold:
- H Δ Y is one cycle;
- H Δ X is connected;
- H Δ X pairs (e₁e₄)(e₂e₃).

**Reason (Lemma 5, rigid case).** k(H Δ X) + k(H Δ Y) ≡ [H Δ X pairs (e₁e₄)(e₂e₃)] (mod 2).

## 2. The proof in one paragraph (details in `RigidIsolation.md`)

**Step 1: cut along C.** Cut S² along C = X ∪ Z₁ ∪ … ∪ Z_r. On X, split v into two points a and b. On each circle, the C-edges of colour 1 and of colour 3 are the two alternating matchings B₁ and B₃ of consecutive points; X also gets a virtual arc ba through v.

**Step 2: the off-C pairings.** The parts of H and of F12 off C pair the points.
- (P-i) On the side of K's region R, both pairings consist of the same colour-2 chords, because R contains no vertex.
- (P-ii) On each far side, a disc, both pairings are non-crossing.

**Step 3: Lemma R.** λ(B₁, N) + λ(B₃, N) mod 2 does not depend on the non-crossing outer matching. Flips connect all such matchings, and each flip is a band surgery, which on S² changes the number of curves by exactly ±1.

**Step 4: read off Lemma 5.** The four Tait subgraphs H, H Δ C, F12 and F12 Δ C are exactly B₃ ∪ N^H, B₁ ∪ N^H, B₁ ∪ N^F and B₃ ∪ N^F. At v, B₁ forces the smoothing (e₁e₂)(e₃·), which costs one indicator per subgraph. Lemma R then gives Lemma 5 directly.

**Step 5: conclude.**
- Lemma 5 plus the dictionary gives Theorem 6.
- Theorem 6 with N(c) = 8 gives RI.

**Correction to a tempting extension (Remark 7).** Swaps on curves *not* through v do **not** preserve N mod 2: this fails on 111,912 of 281,230 link-free moves. The reason is that v is then a degree-4 vertex off C, whose pairings can change. The corrected invariant is **N + L1 + L2 (mod 2)**, with 0 failures on 281,230 link-free moves.

## 3. Data [data]

| check | where | count | failures |
|---|---|---|---|
| Lemma 5 for the X-switch, all DL states (`ti_check.py`) | plantri24 (every 60th, 121 graphs) / frame22–28 (147) / fullerene duals C20–C46 (every 8th, 43) / Census29 cycle graphs p30–p32 (16) / C30#0 | 100,041 / 313,000 / 27,158 / 139,962 / 200 = **580,361** | **0** |
| Lemma 2 (Tait pairings DL-type at every DL state) | same | 580,361 | 0 |
| Tait prediction of "π(c) rigid" vs. vertex engine | same, rigid states | 12,731 rigid states (2,751 / 6,774 / 1,824 / 1,382) | 0 mismatches; **0 rigid → rigid** |
| Theorem 6, primal only, no Tait code (`ti_chains.py`) | plantri24 / frame / fullerenes / Census29 cycle graphs | **580,161** DL states (DL→DL steps all odd: 124,197; DL→S all even: 455,964) | **0** |
| Theorem 6 when K_{αA}(x_{j+2}) has holes (C ≠ X) (`ti_holes.py`) | plantri24, 60 graphs | 16,618 holed + 33,454 hole-free | 0 |
| Lemma 5, chord model, every DL instance (`ti_chordstar.py`) | N ≤ 13 cubic vertices, exhaustive | 170,126 (2,789 rigid) | 0; 0 rigid → rigid |
| Lemma R (`ti_lemmaR.py`) | all I/O labellings, ≤ 12 points | 3,636 labellings | 0 (fails for crossing matchings from 4 points) |
| Remark 7: N + L1 + L2 under link-free moves (`ti_moves.py`) | plantri24, 25 graphs | 281,230 moves | 0 (N alone: 111,912 changes) |
| all-DL π-cycles on spheres: N alternates (`ti_cycprofile.py`, `ti_cycleN.py`) | Census29 cycle graphs (23 cycles, including the TrackH sphere test beds) + C30#0 | 24 cycles | 0 |

**Off the sphere** (`out/cycitems.log`, `out/chains_cyc.log`, `ti_rp2sep.py`):

| surface | Lemma 5 failures | Theorem 6 failures | crossing pairings of H Δ X |
|---|---|---|---|
| RP² (202 graphs) | 90,251 / 259,914 | 60,094 | 75,570 |
| Klein (36) | 28,534 / 72,167 | 19,768 | 19,896 |
| torus (12) | 4,387 / 20,543 | 5,597 | 3,290 |

**The 36 RP² rigid → rigid steps** (`out/cycitems.jsonl`, records with "tait"):
- every Tait quantity at c is sphere-like: kH = k12 = k13 = 1, DL pairings, X closes at e₃;
- π(c) is also Tait-DL with kHX = k12X = 1, and Lemma 5's parity is 1 (it fails);
- X separates RP² in 36/36. So D_X is a disc and its complement is a Möbius band;
- the outer end-matching N_O is crossing for F12 in 36/36 and for H in 33/36, so (P-ii) fails.

Control: on 355 sphere rigid states the same code finds 0 crossings.

**General graphs** (`ti_general.py`): N along the all-DL cycle is 8, 8, …
- in `lp_general_min` (10 steps) and `lpc_general_min` (10 steps);
- in `lpc_general_40` it is 10 at all 40 steps.

Every DL→DL step has even ΔN, so Theorem 6 fails at every step of all three.

## 4. What RI (and Theorem 6) give toward LPC, and what remains

**Starting point.** LPC on the sphere ⇔ no Kempe class 𝒦 at h consists only of states on all-DL π-cycles (LockParity §5.2).

**Now proved [hand, unreviewed]:**
1. **No 𝒦 consists only of rigid states.** This is RI combined with TrackH Lemma H5. It is exactly the shape of TrackH's two rigid general-graph counterexamples.
2. **In any such 𝒦, N alternates in parity along every π-cycle** (Theorem 6, with every π-step DL → DL).
   - Hence at least half the states of each cycle have N ≥ 9: an extra Kempe chain beyond the 8 forced ones, and so a Kempe move other than π, π⁻¹ and renamings.
   - This excludes every class in which N is constant along a cycle, including the non-rigid 40-state general-graph class `lpc_general_40` (N ≡ 10).
3. **Inside such 𝒦 (where L1 = L2 = 1), link-free Kempe moves preserve N mod 2** (Remark 7).

**Not given.** A closed class of all-DL cycles in which N alternates (8/9/10/… with the right parities), with every extra-chain swap landing again on an all-DL cycle state.
- Theorem 6 is a parity statement. Like Heawood-type invariants, it cannot by itself exclude such classes.
- Sphere all-DL cycles that satisfy it do exist (C30#0: N = 10, 9, 10, 9, …; p32.r11#14729: 11, 8, 11, 10, …). They are kept from closing only by exits to filled states. At C30#0 the σ-exits sit exactly at the N = 9 states; across all 23 Census29 cycles, exits occur at 373 of the 460 cycle states.
- Two state-level strengthenings are false on spheres:
  - "no all-DL cycle contains a rigid state": **false**, 11 rigid states on 6 of 23 cycles;
  - "every state with N ≤ 9 on an all-DL cycle has an exit": **false**, 29 of 49 near-rigid cycle states have none.

**Smallest open sub-claim (suggested next target).**

> **Near-rigid LPC (sphere):** no Kempe class at a degree-5 hole of a triangulated sphere consists only of DL states on all-DL π-cycles with N ≤ 9 at every state.

- By Theorem 6, such a class alternates rigid (N = 8) and N = 9 states along every cycle.
- Rigid states have Kempe degree 2. Each N = 9 state has exactly one extra Kempe chain: a free bicoloured Tait cycle, or a second component of one pair graph.
- So the class is a union of π-cycles, joined only through the extra-chain swaps at the 9-states.

This is the next shape after the all-rigid one, and a statement about one extra curve, where the Lemma R machinery (Remark 7) still applies. Not attempted.

General-graph searches (TrackH style) should first check whether near-rigid closed classes exist at all off the sphere: if none exist even in general graphs, the target is local and uninteresting; if they do, it is sphere-specific like RI.

## 5. Files

| file | content |
|---|---|
| `RigidIsolation.md` | the proof: Lemmas 0–5, Lemma R, Theorem 6, Theorem RI, Remark 7; chord-model restatement |
| `ti_lib.py` | Tait objects; independent chord-model generator; primal → Tait conversion (faces = link triangles, so it works on any closed surface) |
| `ti_check.py` | Lemma 5 + RI on real triangulations (any surface), Tait vs. vertex-engine cross-check |
| `ti_chains.py` | Theorem 6 with primal Kempe-chain counts only (independent of the Tait code) |
| `ti_holes.py` | Theorem 6 split by whether K_{αA}(x_{j+2}) has holes |
| `ti_chordstar.py` | Lemma 5 / RI in the exhaustive chord model |
| `ti_lemmaR.py` | Lemma R exhaustively, and its failure for crossing matchings |
| `ti_rp2sep.py` | RP² rigid → rigid steps: separation of X and crossing of the outer end-matchings (the failing step) |
| `ti_general.py` | Theorem 6 on TrackH's general-graph counterexamples |
| `ti_moves.py` | parity of N and N + L1 + L2 under all Kempe moves (Remark 7) |
| `ti_rx.py`, `ti_cycprofile.py`, `ti_cycleN.py` | rigid states on all-DL cycles (RX false), N-profiles and exits along all-DL cycles |
| `out/` | logs (`*.log`) and per-graph records (`*.jsonl`) of all runs |
