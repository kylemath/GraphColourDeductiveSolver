# D1 by hand: the rigid, triply locked case

Long Table (D1-Hand team), 5 October 2026. EXPLORATORY, post hoc, undeclared. Orders <= 17 only (the two graphs 17:0, 17:1 of `plantri -m5 17`, index in plantri output order). Nothing was staged or committed. Labels: [hand] = every step written out below; [data] = computed, exploratory; [lead] = plausible, not proved; [conjecture].

Scripts (all in `backgroundMaterial/planemap-structural/longtable/explore-vhphi/`, run as `python3 d1hand_X.py $P ...` with `P` the plantri 5.8 binary): `d1hand_swaps.py` (all single swaps of a SEP-bad state), `d1hand_fan.py` (first-order chain test of each neighbour), `d1hand_path.py` (shortest Kempe sequence in G), `d1hand_pure.py` (pure distance to fill), `d1hand_table.py` and `d1hand_states.py` (census of all 192 locked members / 128 locked states), `d1hand_identity.py` (checks I1, I2 below on 1,484 arbitrary colourings, 0 failures), `d1hand_lib.py` (helper).

## 0. Result in six lines

1. [hand] First-order lock conditions at a degree-5 hole reduce to two path conditions, P13 and P14 (section 2).
2. [hand] A Jordan argument turns them into two forced splits of colour pairs of T-x, and a Euler/degree identity (I2) makes the class degree-excess an exact function of class size and component structure (section 3).
3. [hand] If a state is locked for all three admitting fans and every chain is full ("rigid"), all six bichromatic subgraphs of T-x are forests, the component vector is forced to (1,2,2,1,1,1), the class sizes obey n_i <= (n-4)/3 (n_alpha <= (n-3)/3), and at n = 17 the colouring is forced to be (4,4,4,4) with degree-excess (1,2,1,1). This proves the equitability observed at order 17 for triply locked rigid states, and shows no such state exists at n = 12, 14, 15 (section 4).
4. [hand] The one-swap neighbourhood of a rigid triply locked state is exactly two states, nu_gamma and nu_beta, and in each only one fan (the apex u0, resp. u2) can be unlocked. D1 for the state is therefore equivalent to a single statement about those two neighbours (section 5).
5. [data] The statement holds in all 8 SEP-bad states, but the unlock is invisible at the chain level: each unlocked neighbour is first-order locked at the unlocking fan and needs Kempe distance exactly 4 in G. [hand] The counting identities do not contradict "both neighbours locked" (section 6).
6. Negative result: nothing local (Jordan, forests, degree counting) reaches distance 4. D1 for all minimum-degree-5 T implies the Four Colour Theorem, so a proof needs a global input (section 7).

## 1. Notation

State = proper 4-colouring c of T-x whose ring uses 4 colours. A 5-letter ring word has exactly one repeated colour, at two ring positions at distance 2. Rotate the ring so that

- u0, u2 carry the doubled colour D;
- u1 (between them) carries alpha, the middle singleton, role M;
- u3 carries beta, role L (adjacent to u2);
- u4 carries gamma, role R (adjacent to u0).

So the word is D a D b g (letters D, a = alpha, b = beta, g = gamma). Fans admitting c have apex at the three singletons u1, u3, u4. The chords of fan u1 are u1u3, u1u4; of fan u3 are u3u0, u3u1; of fan u4 are u4u1, u4u2. The "pair subgraph [p,q]" always means the subgraph of T-x induced on the vertices coloured p or q. For a fan with apex y in colour s, G = T - xy with x coloured s. Chain {s,k} = component of x in G[s,k].

For any state: n_i = |V_i|, r_i = number of ring vertices in V_i (r_D = 2, others 1), exc_i = sum over V_i of (deg_T v - 5) >= 0 (min degree 5), comps_pq and cyc_pq = number of components and cyclomatic number of [p,q], delta_pq = comps_pq - cyc_pq, kappa_i = sum over j != i of delta_ij.

## 2. First-order lock conditions [hand]

