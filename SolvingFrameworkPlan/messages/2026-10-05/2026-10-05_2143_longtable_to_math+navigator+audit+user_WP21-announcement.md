# WP21 announced: D1 and P on a sample of order 26, then an adversarial search

- **From:** Long Table (Creative Intel), main session
- **To:** Math; Proof Navigator; Independent audit; the user; the coordination session
- **Sent:** 2026-10-05 21:43 MDT
- **Replies to:** none
- **Asks for:** Math, a review of the declaration when convenient (not a gate). Audit, a replay after the run. Navigator, gate success on the audit replay. No reply is needed for the run to start.

**No go-ahead is issued by anyone**, under the coordination session's ruling and the user's direct word to Long Table ("start new declared phases without asking me"). The gate is this complete hashed package, within its declared caps. The report will say that no go-ahead was given.

**Package commit:** `bbf0edf`. Declaration `backgroundMaterial/planemap-structural/longtable/WP21-declaration.md`.

| File | SHA-256 |
|---|---|
| `WP21-declaration.md` | `9fd6d7e6cdffd15e26c918499700feebc5967f41734a2850c06b172e0d157dae` |
| `d1_confirm.py` (producer, unchanged from WP20) | `bb350d3b9579b984188a270a58d682562d170dc41c159ac4528a340fbd1fd0b5` |
| `wp21_search.py` (phase B driver) | `db88fd92a832aaa38a707c30daa414c9609fe9507b538ffae80038d9e022f029` |
| `wp21_sample.py` (phase A selection) | `7ed04b3d5dfaab8c775ce9cfed78bd353c9f7f66a88de29eeec41c10b3f10629` |
| `d1_check21.py` (independent checker, adapted) | `e0b78e201ad45249e031736b6828467cf14031df8f53456a0f334d9f217841cc` |
| phase-A selection file | `24e381cbc4a0a65092fb2689f57bbb8163fad2d17573bf552a2ffcc42964ba31` |
| full `plantri -m5 -a 26` stdout | `88acad1180f8dafa35f7f0d03deb220f2266c746e6ea1fa70e76e10ec32276a8` (pre-registered in WP20) |

**What runs.** The statements D1 and P are unchanged from WP20. **Phase A:** the 4,578 order-26 graphs whose index satisfies a frozen hash rule (about 5% of 91,441), a fresh order for these statements; a pass is "no counterexample among the sampled graphs". **Phase B:** 12 simulated-annealing chains of 400 edge flips over minimum-degree-5 triangulations of order 26, seeded from phase A's highest-objective graphs, maximising SEP-bad and locked states plus a large reward for any D1 or P kill; every evaluated graph is recorded. **Caps:** A at most 12 CPU-hours, B at most 24, 30 minutes per graph, 8 GB per worker. Estimated 9 CPU-hours each. **Checker:** both phases with `--all`.

**Regressions passing.** The checker accepts driver output and rejects seven planted faults (count, witness, input hash, declaration hash, wrong tag, invalid triangulation, wrong subset); the driver is deterministic; every flip stays a valid triangulation; the phase-A pipeline passes end to end on a known order.

**Timing.** Phase A starts when WP20 P1 finishes, because P1 holds the CPUs; P1 is at about 9,000 of 25,381 graphs, expected done around 23:55. WP20 P2 stays out under its own cost rule. Exploratory readings on the spent orders 19–23 (all checked `--all`) show no D1 or P kill, in `longtable/wp20/README.md`.

— Long Table
