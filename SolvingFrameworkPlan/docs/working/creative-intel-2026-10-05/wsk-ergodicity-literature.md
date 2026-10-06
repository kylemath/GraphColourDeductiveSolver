# Kempe classes as WSK ergodicity: what is known (Long Table, 6 Oct 2026, evening)

Reading only; nothing computed except text extraction from PDFs. For each item, "read" says how it was checked: **full** (text read), **abstract** (abstract or summary page read), or **second-hand** (cited in another source). Anything from memory is marked **unchecked**.

At zero temperature, Kempe changes are exactly the Wang–Swendsen–Kotecký (WSK) cluster moves of the q-state Potts antiferromagnet. A Kempe class with no filled state is a broken-ergodicity sector.

## (a) What is proved: sphere versus torus

| Setting | Result | Source | Read |
|---|---|---|---|
| 3-colourable (Eulerian) triangulations of a closed orientable surface | **The degree of a 4-colouring mod 12 is a Kempe invariant** (Thm 3.4). There is more than one class iff some colouring has degree ≡ 6 mod 12 (Cor 3.5, which uses Fisk's theorem on that surface). | B. Mohar, J. Salas, "A new Kempe invariant and the (non)-ergodicity of the Wang–Swendsen–Kotecký algorithm", *J. Phys. A: Math. Theor.* 42 (2009) 225204, arXiv:0901.1010 | abstract plus a summary of the ar5iv text |
| Torus T(3L,3M), 3 ≤ L ≤ M | **At least two Kempe classes, so WSK for the 4-state antiferromagnet is not ergodic.** T(6,6): 305,192 colourings of degree 0, 45 with \|deg\| = 6, 1 with \|deg\| = 18, giving exactly 2 classes. T(3,3): 1 class (too few faces for degree 6). | same | same |
| Triangular-lattice tori in general | The paper says WSK ergodicity is open for q = 4, 5, 6 (q ≥ 7 known ergodic, q = 2 trivially not). | same | same |
| Eulerian triangulations of the sphere, projective plane and torus | All 4-colourings of degree divisible by 12 are Kempe equivalent. On the sphere this means a single class. | S. Fisk, "Geometric coloring theory", *Adv. Math.* 24 (1977) 298–340 | second-hand (via Mohar 2006 and Mohar–Salas) |
| Planar G with χ(G) < k | One Kempe class of k-colourings (Cor 4.5). Meyniel: all 5-colourings of a planar graph form one class. | B. Mohar, "Kempe equivalence of colorings", in *Graph Theory: Trends in Mathematics*, Birkhäuser 2006, 287–297; H. Meyniel, *JCTB* 24 (1978) 251–257 | Mohar full; Meyniel second-hand |
| Plane triangulations, 4 colours, not Eulerian | **More than one class can occur.** Mohar's "akempic" triangulations have 4 odd vertices, every degree divisible by 3, and a frozen colouring. 3-sums give arbitrarily many classes. | B. Mohar, *Discrete Math.* 54 (1985) 23–29 | abstract or second-hand |
| Plane triangulations with exactly two odd-degree vertices | Kempe equivalence of their 4-colourings is **an open problem**. A talk proves a weaker version. It also proves that all k-colourings (k ≥ 3) of a 3-colourable projective-planar triangulation are Kempe equivalent. | A. Nakamoto (joint with N. Matsumoto, K. Wakayama), ICMS talk abstract, 2025 | abstract (PDF text) |
| Two-pole plane triangulations G_n (our belts) | At least ⌊n/6⌋ Kempe classes; one class after deleting a pole. | J. Florek, arXiv:2511.00485 (2025) | abstract |
| Degree-5 vertices: R*_v | **Tilley's D-resolvability conjecture (open)**, stated to be stronger than 4CT | J. Tilley, *JGAA* 21(4) (2017) 649–661 | abstract (full text by a sub-agent) |

**Summary.** For 4 colours the only proved non-ergodicity results are on **closed surfaces with an invariant tied to the surface** (torus, degree mod 12), and on **special plane triangulations** (Mohar's akempic family, with degrees divisible by 3 and so no degree-5 vertex; Florek's belts). On the sphere every proved single-class result needs extra structure: Eulerian, χ < k, or 4-critical (Feghali 2022). General plane triangulations remain open, for example the two-odd-vertex case.

## (b) Math's recollection: several Kempe classes on toroidal triangular lattices

- **True for the 3-colourable sizes.** T(3L,3M) with 3 ≤ L ≤ M has at least two classes, and T(6,6) has exactly 2 (Mohar–Salas). T(3,3) has one. **The separating invariant is the degree mod 12:** a colouring of degree ≡ 6 mod 12 is not equivalent to the 3-colouring, which has degree 0.
- **For the non-3-colourable 6-regular tori T(r,s,t), I found no result.** Mohar–Salas call the general triangular-lattice case open for q = 4. Sankarnarayanan (*Ann. Comb.* 26 (2022) 559–569; abstract) completes the classification of which T(r,s,t) are 4-colourable, not their Kempe classes.
- **Is a large flat all-degree-6 region on the sphere a risk for the hybrid lemma?** [hand, unchecked judgement] The torus mechanism is global. The degree is defined on a closed surface, it is invariant only when the triangulation is Eulerian, and the value 6 mod 12 is realised by colourings that wind around the torus's non-contractible cycles. A flat region on the sphere is a disc, and a minimum-degree-5 sphere triangulation has 12 or more odd vertices, so the invariant is not available. Long Table showed today that no disc version is a Kempe invariant (\`disc-degree-parity.md\`, \`path5-tait-sign-invariant.md\`). So **the toroidal obstruction does not transfer directly.** That does not prove flat regions are safe. A sphere obstruction would need a different mechanism, and Mohar's akempic family shows that non-Eulerian plane triangulations can be multi-class through frozen colourings. Those require degrees divisible by 3, which degree 5 breaks, and T − v has no frozen colouring (Long Table, 15:04 message, item 4).

## (c) Numerics we do not have

- Mohar–Salas: exact colouring counts by degree on T(6,6) (above).
- Tilley 2017: every class at every vertex of the Errera, Fritsch, Heawood, Kittell, Poussin and Soifer graphs; over 200,000 runs on internally 6-connected triangulations up to order 125, starting from greedy colourings (via a sub-agent's full-text read).
- Tilley, a-graphs (*Discrete Appl. Math.* 217 (2017); arXiv:1511.06872): order-12 graphs T − xy with a class where x and y always share a colour, containing a Birkhoff diamond.
- Florek 2025: exact class counts for G_n.
- **Not found:** WSK or Kempe-class numerics for the 4-state antiferromagnet on *spherical* triangulations. Physics studies use tori or free boundaries; Mohar–Salas note that free boundaries cannot remove surface effects. Our census (orders 12–26) may be the first systematic sphere data; **this is unchecked, and a targeted search could still find something.**