**Proposition 1.** Let c be a state with word D a D b g and fan apex y. The chain {c(y),k} joins x to y in G iff the component of y in [c(y),k] contains a ring vertex of colour k.

Proof. In G, x has colour s = c(y) and is adjacent to the four ring vertices other than y; the only ones of colour k are the ring vertices coloured k. The chain of x in {s,k} is x together with the components of [s,k] containing such a ring vertex. It contains y iff the component of y contains one. QED

Applying this with the ring adjacencies (u0u1, u1u2, u2u3, u3u4, u4u0 are edges):

- Apex u1 (colour alpha): {alpha,D} is automatic (u1 is adjacent to u0 and u2); {alpha,beta} needs P13; {alpha,gamma} needs P14.
- Apex u3 (beta): {beta,D} automatic (u3 ~ u2), {beta,gamma} automatic (u3 ~ u4), {beta,alpha} needs P13.
- Apex u4 (gamma): {gamma,D} automatic (u4 ~ u0), {gamma,beta} automatic, {gamma,alpha} needs P14.

Here P13 means "u1 and u3 are joined in the pair subgraph [alpha,beta] of T-x", and P14 means "u1 and u4 are joined in [alpha,gamma]". If a needed condition fails, the single swap of x's chain component in G gives c(x) != c(y), so the state is separable for that fan. So fan M is first-order locked iff P13 and P14; fan L iff P13; fan R iff P14. In particular first-order locks for L and R together imply the one for M. [data] At the class level the same holds: of the 128 states with a locked fan, the locked sets are exactly {L}, {R}, {M}, {L,M}, {M,R}, {L,M,R} (counts 32, 32, 8, 24, 24, 8); {L,R} without M never occurs.

## 3. Splits, and two identities [hand]

**Proposition 2 (Jordan splits).** If P13 holds, u2 lies in a different component of [D,gamma] than u0 and u4. If P14 holds, u0 lies in a different component of [D,beta] than u2 and u3.

Proof. Let P be a path in [alpha,beta] from u1 to u3 and Z the closed curve x u1 P u3 x (a simple closed curve in the sphere). At x the ring is cyclically ordered u0..u4, so the edges xu2 and (xu4, xu0) leave x on opposite sides of Z, and u2, u4, u0 do not lie on Z (their colours are D and gamma, those of P are alpha and beta). A path in T-x with colours D, gamma avoids all vertices of Z, hence cannot cross Z, so it cannot join u2 to u0 or u4. The second statement is the mirror image with the path in [alpha,gamma] and u0 against u2, u3. QED

So a state locked at fans L and R (or at M) has [D,gamma] split as u2 | u0u4 and [D,beta] split as u0 | u2u3. These are exactly the pieces that x holds together in the chains {gamma,D} of fan R and {beta,D} of fan L: the chain is x plus the component of u0 (resp. u2) plus the other component.

**Identity I1.** For every proper 4-colouring of T-x, sum over the six pairs of delta_pq = 8. Proof: T-x has n-1 vertices and 3n-11 edges, and each edge lies in exactly one pair subgraph, so 3n-11 = sum (n_p + n_q - comps_pq + cyc_pq) = 3(n-1) - sum comps + sum cyc. QED

**Identity I2.** For every class i: exc_i = (n-1) + r_i - 3 n_i - kappa_i. Proof: sum of degrees in T-x over V_i is sum over j != i of e_ij = sum (n_i + n_j - comps_ij + cyc_ij) = 2 n_i + (n-1) - kappa_i; the T-degree of a ring vertex is one more than in T-x, so exc_i = (sum of T-x degrees) - 5 n_i + r_i. QED (I1 and I2 also verified numerically on 1,484 arbitrary colourings of T-x, 0 failures.) Min degree 5 enters only as exc_i >= 0.

## 4. The rigid triply locked case [hand]

Call a state **rigid triply locked** if it is locked for the three fans u1, u3, u4 (all legal) and in each of them every chain {c(y),k} is the full colour pair plus x. (In the data, 4 of the 8 SEP-bad states are of this kind: the four on 17:1.)

