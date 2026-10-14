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

Coordinator since 14 Oct 14:30 MDT: the cloud project thread (session_01AygaN3CzSnZpnynG8Tqb36, Claude project "Graph Colouring"). Mac check-ins keep running and follow this file; send Studio/agent results there with SendMessage too.

https://claude.ai/artifact/6qHXnnJhWsY9jX1WyyKRpG (source `status-page.html` here). Rewrite it, never append, whenever the board changes: where we stand, running now, the 5 most important recent results, gates, needs-you. Republish with `url` from other sessions (read it first).

## Deadline goals (≈ 27 Dec 2026)

1. Verified-checker paper (Track 2). 2. Combinatorics paper: curvature-organised unavoidable set / 2-ball reducibility
(Track 1). 3. Long shot: a full proof via Track 1.

## Board

| Item | Track | Owner | Status | Next gate | Evidence |
|---|---|---|---|---|---|
| B8 unavoidability of reducible 2-balls | 1 | Long Table agent | first report 14 Oct (ae42e4b5): H0 false (p25#2111); enlarged R (34,403 D-reducible keys, ring ≤ 14) hits all 80,125 census graphs; out-of-sample ≤32→33 misses 1/58,194; 146/154 constructed hit; LP infeasible with constructed graphs, certificate rests on b6666666676, b6666666667 (ring 16). Second agent finishing census-independent check | 24 Oct | `longtable/reducibility/discharge/` |
| B7 rings 15–18, LP-certificate configurations first (Studio Job 13) | 1 | Studio | step 1 DONE: both ring-16 certificate configs D-reducible, Lean-confirmed (wheelcheck16, all fields equal); step 2 (1,173 ring 15–16 keys, dfast18) running; 2 theorems to add | 24 Oct | msg 1305 |
| B8b lone-8 question + LP over the full K ≤ 1 sender list (census-independent) | 1 | Long Table agent (Mac) | interim 14 Oct (5d2c77ff): H8a killed, hemi8 (n=98) has 8 hard lone-8 senders and **no** degree-5 vertex with a D-reducible 2-ball (hemi9 likewise), so 5-centred D-reducible families are avoidable; K ≤ 1 LP infeasible, t* = 2/3 in both cases, weights forced; receiver-centred 8-balls 2,397/2,397 D-reducible so far (ring ≤ 15, run continuing); d ≥ 10 unbounded | 24 Oct | `discharge/` README §8 |
| C-checker (Studio Job 15) and **w66666 C-reducible (CANDIDATE)** | 1 | Studio + coordinator | cfast built, passes RSST cross-checks (caee2731); w66666 C-reducible with X={R0-I1,I2-I3,I3-I4,I4-I5}; independent Python Kempe closure = dfast exactly, all 171 3-colourings reached (abec3fca); sounding-board: admissibility fine, claim rests on closure. hemi C searches stopped (redundant) | Lean: Job 16 | `discharge/c66666/` |
| Lean certificate of w66666 C-reduction (Studio Job 16) | 1, 2 | Studio | top priority | asap | msg via SendMessage 14 Oct |
| Untested K = 1 sender 2-balls, 2,909 keys (Studio Job 14) | 1 | Studio | queued after Job 15 | 24 Oct | msg 1313 |
| B3 checker soundness (loop invariant, planar Kempe-matching step) | 2 | Long Table agent | not started | 7 Nov | `reducibility/dcheck/` |
| B2 Birkhoff separating 4/5-cycle reductions in Lean | 2 | Long Table agent | not started | 7 Nov | — |
| Arena hard set v1: 302 maps (150 census floor-tight, 50 glued, 2 R0, 100 non-reducible 66666 2-balls); max distance 2–3 | 3 | Studio | DONE 14 Oct | — | arena 883467b; msg 1230 |
| A6 termination of "fewest locks, never revisit a star" (Studio Job 11) | 3 | Studio | DONE 14 Oct: H survives, 0/361,293 walks fail (2nd impl agrees); no strictly decreasing measure ((lock,−moves) 99.87%; lateral dF 3→3 steps) | parked | msg 1300; 1bf16c16 |
| Lean certificates for D-reducible 2-balls (Studio Job 12) | 1, 2 | Studio | DONE 14 Oct: 1,693 native_decide theorems pass, 0 disagreements (all 1,440 ring 8–13; 40 ring 14–15 samples; 213 non-reducible samples); rings 14–15 full = 240 CPU-h, deferred until final R is fixed | — | msg 1350; af34f711 |
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

1. B8b (running, MacBook: H8e centred run). 2. Studio Job 13 step 2 (running). 3. Studio Job 16 (Lean: w66666 C-reduction). 4. B8b: LP re-run with R ∪ {66666 vertex}. 5. Studio Job 14 (K=1 untested). 5. Two ring-16 native_decide theorems. 6. Track 2: B3 loop invariant. Deferred: K ≤ 2 sender run (~330 CPU-h) until R's shape is settled; ring 14–15 full Lean (240 CPU-h).

## Parked ideas (look at weekly)

- Lemma E review (B1); A5 re-rank of LPC readings; A7 Fisk Δdeg vs Theorem W; B4 C-reducibility/Steinberger; new game skins.

## Waiting on Kyle

- Nothing.

## Decision log (newest first; one line each, with reason)

- 2026-10-14 15:20 — Job 15 found w66666 C-reducible (one ring–interior contract edge, triad I0). Sounding-board: no admissibility error; rests on the D-closure. Coordinator re-ran the closure independently (Python): identical to dfast, all 171 3-colourings reached. Treated as STRONG CANDIDATE: Job 16 (Lean certificate) top priority; hemi C searches stopped as redundant; B8b told to re-run its LP with every 66666 vertex in R. Kyle told (changes Track 1 if it holds). Literature: nothing found either way in one search.
- 2026-10-14 14:35 — Coordination moved to the cloud project thread at Kyle's request (same charter, same dashboard). B8b interim recorded: hemi8 shows 5-centred D-reducible R is avoidable, K ≤ 1 LP infeasible (t* = 2/3). Before committing Track 1 to receiver-centred R (unbounded in d), test the cheap rescue first: Studio Job 15 = C-reducibility of `b5666665686` (ring 15) and the hemi9 key, ahead of Job 14. K ≤ 2 run stays deferred. Not a deadline-goal change yet (goal 3 was already the long shot), so no alert to Kyle.

- 2026-10-14 14:10 — Ring-16 LP-certificate configurations Lean-confirmed (executable runs; native_decide theorems requested at low priority for the paper). Notified Kyle (certificate survived its kill test).
- 2026-10-14 13:55 — Job 12 done (0 Lean/dfast disagreements in 1,693). Deferred full ring 14–15 Lean (240 CPU-h): certify only the keys the final unavoidable R uses, after B8b; Studio time goes to Jobs 13–14.
- 2026-10-14 13:15 — B8 §7 (90d3235c): census-independent check reduces to a finite list of sender 2-balls (K=1: 22,428 keys, 2,909 untested; K≤2: 108,113 untested, ~330 CPU-h) plus a receiver DP. Started B8b locally (lone-8 question exactly; LP over the full K≤1 list) and queued Studio Job 14 (K=1 untested keys, ~4 CPU-h). K≤2 Studio run (~1–2 days) deferred until B8b says the K≤1 LP is close.
- 2026-10-14 13:20 — Job 13 step 1: both ring-16 LP-certificate configurations D-reducible by dfast (b6666666667 depth 3, b6666666676 depth 4, 1,793,614 classes each). Lean (DCheck16, matchTable range 8→9) running ~25 min each; certificate counts only after Lean. Job 12: 9 files pass so far.
- 2026-10-14 13:05 — B8 original agent had in fact finished (ae42e4b5); narrowed the resumed agent to the census-independent question only. Released B7 as Studio Job 13, two ring-16 certificate configurations first, because the LP certificate depends on them.
- 2026-10-14 12:50 — App restarted (Kyle updated it); B8 agent killed mid-run, its dfast jobs survived. Relaunched B8 to resume from its uncommitted files, with an explicit overfitting check (build family on orders 22–31, test on 32–33 and constructed witnesses), because 'covers the census' is near-circular if the family came from the census.
- 2026-10-14 12:50 — Kyle approved scheduled check-ins; task `fourcolour-coordinator-checkin` created (03,07,10,13,16,19,22 h). Pushes: morning digest, plus gate results / marker moves / needs-Kyle only. Dashboard v2 (flowchart with current position) published.
- 2026-10-14 12:26 — A6 done: survives, no measure; parked (empirical termination does not give a proof route by itself). Studio given Job 12, Lean certificates for D-reducible 2-balls: needed for the paper regardless of B8, and keeps B7 heavy runs held.
- 2026-10-14 12:20 — Studio Job 10 done (hard set v1). Studio idle while B7 waits, so gave it A6 (heuristic termination on hard set + census 22–28): cheap, falsifiable, feeds Track 3's gate.
- 2026-10-14 12:20 — Scheduled check-ins (7 a day) could not be created: auto-mode classifier denied it. Did not work around; asked Kyle.

- 2026-10-14 12:15 — Took over coordination per Kyle's charter. Started B8 locally before more Studio 2-ball runs, because its answer decides whether ring 16 or 3-balls matter. Sent Studio the arena hard-set job (cheap, useful either way).
- 2026-10-14 12:15 — Skins (Gears, Shoreline, Respawn) confirmed live at 4square.studio (sw fth-v29 = local 83eb31f); no deploy pending.
