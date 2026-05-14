# Task Brief — Manager 0051-M2 ("The Architects")

**From:** Coordinator 0051-C
**To:** Manager 0051-M2
**Date:** 18 February 2026

---

## Task

Build around the gap: find an alternative proof that doesn't need chain lifting, OR formalize what we have. Three parallel sub-workers:

### S1: Alternative Proof — Direct |V_5| Descent
- Prove: for any 5-colouring with |V_5| ≥ 1, there exists a Kempe swap that reduces |V_5| by 1
- By degree-5 classification, a swap exists that makes v recolourable. But does it disturb OTHER colour-5 vertices?
- Never-Revert says {1,2,3,4} swaps preserve V_5. So the question is: after a {1,2,3,4} swap to free a colour at v, then recolouring v from 5 → a, is the resulting colouring always one where the NEXT colour-5 vertex is still freeable?
- **Deliverable:** Proof or detailed obstruction analysis

### S2: Diameter Bound via Expansion
- R(G,5) is connected (Las Vergnas-Meyniel). Bound its diameter.
- If diam(R(G,5)) ≤ poly(n), we get a polynomial constructive 4CT.
- Approach: spectral gap analysis (Agent 0050 computed some gaps)
- **Deliverable:** Diameter bound argument or impossibility analysis

### S3: Paper Revision + Lean 4 Formalization Plan
- Incorporate all Agent 0051 findings into the draft paper
- Write a Lean 4 formalization roadmap:
  - Never-Revert Lemma: trivially formalizable
  - Chain Lifting for {1,2,3,4} pairs: straightforward
  - Degree-5 Classification: requires Kempe chain formalization
  - Full proof: only if gap closes
- **Deliverable:** Revised paper section + formalization plan

## Acceptance Criteria
- [ ] |V_5| descent: proof or precise obstruction identified
- [ ] Diameter bound: formal argument or impossibility with evidence
- [ ] Paper updated with 0051 findings
- [ ] Lean 4 roadmap written with difficulty assessments

## Output Location
- Reports: `/Users/kylemathewson/GraphColour/backgroundMaterial/agent0051/coordinator/manager_M2/`
- Paper: `/Users/kylemathewson/GraphColour/backgroundMaterial/agent0051/deliverables/`
