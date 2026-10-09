# Literature check for the chain-parity note

- **Date:** 9 Oct 2026.
- **Who:** a literature sub-agent. It read only; it did not edit `main.tex` and committed nothing.
- **Method:** WebSearch and WebFetch; Crossref, Semantic Scholar and arXiv API look-ups; full text read where open (arXiv, JGAA, Mohar's reprint page, Gonthier's report, Kittell via Kauffman's page).
- **What could not be read:** ScienceDirect blocked every attempt, both plain fetch and the in-app browser. So Fisk 1973/1977/1978 and Mohar 1985 were **not** read in full; their content below comes from secondary sources and is marked as such.

**Stance:** skeptical. The default assumption was that something close is already known. The search found more prior work than the note currently cites. The most important items are §1 (Kittell/Errera, Spencer-Brown) and §2 (the Kempe-invariance of degree parity).

---

## 0. Verdicts in one table

| claim in note | verdict | closest prior work |
|---|---|---|
| Prop. 2 (Kempe duality at the hole) | **KNOWN (classical)** | Kempe 1879 / Heawood 1890 Jordan argument; Errera 1921 and Kittell 1935 build "impasse" on exactly this dichotomy |
| (i) Lock parity (Thm 3: lock ⇔ odd coboundary ⇔ odd number of odd-degree vertices in the αγ / αδ chain of x₂) | **PARTLY KNOWN** | duality part is classical. Parity of Kempe-chain ends at a ring: RSST/Gonthier chord parity bits (Gonthier 2005/2008). Full-triangulation analogue (a Kempe chain's coboundary is a union of even Tait cycles) is standard. **No statement found linking a lock to odd-degree vertices.** |
| Prop. 8 (DL ⇒ N ≥ 8, equality iff rigid) | **PARTLY KNOWN** | Kittell 1935 names eight distinct chains at an impasse (2 circuits, 2 "hand" chains, 3 tangent chains, 1 osculating chain). The bound is implicit there; the "rigid" equality case is not stated. |
| Lemma 10 (Tutte's identity p(X,Y) − p(Z,W) = \|X\|+\|Y\| − e(X,Y) − 1) | **KNOWN** | Tutte 1969; Mohar–Singer 2021 Thm 1 (in summed form J_A = 2\|A\| − deg A + n − 3) |
| Lemma 11 (Fisk degree mod 4: cw ≡ F/2 + 2 deg(A)) | **KNOWN** (immediate) | Fisk 1977 (degree is independent of the target triangle, so cw − ccw = 4·deg f); Tutte 1969 via Mohar–Salas 2009 Lemma 3.1 and Mohar–Singer §3 (deg f ≡ deg(A) mod 2) |
| Lemma 12, last sentence ("a Kempe exchange leaves cw unchanged mod 4 on every closed oriented triangulated surface"); labelled "new here and unreviewed" | **KNOWN** | Equivalent to Kempe-invariance of deg f mod 2: Tutte (reported in Mohar 2006 §5); Mohar–Salas 2009 Cor. 3.3 (any closed orientable surface). **Relabel as [cited].** |
| Lemma 12 (2N ≡ cw + n mod 4, no hole) | **KNOWN in substance** | It is Tutte's parity theorem plus Fisk degree mod 4, written mod 4. That exact display was not found, but it is a two-line combination of cited results; the note already says so. |
| (ii) Thm 5, formula F with a hole: 2N ≡ cw + (n−1) − η + 2(L₁+L₂) mod 4 | **NOT FOUND** (base PARTLY KNOWN) | Nothing found with a boundary term η or lock terms. The no-hole base is known (row above). Fisk's degree theory for discs and boundary words could not be checked (ScienceDirect blocked); this is the main residual risk. |
| Lemma W (cw(πc) ≡ cw(c) + 2 at a DL state) | **NOT FOUND** (link-free half KNOWN) | Its link-free half is the known Kempe-invariance above. The π half is new as far as found. Mohar–Salas compute Δdeg under a Kempe change by counting triangles in the Kempe region, which is the same technique. |
| (iii) Chain-parity law, N(πc) + N(c) odd ⇔ πc DL | **NOT FOUND; close relatives exist** | (a) Full sphere, **no hole**: N mod 2 is a Kempe invariant. This is Spencer-Brown's Parity Lemma (Laws of Form, App. 5; proof in Kauffman 2005) and Tutte's parity theorem. Kauffman notes it fails for non-planar graphs, as the note finds off the sphere. (b) Spencer-Brown tracked how the parity of the number of alternating paths changes along the five steps of his **parity pass** at a 1-deficient pentagon (BKM 2026 §3, citing his 1980 Royal Society MS 734 and Kauffman 2005). That is the closest thing to the law, but its exact content is unpublished and unverified. (c) π itself is Kittell's (1935) "tangent chain" operation ζ/η at an impasse (§1). |
| Thm 9 (link-free exchange preserves N + L₁ + L₂ mod 2) | **PARTLY KNOWN** | This is the hole analogue of the parity lemma / Tutte invariance in (iii)(a). The hole correction term was not found. |
| (iv) Rigid isolation (π never maps a rigid state to a rigid state); "π-cycles of DL states have even length" | **NOT FOUND** | DL π-orbits themselves are classical: Errera 1921, Kittell 1935, Spencer-Brown, BKM 2026. Kittell's ζ has ring period 15 (checked: the note's π acts on link words with period 15). So "even length" is a genuine consequence of the law, not of local periodicity: π-cycle lengths are multiples of 30. No prior even-length or rigid statement was found. |
| Intro: LPC / "every Kempe class has a filled state" = Tilley's D-resolvability | **CONFIRMED** (definition read in full text) | Tilley 2017 §1 defines it, read in full: v is D-resolvable if every 4-colouring of G − v can be turned by Kempe exchanges in G − v into one that extends to v. This is exactly "every Kempe class of T − v has a filled state". Tilley's exchanges act on any non-empty proper subset of the pq-chains, which gives the same classes as single-chain exchanges. LPC is equivalent to this, given that π permutes each Kempe class. **"As far as we can tell" can become a definite statement, with the subset-of-chains remark.** |

---

## 1. The most important prior work the note does not cite

### 1a. Errera (1921) and Kittell (1935): the π-dynamics at a doubly locked pentagon

**Citation:** I. Kittell, *A group of operations on a partially colored map*, Bull. Amer. Math. Soc. 41(6) (1935) 407–413.
- Project Euclid: `bams/1183498239`.
- Full text read from `homepages.math.uic.edu/~kauffman/Kittell.pdf`.

**Errera's setting, as cited by Kittell.** Following Heawood and Errera, a map coloured except for one pentagon is called **impasse** when:
- the ring reads DBABC (one colour repeated);
- two intersecting Kempe circuits run from the vertex A to C and to D.

Kittell's impasse is exactly the note's DL state. The vertex is the region between the two repeated colours (x₁), and the two circuits are L₁ and L₂.

**The nine operations.** Kittell names the eight chains at an impasse and defines nine operations on them (the eight transpositions plus the identity), which generate the **impasse group**:
- left-hand and right-hand chains;
- left and right circuits;
- end tangent chain;
- left and right tangent chains;
- osculating chain.

**Matching π.** The note's π swaps α, γ on K_αγ(x₂), the chain through the repeated colour x₂ and the adjacent singleton x₃. This is Kittell's left-hand (or, mirrored, right-hand) **tangent chain** operation ζ (η).
- I checked this by relabelling: Kittell's ring B A B C D is the note's (α, β, α, γ, δ).
- A short script (scratchpad `piperiod.py`) confirms that π acts on link words with period 15. Kittell gives period 15 for ζ and η.

**Errera's map.** Errera exhibited a map on which the operation α (Kittell's α, swapping on the "left-hand chain"; the note's π is his ζ) stays impasse at every step and returns after 20 steps. Kittell shows that on Errera's map all powers of ζ stay impasse. So **infinite (cyclic) orbits of DL states under the note's π exist on a planar map, and have been known since 1921/1935.**
- These are not counterexamples to LPC: Kittell shows ε (end tangent chain) leaves impasse on that map.

**Consequences for the note.**
- The intro presents π as "the canonical exchange". It should credit Kittell (and Errera) for π, for the DL/impasse notion, and for the existence of DL π-cycles.
- Prop. 8 (N ≥ 8) is implicit in Kittell's eight named chains.
- The law and rigid isolation are **not** in Kittell. He studies the group and the periods, not chain counts.

### 1b. Spencer-Brown's Parity Lemma and parity pass; Baldridge–Kauffman–McCarty (2026)

**Kauffman 2005.** L. H. Kauffman, *Reformulating the map color theorem*, Discrete Math. 302 (2005) 145–172, doi:10.1016/j.disc.2004.07.031 (arXiv:math/0112266).
- §3 proves Spencer-Brown's **Parity Lemma**: in a Tait colouring of a planar cubic graph, the parity of the number of two-coloured circuits is preserved by a Kempe (simple) switch.
- Kauffman notes that a result of Tutte implies it. Tutte: *On the four-colour conjecture*, Proc. London Math. Soc. (2) 50 (1948) 137–149, doi:10.1112/plms/s2-50.2.137.
- Kauffman notes that it fails for non-planar graphs (Petersen minus an edge).

**Translation to the note.** Each two-coloured circuit in the dual separates the sphere, and p(A,B) + p(C,D) = (number of {i,j}-circuits) + 1. So N = 3 + (number of Kempe circuits), and the Parity Lemma says exactly **"N mod 2 is a Kempe invariant on a full sphere triangulation"**. The note's Theorem 9 and the law are hole versions of this.

**Kauffman 2005 §§4–5 on the five-region.** These sections use curve-count parity ("four and five have different parity") to analyse a 1-deficient formation. They then describe Spencer-Brown's **parity pass**: five Kempe-type moves (A–E) at a pentagon with one missing edge, returning to the same local configuration.

**BKM 2026.** S. Baldridge, L. H. Kauffman, B. McCarty, *A counterexample for the polar conjecture of Spencer-Brown*, arXiv:2607.22398 (24 Jul 2026), read in full.
- Their "bad configuration C" at a pentagon is the edge-colouring version of Heawood's interlocked chains, i.e. DL.
- They give a non-polar planar example on which the parity pass loops: 12 full passes, 60 steps, back to the original colouring.
- They remark that some parity-pass steps change the parity of the number of alternating paths and others do not, citing Spencer-Brown's 1980 Royal Society MS 734 and Kauffman 2005.
- **This is the nearest relative of the chain-parity law found.** It sits in a different move set (1-deficient edge colourings, with "complex" moves that shift the missing edge), and its precise statement is in unpublished or hard-to-access Spencer-Brown sources, so it was not verified.
- **Recommendation:** cite it, and say how the law differs: the vertex-colouring hole, the canonical π, an exact mod-4 formula, and the DL condition as the parity switch.
- BKM's open questions 5.1–5.3 (looping at every pentagon) are close to the note's NRC/LPC and to VH∃. Worth citing in the open-problems paragraph.

**Related papers (read, not used):**
- Spencer-Brown, *Laws of Form*, Appendix 5 (Bohmeier, 1997; 6th ed. 2015).
- Kauffman, *On the map theorem*, Discrete Math. 229 (2001) 171–184, doi:10.1016/S0012-365X(00)00207-7.
- Kauffman, *Map coloring and the vector cross product*, JCTB 48(2) (1990) 145–154, doi:10.1016/0095-8956(90)90114-F.

## 2. Degree of a 4-colouring and its Kempe invariance (makes Lemma 11 and the last sentence of Lemma 12 [cited])

**Mohar 2006.** B. Mohar, *Kempe equivalence of colorings*, in J. A. Bondy et al. (eds.), *Graph Theory in Paris*, Trends in Mathematics, Birkhäuser, Basel, 2006, pp. 287–297, doi:10.1007/978-3-7643-7400-6_22. Full text read.
- §5 defines Fisk's degree d(c) for triangulations of orientable surfaces.
- It reports that Tutte studied its parity and **observed that the parity is a Kempe invariant**.
- It states Tutte's 1999 question about similarity classes. Mohar–Singer answer that question.

**Mohar–Salas 2009.** B. Mohar, J. Salas, *A new Kempe invariant and the (non)-ergodicity of the Wang–Swendsen–Kotecký algorithm*, J. Phys. A 42 (2009) 225204, doi:10.1088/1751-8113/42/22/225204, arXiv:0901.1010. Full text read.
- Lemma 3.1 (Tutte): on a closed orientable triangulated surface, deg f ≡ Σ_{f(x)=a} deg x (mod 2) for each colour a.
- Cor. 3.3: deg f mod 2 is a Kempe invariant on every closed orientable surface.
- Main theorem: deg f mod 12 is a Kempe invariant for 3-colourable (Eulerian) triangulations.
- Their proof that Δdeg ≡ 0 counts the triangles of one colour type inside a Kempe region. This is the same mechanism as Lemma W.

**Translation.** cw − ccw = Σ_t (p_t − n_t) = 4 deg f, since the four triangles of ∂Δ³ give the same degree. With F = cw + ccw this gives cw = F/2 + 2 deg f. So:
- Lemma 11 is Fisk's degree combined with Tutte's mod-2 formula.
- "A Kempe exchange preserves cw mod 4" is exactly Kempe-invariance of deg f mod 2.
- The README's item 4 (Lemma W hand proof) depends on this sentence. It now has a published source, which removes one unreviewed step.

**Mohar–Singer 2021** (§3 below). §3 restates the Fisk degree and gives Thm 3 (surfaces): J_A ≡ deg f + n − 3 + g (mod 2), so deg f ≡ deg A (mod 2).

**Ozeki 2022.** K. Ozeki, *Kempe equivalence classes of cubic graphs embedded on the projective plane*, Combinatorica 42 (2022) 1451–1480, doi:10.1007/s00493-021-4330-2. Read via the YNU repository preprint.
- Proposition 10 there shows that the Kempe-invariant "signature" between two Tait colourings is +1. Ozeki notes that any two Tait colourings of a planar cubic graph have the same signature, citing Jaeger 1989 Prop. 1 (*On the Penrose number of cubic diagrams*, Discrete Math. 74 (1989) 85–97, doi:10.1016/0012-365X(89)90201-X), Kauffman 1990 Thm 3.2, and Kauffman 2005's Parity Lemma.
- This is the mod-2 shadow of the cw statements. It does not imply (i)–(iv).

## 3. Tutte's parity theorem and Mohar–Singer (Lemma 10; bibliography)

**Mohar–Singer.** B. Mohar, N. Singer, *The last temptation of William T. Tutte*, **European J. Combin. 91 (2021) 103221**, doi:10.1016/j.ejc.2020.103221 (Crossref); arXiv:1912.07205 (v1, 16 Dec 2019, the only version; the comment field still says "to appear"). Content checked on arXiv v1:
- **Thm 1 (Tutte):** for a plane triangulation and a colour class A, J_A(f) = 2|A| − deg(A) + n − 3, where J_A = Σ_{X≠A} p(A,X) − Σ(other pairs).
- **Cor. 2:** J_A is constant on colourings sharing a colour class, hence its parity is constant on a "similarity" component.
- **§3:** Fisk degree; deg f ≡ t_{ijl} (mod 2).
- **Thm 3:** the surface version, J_A ≡ deg f + n − 3 + g (mod 2).
- Hence the note's citation "[Thms. 1, 3]" for N ≡ n + 1 + deg(A) (mod 2) is **correct** for arXiv v1. Thm 1 gives J_A ≡ n + 1 + deg A, and J_A ≡ N mod 2. The published version's theorem numbering was **not** checked; it should be checked before submission.
- The note's Lemma 10 (pairwise form) summed over the three pairs at A gives Thm 1. The pairwise form is used in Tutte's proof as summarised there (e(A,B) + e(C,D) = n − 2 and Euler).
- **No hole, no mod-4 statement and no near-triangulation** appears in Mohar–Singer. This was checked by full-text extraction.

**Tutte 1969.** W. T. Tutte, *Even and odd 4-colorings*, in *Proof Techniques in Graph Theory* (Proc. Second Ann Arbor Graph Theory Conf., 1968), Academic Press, New York, 1969, pp. 161–169.
- Title, pages and year were confirmed from the reference lists of both Mohar–Singer and Mohar–Salas.
- The volume's editor (F. Harary) is from general knowledge, not from a fetched record.
- No Crossref/DOI record exists for the chapter.

## 4. Kempe classes of planar triangulations (context; no overlap with (i)–(iv))

All bibliographic data below were checked via Crossref.
- Fisk 1977: all 4-colourings of a 3-colourable (Eulerian) plane triangulation are Kempe-equivalent. Reported in Mohar 2006 Thm 4.1 and in Ito et al.
- Meyniel, *Les 5-colorations d'un graphe planaire forment une classe de commutation unique*, JCTB 24 (1978) 251–257.
- M. Las Vergnas, H. Meyniel, *Kempe classes and the Hadwiger conjecture*, JCTB 31 (1981) 95–104, doi:10.1016/S0095-8956(81)80014-7.
- C. Feghali, M. Johnson, D. Paulusma, *Kempe equivalence of colourings of cubic graphs*, European J. Combin. 59 (2017) 1–10, doi:10.1016/j.ejc.2016.06.008.
- M. Bonamy, N. Bousquet, C. Feghali, M. Johnson, *On a conjecture of Mohar concerning Kempe equivalence of regular graphs*, JCTB 135 (2019) 179–199, doi:10.1016/j.jctb.2018.08.002.
- T. Ito et al., *Reconfiguration of colorings in triangulations of the sphere*, arXiv:2210.17105 (SoCG 2023).
- B. Mohar, *Akempic triangulations with 4 odd vertices*, Discrete Math. 54 (1985) 23–29, doi:10.1016/0012-365X(85)90059-7. **Not read** (blocked). It is about odd-degree vertices and Kempe classes, so it is a lead for claim (i).
- S. Fisk, *The nonexistence of colorings*, JCTB 24 (1978) 247–248, doi:10.1016/0095-8956(78)90028-X. **Not read** (blocked).
  - Per Izmestiev (arXiv:1503.00605), it shows that a sphere triangulation with exactly two odd vertices has them non-adjacent.
  - The proof may use a Kempe-chain / odd-vertex parity argument close to the note's lock parity. **Recommend reading it before submission.**
- S. Fisk, *Combinatorial structure on triangulations I. The structure of four colorings*, Adv. Math. 11 (1973) 326–338, doi:10.1016/0001-8708(73)90015-7. **Not read.**

None of the papers read states a chain-count formula at a hole, a lock-parity criterion, or a law for N under a specific exchange.

## 5. Tilley

**Tilley 2017.** J. A. Tilley, *D-resolvability of vertices in planar graphs*, J. Graph Algorithms Appl. 21(4) (2017) 649–661, doi:10.7155/jgaa.00433.
- Bibliographic data correct. Full text read; the definition is in §1 and is summarised in the table above.
- Tilley's terms: "initial state" = the note's unfilled state; "solution state" = filled; a component of H_{G_v} with only initial states is "difficult".
- His conjecture "every vertex in a planar graph is D-resolvable" is stronger than 4CT. He supports it with computation on internally 6-connected triangulations up to order 125.
- **README item 12 can be closed:** LPC at a degree-5 vertex ⇔ v is D-resolvable. This holds because a class with no filled state contains no unfilled non-DL state (one step fills it) and π permutes each class.

**Follow-ups (for the intro):**
- J. A. Tilley, *Using Kempe exchanges to disentangle Kempe chains*, Math. Intelligencer 40(1) (2018) 50–54, doi:10.1007/s00283-017-9741-y. Not read (paywalled). By its title, it addresses Heawood entanglement, i.e. DL.
- J. A. Tilley, *Kempe-locking configurations*, Mathematics 6(12) (2018) 309, doi:10.3390/math6120309.
- J. A. Tilley, *The Birkhoff diamond as double agent*, arXiv:1809.02807.
- Semantic Scholar lists no other citing works for Tilley 2017.

## 6. Other items searched

- **Gonthier.** G. Gonthier, *Formal proof—the four-color theorem*, Notices AMS 55(11) (2008) 1382–1393 (confirmed). The technical report *A computer-checked proof of the Four Colour Theorem* (2005) was read.
  - Its Kempe-chain machinery uses **chromograms**: chords between ring edges carry a **parity bit**, and the sum of closing-bracket parities must match the ring-size parity.
  - So the parity of Kempe chains joining ring positions is classical (RSST/Gonthier). It is a cousin of lock parity, not the same statement: it says nothing about odd-degree vertices or N.
  - No chain-count lemma was found there.
- **Heawood's mod-3 congruence.** Heawood, *On the four-colour map theorem*, Quart. J. Pure Appl. Math. 29 (1898) 270–285, per secondary sources; not fetched. It labels vertices ±1 with face sums ≡ 0 mod 3. This is the local cw/ccw labelling behind Tait triples. No statement on chain counts.
- **Penrose / Jaeger / Aigner.** Penrose's planar evaluation gives a product of vertex signs equal to +1, i.e. cw − ccw ≡ 0 mod 4; this is weaker than Fisk's degree.
  - Jaeger 1989: cited above.
  - M. Aigner, *The Penrose polynomial of a plane graph*, Math. Ann. 307 (1997) 173–189, doi:10.1007/s002080050030.
  - No overlap with (i)–(iv) found.
- **Recent arXiv (2015–2026).** API searches "Kempe AND parity", "Kempe AND triangulation", "Kempe AND chains AND degree", "Tait AND coloring AND parity". The relevant hits:
  - BKM 2607.22398 (above);
  - Florek 2511.00485 (Kempe classes of a family of triangulations; no parity);
  - Liu 2309.09998 / 2309.09999 (Kempe chains at degree 5 in an extremal non-4-colourable MPG; skimmed abstracts only, no parity law);
  - Ito et al. 2210.17105.
  - Nothing on chain-count parity at a degree-5 vertex.
- **"number of Kempe chains" mod 2 or mod 4; "Kempe chain" with odd-degree vertices.** Web searches found only Tutte / Mohar–Singer / Mohar–Salas (parity of J_A and of the degree) and Kauffman's Parity Lemma.

## 7. Search log (abridged)

| query or source | result |
|---|---|
| arXiv 1912.07205 abs + ar5iv full text | Thms 1–3, bibliography; no hole / mod 4 |
| Crossref: Mohar–Singer | EJC 91 (2021) 103221 |
| Crossref: Fisk 1973/1977/1978, Mohar 1985, Tilley, RSST, Appel–Haken, Kempe, Kauffman ×3, Jaeger, Aigner, Ozeki, Las Vergnas–Meyniel, FJP, BBFJ, Tutte 1948 | metadata confirmed (§8) |
| Mohar 2006 PDF (author's reprint) | §5: degree parity Kempe-invariant (Tutte) |
| arXiv 0901.1010 full text | Lemma 3.1, Cor. 3.3, mod-12 invariant |
| ScienceDirect (Fisk, Mohar 1985) via fetch and in-app browser | blocked; not read |
| JGAA Tilley PDF | definition read |
| Gonthier report PDF | chromogram parity bits |
| arXiv math/0112266 (Kauffman) full text | Parity Lemma; parity pass at a five-region |
| arXiv 2607.22398 (BKM) full text | parity-pass loops; bad configuration = DL |
| Kittell 1935 PDF | impasse group; ζ/η = π; Errera's orbit |
| YNU preprint of Ozeki 2022 | signature / parity lemma references |
| Semantic Scholar citations of Tilley 2017, Mohar–Salas | follow-ups listed in §§4–5 |
| web: "Kempe chain" "odd number of odd vertices"; "number of Kempe chains" parity mod 4; Tait bicoloured cycles parity; D-resolvability 2019–2026; Kempe degree-five parity 2020–2026 | nothing beyond the above |

## 8. Bibliography: corrections to `main.tex` (not applied)

- **mohar2019 → mohar2021 (correction needed):** B. Mohar and N. Singer, The last temptation of William T. Tutte, *European J. Combin.* 91 (2021) 103221, doi:10.1016/j.ejc.2020.103221; arXiv:1912.07205. Re-check the theorem numbers "Thms 1, 3" against the published version.
- **fisk1977 (add issue + DOI):** S. Fisk, Geometric coloring theory, *Adv. Math.* 24(3) (1977) 298–340, doi:10.1016/0001-8708(77)90061-5. Crossref also has a duplicate record listing issue 2 (doi:10.1016/S0001-8708(77)80048-0, an abstracts listing); use the issue-3 DOI.
- **tutte1969 (add proceedings detail):** W. T. Tutte, Even and odd 4-colorings, in: *Proof Techniques in Graph Theory* (Proc. Second Ann Arbor Graph Theory Conf., 1968), F. Harary (ed.), Academic Press, New York, 1969, pp. 161–169. The editor is from memory and should be verified.
- **appel1977 (correct; add DOI):** K. Appel and W. Haken, Every planar map is four colorable. Part I: Discharging, *Illinois J. Math.* 21(3) (1977) 429–490, doi:10.1215/ijm/1256049011. Pages are standard; Crossref omits them.
- **robertson1997 (correct; add DOI):** N. Robertson, D. P. Sanders, P. Seymour, R. Thomas, The four-colour theorem, *J. Combin. Theory Ser. B* 70(1) (1997) 2–44, doi:10.1006/jctb.1997.1750.
- **gonthier (correct):** G. Gonthier, Formal proof—the four-color theorem, *Notices Amer. Math. Soc.* 55(11) (2008) 1382–1393.
- **tilley2017 (correct; add initial):** J. A. Tilley, D-resolvability of vertices in planar graphs, *J. Graph Algorithms Appl.* 21(4) (2017) 649–661, doi:10.7155/jgaa.00433.
- **kempe1879 (correct; add DOI):** A. B. Kempe, On the geographical problem of the four colours, *Amer. J. Math.* 2(3) (1879) 193–200, doi:10.2307/2369235.
- **heawood1890 (correct):** P. J. Heawood, Map-colour theorem, *Quart. J. Pure Appl. Math.* 24 (1890) 332–338. A few sources give 332–339.

**Entries to add:**
- Kittell 1935, Bull. AMS 41(6) 407–413.
- Errera 1921, *Du coloriage des cartes et de quelques questions d'analysis situs*, thèse, Gauthier-Villars, Paris, 66 pp. (as cited by Kittell).
- Kauffman 2005, Discrete Math. 302, 145–172.
- Spencer-Brown, *Laws of Form*, Appendix 5 (Bohmeier, 1997; 6th ed. 2015).
- Baldridge–Kauffman–McCarty, arXiv:2607.22398 (2026).
- Mohar 2006 (Graph Theory in Paris, 287–297).
- Mohar–Salas 2009 (J. Phys. A 42, 225204).
- Optionally: Tutte 1948 (PLMS (2) 50, 137–149), Tilley 2018 (Math. Intelligencer 40(1) 50–54), Fisk 1978 (JCTB 24(2) 247–248).

## 9. Recommended text changes (for the author; not applied)

1. **Lemma 11:** relabel from [hand] to [cited: Fisk 1977; Tutte 1969 via Mohar–Salas 2009 Lemma 3.1].
2. **Lemma 12, last sentence:** relabel to [cited: Tutte, reported in Mohar 2006 §5; Mohar–Salas 2009 Cor. 3.3]. This removes an unreviewed step from the hand proof of Lemma W.
3. **Intro:**
   - credit π to Kittell's tangent-chain operation;
   - credit DL π-orbits to Errera/Kittell;
   - mention Spencer-Brown's parity pass and BKM 2026;
   - say that Theorem 9 and the law extend the Spencer-Brown/Tutte parity lemma (N mod 2 is a Kempe invariant on the sphere) to a degree-5 hole.
4. **Tilley sentence:** change "as far as we can tell" to a definite equivalence, after reading the definition.
5. **Before claiming (i) and (ii) are new:** read Fisk 1977 (disc degree and boundary words), Fisk 1978 and Mohar 1985 (odd vertices). These were inaccessible here and are the most likely places for an overlap with lock parity or the hole formula.

## Correction (9 Oct 2026, after RefereeReport2.md, item N2)

Row (iv) of the table above says that "even length" of DL π-cycles is "a genuine consequence of the law, not of local periodicity". **That is wrong.** Second-ring periodicity already gives it:
- each of the 120 unfilled link words has π-orbit of length exactly 15, so 15 | L for a DL π-cycle of length L;
- the compiled Lean theorem `allDL_cycle_length_dvd_ten` (`QuarterBitDynamics.lean`, commit 4d257b72 of 7 Oct; built by `check.sh`) gives 10 | L from the outer-vertex bits, with no chain counts.

Together these give 30 | L, and hence even length, without the law. The law's evenness is a consistency check only. The rest of row (iv) (no prior even-length or rigid-isolation statement found) is unaffected. The row above is left as written; `main.tex` was corrected.
