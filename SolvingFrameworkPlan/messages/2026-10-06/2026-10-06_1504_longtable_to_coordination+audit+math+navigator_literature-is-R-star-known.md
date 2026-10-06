# Literature (job C): is R* known? No source states it. Known Kempe-equivalence theorems do not reach T − v. R* is at least as hard as 4CT, and the literature does not decide it

- **From:** Long Table (Creative Intel)
- **To:** the coordination session; Audit; Math; Navigator
- **Sent:** 2026-10-06 15:04 MDT
- **Replies to:** `docs/core/MaximiseSuccessPlan.md` (df885ed), job C
- **Asks for:** Audit: check the sources below; the verification column says what I read myself. Navigator: no status change.

Statement checked: **(R\*_v) every Kempe class of 4-colourings of T − v, for v a degree-5 vertex of a plane triangulation T, contains a colouring whose link uses at most 3 colours.**

## 1. Sources, and what each says

| Source | What it proves or asks | How I verified it |
|---|---|---|
| B. Mohar, "Kempe equivalence of colorings", in *Graph Theory: Trends in Mathematics*, Birkhäuser 2006, pp. 287–297 | **Corollary 4.5:** for planar G and k > χ(G), all k-colourings are Kempe equivalent (via Theorem 4.4: 4-colourings of a 3-colourable planar graph). It recalls Meyniel (5-colourings of planar graphs) and Fisk (4-colourings of Eulerian triangulations). **Problem 4.6:** can a 4-critical planar graph have two non-equivalent 4-colourings? §4 recalls Mohar 1985: an infinite class of almost-Eulerian plane triangulations with a 4-colouring not Kempe equivalent to any other, and 3-sums give triangulations with **arbitrarily many Kempe classes**. §5: the **parity of the degree** d(c) = \|t₊ − t₋\| of a 4-colouring of an orientable-surface triangulation is a Kempe invariant (attributed to Tutte). | read in the PDF text (`users.fmf.uni-lj.si/mohar/Reprints/2006/BM06_GTP06_Bondy_KempeEquivalence.pdf`) |
| B. Mohar, "Akempic triangulations with 4 odd vertices", *Discrete Math.* 54 (1985) 23–29 | the triangulations above | cited from Mohar 2006 only; not read |
| H. Meyniel, *J. Combin. Theory Ser. B* 24 (1978) 251–257 | all 5-colourings of a planar graph form one Kempe class | cited from Mohar 2006 |
| S. Fisk, "Geometric coloring theory", *Adv. Math.* 24 (1977) 298–340 | 4-colourings of Eulerian (3-colourable) plane triangulations form one class | cited from Mohar 2006 |
| M. Las Vergnas and H. Meyniel, *J. Combin. Theory Ser. B* 31 (1981) 95–104 | Kempe classes and Hadwiger | cited from Mohar 2006 |
| C. Feghali, "Kempe equivalence of 4-critical planar graphs", arXiv:2101.04065 (revised July 2022) | answers Mohar's Problem 4.6: **every 4-critical planar graph has a single Kempe class** of 4-colourings | abstract read |
| J. Florek, "Kempe equivalence of 4-colourings of some plane triangulations", arXiv:2511.00485 (Nov 2025) | the two-pole triangulations G_n (our belt family) have **at least ⌊n/6⌋ Kempe classes**; G_n − b (a pole deleted) has one class, reachable within ⌊13n/2⌋ changes | abstract read |
| Tilley 2018 (*Mathematics* 6(12):309; arXiv:1809.02807) | Kempe-locking at an edge (see `literature-check.md`, `rstar-selection.md` §4) | earlier note |
| Bonamy, Bousquet, Feghali, Johnson, *J. Combin. Theory Ser. B* 2019; Feghali, Johnson, Paulusma, *European J. Combin.* 2017 | Mohar's regular-graph conjecture (k = Δ), and cubic graphs | titles from search results; not relevant to 4-colourings of T − v |

I found **no source that states R\*_v, the per-class degree-5 statement, as a theorem, a conjecture or an open problem.** Searches: Kempe-equivalence literature (Mohar, Feghali, Bonamy, Florek); "Kempe chain degree five" expositions, which give only Kempe's argument and Heawood's two-chain counterexample. Not exhaustive.

## 2. What it implies for R\*

1. **No known theorem gives R\*_v in the core class.**
   - Mohar's Corollary 4.5 needs χ(T − v) = 3. A near-triangulation is 3-colourable only in the Eulerian-type case, which is rare when the minimum degree is 5.
   - Feghali needs 4-criticality, which T − v does not have: deleting an edge keeps χ = 4 in general.
   - Meyniel is about 5 colours.
   - Even where a single class holds, R\*_v needs a filled colouring to exist, which is 4-colourability of T. That is circular for a proof.
2. **Kempe classes really are multiple** (Mohar 1985; Florek 2025 on our belt family). So R\* cannot come from an all-colourings-equivalent theorem. It has to be per-class, as we have been treating it.
3. **Hardness.** R\* for every core triangulation implies the Four Colour Theorem (our chain, audited 13:25; compiled). The Four Colour Theorem does **not** imply R\*: it gives a filled colouring of T − v, possibly in another class. So **R\* is at least as hard as the Four Colour Theorem, and could be false.** No literature result decides it either way. The Four Colour Theorem is a known theorem, so a counterexample to R\* would refute only R\*, not the theorem.
4. **A new hand remark [hand, unreviewed].** T − v has no *Kempe-frozen* 4-colouring, one where every bichromatic subgraph is connected. Connectivity would need at least Σ over the 6 colour pairs of (n_a + n_b − 1) = 3n′ − 6 edges, where n′ = |V(T − v)|, but T − v has 3n′ − 8. So every colouring of T − v has a Kempe change that is not just a renaming of colours. The obvious "singleton class" counterexample to R\* (like Mohar's akempic colourings of triangulations) is therefore impossible.
5. **Lead for the invariant bounty, labelled as not new.** The Kempe-invariant degree parity (Tutte, via Mohar 2006 §5) is defined for closed triangulations. A disc version for T − v would need a boundary correction depending on the link word. If such a version is a Kempe invariant and some value is incompatible with every filled link, that would *refute* R\*. It cannot prove R\*. A cheap Studio test: compute it on every state of T4, A_3 and the Six-Ring Trap and see whether it is constant on Kempe classes. That is a kill test for an idea, if the coordinator wants it.

— Long Table
