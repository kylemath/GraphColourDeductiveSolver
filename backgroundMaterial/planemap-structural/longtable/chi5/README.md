# χ = 5 surface test of LPC (Studio Job 6, 13–14 Oct 2026) [exploratory, data]

## Question

Take a surface triangulation T with χ(T) ≥ 5 and a degree-5 hole h with T − h 4-colourable (a *good hole*).
- No state of T − h is filled, since a filled state would extend to a 4-colouring of T.
- So LPC (TrackF §8–9) demands that every Kempe class of T − h contain a lock-parity violator.
- A **parity-clean class** here is a counterexample to surface-general LPC. By TrackF §8.1 it must consist only of
  states on all-DL π-cycles.

## Tools

| file | role |
|---|---|
| `chilib.py` | exact k-colourability by SAT (CaDiCaL), good holes, non-4-colourable seeds: K7 (torus), K6 (RP²), K6#K6 (Klein), K7#K7 (genus 2), K6#K6#K6 and K7#K6 (rp2x3) |
| `bt_colour.py` | independent check: DSATUR backtracking colourer, no SAT |
| `scan_existing.py` | 4-colourability of every graph line in TrackF `out/` and `graphs/` |
| `analyse.py` | aggregates TrackF `kclass4` output at good holes |
| `walk.py` | annealing flip walks (min degree 5) keeping T non-4-colourable (exact SAT at every step); `--control` runs the same objective on 4-colourable T at all degree-5 holes |

The class engine is TrackF `src/kclass4`, used unchanged.

## 1. Existing data (`out/existing_*`)

- TrackF's data already contains **630 non-4-colourable triangulations**: torus 34, Klein 68, RP² 34, genus 2 261,
  rp2x3 233.
- They have **1,132 good holes**.
- SAT and DSATUR agree on all 930 graphs checked and all 1,132 holes.

| surface | good holes | classes | singletons | all-DL π-cycles | parity-clean classes | violator fraction per class: min / median |
|---|---|---|---|---|---|---|
| torus | 158 | 340 | 185 | 0 | 0 | 0.50 / 1.00 |
| Klein | 110 | 603 | 181 | 0 | 0 | 0.22 / 1.00 |
| RP² | 48 | 243 | 61 | 0 | 0 | 0.82 / 1.00 |
| genus 2 | 466 | 909 | 405 | 0 | 0 | 0.57 / 1.00 |
| rp2x3 | 350 | 950 | 318 | 0 | 0 | 0.67 / 1.00 |

There are 0 filled states (as there must be) and 0 Theorem P failures. Class sizes go up to 7,150.

## 2. Annealing walks vs power control (`out/walks_best_events.jsonl.gz`, `out/control_hits.jsonl.gz`)

**Setup.** 22:06–01:10, `nice -n 10`, 6 χ = 5 workers and 6 control workers (12 χ = 5 workers for the first minute).
Each walk is 1,500 flip attempts at temperature 3, n = 12–40.
- **Score:** a parity-clean class at a good hole; then all-DL π-cycles; then the longest DL π-run; then a low
  violator fraction; then the number of good holes.
- **χ = 5 walks** start from the 630 graphs or from grown seeds.
- **Control walks** start from TrackF `surfaces.make` (random 4-colourable T), use every degree-5 hole, and stop at the
  first all-DL π-cycle.

| surface | χ = 5: walks / flips | χ = 5: walks with an all-DL π-cycle | χ = 5: max DL π-run | χ = 5: min violator fraction | control: walks / flips | control: walks reaching an all-DL π-cycle | control: median flips to hit | control: max DL π-run |
|---|---|---|---|---|---|---|---|---|
| torus | 5,527 / 8.29M | **0** | 11 | 0.250 | 1,138 / 1.66M | 57 (5.0%) | 672 | 60 |
| Klein | 5,213 / 7.82M | **0** | 12 | 0.222 | 2,061 / 3.00M | 106 (5.1%) | 604 | 84 |
| RP² | 3,084 / 4.63M | **0** | 5 | 0.400 | 761 / 1.04M | 91 (12.0%) | 365 | 171 |
| genus 2 | 3,278 / 4.91M | **0** | 11 | 0.250 | 1,881 / 2.81M | 9 (0.5%) | 791 | 58 |
| rp2x3 | 3,432 / 5.15M | **0** | 12 | 0.222 | 1,393 / 2.06M | 36 (2.6%) | 762 | 38 |

There were **0 parity-clean classes** at good holes in all 20,534 χ = 5 walks.

## Reading

- **LPC survives the χ = 5 test**, and the null is meaningful:
  - with the same objective and budget, the 4-colourable control reaches all-DL π-cycles in 0.5–12% of walks on every
    surface (median 365–791 flips);
  - at good holes of χ = 5 triangulations the walks never get one. The longest DL π-run is 12, against cycle lengths
    of 20 or more.
  - On every surface the control's flip budget was smaller than the χ = 5 walks' (1.0–3.0M against 4.6–8.3M), so the
    χ = 5 walks had the larger budget.
- **Caveat.** The χ = 5 walk moves in a smaller space. Any flip that makes T 4-colourable is rejected, and T − h at a
  good hole has few colourings (median class: all violators; 1,150 frozen singletons in the existing data). So the null
  may reflect how rigid near-critical graphs are, rather than a law. It is evidence, not proof, and n ≤ 40.
- **Fable's flag.** If this were the whole story, LPC would look surface-general at χ = 5 holes. The data say only
  this: all-DL π-cycles, the prerequisite for a parity-clean unfilled class, were never produced at a good hole.
