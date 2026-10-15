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
