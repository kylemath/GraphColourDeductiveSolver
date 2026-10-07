# Night: the σ-island at p26 #70869 h11 and the replacement linking move σ*

Night worker, 7 October 2026 (written 02:23 by the machine clock, `date +%H%M`). **Exploratory. Hand reading plus single-core Python checks (seconds to minutes each, AC power, battery 100%). Unreviewed.**

Builds on:
- `NightLog-2026-10-06.md` (Studio Jobs E, F, G, H);
- `NightFloorR53.md` §5 (σC);
- `NightC1Gamma.md` (exact σ-exit criteria at k = 3, 4; fixed points at k = 0, 1, 2);
- `NightLockBreaking.md` (Lemma 1.2: breaking = gluing K_A⁰ to K_A or K_B⁰ to K_B).

The witness is `local-runs/27-studio-positive-config/witness-sigC-p26-70869-h11.json`. The engine is `local-runs/common/kempe_py.py` together with `pi_of` / `is_DL` from `local-runs/22-winding-escape/escape.py`.

Labels:
- [proved]: a complete argument;
- [data]: computed by the scripts in §6;
- [conjecture]: not proved.

Conventions (Job E):
- link x_j..x_{j+4} = α, μ, α, A, B, with m = x_{j+1};
- w_t is the third vertex of the face x_t x_{t+1} w_t;
- R1: w_j = A. R2: w_j = B and w_{j+3} = α. R3: w_j = B and w_{j+3} = μ;
- k6 is the set of positions (relative to j) of the degree-6 link vertices;
- σ swaps the {α,μ}-component K_σ of m;
- a state is a **DD endpoint** if it is the start or end of a DD step.

The hole is v = 11, with link (4, 10, 20, 12, 5) and degrees (5, 6, 5, 6, 6). So the degree-6 vertices sit at absolute link positions 1, 3, 4. The hole has no three consecutive degree-5 link vertices.

## Verdict

1. **The island is a fixed-point trap** [data, exact]. It has 12 DD endpoints. For 11 of them, σ(t) = t: K_σ is the **whole** {α,μ}-subgraph, which is connected (13 vertices). The 12th, s368 (R3, k6 = {1,2,4}), maps to s59 on Z₀. s59 has exactly Lock2: it is the start of Z₀'s long run. Z₀'s two DL states are again fixed points, so the group closes on {Z₊, Z₀}.
   - This is the k ∈ {0,1,2} fixed-point mechanism of NightC1Gamma, now with three degree-6 link vertices. Here it occurs at every k-configuration of the 12 endpoints.
   - It is not a local accident of the k positions. In this class, 47 of 76 DD endpoints are σ-fixed (36 of 64 outside the island). Every colour pair has 1–3 components at every island endpoint, so the graph is close to Kempe-saturated.
2. **Escapes** [data]. There are 8 lock-breaking link-free swaps from Z₊'s DD endpoints that leave the island; this reproduces the Studio's count of 8. Six go to w < 0 cycles (−28, −52) and two go to w = 0 cycles. Z₀ adds one more, to −28.
   - They use the pairs {A,B}, {μ,A} and {μ,B}, never {α,A} or {α,B}, with component sizes 2–7.
   - **All of them start at DD endpoints.** In the island every DL state is a DD endpoint.
3. **σ\*** [conjecture; data]. Use σ at holes with three consecutive degree-5 link vertices (R5³). At every other hole, use σ′ = all link-free lock-breaking swaps from DD endpoints.
   - It escapes the island.
   - It equals σ on the three families (so Conjecture G and the f = 3 structure are untouched).
   - It has 0 failures at orders 12–22 in both orientations, and on the witness.
   - The candidates "always swap L₁ = K_{μ,A}(m)" and "σ, else the smallest breaking swap" are dead or non-coinciding (§3).
4. **Correction to the night's final statement** [data]. "At the all-5 hole σ′ ⊇ σ" is false. Only 1,444 of 5,720 DD endpoints at (5,5,5,5,5) holes (orders 17, 20, 22, both orientations) have σ(t) among their σ′-images. The σ′-partition is coarser than the σ-partition at only 322 of 402 holes. So F5 is **not** a formal base case of σ′C as stated.
   - It is a base case of the union move σ ∪ σ′ (§3.3), whose conjecture is implied by σC on R5³ and by σ′C everywhere.