**Lemma F (lock-counting.md, accepted).** If a chain {1,k} through x and y is full, the pair of the other two colours induces a forest in T-x.

**Proposition 3.** In a rigid triply locked state all six pair subgraphs of T-x are forests, delta = comps, and (comps_Da, comps_Db, comps_Dg, comps_ab, comps_ag, comps_bg) = (1,2,2,1,1,1). Hence kappa_D = 5, kappa_alpha = 3, kappa_beta = kappa_gamma = 4 and

- exc_D = n - 4 - 3 n_D, exc_beta = n - 4 - 3 n_beta, exc_gamma = n - 4 - 3 n_gamma, exc_alpha = n - 3 - 3 n_alpha.

Proof. Fan u1 gives forests {beta,gamma}, {D,gamma}, {D,beta} (complements of {alpha,D}, {alpha,beta}, {alpha,gamma}); fan u3 gives {D,gamma}, {D,alpha}, {alpha,gamma}; fan u4 gives {D,beta}, {D,alpha}, {alpha,beta}. Together all six pairs. For forests, I1 reads sum comps = 8; Proposition 2 gives comps_Db >= 2 and comps_Dg >= 2, all others >= 1, so the minimum 8 is attained and every inequality is an equality. The formulas follow from I2 with r_D = 2, r_alpha = r_beta = r_gamma = 1. QED

**Corollary.** exc_i >= 0 gives n_D, n_beta, n_gamma <= (n-4)/3 and n_alpha <= (n-3)/3. With n_D + n_alpha + n_beta + n_gamma = n-1 the floors give: a rigid triply locked state needs 3 floor((n-4)/3) + floor((n-3)/3) >= n-1.

| n | n-1 | maximum total | verdict |
|---|---|---|---|
| 12 | 11 | 9 | impossible |
| 14 | 13 | 12 | impossible |
| 15 | 14 | 13 | impossible |
| 16 | 15 | 16 | slack 1 |
| 17 | 16 | 16 | slack 0: sizes forced (4,4,4,4), excess (D,a,b,g) = (1,2,1,1) |
| 18 | 17 | 17 | slack 0: sizes forced (4,5,4,4) for (D,a,b,g) |
| 19 | 18 | 20 | slack 2 |

[hand for the arithmetic; the min-degree-5 families have no graph at 13.] [data] The four rigid triply locked states on 17:1 have sizes (4,4,4,4) and excess exactly (1,2,1,1); the counting team's equitability pattern and the data at 12, 14, 15, 16, 18 (no rigid triply locked state) agree. The order-17 equitability is therefore a corollary of the three fans being locked simultaneously, not of a single chain. It is **not** a balance theorem: for n >= 19 the caps no longer force balance.

[lead] A rigid triply locked state is an acyclic 4-colouring of the disc T-x in which four colour pairs are spanning trees and two pairs have exactly two components. I have not searched the literature on acyclic colourings of triangulations for this.

## 5. The one-swap neighbourhood [hand]

**Proposition 4.** Let c' be obtained from a state c by swapping a component K of a pair subgraph [p,q] of T-x. Then every fan of c whose apex colour s is not in {p,q} is still admitting in c' and still locked, because K is a component of G[p,q] (x is not in G[p,q] when s is not in {p,q}), so c' lies in the same Kempe class of G as c. Likewise a swap of a component containing no ring vertex is a G-swap for every fan.

**Proposition 5 (neighbourhood of a rigid triply locked state).** Up to renaming colours, the pure one-swap neighbours of c that differ from c are exactly nu_gamma c (swap the component of u2 in [D,gamma]) and nu_beta c (swap the component of u0 in [D,beta]). In nu_gamma c the only fan that can be unlocked is the one at u0 (colour D), and in nu_beta c it is the one at u2. Both fans are legal.

