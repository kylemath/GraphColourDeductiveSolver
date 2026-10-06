# Adversarial review: (N), the trace and four-connectivity attack, and termination

Independent audit, 6 October 2026, 08:36 MDT. **This is a reading, not a replay.** The audit ran no census. It ran no team script except one 5-line count (§3.2). The audit read these:

- Math: `MathNAttack.md`, `MathNPinchT3.md`, `MathNCaseI.md`, `MathNGstar.md`, `MathNIaIb.md`, `MathTraceFourConnAttack.md`, `MathTerminationUnconditional.md`, and its messages of 5 October 20:56 to 6 October 08:32.
- Long Table: `creative-intel-2026-10-05/n-prove.md`, `n-counter.md`, `d1-hand-attack.md` §0 and §7–§10.

Labels are as in `START-HERE.md` §5. "Checked" below means the audit re-derived the step by hand.

## 1. Where (N) sits, and the main finding

The logical chain, from the teams' own pages:

1. **(N)** is D1 restricted to **rigid** triply locked states (`d1-hand-attack.md` §7, Props 5 and 6).
2. **D1** says every unfilled state at every degree-5 hole is separable, or one pure swap from a separable state. It implies a pure fill at every degree-5 hole. That is **stronger than VH∃**, which needs one good vertex and fan. D1 for all minimum-degree-5 triangulations implies the Four Colour Theorem (§9 there).
3. **Non-rigid triply locked states exist.** They are the 4 states on 17:0. Their escape is [data] only (§8 there).

So a proof of (N) would close neither D1 nor VH∃. It would close one slice of a statement stronger than the one the induction needs. In about 12 hours that slice has absorbed most of the effort of both teams' research workers.

**D1 is the statement WP20 P1 is testing right now, on order 25.** The result is expected between 11:15 and 11:45.
- If P1 kills D1, the motivation for (N) changes completely, and the location of the kill matters:
  - a kill at a rigid triply locked state also kills (N);
  - a kill elsewhere makes (N) moot as a route to D1.
- If P1 passes, (N) remains one unproved slice of a statement with one more confirmatory pass.

**Recommendation 1.** Pause new (N) sub-conjectures until P1 reports. Hand work on statements already written down can continue.

## 2. (N): the conjecture churn is the pattern the fitted ranks showed

Every one of these local targets was proposed from data at orders 17–23. Each was refuted at the next order or the next disc list, within about 12 hours:

| Target | Proposed | Refuted |
|---|---|---|
| "exactly one of c′, c″ is Case II" | MathNPinchT3 §5 (order 17, 4 states) | order 23, `res_23` discs 2 and 3 (Math 07:47; Long Table N-Counter) |
| "at least one is Case II" | MathNPinchT3 | the same discs (Case I × Case I) |
| (G*) | MathNCaseI (8 of 8 at order 23) | order 24, 4 of 22 (Math 07:49) |
| T3* | n-prove §5 (32 of 32) | equals (G*) in Case I, so refuted at order 24 (Math 08:31) |
| "Ib never occurs at a triply locked state" | n-counter §0.5 | order 24, 4 of 52 (Math 08:31) |
| blocking pattern (L1), the Ib half | n-counter §4 (about 207 cases) | order 24 (Math 08:31). The other half is vacuous in the data. |

These kills are good science: they are certificates, and each team reports them plainly. The workflow problem is that each successor statement is fitted to the data that killed its predecessor. It is then "supported" by the same few dozen locked discs, often with counts like 4 of 4 or 8 of 8. This is the fitted-rank pattern (q, lin) that the project already stopped once.

**Math's 08:31 item 7** is "the branching swap at c2 breaks the chain {D,α}", supported 4 of 4. It is the next candidate in the same line.

**Recommendation 2.** Any new (N) sub-target must be written down **before** it meets fresh discs, then tested once.
- Order 24 is now spent, for (N) as well.
- Order 25 discs, split by hash as in the rules amendment, are the natural holdout.
- Until then, a sub-target is a [lead] and is not worth further hand effort.

## 3. Evidence base for "(N) holds on every disc tested"

### 3.1 One unvalidated generator carries everything above order 17

- Everything at orders 18–24 comes from Math's `MathNDiscSearch` generator, `disc_gen2`.
- Long Table's N-Counter **reads Math's discs as data**. It notes that their exhaustiveness at n ≥ 19 "is Math's claim, not re-checked". Math's 07:49 message also says the order-24 generation "is untested against an independent census".
- So "no counterexample to n = 24" is a statement about one program's output.
- The independent part is the check of each listed disc: recheck.py, and the N-Prove certificates for discs 2 and 3. That shows that listed discs are genuine. It does not show the list is complete.

**Recommendation 3, a cheap validation.**
- At orders 17 and 18 (lemma-test use of spent orders), compare the generator's rigid discs with the rigid states found by an independent plantri enumeration, such as N-Counter's `ncounter_p17.py`, extended to order 18.
- They should agree exactly, up to the stated reflection convention.
- The audit can do this if asked.

### 3.2 Some refuting computations are not in the repository

- Math's 07:49 and 08:31 messages say the worker's scratch scripts are in its session scratchpad, not in the repo.
- The order-24 refutations of (G*), T3* and "Ib never occurs" can therefore be reproduced only from the cited disc lines (`res2_24_p0` line 9, `p1` line 3, `p3` lines 4 and 5), with code that no longer exists in the repo.
- A refutation is a certificate and needs independent checking, not a holdout (`START-HERE.md` §5).

**Recommendation 4.**
- Math commits those scripts.
- The audit independently re-verifies the four order-24 certificates (Case I or Ib, the c3 state, and the chain status). The audit offers to do this.

## 4. Technical checks of individual claims

### Checked, correct [hand]

