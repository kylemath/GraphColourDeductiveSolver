# Gear polarity: what the rim chains' parity can and cannot predict [exploratory]

13 October 2026. Written by a Claude Code agent for the user (the 4square "Gears" skin question). **Exploratory throughout.** Hand arguments are short and unreviewed. Computations are small (under 2 minutes in total, one core, on AC), on saved maps only. No declaration, no WP number, no status words.

Scripts and output: `docs/working/GearPolarity-scripts/` (`gear_polarity.py`, `gp_stats.py`, `gp_jam.py`, `output.txt`). They import the game's own engine `~/4square/kempe_engine.py` (sha256 `1d6f9f93…abd8bc`) and `~/4square/mapio.py` (`fa513038…e5ce25`). No research-team code.

Inputs:
- the 16 triangulated 4square maps (`~/4square/maps/*.json`, the level hole of each; 62,003 states);
- the gentri census files `backgroundMaterial/planemap-structural/studiointel/gentri/tri16–tri20.txt` (4-connected, minimum degree 5; every degree-5 hole; 1,550 holes, 242,755 states).

In total: 1,566 holes, 1,606 Kempe classes, 304,758 states (up to renaming), 29,968 doubly locked (DL) states. "17:1" etc. below are **gentri** line indices, not plantri indices. The 4square maps were chosen for hard levels, so they over-represent deep starts.

## 0. The picture being tested

Each edge is a pill (a gear) with one colour at each end. An (a,b) Kempe swap turns every pill inside the chain 180°. A chain from a rim cell of colour a to a rim cell of colour c has odd length; with the hole's two spokes it closes an odd ring through the hole, so the swap "comes back to the rim with the wrong polarity" and only trades rim colours. A chain joining two rim cells of the same colour closes an even ring. Hypothesis: the parity structure of the rim chains predicts whether a start is fillable within k swaps, and the total polarity count relates to the winding of Theorem W.

## 1. What was done before (so it is not redone)

The "polarity of distant chains" idea has been tested before, in other words:
- **Proposition H** (`NightWindingMeander.md`, night swarm, unreviewed; data 0 failures on 4,246 holes, orders 16–21). Lock 2 *is* an odd crossing parity: the token's dual meander B_T crosses the path C between the two singleton Tait edges an odd number of times. Locally the sign is a product of Heawood triangle signs. The parity only re-encodes lock 2, and λ = +1 on every DL step.
- **Theorem W** (formal, `QuarterWinding.lean`: `sum_lam`, `three_F_sub_U_winding`). Σλ = |S| − 4F per class, so 3F − U = −5w. In `QuarterPi.lean`, λ is +1 on an unfilled state with lock 2, −1 on one without, −1 on a filled M3-short state and −3 on a filled M3-long state.
- **W4-S theta test** (NightLog, 80e4936). Whether the π-image of a DL state is again DL (DD) is *not* a function of the two-curve meander of the lock chains. It is a function of the whole boundary of the swapped chain (0 mismatches on 23,766 DL states).
- **Disc-degree parity** (`creative-intel-2026-10-05/disc-degree-parity.md`, killed 6 Oct 15:13). Face-parity (Tutte-type) invariants are not Kempe invariants of T − v. By-product: odd(K) ≡ Δe_pr(w) for a chain meeting the link.
- **Heawood charges** (W1-C, killed as a conserved bound) and **cut parity of all-DL orbits** (`NightCutParity.md`: every step of an all-DL orbit is an {ω,·} swap; the parity of how often a vertex is swapped gives D_b = ∂(A_b △ A_{b+1})).
- The **Kempe-chain lock** itself (Kempe 1879, Heawood 1890): the classical "both chains closed" picture is the DL state.

So the new content here is only: (i) the rim-level version is fully determined by planarity (§2, F4), so it carries no depth information; (ii) the polarity count is a constant; (iii) Theorem W restated in polarity words; (iv) correlations of off-rim chain counts with depth; (v) the game-facing "jam" numbers for the skin.

## 2. Exact facts [hand, short proofs; each also checked by the scripts, 0 failures]

