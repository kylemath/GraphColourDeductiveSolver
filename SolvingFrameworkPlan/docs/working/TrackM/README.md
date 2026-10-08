# Track M: guided Kempe-swap escape from stuck states [exploratory, data]

Studio, 8 Oct 2026, 01:56–03:45. Idea from the project owner. Nothing here is committed, and nothing outside `TrackM/` was changed. Track A's `kempe_py` engine and TrackF/Census29/historical-trap graph files were read, never modified.

Labels:
- **[data]**: computation.
- **[hand]**: a short argument written here, not reviewed.

Compute: at most 4 worker processes, all under `nice -n 10`, about 1 h 50 min of wall time. Load from other users was 12–19.

## 0. Bottom line

1. **The simple "discharge" scores do not work on their own.** On the sphere, every pure score rule fails within 10 swaps on some doubly-locked (DL) start. That covers ΔN, Δℓ, lock-chain size or length, winding, curvature charge Σ(6 − deg) along K, distance from K to the hole, and |K|, each tried in both directions (§3). The best pure score is "shortest lock chains" (min-llen), with 2,895 failures out of 5.4M DL starts. Directional sector sweeping (DIR) fails 1,267 times and needs up to 10 swaps.
2. **What works is lock descent, Φ = L1 + L2, with one specific tie-break.**
   - Rule **Φ>π**: take a filling swap if one exists; otherwise take a swap to a state with the fewest locks; if every neighbour is still DL, apply π.
   - The variants **Φ>min-wind / Φ>max-wind** come to the same thing: prefer the swap that rotates the repeat position by −2 or +2, which is π or π⁻¹.
   - This rule **never fails on any sphere data**: 5.37M DL starts in pass 1 (as Φ>min-wind) and 2.65M in pass 2 (as Φ>π itself; mostly a re-run subset of the pass-1 starts), covering census orders 22–32, the 17 census all-DL π-cycles, IPR fullerene duals, the AW/BV adversarial graphs, and Heawood/Errera/Kittell/Poussin/HoG1152.
   - It still never fails when the tie-break among the remaining choices is **adversarial** (exhaustive over every tie choice: Φ>π-ADV, Φ>min-wind-ADV).
   - **Worst case: 7 swaps.** The optimum (BFS distance) is at most 4 everywhere.
3. **Plain Φ-descent is not enough.** With a random tie-break, lock descent fails 1,370 times (BV, plus one census-30 start). Against an adversarial tie-break it fails 37,028 times: the walk wanders and gets trapped in plateaus of DL states whose neighbours are all DL. These plateaus have up to 192 states in BV, up to 18 in census 30, and up to 7 in census 22–28.
4. **Failure anatomy [data]:**
   - Every failure of every Φ-based rule starts at a **Heawood-trap state**: Kempe's 1879 double swap fails in both orders, and in both orders the first swap cuts the lock chain that was blocking the second (interference_both = n in every row of `out/summary*.txt`).
   - The failing walks spend their whole budget at Φ = 2.
   - A Heawood trap is necessary for a failure but far from sufficient: 36% of census DL states are literal Heawood traps (§6), while failures are about 10⁻⁴.
5. **Candidate lemma (data, 4CT-strength; §4).** π-run bound: on a triangulated sphere, at a degree-5 hole, no π-orbit contains more than R consecutive interior DL states (DL states all of whose Kempe neighbours are DL).
   - Observed R: ≤ 4 on census 27–32 (pass-2 sample), 3 on the cycle graphs, traps and IPR duals, 4 on AW, 5 on BV.
   - [hand] R finite ⇒ rule Φ>π reaches a filled state within R + 2 swaps from every unfilled state ⇒ PureClean ⇒ 4CT. The data match R + 2 exactly: worst counts are 7 on BV, 6 on census 29/30, 5 on census 32, 4 on census 31.
6. **Off the sphere the rule fails, and not only in targetless classes.**
   - Φ>π fails at 136 / 328,740 starts of TrackF's torus/Klein/RP² cycle graphs, and 6 / 52,227 on the 555 cycle graphs, all inside classes that do contain filled states.
   - There, interior π-runs reach 9, BFS distances reach 9–13, and D2 can fail, so π is undefined at some DL states.
   - In targetless classes every rule fails, as it must (59 + 2 starts in the cycle sets, 2,028 in the census torus/RP²/Klein samples).
   - So "fails exactly where there is no filled state" holds on the sphere, trivially, since there are no targetless classes there. Off the sphere the rule also fails in filled classes within 10 swaps. The k = 10 cap is binding there: the optimum alone fails at 4 torus starts with dF > 10.

