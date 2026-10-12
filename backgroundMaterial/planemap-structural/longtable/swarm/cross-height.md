# Height functions, pushed onto a hole and then killed

4 October 2026. Seed: Thurston heights, Conway–Lagarias heights, and the integer lift of a 3-colouring. Variability seed 17 fixes the long lozenge step, difference \(-2\), and prefers the balanced witness at order 17, graph 3, when a population is already flat. No colouring search was run. Nothing here is a proof of the Four Colour Theorem.

The foreign objects are these.

- Thurston's height (Amer. Math. Monthly 97 (1990), 757–773). On a simply connected region of the triangular lattice, a lozenge tiling is an integer function \(h\) with \(h \equiv \chi \pmod{3}\), where \(\chi\) is the lattice's proper 3-colouring. Along an edge whose colour increases by \(1 \pmod{3}\), the step lies in \(\{+1,-2\}\). A local flip changes the volume by 3. The same integer is the dimer height on the dual hexagonal lattice, which is bipartite precisely because every primal degree is 6.
- Conway–Lagarias (J. Combin. Theory Ser. A 53 (1990), 183–208). The boundary word of a region is an element of the tiling group. Its abelian image is the height. Every legal tile preserves that image. A region whose image misses the image of a completed tiling cannot be tiled by those tiles.
- The 3-colouring lift itself. A spherical triangulation admits a proper 3-colouring if and only if it is Eulerian (Heawood). Fisk (1973) then puts all of its 4-colourings in one Kempe class. Both statements stop at odd degrees. On \(G_n\) the odd degrees are the \(2n\) vertices of degree 5.

The pair in each mapping is a vertex hole together with a proper 4-colouring of the rest. The charge barrier is the one the sweeps hit: a singleton slide preserves the sorted colour counts; on Florek's \(G_8\) the deletion counts \((2,5,5,5)\) never fill, because every full 4-colouring has counts \((4,4,5,5)\) (arXiv:2511.00485, Lemmas 2.2–2.3); the equal-pole star swap is the move that changes the counts.

## 1. The abelian tiling height is the colour count

**Foreign object.** The abelian image of a Conway–Lagarias boundary word: the exponent sum that every tile preserves.

**On a pair.** The sorted 4-tuple of colour counts on the coloured vertices.

**Barrier.** The conserved charge.

**Death.** Two published states kill it in the two directions a height would have to work.

On the equal-pole colouring of \(G_8-u_0\), the tuple is \((2,5,5,5)\). Slides preserve it, and the 32-state slide component never fills (`swarm/unequal-poles.md`, `SwarmConsolidation.md`). The star swap of `TwoPoleStarEscape.md` changes it, through \((3,4,5,5)\), to a completed \((4,4,5,5)\). A Conway–Lagarias tile has to preserve the abelian height. The move that completes the colouring does not, so the star swap is not a tile and the count is not a tiling obstruction to extension. It is only the slide invariant already named in the charge barrier.

Off that graph the same integer is already minimal and still not a fill. Order 17, graph 3, root 3, colouring 44 has sorted population \((4,4,4,4)\). Every legal slide preserves it, and all eight Kempe successors preserve it (`swarm/rank-kill.md`). The state is not a target. A height that is a function of the sorted counts does not fall there.

## 2. Thurston's volume, with a slide as a flip

**Foreign object.** The volume \(\sum h\). While a local maximum exists, flip it. Each flip drops the volume by 3, and the minimal section is the flat lift of \(\chi\).

**On a pair.** Declare the 4-colouring to be a lift of a 3-colouring, and declare a singleton slide, or a one-vertex recolour, to be the flip.

**Barrier.** Reversible moves with no Lyapunov function.

**Death.** The identification fails on both sides of Heawood's line.

Where the lift exists, the local move does not. A 3-colourable spherical triangulation is Eulerian, so it has no degree-5 hole at all. Ito, Iwamasa, Kobayashi, Maezawa, Nozaki, Okamoto, and Ozeki (arXiv:2210.17105) produce a 4-colouring of such a triangulation that admits no one-vertex recolour, while Fisk's theorem still joins it to a 3-colouring by larger Kempe chains. Thurston's flip is one of those larger moves. The vacancy calculus does not have it, and there is no degree-5 vacancy to slide.

