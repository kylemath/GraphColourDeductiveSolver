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
| B7 rings 15–18, LP-certificate configurations first (Studio Job 13) | 1 | Studio | DONE for rings 15–16 (379cb8e9): ring 15 616 D / 65 not, ring 16 450 D / 42 not; Lean validation 15/20 identical, 5 running. Rings 17–18 and the two ring-16 theorems DROPPED: 66666-hole 2-balls are subsumed by w66666 | — | `discharge/studio13/` |
| B8b / Job 18: K ≤ 1 discharging LP with R ∪ 66666 | 1 | Studio | DONE 14 Oct (652e3c2e, README §9): hemi8 obstruction gone; untested-excluded case has 0 non-R K=1 senders (H18b survives); worst case hinges only on 47 deferred ring 17–19 keys (now being tested). K ≤ 2: 107,279 non-66666 untested keys (~330 CPU-h at ring ≤ 16) HELD until Job 17 + the 47 keys | 24 Oct | `discharge/` README §9 |
| C-checker (Studio Job 15) and **w66666 C-reducible (CANDIDATE)** | 1 | Studio + coordinator | cfast built, passes RSST cross-checks (caee2731); w66666 C-reducible with X={R0-I1,I2-I3,I3-I4,I4-I5}; independent Python Kempe closure = dfast exactly, all 171 3-colourings reached (abec3fca); sounding-board: admissibility fine, claim rests on closure. hemi C searches stopped (redundant) | Lean: Job 16 | `discharge/c66666/` |
| Lean certificate of w66666 C-reduction (Studio Job 16) | 1, 2 | Studio | DONE 14 Oct (173355bc, dcheck/C66666.lean): run numbers, every ≤3-colour ring colouring reached, extension after X ⇔ ≤3 colours, all native_decide, standard axioms. Written no-loop argument. Gonthier valid_contract allows ring–interior contract edges (RSST 2.126 uses 4). Trust gap = DCheckSound S1/S3 (shared by every reducibility claim) + Birkhoff ring distinctness | — | `dcheck/C66666.lean` |
| Untested K = 1 sender 2-balls (Studio Job 14) | 1 | Studio | DONE 14 Oct (4a237905): all 2,848 non-66666 K=1 keys at rings ≤ 16 D-reducible; 5 non-D are 66666-centred (covered by w66666). 47 keys at rings 17–19 deferred. Lean sample running | 24 Oct | msg 1313 |
| Independent Coq/Gonthier check of w66666 (Studio Job 20) | 1, 2 | Studio | waiting on Kyle (Coq install) | — | — |
| C-reducibility census of wheels, deg-5 links {5..8}^5, deg-6 links {5..7}^6 (Studio Job 17) | 1 | Studio | queued after Job 14; H17: every 5-wheel with link degrees ≤ 6 is D or C | 24 Oct | `discharge/studio17/` |
| B3 checker soundness = DCheckSound S1/S3 | 2 | Long Table agent → Studio Job 19 | S1 PROVED, no sorry (c364be83; propext, Classical.choice, Quot.sound); S3(i) nc_matching, S3(ii) flip_chains_proper proved; R1 matchTable complete (b506b96e; native_decide p=4..8). Remaining: R2 project-level glue (ConfigOcc), Studio Job 19 | 7 Nov | `dcheck/README.md` |
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

1. B8b (running, MacBook: H8e centred run). 2. Studio Job 13 step 2 (running). 3. B3 (DCheckSound S1 loop invariant, S3 Kempe-matching) on the Mac. 4. B8b: LP re-run with R ∪ {66666 vertex}. 5. Studio Job 14 (K=1 untested). 5. Two ring-16 native_decide theorems. 6. Track 2: B3 loop invariant. Deferred: K ≤ 2 sender run (~330 CPU-h) until R's shape is settled; ring 14–15 full Lean (240 CPU-h).

## Parked ideas (look at weekly)

- Lemma E review (B1); A5 re-rank of LPC readings; A7 Fisk Δdeg vs Theorem W; B4 C-reducibility/Steinberger; new game skins.

## Waiting on Kyle

- Coq install on the Studio machine for Job 20 (asked 14 Oct 16:30 in the project thread).

## Decision log (newest first; one line each, with reason)

- 2026-10-14 16:30 — Job 18 done: K ≤ 1 LP obstruction removed; only 47 deferred keys left. Ordered them run after Job 17 (cheap, decides K ≤ 1 completely). K ≤ 2 (330 CPU-h) held until Job 17 says how many senders wheels remove. Coq install treated as Kyle's call (Studio's view, agreed): asked once in the thread.
- 2026-10-14 16:30 — Old Mac coordinator session archived (21:44Z), so its local agents ended. B3 had already closed S1 and R1 (three weeks ahead of the 7 Nov gate). Moved the remaining local work to Studio: Job 18 (B8b LP re-run), Job 19 (B3 R2, needs Studio's Mathlib build), Job 20 (Gonthier/Coq cross-check of w66666, Coq install on Studio's machine; the archived session had asked Kyle, no answer; reversible local install inside the charter's compute remit).
- 2026-10-14 16:25 — Job 14 done: every K=1 sender at rings ≤ 16 is in R (D, or 66666 via w66666). Passed to B8b for the LP re-run (with/without the 47 deferred ring 17–19 keys), then K ≤ 2.
- 2026-10-14 15:55 — Job 17 control fix: Franklin's 666666 6-wheel is NOT C-reducible by contraction ≤ 6 (Studio); arXiv 2603.24880 says Franklin's reduction identifies ring vertices and the wheel is not D-reducible, so consistent. Controls = RSST 2.126, 122.126 (C) and 66667 (neither). Same paper does not claim w66666 reducible alone (Lemma 8.2 uses a larger configuration), so Job 16 is not a rediscovery of it; Franklin 1922 unchecked (open literature item). 47 K=1 keys at rings 17–19 deferred (need DCheck18; only if final R needs them).
- 2026-10-14 15:50 — Job 13 rings 15–16 done. Dropped B7 rings 17–18 (~55 CPU-h) and the two ring-16 theorems: all 66666-hole 2-balls are subsumed by the w66666 C-reduction. Job 14 now skips 66666-centred keys. Queued Job 17 (C-census of 5- and 6-wheels): if wheels alone are C-reducible, the unavoidable set shrinks to wheels and B8 becomes a much smaller discharging problem.
- 2026-10-14 15:10 — Job 16 done: w66666 C-reduction certified in Lean modulo DCheckSound S1/S3 + Birkhoff distinctness. Status: RESULT at the programme's standard (second engine + Lean), not yet a theorem. Literature: arXiv 2603.24880 (Lemma 8.2) handles the 66666 case with a larger configuration, and notes Franklin's 666666 is C- not D-reducible; no claim that w66666 is irreducible found. Started B3 on the Mac (light Lean work): S1/S3 are now the main trust gap. Arena hard set's 100 '66666 2-balls' stay valid as D-hard instances.
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