Notation (`MathQuarterFloorBijections.md` §0): an unfilled rim reads α μ α A B at x_j … x_{j+4}, with m = x_{j+1}, a = x_{j+3}, b = x_{j+4}. Lock 1: m ~ a in {μ,A}. Lock 2: m ~ b in {μ,B}. A filled rim reads W X Y X Y from x_i, with Z absent.

**F1 (parity is a tautology).** A Kempe chain is a connected, properly 2-coloured graph, so it is bipartite with its colours as the sides. A path inside it between cells of different colours has odd length, and between cells of the same colour even length. Adding the two spokes gives a ring of length +2, so odd stays odd and even stays even. ∎ This needs nothing about planarity or the hole.

**F2 (the one-polarity rule).** Let a swap of the {p,q}-chain K act on a state. The rim colour count drops **iff** both p and q are on the rim, and K contains every rim cell of one of them and no rim cell of the other.
*Proof.* After the swap, p-cells of K become q and q-cells become p, and nothing else changes. If K meets the rim in both colours, both colours are still on the rim afterwards, so the count cannot drop. If K meets only p-cells, then p disappears iff K held all of them, and q (if present) stays. ∎
So a chain that "comes back with the wrong polarity" (meets the rim in both of its colours, F1: odd ring through the hole) can never fill on that swap. Checked on every non-web chain of every one of the 304,758 states: 0 failures.

