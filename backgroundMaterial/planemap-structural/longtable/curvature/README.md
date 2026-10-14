# Curvature near vs far from the hole, against locked-run length (exploratory, 14 Oct 2026)

**Prompted by** Kyle's look at the Gears skin: the densely packed centre looks like friction, and the hole sits
next to a freer region.

**Graph-intrinsic version.** Use curvature, i.e. degree-5 vertices (6 − deg > 0), counted at each distance from
the hole.

**Data.** Order-33 frame census, 979,741 holes. Script: `curv.py`; output: `curv-out.txt`.
- Difficulty measures: R, the longest interior π-run (locked run); NR; and mf, the minimum class F/N.
- All taken from `Census33/out/eval-33.jsonl.gz`.

**Findings (correlations only):**
- **More curvature within distance 2 means shorter locked runs.** Mean R falls from 0.81 to 0.60 as the number
  of degree-5 vertices within distance 2 rises from 2 to 14. P(R ≥ 4) falls from 0.47% to 0.
- **More curvature at distance ≥ 3 means longer locked runs.** Mean R rises from 0.80 to 0.93 as that count goes
  from 5 to 14, and P(R ≥ 4) from 0.09% to 0.24%.
- **Floor-tight classes** (mf = 1/4) peak at intermediate curvature (5–6 within distance 2).
- **Consistency:** this matches the wheel results. Degree-5 neighbours make small wheels D-reducible, and the
  flat 66666 hole is the hard case.

**Caveats.**
- Near and far counts are tied together by Euler's fixed total, so they cannot vary independently.
- The effects are moderate.
- Drawing density (Gears tile size) is partly a layout artefact. Curvature is the intrinsic quantity.

---

# Run 2: curvature profile, controls, mechanism and figures (14 Oct 2026, exploratory)

**Bottom line.**
- The near-vs-far effect is real and has the same sign at every order from 28 to 33, and in the game maps. But it is **small**.
- Most of the first-pass gradient (mean R 0.81 → 0.60) came from the hole's own neighbour word, not from curvature further out.
- The "Gauss law" picture is **exact as a parity law**: a lock is shut exactly when its chain holds an odd amount of curvature.
- The *amount* of curvature inside a lock chain does not drive difficulty. Chain size does.

Labels: **[hand]** = derived by hand; **[data]** = computed here.

## 1. What curvature is (plain words)

Build the map out of equilateral triangles: each region is a dot, and each pair of neighbours is joined.
- Around a dot with 6 triangles the sheet lies flat.
- With 5 triangles there is a 60° gap. Closing it makes a cone, so the curvature is **+1** (+60°).
- With 7 triangles there is 60° too much. The sheet buckles into a saddle, so the curvature is **−1**. Degree 8 gives −2, and so on.
- In general, **K(v) = 60°·(6 − deg v)**.

Properties:
- It is a **2-D, intrinsic, point-like** quantity: an ant walking on the surface could measure it.
- **Gauss–Bonnet:** on a sphere, Σ(6 − deg) = 12. Every map carries 12 units of net "charge".
- In the game's region picture (the Gears/Tait cubic map), the curvature sits on the **faces**: pentagons +1, hexagons 0, heptagons −1, octagons −2.

See `figs/c_curvature_explained.png`.

## 2. The shell identity (discrete Gauss–Bonnet for balls around the hole)

Notation:
- B_r = the set of vertices at distance ≤ r from the hole; S_r = the shell at distance exactly r.
- C(r) = Σ_{v∈B_r}(6 − deg v).
- k_r = the number of non-triangular faces of the plane graph induced on B_r (the "holes" of the ball).
- L_r = their total boundary-walk length.
- X_r = the number of edges from S_r to S_{r+1}.

**Exact identity [hand]:**

  **C(r) = 12 − 6·k_r + 2·L_r − X_r.**

Derivation:
- Σ_{B}(6 − deg) = 6|B| − 2E_B − X_r.
- Euler for the connected plane graph B: |B| − E_B + t + k = 2, where t is the number of triangles.
- Edge–face incidences: 2E_B = 3t + L.
- Together these give E_B = 3|B| − L + 3k − 6. Substituting proves the identity.

**Clean-shell corollary [hand]:** suppose the ball is a disc (k = 1) whose boundary S_r is a chordless simple cycle (L = |S_r|), and the annulus to S_{r+1} is a simple strip (X_r = |S_r| + |S_{r+1}|). Then

  **|S_{r+1}| − |S_r| = 6 − C(r).**

- In flat (hexagonal) terrain the shells grow by 6 each step.
- Each unit of curvature enclosed slows the growth by 1.
- Six units stop the growth (a hemisphere). Twelve close the sphere.

