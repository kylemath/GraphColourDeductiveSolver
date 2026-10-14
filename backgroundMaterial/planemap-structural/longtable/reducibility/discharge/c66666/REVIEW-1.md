# Sounding-board review 1 of the w66666 C-reduction (Long Table, Mac, 14 Oct 2026) [exploratory]

**Verdict: GO WITH CHANGES.** Build on it, labelled "certified modulo DCheckSound S1/S3" until that gap is closed or the
reduction has been re-checked in an independently verified checker.

- **Contraction validity: OK.**
  - No loops: the merged sets {R0, I1} and {I2..I5} contain only the X edges, since I2I4, I2I5 and I3I5 are not edges.
  - Ring vertices are distinct in G: R_a = R_b would give a 4-cycle I0–Ij–R–Ik that separates G, which internal
    6-connectivity forbids. Add this argument to README.md.
  - Chords between ring vertices are harmless.
- **The checked condition is the true C-condition.** In `extCAux`, I1 takes R0's colour, and the merged vertex M avoids
  R1..R9 and I1, so the extendable set is exactly the ≤3-colour ring colourings (`extX_iff_three`). `extX_reached`
  proves that set is contained in the reached set.
- **Heesch obstructions do not apply** (each Ij has 3 ring neighbours).
- **Strongest objection:** dfast, the Python check and Lean all share the same chain/matching abstraction, so they agree
  by construction. Mitigation already on record: the same abstraction reproduces RSST's extendable counts and D
  verdicts on all 633 configurations, including 384 "no" verdicts. So it matches the classical Birkhoff–Heesch model,
  and the open risk is the formalisation (S1/S3), not the mathematics.
- **Scratch test (weak):** real Kempe classes over 190 random small outsides found 0 failures. The control also found 0,
  so the test has no power.
- **Decisive independent test:** encode w66666 with X in Gonthier's verified Coq checker (`fourcolor` library). Kill
  criterion: Coq rejects the contract or the closure. Coq/opam is not installed on the Mac (checked 14 Oct), and
  installing it needs Kyle's go-ahead (a download).
