# Chain-parity note (draft, 8 Oct 2026)

This is a short standalone note: *Kempe chains around a degree-five vertex: a mod-4 chain count and a parity law*. The working title was "A parity law for Kempe chains at a degree-five vertex".
- It is separate from the VH∃ record (`../VHE-paper/`), following the coordinator's paper decision of 8 Oct (`docs/working/CoordinatorPlan.md`, "Paused").
- Author: Kyle Mathewson, as in the VH∃ paper.
- Not committed. Not posted anywhere.

## Files and build

- `main.tex` is self-contained, with an inline bibliography. There is no `references.bib`.
- Build: run `pdflatex -halt-on-error main.tex` twice. Last build: 9 pages, exit 0 on both passes, no undefined references, no overfull boxes.
  - The build was done in a scratch directory; no PDF is kept here.
  - Packages used: amsmath, amssymb, amsthm, url, microtype, hyperref, geometry, enumitem.

## Label policy used

- Only results that are compiled in Lean **and** covered by audit J14 (`docs/working/Audit-2026-10-08`) are called Theorem, Proposition or Corollary.
- Everything else carries a label from the VH∃ convention: [hand], [computed], [cited] or [open].
- Every `\lean{…}` name in `main.tex` was checked by grep against `docs/working/StudioMathLean/Mathlib/Combinatorics/SimpleGraph/PlaneMap/*.lean`, or against the base library (`SphericalMap`, `Fills`, `Triangulated`).
- `SHA256SUMS` checks out 40/40. The five module hashes quoted in §6 match the audit's table.

## TODO before this goes anywhere

### Kyle's decisions

1. **Disclosure (§7).** The text is the VH∃ disclosure section copied verbatim (`../VHE-paper/main.tex`, lines 21–54) as a placeholder. A LaTeX comment marks it for Kyle's approval. It still says:
   - "this paper";
   - "the Navigator's ledger";
   - "`AUTHOR-RECORD.md` beside this paper".

   It also describes session roles that did not all touch this note. Kyle must approve it or adapt it. The tag-name placeholder must also be set.
2. **Title.** Choose between the proposed title and the working title.
3. **Where to post, and whether to cite the VH∃ draft.** Reference [13] points to a draft inside the repository.

### Claims to verify: new or unreviewed hand arguments written for this note

4. **Lemma W, hand proof (§4.3).** This is a new derivation. It fills the pentagon (T°) and uses "a Kempe exchange preserves cw mod 4 on a closed triangulation" (the last sentence of Lemma 12, which comes from Fisk degree parity).
   - Lean proves W differently, by a dart sum. The statement is compiled; only this proof is unreviewed.
   - Ask for an independent review.
5. **Proposition 2 (Kempe duality), proof of the converse direction (§4.1).** The argument, which contracts `Q ∪ {v}` and reads off the rotation walk, was written for this note. The statement is compiled.
   - Ask a reviewer to check the claim "consecutive neighbours of u are equal or adjacent" for multigraph contractions.
6. **Lemma 10 (Tutte's identity).** This is a primal Euler proof: faces of T_XY correspond to ZW-chains. `TrackK/FProof.md` uses the dual-region proof instead. It is standard, but not reviewed in this form.
7. **Genus residue `2G mod 4` (§5).** It is hand only (`TrackK/FProof.md` §5) and was not part of the TrackK review.
   - It is checked only on the torus (2,192 hole states; G = 0/1/2 on 340/1,137/715).
   - Genus ≥ 2 is unchecked.
   - The claim "G_i ∈ {0,1} on the torus" is from FProof and is not separately checked.
8. **Matching form (§5).** The following are [hand, unreviewed] (TrackS S1–S4, TrackT §5):
   - "a state is determined by M_t";
   - "N = 7 + k(M_{t−1} ∪ M_t)";
   - "every near-rigid cycle yields such a sequence" (via TrackJ J5 and TrackS S3).
9. **The n = 22 example (TrackU).** It exists only in matching form, on an abstract non-planar graph, and is not a surface triangulation.
   - TrackU notes an unresolved discrepancy: off the sphere, a matching-form cycle need not correspond to a π-cycle. This does not affect the note's use, but should be resolved before anyone relies on the matching form off the sphere.
   - Confirm that the edge list in `TrackU/README.md` §0 is the one meant (`out/t1_n22_first.txt`).

### Claims to verify: numbers, with their sources

10. Check each figure against its source file:

| figure in the note | source |
|---|---|
| 111,912 of 281,230 link-free moves | `TrackI/RigidIsolation.md` (Remark 7 note) |
| 21,968,170 unfilled states (Theorem P off the sphere) | `TrackF/LockParity.md` §4 |
| 1,664,226 / 3,862,132 duality violations on the torus | `TrackF/LockParity.md` §4 |
| torus residue 2G: 2,192 states; 340/1,137/715 | `TrackK/FProof.md` §4 table and §5 |
| law fails at 282/544 torus π-steps | `TrackC/README.md` §6.4 |
| rigid→rigid off the sphere: 23/2,467, 1/1,401, 29/5,205; 53 rechecked | `TrackH-review/README.md` |
| 611/1,261 (48%) under non-planar orders; 0/256 planar | `TrackT/README.md` §4 |
| n = 22, length 10, word 1212121212, 2 engines; none at n = 20 | `TrackU/README.md` |
| near-rigid run 8 at order 33; census 22–33 | `../VHE-paper/main.tex` §6; `Census33/README.md` |
| N(c) = N(πc) = 12 at the 22-vertex DL witness | audit J14 §2 row 9 (script `chains.py`, not Lean) |

11. **Literature check, not redone for this note.**
    - Confirm the bibliographic details of Tutte (1969) and Fisk (1977).
    - Confirm the journal status of Mohar–Singer.
    - Confirm that Theorems 1 and 3 there are what Lemma 12 cites.
    - FProof §6 found no prior statement of the hole formula F or of the law. A proper search is needed before submission. Candidates: Fisk's later papers, Mohar's "Kempe equivalence of colorings", the literature on Tilley's D-resolvability.
12. **Tilley.** Check the claim that LPC at every degree-5 vertex "is, as far as we can tell", D-resolvability. The VH∃ paper says the full-text definition check by audit is pending.

### Lean follow-ups (optional)

13. Write a frozen challenge file and bridge for `ConjectureF` / `ChainParityLaw`. None exists, and the note says so.
14. Write a two-line Lean corollary "no Kempe class consists only of rigid states" (audit W2). It is labelled [hand] in the note.
15. Optionally drop the no-isolated-vertex hypothesis from the law and rigid-isolation corollaries (TrackC §9.4).
16. Rigid states are not exhibited in Lean, so the hypothesis of `rigid_isolation` is shown satisfiable only through its `DoublyLocked` part. The note says this.

## Sanity check run while writing

The note fixes these conventions:
- the link is labelled along the face orientation;
- η is read from (α+β, α+γ, α+δ);
- the fill faces and their cw status are as in the proof of Theorem 5 and Lemma W.

Two independent scripts were written in the session scratchpad; they are not in the repository.
- A table check: T1, the fill-face statuses for c and for πc, and η(πc) = η(c). Result: 0 mismatches.
- Random sphere triangulations, n = 10–30, with Kempe walks: 27,046 unfilled states, 7,417 of them doubly locked. There were 0 failures of:
  - F;
  - Lemma W at π;
  - Kempe duality;
  - L1(πc) = 1;
  - the law.