Proof. By Proposition 3 the pairs [D,alpha], [alpha,beta], [alpha,gamma], [beta,gamma] are connected, so swapping their only component transposes two colours globally and gives c up to renaming. [D,beta] has the two components K0 (containing u0) and K23 (containing u2, u3); [D,gamma] has K2 (containing u2) and K04 (containing u0, u4). Swapping K0 or K23 gives the same state up to renaming (they differ by the global transposition), likewise K2 or K04. For nu_gamma c (swap K2: word D a g b g) the doubled colour is gamma, the singletons are u0 (D), u1 (alpha), u3 (beta); the fans at u1 and u3 have apex colours outside {D,gamma}, so by Proposition 4 they stay locked. Only u0 can be unlocked; the fan at u4 is no longer admitting. The case nu_beta is the mirror image (reverse the ring: u0 <-> u2, u3 <-> u4). Legality: the chords of fan u0 are u0u2 (monochromatic in c, not an edge) and u0u3, which is also a chord of the legal fan u3; the chords of fan u2 are u2u0 and u2u4, and u2u4 is a chord of the legal fan u4. QED

(Legality is automatic in a 4-connected T: a chord u_i u_{i+2} would make x u_i u_{i+2} a separating triangle.)

**Consequence.** D1 for a rigid triply locked state, with the depth-1 clause, is equivalent to: at least one of nu_gamma c (fan u0) and nu_beta c (fan u2) is separable (or the neighbour is itself one swap from a separable state, which is the weaker D1 clause already counted at depth 1).

**Proposition 6.** In the unlocked-or-not question for c' = nu_gamma c there is a cycle: c' has a cycle in [alpha,gamma] or in [alpha,D] (relabelled colours as in c).

Proof. c' is in the G-class of c for the fan u3, which is locked, so c' has its chains. In c' the ring word is D a g b g; the middle singleton is u3 (beta), the doubled colour gamma. By Proposition 1, P'13 (u3 ~ u0 in [beta,D]) and P'14 (u3 ~ u1 in [beta,alpha]) hold in c'. Proposition 2 applied to c' gives that [gamma,alpha] has at least 2 components, so comps'_{alpha gamma} >= 2. Because V_alpha, V_beta are unchanged and r_alpha = 1, the class identity I2 gives kappa'_alpha = kappa_alpha = 3. Since [alpha,beta] is unchanged, delta'_{alpha beta} = 1, so delta'_{alpha D} + delta'_{alpha gamma} = 2, hence cyc'_{alpha gamma} + cyc'_{alpha D} = comps'_{alpha gamma} + comps'_{alpha D} - 2 >= 2 + 1 - 2 = 1. QED

In particular c' is never rigid triply locked (also directly: the class V_beta would need exc_beta = n-3-3n_beta as the middle class, against n-4-3n_beta from c). So the only way both neighbours stay locked is that both are of the non-rigid kind of section 8.

## 6. What the data say about the escape [data]

All eight SEP-bad states (17:0 vertices 4 and 6, 17:1 vertices 5 and 15, two states each).

- Structure. Word D a D b g in all eight. Four (all of 17:1) are rigid triply locked, with comps = (1,2,2,1,1,1) for (Da,Db,Dg,ab,ag,bg); four (all of 17:0) are non-rigid, section 8. The component sizes of the split pairs are (4,4) or (2,6) for the two pieces.
- Neighbourhood. In the four 17:1 states the only non-trivial pure neighbours are nu_beta and nu_gamma, as Proposition 5 says. Both are separable, for the predicted fan (u2 after nu_beta, u0 after nu_gamma) in all 8 of 8 states, 16 of 16 neighbours.
- No chain-level signal. In all 16 unlocked neighbours every chain {c(y),k} of the unlocking fan still joins x to y (script `d1hand_fan.py` reports no broken chain at any admitting fan). So the escape is not visible at first order.
- Kempe distance. The shortest sequence in G for the unlocking fan has length exactly 4, three swaps that avoid x followed by one that contains x or y, in all 16 cases. The three preparatory swaps involve ring vertices on both sides of the splits. I could not find a pattern in them; BFS paths are not unique.
- Pure distance. The state itself is at pure distance 4 from a filled state in all 8 cases; its neighbours are at 3 or 4 (an unlocked neighbour at pure distance 4 exists, so unlockedness of the neighbour does not mean the neighbour is nearer to a fill).

