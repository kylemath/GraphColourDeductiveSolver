# Job 20 pre-registration (Studio, written 2026-10-14 23:41 MDT, before Coq is installed)

**What.** Install Coq/Rocq with opam at the version that math-comp/fourcolor (Gonthier's Coq proof) builds against,
build fourcolor, and run its own reducibility checker on the 66666 wheel w66666 with the contract
X = {R0-I1, I2-I3, I3-I4, I4-I5}, triad I0 (README.md here; dcheck/C66666.lean).

**H20.** fourcolor's checker agrees with ours:
1. the D-closure (Kempe closure of ring colourings) of w66666 alone does not reach every ring colouring
   (ours: 2,461 classes, 530 extendable, 1,241 reached at depth 15, so w66666 is not D-reducible); and
2. with the contract X, fourcolor's `valid_contract` accepts X and its C-reducibility check succeeds.

**Kill / disagreement criteria** (any one is reported as a disagreement with our checkers, with the exact output):
- fourcolor's closure numbers (or its D-reducibility verdict) differ from 2,461 / 530 / 1,241;
- fourcolor's checker says X does not make w66666 C-reducible although valid_contract accepts X.

**Possible outcome that is not a disagreement but is still a result:** fourcolor's `valid_contract` rejects X, or X
cannot be written in its configuration syntax, because X contains a ring–interior edge (R0-I1). That would match the
README's note that RSST's contract may not allow such edges. It would mean the w66666 C-reduction rests on our own
contract-validity argument (README steps 1–2), not on Gonthier's.

**Run limits.** opam and the build at nice 15 with at most 2 jobs, so they don't slow the studio14c Lean workers.
AC power checked first.
