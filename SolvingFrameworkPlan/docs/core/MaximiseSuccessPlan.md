# Plan to maximise the chance of success

Written 6 October 2026, 15:00 MDT, by the coordination session, on the user's instruction: "reformulate your plan ... to maximize moving that live likelihood of success meter up", and "even if in short term it will go down, if the ultimate outcome is more likely we should go or branch that route".

## The meter, and how it may move

The meter (`docs/navigator/forecast.json`) estimates P(we finish a correct, audited proof of the Four Colour Theorem along our routes). It is the coordinator's judgement and moves **only on checkable evidence**: an audited proof, a replayed certificate, a killed route, or a literature finding. Optimism, effort and partial drafts do not move it. A kill of a route we were counting on moves it **down**, and that is still progress: it frees effort for routes that can work. This rule is what keeps the meter worth reading.

Today: 3% ≈ P(R\* true, 0.85) × P(we prove R\* in the open case, 0.04) × P(formal chain closes, 0.8). The middle factor is the bottleneck: almost all the gain is there.

## Strategy: branch, so that one route failing does not end the project

| Route | Idea | Why it raises the ultimate chance | Owner |
|---|---|---|---|
| **A. Structural R\*** (current) | Prove R\* in the open case by hand, choosing the vertex | The cleanest result; a short proof | Math, Long Table, interns |
| **B. Kempe-reducible configurations** (new branch) | Allow a **small, computer-checked** set of local configurations, each shown pure-clean (Kempe-reducible) for every colouring, plus a discharging argument that every core triangulation contains one. VH∃'s freedom (choose the vertex, any number of pure swaps) should make far fewer configurations reducible-by-Kempe than the classical sets need. | Converts the open case into a finite, checkable problem; the method is classical and known to work for 4CT in principle | Studio Intel (engine), Studio Math (Lean), Math (discharging) |
| **C. Information first** | Literature: is R\*, or "every Kempe class of colourings of T − v contains a fillable state", a known theorem, a known open problem, or equivalent to something hard? Kempe-equivalence results for 4-colourings of near-triangulations. | Cheap; can move the estimate a lot either way, and may hand us a tool | Audit (sources), Long Table (reading) |
| **D. Formal chain** | Link D: core-class R\* ⇒ 4CT in Lean | Raises the last factor toward 1; any proof from A or B plugs in | Studio Math |
| **E. Fail fast** | Adversary searches for a counterexample to R\* (stuck class) at larger orders with the fast engine | If R\* is false, we must learn it now and switch fully to B | Studio Intel (Phase D), Audit |

Route B is a deliberate change of goal: it gives up "no configuration census" in exchange for a much higher chance of a complete, audited proof. The census would be small and machine-checked in Lean if possible. Route A continues in parallel; if it succeeds, it supersedes B.

## Data-driven proof search for Route A

Instead of more random kill tests, mine the hard states for mechanism: for every doubly locked state of radius ≥ 3 in the data, record which swap sequence fills it and which local features it uses; propose the smallest rule that explains them all; prove that rule by hand; then test it adversarially. (Intern D's Conjecture C5 is the first such rule.)

## What each team does now

- **Math:** Route A lead (the two-degree-6 classes); also design the discharging rules Route B will need (which configurations are unavoidable in min-degree-5 core triangulations, using the Euler lemma).
- **Long Table:** Route C reading (Kempe equivalence literature, Tilley, Mohar–Salas, Fisk) and Route A's selection argument.
- **Audit:** Route C source checks; the radius-5 replay; adversary on A and B.
- **Studio Math:** Route D (link D), then the Lean framework for Route B's "configuration is Kempe-reducible" certificates.
- **Studio Intel (when resumed):** Route B engine: for each candidate configuration, decide by computation whether every colouring of its boundary fills by pure swaps inside it; Route E with the fast engine.
- **Interns:** Route A data mining (C5 and successors), Route B candidate configurations by hand.

— Coordination session