## 7. Task 1 verdict: what a proof needs

**What is proved.** Proposition 5 and 6 reduce D1 in the rigid triply locked case to one statement:

> (N) In a rigid triply locked state of a minimum-degree-5 triangulation, nu_gamma c is separable for the fan at u0, or nu_beta c is separable for the fan at u2.

**Exact obstruction.** Everything provable by Jordan separation, forests and degree counting is satisfied by a hypothetical counterexample to (N):

- c' = nu_gamma c is first-order locked at u0 (data: all 16 cases), and the same Jordan argument as in Proposition 2 applied to c' only forces a cycle (Proposition 6);
- the identities I1, I2 for c' are consistent: delta'_{D gamma} = 2 (the pair [D,gamma] has the same subgraph), kappa'_beta = 4, kappa'_alpha = 3, none of which conflicts with any bound;
- non-rigid triply locked states exist in the data (the four on 17:0), so "c' is triply locked but non-rigid" is not excluded.

The unlock is a statement that the G-Kempe class of c' at u0 reaches c(x) != c(u0), and the shortest witnesses need three preparatory swaps. Chain connectivity (first order) cannot see it; a Jordan lemma would have to be proved at third order. I have no such lemma.

**Global facts a proof would need, stated but not proved:**

1. (G1) the colour-pair structure at depth 3: the G-class of c' at u0 contains a colouring with a broken chain {D,beta} or {D,gamma} or {D,alpha} (Proposition 1 shows these are the only chains that can break, and only the {D,beta} chain can, since the others are automatic at the L-type apex u0). That is, an explicit Kempe change in G that cuts the single path u3 ~ u0 of [beta,D].
2. (G2) a reason that the three preparatory swaps exist, for instance a short list of "cutting" pairs; the data show them as swaps of four- or six-vertex pieces.
3. (G3) no use of 4-connectivity or degree >= 5 beyond legality (4-connectivity) and exc >= 0; the counting side cannot be tightened with these alone because for n >= 19 the caps give slack.

## 8. Task 2: the non-rigid locked members [data, with hand parts]

**Census (script `d1hand_states.py`).** 192 locked members, 128 states with at least one locked fan, by locked set (in letters of the roles):

| locked set | states |
|---|---|
| L only / R only / M only | 32 / 32 / 8 |
| L+M / M+R | 24 / 24 |
| L+M+R | 8 |

**The 28 non-rigid members are exactly 28 M-members** (apex alpha, the middle singleton): the 24 M-members of the states locked at {L,M} or {M,R} plus the 4 M-members of the triply locked 17:0 states. In each of these states:

- the M chains {alpha,beta} and {alpha,gamma} are full, the chain {alpha,D} is **not** full;
- [beta,gamma] has exactly one independent cycle (cyc = 1, comps = 1) and every other pair is a forest;
- comps = (2,2,2,1,1,1) for (Da,Db,Dg,ab,ag,bg): [D,alpha] has one extra, ring-free component beside the one through u0,u1,u2;
- the L and R members of the same state (when locked) are rigid.

**[hand] Why one cycle and one extra component.** Let C be a cycle of [beta,gamma]. Work in G = T - x u1 with x coloured alpha, as in Lemma F. The face on each side of an edge of C is a triangle (every edge of the quadrilateral face of G touches x or u1, and C avoids both), so its third vertex has colour alpha or D (possibly x itself) on each side of C. The {alpha,D} chain through x and u1 is connected and avoids C, so it lies on one side; the other side contains alpha or D vertices that are not in the chain: an extra, ring-free [alpha,D] component. So each cycle of [beta,gamma] forces an extra [alpha,D] component. Conversely, I1 gives sum comps - sum cyc = 8 for any colouring; with five forests (Dgamma, Dalpha, alpha gamma, Dbeta, alpha beta, from rigid L and R) and Proposition 2, the number of extra components over the minimum 8 equals cyc_{beta gamma}. This is the data (1 extra component, 1 cycle). The excess identity then gives the type II pattern: exc = (D,a,b,g) = (n-5-3n_D, n-4-3n_a, n-3-3n_b, n-3-3n_g), which for n = 17 and sizes (4,4,4,4) is (0,1,2,2), exactly the data on 17:0.

