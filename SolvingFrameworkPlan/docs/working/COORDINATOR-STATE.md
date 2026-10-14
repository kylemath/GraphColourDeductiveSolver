# Coordinator state: read this first

Owner: Long Table (Claude), running the programme autonomously since 14 Oct 2026 by Kyle's delegation.
Every coordinator session and scheduled check-in reads this file first and updates it before ending.
Background and history: `CoordinatorPlan.md` (13 Oct revision and later sections). Charter: below.

## Charter (Kyle, 14 Oct 2026)

- **Claude decides alone:** runs inside the three tracks and gates; Studio jobs; local agents; stopping lines that hit their
  written kill criterion; commits/pushes to Kyle's repos (explicit paths); errata; arena and lab-game work; parking ideas.
- **Kyle decides:** 4square production deploys (Claude prepares, hands him the command); anything public beyond the repos;
  opening a new line or dropping a deadline goal; money; compute that would touch EEGLearn.
- **Contact Kyle** only through the daily digest, except: a finding that changes the deadline goals, broken prod, a deploy needed.
- **When unsure:** ask the `sounding-board` agent (`.claude/agents/sounding-board.md`); log the exchange below.
- **Rules kept:** falsification-first (hypothesis + kill criterion written before a run); no claim counts without a second
  engine or Lean; errata the same day; commit by explicit path; check `pmset -g batt` before heavy local runs.

## Kyle's status page

https://claude.ai/artifact/6qHXnnJhWsY9jX1WyyKRpG (source `status-page.html` here). Rewrite it, never append, whenever the board changes: where we stand, running now, the 5 most important recent results, gates, needs-you. Republish with `url` from other sessions (read it first).

## Deadline goals (≈ 27 Dec 2026)

1. Verified-checker paper (Track 2). 2. Combinatorics paper: curvature-organised unavoidable set / 2-ball reducibility
(Track 1). 3. Long shot: a full proof via Track 1.

## Board

| Item | Track | Owner | Status | Next gate | Evidence |
|---|---|---|---|---|---|
| B8 discharging LP: must a degree-5 vertex with a safe 2-ball exist? | 1 | Long Table agent | started 14 Oct | 24 Oct | `longtable/reducibility/discharge/` |
| B7 2-ball family: ring 16, then 3-balls around failing (7/8) 2-balls | 1 | Studio | queued behind B8 first read | 24 Oct | `wheels/studio/` |
| B3 checker soundness (loop invariant, planar Kempe-matching step) | 2 | Long Table agent | not started | 7 Nov | `reducibility/dcheck/` |
| B2 Birkhoff separating 4/5-cycle reductions in Lean | 2 | Long Table agent | not started | 7 Nov | — |
| Arena hard set v1: 302 maps (150 census floor-tight, 50 glued, 2 R0, 100 non-reducible 66666 2-balls); max distance 2–3 | 3 | Studio | DONE 14 Oct | — | arena 883467b; msg 1230 |
| A6 termination of "fewest locks, never revisit a star" (Studio Job 11) | 3 | Studio | DONE 14 Oct: H survives, 0/361,293 walks fail (2nd impl agrees); no strictly decreasing measure ((lock,−moves) 99.87%; lateral dF 3→3 steps) | parked | msg 1300; 1bf16c16 |
| Lean certificates for all D-reducible 2-balls, ring ≤ 13 (+ estimate 14–15) (Studio Job 12) | 1, 2 | Studio | started 14 Oct | 7 Nov | `wheels/studio/` |
| B1 Lemma E review | — | sounding-board | parked | weekly review | `axioms/proof/R0-ATTEMPT-1.md` |
| D1/D2 paper drafts | 1, 2 | Long Table | outline only | 1 Dec | — |

## Gates

| Date | Gate | If it fails |
|---|---|---|
| 24 Oct | B8: discharging LP answer | Track 1 moves to 3-balls / larger sets; arena hunts the failing cases |
| 7 Nov | B3 loop invariant + Birkhoff 4-cycle reduction in Lean | paper narrows to checker + certified data |
| 14 Nov | arena hard-set benchmark + first A6 result | arena becomes falsification support only |
| 1 Dec | paper outlines frozen; no new lines | keep only evidenced claims |
| 20 Dec | everything reproduced from a clean checkout | ship what reproduces |

## Queue (next to start, in order)

1. B8 (running, MacBook). 2. Studio Job 12 = Lean certificates for 2-balls (running). 3. B7 on the Studio per B8's first read. 4. Track 2: B3 loop invariant.

## Parked ideas (look at weekly)

- Lemma E review (B1); A5 re-rank of LPC readings; A7 Fisk Δdeg vs Theorem W; B4 C-reducibility/Steinberger; new game skins.

## Waiting on Kyle

- Approve the scheduled check-in task (creation was blocked by the auto-mode classifier). Prompt and schedule: `coordinator-checkin-prompt.md`. Until then, check-ins happen when this session is active.

## Decision log (newest first; one line each, with reason)

- 2026-10-14 12:26 — A6 done: survives, no measure; parked (empirical termination does not give a proof route by itself). Studio given Job 12, Lean certificates for D-reducible 2-balls: needed for the paper regardless of B8, and keeps B7 heavy runs held.
- 2026-10-14 12:20 — Studio Job 10 done (hard set v1). Studio idle while B7 waits, so gave it A6 (heuristic termination on hard set + census 22–28): cheap, falsifiable, feeds Track 3's gate.
- 2026-10-14 12:20 — Scheduled check-ins (7 a day) could not be created: auto-mode classifier denied it. Did not work around; asked Kyle.

- 2026-10-14 12:15 — Took over coordination per Kyle's charter. Started B8 locally before more Studio 2-ball runs, because its answer decides whether ring 16 or 3-balls matter. Sent Studio the arena hard-set job (cheap, useful either way).
- 2026-10-14 12:15 — Skins (Gears, Shoreline, Respawn) confirmed live at 4square.studio (sw fth-v29 = local 83eb31f); no deploy pending.
