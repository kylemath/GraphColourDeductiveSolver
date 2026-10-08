# Track K: Conjecture F (Route Q), proved [hand, unreviewed]

8 Oct 2026. Brief: find a hand proof of Track C's Conjecture F (`TrackC/README.md` §6.4).

## Status

**F is true as stated on the sphere.** The full proof is in `FProof.md`.
- It is **[hand, unreviewed]**.
- Every step is checked separately against data, with 0 failures:

| run | sphere hole states | of which parallel diagonal | no-hole sphere colourings | torus hole states | torus no-hole colourings |
|---|---|---|---|---|---|
| scale 6 (`tk_check_x6.log`) | 165,251 (min5 72,339; min3 67,864; Census29 frame class 25,048) | 42,340 | 14,400 | 14,553 | 2,520 |

- Sphere: 0 failures of S1–S7 (each proof step and F itself).
- Torus: 0 failures of the local steps and of the exact torus prediction S8 (residue = 2G, with G = 0/1/2/3 on 2,099/4,509/6,274/1,671 hole states).
- No correction to the statement is needed.

## The argument in five lines

1. **F0 (no hole) is Tutte's parity theorem in mod-4 form.**
   - For each partition {XY|ZW}, Euler/Jordan for the Tait 2-factor S_i gives:
     - `2p(XY) − k_i = |X|+|Y| − e(XY)`;
     - `p(XY)+p(ZW) = k_i + 1`.
   - Summing over the three partitions containing colour A: `N ≡ n + 1 + deg(A) ≡ n + 1 + d`.
   - Fisk's degree, by a local edge-cancellation argument, gives `cw = n − 2 + 2d`.
2. **Hole.** Fill the pentagon with the diagonals x₁x₃ (μA) and x₁x₄ (μB).
   - The colouring stays proper.
   - These are exactly the two lock edges, so `N(T−h) = N(T°) + 2 − L1 − L2`.
3. The three new faces all have Tait orientation `hand` (finite table), so `cw(T°) = cw + 3·hand`.
4. F0 on T° (n − 1 vertices, parallel edges allowed) then gives F immediately.
5. **Torus.** Every step is local except `#regions = k_i + 1`. On genus g the residue of F is exactly `2(G₁+G₂+G₃) mod 4`, where G_i is the total genus of the regions of S_i. This explains the ~50% failure rate exactly (0 mispredictions).

## Consequences

- F needs neither Theorem D nor the Jordan arguments at the hole. Its only planar input is Proposition 1(b) for one map.
- With Lemma W (Track C sketch, still unreviewed), F gives:
  - **Theorem 6**: a second proof, avoiding Lemma R and the disc structure;
  - **Remark 7**, which had no proof before.
- For Lean Route Q, what remains is W plus Tutte's identity for a sphere map (`FProof.md` §3, remarks).

## Files

- `FProof.md`: the proof, the data table, the torus explanation and the literature.
- `scripts/tk_tables.py`: exhaustive finite tables T1–T3 (0 mismatches).
- `scripts/tk_check.py`: checks each step S1–S8 of the proof on states. It reuses `TrackI-review/ri_core.py` and `TrackC/scripts/tc_mod4.py` read-only.
- Logs: `scripts/tk_check.log` (scale 1, about 30 s) and `scripts/tk_check_x6.log` (scale 6).

## Literature

Tutte's parity theorem and Fisk's degree, as presented in arXiv:1912.07205 ("The Last Temptation of William T. Tutte"), Thms 1 and 3.
