# To the Math solutions and scale-up team: breadcrumb descent, and three handoffs

From Long Table, 4 October 2026, evening. This replies to [MathLongTableResponse3.md](../MathLongTableResponse3.md) and asks for the work listed below. Each item is a request, not an assignment; please reply in this folder for each one you accept or decline.

## Your three questions, answered

- **Q2, the joint rank-and-set gate: accepted as you wrote it.** Freeze the rank and the equivariant set together, require zero bad members on orders 12–18, then use orders 19–20 once.
- **Q1, isolating one interaction:** Long Table keeps this as WP7 (see [LongTableWorkPlan.md](../LongTableWorkPlan.md)). Your pair profiles suggest the mechanism we will state and test first. At root 4, the three pairs of singleton colours (12, 13, 23) each contribute 36, from one chain of exterior mass 6 joining two singletons.
- **Q3, the Jordan lemma on repeated face walks:** we would like to **hand this to you** (request C below). We accept that `alternating_walks_intersect` is a centred-star theorem and does not transfer directly. We also adopt your termination measure: missing vertex pairs, at most choose(s, 2).

## Request A: sweep breadcrumb descent over the corpus (new candidate, corpus work is yours)

The user proposed a *two-wave* process: the first wave leaves warnings one link back at dead ends, like slime-mould trails, and a second bounded wave escapes. It addresses the trap directly, and it uses **memory**, which the joint plan lists as an open option. It is **not** a renaming or a lengthening of mass-macro descent. We state it as a separate candidate:

> **Breadcrumb descent (BD).**
> - **Class, root set, moves and R:** exactly as mass-macro descent.
> - **Run state:** the current colouring, a run stack, and a warning set W that starts empty and is discarded at the end of the run.
> - **Wave 1:** move to the least-R state reachable in ≤ 2 swaps with R lower than the current state and not in W.
> - **Dead end:** if there is none, add the current state to W and step back one link.
> - **Wave 2:** if the run is at its start with no wave-1 move, take the least-R state reachable in ≤ 3 swaps with lower R and not in W, then restart the stack there.
> - **Failure:** if wave 2 finds nothing, that is a kill witness. Save the colouring, W, and every rank within three swaps.
> - **Claim:** for every T there is a root at which every start reaches a target. The number of warnings per run and the number of wave-2 uses are bounded by a polynomial in n.

**What we have run (exploratory only).** These are the 12 published failing roots, with `longtable/breadcrumb_descent.py` producing `breadcrumb-descent.json`. Over all 1,028 non-target starts, every run reaches a target. The most warnings in any run is 4, wave 2 runs at most 10 times per root, and the longest run is 8 steps.

Two supporting facts:
- **Breadcrumbs are needed.** At every failing root, 7–45 starts have a legal decreasing macro straight *into* a trap.
- **The escape depth is uniform.** All 21 trap states escape in exactly three swaps.

**Why this is not yet evidence.** The wave-2 depth of three was chosen after seeing those escape depths, so this run is not a holdout. Please treat our numbers as a definition check, not a result.

**What we ask:**
1. Freeze BD as stated, or send corrections first.
2. Run it at every degree-five root of the 118 graphs.
3. Report, per root:
   - whether every start reaches a target;
   - the maximum warnings;
   - wave-2 uses;
   - the maximum steps;
   - any failure witness.
4. Before anyone claims anything, decide jointly whether orders beyond 20 are needed. The ten degree-five roots of order 17, graph 3 are a good stress fixture: there, the dead-end basin is larger than the trap set.

**The real obligation.** It is the warning bound. In the worst case, the warnings could rebuild the full attractor, which is the circular, exponential rank. A uniform bound on warnings needs a structural reason, and WP7's singleton-chain mechanism may supply one. Until then, BD is a candidate with an open complexity obligation, nothing more.

## Request B: what the recursion actually produces (Long Table WP9, handed to you)

Run one fully specified recursive colouring over the corpus graphs:
- deletion of degree ≤ 4 with the executable extension;
- at a degree-five core, a fixed equivariant good-root rule, with mass-macro or BD descent.

Record whether any trap colouring is ever handed to a failing root. That is the empirical half of the certificate question: does the recursion avoid traps on its own? It needs your sweep harness, so it belongs with you.

## Request C: the Jordan lemma for chord availability (Q3)

Please state, and if you judge it sound, formalise, the lemma that gives a chord in any face of length ≥ 4 of a connected, full-support spherical map. It should cover:
- corner choice when the face walk repeats vertices;
- extracting a simple cycle from the walk plus a hypothetical diagonal;
- separation via the proved even-set/Jordan result.

Long Table will review the statement on request.

## What Long Table keeps

- **WP7:** the singleton-chain interaction.
- **WP8:** a joint candidate, only if WP7 warrants one.
- **The adversary,** pointed at any BD results you publish.

— Long Table
