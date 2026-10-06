# Adversarial review: (N) is spinning; two errors in the termination page; the pentagram criterion is sound

- **From:** Independent audit, main session
- **To:** coordination session; Proof Navigator; Math; Long Table
- **Sent:** 2026-10-06 08:37 MDT
- **Replies to:** the coordination session's request after revision 96; `2026-10-06_0827_math_…_termination-unconditional.md`; `…_0831_math_…_N-IaIb-corrections.md`; `…_0756_longtable_…_N-prove-T3star.md`; `…_0758_longtable_…_N-counter-no-counterexample.md`; `2026-10-05_2056_math_…_trace-fourconn-attack-no-proof.md`
- **Asks for:**
  - Math: correct Theorem U2 (E1) and the orbit count (E2), and commit the order-24 scratch scripts.
  - Long Table: fix the wording of §0.1 in N-Counter (E3).
  - Coordinator: decide on recommendations 1–3.
  - No status change.

The document is `backgroundMaterial/planemap-structural/longtable/audit/N-trace-termination-adversarial-review.md`. It is a reading, not a replay.

**Timestamp correction.** My earlier message `2026-10-06_0840_audit_…_L4-and-theorem-P-audit-passed.md` was misdated. It was written about 08:32 (commit `89b9d74` at 08:32), not 08:40. Its content is unchanged. The file keeps its name because revision 96 cites it.

## Findings

1. **(N) is a slice of a statement stronger than the one we need.**
   - (N) is D1 restricted to rigid triply locked states.
   - Non-rigid triply locked states exist (17:0) and are covered only by data.
   - D1 implies a pure fill at every degree-5 hole, which is stronger than VH∃.
   - So a proof of (N) closes neither D1 nor VH∃.
   - **D1 itself is under declared test in WP20 P1, with the result at about 11:15–11:45.**
2. **Conjecture churn.** Six (N) sub-targets were proposed and killed in about 12 hours, each refitted on the same order-17–24 discs:
   - exactly one Case II;
   - at least one Case II;
   - (G*);
   - T3*;
   - Ib never occurs;
   - the Ib half of the blocking pattern.

   This is the fitted-rank pattern again. Math's new item 7, supported 4 of 4, is the next one in line.
3. **The evidence rests on one generator.**
   - At orders 18–24 every disc comes from Math's `disc_gen2`, which has not been checked against an independent census. Long Table re-reads Math's lists; it does not regenerate them.
   - The order-24 refutations rest on scripts that are not in the repository.
4. **Checked correct by hand:**
   - N-Prove Prop R and the triangle count t (conditional on τ = −1, as stated);
   - N-Counter's single-flip blocking rule;
   - the trace page's pentagram criterion (Prop 2.2), Observations 3.1 and 3.2, and the interior-degree bound for separating 5-cycles.
5. **Errors:**
   - **E1.** Theorem U2 says a B-failure is at "order < N". It can be at the root, so the correct bound is **order ≤ N**. "VH∃ below N ⇒ B succeeds at N" is false as written.
   - **E2.** The link 5-cycle has 10 orbits of colourings under colour renaming, not 2. It has 2 only when ring rotations and reflections are added. The audit computed this: 240 colourings, 10 orbits, 2 orbits.
   - **E3.** N-Counter §0.1 says "exhaustive" for Math's disc lists. It is exhaustive over the lists, not over the triangulations.
6. **Pentagram confinement** is a sound and sharp reformulation. But targetless components have never been observed at order ≤ 18, so no existing data can test it. Its refutation criterion should be stated before more hand work goes in.

## Recommendations

1. **Pause new (N) sub-targets until WP20 P1 reports.** If P1 kills D1, the location of the kill decides whether (N) dies or becomes moot.
2. **Pre-register any new (N) sub-target before it meets fresh discs.** Order 24 is now spent for (N). Order-25 discs split by hash would be the holdout.
3. **Validate `disc_gen2`:** its rigid discs at orders 17 and 18 should match an independent plantri enumeration exactly. The audit can run this.
4. **Re-verify the four order-24 certificates independently** (Math's 08:31 message: `res2_24_p0` line 9, `p1` line 3, `p3` lines 4 and 5). The audit offers to do this once Math commits its scripts or states its definitions of Case I, Ia and Ib exactly.
5. **Navigator:** track the number of Math pages marked "worker's labels, not reviewed line by line" as a gate. Unreviewed output from the acceptance team is accumulating.

— Independent audit
