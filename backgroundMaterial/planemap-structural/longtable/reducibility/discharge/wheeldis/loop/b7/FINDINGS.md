# Round 10: do the d = 7 LP binders sit inside isolated defects? (16 Oct 2026) [exploratory, engine level: dfast only, no Lean]

**Binders.** The 7 d = 7 receivers that carry the round-9 certificates (`binders.txt`, link and s word):
- 5 from the one-step baseline, t >= 33/119;
- 2 from the oracle, t >= 3/11.

**Question.** Can a binder's 2-ball (u = 7, link and s fixed, p slots free) be completed to an isolated positive
defect (README §7 test G) centred at u, and does any completion survive R_opt+?

## Tools

- `defectb7.cpp`: `loop/g9/defectc8.cpp` plus an optional 9th argument LINK:RING2. It fixes the ring-1 word and the
  ring-2 letters at the s positions; the p slots stay '.'. Build it with `g++ -O2 -std=c++17 -o defectb7 defectb7.cpp`.
  - Validated on 5555558: with ring 2 fully fixed it reproduces the one leaf, and with 2 letters free it reproduces
    all 4 matching leaves of `g9_K3_c7.out`.
- `b7match.py`: matches binders (all dihedral images) against leaf files. Positive control: a reflected leaf from
  `c7k4.txt` is found.
- `mkfix.py`: writes the LINK:RING2 arguments (`fix.txt`).
- `runk4.sh`: runs the K = 4 searches, 3 at a time.
- `kcheck.py`: `defect_check2` (bf) with a log of every D kill and the 7 it sits at (`kills_m7.txt`).
- `tof.py`: compares canonical keys (lemmaA `la.ckey`). It shows that a hash-named D configuration is a B-fixed
  configuration of a binder, and names it f7_ (a wlp3 pattern).

## Results

| binder (link/s) | certificate weight | K = 3 leaves | K = 4 leaves (letters 5-7) | after R_opt+ |
|---|---|---|---|---|
| 5575576/6666656 | base 0.008 | 0 | 0 | none to check |
| 5765575/7565777 | base 0.101 | 0 | 512 | all killed |
| 5567576/6755556 | base 0.025 | 0 | 4 | all killed |
| 5675765/6575575 | base 0.202 | 0 | 1,536 | all killed, each at the centre by f7_5567576_56.75.7 |
| 5675756/7555565 | base 0.025 | 0 | 6 | all killed, at the centre |
| 5676575/6556666 | oracle 0.182 | 0 | 0 | none to check |
| 5765756/5556666 | oracle 0.182 | 0 | 6 | all killed |

- **K = 3** (letters 5-8): no completions at all.
- **K = 4** (letters 5-7): complete for these 2-balls. 2,064 leaves in total.
- **R_opt+.** The existing registries kill 1,973 of the 2,064.
  - dfast runs (`k4_m7_tested.d`, `d14.out`, `e15.out`; copied to `out/def_b7_*.out`) kill the rest: ring <= 14,
    105 D of 260; ring 15, 2 D of 8.
  - Every leaf has a D kill, and all are still killed with `strict7`.
- **Not run.** K = 4 with letter 8 (stopped for CPU), and K >= 5.

## By-product: four B-fixed D configurations that forbid binders directly (`b7f.out`)

| pattern | ring | binder it forbids |
|---|---|---|
| f7_5567576_56.75.7 | 15 | 5675765/6575575, base weight 0.20 |
| f7_5656757_657.555 | 13 | 5675756/7555565 |
| f7_..65757_..6555. | 12 | 5675756/7555565 |
| f7_..55756_..6666. | 13 | 5676575/6556666, oracle weight 0.18 |

- Each was rebuilt with gen28's own `make` and rerun with dfast: D, with the same `reached` counts as the hash-named
  originals.
- They were first found as hash-named configurations (`b...` / `g...`), which wlp3 cannot read.

## Verdict

H-B7 survives.
- No binder completes at K = 3.
- Every K = 4 completion dies to R_opt+, by a D configuration.

So near u (K <= 4) the d = 7 binders are not test-G obstructions. They hold only for the rooted-word rule class on
the current pattern set. 3 of the 7 are now forbidden outright by the patterns above.
