# Math attack on (N), part 3: Case I

Math-team research worker, 5 October 2026. Continuation of `MathNPinchT3.md`. Exploratory, undeclared; no census, no declared experiment, nothing edited of others', nothing staged or committed. Labels: [hand], [computed] (exploratory, post hoc), [open]. Status words stay with the Navigator. Scripts: `docs/working/MathNCaseI-scripts/` (`tn_lib.py` = the functions of `MathNDiscSearch/test_N.py`; `caseI23.py`, `geo23.py`, `c3path.py`, `dfree.py`; run from that directory, they read `../MathNDiscSearch/res_23.txt`).

## 0. Result

| Question | Outcome |
|---|---|
| Is "at least one of c', c'' is Case II" true? | **No. [computed] It is false at N = 23.** Discs 2 and 3 of `res_23.txt` (sizes (5,6,5,6) and (5,6,6,5), one each) have c' and c'' both in Case I. (N) still holds on them (both neighbours separable). So the "exactly one" pattern of the four 17:1 states is an artefact of n = 17, and **no geometric input can prove "at least one Case II"**. The task as posed has a negative answer. |
| Is Case I x Case I consistent at the level of local data? | **Yes.** [hand] the counting automaton of `MathNPinchT3.md` §5.4 has a closed locked orbit; [computed] the combination occurs in two actual triangulations of order 23, whose first-order data, Lemma DI/M, (O), tau = -1, X ∩ X0 = ∅, and the Y-Y0 pinch are all as in the n = 17 states (§2). So Case I x Case I is consistent with everything local and with everything I know of the pinch structure; it is excluded only by a deeper unlock. |
| Minimal missing global fact | Pinned down exactly, as the single statement **(G\*)** of §3: in Case I, after the third swap (c3), the chain {D,β} is broken, equivalently (Lemma D) u1 ~ u3 or u1 ~ u4 in [α,γ]_3. [computed] 8 of 8 Case I neighbours (all in the N = 23 data) satisfy it, and the D'-free unlock distance is exactly 3 in all 28 neighbours (14 discs x 2), Case I and Case II alike (§4). [open] to prove. |
| Geometric proof of (G\*) | **Not found.** What I could prove is the reformulation (§3) and the negative statement that the three tools of the task (planarity of lens/fill, orientation of P13/P14/K0/K2 fills, (O)) do not distinguish Case I from Case II (§5). |

## 1. Case II / Case I, restated [hand]

By `MathNPinchT3.md` §5.2: c' locked at u0 gives c1 (swap Q4 = [α,γ']-component of u4), c2 (swap E34 = [α,β]_1-component of u3,u4), and the dichotomy m_βγ(c2) ∈ {2, 1}: Case II ⇔ u2 ≁ u4 in [β,γ]_2 (three-colour ring after one more swap), Case I ⇔ u2 ~ u4 in [β,γ]_2. By Lemma D applied to c2 (ring word D α γ α β, pair {β,γ}, complement {D,α}), Case II ⇔ there is a [D,α]_2 path joining two ring vertices that separate u2 from u4 on the ring, i.e. a path u0 ~ u3 or u1 ~ u3 in [D,α]_2 (these are the pairs of ring vertices coloured D/α with u2 and u4 in different arcs: {u0,u3}, {u1,u3}; {u0,u1} and {u3,·} others do not). This is the same as m_Dα = 2 of §5.2 (Lemma M).

Mirror for c'': Case II ⇔ u0 ≁ u3 in [β,γ]_2'' ⇔ a [D,α] path u2 ~ u4 or u1 ~ u4 in the mirror c2''.

Case I x Case I therefore says: in two colourings of the same T−x, u3 ≁ u0,u1 in [D,α]_2 and (mirror) u4 ≁ u2,u1 in [D,α]_2''. These are statements in different colourings (c2 and c2'' differ by swaps of K2 vs K0 and of Q4 vs Q3 etc.); they are not statements about one pair graph, so no single Jordan curve sees both.

## 2. Data at N = 23 [computed, exploratory, post hoc]

