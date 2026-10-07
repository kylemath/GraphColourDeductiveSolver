# NightTwoPocket: the two-pocket planar route to A₃₄′ on L = 20, closed

Night worker, 7 October 2026 (written 05:05 MDT). **Exploratory. Hand arguments from the period table plus scripts on Job AV/BD/BE records and the Job AW counterexample. Unreviewed.**

Builds on: `NightA34Two.md` (exchange pair c, d = Gc; crossing lemma), `NightA34.md` §1–§3 (table, pocket lemma, window lemma), Jobs AV, AZ, BB, BD, BE, AW; Lean `QuarterTwoPeriod`, `QuarterZsplit`, `QuarterK8`, `QuarterCrossing`. Scripts in `backgroundMaterial/planemap-structural/longtable/local-runs/35-nighttwopocket/`.

## Verdict

**The two-pocket route is closed: its target is false.** Studio Job AW found constructed 37-vertex (5,5,5,5,6) graphs with an L = 20 Γ-cycle whose two runs both break. §4 examines one: both pockets reach w⁺, and they enter m through *different* far neighbours of m. What survives is the bookkeeping in §1–§2 (proved) and the data in §3.

## 1. The two curves on the sphere [proved]

Frame: position 9 (R1k2) of the common pulled-back frame. The colours are
- p = 0, x⁺ = 2, x₂ = 3, x₃ = 0, x⁻ = 1;
- z = 1, w⁺ = 0, w₂ = 1, w₃ = 2, y = 3;
- m = 2.

The pocket pair is {0, 2} and the J pair is {1, 3}. By `ring_agree`, c₉ and d₉ carry exactly these colours on the 11 hole vertices.

- **Hole vertices a pocket can contain.** The pair-coloured hole vertices are p, x⁺, x₃, w⁺, w₃ and m. p and x⁺ are deleted.
  - x₃ has degree 5. Its only pair-coloured neighbour off h is w₃, so it is at most a leaf.
  - w₃ can be passed only from the far side.
  - [data] Every pocket in Jobs BD and AW contains exactly {m, w⁺} from the hole.
- **The ring disk.** The ring z w⁺ w₂ w₃ y m bounds a disk containing h and the link. A pocket path Q from w⁺ to m is therefore a chord of the complementary (outer) disk O. It cuts O into two parts:
  - the **z-part**, bounded by Q and the ring arc w⁺ z m;
  - the **y-part**, bounded by Q and the arc w⁺ w₂ w₃ y m.
  
  The pocket curve is C = p x⁺ w⁺ Q m p, and z's J-component lies in the z-part.
- **Two curves.** In a double break, Q_c and Q_d are two chords of O with the same endpoints w⁺ and m.
  - A vertex they share has a pair colour in both colourings.
  - Where they differ, they pass through X₉ or through agreement vertices of different components.
  - The crossing lemma (formal, `QuarterCrossing`) says the healing J-path of the non-breaking member must use X₉ ∩ Q_c. With both members breaking, that lemma has no hypothesis to act on.
- **Degree 6 versus degree 7.** At degree 6 both chords end at the single vertex m, which is adjacent to both y and z. At degree 7 they end at M′, which is adjacent to z only. Job BB found that the 7 degree-7 consecutive-break pairs use M′ in both runs. So "two routes past p" was never the difference, and §4 shows that a single m is not an obstruction either.

## 2. The m-neighbourhood automaton at deg(m) = 5 [proved; `mlocal.py`]

Set-up:
- Around m the rotation is p, z, u₁, u₂, y, where u₁ ~ z, u₂ ~ y and u₁ ~ u₂.
- At position 9 the possible states (u₁, u₂) are (0,1), (3,0) and (3,1).
- The pocket is {m} ⇔ the state is (3,1). Equivalently, z u₁ u₂ y is a J-path, so J holds.

Tracking through G:
- Track (u₁, u₂) through step 9, then ρ⁻¹, then steps 0–8.
- Each step uses the table's pair and its hole members (p, m, y, z from `pair_own` / Job O).
- The rule is: a neighbour of a pair-coloured hole vertex is in K exactly when that hole vertex is.

Result:
- The transition relation is **complete**: all 9 transitions (s → e) are locally possible.
- The free choices are four memberships:
  - u₂ ∈ K₃;
  - u₁ ∈ K₄;
  - u₂ ∈ K₇;
  - u₁ ∈ K₈.