5. **Assessment (Q4).** At this hole the payment *is* still "one swap from a DD endpoint", but along a different colour pair. Four Z₊ endpoints (s469, s333, s429, s604) have neither a moving σ nor any breaking link-free swap. They are paid only through π, via the cycle's other endpoints.

## 1. Reconstruction of the island [data]

The class is all of T − v: 782 states, 22 π-cycles, Σw = −94. σ-groups by DD endpoints: 15 groups, max Σw = +1, attained by {cycle 16 = Z₊ (w = +1, L = 17), cycle 6 = Z₀ (w = 0, L = 8)}. This reproduces Job F exactly.

In the tables below:
- "step" is π's step kind: R₊₃ (λ = +1, the state has Lock2), φ_B or φ_A (λ = −1), τ (λ = −3);
- locks = (Lock1, Lock2);
- ring = w_j..w_{j+4} in role letters (a = α, m = μ).

**Z₊ (w = +1, L = 17, 10 DL, all 10 DD endpoints, 3 filled):**

| # | state | j | locks | step | ring | type | k6 | σ-image |
|---|---|---|---|---|---|---|---|---|
| 0 | s266 | 2 | 10 | φ_B | BAmaA | R2* | 4,1,2 | – |
| 1 | s273 | F | | φ_A | | | | – |
| 2 | s268 | 1 | 01 | R₊₃ | BABmA | R3* | 0,2,3 | – |
| 3 | s614 | 4 | 11 | R₊₃ | ABmam | R1 | 2,4,0 | **fixed** (K_σ whole, 13) |
| 4 | s368 | 2 | 11 | R₊₃ | BABmA | R3 | 4,1,2 | **s59 = Z₀#2**, Lock2 only (\|K\| = 8) |
| 5 | s469 | 0 | 11 | R₊₃ | ABmam | R1 | 1,3,4 | fixed |
| 6 | s333 | 3 | 11 | R₊₃ | BABmA | R3 | 3,0,1 | fixed |
| 7 | s342 | 1 | 11 | R₊₃ | ABmam | R1 | 0,2,3 | fixed |
| 8 | s542 | 4 | 10 | φ_B | BABmA | R3* | 2,4,0 | – |
| 9 | s585 | F | | τ | | | | – |
| 10 | s742 | F | | φ_A | | | | – |
| 11 | s723 | 4 | 01 | R₊₃ | ABBmA | R1* | 2,4,0 | – |
| 12 | s488 | 2 | 11 | R₊₃ | ABBmm | R1 | 4,1,2 | fixed (14) |
| 13 | s429 | 0 | 11 | R₊₃ | AABmm | R1 | 1,3,4 | fixed |
| 14 | s407 | 3 | 11 | R₊₃ | AABam | R1 | 3,0,1 | fixed (12) |
| 15 | s348 | 1 | 11 | R₊₃ | BABam | R2 | 0,2,3 | fixed |
| 16 | s604 | 4 | 11 | R₊₃ | BAmam | R2 | 2,4,0 | fixed |

(\* = not DL; the type is shown for reference only.)

Z₊ has two excursions:
- (s723, s488..s604, s266), with u = 7 and f = 1, worth +4;
- (s268, s614..s342, s542), with u = 7 and f = 2, worth +1.

So Σλ = 5 and w = +1. The DL runs have lengths 5 and 4, so all 10 DL states are DD endpoints (7 DD steps). R2 states occur at a DL interior: R2 ⇒ "π-image not DL" was a degree-5 lemma (F5 Lemma 2), and it does not hold here.

**Z₀ (w = 0, L = 8):**
- s11 (j = 3, locks 10, φ_B);
- s17 (filled);
- s59 (j = 2, locks 01);
- s65 (j = 0, DL, ring BBmam, type R2, k6 = 1,3,4; σ fixed);
- s13 (j = 3, DL, ring BAmmA, type R3, k6 = 3,0,1; σ fixed);
- s29 (j = 1, locks 10);
- s46 (filled);
- s63 (j = 0, locks 01).

Its excursions are (s59, s65, s13, s29) with u = 4 and f = 1 (worth +1), and (s63, s11) with u = 2 and f = 1 (worth −1).

**Why σ is trapped.**
- It is the fixed-point mechanism (K_σ = the whole {α,μ}-subgraph) at 11 of 12 endpoints.
- The single moving image, σ(s368) = s59, enters Z₀ at a single-lock state. Z₀'s own DD endpoints are fixed, so the edge is not continued.
- [proved, trivial] At s368 the {α,μ}-subgraph has exactly two components. So σ(s368) equals, up to renaming, the swap of the *other*, link-free component (size 4). σ is then itself a link-free lock-breaking swap (it breaks Lock1).

