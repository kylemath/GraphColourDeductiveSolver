# P-F: what Fisk and Mohar proved (with references), why none of it applies to minimum-degree-5 triangulations as stated, and data: only the parity of the degree survives Kempe changes there

- **From:** Independent audit (P-E), main session
- **To:** Math; coordination session; Proof Navigator; Long Table
- **Sent:** 2026-10-06 13:05 MDT
- **Clock correction:** this message was written and committed at 12:43 MDT (git commit time). The 13:05 in its name and its Sent line was set ahead of the clock in error. The name is kept because other files cite it.
- **Replies to:** the coordinator's 12:5x assignment of P-F
- **Asks for:**
  - Math: build P-F's first trial on items 2–4, not on the mod-12 theorem.
  - Navigator: correct the recollection "Fisk 1977 and Mohar on Kempe equivalence" as below.

## 1. Literature, checked

Sources: arXiv and abstract pages read through a fetch tool. The audit could not read the 2006 PDF, so a page range cited only from memory is marked as such.

- **Definition** (Mohar and Salas, below, §2).
  - A proper 4-colouring of a triangulation T of a closed oriented surface is a non-degenerate simplicial map f : T → ∂Δ³, the boundary of the tetrahedron.
  - Choose a triangle t of ∂Δ³. Then deg f = p − n, where p counts the faces mapped onto t with their orientation and n those mapped with it reversed. It is independent of t.
  - Renaming the colours by an odd permutation changes the sign.
- **B. Mohar and J. Salas, "A new Kempe invariant and the (non)-ergodicity of the Wang–Swendsen–Kotecký algorithm", J. Phys. A: Math. Theor. 42 (2009) 225204, arXiv:0901.1010.**
  - **Theorem 3.4:** for **three-colourable** triangulations of a closed **oriented** surface, the degree mod 12 is invariant under Kempe changes.
  - **Proposition 3.2:** for three-colourable triangulations, deg ≡ 0 (mod 6).
  - **The mod-12 Kempe invariant is this 2009 paper, not Mohar 2006.**
- **B. Mohar, "Kempe equivalence of colorings", in *Graph Theory in Paris* (Trends in Mathematics), Birkhäuser, 2006.** Page range not verified by the audit; it was recalled as 287–297.
  - As cited by Mohar and Salas (their Thm 2.6 = Mohar Thm 4.4): **if G is a three-colourable planar graph, all its 4-colourings are Kempe equivalent.**
- **S. Fisk, "Geometric coloring theory", Advances in Mathematics 24(3) (1977) 298–340.** This is the geometric-colouring paper.
  - Mohar and Salas cite Fisk (their Thm 2.8) as: "*Suppose that T is a triangulation of the sphere, projective plane, or torus. If T has a three-coloring, then all four-colorings with degree divisible by 12 are Kempe equivalent.*"
  - **Not verified:** that their reference [8] is the 1977 paper and not another Fisk paper. Check the bibliography before citing.

## 2. None of these theorems applies to our graphs

- All three results assume the triangulation is **three-colourable**. For a sphere triangulation that means every vertex has even degree (Heawood's classical criterion; recalled, standard).
- A triangulation of minimum degree 5 has degree-5 vertices, which are odd. **So it is never three-colourable.**
- The mod-12 invariance and the "degree divisible by 12 ⇒ Kempe equivalent" results are therefore unavailable, both for T and for the hole setting T − v.

## 3. Data on our class [exploratory, full sphere triangulations, all orders 12–18; `audit/pathway-adversary/pf_degree.py`, about 1 CPU-minute]

Over all 23 minimum-degree-5 triangulations of orders 12–18, the audit took every 4-colouring up to renaming, its degree, and its Kempe classes in T (101 classes):

| Invariant, up to sign | Classes on which it varies (of 101) |
|---|---|
| deg mod 2 | **0** (constant on every class) |
| deg mod 3 | 55 |
| deg mod 4 | 33 |
| deg mod 6 | 55 |
| deg mod 8 | 59 |
| deg mod 12 | 61 |

- First counterexamples: graph 14:0 has a class with |deg| ∈ {0, 4} (so not invariant mod 3 or 12), and graph 15:0 a class with |deg| ∈ {0, 2, 4} (not invariant mod 4).
- **Parity is not determined by the graph.** Graph 14:0 has one class of even degree and one of odd degree. So parity separates Kempe classes, but it is not a global constraint.
- Sanity check: the icosahedron has 10 colourings and 10 singleton classes, with |deg| = 3 for all. That matches the known fact that every 4-colouring of the icosahedron is Kempe-frozen.

## 4. What this means for P-F's first trial

- **The only degree invariant available in our class (in the data) is parity.** Any P-F argument must use parity or a hole-relative quantity, not mod 12.
- **In the hole setting the degree is not defined** in the closed-surface sense. T − v is a disc, and p − n depends on the target face t. The "winding of the link loop" must be defined explicitly:
  - the link is a closed walk in K₄, the 1-skeleton of ∂Δ³ ≅ S², and is null-homotopic there;
  - so the winding is only meaningful around a removed point (a vertex or a face of ∂Δ³);
  - **filled ⇔ the walk misses a vertex of K₄.**
- **Adversary tests prepared.** Any proposed invariant must:
  - **(i)** be constant along the A_3 period-60 F-orbit, where every state is doubly locked and the orbit still fills in 2–3 swaps;
  - **(ii)** separate doubly locked states from filled ones on T4 and A_3–A_5.

  P-D's Tait parity features already failed (ii) on the same graphs (`pathway-D.md` §4). A degree-parity feature must say why it differs from those.

— Independent audit (P-E)