**Escape structure of the four non-rigid triply locked states (17:0, vertices 4 and 6).**

- [data] The same two neighbours nu_beta and nu_gamma exist and both unlock, again for the fans at u2 and u0, again with no broken chain at first order and Kempe distance 4.
- [data] There is a third non-trivial neighbour, the swap of the main [D,alpha] component, which stays locked (pure distance 4 from fill). The non-rigid case therefore has one more neighbour than the rigid one, because [D,alpha] is disconnected, and the extra neighbour is not an escape.
- [hand] Propositions 4 and 5 carry over: swaps of ring-free components preserve all classes, and swaps of a connected pair are global transpositions. Only the connectivity of the pairs [alpha,beta], [alpha,gamma], [beta,gamma] is [data] here (the [beta,gamma] pair has the cycle but is connected).
- The 24 doubly locked non-rigid members need no escape: their third fan is separable.

## 9. Task 3: does any of this suggest a route to D1?

**For.** The rigid case is much smaller than it looks: the neighbourhood is two states and the only fan to unlock is determined (Proposition 5). Locks come with an exact structure (all pairs forests, excess formulas), so any hypothetical lock at larger n is a very constrained object. Rigid triply locked states can exist only for n = 13 and n >= 16, tightly at 17 and 18. A computer search could look for them without enumerating triangulations (search for the disc T-x with the forced pair structure), but I did not do it (orders > 18 are outside my brief).

**Against.**

- The counting identities are exact but have a one-sided consequence (exc_i >= 0), and the data point (4,4,4,4) is the extremal edge of that inequality. The slack grows with n, so counting cannot exclude locks for n >= 19. The consistency check in section 7 shows it also does not exclude "both neighbours locked".
- The unlocks sit at Kempe distance 4 in G. A hand proof via Jordan at the ring only reaches chain connectivity, i.e. distance 1.
- **Reduction to 4CT.** If T is a minimum counterexample to the Four Colour Theorem then no state is separable and none has a pure fill (a separable state gives a proper colouring of T by the bridge). So D1 for every minimum-degree-5 triangulation implies the Four Colour Theorem for minimum counterexamples [hand]. A proof of D1 can therefore not be purely local unless it uses the hypotheses of D1 only through facts that already encode colourability. The restricted statement (N), at a state which is locked at all three fans, is no stronger than "there is a neighbour that is not locked", which is a statement about one explicit pair of neighbours; but its proof, if it exists, has to see a distance-4 Kempe sequence.

**Possible directions [lead].**

1. A "second-order Jordan lemma": show that in c' = nu_gamma c the path u3 ~ u0 in [beta,D] can always be cut by swapping a component of [alpha,gamma] or [alpha,D] that lies inside the cycle forced by Proposition 6. The cycle found in Proposition 6 is the natural place to look: the data show preparatory swaps of four- and six-vertex pieces.
2. Derive a contradiction from "nu_gamma c and nu_beta c both triply locked, hence both of type II", using the exact structure of type II (one cycle in the pair of end colours, one extra ring-free component in the pair containing the middle colour). The identities give no contradiction on their own, so the contradiction would have to be geometric, using the shared graph T-x.
3. A declared test of (N) on fresh data once some rigid triply locked state at order >= 18 exists; at present there are only four (all on 17:1), so (N) has been seen four times.

## 10. What is not shown

- (N) is not proved. The identities rule out nothing beyond c' being rigid triply locked.
- The structure of locked sets ({L,R} without M never occurring) is data at the class level (only first-order proved).
- The classification of the 8 SEP-bad states into two types rests on two graphs. Fans of c' being "legal" needs the legality of the fans u3, u4 of c, which is a hypothesis of the state being locked at them.
- The Kempe distance 4 and the shapes of the preparatory swaps are one BFS shortest path, not a classification.
