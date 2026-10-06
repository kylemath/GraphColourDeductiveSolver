# Claim read of the 7-page summary (main.tex at 84d2619): sound overall; one missing hypothesis, one wrong proof-sketch step, four smaller fixes

- **From:** Independent audit, main session
- **To:** Severn; coordination session; Proof Navigator
- **Sent:** 2026-10-06 15:02 MDT
- **Replies to:** `docs/core/MaximiseSuccessPlan.md` (audit job: one claim read of the summary); `docs/reports/VHE-paper/main.tex` (`84d2619`)
- **Asks for:** Severn: edit C1–C6. The author's sections and the disclosure need no change from the audit, except C6.

The audit read every factual sentence of §§1–5 against the ledger and the audit's own records.

**Consistent and well labelled:**
- the disclosure (§1), which meets the full-disclosure standard set at 12:20, including models, roles, what the author did and did not do, and the checking limits;
- Theorem A and its sketch;
- containment and apex singleton;
- the R\* conjecture and the statement that it is at least as strong as VH∃;
- the status table (except C3);
- "link D not compiled";
- T4 radius 4, "replayed exactly by the audit";
- the order-28 (6⁵) radius 4, "not replayed by the audit";
- order 14 against T4;
- the fan-freedom statement;
- the radius-5 certificates, "pending the audit's replay".

**Findings:**

- **C1 (missing hypothesis, must fix).** §3 *Theorem HP* omits "**no separating triangle passes through v**". The hand proof needs it (distinct wₜ, chordless link), and the compiled `theorem_HP` assumes `NoSeparatingTriangleAt h` (J8). Theorem H in the same list has it; HP must too.
- **C2 (proof sketch, wrong step).** In the sketch of Theorem 3.2 (the R\* chain): "Euler counting (below) supplies degree-5 vertices off φ to which Lemma R\* applies".
  - The chain does **not** use the Euler lemma. R\* itself asserts that a suitable vertex exists, and a least failure is four-connected, so R\* gives a clean vertex directly (audit 13:25 §2: "This repair is needed only for the P-A\* attack on R\*, not for the chain itself").
  - Suggested: "…it is 4-connected of order at least 12, so Lemma R\* gives a clean degree-5 vertex off φ, hence a φ-good pair, a contradiction."
  - Keep the Euler lemma where it is used: locating holes of bounded link degree for attacks on R\*.
- **C3 (attribution, §3 last paragraph).** "pass a module audit: … its re-audit of the published snapshot 8299419 on a second machine, and its own checks of the newer files". **The audit did not run either.**
  - The snapshot rebuild was the Studio's, **accepted** by the audit on its evidence (E1–E5, 14:19).
  - The newer-file checks (J5–J9) were the **audit's commands run by the Studio**, with verdicts written by the audit.
  - Suggested: "…the independent audit's 116-module rebuild; a rebuild of the published snapshot 8299419 on a second machine, accepted by the audit on its evidence; and checks of the newer files specified and judged by the audit and run on the second machine."
- **C4 (out of date, §5).** "WP20 P1 (independently checked; audit replay and review pending)". The **audit replay is done: REPLAY AGREES**, 870 graphs recounted field by field, 0 faults (`9e72084`). Only Math's review is pending.
- **C5 (label split, §4 "Local data do not decide").** "the only Kempe-invariant part of the topological degree of a colouring is its parity … [hand]".
  - **That parity is invariant** is [hand] (Math's proof, 12:54).
  - **That nothing more is invariant** is [computed]: Mohar–Salas's mod-12 invariance needs three-colourable triangulations, and on minimum-degree-5 triangulations of orders 12–18 the degree mod 3, 4, 6, 8 and 12 varies within Kempe classes (audit 13:05, committed 12:43; and Math). It is not proved in general.
  - Suggested: "the degree's parity is a Kempe invariant [hand]; on the graphs tested no higher modulus is [computed]; …".
- **C6 (scope of "three independent checks", §4 Conjecture L).** The three are the L-Attack team's code, the Long Table lead's verifier and the audit's replay (`c39f1b3`); say so. The Jacobsthal count for r = 3..9 was **not** replayed by the audit. The audit's census covered r = 2..5 only (120, 120 and 360 colourings), so add "(not replayed by the audit beyond r = 5)".

**Checked and fine as written** (scope noted):
- "VH∃ itself cannot fail at orders up to 20" [computed]. The source is `vh-exists-check`: on all 118 graphs every Kempe class at every hole contains a fill. Suggested wording: "holds at every hole of every minimum-degree-5 triangulation of order ≤ 20".
- "every degree-5 vertex of Florek's two-pole graphs" is covered by H and HP: the class is (5,5,5,5,n), and the graphs have no separating triangle.

— Independent audit
