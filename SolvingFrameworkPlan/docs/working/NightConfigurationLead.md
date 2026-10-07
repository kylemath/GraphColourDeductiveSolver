# Night: the configuration lead (Conjecture P)

Night worker, 7 October 2026 (written 00:51 MDT). **Exploratory. Hand work plus small single-core checks. Unreviewed.**

Cited notes:
- **EH** = `NightEulerHole.md` (Theorem W, π, λ);
- **WM** = `NightWindingMeander.md` (w(Z) = (|Z| − 4F_Z)/5, tokens);
- **CS** = `NightClosedSets.md` (C1–C3, rotation equivariance);
- **QW** = `StudioMathLean/.../PlaneMap/QuarterWinding.lean` (Theorem W, formal);
- **QP** = `QuarterPi.lean` (Lemma Π, formal);
- **run 23** = `longtable/local-runs/23-positive-cycles`;
- **run 24** = `longtable/local-runs/24-positive-vs-config`.

Labels:
- [proved] means a complete argument is given here, modulo the cited formal or audited facts.
- [sketch] means the gap is named.
- [conjecture] means not proved.
- [data] means computed here by the scratchpad scripts in §7. Those scripts are not committed.

Diamond and 2.122 follow the conventions of run 24's `conf.py`. Both are K4 − e with two faces and non-adjacent tips. The diamond has degrees 5555; 2.122 has one degree-6 centre and the other three vertices of degree 5.

**Conjecture P.** In a core triangulation with no diamond and no 2.122, no Kempe class at any degree-5 hole has a π-cycle of positive winding.

**Nothing here proves P.** P is 4CT-strength (§5.1).

## Verdict

1. **The headline statistics are at base rate** [data].
   - At orders 22–24:
     - 94.2–96.9% of all degree-5 holes are configuration vertices;
     - only 6 of 9,912 graphs are configuration-free.
   - So "116/123 holes in a configuration" (94.3%) and "108/108 graphs contain one" are what a configuration-blind null predicts.
   - The only evidence for P is the negative side:
     - 81 holes in 6 configuration-free gentri graphs;
     - 425 IPR-dual holes.
   - At the observed positive rate (about 0.08% per hole), both samples are too small to discriminate (§4).
2. **Task 2's local lemma is false at radius 1** [data].
   - At 24 #6811 (1-based), hole 22, the link degrees are (7,5,7,5,5).
   - That hole has an **all-DL Γ-cycle** (L = 20, w = +4), although neither v nor any link vertex lies in a diamond or 2.122. The nearest configuration vertex is at distance 2.
   - At 23 #1109 hole 19, v is in no configuration and still has a Γ-cycle.
3. **Mechanism at gentri 17 #3** (0-based), holes 0 and 16 [data plus a proved local fact].
   - The graph is the D₅-symmetric 1-5-5-5-1 triangulation.
   - On the Γ-cycle, π⁴ equals the automorphism ρ², so the cycle is one 4-step block repeated 5 times.
   - Both lock chains run **through the antipodal diamond cap** (ring 3 and the pole), not near v.
   - The hole's own diamonds act only through Heawood rigidity: a degree-5 m forces both locks to leave m through distinct, unique outer neighbours.
   - Every vertex of T − v is recoloured along the cycle.
   - Symmetry is **not** the general mechanism: two Γ-cycles have a trivial stabiliser.
4. **Exact facts** [proved]:
   - 5w(Z) = #DL + 2m − N₀ − 3F, so a positive cycle needs a DD step (§3.1).
   - The Occ-free conditions on the 2-ball of v (§2.1).
   - **Theorems H, HP and R5³ only ever apply at diamond centres**, so they are vacuous on configuration-free graphs. Every degree-5 hole there is in the open case of two or more high neighbours (§3.3).
5. **Remains:** all of P. Any statement excluding Γ-cycles in configuration-free graphs implies 4CT. P can be false at larger orders: nothing local forbids it (§5).

---

## 1. Task 1: mechanism at the smallest positive cycles

