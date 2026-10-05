# Lean drafts: the unequal-pole belt walk

Long Table, 5 October 2026. This is a draft outside the accepted build. Math owns the accepted build and decides what enters it. Nothing here edits Math's repository or the accepted overlay.

Source: `longtable/swarm/belt-joined.md`, §1 and §4–§7, which Math accepted as a hand proof.

## Status in one paragraph

Every statement elaborates, and **every proof is complete. The two draft files contain no `sorry`.** The final theorem `SimpleGraph.BeltDraft.belt_unequal` depends only on `[propext, Classical.choice, Quot.sound]`; this is checked by `#guard_msgs` in `AxiomCheck.lean`. A fresh build gives exit code 0 with no errors and no warnings (`build-output.txt`). The task allowed `sorry` for the proofs, but the local rows proved quick enough that the whole chain was closed.

There is a dependency caveat. The drafts import two modules that are **not** in the accepted 83-module overlay:

- Team A's `BeltVacancyTeamA.lean` (the graph, neighbour lists, `SlidePath`, the D, A_τ, A_ρ and B_τ rows);
- Math's `BeltCapsMath.lean`.

Both are compiled fresh from Math's repository (read-only) by `build.sh`. The proof is therefore complete *relative to those two modules as they stand at the hashes below*.

Those hashes equal the snapshots in `longtable/audit/team-a-lean-belt-*.lean`, and `belt-cap-lean/` holds a compile audit of the same two modules that appeared while this draft was being written.

Team A's later `BeltDWalkTeamA.doubled_one_walk` (see `audit/team-a-lean-belt-BeltDWalkTeamA.lean`) overlaps `controls_D` and `macroD` here. Math should keep one of the two.

## Files

| File | Content |
|---|---|
| `BeltGraph.lean` | §1: `G n`, neighbour lists, the automorphisms, slide transport, `SlideStep` ↔ `SlidePath`, the pole invariant |
| `BeltWalk.lean` | §4–§7: openings, Z/D rows, interval and potential, caps, macro steps, controllers, `budget`, and the final theorem |
| `AxiomCheck.lean` | axiom guards for `belt_unequal` and `ringSwap` |
| `build.sh` | full fresh elaboration (the method of `audit/belt_preparation_audit.py`) |
| `check.sh` | re-elaborate one draft after `build.sh` |
| `build-output.txt` | output of the last `build.sh` |
| `_build/` | disposable overlay and `.olean` files (git-ignored) |

## Elaboration

```
cd backgroundMaterial/planemap-structural/longtable/lean-drafts && ./build.sh
```

The build does the following:

1. It symlinks the accepted overlay `/tmp/planemap-audit-20261005-short-fill/lib`, whose manifest status is `passed`, into `_build/lib`.
2. It runs `lean -o` (toolchain `v4.35.0-rc3`, with `LEAN_PATH` taken from that manifest) on `VacancyPotential`, `BeltOpeningWords`, `BeltVacancyTeamA` and `BeltCapsMath`, using the sources in `/Users/fulkanjou/mathlib4-planemap`.
3. It then runs `lean -R . -o _build/lib/<M>.olean <M>.lean` for `BeltGraph`, `BeltWalk` and `AxiomCheck`.

**Result:** exit 0, 0 errors, 0 warnings, 0 `sorry`. It takes about 17 s. The axiom guard passes.

The input hashes (sha256) are:

