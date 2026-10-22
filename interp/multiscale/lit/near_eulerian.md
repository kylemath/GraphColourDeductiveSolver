# Dvořák–Moore–Seifrtová–Šámal, "Precoloring extension in planar near-Eulerian-triangulations"

arXiv:2312.13061 (v1, 20 Dec 2023; extended abstract EuroComb 2023). Read from the arXiv HTML on 22 Oct 2026, through a summarising fetch tool, so theorem *numbers* are reliable and the wording below is paraphrased. **[Paper]** = what the paper states; **[Ours]** = my analogy or comparison, not in the paper.

## 1. Definitions [Paper]
- **Near-Eulerian triangulation:** a plane graph in which every face except possibly the outer one is a triangle, and every vertex *not on the outer face* has even degree. So any odd-degree vertices lie only on the boundary. **There are no interior odd vertices.** In a hued graph they cannot occur (Obs. 5).
- **Hue:** a proper 3-colouring ψ: V → Z₃ (it exists by Obs. 5). **Colour:** a proper 4-colouring φ: V → Z₂². Hue together with colour gives a *dappled* graph.
- **Dappled triangular grid T:** vertex set Z², with neighbours ±(1,0), ±(0,1), ±(1,1); hue (i+j) mod 3, colour (i mod 2, j mod 2). The quotient is K₃ × K₄, a triangulated torus with universal cover T.
- **Topological condition ("viable"; there is no winding number):** φ on the outer cycle C is viable if C^φ has a hue- and colour-preserving homomorphism to T. Equivalently, the image of C in the torus K₃×K₄ is a contractible (null-homotopic) closed walk. Thm 7: every dappled patch maps to T. Cor 8: an extendable precolouring is viable. Lemma 21 and Cor 22 give the null-homotopy form of the necessary condition.
- **Single-hexagon:** the image of C lies in one hexagon of T (a centre vertex and its 6 neighbours). The centre has a central hue c and a central colour k.

## 2. What is characterised [Paper]
- **Thm 1:** fix ℓ. Suppose the outer cycle has length ≤ ℓ, *every outer vertex has odd degree*, and the precolouring uses 3 colours. Then extension is decidable in linear time. Route: Lemma 10 (a hexagon is a retract of T), then Cor 11 (single-hexagon extension ⇔ 3-colouring, avoiding k, of the bipartite subgraph of hues ≠ c), then Cor 12 and the Dvořák–Král'–Thomas algorithm.
- **Thm 2:** outer cycle of length ≤ 5 and any precolouring: decidable in linear time. The key step is that every viable colouring of a cycle of length ≤ 5 is single-hexagon, which the paper states without proof. **The paper does not prove "extends ⇔ viable" for ℓ ≤ 5.** It reduces the question to a bipartite 3-precolouring problem.
- **Lemma 23:** an iff for patch extensions of near-quadrangulations: φ null-homotopic on C *and* no φ-shortcut. The 6-cycle 1,2,1,3,1,4 is viable but does not extend, so viability is not sufficient.
- **Conj 3:** a polynomial algorithm exists for every ℓ. **Conj 4:** for even ℓ there is d such that every viable colouring of C extends if G−U has d faces of length ≥ 6 that are far apart and not separated by short cycles ("enough room").
- **Not in the paper:** annuli, interior odd vertices, any height or statistical-physics citation (Kondev–Henley and Moore–Newman are absent).

## 3. Relation to the Kondev–Henley / Burgers picture [Ours]
- The match is close but not word for word. T is our Λ, with the colour as the coset in Λ/2Λ ≅ Z₂². The hue-(+1) steps (1,0), (0,1), (−1,−1) are our e₁, e₂, e₃, so our rule H_{i+1} = H_i + e_{r(i)⊕r(i+1)} is their homomorphism C^φ → T. **Viable ⇔ boundary Burgers vector t = 0.** Their torus K₃×K₄ = Λ/(index-12 sublattice) is the hue-resolved cover of our pillowcase S²(2,2,2,2). Hue exists exactly because no interior vertex is a vortex. So their setting is the zero-vortex sector, and odd boundary vertices are harmless there.
- Their single-hexagon condition equals our "level" condition (τ ≤ 1, the walk lies in a radius-1 hexagon). Their (c, k) is our skeleton colour at the centre 0. Lemma 10's retract is the analogue of our 3-layer hexagon automaton (bandfill §1).

## 4. Our tables (bandfill §2, reviewer_tests B; L = 5..9) [Ours]
- **Not directly comparable.** Their objects are discs with one precoloured boundary. Ours are degree-6 annuli with two boundary rows and k inserted rows, the "insertion width". No theorem of theirs states or implies k*(L).
- **Consistent, with no contradiction found:**
  - (a) With all hue steps +1, a closed walk in T needs L ≡ 0 (mod 3). This is our f(t) ≡ L (mod 3), so for L ≢ 0 the level rows have t ≠ 0 and are non-viable as disc boundaries (Cor 8).
  - (b) Our "t is invariant along an Eulerian band; rows with different t never join" is the annulus analogue of Lemma 21. Free homotopy in the torus, up to the renaming D_π, is our extrapolation, not their theorem.
  - (c) Viable but non-extendable (their 6-cycle example), and Conj 4's "far-apart room", match our finding that a matched class is not enough and some width k* ≥ 1 is needed (k* = 2/1/2/4/2 at L = 5..9). Conj 4 is the disc analogue of our [C] "k* ≤ 4 for all L".
- **Thm 2 (ℓ ≤ 5)** concerns 5-cycle discs and says nothing about our L = 5 cylinder rows.
- Our vortex results (5–7 dipoles, 5,5,7,7 quadrupoles) lie outside their framework.

## Checked against the LaTeX source k sent (22 Oct 23:50Z)
Statements above confirmed. Three additions from the exact text:
1. **Retraction / maximum principle (Lemma lem-retract + Cor cor-eq3).** Every hexagon of the grid is a retract of the grid (Hell). Hence for a single-hexagon (our "level", walk in one radius-1 hexagon) boundary on a hued patch (no interior odd vertices), the boundary extends iff it extends by a colouring whose whole height map stays inside that hexagon, i.e. the central colour k sits exactly on hue class c and the rest is a 3-colouring of the bipartite remainder. Consequence for us [P, their proof]: in a zero-vortex disc, levelness of the boundary can be assumed to propagate to the interior. This is a max-principle we can cite.
2. **Shortcut criterion (Lemma lemma-noshort).** For patch extensions of near-quadrangulations: extends iff null-homotopic and no generalized chord P shorter than the topological retract (reduced word) of f(base). This is a Lipschitz-type criterion (grid distance <= graph distance along chords) and is the disc analogue of our insertion width k*.
3. **Their programme lists the cylinder (two precoloured faces) as the next basic case.** Our tube/band results are exactly that case, with vortices added. The 1,2,1,3,1,4 hexagon counterexample is in the final paragraph.