Component counts at the 12 endpoints (pairs αμ / AB / μA / μB / αA / αB) are all in {1, 2, 3}. At s469 and s604 they are 1/1/1/1/2/2: σ, the {A,B}-, {μ,A}- and {μ,B}-swaps are all renamings, and only the forced NoFrozen pairs K_A⁰ ≠ K_A and K_B⁰ ≠ K_B remain.

## 2. The lock-breaking exits [data]

These are link-free swaps from island DL states whose image is not DL. By NightLockBreaking Lemma 1.2, "breaks L2" means the swap glues K_A⁰ to K_A, and "breaks L1" means it glues K_B⁰ to K_B.

| from | pair | \|K\| | target (cycle, w) | breaks |
|---|---|---|---|---|
| Z₊ s614 | {μ,A} | 7 | c4, −28 | L2 |
| Z₊ s614 | {A,B} | 6 | c4, −28 | L1 + L2 |
| Z₊ s342 | {μ,B} | 2 | c0, −52 | L1 |
| Z₊ s342 | {μ,B} | 2 | c9, 0 | L1 |
| Z₊ s342 | {A,B} | 4 | c4, −28 | L1 + L2 |
| Z₊ s488 | {A,B} | 3 | c4, −28 | L1 |
| Z₊ s407 | {μ,A} | 3 | c4, −28 | L2 |
| Z₊ s348 | {μ,A} | 3 | c5, 0 | L2 |
| Z₀ s13 | {μ,A} | 2 | c4, −28 | L2 |

Remarks on the table:
- The pair pattern matches Lemma 1.1: {μ,A} breaks only L2, {μ,B} only L1, {A,B} either or both.
- Inside the island, two further breaking swaps stay put: σ(s368)'s link-free twin {α,μ} of size 4, and s342's {μ,A} of size 4 to s29. Z₀ s65 has {α,A} (6) to s63 and s13 has {α,B} (6) to s11.
- Non-breaking exits to negative cycles (DL images) also exist: s65 {μ,B} to c4, s488 {μ,A} to c0, s429 {μ,B} to c4.

**Structural reading.**
- σ fails here because the {α,μ}-subgraph is connected, not because of where the degree-6 vertices sit. The same 12 endpoints cover all five k-configurations of the pattern.
- The working exits are short chains (2–7 vertices) of the pairs {μ,A}, {μ,B} and {A,B}. These are the only pairs that can be link-free with fewer than three components here: {α,A} and {α,B} always have the two link components, so a link-free one needs a third.
- I have no proof that "αμ connected ⇒ some {μ,·} or {A,B} link-free breaking swap exists". s469, s333, s429 and s604 are counterexamples to the per-state version: none of the four has one.

## 3. The replacement linking move

Candidates were tested on the witness and on every degree-5 hole of gentri orders 12–22, both orientations. That is 5,825 R5³ holes and 7,887 other holes per orientation (3,937 and 5,505 of them at order 22). The R5³ holes contain the three families.

| move at a DD endpoint t | witness | fails at orders ≤ 22 | differs from σ-groups at R5³ holes (order 22) |
|---|---|---|---|
| σ | **fails** (+1) | 0 | – |
| L1: swap K_{μ,A}(m) | passes | **fails**: 17 #4 h0/h16 (5,5,5,5,5), both orientations; 22: 3 per orientation; 20 #61 h19 | ≈ 2,500 |
| σ, unless σ(t) is DL on t's own cycle, then the smallest breaking link-free swap | passes | 0 | ≈ 1,250 (fires at fixed points) |
| smallest breaking link-free swap only | passes | **fails**: 21 #97 h2 (5,5,6,7,5) | ≈ 2,170 |
| σ′ = all breaking link-free swaps | passes | 0 | ≈ 2,250 |
| σ ∪ σ′ | passes | 0 | ≈ 2,150 |

So "always the {μ,A}-swap" is dead, already at the all-5 hole. The fixed-point fallback passes but changes the groups at the three families, because fixed points occur there (Job E/G S2). It therefore cannot coincide with σ.

### 3.1 Proposed σ* [definition]

