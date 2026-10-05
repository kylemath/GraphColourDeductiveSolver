# Portfolio contact and a genuinely different mobile-vacancy attack

4 October 2026. No external messages or producer experiments.

## Compiled conditional result

`RankPortfolio.lean` fixes a finite family of ranks before the graph. Its hypothesis chooses root and portfolio index from the graph before universally quantifying over deletion colourings. The resulting general spherical four-colour statement is conditional on exactly that hypothesis. No selector, structural descent or complexity theorem is claimed.

The separate lower-envelope theorem proves that an actual minimizing coordinate can decrease the envelope. It assumes active-minimum coverage; arbitrary statewise convenient coordinates do not suffice. A Boolean two-state regression exhibits convenient-coordinate descent while the envelope is constantly zero. Seven exact axiom guards list only propext, Classical.choice and Quot.sound.

## New attack: allow the vacancy to move through degree-six vertices

The bad mass fixture at order17 graph0 root4 cannot slide immediately to another degree-five root: all three singleton-colour neighbours have degree six. Rather than insist on a different feature at the same root, allow those moves and study one coherent partial colouring with a mobile hole.

A state is (r,c), where c properly colours every vertex except r. A singleton slide to adjacent x colours r with c(x), uncolours x, and preserves all other colours. The uniqueness of c(x) on the current boundary proves properness. This is reversible. Combine these slides with actual component swaps in the CURRENT deletion graph, never transplant components between carriers.

**Elementary new local fact.** Suppose the hole has d neighbours, its boundary uses four colours, and d≤7. If s is the number of singleton colour classes on the boundary, then

    d ≥ s + 2(4-s) = 8-s,

so s≥8-d. Every non-target hole of degree5 has at least3 slides, degree6 at least2, degree7 at least1. A hole whose boundary uses at most3 colours is already extendible. Thus on a degree5/6 triangulation there is never a non-target state with no legal vacancy slide. This eliminates the immediate degree-five-carrier obstruction; it does NOT eliminate cycles.

**Why mobility alone cannot be enough.** K5 with a vacant vertex has four uniquely coloured neighbours. Every slide is legal forever, but no target exists. Any argument using only boundary multiplicities and reversibility would incorrectly prove K5 four-colourable. The missing ingredient must exploit the sphere.

## A structural obstruction lemma for closed vacancy classes

Fix a connected component C of the slide-state graph containing no target, and let S be the set of vertices that occur as vacancies in C. For every state in C at r, all singleton-coloured neighbours of r belong to S, since sliding to any of them stays in C. If the graph has maximum degree6, then each r∈S has at least2 neighbours in S. Therefore the induced graph on S contains a cycle. With maximum degree5 it has minimum degree at least3.

This is a graph-level consequence, not a search score. It suggests looking for an innermost vacancy cycle and analyzing the recolouring monodromy obtained by transporting the hole around it. Along a simple slide path the colours of visited vertices shift one step; a closed path can change a full colouring on that cycle while returning the vacancy to its original position. These moves are not restricted to a single bichromatic chain.

The tempting but unproved pumping lemma is:

> In a minimum-degree-five spherical triangulation of maximum degree six, a targetless connected component of the slide-plus-Kempe partial-colouring graph cannot exist.

This would be a substantial theorem for the degree5/6 class, which includes the known first traps and symmetric fullerene-type fixtures. It is stronger than existence of a colouring and has no polynomial bound yet. Proving it may be as difficult as the Four Colour problem on that class. The useful first hand target is narrower: characterize the colour constraints on an innermost simple vacancy cycle and show when its monodromy yields a target or enlarges S. A successful mechanism must name the planar separation fact and a decreasing region measure; 'some future hole extends' is circular.

## Why this direction is worth a bounded exploratory investment

It directly uses the observed obstruction (singleton exits leading to degree6), retains an actual colouring through root changes, and offers cycles/regions rather than another fitted weighted rank. It also has crisp kill points: exhibit a targetless slide-plus-Kempe class in the degree5/6 domain; or exhibit an innermost cycle whose rotation cannot change any boundary lock. A failure of slides alone would only demand Kempe preparation, not kill the combined route.

Nothing here releases additional corpus work, alters WP11, or claims a theorem about all Kempe classes. The conditional portfolio formalization is ready for review; the mobile-vacancy mechanism is a distinct mathematical proposal.
