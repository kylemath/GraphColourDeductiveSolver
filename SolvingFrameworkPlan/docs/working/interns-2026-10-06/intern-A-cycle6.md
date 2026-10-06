# Intern A, cycle 6: inert-disc claims under (Q-all), and the 20/51/1 data

Hand only. Names as in InternA-inert-disc.md: x0..x4 = link (a,b,a,g,d), L1 a {b,g}-path x1~x3, K1 the whole {b,g}-chain (component of x1 and x3), D1(P) = side of J1(P) = v + P that contains x2.

## 1. Quantifiers
- (Q-exists): K strictly inside D1(P) for some simple lock-1 path P.
- (Q-all): K in D1(P) and disjoint from P for every simple lock-1 path P.
- (Q-chain, strongest): K disjoint from K1 and inside the region cut off by K1. Q-chain implies Q-all implies Q-exists.
x2 is inside D1(P) for every P (rotation at v), so the component of T - v - K1 containing x2 satisfies Q-chain, and so does anything cut off from x1 by a dangling cycle of K1. A vertex like 11 in the hexagon is Q-exists (inside for path A) and not Q-all.

## 2. My claims under Q-all (K contains no link vertex)
- **(i) lock 1:** survives. K misses every lock-1 path, so each lock-1 path keeps its colours; the link and frame are unchanged. [hand] Lock 1 survives already under Q-exists.
- **(i) lock 2:** survives iff some lock-2 path misses K. Q-all does not give this: L2 can enter D1(P) through a b vertex of P and return, so an {a,d}-component K can contain a d vertex of the excursion. Sufficient: K misses K2 (for example K is a {b,d}-component other than K2), or L1 and L2 meet only in x1. [conditional, unchanged]
- **(i) K containing x2:** only K_D2, a catalogue move that changes the frame. [unchanged]
- **(iii)** survives and sharpens: under Q-chain, K1 is untouched as a set and as colours, so every lock-1 path survives, and {a,d}-connectivity outside D1 is unaffected (an {a,d}-chain cannot cross J1). Still changeable: the colours at x2's neighbours, K_F, K_AB, K_D2 membership, and the {a,b}/{a,g} chains crossing J1. [hand]
- **(ii) the sage's pruning claim:** NOT refuted by the 20/51/1 move {11} (it fails Q-all), and NOT proved by (i). My mechanism (below) is Q-all-compatible, so the claim can only hold with an exception for swaps adjacent to x2.

## 3. The mechanism, restated and sharpened [hand]
**Kill.** Hypotheses: x2 has degree 5, w1 is g (not d), w2 = d, and Y := the {b,d}-component of w2 is not K2. Then Y, F, fill is a sequence of length 3 (or 2 if Y breaks lock 1). Proof: the Y-swap recolours w2 to b and touches no link vertex; x2's neighbours become x1 = b, x3 = g, w1 = g, w2 = b, so x2 has no d-neighbour; F leaves the {b,d}-graph unchanged and x2 becomes g, so lock 2' (a {d,g}-path x4 ~ x2) fails; an unfilled non-DL state fills in one swap.
**Consequences.**
1. No state of radius >= 4 satisfies these hypotheses. So the mechanism can contradict pruning only at radius exactly 3.
2. It does not need Y strictly inside any disc to be a valid kill; Y inside is what makes the first swap "inert" by the sage's definition.

## 4. Data 20/51/1 (from the plantri line in inertdisc-first-instance.json, read by hand)
x0..x4 = 6,7,8,2,0; x2 = 8 has neighbours {1,7,16,9,2}, so degree 5, w1 = 16 (colour 1 = g), w2 = 9 (colour 0 = d). **All my mechanism hypotheses hold in this graph.** x3 = 2 has degree 7 with neighbours in rotation 0,1,8,9,10,11,3: after w2 = 9 come 10 (b), 11 (a), then w3 = 3 (b). 9's neighbours are 2,8,16,17,10 with colours 1,3,1,3,2, and 10's neighbours 2,9,17,18,11 have colours 1,0,3,1,3, so **Y = {9,10}** exactly. Swapping Y: 9 -> b, 10 -> d. Then 8 has neighbours b,g,g,b: no d. F then fails lock 2' (8 becomes g with no d-neighbour), fills in one more swap: **a second shortest sequence of length 3, beginning with Y**. Y is disjoint from path A = 7-14-19-12-3-2 (so strictly inside D1(A), and both locks survive via A) but contains 10, which lies on path B = 7-14-19-18-10-2 (so not inside D1(B)). So this is a second instance of the sage's claim failing, path-dependent in exactly the way {11} is, and it is my mechanism after all; it fails Q-all.

## 5. Could the mechanism occur when K1 is a tree (so Q-exists = Q-all)? [hand, conditional]
Yes, in principle. The vertex n after w2 in x3's rotation is adjacent to w2 and to x3, so n is a or b. If x3 has degree 5, n = w3 and must be x3's b-neighbour (lock 1 needs one among w2,w3), so n lies on every lock-1 path and in Y: impossible. **So the mechanism needs deg x3 >= 6.** For Q-all (every path) it suffices that n is either a, or b and off every simple lock-1 path. In 20/51/1, n = 10 is b and on path B because 10's other {b,g}-neighbour 18 (colour g) links to 19; if 18 were not g, 10 would be a pendant b hanging from x3, K1 would be a tree, and Y = {9,10} would satisfy Q-all (but not Q-chain, since 10 is in K1).
For **Q-chain** the instance needs: x2 degree 5, w1 = g, w2 = d, deg x3 >= 6 with the neighbour n after w2 equal to a, lock 1 entering x3 elsewhere (w3 or a later m), Y = {b,d}-component of w2 disjoint from K1 and not K2, and radius exactly 3 (no 2-sequence). I do not have such a state. Candidate pattern classes (HP ring strings with w1 = g, w2 = d and deg x3 >= 6): dgdbg at S containing 3 (for example O3 with m3 = a) and gdb... only those; the pairs {3,4} classes E1/E2 have radius <= 2 (E2: m3 = b = n forced, so Y meets lock 1).

## 6. Self-check, two weakest points
1. Section 4 reads adjacency from the plantri string by hand (letters a..t = 0..19, 20 strings); I rechecked the neighbourhoods of 8, 9, 10 and 2 once, but an off-by-one in one letter would change Y.
2. In section 3 I treat F's image as having no d-neighbour at x2 using only x2's five neighbours; this needs x2's degree to be exactly 5 and that F does not recolour w2 (w2 is b after Y, and F recolours only a/g vertices), which I checked.
