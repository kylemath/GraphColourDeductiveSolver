# Intern C, cycle 8: hand derivation of 3F - U = 2N0 + 1.5 L_F + sum_P (1 - d(P)) - D_cyc (MathQuarterFloorBijections.md §1-§4, §5 per-j) (hand only, nothing run)

## Verdict: NO ERROR FOUND in the derivation. The identity follows from the stated bijections. Two wording defects, no step that rests on data.

## 1. Inputs I re-derived (each used in the algebra)
1. **Dichotomies M3/M2 (exactly one of short/long).** Tait colours of the pentagon edges at a filled f in F_i: e_i = c2, e_{i+1} = e_{i+2} = e_{i+3} = c1, e_{i+4} = c3. The (c1,c3)-subgraph has the four P-edges e_{i+1..i+4}, and non-crossing pairings are exactly the two stated. For K = the {W,X}-component of x_{i+3}, the cut set at P is e_{i+2}, e_{i+3}; in the short matching these pair with e_{i+1}, e_{i+4}, which forces x_{i+1} and x_i into K. The Jordan argument of pd2 Step 2 gives the opposite non-connections. So the "region principle" is valid: the arcs of the pentagon between two link vertices in one region have an even number of cut ends, and cycles avoiding P never separate link vertices.
2. **phi_A: F_i with M3 short bijects with U_{i+1} with lock 1 failing.** The image link is (W,X,Z,X,Y); the {Z,Y}-component of m is the swapped set K, which misses x_{i+4}, so lock 1 fails. The inverse swaps the component of m, and it is onto: a lock-1-failing s at index j comes from f with i = j-1 and M3 short (m's and a's components differ).
3. **phi_B: F_i with M2 short bijects with U_{i+2} with lock 2 failing.** Same check (image link (W,Z,Y,X,Y), repeat Y at i+2, i+4).
4. **tau: M3-long bits in bijection with M2-long bits.** The {Y,Z}-graph is unchanged by the {W,X}-swap, so x_{i+2}, x_{i+4} stay joined and the image has M2 long. So L_{M3} = L_{M2} = L_F/2, and (3/2)L_F is an integer.
5. **R+3 is a bijection {lock 2 at j} -> {lock 1 at j+3}.** R+3 defined iff lock 2: I re-derived (=>) by the cut argument (delta/beta matching with lock 2 failing is (e_j e_{j+1})(e_{j+3} e_{j+4}); K = comp_{alpha,A}(x_{j+2}) missing x_j would have cut set {e_{j+1}, e_{j+3}}, contradicting the matching). The converse is pd2 Corollary (i). R+3 and R+2 invert each other since both swap the same vertex set K.

## 2. Algebra (the part the note leaves to two lines)
- Failed locks over unfilled states = N1 + 2 N0. By 2-3 this equals the number of short bits = 2F - L_F. So N1 = 2F - L_F - 2 N0. (No double counting: a state with both locks failing is the image of two different filled states, in F_{j-1} and F_{j+3}.)
- Gamma is a functional graph of the injective map R+3, so it is paths plus cycles; a state's Gamma-degree equals its number of locks. N1 states are path ends, one e_- (out-edge only) and one e_+ (in-edge only) per path, so N1 = 2P with P the number of paths.
- 3F - U = 3F - N0 - N1 - D with D = sum d(P) + D_cyc. Substituting N1: 3F - U = F + N0 + L_F - D.
- The claimed right side is 2 N0 + 1.5 L_F + P - D. These agree iff F = N0 + L_F/2 + P, which is exactly N1 = 2P rewritten. The 1.5 is 1 (from L_F) plus 1/2 (from P = F - L_F/2 - N0). Verified. Wheel and floor-quartet checks also agree.

## 3. The per-j identity (§5)
Using phi_A, phi_B at the right indices (F_{j+4} with M3, F_{j+3} with M2, F_{j+1} with M2 against U_{j+3}) gives F_{j+1}+F_{j+3}+F_{j+4} - U_j = L_j + N0_j + N0_{j+3} + B_{j+3} - D_j, where B is the set of lock-1-only states. Partitioning the domain of R+3 by the type of its image gives B_{j+3} = |E_j| + D_j - |DD_j|. So the identity holds as stated. The consequences (H gives 3F >= U; equality iff N0 = L_F = 0 and all d(P) = 1) follow.

## 4. Defects found (none changes the identity)
1. **§3, "a path's two endpoints fill into the same F_i" is false in general.** e_- at index j fills into F_{j+4}; e_+ at index j+3(d+1) fills into F_{j+3(d+1)+3}. These are equal only for d = 1 (mod 5); for d = 0 they are F_{j+4} and F_{j+1}. The note's own next sentence ("these agree when d = 1") contradicts the generality. The identity does not use it.
2. **§4, "|F_i| = |U_{i+1}| = |D_{i+4}| = |U_{i+2}| for each i that occurs"** is true only when a single i occurs; with several i the counts are sums, because e_+ at index i+1 comes from a path whose e_- is at index i.
3. Minor: the cycle length is also a multiple of 3 (colour roles rotate), so 15 | length, which is stronger than "mod 5" and consistent with Lemma O.
4. Not derived, only asserted from data: the 405/365 floor statements and "intern C's signature implies two components" (that signature holds only in one-filled-state classes, and the sentence is hedged).

## Self-check: what would make this wrong
- If phi_A, phi_B were not onto the stated sets, the first identity would shift. I checked the inverse maps directly.
- If a swap in the bijection list merged components other than the stated ones. The vertex-set argument (a swap preserves the component vertex set of its own colour pair) covers every inverse.