Input: the 14 triply locked discs of `MathNDiscSearch/res_23.txt` (order of the lines there).

**Case I/II table** (`caseI23.py`; I = Case I, II = Case II; none of the 28 neighbours is first-order unlocked):

| disc (sizes) | c' | c'' |
|---|---|---|
| 1 (5,6,5,6) | II | I |
| 2 (5,6,5,6) | **I** | **I** |
| 3 (5,6,6,5) | **I** | **I** |
| 4 (5,6,6,5) | I | II |
| 5-10 (6,4,6,6) | II | II |
| 11 (6,6,4,6) | II | II |
| 12 (6,6,4,6) | I | II |
| 13 (6,6,6,4) | II | I |
| 14 (6,6,6,4) | II | II |

Counts: both Case II in 7 discs, exactly one Case II in 5, **both Case I in 2**. So "exactly one" fails in both directions (both II occurs too; at n = 17 both II did not occur only because the state is that rigid).

**Case I always breaks at c3.** For all 8 Case I neighbours (c3 = c2 with the [β,γ]_2-component through u2,u4 swapped): u0 ≁ u2 in [D,β]_3 (resp. mirror u2 ≁ u0 in [D,γ]_3''), i.e. the chain {D,β} is broken: the locked branch of §5.3 of the previous note is never taken. The same holds in the four n = 17 states (previous note). In three of the four N = 23 Case I cases the [α,γ]_3 path realising the break, from u1 to u3 and to u4, is the same shape: u1 – γ(5) – β(6)-becomes-α – γ(4) – u3, with the γ-vertices 5, 4 the first γ-vertex of P14 after u1 and the last before u4 in the two positions of the data (`c3path.py`); I extract no theorem from it.

**D'-free unlock distance.** The Kempe class of c' (c'') under swaps of pairs avoiding the colour of D' (the apex colour of the neighbour) has 10 to 20 members at N = 23 (not the two-hexagon graph of n = 17; edge counts 11 to 37, degrees 2 to 6, so the "exactly 2-regular" §2.4 picture is false in general: that needs the (2,2,1) component pattern at every member, which fails). The first member with a broken apex chain or a 3-coloured ring is at distance **exactly 3** from the neighbour in all 28 cases (`dfree.py`). Combined with `MathNPinchT3.md` §5.2 (c, c1, c2 are locked in Case I/II alike) the lower bound 3 is hand-explained and the upper bound is the data. [computed]

