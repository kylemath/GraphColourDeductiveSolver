# Belt case map and the equal-pole / pole-hole Lean files

6 October 2026. Math. Status: compiled, no `sorry`, axioms `[propext, Classical.choice, Quot.sound]` only. Nothing staged or committed. No existing file was edited.

## 1. Case map (before this work, then now)

| Hole | Poles | Hand proof | Compiled before | Compiled now |
|---|---|---|---|---|
| belt | unequal | belt-joined §4-§7 | `TwoPoleBeltWalk.belt_unequal_at` (<= 2n slides) | same |
| belt | equal | §3 (one Kempe swap) | **not compiled** | `TwoPoleBeltEqual.equal_u`, `equal_v` (<= 1 swap) |
| belt, any poles | both | §0 | only the unequal half | `TwoPoleBeltPoleHole.belt_complete` (<= 2n moves) |
| pole `a`, link <= 3 colours | | trivial | n/a | inside `pole_a_complete` (0 moves) |
| pole `a`, ring singleton | any (poles may become equal after the slide) | §2 item 2 | **not compiled** | `pole_a_singleton` (<= 2n+1) |
| pole `a`, no singleton | | `pole-hole-noflorek.md` | `TheoremPPole.theoremP` (Kempe swaps, <= 3(n0-2)+n) | used inside `pole_a_complete` |
| pole `a`, every colouring | | | not assembled | `pole_a_complete` (<= 6n) |
| pole `b` | | by symmetry `s` | not compiled | `pole_b_singleton`, `pole_b_complete` (<= 6n) |
| every hole | | §0 theorem | not assembled | `belt_theorem_all_holes` (<= 6n) |

Files (new only, in `/Users/fulkanjou/mathlib4-planemap/Mathlib/Combinatorics/SimpleGraph/PlaneMap/`): `TwoPoleBeltEqualPoles.lean`, `TwoPoleBeltPoleHole.lean`, `TwoPoleBeltPoleB.lean`; test `MathlibTest/PlaneMapTwoPoleBeltEqual.lean`. Copies, logs and `SHA256SUMS`: `backgroundMaterial/planemap-structural/lean-belt-equal/`.

## 2. Line-by-line check of the hand proofs (belt-joined.md)

**§3 (equal poles).** Checked and correct; the Lean proof follows it.
- "No belt vertex has colour A": every coloured `u_j` meets `a`, every coloured `v_j` meets `b`. Used as `noA_u`, `noA_v`.
- "Singleton on the v-side": the four belt link vertices of `u_i` form the path `u_{i+1} - v_i - v_{i-1} - u_{i-1}` (there is no edge `u_{i+1}v_{i-1}`, `u_{i+1}u_{i-1}`, `v_iu_{i-1}`; the proof only needs the three path edges). With three non-A colours all present, one of the two middle vertices is uniquely coloured among the four. Lean: `middle_unique`, a `decide` on `Fin 4`. Needs no multiplicity-(2,1,1) discussion and no `n mod 3`.
- "The (A,B)-component of `b` is `{b} ∪ {v_j : c = B}`": checked in Lean as a `VacancyShortFill.Whole` (the full reachable set of the two-colour graph, not just a closed set): closure uses that `a` is not adjacent to any `v`, `u_k` adjacent to `a` cannot be A, and a `v_j` coloured B has no B-neighbour.
- After the swap every `v_j` has colour != B (`swap_v_ne`), the two `u` link vertices keep their colours != B, `a` keeps A. So B is absent: filled. Matches the text.
- The residue paragraph (n mod 3) is not needed for the theorem. It only says when the case occurs. Not compiled and not needed.
- Hole `v_i` is not written out in §3; it is the `s`-image. Lean proves it directly (`equal_v`, star of `a`, chain `v_{i-1} - u_i - u_{i+1} - v_{i+1}`).

**§2 item 2 (pole hole after a singleton).** Correct as written. After the slide `a -> u_i`, `c(a) := c(u_i)` and `c(b)` unchanged, so the poles can be equal or unequal, and the hole is the belt vertex `u_i`. Lean: `pole_a_singleton` applies `belt_complete`, which splits on `c a = c b`. Slide-step properness is `properOff_slide`; uniqueness is the hypothesis. The text's remark "belt holes are proved for every colouring, whichever colour `a` received" is exactly what `belt_complete` states.

