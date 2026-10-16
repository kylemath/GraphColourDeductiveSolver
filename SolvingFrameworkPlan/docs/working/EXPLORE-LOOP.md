# Exploration loop: short rounds over the open gaps (started 16 Oct 2026)

Why: Kyle (16 Oct): the programme was waiting on day-long searches instead of exploring the space between loose
connections. Since 14 Oct each step was "pre-register, run the complete enumeration, wait, then decide". The single tests
that decide things are fast (dfast at ring <= 15 takes 0.2-40 s; defectc K = 3 takes seconds). The slow parts are
exhaustive enumeration, rings 17-19 and Lean. Those keep running, but nothing waits on them any more.

## The loop

1. **Pick a gap** from the register below (the one whose answer would change the most, cheapest first).
2. **Write 3 lines** in the log: the question, my guess, what result would change the plan. (Falsification-first, kept
   short. Full pre-registration is still required before a result becomes a claim on the board.)
3. **Probe** with a hard cap: about 30 minutes wall, at most 3 cores, samples instead of enumerations, "assume X is
   reducible and see what is left" before proving X.
4. **Log** one paragraph: what came out, what it means, the next probe. Commit by explicit path.
5. **Spin off** anything that needs hours (complete enumeration, rings >= 16, Lean) as a background job: add it to the
   background table, never wait on it, fold its result in when it lands.

Rules kept from the charter: engine-level results are exploratory until a second engine or Lean; nothing here edits
COORDINATOR-STATE.md (the coordinator thread does); errata the same day.

## Gap register (the loose connections, 16 Oct)

| id | gap | where it stands | cheapest next probe |
|---|---|---|---|
| G1 | d = 7..15: which reducible family is locally unavoidable near 7s? | H7b survives: B-fixed configs kill all 418,551 K <= 4 candidates found (search incomplete). Lemma B done (Lean). Lemma A open | lemma A as a finite check (stream A); K = 5 defects by randomised search (round 4) |
| G2 | rules: does a discharging rule reach t* <= 0 at d = 7..15 once the G1 family is forbidden? | Job 28 (Studio): rooted-word LP loop, t* = 5/17 after round 1, predicted to stall on the rule class | richer rule classes on small LPs (stream R) |
| G3 | 7-wheel 5666567 C-reducible (lemma B) | DONE: cfast + independent Python (round 3) + Lean (CWheels.lean, 4d799f71) | other C-candidate 7-wheels and 565xxx 6-wheels only if a defect needs them |
| G4 | "appears" for receiver centres 7..15 (Job 26 covers 2-balls at 5s) | open | check whether the B2 hand argument transfers to receiver-centred configurations |
| G5 | folded rings, Job 26 piece (ii) | Studio, Lean, 20 Nov kill | (Studio) |
| G6 | 6-wheels with a letter >= 8 counted reducible, untested | untested | not needed while defects use letters 5-7 only |
| G7 | defect_check2 marks a candidate killed when a configuration's ring is not a simple induced cycle, with no reducibility verdict (B-fixed case: no expansion tried) | found in round 4 | count how many H7b kills rest only on that; decide whether a non-simple ring forces a short separating cycle (stream E) |
| G8 | defects with K >= 5 rings | rounds 4-5: ~950 sampled, plus ~660 pruned seeds; no R_opt survivor | longer pruned runs (background) |
| G9 | defects containing a vertex of degree >= 8 (defectc uses 5-7 only) | never searched | extend defectc's alphabet to 8 |

## Background jobs (never waited on)

| job | where | expected | feeds |
|---|---|---|---|
| studio14c: Lean for 43 K <= 1 keys, rings 17-18 | Studio | ~16 Oct midday | K <= 1 claim |
| studio14d: ring-19 key | Studio | ~22 Oct | K <= 1 claim |
| run24b: ring <= 16 per-key modules | Studio | 16 Oct | Lean chain |
| H7b: K = 4 defect search vs R_opt+ | done 16 Oct (README 7.3.1), centre 7 far from complete | G1 |
| Job 28: long-run version of the defect loop (wheeldis/JOB28.md) | Studio | running | G1 |
| Job 26 (ii) vertex splitting | Studio | 20 Nov kill | G5 |

## Log

See `EXPLORE-LOG.md` (newest first).
