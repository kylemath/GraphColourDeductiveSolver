# Twin-hole mirror sums (exploratory, 13 Oct 2026)

Status: exploratory and post hoc. Nothing was predeclared, so none of this is evidence for any statement in the
proof programme. Its purpose is to find deeper puzzle levels for the game (4square) and the RL arena.

## The construction

- Take a census map G: a triangulation with one hole h, where h is a removed degree-5 vertex.
- Glue G to a second copy of itself along one face triangle Δ = (x, y, z) that avoids the hole. Drawn on the
  sphere, the copy is the mirror image; for Kempe moves only adjacency matters.
- Both copies keep their hole. A start is filled when **both** rims use at most 3 colours.

This is the user's mirror-doubling idea, glued at the triangle where the sphere was cut, so the hole survives
alongside a copy of the whole graph.

## The model (`twinhole.py`; vectorised BFS in `twinhole_np.py`)

**States.** Fix the colour renaming by colouring Δ as (0, 1, 2). A joint state is then a pair (i, j) of
colourings of G − h that both use (0, 1, 2) on Δ. The joint space is exactly S × S, where S is the number of
single-hole states.

**Moves.** Each move falls into one of two kinds:
- **An (a,b)-chain on one side that misses Δ.** It is a whole chain of the glued graph, so the move is
  (i, j) → (swap(i), j), or the same on side j. It is never the only (a,b)-chain, because Δ always holds a or b,
  so it is never a renaming.
- **A colour pair at Δ.** Δ uses three of the four colours, so every pair (a,b) meets it. The Δ vertices coloured
  a or b are adjacent, so they lie in one chain K = C_i ∪ C_j. Swapping K and then renaming a↔b gives
  (T_p[i], T_p[j]).

**Depths.** Exact BFS from the jointly filled set. The single-hole depth dG uses the same moves on one side. It
matches `~/4square/kempe_engine.py` exactly: the dF histograms are identical on C30, the icosahedron,
Tidy Trap and the 66666 six-ring. The two BFS codes give identical histograms on Tidy Trap and 66666.

**Inputs.** `~/4square/maps/*.json` at 4square commit d1ff4e3, without the onboarding maps `ob*`. Two faces per
map: `far` is the face farthest from the hole; `near` is the closest face that avoids the hole.

## Results

| map | S | single-hole max dG | twin max dJ (far / near) | starts at the max (far / near) |
|---|---:|---:|---:|---:|
| warm-up 9, 13, 18 | 7–63 | 1 | 1–2 | – |
| icosahedron | 20 | 1 | 2 / 2 | 50 / 34 |
| p22#196 | 502 | 2 | 4 / 4 | 10 / 8 |
| C30#0 | 100 | 3 | 4 / 4 | 598 / 416 |
| six-ring 66666, order 28 | 1,118 | 4 | 5 / 5 | 34 / 34 |
| Tidy Trap, order 17 | 64 | 4 | **6** / 5 | 6 / 34 |
| **p34.r178#11764701** | 7,481 | **6** | **7 / 7** | **80 / 20** |

- On every map tested, every twin start fills; none is unsolvable.
- **The twin adds at most 2 moves** over the harder of its two sides: dJ − max(dG(i), dG(j)) ∈ {0, 1, 2}
  everywhere.
- **The game's previous record depth of 6 is beaten.** p34.r178's twin has 80 starts at joint depth 7 (far face)
  and 20 (near face). Each pairs the side-state at single-hole depth 6 with a side at depth 1–2. Examples are in
  `deepest_pairs` in the results files.
- **Symmetric starts (i, i)** take dJ ∈ {dG(i), dG(i) + 1}, never more. Copying a move to the mirror is free only
  for chains through Δ. A chain that misses Δ has a separate copy on each side, so mirroring it costs a second
  swap.
- **Skipped:** C60 dual (S = 4,840) and p31–p34 except r178 (S = 5,459–10,634). These are within reach of
  `twinhole_np.py`, but each holds 30–113 M states. p34.r178 took 56 s and about 0.5 GB per face on the MacBook.
  Only p34.r178 has single-hole depth 6, and p34.r210 is the only other with depth 5.

## Hand facts behind the design (not reviewed)

1. **Projection lemma.** If a graph D is G and G′ glued along a common subgraph, then every Kempe chain of D, cut
   down to G, is a union of whole chains of G. So the G-side colourings reachable through D lie in G's own Kempe
   class: gluing never unlocks anything.
2. **When the glue is a triangle,** the cut-down part is one chain of G or nothing, because two Δ vertices of the
   pair's colours are adjacent. Each move of D is then at most one move on each side. With a 4- or 5-cycle as the
   glue, chains can merge through the copy, which adds locks.
3. **Corollary.** If the copy is a full triangulation without a hole, the single-hole puzzle is unchanged
   (dJ = dG). Twin holes are the variant that can get deeper.

## Next

- **Use it in the game.** Twin levels need two holes in the game engine and level format. As far as checked, the
  current game supports one hole; that is a product decision for the user.
- **Run p34.r210** (S = 10,634, about 113 M states, about 1 GB) when the machine is plugged in.
- **Try gluing along a separating 4- or 5-cycle.** By fact 2 this adds locks and may go deeper still.

## Addendum, 13 Oct 2026: the two win rules

**The two rules.**
- **Simultaneous** (dJ, above): both rims must be at ≤ 3 colours at the same time.
- **Sequential** (dS, `maxSeq` in `twinhole_np.py`): as soon as one rim is at ≤ 3 colours, that hole is filled
  (no swap is counted) and becomes an ordinary coloured region; then the other hole is played.

**Computing dS.** After the first fill, that side is a full triangulation glued at a triangle. Hand fact 3 then
makes the remaining cost exactly the other side's dG. So dS is a BFS that starts from these end costs.

**Brute-force check.** On Tidy Trap's twin (far face), a separate brute force builds the after-first-fill states
explicitly: one side fully coloured, with every free-colour choice. It runs a 0–1 BFS without using fact 3 and
gives the same values on all 4,096 starts.

**Observed: dS = dJ on every start tested.** That covers C30, p22, Tidy Trap (both faces) and the C60 dual (far
face). The histograms match, and so does every individual start.

**Conjecture (open): when side i is filled, dJ(i, j) = dG(j).** dJ ≥ dG(j) holds by projection. For the other
direction, lift an optimal single-hole path for j. Chains that avoid Δ leave side i alone. A move through Δ also
swaps side i's Δ-chain K_i for the same colour pair (a, b), and that keeps i filled unless:
- the free colour c of side i's rim is in {a, b}, and
- K_i holds some, but not all, of the rim cells of the other colour.

That single case is the gap. No counterexample is known.