**Verification [data]** (`run2/gb.py`, `run2/gb-out.txt`):
- The general identity has **0 failures in 115,543 balls**: every 50th degree-5 hole of orders 28–33, all radii.
- The clean law holds at **100% of balls at r = 1 and r = 2**.
- On all 979,741 order-33 holes, |S_3| = 17 − C(1) − C(2) holds at every hole (`run2/ana-out.txt`).
- At r = 3 the shells start to fold as the sphere closes up. The clean form holds at 31% of balls; the residual is always ≤ 0 at r = 3. At r = 4 the residual spreads from −3 to +1.
- Hole eccentricity is only 4 (64%) or 5 (36%), so "far" means shells 3–5.

**Reading.** C(2) is the same thing as the size of the third shell, given the word. Large near curvature means the hole sits near a *cap* (a pole of the sphere). Small near curvature means the hole sits on a flat plateau whose curvature lies at its rim.

## 3. Effect sizes (order 33, 979,741 holes) [data]

Scripts and output: `run2/feat.py` → `run2/ana.py` → `run2/ana-out.txt`.

Method:
- SEs are cluster-robust by graph.
- **A** = pooled regression with hole-word fixed effects plus #vertices of degree ≥ 7.
- **B** = within-graph regression with graph fixed effects plus word fixed effects. All graph totals are absorbed.
- Given the word and the graph, "near" and "far" are one degree of freedom, since C(2) + far = 12 − C(1). So C(2) is the single predictor.

| outcome (mean) | per +1 of C(2), A | per +1 of C(2), B | partial r, B |
|---|---|---|---|
| R (0.867) | −0.0132 [−0.0144, −0.0120] | −0.0173 [−0.0185, −0.0161] | −0.030 [−0.032, −0.028] |
| P(R ≥ 3) (0.85%) | −0.06 pp [−0.08, −0.04] | −0.06 pp [−0.08, −0.04] | −0.007 |
| P(R ≥ 4) (0.08%) | −0.018 pp [−0.024, −0.012] | −0.019 pp [−0.026, −0.013] | −0.006 |
| NR (1.72) | +0.009 [+0.007, +0.010] | −0.011 [−0.012, −0.009] | −0.014 (sign not robust) |
| min class F/N (0.495) | +0.0002 | +0.0008 [+0.0007, +0.0009] | +0.018 (negligible) |
| floor-tight, mf = 1/4 (0.87%) | +0.00 pp | +0.03 pp | ≈ 0 |

Further results:
- **Logistic regression** (case-control: all cases plus 150k controls; word dummies plus deg-7+ count; cluster-robust):
  - **P(R ≥ 4): OR 0.80 per +1 of C(2), 95% CI [0.74, 0.86].** That is 0.74 per SD (1.33).
  - P(R ≥ 3): OR 0.93 [0.90, 0.95].
  - mf = 1/4: OR 1.00 [0.98, 1.03].
- **Size of the effect.** The relative effect on the rare long-lock tail is meaningful, but the variance explained is tiny.
  - Raw corr(C2, R) is −0.073. After word control it is −0.022.
  - The first pass's "deg-5 within 2" is dominated by the hole's own neighbours.
- **Positive and negative charge both count.** Within-graph slopes for R are −0.024 per extra pentagon at distance 2 and +0.010 per unit of negative charge at distance 2. Both have the sign that net curvature predicts.
- **C(3) beyond C(2)** has a small coefficient whose sign is unstable.
- **The 25 all-DL π-cycles** sit at holes with mean C(2) 4.56, against a word-matched expectation of 4.67. There is no signal.
- **Orders 28–33** (`run2/orders.json`, Fig. a panel D): the within-graph slope of R on C(2) is negative at all six orders. It is significant at 30–33, ranging −0.017 to −0.033 (partial r −0.03 to −0.05). At 28–29 the CIs include 0.
- **Deep game maps** (`run2/game.py`, `run2/game_ana.py`, `run2/game-ana-out.txt`): 24 maps of order 17–34, 368 degree-5 holes, exact HoleGame swap distances. Correlations with C(2) within a map:
  - worst-start swaps: **−0.18 [−0.28, −0.07]**;
  - mean swaps: −0.17 [−0.27, −0.06];
  - longest DL run: −0.20 [−0.30, −0.09].
  - These CIs assume holes are independent.
  - The designated level holes have lower C(2) than the other holes of their maps (5.00 vs 5.54).
  - Counter-example: c30's 55555 hole has C(2) = 6 and still carries an all-DL π-cycle.

## 4. Mechanism test: curvature inside the lock chains [data]

Scripts and output: `run2/mech.py`, `run2/mech_ana.py`, `run2/mech-out.txt`; sample in `run2/mech-sample.txt`.

Sample: 2,391 order-33 holes (all 791 with R ≥ 4, plus 400 at each of R = 0..3), giving 8.2M unfilled states and 1.71M DL states. The engine is `~/4square/kempe_engine.HoleGame`.

