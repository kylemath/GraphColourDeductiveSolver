# Math review of the interior witness and connectivity

5 October 2026. Scope: the Creative Intel hand pages `docs/working/creative-intel-2026-10-05/interface/interior-witness.md` and `interface/positions/connectivity.md`. No census or new graph was run. These are hand results, not Lean results.

## Accepted interior lift

Math accepts section (A), with its full quantifiers: a fixed interior degree-five vertex and legal fan work in the whole triangulation if every fan-admitted side colouring has a filling path whose every hole stays strictly off the separating triangle. The path may depend on the start. Mere existence of one side colouring or one path is insufficient.

At an interior hole the side and global neighbourhoods agree. Every bichromatic excursion through the other side can be shortened to an edge of the interface clique (or a zero-length walk). Thus a global component restricts to exactly one whole side component when its restriction is nonempty. Lifting each chosen side component, and then each interior singleton slide, preserves the side colouring and properness. At the final interior hole the fill targets agree. A fan chord that is absent from the induced side is absent globally: an edge supplied by the other side would have both ends on the interface and would already be in the side clique.

The same component restriction remains valid when the hole lies on the triangle: its two surviving interface vertices still form a clique. The obstruction there is the larger global neighbourhood, both for singleton legality and for the fill target. It is not a failure of Kempe-component restriction.

Consequently a smallest failure cannot contain a separating triangle with such an interior witness. This does **not** prove that a smallest failure is four-connected. The boundary-hole passage and completed sides outside the minimum-degree-five induction class remain open. The previously accepted H₂ construction is a success carrying an interior, fixed-hole pure-Kempe witness.

## Accepted connectivity core

Math checked the link argument, connectedness, absence of one- and two-vertex cuts, and sections (A)/(B) and their equivalence. In the stated finite simple spherical cell decomposition, links are cycles and the graph is three-connected. Every vertex of a three-cut meets every component after deletion. Removing the other two cut vertices from its link leaves exactly two nonempty arcs, forcing the cut to be a non-facial triangle and leaving exactly two components.

For order at least five, absence of separating triangles is therefore equivalent to four-connectivity. K₄ is the stated order-four exception. At an interface vertex the degree identity is dT=dA+dB−2, with side degrees at least three and total at least four. A floor of five requires the separate minimum-degree-five assumption.

This acceptance covers the connectivity core, not the subsidiary spanning-tree-complement proof in section (C). Its instruction to replace every maximal excursion through a disk needs a finite or continuity argument when a path has infinitely many excursions. The later curvature calculation is valid conditional on Euler's formula; that formula may be cited or supplied with a separate complete proof. None of this affects the accepted three-cut argument.

## Fixed-hole calculation and remaining work

Math also checked the six-pair calculation and the two explicit certificates in section (C) of the interior-witness page. The order-nine double lock has no one-swap fill and the two named swaps fill it. Its degree-three vertex excludes it from the minimum-degree-five class. It supplies no universal double-lock lemma.

The next structural deliverable should prove the double-lock statement for arbitrary interiors, or isolate the additional crossing-component condition a side interface must carry. Keep the inner-triangle carry separate: even a fixed-hole theorem for this one link does not automatically transfer an arbitrary good pair. The completed side loses one neighbour at each boundary vertex and may leave the induction class.

For Lean, the useful next interface is a clique-separator component restriction/lift lemma followed by an interior-path lifting theorem. Its statement must quantify over all holes of the side path, rather than merely its endpoints. This packages the accepted result without assuming the missing boundary passage.