- So colour tracking through the ten swaps cannot forbid two pockets. Every break-to-break transition is realised by some branch set (listed in `mlocal-output.txt`).

One planar refinement is proved. **If u₁ ∈ K₈, then u₂ = 1 at position 8, and Lock2's {1,2}-chain leaves z along the edge z–m.**
- If the chain left z through a far neighbour f, the closed curve h x⁺ z Λ w₃ x⁻ would put u₁ on p's side (u₁ lies between m and f in z's rotation).
- K₈ lies on x₂'s side.

This is consistent with every transition, so it kills none.

## 3. Data on the 19 degree-6 breaks [data; `mdata.py` → `mdata-output.txt`]

- **deg(m) = 5 (15/19 breaks).** The breaking member is in state (0,1) (8 cases) or (3,0) (7 cases). The partner is in (3,1) in 15/15, so its pocket is {m}.
  - Branches used: from (0,1), u₁ ∉ K₄, u₂ ∈ K₇, u₁ ∉ K₈; from (3,0), u₂ ∉ K₃, u₂ ∉ K₇, u₁ ∉ K₈.
  - This matches Job BE: the step-13 swap never touches m's far neighbours on a break.
- **deg(m) = 6 (4/19 breaks).** The partner's pocket is nontrivial (Job BD overlap cases).
- **The tempting one-period lemma "a deg-5 break forces the partner into (3,1)"** is a one-period statement (B(u₉) ⇒ ¬B(u₁₉)). It cannot be true in general for deg(m) = 6: the local open double break gentri 24 #3611 h0 (`open24.py`) has deg(m) = 6, with state (u_z, u_mid, u_y) = (3,0,1) at both R1k2 states and both pockets reaching w⁺. The open-run scan for deg(m) = 5 (`openscan.py`) was stopped unfinished, so deg 5 is **untested on open runs**.

## 4. The counterexample A7f2-A34-w5-it918 (mirror; `aw918.py` → `aw918-output.txt`)

- 37 vertices; Python state space 17,512 states.
- The L = 20 Γ-cycle has step-8 breaks in **both** periods (k4fail = [T, T]).
- Names: p = 18, m = 13, z = 16, y = 28, w⁺ = 21. deg(m) = 6, and m's far neighbours are 15 (adjacent to z), 19 (middle) and 20 (adjacent to y).

| | c₉ (period 0) | d₉ = ρ⁻¹c₁₉ |
|---|---|---|
| far neighbours 15, 19, 20 | 3, 0, 1 | 0, 3, 1 |
| pocket | {3, 11, 13, 19, 21, 24, 25, 29, 34, 35} | {1, 5, 6, 11, 12, 13, 15, 21, 25, 35} |
| enters m via | 19 (middle) | 15 (z-side) |
| reaches w⁺ | yes | yes |

- Shared vertices: P_c ∩ P_d = {11, 13 = m, 21 = w⁺, 25, 35}. These are far vertices that agree, plus m and w⁺.
- X₉ = {1, 5, 6, 8, 9, 12, 15, 19, 33, 34}.
  - X₉ ∩ P_c = {19, 34}, with (c₉, d₉) colours (0,3) and (0,1).
  - X₉ ∩ P_d = {1, 5, 6, 12, 15}.
- Hole vertices in both pockets: {w⁺, m}.

Which intermediate claims fail here:
- **"P_c reaches w⁺ ⇒ P_d = {m}"** (the BD/BE reading, 15/19) fails.
- **"the two curves must cross in X₉"** fails: they share only agreement vertices.
- **"a single m forces both curves through the same edge pair at the ring"** is true, since both pass p–m between y and z, but it is harmless. The chords enter m from different far neighbours, the middle one and the z-side one, and the m-local J-path z u … y is cut in both.
- The deg-5 lemma of §3 is **not tested** by this example (deg(m) = 6). Whether a deg(m) = 5 counterexample exists is open. The 15/15 pattern is the only remaining local regularity, and with A₃₄′ false it has no target.

**Verdict: the two-pocket route to A₃₄′(L = 20) is closed, because A₃₄′ itself is false at degree 6 (Job AW). §1–§2 remain correct bookkeeping for whatever replaces it.**
