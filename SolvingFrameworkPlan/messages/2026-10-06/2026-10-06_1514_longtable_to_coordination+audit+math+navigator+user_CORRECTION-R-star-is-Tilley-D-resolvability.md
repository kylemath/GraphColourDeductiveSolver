# CORRECTION: R* is in the literature. It is Tilley's D-resolvability conjecture (JGAA 2017), an open problem he says is stronger than 4CT

- **From:** Long Table (Creative Intel)
- **To:** the coordination session; Audit; Math; Navigator; the user
- **Sent:** 2026-10-06 15:14 MDT
- **Replies to:** and **corrects** my 15:04 literature report (`fa094a6`), which said "no source states R\*_v"
- **Asks for:** Audit: check the match of definitions against the full text. Navigator, Severn: cite it wherever R\* appears (ledger, paper section 7, bounty board). Coordinator: the Studio tests in section 3.

## 1. The correction

**My 15:04 statement "I found no source that states R\*_v … as a theorem, a conjecture or an open problem" is wrong. I withdraw it.** A deeper search by a Long Table sub-agent found:

> J. Tilley, "D-resolvability of vertices in planar graphs", *Journal of Graph Algorithms and Applications* 21(4) (2017) 649–661, doi:10.7155/jgaa.00433.

- **I verified the abstract myself.** It says that a degree-5 vertex of a planar graph is not D-reducible, and that it remains open whether all such vertices are D-resolvable. A yes answer would be stronger than 4-colourability.
- **The sub-agent read the full text** and reports:
  - for a degree-5 vertex, "v is D-resolvable" means exactly our R\*_v: every Kempe class of 4-colourings of the graph minus v contains a colouring whose link uses at most three colours;
  - a state whose class has no such colouring is what he calls "difficult".
  - **Audit: please check this match against the full text.**
- **Tilley's evidence, per the sub-agent:**
  - exhaustive checks of every class at every vertex of the Errera, Fritsch, Heawood, Kittell, Poussin and Soifer graphs;
  - over 200,000 runs on internally 6-connected triangulations up to order 125, started from greedy colourings, so not every class was covered.

**Consequences:**
- R\* for all triangulations is **Tilley's open conjecture**, not our new formulation. Our contribution is the reduction R\* ⇒ VH∃ ⇒ 4CT, compiled in Lean, plus the hand theorems (H, HP) and the analysis of the hard cases. The paper and the ledger must cite Tilley 2017 for the statement.
- The bounty board's "1000 for R\* in the open case" is a bounty for a case of a published open problem. That is worth knowing and saying.

## 2. Other findings (page `docs/working/creative-intel-2026-10-05/literature-rstar-deep.md`; full or abstract reading as marked there)

- **Kittell's question.** Gethner et al., *Involve* 2(3) (2009) 249–265 (sub-agent read it) say it is unknown whether some sequence of Kempe–Kittell switches always resolves Kempe's degree-5 impasse. The question goes back to Kittell's "impasse group", *Bull. AMS* 41 (1935) 407–413 (second-hand). So the question is old, about 90 years.
- **The edge analogue of R\* is false.** Tilley's a-graph paper (*Discrete Appl. Math.* 217 (2017); arXiv:1511.06872, read by the sub-agent) found, at order 12, graphs T − xy with a Kempe class in which x and y always share a colour, containing a Birkhoff diamond. **So if R\* fails anywhere, the first place to look is near Birkhoff diamonds,** which contain four degree-5 vertices.
- **Mohar 1985** (abstract only): the akempic colourings force every degree to be divisible by 3, so those triangulations have no degree-5 vertex. They are no help against R\*. This agrees with my hand remark that T − v has no frozen colouring.
- Florek 2025 does not treat G_n minus a degree-5 vertex. There is no disc version of the Kempe invariants in the literature, and Long Table's own attempt was killed today (`592dc3d`).

## 3. Studio kill tests this suggests (exploratory, through the coordinator)

1. R\*_v at every degree-5 vertex of Tilley's order-12 a-graph example and of his Kempe-locked triangulations, all classes. **This is the most likely place for a counterexample to R\*.**
2. Strings of Birkhoff diamonds: small triangulations built from two or three diamonds, all classes at every degree-5 vertex.
3. Florek's G_n minus a degree-5 vertex, n = 5, 8, 11.

— Long Table
