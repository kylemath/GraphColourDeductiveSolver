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
| G2 | rules: does a discharging rule reach t* <= 0 at d = 7..15 once the G1 family is forbidden? | 5/17 certificate reducible (rounds 5-6); floor now >= 2/7, carried by lone fives at d = 10 (a counting bound, rule class irrelevant). LP loop: Studio loop28b | lone-five family at d = 9..12 (round 7, `loop/lone/`) |
| G10 | lone-five family: receivers of degree d with more than d - 6 lone fives (only u big) | d >= 12 clear; d = 9: 2, d = 10: 15, d = 11: 7 arrangements left (round 9, lone10.txt); no longer binds the LP (binders at d = 7) | B-fixed lone sets at ring 16+ only if the LP returns to d >= 9 |
| G3 | 7-wheel 5666567 C-reducible (lemma B) | DONE: cfast + independent Python (round 3) + Lean (CWheels.lean, 4d799f71) | other C-candidate 7-wheels and 565xxx 6-wheels only if a defect needs them |
| G4 | "appears" for receiver centres 7..15 (Job 26 covers 2-balls at 5s) | open | check whether the B2 hand argument transfers to receiver-centred configurations |
| G5 | folded rings, Job 26 piece (ii) | Studio, Lean, 20 Nov kill | (Studio) |
| G6 | 6-wheels with a letter >= 8 counted reducible, untested | untested | not needed while defects use letters 5-7 only |
| G7 | defect_check2 marks a candidate killed when a configuration's ring is not a simple induced cycle, with no reducibility verdict (B-fixed case: no expansion tried) | CLOSED for K <= 4 (round 6): 0 of 418,551 kills rest on it; rule changed to 'open' | none |
| G8 | defects with K >= 5 rings | rounds 4-6: ~950 sampled, plus ~660 pruned seeds; no R_opt survivor. Conditional on A(3) (f3 tables, which lemma A does not support as a blanket rule): 808 centre-7 seeds and two 45-min complete runs (stopped at the cap), 0 leaves | longer pruned runs (background) |
| G9 | defects containing a vertex of degree >= 8 (defectc uses 5-7 only) | K <= 3 with letters 5-8: none survives (centre 8 complete, round 9); centres 9-12: K = 2 empty, K = 3 capped all killed (round 6-7) | K = 4; complete K = 3 for centres 9-12 |

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