- **N-Prove Prop R (region theorem).**
  - Each H-triangle has one vertex of each of the three colours other than D.
  - Two triangles that share an edge share a vertex coloured p or q.
  - The propagation argument is sound.
  - Math's 08:31 message reached the same conclusion independently.
- **N-Prove triangle count**, t = 2n − 7 − Σ_{V_D′} deg.
  - Faces at x: 5. Faces meeting the independent set V_D′: Σ deg. The overlap is the 2 faces at x and u0.
  - With the type II excess, t = n − 4 − 2n_D′.
  - This is conditional on τ = −1, exactly as the page says.
- **N-Counter, the single-flip blocking rule.**
  - Deleting ab raises comps_pq by 1.
  - Adding cd either merges two r,s-components, which first-order locks forbid (comps_Dβ and comps_Dγ ≥ 2), or closes a cycle, which rigidity forbids.
  - So no single flip preserves a rigid triply locked state. The two-flip result is [computed] only.
  - The page says plainly that recolouring after a flip was not tried. Flips with the colouring fixed are a very small neighbourhood, so §3 of N-Counter is weak evidence against counterexamples. It should not be cited as more.
- **Trace page, Lemma 2.1 and Proposition 2.2 (the pentagram criterion).**
  - A family of edges of a 5-cycle with no common vertex contains two disjoint edges.
  - So "no good fan" is equivalent to "two targetless states with disjoint repeat pairs". Correct.
- **Trace page, Observation 3.1.**
  - The audit also checked the swaps the page does not list: every swap that recolours an α ring vertex drags a ring neighbour (x0 is adjacent to x4 and x1; x2 is adjacent to x1 and x3).
  - So only changes at the singleton vertices can remove a colour. The claim stands.
  - Wording: "stuck" here means "no single swap fills". "Targetless" (no filled state in the whole component) is much stronger. The page uses both words in the same paragraph.
- **Trace page, Observation 3.2 (Jordan).** The {β,δ} curve separates x0 from x2, so the {α,γ}-swap at x2 moves the repeat pair to {x0, x3}. Correct.
- **Trace message item 6.** With two interior vertices in a separating 5-cycle there are 3k + b − 3 = 8 interior edges, so the interior degree sum is at most 9 < 10. Correct.

### Errors found

- **E1, `MathTerminationUnconditional.md`, Theorem U2: the bound "order < N" is wrong.**
  - Take T itself of minimum degree 5, with every child B(T*_p) returning a colouring, but every pair stuck.
  - Then the FAIL node T′ chosen in the proof is the **root**, of order N.
  - So the theorem should read "order ≤ N". The sentence "if VH∃ holds for all triangulations of order < N then B succeeds on every input of order N" is false as written: it needs VH∃ at order N as well.
  - The 08:27 message repeats the error.
  - The proof itself is otherwise correct: B halts, and a deepest FAIL node carries one stuck start per legal pair.
- **E2, the same page, §4.1: the orbit count is wrong.**
  - "240 proper colourings of the link 5-cycle … two orbits under colour renaming" is not right.
  - Under colour renaming alone there are **10** orbits: 5 with three colours and 5 with four.
  - With rotations and reflections of the ring added there are **2**.
  - [computed by the audit: 240 colourings, 10 orbits, 2 orbits.] The point the page makes does not depend on this.
- **E3, a quantifier slip in N-Counter §0.1.**
  - It says the search was "exhaustive" within Math's disc lists for orders 17–23.
  - It is exhaustive over the lists, not over the triangulations. The page says so in §1; §0 should say it too.

### Correct and worth stating more strongly

- **Termination U1/U2 is a genuinely useful unconditional result.** Halting, together with "B fails only at an explicit VH∃ counterexample, at order ≤ N", turns VH∃ into a checkable property per instance.
- **§3, P(K, R), is the honest form of the polynomial-time question.**
- **The §0 correction is right.** "A degree-5 vertex next to a degree-≤4 vertex" is vacuous at d = 5 levels.

## 5. On the trace and four-connectivity line

- The pentagram reformulation is the cleanest new object of the day. It reduces "no good fan at v" to **two** targetless states with disjoint repeat pairs.
- Math has made "pentagram confinement" its sharpest open lemma.
- It is falsifiable cheaply: on graphs where targetless states exist, compute the family of repeat pairs at each root. A root whose family has two disjoint pairs refutes confinement at that root, though not the "some root" form.
- The trace page itself notes that targetless components do not appear at orders ≤ 18 at all. Every saved WP18/WP19 start fills. So **no existing data can test confinement**: the lemma is about objects that have never been seen.
- That is a reason to be careful, not to stop. A lemma about objects whose existence is the open question is close to the original problem in disguise. `d1-hand-attack.md` §9 warns of exactly this for D1.

## 6. Workflow summary for the coordinator

| Line | Verdict | Next step |
|---|---|---|
| (N) | **Spinning wheels.** Six sub-targets killed in about 12 hours, each refitted on the same discs; it is also a slice of D1, which is stronger than VH∃. | Wait for WP20 P1. Pre-register any new sub-target. Validate the disc generator. Commit the scripts. |
| D1 / WP20 | On track: a declared, confirmatory test of the parent statement. | Audit replay as pre-registered (`WP20-P1-audit-replay-plan.md`). |
| Trace / pentagram confinement | Sound reformulation; the open lemma has no test data by construction. | Hand work only; state in advance what would refute it. |
| Termination | Solid unconditional result, with one off-by-one (E1). | Math corrects U2 to "order ≤ N". |
| Review load | Several Math pages carry "worker's labels, not reviewed line by line". Math is the acceptance team, so unreviewed Math output is accumulating. | The Navigator should track the "unreviewed by Math" count as a gate. |

No status changes are requested. Status words stay with the Navigator.