**F3 (Kempe's criterion).** An unfilled state fills in one swap iff it is not doubly locked.
*Proof.* By F2 a filling chain must hold all rim cells of one colour and none of the other. α is on two rim cells and each α-cell is adjacent to the μ-cell, and x_{j+2} is adjacent to a and x_j to b, so no {α,·} chain qualifies. a and b are adjacent, so {A,B} does not qualify. That leaves {μ,A} and {μ,B} at m, which qualify exactly when lock 1 or lock 2 fails. ∎ Data: dF = 1 ⇔ unfilled and not DL on all 304,758 states.

**F4 (planarity fixes the whole rim structure).** For an unfilled state:
- exactly one of lock 1 and x_{j+2} ~ b in {α,B} holds;
- exactly one of lock 2 and x_j ~ a in {α,A} holds;
- all other rim adjacencies in all six colour pairs are forced: {α,μ} joins x_j, m and x_{j+2}; {A,B} joins a and b; {α,A} joins x_{j+2} and a; {α,B} joins x_j and b; and x_j ~ x_{j+2} in {α,A} (resp. {α,B}) iff lock 2 (resp. lock 1) fails.

*Proof.* The first two bullets are the region principle of QFB §0 for the complementary pairs {μ,A}/{α,B} and {μ,B}/{α,A}. P has degree 4 in the two Tait colours that bound these chains, and the two non-crossing matchings give exactly the two cases, as in Dichotomies M2 and M3. The third bullet is adjacency on the rim plus the first two. ∎

So the partition of the rim cells into chains, over all six colour pairs, is a function of (lock 1, lock 2). Data: exactly one rim signature for each of the four lock patterns, over all 153,206 unfilled states.

**Consequence: the rim-level parity structure predicts depth exactly as far as Kempe's criterion and no further.** It says filled (dF = 0), one swap (dF = 1, not DL) or at least two (DL). Every DL state has the same rim chain structure, yet DL depths run from 2 to 6 (§3). The hypothesis "fillable within k swaps is predicted by the rim chains' parity" is **refuted for k ≥ 2 by F4**, not merely by data. A single map shows it: r178 (hole 10) has DL states at dF = 2, 3, 4, 5 and 6, all with the identical rim structure.

**F5 (the polarity count is a constant).** Look at the five distance-2 pairs of rim cells; adjacent pairs give the hole's own faces (triangles, trivially odd). Count the pairs of different colours that are joined in their own pair's chain: the odd rings through the hole that are not faces. On every unfilled state this number is exactly **2**: lock 1 or its complement x_{j+2} ~ b, plus lock 2 or its complement x_j ~ a (F4). Data: 153,206 of 153,206.
On a filled state it is [M3-short] + [M2-short] ∈ {0, 1, 2}: the odd rings are x_i ~ x_{i+3} in {W,X} and x_i ~ x_{i+2} in {W,Y}. Each dichotomy M2, M3 contributes either its odd ring or the complementary even ring x_{i+1} ~ x_{i+3} in {X,Z} (resp. x_{i+2} ~ x_{i+4} in {Y,Z}), never both.
So **"how many odd rings close through the hole" is not a state variable** for unfilled states. What varies is *which* pair carries each of the two odd rings: the lock (μ to a singleton) or its complement (α to a singleton).

**F6 (Theorem W in polarity words).** From the Lean λ table and `sum_lam`:
- Σλ = #(U, lock 2) − #(U, no lock 2) − #(F, M3-short) − 3·#(F, M3-long) = |S| − 4F.
- Hence, in every Kempe class, **#(unfilled states whose μ–B odd ring is open) = #(filled states whose Y–Y even ring is open)**, that is U_¬L2 = F_M3short. Mirror: U_¬L1 = F_M2short.
- The winding is 5w = U − 3F.

This is a restatement of a formal theorem, not a new result. Check: both identities hold in all 1,606 classes. **Observed, not proved here:** the crossed identities U_¬L2 = F_M2short and U_¬L1 = F_M3short *also* held in all 1,606 classes, i.e. U_¬L1 = U_¬L2 in every class [computed, post hoc]. It may follow from a known bijection; I did not check.

**F7 (one exact depth fact beyond the rim).** If s is DL and π(s) is not DL, then dF(s) = 2, because π(s) is unfilled and not DL, so dF(π s) = 1 by F3. Data: all 23,125 DL states with π(s) not DL have dF = 2.

## 3. What correlates with depth among DL states [computed, post hoc]

DL states: 29,968. dF = 2: 29,308; 3: 598; 4: 57; 5: 4; 6: 1. Since F4 makes the rim structure constant, every candidate predictor is an off-rim quantity.

| feature (DL states) | Spearman with dF (all DL) | AUC for dF ≥ 3 vs dF = 2 among DD states (n = 6,843, 660 deep) |
|---|---|---|
| DD bit (π(s) is DL) | +0.28 | n/a (F7: DD = 0 forces dF = 2 exactly) |
| quiet chains = Euler slack Σk − 8 | −0.18 | 0.15, i.e. **0.85 for "fewer quiet chains ⇒ deeper"** |
| number of legal swaps | −0.17 | 0.17 (0.83 for "fewer ⇒ deeper") |
| size of lock chain 1 / lock chain 2 | −0.01 / −0.01 | 0.44 / 0.35 |
| vertices shared by the two lock chains (the theta) | +0.02 | 0.46 |
| size of the π chain | −0.06 | 0.56 |
| map order n | −0.06 | 0.36 |

(AUC 0.5 = no information; AUC > 0.5 means larger values go with deeper states.)

Readings:
- At DL states the number of quiet chains (two-colour chains touching no rim cell) equals the Euler slack Σk − 8 exactly (29,968 of 29,968). This is Lemma 2.2 of `NightWindingMeander.md`: every rim-touching component count is fixed at a DL state.
- **Depth goes with saturation, not with the lock chains' shape.** Deep DL states have few closed off-rim chains: of 660 DD states with dF ≥ 3, 549 have slack ≤ 1. A saturated state (slack 0) has only π and π⁻¹ as moves (Corollary 2.3 there), so the trap is "no spare chain", not "an odd ring of a special kind".
- The lock-chain geometry ("how they nest/cross": sizes and shared μ-vertices) carries almost nothing: H(dF | sizes, shared) = 0.133 bits against H(dF) = 0.164.
- All ten features together leave 111 mixed groups; H(dF | all) = 0.039 bits, an in-sample fit over 7,091 groups. **Counterexample to "features determine depth":** gentri 17:3 hole 0, state 62 and 4square c30 hole 0, state 16 have identical vectors (DD, slack 2, 10 chains, lock chains of size 8 and 8, 4 shared, π chain of size 4, 8 swaps, n = 17) and dF = 2 vs dF = 3.
- Not a predictor: slack 0 also occurs at 238 DD states with dF = 2.

## 4. Polarity count against W, λ, κ

- **Per state:** the non-face odd-ring count is 2 on every unfilled state (F5). It therefore bounds nothing beyond F3 (DL ⇒ κ ≥ 2; here κ = the game's dF, the pure-Kempe distance at the fixed hole).
- **λ:** on unfilled states λ is exactly the lock-2 polarity bit (+1 if the μ–B odd ring is closed, −1 if open). On filled states it is the M3 bit (−1 if the Y–Y even ring is open, −3 if closed). This is Lean's definition. Proposition H gives the same bit as a meander crossing parity.
- **W:** class winding w = (U − 3F)/5 depends on U and F only. The class-total odd-ring count Ω = 2U + F_M2s + F_M3s = 2U + U_¬L1 + U_¬L2 (F6). Across classes, Ω/|S| and w/|S| have Spearman 0.91, but both are affine in the filled share up to the lock-failure term, so this is no new information. **Ω does not equal or bound w** beyond what Theorem W already gives.
- **κ:** the rim-level polarity is constant on DL states (F4), so it cannot bound κ above 2. The best single off-rim correlate is saturation (§3), and no exact bound was found.

## 5. Verdicts

| claim | verdict |
|---|---|
| chain between differently coloured rim cells is odd; with the spokes it closes an odd ring | **exactly true, a tautology** (F1) |
| such a chain's swap leaves the rim colour count unchanged | **exactly true** (F2): it cannot fill on that swap |
| …and "only trades the two rim colours" | **true only when the chain holds every rim cell of both colours** (a lock chain, or the {α,μ} / {A,B} chains through the hole's faces). Then the rim sees a pure renaming. A chain meeting both colours but not all their rim cells changes the rim word (§6) |
| same-colour rim chains close even rings | exactly true (F1) |
| fillable within k swaps is predicted by rim-chain parity | **true for k ≤ 1 (F3), refuted for k ≥ 2 (F4)**: all DL states share one rim structure, with depths 2–6 |
| depth is predicted by off-rim chain structure | **correlates**: fewer quiet chains (Euler slack) means deeper, AUC 0.85 among DD states. Not determined: explicit counterexample in §3 |
| total polarity count relates to Theorem W winding | constant per unfilled state (F5). The polarity bit that matters is lock 2 = sign of λ, i.e. Theorem W itself (F6). No new bound |

## 6. Game-facing numbers (for the Gears skin)

Classify every legal swap at an unfilled state by how its chain meets the rim:
- **full**: every rim cell of both colours, so the rim is only renamed;
- **part**: both colours, not all;
- **one**: one colour;
- **quiet**: no rim cell.

Data are the 4square maps plus gentri 16–19 (`gp_jam.py`).

| state | kind | swaps | lowers dF | keeps dF | raises dF |
|---|---|---|---|---|---|
| DL | full | 21,333 | 0.59 | 0.40 | 0.01 |
| DL | part | 23,978 | 0.78 | 0.20 | 0.02 |
| DL | one | 23,978 | 0.85 | 0.13 | 0.02 |
| DL | quiet | 37,734 | 0.48 | 0.52 | 0.01 |
| not DL | full | 71,657 | 0 | 0.83 | 0.17 |
| not DL | part | 28,426 | 0 | 0.36 | 0.64 |
| not DL | one | 170,418 | 0.83 | 0.05 | 0.12 |
| not DL | quiet | 155,324 | 0 | 0.88 | 0.12 |

**Honest consequence for the skin:**
- A "jam" (the turn comes back to the rim with the wrong polarity) means **this swap cannot fill the hole now**. That is exact (F2).
- It does **not** mean the swap is wasted: at a DL state, 59% of full-jam swaps and 78% of partial ones bring the fill closer. The π move itself is a partial-polarity swap.
- So the skin may show a jam at the rim (rim unchanged, or only renamed) but must not mark the move as useless or block it.