### 1.1 The graph, gentri 17 #3 (line 4 of tri17.txt) [data]

The graph is in rings:

| ring | vertices | degree |
|---|---|---|
| v | 0 | 5 |
| R1 | 1–5 | 5 |
| R2 | 6–10 | 6 |
| R3 | 11–15 | 5 |
| pole | 16 | 5 |

- There are 10 diamonds:
  - (0, x_i) with tips x_{i±1}, for i = 1..5;
  - the mirror family at the pole, (16, y) for y ∈ R3.
- There is no 2.122. The graph is symmetric under v ↔ 16.
- The class of hole 0 has 100 states, split into one Γ-cycle (L = 20, w = +4) and one cycle (L = 80, w = −16).

**Lock chains** for the first 5 states of the Γ-cycle. The link is x_j..x_{j+4}; m = x_{j+1}, a = x_{j+3}, b = x_{j+4}.

| step | j | (x_j..x_{j+4}) | L1: m → a ({μ,A}) | L2: m → b ({μ,B}) | outer neighbours of x_{j+2} |
|---|---|---|---|---|---|
| 0 | 4 | 5 1 2 3 4 | 1–6–12–13–8–3 | 1–7–12–11–10–4 | 7 = B, 8 = μ |
| 1 | 2 | 3 4 5 1 2 | 4–10–11–12–7–1 | 4–9–14–16–11–6–7–2 | 10 = A, 6 = B |
| 2 | 0 | 1 2 3 4 5 | 2–7–6–11–16–14–9–4 | 2–8–9–15–16–12–6–5 | 8 = B, 9 = μ |
| 3 | 3 | 4 5 1 2 3 | 5–6–12–16–15–9–8–2 | 5–10–15–14–8–3 | 6 = A, 7 = B |
| 4 | 1 | 2 3 4 5 1 | 3–8–14–15–10–5 | 3–9–14–13–7–1 | 9 = B, 10 = μ |

- Step 4 is ρ²(step 0), with ρ: i ↦ i+1 in each ring. Under ρ², L1 = 1–6–12–13–8–3 maps to 3–8–14–15–10–5.
- **π⁴ = ρ² on this cycle** [data: checked state by state]. So the 20 states are the 4-step block (steps 0–3) and its images under ρ², ρ⁴, ρ, ρ³.
- Every step is R₊₃, and j advances by 3. Each lock chain runs link → R2 → R3 (sometimes through the pole) → R2 → link.
  - So the locks are held up by the far half of the sphere, which is the antipodal diamond cap.
  - By rotation equivariance (CS E1), the new lock 1 is the old L2 at every step. So each chain lives for two steps: it is born as L2, serves as L1, and is then broken by the next R₊₃.
- **Support:** the union of the swapped K_A over the cycle is all 16 vertices of T − v.

### 1.2 Heawood rigidity at m [proved]

**Lemma R.** Let s be unfilled at j and m = x_{j+1}. If deg_T m = 5, the two outer neighbours p, q of m have colours {A, B}, one each. Hence L1 must leave m through its unique A-neighbour and L2 through its unique B-neighbour.

*Proof.*
- In T − v the neighbours of m form the path x_j, p, q, x_{j+2}, with faces x_j m p, m p q, m q x_{j+2}.
- p is adjacent to m (μ) and x_j (α), so p ∈ {A, B}. Likewise q ∈ {A, B}.
- p is adjacent to q, so p ≠ q. ∎

**If deg m = 6**, with neighbours x_j, p, q, r, x_{j+2}:
- p and r are in {A, B}, and q ∈ {α, A, B} \ {p, r};
- p = r is possible, and then m has a single lock-exit colour.

In the Γ-cycle of §1.1 every link vertex is m four times. Lemma R fixes the first edge of both locks every time; that is the column pattern above (6 = A, 7 = B at m = 1, and so on).

**This is the only place the hole's own diamonds enter that I can identify.** It is a statement about one state, not about the closing of the orbit.