**§2 item 3 and the table's last row.** Not re-derived here. It is `TheoremPPole.theoremP` (already compiled). `theoremP_fill_or_singleton` carries an unused hypothesis (`_htwice`, every colour twice) so I called `theoremP` directly: it ends in a state with a colour used at most once on the ring (`Good`). Either the colour is absent (filled) or it is a ring singleton, which is `UniqueAt a (u i)` because `N(a)` is the ring (`adj_a_iff`).

**Small points in the page, no error found.**
- §0 says the belt-equal row uses "no slides"; true.
- The pole-hole bound in §0 is `3(n0-2)+n` swaps; with `n0 <= n` this gives `<= 4n` swaps, and `pole_a_complete` states `<= 6n` in total (4n swaps + 1 slide + <= 2n belt moves is `<= 6n` for n >= 5, since `4n - 6 + 1 + 2n <= 6n`). The 6n is loose.

## 3. What compiled (exact statements are in `lean-belt-equal/test.log`)

Notation: `G = TwoPoleBelt.graph n`, `Filled t := Target t.1 t.2` (a colour missing from the link of the hole), colourings `Vertex n -> Fin 4`, `ProperOff` is properness off the hole.

- `equal_u (hn : 5 <= n) (i) (hc : ProperOff G (u i) c) (heq : c a = c b) : Target (u i) c ∨ ∃ d, KempeStep G (u i) c d ∧ ProperOff G (u i) d ∧ Target (u i) d`. `equal_v` is the same for `v i`.
- `belt_complete (hn) (h) (IsBelt h) c (ProperOff G h c) : ∃ k ≤ 2*n, ∃ t, MixedPath G k (h,c) t ∧ Filled t ∧ ProperOff G t.1 t.2` (equal poles: <= 1 Kempe swap; unequal: `belt_unequal_at`).
- `pole_a_singleton` / `pole_b_singleton`: hole at a pole, `UniqueAt G a (u i) c` (resp. `b`, `v i`): `∃ k ≤ 2*n+1, ... MixedPath ... Filled ... ProperOff ...`.
- `pole_a_complete (hn) [NeZero n] c (ProperOff G a c)`: `∃ k ≤ 6*n, ...` same conclusion.
- `pole_b_complete (hn) c (ProperOff G b c)`: same, via transport along `ringSwap`: new lemmas `kempeStep_transport`, `mixedStep_transport`, `mixedPath_transport`, `transport_slide`, `uniqueAt_transport` (a Kempe swap, with its whole component, and a mixed path commute with any automorphism of `G`).
- `belt_theorem_all_holes (hn : 5 <= n) (h : Vertex n) c (ProperOff G h c) : ∃ k ≤ 6*n, ∃ t, MixedPath G k (h,c) t ∧ Filled t ∧ ProperOff G t.1 t.2`. This is the vacancy hypothesis at every hole of every `G_n`, `n >= 5`.

`#print axioms` for all eight statements: `[propext, Classical.choice, Quot.sound]`. Build: `lake build Mathlib.Combinatorics.SimpleGraph.PlaneMap.TwoPoleBeltPoleB` completed (3202 jobs). Warnings only (deprecated `Set.mem_setOf_eq`, long lines, unused `hn`).

## 4. Remaining gaps (honest)

1. This is the theorem about the explicit graph family `TwoPoleBelt.graph n` (Fin 4 colours, n >= 5). Connecting `G_n` to Florek's triangulation, and plugging `belt_theorem_all_holes` into a hole-induction framework for general planar graphs, is not done here.
2. The audit script `belt_source_audit.py` baseline (95 modules) was not rerun; I built only the three new modules and the test (their dependencies were already built). A fresh full audit should add the three files.
3. The 6n bound is not tight; the computed census says far fewer moves are needed (<= 6 swaps by the strategy).
4. `mixed paths` here count a Kempe swap and a slide as one move each; no claim about slide-only paths for equal poles (they need a Kempe swap, as `belt-joined.md` §3 shows).
