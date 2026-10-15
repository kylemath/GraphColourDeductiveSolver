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

## Result (15 Oct 2026; Coq 8.20.1, mathcomp 2.5.0, coq-fourcolor 1.4.3 via opam; `fourcolor_w66666.v` → `.out`)

**H20 survives. fourcolor agrees with our checkers on every number.**

| quantity | fourcolor | ours (dfast / kempe66666.py / C66666.lean) |
|---|---|---|
| ring size, kernel edges | 10, 25 | 10, 25 (5 spokes + 5 rim + 15 kernel–ring) |
| normalised ring traces | 7,383 | 2,461 classes (× 3) |
| traces not in the Kempe co-closure | 3,660 (so not D-reducible) | 2,461 − 1,241 = 1,220 (× 3) |
| contract traces for X | 513 | 171 three-colourings (× 3) |
| X accepted (`cfctr` Some, `valid_ctrm`, incl. triad) | true, true | triad I0 |
| `check_reducible` | **true** | C-reducible |

- The factor 3 is fourcolor's trace normalisation against our colouring classes. It is the same factor on all three counts.
- `Lemma w66666_Creducible : cfreducible cfW` is proved by `vm_compute` and `check_reducible_valid`. That is, `C_reducible (cfring cfW) (cfcontract cfW)`: X is a valid contract and every contract trace is in the Kempe co-closure. `Print Assumptions` reports **"Closed under the global context"**, so it uses no axioms.
- Control: fourcolor's configuration 1 (Birkhoff diamond, ring 6) gives `check_reducible = true`.
- **The ring–interior edge is admissible.** fourcolor's `valid_contract` only requires the contract to be disjoint from the ring darts, sparse, of size 1–4, and to have a triad at size 4. The edge R0-I1 is a kernel edge (not a perimeter dart), so this is not the reason w66666 is absent from RSST's list.
- The encoding was found with `cfprog.py`, a Python transcription of cfmap.v that reproduces configurations 1, 2 and 4: program `H 1 H 3 H 1 H 3 H 1 Y 1 H 2 Y 1 Y Y 1 Y Y Y Y`, contract indices 0, 20, 11, 23.
  - Coq confirms the ring size 10 and the 25 kernel edges.
  - The kernel arities [5,6,6,6,6,6] and the wheel adjacency were checked in Python only. Evaluating face orbits under `vm_compute` is too slow.
- What this does and doesn't cover:
  - It certifies w66666 in Gonthier's C_reducible sense, which is the same notion his 633 configurations use.
  - Turning this into "w66666 cannot occur in a minimal counterexample" still needs his embedding argument (`embed.v`), which is stated for `the_configs`. The steps 1–2 argument in README.md plays that role here.