### 1.3 All Γ-cycles at orders ≤ 24 [data]

There are 11 Γ-cycles, in 10 classes and 9 distinct (graph, hole) cases up to the v ↔ 16 symmetry. **Every one has L = 20 and w = +4.**

| case (1-based) | link degrees | v's role | Aut fixing v | π⁴ an automorphism? | support |
|---|---|---|---|---|---|
| 17 #4 h0, h16 | 5,5,5,5,5 | 5 diamond centres | 10 | yes (ρ²) | 16/16 |
| 22 #418 h21 | 6,5,6,5,5 | 2.122 (4) | 2 | only id and reflection | 21/21 |
| 22 #649 h0, h21 | 5,5,5,5,5 | 5 diamond centres | 10 | yes | 21/21 |
| 23 #1109 h19 | 5,6,6,6,5 | **none** (config at distance 1) | 1 | no | 22/22 |
| 24 #4101 h22 | 6,5,5,6,5 | 2.122 (4) | 2 | no | 23/23 |
| 24 #5375 h19 | 7,5,5,5,5 | diamond (2) | 1 | no | 23/23 |
| 24 #6811 h22 | 7,5,7,5,5 | **none** (config at distance 2) | 2 | no | 23/23 |
| 24 #906 h22 (2 cycles) | 5,5,5,5,5 | 5 diamond centres | 2 | no | 23/23 |

Reading:
1. **Γ-cycles are global objects.** Every vertex of T − v changes colour, so no bounded-radius mechanism carries the locks.
2. **The symmetric closing at 17 #3 is special.** At 23 #1109 and 24 #5375 the hole has a trivial stabiliser, and the orbit still closes after 20 steps.
3. **[conjecture, data-thin] Γ-cycle lengths are ≡ 0 mod 20**, that is, w ≡ 0 mod 4.
   - Evidence: the 11 cycles of length 20, plus the A7 adversarial cycle of length 800 (CS §3).
   - This would sharpen CS C3 (≡ 0 mod 5) and EH's mod-10 conjecture.

### 1.4 Link-degree patterns of the 123 positive classes [data]

Patterns are cyclic, up to reflection, with degrees ≥ 8 capped at 8. The base column is all degree-5 holes at orders 17–24.

| pattern | positive classes | base holes | rate | v forced to be a configuration centre by the link? |
|---|---|---|---|---|
| 5,5,6,5,7 | 24 | 11,526 | 0.21% | yes (5,6,5) |
| 5,5,5,6,7 | 14 | 11,123 | 0.13% | yes |
| 5,5,6,5,6 | 13 | 9,014 | 0.14% | yes |
| 5,5,6,5,≥8 (one at degree 9) | 14 | 7,126 | 0.20% | yes |
| 5,5,5,5,7 | 10 | 8,533 | 0.12% | yes |
| 5,5,5,5,5 | 8 | 2,867 | 0.28% | yes |
| 5,6,5,6,6 | 7 | 6,338 | 0.11% | yes |
| 5,6,5,6,7 | 6 | 6,192 | 0.10% | yes |
| 5,6,6,5,7 | 5 | 3,273 | 0.15% | no |
| 5,5,7,5,7 | 4 | 3,228 | 0.12% | no |
| 5,5,6,6,6 | 4 | 6,190 | 0.06% | no |
| 5,5,6,6,7 | 4 | 6,041 | 0.07% | no |
| 5,6,6,5,8 | 3 | 1,349 | 0.22% | no |
| 5,5,5,6,8 | 2 | 6,311 | 0.03% | yes |
| 5,5,5,5,8 | 2 | 7,481 | 0.03% | yes |
| 5,6,6,7,6 | 2 | 2,107 | 0.09% | no |
| 5,6,6,6,7 | 1 | 2,252 | 0.04% | no |

- **v's role** over the 123 classes:
  - 2.122 centre and 2.122 tip: 62;
  - diamond centre only: 24;
  - diamond centre and 2.122 tip: 12;
  - 2.122 tip only: 16;
  - 2.122 centre only: 2;
  - none: 7.