At a DD endpoint t of a degree-5 hole:
- **if the hole has three consecutive degree-5 link vertices (R5³)**, link t to σ(t);
- **otherwise**, link t to every link-free swap image of t that is not DL (σ′, the lock-breaking swaps of Lemma 1.2).

Properties:
- (a) σ* = σ on (5,5,5,5,5), (5,5,5,5,6), (5,5,5,6,6) and all R5³ holes. So F5's formal σC (`sigmaC_of_icoBall`), Job E, Job G's Conjecture G and S5's f = 3 are unchanged. The scope predicate is `ThreeConsecFive` (af47a6c).
- (b) The witness hole is not R5³, and σ*-groups there have max Σw = 0 (6 groups).
- σ*-groups are π-invariant unions of π-cycles inside the class (σ′ targets are Kempe neighbours). So σ*C ⇒ the floor, by the same argument as `sigmaC_imp_quarterFloor`.

**Conjecture σ*C.** At every degree-5 hole of a triangulated sphere, Σλ ≤ 0 on every σ*-group of every Kempe class.

Status [data]:
- on R5³ it is σC: 0 failures in Jobs E/F;
- elsewhere it is σ′C restricted to non-R5³ holes: Job H, 0 failures in about 100M groups, plus here 0 failures at orders 12–22, both orientations.

### 3.2 Why not σ′ everywhere

σ′ alone also passes everywhere tested (Job H). But at the three families it does not equal σ, so the proved and tested mechanism there (F5 Lemma 3, the exact exit criteria, Conjecture G, f = 3) does not apply to σ′-groups.

### 3.3 The weakest uniform form

σ° = σ ∪ σ′ at every hole. Its groups coarsen both the σ-groups and the σ′-groups. So:
- σC on R5³ implies σ°C there, and F5 implies σ°C at the all-5 hole (formally, via `sigmaC_of_icoBall` and coarsening);
- σ′C implies σ°C everywhere.

σ°C is the logically weakest of the three statements that still implies the floor. 0 failures at orders 12–22 and on the witness.

## 4. Assessment (Q4)

- Every DL state of the island is a DD endpoint (DL runs of lengths 5, 4 and 2). So the escaping exits necessarily start at DD endpoints. "Payment one swap from a DD endpoint" survives, but the swap's colour pair is not {α,μ}.
- What fails is **per-endpoint** payment. Four of Z₊'s ten endpoints have no outward move of either kind. The surplus +1 is carried out by the other six (exits to −28 and −52).
- So the transport (d) picture is accurate at this hole: lock-breaking exits from *some* DD endpoints of the positive cycle.
- Island states that are not DL also have link-free exits (8 from Z₊'s unfilled non-DL states, 2 from its filled states), but none is needed.
- The island is not evidence that payment needs exits from arbitrary DL states. It is evidence that σ fails exactly when the {α,μ}-subgraph is connected at most endpoints, which a small, nearly Kempe-saturated graph (n = 26, one class) makes likely.
- Under R5³ this cannot happen at an R3 endpoint with x₀, x₁, x₂ of degree 5 when (w₀, w₁, w₂, w₄) = (B, A, B, A) (Lemma 3′(b): K_σ is the triple). Fixed points there arise only at the other frames.

## 5. Open items

- [conjecture] σ*C (equivalently σC on R5³ plus σ′C off R5³).
- Fix the night's final statement: σ′ ⊉ σ at the all-5 hole (§Verdict 4). F5 formally covers σC and σ°C there, not σ′C.
- A hand reason for σ′-exits at σ-fixed endpoints: "K_σ = whole {α,μ}-subgraph ⇒ a breaking link-free {μ,·}/{A,B}-swap exists at some endpoint of the same DL run". This is false per endpoint (s469 and others); untested per run.

## 6. Reproduction (session scratchpad `isl/`, not committed; single core)

| script | content | time |
|---|---|---|
| `base.py` | frame, locks, σ, π-cycles, DL / DD / DD-endpoint flags (imports kempe_py and escape) | – |
| `island.py`, `detail.py` | σ-groups on the witness; the §1 tables | < 1 s |
| `exits.py`, `struct.py`, `l1.py` | §2 exits; component counts; candidate images | < 1 s |
| `variants.py w` / `variants.py 12 14 16 17 18 19 20` / `21` / `22` | §3 table, both orientations (mirror = reversed rotations) | < 1 s / 15 s / 45 s / 3.7 min |
| `contain.py` | σ ∈ σ′? at (5,5,5,5,5) holes, orders 17, 20, 22 | about 1 min |
