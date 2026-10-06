# Intern D, cycle 4: why an edge-deletion class can trap x,y together (order 17, graph 0, edge {0,1})

Hand work on the first record of `longtable/studio-explore/kempe-classes/edge-new-classes.jsonl`. Adjacency from the plantri ascii; colour classes and components traced by eye; nothing run. Labels: [hand-read] data reading, [hand] argument, [open] not proved.

## The example
x=0, y=1 (degrees 5, 5), kappa(T)=8, kappa(T-e)=3. Common neighbours (the two triangles on e): p=2 and q=5. Class representative: colour 0 = {0,1,8,10,13}, colour 1 = {2,4,12,14}, colour 2 = {3,6,11,15}, colour 3 = {5,7,9,16}. So x,y have colour c=0, p has colour 1, q has colour 3, and the fourth colour is r=2.

Connectivity of the six pairs [hand-read]:
- {0,1}, {0,2}, {0,3}: each connected, so x and y lie in one component for every pair containing c=0.
- {2,3}: connected.
- {1,2}: two components ({2,3,4,11,12,6} and {14,15}); {1,3}: two components ({2,7,14,9} and {4,5,12,16}).
That is 4 of 6 connected (inside the 3-5 range reported). Colour 0 is also a dominating set: every other vertex has a colour-0 neighbour.

## Why x and y cannot separate [hand, partly open]
1. **Two of the three pairs are connected for free.** x and y share the neighbours p and q. So x-p-y is a {c, c(p)}-path and x-q-y is a {c, c(q)}-path. Only the pair {c, r} (r = the colour on neither p nor q) can separate them. This holds in every state of T-e where x,y share a colour and p,q have two different colours.
2. **The remaining pair is a single dual alternative.** The deleted edge leaves a quadrilateral face x,p,y,q. Jordan, exactly as in the lock criterion: either p and q are joined by a {c(p),c(q)}-path (a closed curve through the face separates x from y, so x,y are NOT {c,r}-connected), or they are not (then x,y are {c,r}-connected). Here {1,3} does not join p=2 to q=5 (they sit in different components), hence {0,2} joins x to y: verified by the path 0-3-10-15-13-6-1.
3. **A swap can only part x from y by a {c,q'}-chain that contains one of them without the other.** For q'=c(p) or c(q) this is impossible by step 1. For q'=r it is impossible while step 2 puts both in one {c,r}-component. Swaps of chains avoiding colour c do not move x or y.
4. **The remaining question is whether swaps of chains of colours {1,2,3} can break the {c,r}-connection** (it needs the {c(p),c(q)}-path to appear). I checked two swaps by hand (flip {14,15} in {1,2}; flip the large {1,2}-component {2,3,4,11,12,6}): after each, {0,1} and {0,2} are still connected and x,y still share a component in {0,2}. The class has only 6 states, so closure under these flips is a finite check I did not complete by hand [open: Studio to verify, request below].

So the trap is: x,y have colour c, and p,q (their two common neighbours) are never joined by a {c(p),c(q)} chain, in any state of the class.

## Link of a deleted vertex: does the same trap occur? What breaks
Replace x,y by x_j,x_{j+2} (repeat colour alpha), with common neighbour m (v is gone). The free connection is {alpha, mu} via m, matching step 1. But now there are **two** nontrivial pairs, {alpha,A} and {alpha,B}, not one, and the lock criterion shows both can separate x_j from x_{j+2} (two Jordan curves, closed through v, using paths m~a and m~b). The Studio's no-frozen lemma says a doubly locked state has both pairs disconnected, i.e. the opposite of the edge trap (where the nontrivial pair is connected). A targetless class at a vertex would need both lock paths in every state and closure under the F move, which Long Table's Z/Y/W system reduces to a meander condition. That is exactly R*, still open; the data say no such class exists at degrees 5-7.

**One sentence: an edge has two common neighbours that connect its ends in two of the three colour pairs for free, leaving a single dual alternative that a small closed class can satisfy everywhere, whereas a vertex link needs two simultaneous lock paths in every state, and the move F always touches one of them.**

## Requests for the Studio
1. For all 16 edge classes: record c, c(p), c(q), r, and whether {c,r} connects x to y in every state of the class (prediction: always yes; and p,q are never {c(p),c(q)}-connected).
2. Check whether colour c is a dominating set in every state of every class (prediction: yes in the example; if true it is the mechanism for preservation under swaps).
3. For each non-trivial swap in each state, check that x,y stay {c,r}-connected after it (completes step 4).
4. Are there edge-deletion new classes where c(p)=c(q)? Step 1 changes (only one free pair), so the trap may fail there.

## Self-check
Most likely failure: step 4 is unproved; the closure could rely on global features (dominating set, tiny class size) that do not generalise. The vertex comparison is an analogy, not a proof, and the last sentence is a heuristic summary of it.