- **Enrichment is mild.**
  - Holes whose link pattern forces v to be a centre: 100 positives in 105,983 (0.094%).
  - Other holes: 23 positives in 49,988 (0.046%).
  - So the factor is about 2, nowhere near "necessary".
- **Every positive hole has at least one degree-5 neighbour** (123/123). The base count of holes with no degree-5 neighbour is 492, so this is uninformative.
- **Striking zeros** [data; unexplained]. The overall rate is 0.079%, and treating holes as independent overstates significance. With that caveat, three patterns stand out:

  | pattern | positives / holes | expected count | P(0) if independent |
  |---|---|---|---|
  | 5,5,5,5,6 | 0 / 11,791 | 9.3 | ≈ 1e−4 |
  | 5,5,5,6,6 | 0 / 8,971 | 7.1 | ≈ 1e−3 |
  | 5,6,6,6,6 | 0 / 3,398 | – | – |

  - By contrast, 5,5,5,5,7 has 10 positives and 5,5,5,6,7 has 14.
  - This is **not** a DL-run effect. 5,5,5,5,6 has DD/DL = 0.14 and runs up to 17 at orders ≤ 22, comparable to the positive patterns.
  - A degree-6 neighbour in these positions seems to kill positivity. **This is a sharper and more local lead than "configuration present", and it points the other way**: 5,5,5,5,6 is full of configurations.

**Answer to "is the link arrangement what matters?"** Not by itself.
- Positive classes occur in 17 patterns (18 without capping).
- 23 of them occur at holes whose link does not make v a centre, and 7 at holes in no configuration at all.
- No single pattern has a rate above 0.3%.

## 2. Task 2: the local lemma

### 2.1 Exact local consequence of Occ-freeness at v [proved]

Setting:
- T is a core triangulation (no separating triangle, minimum degree 5).
- v has degree 5, with link x₀..x₄ and d_i = deg x_i.
- y_i is the apex of the outer face on x_i x_{i+1}.

Tips are automatically non-adjacent. Suppose the tips p, s of a centre edge qr were adjacent. Then pqs is a triangle. It is not a face, since q has other neighbours, so it is separating.

The configurations containing v are excluded exactly by four conditions:
- **(Dc)** no i with d_{i−1} = d_i = d_{i+1} = 5 (diamond with centres v and x_i);
- **(Tc)** no i with d_i = 6 and d_{i−1} = d_{i+1} = 5 (2.122 with centres x_i (degree 6) and v);
- **(Dt)** no i with d_i = d_{i+1} = 5 and deg y_i = 5 (diamond with v a tip);
- **(Tt)** no i with {d_i, d_{i+1}} = {5, 6} and deg y_i = 5 (2.122 with v a tip).

Consequences for the link pattern (from Dc and Tc alone):
- v has at most 3 degree-5 neighbours.
- If it has 3, the pattern is (5,5,≥7,5,≥7).
- A degree-5 or degree-6 link vertex never sits between two degree-5 link vertices.
- So **v has at least 2 neighbours of degree ≥ 6.**

The conditions "a link vertex is in no configuration" add the analogous constraints one ring further out, on y_i and on the outer neighbours of the link vertices.

### 2.2 The lemma is false at radius 1 [data]

The proposed form was "if v and its link lie in no diamond and no 2.122, then no all-DL π-orbit closes". It is refuted by **24 #6811, hole 22**:
- Link 14, 21, 17, 16, 15, with degrees 7, 5, 7, 5, 5.
- The rotation system was checked to have minimum degree 5 and 0 separating triangles.
- Configurations exist only at distance ≥ 2 from v (2.122 with centre 19 at distance 3).
- The class has an all-DL Γ-cycle of length 20, w = +4, recolouring all 23 vertices.

**23 #1109, hole 19**, refutes the weaker "v in no configuration ⇒ no Γ-cycle". Its link degrees are 5,6,6,6,5, and its nearest configuration is a 2.122 at distance 1.