Where the charge lives, the descent points into the trap. On the equal-pole colouring of \(G_8-u_0\) the belt is periodic of period 3 in the three non-pole colours (`unequal-poles.md`). That is the flat section: every zigzag step is the same residue mod 3, and the long-step height \(\widetilde H\) defined in mapping 5 is already 0. The star swap is what leaves this section. It replaces three belt vertices of colour 3 by colour 0, so it changes the colouring mod 3. A lozenge flip preserves \(h \pmod{3}\). The repairing move is not a flip, and the minimal section is the unfilled component.

## 3. Cone curvature forces the pentagon bridge

**Foreign object.** In an equilateral triangulation a vertex of degree \(d\) has curvature \((6-d)\pi/3\). Degree 5 is a cone point of angle \(\pi/3\). The developing map fails to close by that angle.

**On a pair.** The hole is the cone point. The curvature, or the rotational holonomy of the developing map, is taken to be the obstruction that forces a second slide onto a far pentagon.

**Barrier.** The pentagon with no forward exit.

**Death.** Curvature does not read the colouring. The 15-vertex pentagon star of `swarm/isolated-local.md` has the same degrees in every colouring. Exhibit A colours it by
\[
\gamma(m)=(0,1,0,2,3),\qquad \gamma(p)=(1,0,1,0,0),\qquad \gamma(q)=(2,2,3,1,2)
\]
and every second slide onto a far pentagon is illegal. Of the \(13200\) colourings of that star with boundary type \(2,1,1,1\), \(6360\) have every far pentagon illegal and the rest do not. The cone angle is the same in both classes. The same kill, with a different orbit of degree-5 vertices, is the pentakis colouring in that note. Geometry does not force the bridge; that is the barrier, and the developing map is colour-blind, so it cannot attack it.

## 4. One puncture makes the dimer height single-valued

**Foreign object.** The integer height of a perfect matching on the hexagonal lattice, equivalently \(h\equiv\chi\pmod{3}\) on the dual Eulerian triangulation. The construction needs a bipartite dual, so that a black-to-white orientation exists and the height closes around every face.

**On a pair.** Take a 4-colouring of \(G_n-h\), read it as Tait data on the dual, delete the one pentagon that belonged to the hole, and ask for Thurston's height on what remains.

**Barrier.** The charge, read as a defect of Fisk's hypothesis at the degree-5 vertices.

**Death.** One hole does not clear the odd degrees. In \(G_8-u_0\) the degrees are: \(a\) has degree 7; \(u_2,u_3,u_4,u_5,u_6\) and \(v_1,\ldots,v_6\) have degree 5; \(b\) has degree 8 and \(u_1,u_7,v_0,v_7\) have degree 4. That is 12 odd-degree vertices. An interior vertex of odd degree still forbids a proper 3-colouring, so there is no \(\chi\) to lift, on the pair that carries the population \((2,5,5,5)\). Fisk's theorem is the case where the height does exist. Deleting one belt vertex does not reach that case. The same count shows the dual is not bipartite, so the dimer orientation is not defined either.

A boundary-only shadow dies for a different published reason. Every proper 4-colouring of a 5-cycle of type \(2,1,1,1\) is one orbit under dihedral symmetry and permutation of the colours: the repeated colour sits at distance 2, and the other three colours are distinct. The equal-pole link \((0,1,2,3,1)\) and the unequal link \((0,1,2,3,2)\) are the same orbit. The first never fills by slides. The second fills by \(u_0\to v_7\to v_6\to u_6\to u_5\) (`unequal-poles.md`). A height that is a function of the boundary word cannot tell them apart. Conway–Lagarias can, only because their word is the shape of the region. Here the shape is the same and the colouring is not.

## 5. The long lozenge step along the zigzag

**Foreign object.** The step set \(\{+1,-2\}\) from Thurston's lozenge height. Seed 17 selects the long step: \(17\equiv 2\pmod{3}\).

**On a pair.** Let \(Z=(u_0,v_0,u_1,v_1,\ldots,u_{n-1},v_{n-1})\) be the zigzag cycle of the belt; its edges are \(u_i v_i\), \(v_i u_{i+1}\), and \(v_{n-1}u_0\). For a belt hole, sum along the path \(Z\) minus the hole. For colours in \(\{0,1,2,3\}\),
\[
\beta(x,y)=\begin{cases}
+1 & \text{if }(y-x)\equiv 1\pmod{4},\\
-2 & \text{otherwise.}
\end{cases}
\]
Set \(\widetilde H=3\) times the number of steps with difference \(1\pmod{4}\). This is the excess of the path over the pure long-step section. The label-invariant version is the minimum of \(\widetilde H\) over the \(24\) renamings of the colours.

