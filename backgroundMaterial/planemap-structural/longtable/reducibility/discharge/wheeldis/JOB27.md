# Job 27 (Studio): K = 2 plan for the 24 Oct gate [exploratory]

Pre-registration, written 2026-10-15 03:02 MDT before any run.

**Tasks (in order).**
- (a) `studio15/cfast --search --kmax 4` on the not-D equal-split overload configurations at a 7 (`out/eq_D7_dfast.out`
  D=false lines: 5,015 lines; the README table counts 4,980; the difference is to be reported). Inputs: `eq_D7_k2.txt`,
  `eq_D7_k3.txt.gz`. Report the D ∪ C share by number of free big vertices (count of `B` in the name) and by demand type.
- (b) dfast18 on the 10 untested ring 17–18 classes of "four lone senders at a 9" (`lone.py`, `pairs_D9_k4.txt`).
- (c) Lean (wheelcheck16/18 by ring size) on the lone-sender families: 59 at 7, 256 at 8, 524 at 9.

**H27.** With C added, every two-sender minimal overload at a 7 (demand types `1/b+1`) is D or C.
**Kill.** More than 5% of the two-sender overloads are neither D nor C. Then receiver-centred 2-balls are not enough at
d = 7, and the K = 2 plan moves to 3-balls or larger configurations at 7s.
**Caveat, fixed in advance.** A cfast hit is a C *candidate*: the contraction is checked for local admissibility (no loop;
Gonthier's sparse, size 1–4 and triad conditions), not for the global minimal-counterexample conditions. Contractions
that merge two ring vertices are flagged separately, as for the 565xxx wheels in Job 21. They count as C-candidates,
not certified.
**Cores.** studio14c (12), the ring-19 key (1) and the 2,855-key run (1) come first. Job 27 runs on the remaining cores at
nice 10.

## Interim result (2026-10-15 15:15 MDT)

**H27 is killed.** All 188 two-sender not-D overloads have been searched (|X| ≤ 4). Only 25 are C-candidates, and 163
are neither D nor C. Over all 687 two-sender minimal overloads: D 499, C 25, neither 163 (23.7%, against the 5% kill).
By type: 1/2+1 C 1, neither 23; 1/3+1 C 24, neither 84; 1/4+1 C 0, neither 48; 1/5+1 C 0, neither 8. So by the
pre-registered rule, receiver-centred 2-balls are not enough at d = 7. The K = 2 plan moves to 3-balls or larger
configurations at 7s.

(a), all types, 2,597 / 5,015 not-D lines tested: C 1,007, neither 1,590. The untested lines are three-sender types at
rings 13–14. By free big vertices (`B` count, C / neither / untested): 1: 1/23/0, 2: 32/113/41, 3: 222/270/515,
4: 449/544/1199, 5: 258/520/635, 6: 45/114/28, 7: 0/6/0. Full table: `job27/tally27.txt`.
C hits: 858 size-1 (one ring edge), 65 size-3, 108 size-4 with triads. The ring-vertex-merge check has **not** been run on the
hits yet, so all remain candidates.

(b) dfast18, 10 ring 17–18 classes of four lone senders at a 9: 4 / 10 done, all D=true (ring 17, about 15 min each).
(c) Lean wheelcheck16: 7 family 59/59 D; 8 family 212/256 D; 9 family 210/524 D; no failures. The runs were interrupted
by a session restart and resumed (`job27/restart.sh`).

## (a) stopped (2026-10-15 15:20 MDT)

Stopped on Long Table's instruction: the cloud upper-bound LP gives t* ≥ 24/227 > 0 even with all 5,015 not-D overloads
counted reducible (README §6.1), so the remaining three-sender verdicts cannot change the outcome. Final (a) coverage:
2,597 / 5,015 tested, 1,007 C-candidates (list = `C-REDUCIBLE` lines in `job27/part0?.cfast`, `k2?.cfast`), 1,590 neither.
The ring-merge check was not run. (b) and (c) continue at nice 20.