The positive classes with v in no configuration are:

| case | w | nearest configuration |
|---|---|---|
| 22 #370 h1 | +1 | distance 1 |
| 22 #370 h6 | +1 | distance 1 |
| 23 #1109 h19 | +4, Γ | distance 1 |
| 24 #6650 h13 | +4 | distance 1 |
| 24 #6811 h22 | +4, Γ | distance 2 |
| 24 #6814 h6 | +1 | distance 1 |
| 24 #7170 h2 | +2 | distance 2 |

**Radius 2** (no configuration vertex within distance 2 of v) is consistent with the data: no positive class has the hole at distance ≥ 3. But the base count of such holes at orders 22–24 is only 92, with expected positives ≈ 0.07, so this is **uninformative**.

### 2.3 Why no "DL image only if …" lemma of local type can work [proved plus data]

- The facts available at one DL state are:
  - exactly 8 link-touching components (CS C2);
  - K_B(R₊₃s) = K_A(s) (CS E1);
  - the Hex dichotomy (R₊₃ is defined ⇔ Lock2);
  - Lemma R (§1.2).
- These constrain **one** DD step: the new lock 2 must leave x_{j+2} through a B-coloured outer neighbour that x_{j+2} already has, in K_B⁰(s).
- DD steps are common in every link pattern and at every distance from configurations:

  | where v sits | DD/DL at orders 17–22 |
  |---|---|
  | configuration vertex | 0.20 |
  | distance 1 | 0.21 |
  | distance 2 | 0.26 |
  | configuration-free graph | 0.06 (24 of 384) |

- Maximum DL runs:
  - 20 at distance 0;
  - 11 at distance 1;
  - 5 at distance 2;
  - 2 in the order-22 configuration-free graph.
- So the only local-looking signal is that **DL runs shorten as configurations recede**. But the sample at distance ≥ 2 has 50 holes, and a run of 11 already occurs at distance 1.
- An all-DL orbit is a closed loop of DD steps whose support is the whole graph (§1.3). Its closing is a global event.

## 3. Task 3: weaker targets

### 3.1 Positive cycles need DD steps [proved]

Let Z be a π-cycle with filled states. Split it into m unfilled runs and m filled runs, of lengths u_i and f_i, and let N₀ be the number of runs with u_i = 1.

**Run bookkeeping** (EH table):
- In an unfilled run, the first state lacks lock 1 (it was entered by φ_A) and the last lacks lock 2 (it leaves by φ_B⁻¹). The states in between are DL.
- So u_i = DL_i + 2 − [u_i = 1].

**Formula.** By WM, 5w = |Z| − 4F = U_Z − 3F_Z. Hence

  **5w(Z) = #DL(Z) + 2m − N₀ − 3F_Z ≤ #DL(Z) − m − N₀**, since F_Z ≥ m.

**Consequences.**
- w(Z) > 0 forces #DL > m: **some unfilled run contains two consecutive DL states, i.e. a DD step** (R₊₃ maps a DL state to a DL state).
- More quantitatively, a positive Z needs at least m + N₀ + 3(F_Z − m) + 1 DL states.
- Checks: 20 #59 h18 has L = 21, F = 4, #DL = 11, w = 1; 21 #97 h2 has L = 14, F = 1, #DL = 11, w = 2. Both agree.

**For a Γ-cycle,** w = L/5 > 0 always. So "w ≤ 0 for all-DL cycles" is not a weaker target: it is the statement that **no Γ-cycle exists**. That implies R\* for the graph (a targetless class is a union of Γ-cycles, CS C3), and is 4CT-strength on configuration-free graphs (§5.1).

### 3.2 Forcing three consecutive degree-5 neighbours: false [data]

The statement "an all-DL π-cycle forces three consecutive degree-5 link vertices or a diamond at v" fails three times:
- 22 #418 h21 (6,5,6,5,5: 2.122 only);
- 23 #1109 h19 (5,6,6,6,5: nothing at v);
- 24 #6811 h22 (7,5,7,5,5: nothing within distance 1).