## 1. Setup [definitions]

- **States, moves, engine.** States are proper 4-colourings of T − h up to renaming, where h is a degree-5 hole. A move is a whole-component Kempe swap in T − h; renamings are dropped. The engine is `kempe_py.Space` (bitmask, stdlib), and all features are computed in `tm_lib.py`. No planarity is assumed, so the same code runs on the torus, Klein bottle and RP².
- **Frame of an unfilled state.** As in TrackG and LockParity.md: link (α, μ, α, A, B) at x_j … x_{j+4}.
  - L1 = x_{j+3} ∈ K_{μA}(x_{j+1}), and L2 = x_{j+4} ∈ K_{μB}(x_{j+1}).
  - **Φ = L1 + L2**, with Φ = −1 for a filled state. DL means Φ = 2.
- **Moves used by the rules.**
  - π = swap K_{αA}(x_{j+2}), defined iff x_j ∉ it.
  - π⁻¹ = swap K_{αB}(x_j), defined iff x_{j+2} ∉ it.
  - σ = swap K_{αμ}(x_{j+2}).
- **Kempe 1879 at a DL state.** K1 = K_{αB}(x_{j+2}) (x_{j+2} → B) and K2 = K_{αA}(x_j) (x_j → A).
  - *Literal* (Kempe's text): swap both at once. It succeeds iff the result is proper. Heawood's objection is exactly the case where it is not.
  - *Sequential*: swap K1, then recompute K2 in the new colouring (and the mirror order). *Interference* means that swap 1 broke the lock chain that blocked swap 2.
- **Lemma A [hand, any surface].** An unfilled state that is not DL has a filling swap. If, say, ¬L1, swap K_{μA}(x_{j+1}); then x_{j+1} becomes A and the link uses 3 colours.
  - Hence every rule that takes Φ-decreasing moves faces exactly one problem: leaving DL.
  - [data, + hand sketch] No DL state is adjacent to a filled state: k ≤ 1 success = 0 for every DL start. The case check: the only single swaps that change one link colour to a non-adjacent link colour are the two lock-chain swaps K_{μA}(x_{j+1}) and K_{μB}(x_{j+1}), which L1 and L2 block. Every other swap through a link vertex drags an adjacent link vertex along.
- **Score features** (computed after a trial flip, in the target's own frame):

| name | meaning |
|---|---|
| N / ell | ΔN (total chains; merges < 0 < splits) / Δℓ (link-free chains; at DL states N = 8 + ℓ, TrackJ J1) |
| lsize / llen | \|K_{μA}(x_{j+1})\| + \|K_{μB}(x_{j+1})\| / shortest-path lengths of the lock chains |
| wind | signed change of the repeat position j, in {−2, …, 2}. π has Δj = −2 and π⁻¹ has Δj = +2. It is the move-level version of Theorem W's λ. |
| curv | Σ_{v∈K}(6 − deg v), the curvature charge along the chain |
| dist | min_{v∈K} d_T(h, v) |
| size | \|K\| |
| rim colours | number of distinct link colours. This only distinguishes filling moves (every unfilled state has 4), so it equals the fill check below. |

- **Rules** (`tm_lib.RULES`, `RULES2`). Every rule takes a filling swap if one exists. Every rule except KEMPE, BEAM and OPT is tabu (never revisits a state in its walk). The step budget is k = 10.
  - Pure scores: `min-X` / `max-X` for each X above; `sigma` (prefer σ); `RAND`.
  - Lock descent: `PHI`, then `PHI>X` (lexicographic: Φ of the target first, then X), `PHI>pi`, `PHI>piinv`, `PHI+sigma`, and combinations `PHI>lsize>N`, `PHI>sigma>lsize`, `PHI>dist>curv`.
  - `KEMPE`: a single filling swap, or else the sequential double swap at DL.
  - **(b) beam:** `BEAMb+w` keeps the b best and the w worst children by (Φ, lsize, −N), with global pruning of visited states; tested as (2,0), (2,2), (4,4).
  - **(c) directional:** `DIR` uses cells (radius r, sector). The sector is the nearest link vertex, counted from x_j. Chains are anchored at their vertex nearest the hole. The sweep runs radius-major and restarts at the hole after each swap; within a cell it takes the best chain by (Φ, lsize).
  - Robustness checks: `-ADV` rules are exhaustive over every tie choice, so the result is the worst case over tie-breaks. `#1` and `#2` are other random seeds.
  - `OPT` is the BFS distance to a filled state (the optimum).

## 2. Data

| set | graphs / holes | DL starts (pass 1) | notes |
|---|---|---|---|
| census 22–27, 28, 29, 30 | 43 / 639, 104 / 1,563, 296 / 4,533, 590 / 9,267 | 64k, 249k, 996k, 2.70M | orders 22–29 exhaustive; order 30 one half (`--stride 8`, offsets 0–3) |
| census 31, 32 (pass 2 only) | 10 / 175, 7 / 119 | 62k, 64k | small partial samples; the full-sample jobs were stopped for time |
| cyc13 | 13 / 220 | 108k | every hole of the 13 census graphs carrying the **17 all-DL π-cycles** (340 cycle states) |
| ipr | 27 / 81 | 433k | IPR fullerene duals n ≤ 43 (C60–C82), 3 holes each (66666), all DL starts plus a sample; n ≥ 44 is too big for the Python enumeration |
| aw | 3 / 63 | 123k | `jobaw/counterexamples.txt` (100 cycle states) |
| bv | 12 / 267 | 689k | `jobbv/graphs/*.json` (19,480 all-DL-cycle states; interior plateaus up to 192 states) |
| traps | Heawood 1890, Errera, Kittell, Poussin (+ HoG1152 in pass 2) | 1.7k | §6 |
| off_cyc / off_cyc555 | 421 / 604, 65 / 82 | 131k, 17k | TrackF cycle graphs (torus, Klein, RP²), cycle holes only |
| off_torus / rp2 / klein | 150 / 300, 150 / 300, 75 / 150 | 34k, 92k, 15k | samples of TrackF's census graphs, which contain targetless classes |

- Pass 1 ran every rule of `RULES`.
- Pass 2 ran the π-family and the adversarial checks (`RULES2`) on census 27, 28, the 29 half, the 30 eighth, the 31/32 samples, cyc13, ipr, aw, bv, traps and off_cyc(555).

## 3. Results: rules × success [data]

**Sphere, DL starts (pass 1, 5,367,027 starts).** Each k column is the share of starts that reach a filled state within k swaps; "fails" counts starts not filled within 10 swaps. Non-DL starts are always filled in 1 swap (Lemma A).

| rule | k ≤ 2 | k ≤ 3 | k ≤ 4 | k ≤ 6 | k ≤ 10 | fails | worst |
|---|---|---|---|---|---|---|---|
| OPT (optimum) | 0.9888 | 0.9996 | 1 | 1 | 1 | 0 | **4** |
| **PHI>min-wind** (= Φ>π) | 0.9888 | 0.9984 | 0.9993 | 1.0000 | 1 | **0** | **7** |
| PHI>max-wind (= Φ>π⁻¹) | 0.9888 | 0.9984 | 0.9993 | 1.0000 | 1 | **0** | 7 |
| BEAM4+4 | 0.9888 | 0.9996 | 1.0000 | 1.0000 | 1 | 0 | 9 |
| BEAM2+2 | 0.9888 | 0.9993 | 0.9999 | 1.0000 | 1.0000 | 15 | 10 |
| BEAM2+0 | 0.9888 | 0.9977 | 0.9989 | 0.9994 | 0.9998 | 827 | 10 |
| PHI>min-dist | 0.9888 | 0.9966 | 0.9986 | 0.9995 | 0.9999 | 677 | 10 |
| PHI>dist>curv | 0.9888 | 0.9968 | 0.9987 | 0.9995 | 0.9998 | 940 | 10 |
| PHI>min-curv | 0.9888 | 0.9957 | 0.9978 | 0.9991 | 0.9998 | 1,084 | 10 |
| PHI (random tie-break) | 0.9888 | 0.9955 | 0.9976 | 0.9991 | 0.9997 | 1,370 | 10 |
| DIR (directional) | 0.9002 | 0.9734 | 0.9898 | 0.9978 | 0.9998 | 1,267 | 10 |
| PHI+sigma | 0.9888 | 0.9935 | 0.9967 | 0.9985 | 0.9996 | 2,170 | 10 |
| PHI>max-N | 0.9888 | 0.9963 | 0.9979 | 0.9990 | 0.9995 | 2,447 | 10 |
| PHI>min-llen | 0.9888 | 0.9979 | 0.9987 | 0.9992 | 0.9995 | 2,795 | 10 |
| min-llen (pure) | 0.9832 | 0.9978 | 0.9987 | 0.9992 | 0.9995 | 2,895 | 10 |
| PHI>min-lsize | 0.9888 | 0.9961 | 0.9976 | 0.9988 | 0.9993 | 3,936 | 10 |
| min-lsize | 0.9604 | 0.9901 | 0.9943 | 0.9968 | 0.9980 | 10,572 | 10 |
| min-dist | 0.6716 | 0.8829 | 0.9473 | 0.9847 | 0.9966 | 18,155 | 10 |
| PHI>max-dist | 0.9888 | 0.9923 | 0.9930 | 0.9936 | 0.9946 | 29,014 | 10 |
| PHI-adv (Φ, adversarial ties) | 0.9888 | 0.9915 | 0.9923 | 0.9928 | 0.9931 | 37,028 | 10 |
| RAND | 0.5741 | 0.8099 | 0.9042 | 0.9682 | 0.9922 | 42,012 | 10 |
| min-wind (pure) | 0.7995 | 0.9157 | 0.9647 | 0.9882 | 0.9921 | 42,511 | 10 |
| sigma | 0.5947 | 0.8244 | 0.8987 | 0.9640 | 0.9917 | 44,339 | 10 |
| max-size / min-size | 0.65 / 0.66 | 0.86 / 0.85 | 0.92 / 0.91 | 0.97 / 0.96 | 0.990 / 0.986 | 56k / 77k | 10 |
| max-N / min-N | 0.59 / 0.59 | 0.82 / 0.83 | 0.91 / 0.91 | 0.965 / 0.961 | 0.988 / 0.978 | 66k / 118k | 10 |
| max-curv / min-curv | 0.63 / 0.56 | 0.84 / 0.79 | 0.91 / 0.88 | 0.96 / 0.95 | 0.985 / 0.980 | 82k / 107k | 10 |
| KEMPE (1879, sequential) | 0.9248 | — | — | — | 0.9248 | 403,748 | 2 |
| max-dist | 0.3145 | 0.5067 | 0.5982 | 0.7134 | 0.8092 | 1.02M | 10 |
| max-lsize / max-llen | 0.19 / 0.07 | 0.32 / 0.17 | 0.40 / 0.25 | 0.52 / 0.38 | 0.65 / 0.55 | 1.85M / 2.44M | 10 |

(Δℓ rules coincide with ΔN rules exactly, as J1 predicts at DL states.)

**Sphere, starts on all-DL π-cycles (19,960 states, 340 of them on the 17 census cycles).**

| rule | k ≤ 2 | k ≤ 3 | k ≤ 4 | k ≤ 10 | fails | worst |
|---|---|---|---|---|---|---|
| OPT, BEAM4+4, BEAM2+2 | 0.61 | 0.99 | 1 | 1 | 0 | 4 |
| PHI>min-wind / PHI>max-wind | 0.61 | 0.97 / 0.96 | 0.98 / 0.97 | 1 | 0 | 7 |
| min-llen, PHI>min-llen | 0.59 / 0.61 | 0.96 | 0.98 | 1 | 0 | 9 |
| PHI>min-dist | 0.61 | 0.86 | 0.95 | 1 | 0 | 10 |
| PHI | 0.61 | 0.80 | 0.90 | 0.998 | 45 | 10 |
| sigma | 0.51 | 0.53 | 0.71 | 0.94 | 1,225 | 10 |
| KEMPE | 0.06 | — | — | 0.06 | 18,681 | 2 |
| min-N, max-lsize, max-llen | < 0.03 | | | < 0.06 | ≈ 19k | 10 |

**Pass 2 (2,653,349 DL starts; census 27–32, cyc13, ipr, aw, bv, traps).**

| rule | fails | worst | per set (worst) |
|---|---|---|---|
| OPT | 0 | 4 | 3–4 |
| **PHI>pi**, PHI>piinv, PHI>pi>min-wind | **0** | **7** | census27 5, census28 5, census29 6, census30 6, census31 4, census32 5, cyc13 5, ipr 5, aw 6, bv 7, traps 5 |
| **PHI>pi-ADV** (adversarial over the remaining ties) | **0** | **7** | identical to PHI>pi |
| PHI>min-wind / -ADV, PHI>max-wind / -ADV, seeds #1, #2 | 0 | 7 | |
| PHI>abs-wind (rotate j either way, \|Δj\| max) | 75 (bv) | 10 | |
| PHI-ADV (census 31/32 only) | 0 | 10 | |

The direction matters: always following π, or always π⁻¹, works. Mixing the two directions (abs-wind) fails, because it can walk back along the orbit.

**Kempe 1879 alone.**
- Sequential double swap: fails at 7.5% of sphere DL starts and at 94% of all-DL-cycle states.
- Literal (simultaneous) swap: fails at **36%** of census 22–28 DL states (113,130 / 318,322), and at 16 / 20 states of the p30.r10#1252 cycle (§6).

## 4. Best rule and candidate lemma

**Rule Φ>π.** At an unfilled state c:
1. if a Kempe swap gives a filled state, do it;
2. else, if some swap gives an unfilled state with fewer locks, do one of minimum Φ (any tie-break);
3. else (every neighbour is DL, so c is DL) apply π = swap K_{αA}(x_{j+2}).

Never revisit a state.

**Proposition [hand].** Let T be a triangulated sphere with a degree-5 hole h. Call a DL state *interior* if all its Kempe neighbours are DL. Let R(T, h) be the largest number of consecutive interior states along a π-orbit (R = ∞ if some π-cycle is all interior). If R < ∞, rule Φ>π reaches a filled state from every unfilled state within R + 2 swaps.

*Proof.*
- On the sphere, at a DL state, π is defined, because D2 gives L2 ⇔ x_j ∉ K_{αA}(x_{j+2}) (formal, `QuarterPairDuality` / `NoFrozen`).
- At an interior state u, π(u) is a neighbour of u, so it is DL. The rule follows π, and π is injective, so π(u) is new unless the walk has closed an all-interior π-cycle, which R < ∞ excludes.
- After at most R π-steps the walk is at a DL state with a non-DL neighbour (it has no filled neighbour by step 1). Step 2 moves to Φ ≤ 1 or fills.
- From Φ ≤ 1, Lemma A fills in one swap. A start that is not DL is filled in at most 1 swap. ∎

**Candidate lemma (π-run bound, data).** On every triangulated sphere, at every degree-5 hole, R(T, h) ≤ 5. Equivalently, rule Φ>π fills within 7 swaps.
- Observed maximum R: census 27–32 ≤ 4 (pass-2 sample), cyc13 3, IPR duals 3, traps 3, AW 4, **BV 5** (adversarially searched graphs).
- The worst Φ>π counts equal R + 2 in every set where R was measured.
- **Qualitative version.** Every all-DL π-cycle on a sphere contains a state with a non-DL Kempe neighbour. By the proposition this already implies PureClean, hence R\* and 4CT, so the lemma is **4CT-strength** and should not be expected to be easier than LPC.
  - It is implied by TrackG's σ-escape conjecture (σ is one particular non-DL neighbour).
  - The quantitative bound R ≤ 5 is new data, and it is stronger: it constrains *every* π-run of interior states, not only cycles.
- **Links.**
  - Rigid states (N = 8) have Kempe degree 2 (neighbours π and π⁻¹, TrackJ J4), so a rigid state is interior whenever both of its π-neighbours are DL.
  - TrackJ's NRC (no π-cycle with N ≤ 9) and its observed π-runs ≤ 7 inside {N ≤ 9} are the near-rigid shadow of this bound.
  - A proof route would bound how long π can keep every Kempe neighbour DL, by planar Jordan / band-surgery arguments of the TrackI kind.
- **Not usable as stated off the sphere.** Interior π-runs reach 9 on TrackF's torus/Klein/RP² cycle graphs, D2 fails (so π can be undefined at DL states), and BFS distances reach 13.

## 5. Failure anatomy [data]

- **Where rules fail.** Only at DL starts with dNDL ≥ 2, i.e. no non-DL state within one swap. On the sphere, dNDL ≤ 3 and dF ≤ 4 everywhere.
  - Pure-score rules also fail at dNDL = 1 starts, because they ignore the exit.
  - Every Φ-family failure record has dNDL ∈ {2, 3}.
- **Heawood-type interference is necessary.** In every sampled failure of every rule (sphere: thousands of records, `out/summary*.txt` "Failure anatomy"), the start is a sequential-Kempe trap: both orders of Kempe's double swap fail, and in both the first swap cuts the other lock chain (`interference_both` = n).
  - [hand] Why: if one order of the double swap works, the state after its first swap is unfilled and adjacent to a filled state, so it is not DL (by the case check in §1). Hence dNDL = 1, and Φ-descent exits immediately.
  - The converse fails: about 7.5% of DL states are such traps, while failures are about 10⁻⁴ (Φ) or 0 (Φ>π).
- **Two failure modes:**
  1. *Plateau wandering.* Φ-descent with a random or adversarial tie-break walks inside a connected set of interior DL states and either runs out of its 10 steps (all 1,370 PHI failures) or traps itself under tabu (all 37,028 PHI-adv failures).
     - The plateaus are small in the census: max 4 (orders 22–27), 7 (28), 8 (29), 18 (30).
     - They are large in the adversarial graphs: AW 44, BV 192.
     - The one census failure of PHI (p30.r23#26360, hole 20, a dNDL = 2 start) trapped itself after 5 moves.
  2. *Wrong turn.* Score rules that favour long chains or far chains (max-lsize, max-llen, max-dist) steer away from the exit. Their failures are mostly dNDL = 1 starts that never leave DL.
- **What π does differently.** Inside a plateau π is a fixed direction: it is injective, has no back-tracking, and moves along the orbit that Theorem W winds. It runs out of interior states within ≤ 5 steps on all sphere data.
- **All-DL π-cycles are heavily trapped.** At cycle states:
  - the sequential Kempe double swap fails 94% of the time;
  - in Errera's graph all 40 cycle states are literal and sequential Kempe traps;
  - yet Φ>π leaves every cycle within ≤ 7 swaps and the optimum within ≤ 4, matching TrackG (dS ≤ 2, dF ≤ 3 on census cycles).

## 6. Historical Kempe traps (constructed / verified) [data]

Graphs are taken from `longtable/historical-traps/heawood1890.json` (built from Heawood's 1890 plate via MathWorld; 25 vertices, 69 edges, degrees 5^16 6^5 7^4) and from `studio-explore/historical-traps/{Errera,Kittell,Poussin}.json` (edge lists from Sage `smallgraphs.py`, parsed as data). They were re-checked here as closed triangulations by the face/rotation build (`rot_from_faces`): every edge lies in exactly 2 faces.

- **Heawood 1890** (`out/heawood_colouring.json`). Heawood's own colouring at V has link b, r, y, g, r and is DL.
  - The literal Kempe step fails: K1 = r–g chain {G1, G2, G3, R1, R2, R3} and K2 = r–y chain {R4, R5, R6, Y4, Y5, Y6} are disjoint, but the simultaneous swap is improper (adjacent g→r and y→r vertices).
  - **This reproduces Heawood's objection.**
  - The sequential version succeeds in one order (r–g first). It fails in the other order, because swap 1 breaks the lock chain.
  - dF = 2. Every Φ-rule fills it in 2 swaps.
- **Literal-Kempe failures at DL states:**

| graph | DL states | literal failures | sequential (both orders) failures |
|---|---|---|---|
| Heawood 1890 | 824 | 292 | 26 |
| HoG 1152 (Saaty-type) | 792 | 320 | 44 |
| Errera | 200 | 120 | 60 |
| Kittell | 670 | 361 | 103 |
| Poussin | 38 | 6 | 0 |
| census 22–28 | 318,322 | 113,130 (36%) | 16,358 |

  So all of them are Kempe-trap graphs in the literature's sense: some colouring defeats Kempe's 1879 step. Every one of them is also escaped by Φ>π in ≤ 5 swaps.
- **Errera** carries all-DL π-cycles at 2 of its holes (40 cycle states), every one a literal and sequential trap. It has order 17, below the census range (22–32). Errera is in the core class (min degree 5, no separating triangle); its frame-class status was not checked here.
- **Soifer graph: not built.** It is not in Sage's `smallgraphs.py` (checked), and I have no trustworthy edge list. It is a 9-vertex non-triangulation, so the lock framework would also need a non-triangular link.

## 7. Off the sphere [data]

Fails in classes that contain filled states / starts; TL = starts in targetless classes (every rule fails there):

| rule | off_cyc | off_cyc555 | off_torus | off_rp2 | off_klein |
|---|---|---|---|---|---|
| OPT | 0 / 328,740 (worst 9) | 0 (6) | 4 / 101,260 (dF > 10) | 0 (8) | 0 (10) |
| PHI>pi | 136 | 6 | n/a (pass 1 only) | | |
| PHI>pi-ADV | 886 | 162 | | | |
| PHI>min-wind | 171 | 24 | 1,600 | 611 | 638 |
| PHI | 473 | 59 | 1,416 | 376 | 400 |
| BEAM4+4 | 0 | 0 | 13 | 0 | 1 |
| TL starts | 59 | 2 | 933 | 377 | 718 |

- Off the sphere, the guided rules fail in filled classes too. The sphere-specific ingredients are:
  1. π is defined at every DL state (D2);
  2. interior π-runs are short;
  3. distances are short (dF ≤ 4 on the sphere, against 9–13 off it).
- This is consistent with TrackG (escapes are deeper off the sphere) and TrackH (local facts cannot force LPC).

## 8. Verdict

- **The "discharge read along the chain" idea, as a scalar score, fails.** No geometric chain score (curvature charge, distance, size, chain counts, lock-chain size/length, winding magnitude), in either direction, gives a rule that never fails on the sphere. Directional sector sweeping is no better than random-tie Φ-descent.
- **The ingredient that matters is lock descent (Φ = L1 + L2) plus a consistent direction (π) on DL plateaus.** That rule never fails on 5.4M sphere DL starts (2.65M re-checked as Φ>π), including adversarial graphs and adversarial tie-breaks, and its worst case is 7 swaps against the optimum's 4.
- **The resulting candidate lemma (π-run bound R ≤ 5, or qualitatively "no all-interior π-cycle") is 4CT-strength.** It is a uniform, checkable reformulation of the escape certificate: one named move (π) inside plateaus, any lock-decreasing move at their edge.
- It sits between TrackG's σ-escape (stronger: it names the exit move) and LPC (weaker: it is global).
- **Recommended next steps:**
  - (i) Measure R exhaustively on census 30–32, which is cheap in C. The Python pass-2 sample here covers orders 27–29 fully or half and 30–32 partially.
  - (ii) Try to prove "an interior π-run of length ≥ 6 is impossible on the sphere" in the TrackI/TrackJ style. Interior states are near-rigid: only π, π⁻¹ and link-free swaps, which stay DL.
  - (iii) Push an adversarial search, as in AW/BV, directly on R.

## Files

| path | content |
|---|---|
| `tm_lib.py` | `Hole` (states, frames, Φ, N, ℓ, lock chains, π, π⁻¹, σ, sequential Kempe step, chain features, sectors); rules `RULES` (pass 1), `RULES2` (pass 2), walkers, beam, directional sweep, adversarial (exhaustive tie-break) evaluators |
| `tm_run.py` | driver: every rule from every unfilled start at each hole → JSON line with step histograms by category (U / DL / CYC / TL), failure records, interior-plateau sizes, interior π-run maxima |
| `tm_summary.py` | aggregation → `out/summary.txt` (pass 1: `python3 tm_summary.py`), `out/summary_pass2.txt` (`python3 tm_summary.py out/parts2 out/summary_pass2.txt`) |
| `tm_kempe1879.py` | literal vs sequential Kempe step at DL states → `out/kempe1879.jsonl` |
| `tm_heawood.py` | Heawood's own colouring: trap verification and rule outcomes → `out/heawood_colouring.json` |
| `run_all.sh`, `jobs_main.txt`, `jobs_off.txt`, `jobs_pass2b.txt`, `jobs_pass2_c3132_partial.txt`, `chain2.sh` | the runs (nice 10, ≤ 4 workers) |
| `out/parts/*.jsonl.gz`, `out/parts2/*.jsonl.gz` | per-hole records (pass 1, pass 2) |
| `out/logs/` | per-job stderr |
