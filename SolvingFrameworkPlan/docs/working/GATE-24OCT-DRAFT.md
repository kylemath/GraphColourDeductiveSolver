# 24 Oct gate (B8, discharging LP answer): DRAFT, 18 Oct 2026

Draft kept by the coordinator and revised as results land. Tags: **[L]** proved in Lean, **[E2]** two independent
engines agree, **[E]** one engine, **[I]** inferred. Evidence paths are relative to `longtable/reducibility/discharge/`.

## Answer in one paragraph

**K ≤ 1 (at most one big vertex in the configuration): closed.** Every discharging sender with one big
neighbour is in the reducible set R, so the forbidden-pattern LP has t* ≤ 0 on that case. This rests on Lean for 46
of the 47 large keys and two independent engines for the last one. Lean on that key finishes 22–25 Oct. **K = 2: open.**
The best LP bound is t* = 7/27 ≈ 0.259 (need ≤ 0). It did not move when big–big charge-sharing was added. The
remaining binders are a small set of degree-7 receiver patterns whose kills lie beyond ring 16.

## K ≤ 1 evidence

| Piece | Status | Where |
|---|---|---|
| K=1 sender keys at rings ≤ 16: 2,848 non-66666 keys all D; 5 others 66666-centred, covered by w66666 | [E] dfast; Lean for the 2,855-key Studio-D set (Job 24b) | `studio14/`, `dcheck/occ24/results24b.txt` |
| 47 deferred keys at rings 17–19 | 46 [L] (3 early + studio14c 43/43, d627087b); k19 (ring 19, 48.4M classes) [E2]: dfast18 and kc agree on classes 48,427,561, ext 3,909,279, D, depth 4 | `studio14b/`, `wheeldis/loop/kc/` |
| kc validation (independent of dfast; no dfast, cfast or Lean source read) | 101 keys at rings 10–17 (82 not-D) + ring-18 D, all fields equal | `wheeldis/loop/kc/FINDINGS.md` |
| w66666 C-reducible | [L] (C66666.lean) + Coq/Gonthier independent | `c66666/`, `dcheck/C66666.lean` |
| Checker soundness, r ≤ 19 | [L] Jobs 19 and 23 | `dcheck/JOB19.md`, `dcheck/JOB23.md` |
| Per-key Occ modules (49) | [L] Job 24, hD closes as keys land | `dcheck/occ24/` |

**Scope caveat.** A 2-ball's ring can fold in large maps. Until Job 26 proves Kempe matching for a face-boundary-walk
ring, the K ≤ 1 claim covers appearances with a simple ring. Job 26 has proved FaceGlue (i) and Kempe matching for any face walk with distinct darts, so any number of pinches
and folds (FaceWalk.ringTNC/kempeMatching, 758a293b; sabotage test rejects). Only (iii) is left: extracting the face walk
from an appearing 2-ball and wiring it into colorable_of_occ_dred. It has a 20 Nov kill, and the fallback is to state the simple-ring hypothesis in the paper. The Track 1 hand
argument (B2 + no separating triangle ⇒ injective, induced embedding) closes the gap on paper. Its Lean is Job 26 step 3a.

## K = 2 evidence

| Step | t* | Note |
|---|---|---|
| Job 28 rounds 1–12 | 5/17 → 13/49 | loop: find patch, kill with B-fixed D/C at ring ≤ 16 |
| Round 13 (+ win14, win8, win89) | 7/27 | binder d=7 5675765/6577575 |
| Job 29 L2: oriented big–big transfers, full registry (16,411 patterns) | 7/27 exactly [E] | upper bound by an exhaustive separation of the x=0 solution; lower bound by row generation (feascheck.py). Charge-sharing adds nothing on this pattern set |
| Explore rounds 24–32 | (restricted-LP values were under-separated; superseded) | ~30 binding rows forbidden; all windows second-engined |

What blocks K = 2 [E]: one row. The 7/27 certificate is a single receiver row R = d7 5675765/6577575, whose
fives are of sender types 55667, 55767 and 77777. With the sender rows forcing Σy ≥ 1 − t, row R gives
1.7(1 − t) ≤ 1 + t, so t ≥ 7/27 exactly (dual weights 10/27, 10/27, 5/27, 2/27; EXPLORE-LOG 08:50Z, 98d63411).
So only a kill of R itself, or of one of its three sender types, can move the LP. Transfers can't move it
either: R fits as its own 7-neighbour (self-pairing, rounds 12 and 20). R's three B-fixed windows (rings 16–17)
are not D [E2: kc and dfast18 agree on every count]. The certificate breaks only if all 25 (s1, s4) fillings of R die:
9 (a 5 at s1 or s4) are dead by ring-13 D on both engines, and 16 remain (loop/k34/fill.txt). A C verdict on R's ring-16/17
windows would cover all 16. kc -C (independent, matches cfast on 163 configs: 30/30 C, 133/133 not C) and Studio's
cfast are both running on them.

## Options for K = 2 after the gate

- **A. Ring 17–18 windows at the binders.** These were dead on cost (dfast18: 60–70 min per ring-18 D). kc does ring 18
  in about 5 minutes, so this is cheap now. Running overnight 18 Oct (explore round 34). Claims still need dfast18.
- **D. Defect-style search at each surviving binder** (round 18's method). It asks whether the row can occur near a
  minimal counterexample at all. Cost: per-row, capped.
- **E. Change the rule class** (Opus team, 18 Oct): send charge through 6s, which could void R's certificate
  without killing R. Ceiling on what Rule T can buy: t ≥ 11/71 ≈ 0.155 for the whole Rule T class (Opus, H_floor_check), lifted only by killing one of four named arrangements or an L2 transfer out of w2/w4. Also: RSST's 249 D configurations, already Lean-checked, remove every known K ≤ 4 defect but not R. H7's 1/21 floor is specific to its LP solution: its defect D3 contains RSST #110, D on two engines (explore 4b12ef00).
- **C. Narrow.** State K = 2 as open with the evidence above. Track 1's paper becomes "K ≤ 1 closed by 2-ball
  reducibility; K = 2 obstructed by self-pairing", and the long shot moves to 3-balls.

## Open items before 24 Oct (to fill in)

- [ ] run29d: 7/27 binders and the xcap=1000 cap test (Studio).
- [ ] Explore round 34+: ring 17–18 kc sweep on binders; any re-solved t*.
- [ ] k19 Lean (22–25 Oct): upgrade [E2] → [L] if it lands.
- [x] Job 26 status (18 Oct 09:05Z): multi-pinch proved; only (iii) left.
- [ ] Recommendation line, once A has run.