### 3.3 Connection to H, HP and R5³ [proved, elementary]

| theorem | hypothesis | why that makes v a diamond centre |
|---|---|---|
| H, HP | at most one neighbour of degree ≥ 6 | at least four degree-5 neighbours, so three consecutive |
| R5³ | three consecutive degree-5 neighbours x_{i−1}, x_i, x_{i+1} | (v, x_i) is a diamond centre pair with tips x_{i±1}, which are non-adjacent by §2.1 |

- So **every audited R\*-type theorem applies only at holes that are diamond centres.** On a configuration-free graph they are all vacuous.
- By §2.1, every degree-5 hole there has at least two neighbours of degree ≥ 6. That is precisely the BountyBoard's open case, where core-class states of radius 5 were found.
- So the hybrid route's remaining lemma lives entirely in the regime no current theorem touches.
- Also [data]: bounded radius does not bound winding. Holes covered by H and R5³, with pattern 5,5,5,5,5 (17 #4, 22 #649, 24 #906), carry Γ-cycles. A radius bound only says the class is not targetless.

## 4. How much evidence does the data give for P? [data]

**Configuration-free graphs are rare and holes are almost all configuration vertices.**

| order | graphs | configuration-free graphs | degree-5 holes | configuration vertices |
|---|---|---|---|---|
| 22 | 649 | 1 | 9,442 | 9,153 (96.9%) |
| 23 | 2,054 | 1 | 30,829 | 29,499 (95.7%) |
| 24 | 7,209 | 4 | 111,492 | 105,061 (94.2%) |

The positive side matches this base rate: 116 of 123 (94.3%), and 108 of 108 graphs.

**Negative side.**
- Configuration-free gentri graphs have 81 holes. At about 0.08% per hole the expected number of positives is about 0.06, so seeing 0 has probability about 0.94 under the null.
- IPR duals have 425 holes at n = 32–44.
  - The per-hole rate there is unknown; the per-graph rate rises with n.
  - Every IPR hole has an all-degree-6 link, a pattern class with 0 positives in 492 base holes at orders ≤ 24.
  - So the IPR result is equally explained by "positive needs a degree-5 neighbour". That is an alternative hypothesis, also untested.
- **Conclusion:** the data are compatible with P but give it almost no support. The lead stands as a formulation, not as a signal.

## 5. Task 4: what remains, and could P be false?

### 5.1 P is exactly 4CT-strength [proved, given D-reducibility of the two configurations]

Let T be a minimal counterexample to 4CT. Then:
- T is a core triangulation (classical).
- T contains no diamond and no 2.122, since both are D-reducible: Birkhoff, and RSST's list.
- For a degree-5 vertex v, T − v is 4-colourable, but every Kempe class of T − v is targetless, else the colouring extends.
- By CS C3 and Theorem W (QW), each class is a nonempty union of Γ-cycles, all with w = L/5 > 0.

So P fails at T. **P, and even its existential form P∃ ("some degree-5 hole has no positive cycle"), implies 4CT.**

The same argument shows that any statement excluding Γ-cycles in configuration-free graphs implies 4CT.
- A proof of P would be a 4CT proof with an unavoidable set of two configurations plus a Kempe argument at one vertex.
- That argument must be global: it has to see the whole support of a Γ-cycle (§1.3).

### 5.2 What remains

Everything in P. Specifically, one of the following would have to be proved:
- **(P-Γ)** a configuration-free core triangulation has no Γ-cycle at any degree-5 hole (4CT-strength by itself);
- **(P-mixed)** no mixed positive cycle. By §3.1 this needs control of DD-step density along a cycle: #DL ≤ m + N₀ + 3(F_Z − m).

### 5.3 Could P be false at larger orders?

Yes; nothing seen rules it out.
1. Γ-cycles exist whose hole has no configuration within distance 1 (24 #6811). Positive cycles occur at distance 2 from the nearest configuration. The configurations present are always far from where the locks run (§1.1), so their role, if any, is global.
2. The sample is tiny and biased:
   - 6 small configuration-free graphs;
   - IPR duals, whose degree-5 vertices are pairwise non-adjacent. That is a regime where even ordinary DL runs are short, with run length 2 in the order-22 configuration-free graph.
   - Configuration-free core triangulations with **adjacent** degree-5 vertices are allowed. Examples: pattern (5,5,≥6,≥6,≥6) with apexes of degree ≥ 6, or (5,5,7,5,7). They exist at larger n and are untested; the Studio's order-25/26 and full-IPR runs do not cover them.
3. P quantifies over **every** hole and every class, which is far more than the hybrid frame needs (one hole, and only "not targetless"). A single positive cycle in any configuration-free graph refutes P without touching R\*.
   - **The safer target is P∃-R\*:** some degree-5 hole of each configuration-free core triangulation has no targetless class.
4. The zeros of §1.4 (5,5,5,5,6 and 5,5,5,6,6) show that link geometry can suppress positivity **inside** configurations. So "configuration ⇒ positivity possible" is not the right causal reading either.

**Recommended tests** (Studio; not run here: no plantri, and the single-core limit):
- configuration-free core triangulations at n = 26–34 with adjacent degree-5 pairs, random-flip generated, at every hole;
- the 5,5,5,5,6 zero at orders 25–26: if it persists, try to prove it by hand. It is local, and it would be the first positivity-excluding statement tied to a link pattern.

## 6. Status table

| Item | Status |
|---|---|
| Occ-free conditions at v: (Dc), (Tc), (Dt), (Tt); at least 2 high neighbours | [proved] |
| H, HP and R5³ apply only at diamond centres, so they are vacuous on configuration-free graphs | [proved] |
| Lemma R (degree-5 m forces the lock exits) | [proved] |
| 5w = #DL + 2m − N₀ − 3F; positive ⇒ DD step | [proved] |
| P (and P∃) ⇒ 4CT, via D-reducibility | [proved] |
| Local lemma at radius 1 | **false** (24 #6811 h22) [data] |
| "Γ-cycle ⇒ three consecutive 5s or a diamond at v" | **false** [data] |
| Symmetry carries Γ-cycles | only at the D₅ graphs [data] |
| Γ-cycle support = all of T − v; L = 20 at orders ≤ 24 | [data] |
| Γ-length ≡ 0 mod 20 | [conjecture] |
| 108/108 and 116/123 | at base rate [data] |
| 5,5,5,5,6 and 5,5,5,6,6 have no positive class (0 of 20,762 holes) | [data], unexplained |
| P | [conjecture], weakly supported |

## 7. Reproduction (session scratchpad, not committed)

The scripts use `longtable/local-runs/common/kempe_py.py`, `22-winding-escape/escape.py` (π, λ, DL) and `24-positive-vs-config/conf.py`. Graphs come from `studiointel/gentri/triN.txt`. All runs are single core and were run on AC power.

| script | what it does | run time |
|---|---|---|
| `pat.py` | link patterns and v's configuration roles for run 24's `task1.json` | seconds |
| `runs.py N full\|base` | per degree-5 hole: distance to a configuration and link pattern; with `full`, also π-cycles, #DL, #DD, max DL run, max w | orders 17–21 in 25 s, 22 in 90 s; 23–24 base only |
| `an.py`, `an2.py`, `an3.py` | tables of §1.4, §2.3 and §4 | seconds |
| `g17.py`, `paths.py` | 17 #3 Γ-cycle lock chains and colourings; the ρ² test | seconds |
| `gam.py`, `aut.py` | Γ-cycle support and the automorphism test at the 9 cases | seconds |
| `vfree.py`, `chk.py` | positive holes outside configurations; core check of 24 #6811 | seconds |
| `a7.py` | adversarial run_dd graphs all contain configurations (A7: hole 22 is a diamond centre), so they are consistent with P | seconds |
