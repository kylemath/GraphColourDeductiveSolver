# Independent replay: the refutation of Conjecture L

Independent audit, 6 October 2026, 09:25 MDT. This replays Long Table's message `2026-10-06_0915_longtable_…_conjecture-L-false.md` and `creative-intel-2026-10-05/l-attack.md`.

The audit's code is `l_check.py` and `kempe_radius.py`. It imports and reads no team code. The witness data were copied as data:
- W6 from `l-attack.md` §0;
- the A_3 faces, hole and colouring from the data constants of `lattack_witness.py`.

The audit **rebuilt A_2–A_5 itself** from their description: a hub, r rings of 5 joined by antiprism strips, and a pole.

Definitions are Math's, from:
- `MathConfinementAttack` Step 1 (both locks);
- `MathCleanVertexAttack` §1 (F swaps the {c_j, c_{j+3}}-component of x_{j+2});
- `MathVHLine` §4 (Conjecture L: some absolute N with no chain s, F(s), …, F^N(s) all doubly locked; any planar graph, degree-5 v, no other hypothesis).

## Results

**Every graph is checked as a sphere triangulation**: consistent orientation, every edge in two oppositely oriented faces, Euler's formula, 2n − 4 faces. Every colouring is checked to be proper on T − v.

1. **W6** (20 vertices, degrees 3–8, hole v = 16).
   - The stated link x0..x4 = 13, 8, 3, 5, 1 is the counter-clockwise rotation at v.
   - Under F the chain s, F(s), …, F⁵(s) is doubly locked and F⁶(s) is not: **chain length exactly 6**, so Conjecture L with N = 5 is false.
   - The repeat index steps +3 mod 5 each time (2, 0, 3, 1, 4, 2), as Math's Prop. 1 says.
   - Under the reverse orientation, where F becomes Math's B = F⁻¹, the chain has length 1. L is stated for F, so this does not matter.
   - **Labelling slip in `l-attack.md` §0.** The listed link colour sequence (0,2,1,3,2) and repeat indices 4, 2, 0, … correspond to x0 = 5 (link 5, 1, 13, 8, 3), not to the stated x0 = 13. This is a rotation of the labels, with no effect on any claim.
2. **A_3 witness** (17 vertices, twelve of degree 5, five of degree 6, minimum degree 5).
   - The F-orbit is **periodic with period exactly 60**, and all 60 states are doubly locked, so the chain is infinite. The same holds in the reverse orientation.
   - The team's A_3 is isomorphic to the audit's own A_3, by a planar code with v fixed.
3. **Exhaustive census on the audit's A_r**, with x0's colour fixed, over all proper 4-colourings of T − v:

   | Graph | Order | Colourings | 4-colour links | Doubly locked | Infinite chains (all period 60) | Longest finite chain |
   |---|---|---|---|---|---|---|
   | A_2 (icosahedron) | 12 | 120 | 60 | 0 | 0 | – |
   | A_3 | 17 | 600 | 360 | 180 | **120** | 1 |
   | A_4 | 22 | 3,120 | 1,920 | 480 | **120** | 1 |
   | A_5 | 27 | 16,320 | 10,080 | 3,180 | **360** | 3 |

   - The infinite-chain counts 120, 120 and 360 match the team's, and A_2 has none, as the team says.
   - The team reported "chain length ≥ 40 (cap)" for these. The audit shows they are **exactly infinite** (periodic).
   - **A_4 and A_5 were not verified by the Long Table lead. They are now verified independently.**
4. **The refutation does not touch VH∃** (the team's claim 3, which the lead did not recheck). These are complete Kempe classes in T − v, over canonical states:

   | Witness | Class size | Filled | Kempe distance to the nearest filled state |
   |---|---|---|---|
   | W6 | 127 | 63 | 2 |
   | A_3 witness | 100 | 40 | 3 |
   | All 120 infinite-chain states of A_3 | 100 | 40 | 2 (60 states) or 3 (60 states) |
   | All 120 of A_4 | 520 | 200 | 2 |
   | All 360 of A_5 | 2,720 | 1,040 | 2 |

   The team sampled 12 states on A_4 and A_5; the audit checked all of them. No targetless component is involved, so the replay confirms the team's reading: L is false, and "L ⇒ clean vertex" is true but unusable.

## Adversarial notes

- **The objection "W6 has degree-3 vertices" does not save L.** A_3–A_5 are minimum-degree-5 triangulations, with degrees 5 and 6 only. So L fails also inside the class the induction uses.
- **Conjecture R** (the Kempe radius to a filled state is bounded by an absolute R) is the natural repair. Two points:
  - R is **stronger** than the clean-vertex statement: it bounds the distance, not only its finiteness.
  - It is essentially the pure-Kempe form of Math's P(K, R) from `MathTerminationUnconditional.md` §3. It should be stated with that link, and pre-registered as the team proposes (S2) before any search.
  - The radii found so far (2–3) are on symmetric or hill-climbed instances, which is weak evidence for a bound.
- **Pre-registration.** The hill-climb reached W6 before it was registered. A refutation is a certificate, so this does not matter for the kill. It does mean the hill-climb's "max chain" statistics are not evidence for anything.

## Files

- `l_check.py`, `kempe_radius.py`
- `out/l_check.json`, `out/l_check.err` (A_r census lines and timing)
- `out/kempe_radius.json`
- `SHA256SUMS`

Cost: about 2 CPU-minutes.
