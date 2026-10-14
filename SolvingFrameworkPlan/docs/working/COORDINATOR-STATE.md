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
| Arena hard set (failing 2-balls, floor-tight glued, R0 maps) | 3 | Studio | queued | 14 Nov | `GraphColourRLArena` |
| A6 termination of "fewest locks, never revisit a star" | 3 | arena | not started | 14 Nov | — |
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

1. B8 (running). 2. Studio: arena hard-set build (light), then B7 per B8's first read. 3. Track 2: B3 loop invariant.

## Parked ideas (look at weekly)

- Lemma E review (B1); A5 re-rank of LPC readings; A7 Fisk Δdeg vs Theorem W; B4 C-reducibility/Steinberger; new game skins.

## Waiting on Kyle

- Nothing.

## Decision log (newest first; one line each, with reason)

- 2026-10-14 12:15 — Took over coordination per Kyle's charter. Started B8 locally before more Studio 2-ball runs, because its answer decides whether ring 16 or 3-balls matter. Sent Studio the arena hard-set job (cheap, useful either way).
- 2026-10-14 12:15 — Skins (Gears, Shoreline, Respawn) confirmed live at 4square.studio (sw fth-v29 = local 83eb31f); no deploy pending.
