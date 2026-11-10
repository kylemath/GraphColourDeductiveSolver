# W6b round 9 (RSST-NONE): why our engines reject RSST's 51 "none" configurations

(Saved by the lead from W6b's hand-back text, 10 Nov 2026 ~10:30Z. Full write-up in ADMISSIBILITY.md cf3aa0f0; MD5SUMS f5b231f7, this REPORT.md not in it.)

**Answer.** All 51 have one cause, which is admissibility and not reducibility.
- RSST's own contraction set X puts 2 or 3 ring vertices in one X-component.
- kc -C (conservative) allows at most one ring vertex per component, and so does Lean `admissibleX` (CGlue.lean:375).
- Round 44 needed a conservative X, so all 51 became "none". The colouring check never fails.

**Engines with RSST's own X:**
- kc_rn (W6b's diagnostic build of kc.cpp f9da2a70): -B (broad check on a fixed X) and -F (no-loop-in-configuration only) both give leftover 0 on 51/51.
- cfast --fixed (e319f040): C-REDUCIBLE, leftover 0, 51/51, with and without --nogonthier.
- The stock kc binary (49393b29) with -x refuses all 51 with adm=no ("two ring vertices in one component").
- Round 44's own -C2 search had closed only 22 of the 51.

**The 4 in W6r's 33-configuration cover:**

| RSST | kc id | X | merged pair |
|---|---|---|---|
| 2.126 | rsst003_2o126 | {R0-I0,R2-I0,R4-I2,R6-I2} | R0, R2 |
| 3.1324817 | rsst061_3o1324817 | {R0-I4,R6-I3,R8-I3,R10-I4} | R6, R8 |
| 128.1324802 | rsst065_128o1324802 | {R0-I5,R6-I4,R8-I4,R10-I5} | R6, R8 |
| 124.1324817 | rsst202_124o1324817 | {R0-I5,R8-I4,R10-I4,R12-I5} | R8, R10 |

Leftover 0 out of 154, 11,189, 12,492 and 133,573 bad classes.

**Independent checks (W6b's own script):**
- The Gonthier local conditions hold on all 51.
- There are 94 merged ring pairs. Each one's X-path runs through interior vertices only, is at most 3 edges long, and joins two ring vertices that are not adjacent on the ring.
- X read straight from unavoidable.conf matches rsst_x.txt 51/51, and RSST's header counts match our engines 51/51.

**Soundness of the relaxation:**
- Contracting can create a loop only through an outside chord that joins two merged ring vertices.
- That chord plus the X-path (length at most 3) is a separating cycle of length at most 4.
- Birkhoff's lemma (`MinimalCounterexample.noShortSep`) excludes such cycles.
- Equal colours for merged vertices are already enforced by cfast ringEq and Lean extCAux.

**Lean needs:**
- relax the last conjunct of `admissibleX`;
- a C4b case for an outside edge;
- a cycCertB-style certificate plus a soundness lemma (at l = 2 it needs a ring–interior crossing edge, which cycCertB lacks);
- a review of `foldSafeX` with shared labels.

The 3 held registry ring-merge entries fall under the same lemma.

**Not verified:**
- the RSST paper text and fourcolor `valid_contract`;
- a fourcolor run on the 51;
- folded rings;
- whether `Cyc`/`apex_sides` accept an outside edge;
- the Lean effort.

## RSST-NONE2 (W6b, 10 Nov ~10:56Z; the lead saved it from the hand-back)

**All 51 RSST X's satisfy Gonthier's `valid_contract` (coloring.v:462) as defined:**
- off-ring 51/51;
- sparse 51/51;
- size 1..4 51/51 (37 of size 4, 14 of size 3);
- a triad in the kernel for 37/37 of the size-4 X's.

**How it was checked.**
- `code/vc_check.py` builds Gonthier's configuration map from unavoidable.conf as the cubic dual of the free completion. The map is checked for the hypermap axioms and genus 0.
- The conjuncts are then evaluated as the source defines them. The result agrees with analyse_x.py on 51/51.
- Sanity check: all 384 RSST C contracts are valid.
- Per-config results are in results/vc_none51.tsv (92690dbc) and vc_all633.tsv (8ba1a9df).

**Our Lean `admissibleX` and `valid_contract`: neither implies the other.**
- `admissibleX` is stronger on two points:
  - distinct ring labels per component, the only failure for all 51 and for 77 of the 384;
  - local loop-freeness.
- It is weaker in one: it has no triad condition at |X| = 4.

**Lean port.**
- Needed:
  - a decidable validContract;
  - ports of contract_ring, sparse_contract_ring, contract3_valid and triad_valid (contract.v:46-247), on our `NoShortSepCycle` (ClaimGlue.lean:64, lengths 3–5, two on each side at 5);
  - a lift through ConfigOccW, as in embed_valid_contract.
- Not needed: contract_coloring's induction, because C4a already contracts. hC is unchanged.
- Under this route the two soft spots in the chord argument become moot.

**Definitions.** The lead fetched hypermap.v and geometry.v at 10:58Z, and they confirm W6b's readings:
- insertE (geometry.v:777) holds both darts of each edge;
- kernel (geometry.v:182) is the complement of the ring's face band;
- adj (geometry.v:713) means some dart of x's face has its edge in y's face.

**Not verified:**
- the length-5 "two on each side" match with Gonthier;
- triads for the registry's 4-edge entries;
- any Lean.
