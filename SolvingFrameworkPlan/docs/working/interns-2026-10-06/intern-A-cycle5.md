# Intern A, cycle 5: independent hand review of Lemma O and Lemma LC (FellowF-55656.md, §2.2 and §4.5)

By hand only, no code. I re-derived each step from the frame definition in §1 (x_i = port(j+4+i), word (A,B,A,Γ,Δ) on x0..x4) without relying on Fellow F's wording. Verdicts: correct / gap / wrong.

## Lemma O (§2.2)

| Step | Verdict | Check |
|---|---|---|
| O.0 F is well defined on D and F(s) has link (a,b,g,a,d) | correct | x2, x3 are adjacent so one {a,g}-component K_F. x0 is not in K_F (Jordan fact, uses lock 2 of s, hence needs s in D). x1 = b, x4 = d are not a/g. So only x2 -> g, x3 -> a change on the link. |
| O.1a B(F(s)) = s | correct | F(s) read in the frame x'_i = x_{i+3} has word (a,d,a,b,g) = (A,B',A,Γ',Δ') with B'=d, Γ'=b, Δ'=g. B in that frame swaps the {A,Δ'} = {a,g}-component of x'_0 = x3. That component is exactly K_F: K_F was a whole component in s (no outside a/g neighbour) and the outside is unchanged, so it is still a whole component with colours exchanged. Swapping again restores s. This identity needs only that F(s) has an unfilled link, not that F(s) is DL. |
| O.1b F(B(s)) = s | correct | B(s) has link (d,b,a,g,a) (x2 not in K_B by the mirror Jordan fact), frame x'_i = x_{i+2}, F swaps the {a,d}-component of x'_2 = x4 which is K_B. |
| O.2 in/out degree <= 1, components are paths or cycles | correct | F is a function; O.1a makes it injective on D (this is where O.1a is actually needed: it excludes rho-shaped orbits). D is finite. |
| O.2 path end fills within k+2 swaps | correct | F(s_end) is proper, has a 4-coloured link, is not in D, so it is an unfilled non-DL state, which fills in one swap (Unlock, cited, correct by HP review step 0). Count: k F-steps, one more F, one fill swap = k+2. |
| O.3 F: j -> j+3, (beta,gamma,delta) -> (delta,beta,gamma), A fixed | correct | New middle is x4 = port(j+8) = port(j+3). New x'_3 = x1 (beta), new x'_4 = x2 which is gamma after F, new x'_0 = x3 and x'_2 = x0 both a. So the repeated colour stays a. |
| O.3 the link colouring determines (j, triple) | correct | Four colours on five ring vertices give exactly one repeated pair at distance 2, so the middle is unique; sigma is then forced. Reflection is not needed because sigma is an arbitrary renaming. |
| O.3 F^k(s)=s forces 15 | k | correct | j returns iff 5 | 3k iff 5 | k; the 3-cycle on the three non-A colours returns iff 3 | k. |
| Corollary O | correct, with a dependency | Uses Lemma Q (cited): in a targetless class all states are DL and the class is closed under swaps, so F(s) in the class is DL, no path end exists (it would fill), hence all orbits are cycles of length 15k. |

**Remarks (not errors).**
1. O.1 holds for every s with x0 not in K_F; the statement "on D" is stronger than needed. D is only used so that the Jordan fact applies.
2. The lemma proves "multiple of 15", not that 15 itself occurs.
3. Useful by-product: lock 1 of F(s) is automatic (see LC), so F(s) is DL iff lock 2' ({d,g}-path x4 ~ x2) holds in F(s). Fellow F's tables use this implicitly.

## Lemma LC (§4.5)

| Step | Verdict | Check |
|---|---|---|
| F leaves the {b,d}-subgraph unchanged | correct | F recolours only vertices of K_F, which carries only colours a and g. Vertices of colour b or d keep their colour, so the {b,d}-induced subgraph of T - v is identical in s and F(s). |
| roles of F(s): b' = d, g' = b; lock 1' = {b',g'}-path x'_1 ~ x'_3 | correct | x'_1 = x4 (colour d) and x'_3 = x1 (colour b). So lock 1' is a {d,b}-path from x4 to x1. |
| conclusion: lock 1 of F(s) equals lock 2 of s; K_1(F(s)) = K_2(s) | correct, slightly understated | Lock 2 of s is a {b,d}-path x1 ~ x4 in the same graph. Both the endpoint pair and the colour pair coincide, so the sets of lock paths are identical, not only the components. Consequence: if s is DL, lock 1' of F(s) holds automatically. The statement does not need F(s) to be DL. |
| mirror: lock 2 of B(s) is lock 1 of s | correct | B(s) has frame x'_i = x_{i+2}, middle x3 (colour g) with b'=g, d'=b (x'_4 = x1). Lock 2' = {g,b}-path x3 ~ x1 = lock 1. B changes only a/d vertices, so the {b,g}-graph is unchanged. |
| Consequence: W34-a propagates (w'_0 = w3, w'_1 = w4, cut at the middle) | correct | I recomputed the ring correspondence w'_t = w_{t+3}: the exits of the new middle x4 into the b-coloured side are w3 = w'_0 and w4 = w'_1. A lock-1' path from x4 enters through w3 iff w3 is joined to x1 in K_2 - x4. So "w3 cut from x1 in K_2 - x4" means no lock-1' path uses exit w'_0. At L1(g,a) -> M(O4) the middle's outer letters (w3,m4,w4) become (g',d',g') because m4 = a lies in K_F and turns g, which matches the text. |

**Gap noted (small).** In the Consequence, "this is not a one-move kill ... memory constraint" is a heuristic judgement: I did not check that no other swap exploits the cut; but it is not part of the Lemma LC statement.

## Overall
No step of Lemma O or Lemma LC is wrong. Both are correct as stated. O.1a is the only step that carries real content (injectivity of F, excluding rho-shaped orbits); everything else is bookkeeping, and I verified each of those entries.

## Self-check, two weakest points
1. The orientation and index conventions (x_i = port(j+4+i), "j -> j+3", ring w'_t = w_{t+3}) were checked once each by hand; an error of one in a shift would change the divisor 15 into 5 or 10 only if the convention were wrong, but all my re-derivations agree with the document, so a shared mistaken convention is the risk.
2. Unlock (an unfilled non-DL state fills in one swap) is cited, not re-proved here beyond the one-line argument in the HP review; the k+2 bound in O.2 depends on it.