- **Parity law, exact: 0 mismatches in 8,210,473 unfilled states.**
  - The engine's lock 2 is shut ⇔ Q(K_{αγ}(x2)) is odd. This is the π-swap chain, TrackF's K_{αA}(x_{j+2}).
  - Lock 1 ⇔ Q(K_{αδ}(x2)) is odd.
  - In every DL state, K_{αβ}(x2) and both lock chains (x1–x3 and x1–x4) also hold odd Q.
  - This re-confirms TrackF Lemma LP on a new sample.
- **Amount of curvature, beyond parity, hardly matters:**
  - Q in the π-chain is 1 in 31% of DL states, 3 in 30%, 5 in 20%, and negative in 5.5%.
  - Whether the π-swap leaves the state DL (P = 0.25 overall) depends mainly on the **size** of the π-chain: 0.41 for 2–5 regions, 0.05 for 14+.
  - Logistic regression, log-OR per SD: size −1.39, Q −0.03, mean distance from the hole +0.63 (naive SEs).
  - At fixed size, extra curvature lowers continuation only modestly, and only for small chains.
  - The distance to fill at DL states is ≈ 2 (mean 2.01) and is uncorrelated with any chain's Q (|r| ≤ 0.04).
- **Does near curvature act through the chains?**
  - At the hole level, high C(2) sharply cuts the share of DL states whose π-chain must reach ≥ 3 steps for its nearest pentagon (r = −0.46).
  - But this "reach" variable does **not** mediate the effect on R. The within-word slope of R on C(2) moves only from −0.106 [−0.173, −0.047] to −0.099 [−0.165, −0.039].
  - Note that this is a stratified sample, so these slopes are not population effects.
- **Verdict on the hydraulic picture.**
  - Charge works as a **mod-2 conservation law** that decides which locks are shut. That part is exact.
  - "More pressure" (more curvature) inside a chain does not make the lock harder. The geometry that matters is chain size.
  - The near-curvature effect on R is real, but this analysis does not identify its mechanism.

## 5. Figures (`figs/`, PNG + SVG)

- `a_radial_profile`: four panels.
  - (A) mean R against C(r), r = 1..4.
  - (B) P(R ≥ 4) against C(2), raw and word-adjusted, with the odds ratio.
  - (C) the Gauss–Bonnet shell-growth law: exact on the line at r = 1, 2, folding below it at r = 3.
  - (D) the slope at each order, 28–33.
- `b_maps_curvature`: six game maps, regions coloured by curvature (red +, white 0, blue −), with the hole and distance-shell contours drawn.
  - r178: record hole (hard) vs its easiest hole.
  - r210: deepest hole vs its easiest hole.
  - six (flat 66666 hole) and c30 (55555 hole, all-DL cycle).
  - The hard holes have C(2) of 5 and 4; the easy ones have 7.
- `c_curvature_explained`: angle defect (5 / 6 / 7 triangles), and the "six" map shown as a triangulation (curvature at dots) and as the Gears/Tait region map (curvature on faces).
- `d_lock_chains_r178`: four consecutive states along the longest locked run at r178 hole 10 (21 DL states). The two parity chains of x2 are overlaid, with their enclosed curvature (odd ⇒ lock shut). Colours are normalised so that the rim always reads α β α γ δ.
- `e_mechanism`: (A) Q distribution in the chains (all odd); (B) run continuation against chain size, split by Q; (C) near curvature against how far the π-chain must reach.

## 6. Game feature suggestions

- **Supported (exact):** a "charge counter" on a highlighted chain. When a player selects or hovers a chain at the hole's rim, show the number of pentagons (+) and 7+ regions (−) inside it, and its parity. Odd means that lock is shut.
  - This is Lemma LP, so it is a true, teachable rule.
  - It makes the Gears picture's "pressure" intuition precise: what matters is parity, not amount.
- **Weakly supported:** an optional "terrain" skin shading regions by curvature (red pentagons, blue heptagons), with faint distance rings around the hole.
  - It is a good explanatory overlay. The cap-vs-plateau reading is real.
  - As a difficulty *hint* it is weak. Near curvature lowers the odds of a long lock by about 20% per unit, but it explains well under 1% of the variation. Do not promise players that "flat around the hole = hard".
  - Level design could still use C(2) as a mild filter when looking for hard holes.

## 7. Run notes

- Every run used `nice -n 10`, at most 3 processes, and each finished within 15 min. The machine was on AC power at 100% battery.
- The feature arrays (`f28..f33.npz`, about 22 MB) were written to the session scratchpad and not committed. Regenerate them with `run2/feat.py ORDER OUT.npz`.
- Inputs:
  - Census33 eval and frames;
  - TrackO `frame-NN.jsonl` for R and NR at orders 28–32;
  - Census29 `eval-NN.jsonl` for minfrac;
  - `~/4square/maps`, `layout.js`, `levels.js`.
- Every number here is exploratory **[data]**, except the shell identity, which is **[hand]** with a data check.
