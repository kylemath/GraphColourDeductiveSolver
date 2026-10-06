# Intern D: a coset-curvature potential for the Tait lock picture

Status: candidate, unreviewed. Nothing was run. Labels: [hand] derived by hand, [open] not tested.

## 0. Framing (what a useful invariant can be)

P-F already found that at every tested hole (T4, A_3, A_4, A_5, order-14) the labelled Kempe graph has one class. So any true Kempe *invariant* is constant on the data and cannot separate anything. The only useful object is a **potential**: a global quantity that changes by a known, local-to-the-chain amount under a swap, and that might correlate with fill distance or with double locking. That is what I propose.

## 1. The invariant

Work in Z2xZ2 as in `pd2_lock_proof.md`, colours 0, beta, gamma, delta (c(u)+c(w) is the dual edge colour). For a vertex u of G-v put curvature k(u) = 6 - deg_G(u) (degree in the full triangulation G; k = +1 at degree 5, 0 at degree 6, negative above).

For each colour x in {beta, gamma, delta}, the subgroup {0, x} gives a **coset 2-colouring** of the vertices of G-v: A_x = {c in {0,x}}, B_x = {c in the other coset}. Dual edges of colour y or z (the other two) are exactly the edges between A_x and B_x. So **the (y,z) 2-factor of H is the boundary of the coset region** (fact [hand], one line from c(u)+c(w)).

Define the **coset curvature** and the **colour-class curvature**:

    kappa_c(s) = sum over u in G-v with c(u)=c of k(u)          (four numbers, sum = 11 for a full triangulation)
    Phi_x(s)   = sum over u in A_x of k(u) = kappa_0 + kappa_x    (three numbers; Phi_x + Phi_y... complement = 11 - Phi_x)

For a stuck state with repeat colour alpha at x_j, x_{j+2} (roles of the lock criterion: mu = c(m), c(a), c(b)), record the **role vector**
K(s) = (kappa_alpha, kappa_mu, kappa_{c(a)}, kappa_{c(b)}), and the three coset potentials Phi_beta (beta = alpha+mu), Phi_gamma, Phi_delta. Phi_beta is the curvature mass on the two sides of the (gamma,delta)-boundary, the curve that contains the lock path W through P.

Relation to the Tait picture [hand]: for a simple closed curve C of H bounding a disc with l nodes, i spokes pointing inside and interior faces f, Euler gives sum over the interior faces of (6 - d_f) = 6 + 2i - l. The interior faces are G-vertices, so the enclosed curvature of a boundary component of a coset region equals 6 + 2i - l: it is the spoke imbalance of that curve. So Phi_x is the total spoke imbalance of the (y,z) 2-factor. (It is *not* the degree of P-F: that counts oriented triangles; this is unsigned and orientation-free.)

## 2. Change under a Kempe swap [hand]

Swap the {p,q}-chain K (a Kempe component, p and q two colours, r and s the others).

- If {p,q} is a coset of x (i.e. p+q = x): every vertex of K stays in its coset. **Phi_x is exactly unchanged**, and so is the whole (y,z) 2-factor, in particular the path W if x = beta.
- Otherwise the swap moves the p-vertices of K to the other coset and the q-vertices the other way. With k_p(K), k_q(K) the curvature of K's p- and q-vertices:
  Delta Phi = k_q(K) - k_p(K) (for the coset containing p, sign reversed for the one containing q), and Delta kappa_p = k_q(K) - k_p(K) = -Delta kappa_q.
  Proof: recolouring is vertex-wise; no other vertex is touched. The 2-factor changes by the symmetric difference with the dual cycle of K (swap adds p+q to the dual edges of that cycle).

So each swap changes the potential by a difference of two curvature sums over one chain, with no global recomputation. Since k = +1 only at the at most 11 degree-5 vertices of G-v (for the cases in the files), Delta kappa is controlled by how many degree-5 vertices lie in each colour half of K.

## 3. Why it might separate stuck from fillable [open]

1. The fill criterion is a statement about colour classes at the link. A fill puts v in a colour m absent from the link, and then kappa_m(G) = kappa_m(G-v) + 1. Conjecture to test: **in a stuck state, the colour class that "wants to be missed" is detectable from K(s)**, namely the fill target after the shortest fill sequence is a colour with minimal kappa (a low-curvature class has fewest degree-5 vertices needing separation from v's neighbours).
2. Hand test, the one case I can finish: the icosahedron, all k = 1. A 4-colouring of G-v has class sizes at most 3 (independence number of the icosahedron is 3) and total 11, so the sizes are exactly (3,3,3,2) and K(s) is a permutation of (3,3,3,2). A fill needs a missing colour m, and then kappa_m must be 2 (otherwise the class of m would reach 4 in G). So for the icosahedron: **fillable <=> the unique deficient colour (size 2) is absent from the link** [hand, from the independence bound; the converse direction is by counting: a filled state has class m of size 2 in G-v]. A stuck state has the deficient colour on the link. This is consistent with the picture but is an artefact of alpha(G)=3; it says nothing about degree-5 holes in the 'bad' graphs (the file P-F says the icosahedron has no doubly locked state).
3. Computation to request from the Studio (cheap, no search): for every labelled state at T4 v=4 (1632) and A_3 centre (2400), compute K(s) in role coordinates, Phi_beta, Phi_gamma, Phi_delta, the doubly-locked flag and the shortest-fill radius. Tabulate (radius) vs (Phi_beta - 11/2, kappa_alpha - kappa_mu, the role of the argmin kappa). Success criterion: some role-ordered statistic takes disjoint ranges on radius-2 versus radius-3/4 doubly locked states. Failure: ranges overlap as P-F's |N| did. Second test: along each shortest fill path, does Phi (or the argmin class) change monotonically? Each swap contributes a computable Delta, so the table is a direct check of section 2.

## 4. Self-check: most likely failure

- Most likely: the potential carries no radius information. Curvature is concentrated on at most 11 vertices, so Delta kappa takes only a handful of values, and doubly locked states at radius 2 and radius 4 probably share ranges (exactly what killed the degree). It would then be a bookkeeping device for swap bookkeeping, not a separator.
- Second: the two arguments above (the icosahedron count) only use class sizes; for graphs with many degree-6 vertices (k = 0) the potential degenerates, since a class made entirely of degree-6 vertices has kappa 0 whatever its size.
- Third: sections 1 and 2 are definitions plus a one-line recolouring argument and I have not tied Phi to the lock paths beyond the spoke-imbalance identity, so it does not yet say anything about Z1, Z2 or the pairing at P.
- Not claimed: nothing here proves or refutes R*, and I make no claim about A_3's period-60 orbit (I did not reason through its orbit by hand).
