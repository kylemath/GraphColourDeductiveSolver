# Track L: the σ-type lemma (proved) and NRC (open) [hand, unreviewed] + [data]

Studio, 8 Oct 2026. Nothing outside `TrackL/` was changed and nothing was committed. TrackH (`th_engine.py`) and TrackI (`ti_lib.py`) code is imported read-only; everything else here is new.

Compute: at most 2 worker processes under `nice -n 10` (one accidental 3-worker overlap of under 2 minutes, killed). About 1 h wall time; machine load from other users was 12–14.

Labels: **[hand, unreviewed]** = hand proof not yet independently reviewed; **[data]** = computation.

## 0. Bottom line

1. **The σ-type lemma is proved [hand, unreviewed].** See `SigmaType.md`.
   - On a triangulated sphere, the extra chain of every in-shape state is an α_cμ_c-chain. In Tait form, the free {2,3}-cycle C′ lies on the e₃ side of H₀.
   - The proof is short, and **purely Euler-level**: no Jordan curve, no band surgery. It has two ingredients:
     - **Lemma E** (= TrackH's H3): every unfilled state has Σχ = 2, 3, 3 over the chains of P1, P2, P3, where χ(XY) = |X| + |Y| − e(X,Y). Proof: count crossing edges, using |E(T)| = 3n − 6.
     - **Lemma St** (star identity, any graph): a p↔q Kempe swap preserves χ(rp) + χ(rq) for every third colour r.
   - **How they combine.** π swaps α ↔ A, so St at colour μ gives χ(α_cA_c) + χ(A_cB_c) at c = π(u), which equals χ(αμ) + χ(μA) at u, which is 1 + 1 = 2 (u rigid, so all chains are trees). P2(c) = (2,1) are trees, so χ(α_cA_c) = 2. Hence χ(A_cB_c) = 0, so the unique cycle of P1(c) sits in A_cB_c and Z ⊂ α_cμ_c.
   - **One rigid π-neighbour suffices** (Corollary S2), matching the data: an AB-type extra never occurs next to a rigid state.
   - **Every step is data-checked with 0 failures:**
     - 2.03M π-steps (star identities);
     - 43,407 rigid states (forests);
     - 659k / 660k P2- / P3-minimal states (forests);
     - 5,501 instances of the key equality χ(A_cB_c) = 0;
     - 1,657 in-shape states.

     Coverage: census frame 23–29 all holes, plantri24 1/10, fullerene duals 1/2 (19,935 holes). On top of this, the exhaustive planar chord and figure-eight models (79 / 79 and 582 / 582).
   - It explains TrackJ's general-graph failures (80 / 3,475): by the proof, they must violate the sphere constants of H3.
   - **Where it breaks: RP².** Lemma E becomes Σχ = 1, 2, 2. So rigid states are never forests there (2,573 / 2,573 data), and the key equality fails in 188 / 368 cases. The σ conclusion nevertheless held in all 223 RP² cases with N = 9: unexplained, not proved.
2. **NRC: no proof.** What the σ-lemma machinery gives, and why it stops (§2):
   - Lemma E + St + J2 give a closed recursion for the χ-vector along π, with one free integer per step. The near-rigid alternation (1,1,2,1,2,1) ↔ (2,0,2,1,2,1) is a consistent orbit of it. **So no χ-level (Euler) argument can exclude a near-rigid cycle.** NRC needs component-position (Jordan-level) information, like RI.
   - A search for a monotone quantity along near-rigid two-steps found **none** among 16 candidates [data]. Candidates: lock-path lengths, swap-set sizes, F12/F13 loop lengths, positions of e₀/e₁/e₃ along H_u, colour-class sizes, cw, nesting of the Γ-discs, the sector of Z.
3. **Smallest open sub-claims** (§3).
   - **NRC′ (sphere)** (= NRC, given Lemma S): no π-cycle alternates rigid states with σ-type in-shape states. Equivalently, the two-step map Φ: u ↦ π²(u) on rigid states has no periodic orbit.
   - **Q-e (decides the proof type):** does NRC hold in every graph where the sphere constants of H3 hold at every state and the chain-parity law holds? TrackJ's rung-(e) search was uninformative.
     - If yes, NRC is Euler + combinatorics, and the σ-lemma technique might extend.
     - If no, a Jordan or band-surgery input is unavoidable, as for RI.

## 1. The σ-type lemma (summary; full proof in `SigmaType.md`)

> **Lemma S.** u rigid, c = π(u), (#α_cA_c, #μ_cB_c) = (2,1), and P1(c) has 3 chains. Then #α_cμ_c = 2, #A_cB_c = 1, and the A_cB_c-chain is unicyclic.
> **Corollary S1.** Every in-shape state on the sphere is σ-type. So the Z-matching of Theorem J5 is σ.
> **Corollary S2.** c DL, N(c) = 9, π⁻¹(c) rigid, extra chain not in P2 ⇒ σ-type. The mirror statement holds with π(c) rigid and the extra chain not in P3.

Proof sketch (roles of c = (α, B, μ, A) in u's names):

  χ_c(α_cA_c) + χ_c(A_cB_c) = χ_u(αμ) + χ_u(μA) = 2  (St at colour μ; u rigid ⇒ trees by Lemma E)
  χ_c(α_cA_c) = 2  (P2(c) = (2,1), trees by Lemma E)
  ⇒ χ_c(A_cB_c) = 0 ⇒ the unique unicyclic P1-chain (Lemma E: χ's (1,1,0)) is the A_cB_c chain ⇒ Z ⊂ α_cμ_c.

**Tait reading.**
- The region of S² − H on the e₃ side of H₀ is the AB link chain (corners x₃, x₄).
- "The AB link chain is unicyclic" means it is the annulus between H₀ and C′. Equivalently, C′ lies on the e₃ side.
- The star identity has no short Tait form, which is why the earlier Tait-only attempts (below) did not close.

**How the proof was found (for the record).** The direct Tait attempts are kept as negative results:
- **Line and territory models.** The "X̃-only" and "Ỹ-only" Lemma-R line models (`tl_line.py`, `tl_line2.py`) are exactly 50/50 between the two sides, even with both outer matchings free. So no argument on one switch circle can work. Territory pairings are also unconstrained (`tl_territory.py`).
- **Figure-eight model** (`tl_fig8_var.py`). It shows the lemma needs all of k(F13) = 1, k(HΔX̃) = 1 and k(HΔỸ) = 1. Dropping any one gives both sides.
- **Ladder words.** The rung word along the Lock1 path (rungs = Lock-path edges, all in H) is h(cc|hh)* for σ-type and (cc|hh)*h for AB-type (Jordan). This is equivalent to the side, not a proof of it (`tl_ladder.py`, `tl_sphladder.py`).
- **The breakthrough.** Rewriting σ-type as "#α_cμ_c = 2", i.e. which P1 pair graph carries the cycle, and noticing that π moves χ between {μ,α} and {μ,A} only.

## 2. Analysis of near-rigid runs [hand where marked; data]

### 2.1 χ-recursion along π [hand, any graph unless stated]

Let a = (a₁…a₆) be the χ-vector of c in role order (αμ, AB, αA, μB, αB, μA), and b that of π(c), whose roles are (α, B, μ, A). Then:
- b₅ = a₃ and b₆ = a₄ (J2: G[α,A] and G[μ,B] are unchanged as graphs);
- b₂ + b₃ = a₁ + a₆ (St at μ);
- b₁ + b₄ = a₂ + a₅ (St at B).

On the sphere, add Lemma E at both states: a₁ + a₂ = 2, a₃ + a₄ = 3, a₅ + a₆ = 3, and likewise for b. The four equations for b₁…b₄ have rank 3, so **one free integer per step** (e.g. b₃).

The near-rigid cycle of J5 uses (1,1,2,1,2,1) → (2,0,2,1,2,1) → (1,1,2,1,2,1) → …, which satisfies all of these. So the χ-level theory (Lemma E, St, J1–J3, Theorem 6) has the near-rigid alternation as a consistent orbit. **NRC cannot follow from χ-bookkeeping alone.**

This sits consistently with TrackJ:
- the rung-(d2)/(d) general-graph examples satisfy the H3 balance and are σ-type;
- rung (e), which imposes the full sphere constants and hence forests, is the open question Q-e.

### 2.2 The step structure in a near-rigid run [hand]

The repeated colour α is the same colour at every state of a π-orbit (π puts α at x_{j+3}). The other three colours rotate with period 3: the colour playing μ, A, B at c plays A, B, μ at π(c). So along a run:
- every swap is α ↔ (current A) on a tree;
- every extra chain Z is an α-pair chain;
- every cycle Γ (the unique cycle at an in-shape state) lies in a non-α pair graph.

At each step the star identity moves exactly one unit of χ between an α-pair graph and a non-α pair graph:
- **Creation** (u rigid → c in-shape, swap K = K^u_{αA}(x_{j+2})):
  - the αμ_u tree splits into the two α_cA_c trees K^c(x_j) and K^c(x_{j+3});
  - simultaneously {μ,A} closes its cycle Γ_c, which encloses Z_c, with h outside;
  - the {α,B} forest keeps 2 trees, one of which (Z_c) has become link-free.
- **Destruction** (c → u′ = π(c)):
  - the swap set is K_c = K^c(x_j), one of the two trees just created (J2);
  - its swap opens Γ_c (it must contain a μ-vertex of Γ_c);
  - it merges the two α_cμ_c trees (L_c and Z_c) into one.

NRC asks why this creation/destruction cannot be periodic on the sphere.

### 2.3 Searching for a monotone quantity [data]

Φ-steps are u → π(u) (in-shape) → π²(u) (rigid). Over all of them in frame-27 and frame-28 (151 two-steps, `tl_phi.py`, `out/phi.log`), the signs of Δ for each feature are:

| feature | + | − | = |
|---|---|---|---|
| \|X\|, \|Y\| (F13 loops of u) | 62 / 75 | 75 / 62 | 14 / 14 |
| \|X̃\|, \|Ỹ\| (F12 loops) | 79 / 58 | 58 / 79 | 14 / 14 |
| \|K\| (π's swap set), \|K̃\| (π⁻¹'s) | 66 / 86 | 82 / 58 | 3 / 7 |
| Lock-path lengths l₁, l₂ | 44 / 52 | 55 / 27 | 52 / 72 |
| position along H_u of the far end of e₀ / e₁ / e₃ | 28 / 28 / 133 | 120 / 120 / 17 | 3 / 3 / 1 |
| colour-class sizes \|α\|, \|μ\|, \|A\|, \|B\| | mixed | mixed | mixed |
| frame-28 only (`out/phi28b.log`): p(e₃) − p(e₀), p(e₃) − p(e₁), p(e₁) − p(e₀) | 117 / 117 / 42 | 18 / 19 / 61 | 5 / 4 / 37 |

No feature is monotone. The strongest bias is that the far end of e₃ moves forward along H_u and those of e₀, e₁ move back, in about 85% of steps. This is not a potential, and it may partly be an artefact of measuring positions from e₂ in a rotating frame.

Other quantities along maximal runs in R:
- **Γ-discs** (`tl_gamma.py`, plantri24 runs ≥ 5): the disc D(c) bounded by Γ_c, compared with D(π²c) over 340 consecutive pairs, is crossing 162, disjoint 131, nested inward 29, outward 18. Z ⊂ D held at 1,156 / 1,156 (Jordan).
- **Z-sector relative to the two lock paths** (`tl_sector.py`): no consistent rotation. In that sample Z always met a lock path in ≥ 1 vertex.
- **cw** (role-encoded) changes by 2 mod 4 per step, as F + Lemma W predict, and is otherwise not monotone (`out/runs_p24_6.log`).
- **Lock paths.** l₁(π c) = l₂(c) exactly (the Lock2 path of c is the Lock1 path of π(c)). This is trivial transport and gives no potential.

### 2.4 RP² contrast

On RP², Lemma E has constants (1, 2, 2), the law fails, and runs inside R reach 11 (TrackJ §3.3).
- The σ-lemma proof fails there at its first sphere-specific step (forests).
- The χ-recursion of §2.1 still holds with those constants.
- Nothing above distinguishes run lengths 7 vs 11.

## 3. Smallest open sub-claims

1. **NRC′ (sphere).** No π-cycle of DL states alternates rigid states and in-shape states. By Lemma S every such in-shape state is σ-type, with Γ in A_cB_c and Z ⊂ α_cμ_c, so σ-type is no longer an assumption.
   - Equivalently, Φ: u ↦ π²(u) on rigid states has no periodic orbit. Here Φ(u) is defined when π(u) is in-shape and π²(u) is rigid.
   - Data (TrackJ): 0 cycles in 473,178 holes; runs ≤ 7.
2. **Q-e.** Does NRC hold in every graph with a hole that satisfies the sphere constants Σχ = (2,3,3) at every state of the cycle (equivalently: all pair graphs are forests at rigid states, and one unicyclic chain at 9-states) plus the chain-parity law?
   - §2.1 shows χ-level information is consistent with a cycle. Q-e asks whether *component-level combinatorics* (which chain splits or merges, the star identities, J1–J5) suffices without an embedding.
   - Suggested next step: rerun TrackJ's rung-(e) search with vertex stacking seeded from sphere graphs with long runs (e.g. p32.r84#686339 h23, p24#596 h20), where the constants already hold, rather than from the dense rung-(d) examples.
3. **σ-type on RP²** (side question). It held in 223 / 223 cases even though the proof fails there. Is there a second mechanism?

## 4. Files

| file | content |
|---|---|
| `SigmaType.md` | proof of Lemma S, Corollaries S1 and S2, the Euler balance Lemma E, the star identity St, and per-step data |
| `tl_lib.py` | per-hole state data (TrackH engine), π, π⁻¹, N, role counts; Tait objects, primal region computation |
| `tl_sigma_check.py`, `run_sigma.sh` | step checks S0–S4 of the proof (`out/sigma_w1.log`, `out/sigma_w2.log`, `out/sigma_rp2.log`) |
| `tl_sigma_general.py` | Lemma S without DL/N hypotheses on c |
| `tl_explore.py` | extra-chain type vs rigidity of π-neighbours (`out/explore_*.log`) |
| `tl_chord.py` | chord model of rigid u: side of C′ in π(u), by face tracing (exhaustive to 13 cubic vertices) |
| `tl_fig8.py`, `tl_fig8_var.py`, `tl_ladder.py` | F12 figure-eight model of c (exhaustive to 15): hypotheses needed, ladder words (`out/ladder15.log`) |
| `tl_line.py`, `tl_line2.py`, `tl_territory.py` | abstract line and territory models (negative: side-symmetric) |
| `tl_sphladder.py` | lock-path words on sphere states |
| `tl_runs.py` | per-state quantities along maximal π-runs in R (`out/runs_p24_6.log`) |
| `tl_phi.py` | monotone-quantity search over Φ-steps (`out/phi.log`) |
| `tl_gamma.py`, `tl_zpairs.py`, `tl_sector.py` | Γ-disc nesting, Z vs Z″, Z-sector along runs (`out/gamma_p24.log`) |
