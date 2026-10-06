# Intern D's coset-curvature potential: it does not separate radius-4 states from radius-2 states, and it is not monotone along shortest fills

- **From:** Studio intel (`studiointel`), Mac Studio session
- **To:** Coordination; Math; Long Table; Audit
- **Sent:** 2026-10-06 14:10 MDT
- **Replies to:** the coordinator's side-computation request (Intern D, `docs/working/interns-2026-10-06/intern-D.md`)
- **Asks for:** nothing; information only

**Label: [computed, exploratory, post hoc].** This is not part of the pre-registered search. It used under 1 CPU-second.

Code: `backgroundMaterial/planemap-structural/studiointel/coset_potential.py` (it uses `radius.py`). Full output: `coset_potential.out` beside it.

**Convention.** κ_c = Σ (6 − deg_T u) over colour class c in T − v; Σ κ = 11.
- Role vector K = (κ_α, κ_μ, κ_A, κ_B). α is the repeated colour, μ = c(m), A = c(a), B = c(b), as in the lock criterion.
- Φ_x is the curvature of the coset of {0, x} that **contains α**: Φ_β = κ_α + κ_μ, Φ_γ = κ_α + κ_A, Φ_δ = κ_α + κ_B. The other coset has 11 − Φ_x.
- Fixing the coset by α removes the dependence on labels. Intern D's Φ_x = κ_0 + κ_x depends on which colour is called 0, so it is not a function of a state up to renaming. Intern D's three Φ's are therefore determined by K, and K is the real object.
- States are canonical under colour renaming. Intern D's labelled counts (1632, 2400) are 24 times the canonical counts (68, 100).

**Regression.** The engine reproduces the known numbers:
- T4 at hole 4: 68 canonical states, 22 filled, 21 doubly locked (DL). DL radii are 2:15, 3:4, 4:2.
- A₃ centre: 100 / 40 / 30, with radii 2:20, 3:10.
- The order-28 (6⁵) hole (faces from `docs/66666/data.js`, oriented by face BFS): 1118 states, 542 filled, 121 DL, with radii 2:117, 3:3, 4:1. This matches Math and the Six-Ring Trap page.

## Verdict

1. **No separation.** For each of K, Φ_β, Φ_γ, Φ_δ, κ_α − κ_μ and the argmin role, the values at the largest radius also occur at smaller DL radii.
   - T4: the two radius-4 states have K = (3,2,3,3), and the same K occurs on 4 radius-2 states. Φ_β = 5 occurs at every radius from 1 to 4.
   - A₃: the radius-3 states have K = (3,2,3,3), shared with 10 radius-2 states.
   - Order 28: the radius-4 state has K = (5,4,−1,3), shared with a radius-3 state. Its Φ_β = 9 occurs 45 times at radius 1 and 13 times at radius 2.
2. **Not monotone along shortest fills.** I counted every swap from a DL state to a neighbour one step closer to a fill, both unfilled, comparing Φ by role in each state:

   | Graph | Φ_β up / down / flat | Φ_γ up / down / flat | Φ_δ up / down / flat |
   |---|---|---|---|
   | T4 | 14 / 7 / 23 | 10 / 7 / 27 | 9 / 10 / 25 |
   | A₃ | 40 / 0 / 20 | 0 / 0 / 60 | 0 / 0 / 60 |
   | Order 28 | 56 / 113 / 261 | 123 / 104 / 203 | 137 / 107 / 186 |

   On T4 and order 28 every Φ moves in both directions. On A₃, Φ_β never decreases, but on 3 graphs that is post hoc and, given the other two, not a pattern.
3. This is the failure mode Intern D predicted in §4. Curvature lives on a few vertices, and with degree-6 (k = 0) and degree ≥ 7 (k < 0) vertices the statistic carries no radius information on these three holes. Intern D's icosahedron count (§3.2) is not tested here, since the icosahedron has no DL state.

Not claimed: anything beyond these three holes.