- `VacancyPotential.lean`: `ded80923…` (same as Math's helper audit)
- `BeltOpeningWords.lean`: `0edb2375…` (same as Math's helper audit)
- `BeltVacancyTeamA.lean`: `cc9465bc…` (not accepted)
- `BeltCapsMath.lean`: `6575b535…` (not accepted)
- `BeltGraph.lean`: `ded99edf…`
- `BeltWalk.lean`: `35aaa1b3…`

## The theorem

```lean
theorem belt_unequal (hn : 5 ≤ n) (c : Vertex n → Colour) (hc : ProperOff (G n) (u 0) c)
    (hab : c a ≠ c b) :
    ∃ k t, VacancyPotential.Path SlideStep k (u 0, c) t ∧ k ≤ 2 * n ∧ Filled t ∧
      ProperOff (G n) t.1 t.2 ∧ IsBelt t.1 ∧ t.2 a = c a ∧ t.2 b = c b
```

Here `SlideStep` is exactly one singleton slide: an adjacent `x`, then `UniqueAt`, then `slide`. `Filled` is Team A's `Target`, meaning the hole's link misses a colour.

The proof runs as follows:

- colour normalisation (`exists_perm_poles`, `slidePath_recolour`);
- then `opening_classes`, using Math's `BeltOpeningWords.classification` and the reflection `R`;
- then one of four openings;
- then `VacancyPotential.budget` (`walk_of_controls`, slack 0), with the controller premise discharged by `controls_S`, `controls_S0` and `controls_D`. These are built from the row, cap and macro lemmas.

The proof actually gives at most 2n−2 slides for the Z-families and at most 2n−1 for D.

## Lemma map (all proved)

| belt-joined.md | Lean (file: name) |
|---|---|
| §1 graph, neighbour lists | `BeltGraph`: `G`, `nbr_u`, `nbr_v`, `nbr_a`, `nbr_b`, `not_adj_ab` (graph and lists reused from Team A) |
| §1 automorphisms r, s, R | `BeltGraph`: `rot k`, `ringSwap`, `reflection` (each a `G n ≃g G n`), `edge_rot`, `edge_swap`, `edge_refl`, `reflection_u0` |
| §1 moves commute with automorphisms and colour permutations | `BeltGraph`: `slidePath_transport`, `properOff_transport`, `target_transport`; `BeltWalk`: `slidePath_recolour`, `target_recolour` |
| §1 slide lemma | Math's `properOff_slide`; `Path.proper` |
| §1 pole invariant | `BeltGraph`: `PoleInvariant`, `poleInvariant_of_proper`, `unequalPoles_slide` |
| §4 classification | `openings_classes` (`decide` over the 14 words), `opening_classes` (on the graph) |
| §4 O1, O3a, O3b, O2 | `opening_O1`, `opening_O3a`, `opening_O3b`, `opening_O2` |
| §5 Z-state, row exhaustiveness | `ZState`, `zrow_cases` (`decide`), `rhotau_branch`, `upper_branch` (`decide`) |
| §5 fill rows S_ρ1, S_{0,1} | `row_fill` |
| §5 S_τ1 | `row_tau1` (wraps Team A's `a_tau_return`) |
| §5 S_ρτ, forced u_{i-1}=1 | `rhotau_forced_u` |
| §5 S_ρτ-A fill / return | `row_rhotau_fill`, `row_rhotau_A` (wrap Team A's `s_rho_tau_first_two` and `a_rho_return`) |
| §5 S_ρτ-B | `row_rhotau_B` (wraps Team A's `b_tau_return`) |
| §5 S_0 | `row_S0_branch`, `row_S0_fill`, `row_S0_return` (new, complete) |
| §5 families closed | built into `GoodS`, through the clause `x = 0 → y = 1`, which every S-macro re-establishes |
| §6 D | `DState`, `rowD_fill`, `rowD_return` (wrap Team A's `doubled_one_first` and `doubled_one_return`) |
| §7 linear interval | `ZInterval`, `DInterval`, `zInterval_slide`, `dInterval_slide`, `zInterval_opening` |
| §7 potential and drop of 4 or 6 | `potential`, `potential_v`, `potential_u`; the drop is a conclusion of each `macro*` |
| §7 Cap S (short, landing range, long) | `capS_short`, `capS_tau1`, `capS_A`, `capS_B`, `capS_long` (uses `BeltCapsMath.z_long_cap_impossible`) |
| §7 Cap S0 | `capS0_two`, `capS0_three` |
| §7 Cap D | `capD_prelast` (uses `BeltCapsMath.d_prelast_impossible`), `capD_last` |
| §7 macro steps | `macroS_tau1`, `macroS_A`, `macroS_B`, `macroS0`, `macroD` |
| §7 termination and length | `controls_S`, `controls_S0`, `controls_D`, `walk_of_controls`, `walk_of_opening`, `belt_unequal_normalised`, `belt_unequal` |

The finite Fin 4 facts proved by `decide` are `zrow_cases`, `rhotau_branch`, `upper_branch`, `pair_of_ne` and `openings_classes`.

## Departures from the page

These are worth Math's review.

1. **Poles fixed.** The theorem certifies the pole colours and a belt hole at the end. It also certifies them at every macro landing, through `GoodS`, `GoodS0` and `GoodD`. Intermediate holes are not separately certified to be belt vertices. The steps used are all belt slides, but `SlideStep` does not record that. A `BeltStep` relation would make this explicit if Math wants it.
2. **Long cap.** `capS_long` is proved, but the budget proof does not need it. The budget needs only that landings stay at `j ≥ 1`. That comes from `capS_tau1`, `capS_A` and `capS_B`, using `c⁰(v_0) = ρ` and `c⁰(u_1) = 1`.
3. **Cap S0 at j = 3.** `capS0_three` uses only current properness, not properness of `c⁰`.
4. **Doubled-zero route.** Team B's `TwoPoleBeltTeamB.doubled_zero_II_*` is a separately compiled upward walk for the doubled-zero opening, on its own `Vertex` type. It is not used here, and this draft does not duplicate it. O3b goes through the page's downward S0-family instead.
5. **Scope.** Only the unequal-pole belt hole at `u_0` is covered (§4–§7). Equal poles (§3), pole holes (§2), and the transfer to an arbitrary belt hole via `rot` and `ringSwap` are not drafted.

## Suggested order for Math

1. Decide whether `BeltVacancyTeamA` and `BeltCapsMath` enter the accepted build, since everything here rests on them. Alternatively, move the needed parts into one Math-owned belt module.
2. Review `BeltGraph`: the automorphisms, `SlideStep`, and the conversions. It is small and self-contained.
3. Review the definitions that carry the meaning of the theorem: `ZState`, `DState`, `ZInterval`, `DInterval`, `potential`, `GoodS`, `GoodS0`, `GoodD`, `Done`, `Controls`, and the statement of `belt_unequal`.
4. Review the rows, then the caps, then the macros and controllers. Each is local, and the bookkeeping is mechanical.
5. Re-home the modules under `Mathlib/Combinatorics/SimpleGraph/PlaneMap/`, add `#print axioms` guards in `MathlibTest`, and run your fresh-source audit.
6. Optional follow-ups:
   - a `BeltStep` version with poles fixed throughout;
   - the corollary for every belt hole, via `rot` and `ringSwap` (both proved automorphisms here);
   - §3 and §2.
