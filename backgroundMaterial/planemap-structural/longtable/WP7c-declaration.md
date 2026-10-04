# WP7c declaration: does each warning charge a distinct locked pattern?

Long Table, 4 October 2026. Committed **before** the test. The input is the math team's `breadcrumb-warning-traces.json`, verified against `breadcrumb-warning-SHA256SUMS`. It covers 12 roots, 1,700 starts, 940 non-target starts and 39 runs with warnings. No colourings are regenerated.

**Erratum.** Our message `2026-10-04-longtable-to-math-breadcrumb-and-handoffs.md` and its summary said "1,028 non-target starts" for our exploratory run at the same 12 roots. The correct total is **940** (38+38+48+48+60+60+84+84+128+88+132+132). The math team and the Proof Navigator have already recorded this. Our message is left unedited, per the folder convention.

## The pattern of a warned colouring

Fix a run at root r. Let b0, …, b4 be the root's boundary in the trace's `boundary_cyclic_order`. All warnings in a run share this root, so **boundary positions are not rotated or reflected**. Patterns are compared only within one run, and descriptively within one root.

1. **Colour normalisation.** Rename the colours in order of first occurrence along b0, …, b4. A warned state is non-target, so all four colours occur on B and the renaming is unique. Pairs are labelled with the normalised colours.
2. For each of the six normalised pairs {x, y}, let I be the set of boundary positions k with colour x or y. Record:
   - **F:** the partition of I by connectivity in the **full** {x,y}-subgraph of T − r;
   - **L:** the partition of I by connectivity in the {x,y}-subgraph **induced on B alone**, using the actual edges of T among b0, …, b4, chords included;
   - **E:** for each block of F, whether its full component contains a vertex outside B.

   F, L and E are recorded independently. A chain may have a route along the boundary and exterior vertices at the same time; nothing makes those labels exclusive.
3. **Pat(c)** is the normalised boundary tuple together with (F, L, E) for each of the six pairs.

Pat takes finitely many values, bounded by a constant independent of n: the boundary tuple, and the partitions and flags on at most 5 positions per pair. It depends on the root only through B, not on any colouring outside the chains' connectivity.

## Claim under test

**C7c (injective charging within a run):** in every run, distinct warned colourings have distinct patterns.

- **Kill:** a single run with two distinct warned colourings of equal Pat. We record the run and both colourings.
- **A pass would not prove:** injectivity in general, preservation under any recursion, or a global warning bound. It would be finite evidence that this object is worth a proof attempt.
- **What a failure would not kill:** a bounded-multiplicity variant would need its own stated bound and structural reason. It would not be inferred from these data.

## Also reported (descriptive)

Per root, across all its runs:
- the number of distinct warned colourings;
- the number of distinct patterns among them;
- the largest number of distinct warned colourings sharing one pattern.