**Barrier.** The charge on \(G_8\), and the missing Lyapunov on a slide component.

**Death.** The label-invariant height is already 0 on a non-target state that slides can still finish.

Start from the unequal \(n=8\) colouring in `unequal-poles.md`, then swap colour names \(0\) and \(1\). Poles are \(a=1\), \(b=0\), and the belt is

| \(u_1\) | \(u_2\) | \(u_3\) | \(u_4\) | \(u_5\) | \(u_6\) | \(u_7\) | \(v_0\) | \(v_1\) | \(v_2\) | \(v_3\) | \(v_4\) | \(v_5\) | \(v_6\) | \(v_7\) |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 2 | 0 | 2 | 0 | 3 | 2 | 2 | 3 | 1 | 3 | 1 | 2 | 1 | 3 |

The published walk remains legal, because a global renaming preserves properness and uniqueness on a link. After \(u_0\to v_7\to v_6\to u_6\), the hole is \(u_6\), \(u_0=3\), \(v_7=1\), \(v_6=3\). The zigzag path from \(v_6\) to \(v_5\) has colours
\[
(3,2,1,3,2,0,3,2,1,0,3,2,1,0,2).
\]
Every one of the 14 steps has difference \(2\) or \(3\pmod{4}\), so \(\widetilde H=0\). The minimum over renamings is therefore 0 as well. The link of \(u_6\) is \((a,u_5,u_7,v_5,v_6)\) with colours \((1,0,2,2,3)\), all four colours. The state does not fill. No slide can make \(\widetilde H\) negative. Strict descent stops one legal slide before the published fill: the next step \(u_6\to u_5\) keeps \(\widetilde H=0\) and the walk then colours \(u_5\) with 3.

The same formula misses the charge repair in the other direction. On the equal-pole colouring the zigzag is \((2,1,3)\) five times, every step is long, and \(\widetilde H=0\). Swapping colours 0 and 3 on \(\{b,v_1,v_4,v_7\}\) leaves another all-long path, so \(\widetilde H\) stays 0 while the population leaves \((2,5,5,5)\).

The face-valued twin dies on the same colouring, with the wrong inequality. A completed triangle omits one colour in \(\{0,1,2,3\}\). On \(G_8-u_0\) with the equal-pole colouring, the 27 complete faces omit colours with counts \((13,6,4,4)\), sorted \((4,4,6,13)\). The three legal slides do not all respect a descent toward a fill:

- the slides to \(v_0\) and to \(v_7\) keep the sorted tuple \((4,4,6,13)\);
- the slide to the pole \(a\) replaces it by \((3,3,5,13)\), which is lexicographically smaller, and does not fill;
- the star swap replaces it by \((4,6,8,9)\), which is lexicographically larger, and does fill.

Descent of the sorted omission tuple prefers the pole slide. The notes already record that a slide onto a pole keeps the bad population. The filling move is an ascent.

What looked like a slide invariant inside this tuple is the count of faces that omit the common pole colour. It equals 13 on the equal-pole component, for a counting reason and not a new constraint. Poles have colour \(A\), so every cap contains \(A\). Every complete belt triangle then omits \(A\) exactly when none of its vertices is coloured \(A\). In this component the only \(A\)-coloured vertices are the two poles, or one pole and a single belt vertex while the other pole is the hole, and the count is \(2n-3=13\) throughout. The star swap drops it to 8 by putting \(A\) on three belt vertices. That is the population change again. It is constant on the 32 states where a Lyapunov would have to choose a slide, and it is no finer than the charge killed in mapping 1.

## Verdict

KILL ALL.

Every integer tried here is one of: undefined on \(G_8-u_0\) because a 3-colouring lift needs even degrees (mappings 2 and 4, Heawood and Fisk); colour-blind, hence constant on Exhibit A (mapping 3); a function of the sorted colour count, hence frozen on colouring 44 and on the 32-state component (mappings 1 and the omission count); or defined, and pointing the wrong way on a published \(G_8\) colouring (mapping 5). The star swap changes colours mod 3, so it is not a lozenge flip. The flat section of the belt is the unfilled equal-pole state, not a state one should descend toward.

Feasibility that some further height, not a function of the sorted population and not one of these five, falls under the star swap and orients slides on a pair \((h,c)\): **Low**. The equal-pole repair is already one explicit Kempe swap, and the natural lifts do not see it.

Next step: do not score another mod-4 sum on the zigzag. A later calculation only repeats mapping 5.
