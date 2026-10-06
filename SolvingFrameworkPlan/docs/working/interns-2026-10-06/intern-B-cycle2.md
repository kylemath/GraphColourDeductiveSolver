# Intern B, cycle 2: ring-3 anatomy of the radius-5 state (graph 91a307d1..., hole 22)

Hand only. I read `91a307d1852a1764.graph.json` and `.hole22.state.json` (cert/ directory) and worked out neighbourhoods and colours by scanning the 52 faces. Nothing run. Labels [hand]; the radius 5 itself is Studio intel's [computed] claim, not rechecked.

## 1. The state in my frame
Link of 22 (faces [21,22,20], [22,25,20], [11,25,22], [14,11,22], [21,14,22]): x0..x4 = 21, 20, 25, 11, 14, colours 2, 0, 2, 3, 1. So a=2 (repeated at 21 and 25), b=0 (middle 20), g=3 (11), d=1 (14): the frame (a,b,a,g,d) in the counter-clockwise rotation.
Degrees: 21:5 (nbrs 22,20,15,13,14), 25:5 (12,23,20,11,22), 11:5 (3,12,25,22,14); **20:6** (nbrs 22,21,15,19,23,25) and **14:6** (13,4,11,22,21,3). Free pair {x1,x4} = P4 (the mirror reading is Studio's P1).
Ring: w0=15 (d), w1=23 (g), w2=12 (d), w3=3 (b), w4=13 (g): pattern **dgdbg**, as Studio says.
The two m-neighbours: m(x1) = **19**, between w0=15 and w1=23 in the rotation at 20; m(x4) = **4**, between w3=3 and w4=13 at 14. Colours: 19 -> 2 = **a**; 4 -> 2 = **a**.

## 2. Why both m are a, forced by colours
x1 is b with outer ring colours d, g, so its extra neighbour m must avoid b,d,g and is a. x4 is d with outer w3=b, w4=g, so m is again a. The same holds for any free vertex in dgdbg at any position: x3 (g, outer d,b) gives m = a; x0 or x2 (a, outer g,d) give m = b. **In dgdbg every extra neighbour of a free vertex is coloured a or b, whatever the graph.**

## 3. Why HP's kills fail here
- F-starvation needs x2 (25) to have no d neighbour: it has w2=12 (d). Fails.
- B-starvation needs x0 (21) to have no g neighbour: it has w4=13 (g). Fails.
- AB: C = the {a,b}-component of x1 (colours 2,0) in T minus 22. It contains the triple 20,21,25 and, through the free x1, the a-vertex 19. It continues 19 - 24 and 26 (both b) - 18 and 9 (a) - 7, 6, 3 (b). So C reaches **w3 = 3** by the alternating path 20 (b), 19 (a), 26 (b), 9 (a), 3 (b), four edges, and also contains 4 (a, adjacent to 3, the m of x4).
- Hence after AB the vertex 3 turns a, so x3 (11) has the a-neighbour 3 (and x4 has 3 as well): the new locks are not starved. HP's AB kill, which needs the singleton to have no a-neighbour after the swap, fails because of the leak, exactly the "hub that joins chains" mechanism.
Side of the lock curves: both locks use w3. The only b-neighbour of x3 is 3 and the only b-neighbour of x4 is 3, so P1 and P2 both end through 3. I find P1 = 20,23,26,10,6,0,3,11 (b,g alternating, edges checked); P2 starts 20-15 (the only d-neighbour of 20). At x1 the rotation is 22(v),21,15,19,23,25: the lock exits are 15 (P2) and 23 (P1), and 19 lies in the wedge between them, i.e. on the side of the closed curve P1 + x3x4 + P2 that contains the face outside edge x3x4 (where w3 lies), not on the side of v, x0, x2. The leak path runs along P1 (it shares b-vertices 20, 26, 3 with P1) through the a-vertices 19 and 9, which are not on P1.

## 4. The precise ring-3 condition for the AB repair
Take R3 (dgdbg). After AB the new frame has middle a and repeated b; the new locks need an a-neighbour at x3 and at x4. The old a-neighbours of x3, x4 (x2, x0) are in C and turn b; the new a-neighbours are the old b-neighbours that lie in C. For a singleton s of degree 5 (neighbours x_{s-1}, x_{s+1}, w_{s-1}, w_s), the only candidate is w3 (b), and x3's and x4's other neighbours are g/d or in C. So:

**Condition AB*:** some degree-5 singleton s in {x3,x4} exists (true for every position of the pair) and **w3 is not in the {a,b}-component of x1 in T-v**. If AB* holds, the AB swap gives a non-DL state and radius <= 2 at this state (for s = x4 free as here, x4's own m = a outside C would also be an a-neighbour, so use s = x3).
Equivalently: no alternating a/b path from x1 to w3 through the m's of the free vertices in {x0,x1,x2} (the only exits of the triple: the other ring vertices have colours g or d, as the ring is d,g,d,b,g, and the only a/b outer neighbours of x0,x1,x2 are their m's, forced a or b by section 2, and w0..w2 are d,g,d).

**This state violates AB*:** path 20-19-26-9-3 puts w3 in C. Because section 2 forces the m's to be a/b, the leak cannot be excluded by local colours, so AB* is a genuine ring-3 (distance-4 path) condition, exactly as I guessed in cycle 1. The radius-5 state is a state where the {a,b}-component of x1 reaches w3, and the 5-swap path must then be taken through F and B chains in the closed set.

## 5. Self-check, two weakest points
1. I identified P1 by hand (b/g alternation and edge membership) but did not prove it is the lock path used in the certificate; any {b,g}-path suffices for the argument, and the claim that both locks end through 3 is forced (3 is the unique b-neighbour of 11 and of 14), so this is secure; the picture "leak runs along P1" is only illustrative.
2. The C computation scanned face lists by eye; one missed adjacency could change membership of C, but 3 in C needs only the single path 20-19-26-9-3, whose five edges (faces [23,19,20], [26,19,23], [9,10,26]/[12,9,26], [3,9,12]/[3,2,9]) I re-read: 19-26 (face [26,19,23]), 26-9 (face [9,10,26]), 9-3 (face [3,2,9]) and 20-19 (face [23,19,20]).
