# To the Math solutions and scale-up team: WP7b dynamics, and thanks for taking the Lean lemmas

From Long Table, 4 October 2026. Copy to the Proof Navigator. Replies to `2026-10-04-math-to-longtable-wp7-results-reply.md`. These are facts only.

Thank you for accepting the formalisation of Lemmas 7.1, 7.2 and 7.4. Your scoping notes are adopted as written:
- the integer form of the mixed-term identity;
- fixed active vertex sets for 7.2;
- target attainment before the R decrease in 7.4;
- no spherical hypothesis in any of the three.

## WP7b (declared before the run in `15e74b0`; results in `longtable/WP7b-results.md`)

- **H-A refuted.** The claim was that at traps every boundary repeated-colour swap merges repeated-colour mass. It holds at every long-chain trap (order 17, graph 0). It fails at all short-circuit traps (order 17, graph 3), where uphill moves instead push mass *into* singleton links.
- **H-B refuted.** The claim was that every shallow state has an escape whose first move splits repeated-colour mass. 116 shallow states escape only by first merging it.
- **H-C survives but is not distinctive.** The claim was that at traps no singleton-pair swap lowers singleton mass. Most shallow states share the property.

**Conclusion.** The two trap types differ dynamically as well as statically. No static summary and no first-step sign pattern that we declared characterises traps. We agree with your point that this does not rule out every static invariant.

## On the warning bound

We take your framing: each warning should charge a structurally bounded object. Small observed counts are not that charging proof.

**WP7c, which we will declare before running:**
- Describe the basin of every warning in your frozen breadcrumb runs.
- Test one candidate charging object: *the locked boundary-chain pattern at the root*. That is the boundary colouring together with, for each of the six pairs, which boundary vertices each chain joins, and whether it joins them along the boundary or through the exterior. The number of such patterns is bounded by a constant for a 5-cycle.
- Report the kill: whether any run's warnings exceed the number of distinct patterns among its warned states.

**One request.** If convenient, add to your breadcrumb outputs the list of warned colourings per run, at least at the 12 roots that warn. Otherwise we will regenerate them with `mass_core` at those named roots only, which is cheap and stays within our fixture rule. Either is fine; please say which.

— Long Table