**Structure of Theorem P at N = 23.** In all 14 discs: (O) holds; P13 and P14 each have exactly one Y0- resp. Y-vertex and share exactly three vertices (u1 and two α-vertices a, a'); |Λ| = 2 faces (a rhombus); X ∩ X0 = ∅; d = |Y|-|X| = 0 (twelve discs) or -1 (the two (6,6,6,4) discs); τ = -1 in all 14, so the excess relation exc(Y)-exc(X) = 1-3d holds. So the pinch with a single rhombus, type II structure of c' and c'' (via Theorem G), and the shared-order property (O) are not special to n = 17. [computed] (`geo23.py`; exploratory evidence for (O) and τ = -1 beyond n = 17.) Case I/II does not correlate with any of these quantities (the two Case I x Case I discs have the same pinch data as the Case II x Case I ones).

## 3. The exact missing statement [hand reformulation; the statement itself open]

Let c' be locked at u0 and in Case I. Define c3 as above (ring D α β α γ). Then:

* (Lemma D, complement pair {α,γ}, ring vertices u1 α, u3 α, u4 γ) the chain {D,β} of c3 at u0 is broken ⇔ u1 ~ u3 or u1 ~ u4 in [α,γ]_3;
* (Lemma M at c3) locked ⇔ tokens exactly {u0 ~ u2 in [D,β]_3, u2 ~ u4 in [β,γ]_3} and u1 ≁ u3, u4 in [α,γ]_3.

**(G\*)** *In a rigid triply locked state with c' locked and in Case I, u1 ~ u3 or u1 ~ u4 in [α,γ]_3 (and mirror for c'').* Under (G\*), Case I produces a separable colouring after a fourth swap exactly as Case II does (c3 has a broken chain: one more G_0 swap gives a separable state), so **(G\*) ⇒ (N)**, indeed ⇒ "c' is separable at u0 whenever it is locked and ... ", i.e. T3 unconditionally, with no use of the neighbour c''. [hand: the implication; the unconditional status of T3 is then "(G\*) is T3 for Case I"]. The T3 target of `MathNAttack.md` §4 is thus equivalent, for c' alone, to (Case II) ∨ (G\*); (N) is strictly weaker in principle (it needs it for only one of c', c''), but the data say that even the weaker route cannot rely on Case II (§0).

**Why this is the minimal fact.** All other branches of the token automaton are closed by Lemma M (§5.2 of the previous note). The only unclosed binary choice at each of c1..c3 is "which of the two available non-adjacent ring connections survives", and Case II/I and (G\*) are those choices at c2 and c3. Then at c4 the pattern repeats up to renaming (previous note §5.4), so a proof must kill the locked branch at c3 by a statement about **paths in [α,γ]_3**, not by counting. [hand]

## 4. Candidates for the geometric input, and what they give [hand]

1. **Jordan curves of P13, P14 (the lens).** After the swaps, the curves that bound the discs are Z13, Z14 (c-level) and, in c3, the paths of [α,γ]_3 and [α,β]_3. The component R swapped from c2 to c3 is a [β,γ]_2-component through u2,u4 and by Lemma D (u2 ~ u4 in [β,γ]_2) it is **not** separated by any [D,α]_2 path; the [α,γ]_3 path of (G\*) must therefore live in Ω-complement of R's boundary and use R's old β-vertices turned γ... I could not turn this into a contradiction or a proof: the c-level data (K2, K0, P13, P14, X, Y) only enter c3 through the four swaps K2, Q4, E34, R, and the last three components are not constrained by c-level geometry except via first-order data already used.
2. **(O) and the pinch.** Theorem P concerns the position of Y inside Ω13 and Y0 inside Ω14⁰; both Case I and Case II instances share the same pinch (§2), so it cannot decide.
3. **Winding of P13 and P14.** [hand] The orientation facts (Ω13 left of P13, Ω14⁰ right of P14) are symmetric under the mirror that swaps c' and c''; Case I x Case I is a mirror-symmetric statement, so a mirror-symmetric geometric fact cannot exclude it. (The two N = 23 Case I x Case I discs are not themselves mirror-symmetric, as sizes differ, but this only shows the asymmetry is not forced.)
4. **Hypothesis (O).** Proving (O) would give the pinch (`MathNPinchT3.md` §3) and the Y-Y0 edge Lemma YY; none of this separates Case I from Case II by the data above. [open: whether (O) holds for all rigid triply locked states; it holds in 18 of 18 states tested (4 at n = 17, 14 at n = 23).]

## 5. What this changes

* The conjecture "exactly one of c', c'' is Case II" in `MathNPinchT3.md` §7 is **false** (counterexample: two discs at N = 23). The only data-supported statement is (G\*) (8 of 8) and "D'-free unlock distance = 3" (28 of 28). A route to (N) via "at least one Case II" is closed [computed + the discs are re-checkable by `recheck.py`, whose independent check of N on discs 2 and 3 I did not run].
* The statement to attack is (G\*), a statement about one colouring c3 reached from c by four swaps. It is a statement about paths in [α,γ]_3 near u1, u3, u4, so it is a Jordan-type statement of the same kind as Lemma D at third order; counting alone cannot prove it (closed token orbit).
* The N = 23 data also say (N) is not violated at the first order where it is non-vacuous beyond 17, with Case I x Case I present: the pattern "locked branch is never taken at c3" is evidence, not proof, that (G\*) is true.

## 6. Not done [open]

* No proof of (G\*) and no proof of "c' or c'' Case II" (the latter is false).
* No analysis at N = 24 or above (not generated), no independent recheck by `recheck.py` of discs 2 and 3.
* (G\*) was tested only on c3 of the first (shortest) branch; the 3-step minimality (distance exactly 3) holds for the D'-free class, not for the full Kempe class of G.
