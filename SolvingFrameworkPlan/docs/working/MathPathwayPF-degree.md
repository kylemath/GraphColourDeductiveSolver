# Pathway P-F: topological degree invariants at a degree-5 hole

Status: DONE (exploratory, Math worker, 2026-10-06). Verdict: **killed as a radius / targetless-class tool**; one clean structural lemma survives (§2). Labels: [hand] [cited] [computed] [open]. CPU used: about 1.5 min on 1 core.

Script: `MathPathwayPF-scripts/degree_invariants.py` (run from that folder; needs `../MathRadiusCensus/gen_tri`). Throwaway analysis snippets (link-swap table, parity test) were run from the scratchpad; their outputs are summarised in §3.

## 0. Literature (what was actually read)

- [cited, search-result abstract only; full text NOT read: PDF fetch failed] Mohar & Salas (arXiv 0901.1010, "A new Kempe invariant and the (non)-ergodicity of the Wang-Swendsen-Kotecky algorithm"): for *three-colourable* (Eulerian) triangulations of a closed oriented surface, the degree of a 4-colouring mod 12 is invariant under Kempe changes. Same abstract: Fisk (1973) proved all 4-colourings of a 3-colourable sphere triangulation are Kempe-equivalent.
- Fisk 1977 ("Geometric coloring theory", Adv. Math.) and Mohar, "Kempe equivalence of colorings" (2006, users.fmf.uni-lj.si/mohar/Reprints/2006/BM06_GTP06_Bondy_KempeEquivalence.pdf) were located but **not read** (PDF text could not be extracted, then web fetch hit a session limit). Nothing from them is quoted. Anyone citing the definitions below as "Fisk's" must check them first.
- Our triangulations have degree-5 vertices, so they are not Eulerian; the mod-12 theorem does not apply, and §3 shows it fails here (free swaps change the degree by 2).

## 1. Definitions [hand]

Orient T (a sphere). Fix a hole v of degree 5 with oriented link x0..x4 (the order induced by the star faces (v, x_i, x_{i+1})). D = T minus the open star of v, an oriented disc with boundary the link. A state s is a proper 4-colouring c of T - v, with **labelled** colours 0..3 (not up to permutation; an odd colour permutation reverses every sign below).

- **Signed triple counts.** For k in {0,1,2,3}, n_k(s) = sum over faces (p,q,r) of D (oriented) whose colours miss k, of sign(c(p), c(q), c(r), k) as a permutation of (0,1,2,3). This is the pushforward c_*[D] as a 2-chain on the boundary of the tetrahedron, written in the basis of its four faces F_k (F_k = face missing colour k, with the boundary orientation). On a closed sphere all four n_k are equal: that common value is the degree of c (sanity-checked on every filled state below: the extension by the missing colour gives four equal counts).
- **Boundary loop.** gamma(s) = (c(x0), ..., c(x4)), a closed walk of length 5 in K4. A proper 5-cycle colouring always has a backtrack (some x_j, x_{j+2} share a colour), and cyclic free reduction always leaves an **oriented triangle** of K4 (proof: a closed walk of odd length 5 in K4 must repeat a colour at distance 2; cancelling it gives length 3, which has no backtrack). Write the reduced triangle as boundary of eps * F_m: m(s) = its missing colour, eps(s) = +-1 its orientation.
  - Unfilled state, link a b a c d (repeated pair x0, x2, apex x1): reduced loop a c d, so m = b = the **apex colour**.
  - Filled state, link a b a b c (counts 2,2,1): reduced loop a b c, so m = the colour absent from the link = the colour v receives.
- So the "class of the link loop" is just the pair (m, eps): 8 values, a function of the 5 link colours.

## 2. Results

**Lemma 1 (shape of the triple counts) [hand, computed].** For every state, n(s) = N(s)(1,1,1,1) - eps(s) e_m(s) for an integer N(s). (Up to my global sign convention: computed, sp = n_m - N equals -eps in all 1632 + 2400 + ... states.)
Proof [hand]: the boundary of the 2-chain c_*[D] is the 1-cycle gamma. Backtracks cancel as chains, so gamma = boundary of (eps F_m) as a 1-cycle. Two 2-chains on the tetrahedron surface with the same boundary differ by a multiple of the fundamental cycle F_0+F_1+F_2+F_3 (H_2 of the sphere is Z, and there are no 3-cells). Hence c_*[D] = -eps F_m + N * sum F_k (sign per convention). QED.
Consequence [hand, computed]: for a filled state, the cone from v (coloured m) adds nothing to F_m (its triangles all contain m) and +-1 to each other face, so deg(extension) = n_m(D) = N - eps (checked: on every filled state the four extended counts are equal and equal n_m).
So the whole degree information of a state is **one integer N(s) plus the boundary data (m, eps)**.

**Lemma 2 (swaps not meeting the link) [hand, computed].** If the swapped (p,q)-component K contains no link vertex, gamma is unchanged and N changes by -2t, t = signed count of triangles of D with colour set {p,q,r} having their p,q-edge in K (the same t for both r). Proof: only faces with a p-q edge in K change sign (a transposition reverses orientation); faces with one of p,q move between F_p and F_q and do not touch n_r for r not in {p,q}; by Lemma 1 the change is the same constant on all four counts, read off at index r. QED. [computed] t takes the values 0, +-1, +-2, +-3 (T4: deltas up to +-6); so **the degree mod 12 (Mohar-Salas) and even mod 4 are not Kempe invariants here; only N mod 2 survives link-free swaps.**

**Lemma 3 (swaps through the link) [hand for gamma, computed for N].** The new loop is gamma with p and q exchanged at the link vertices lying in K (a deterministic rule on the 5 link colours), hence (m, eps) is recomputed from it; m changes in some cases and not others (table in the scratch run). The change of N is **not** determined by the link data: for one and the same old/new link pattern, Delta N takes up to 7 different values in T4 (e.g. link pattern 01203 -> 02103, normalised by the old link: (Delta N)*sp in {-6,-4,-2,0,2,4,8}), of both parities when m changes. So no local rule for N.

**"Filled" in these terms [hand].** Filled <=> the link misses a colour <=> m(s) is absent from the link. Unfilled <=> m(s) is the apex colour (present once). Filledness is a property of gamma alone; N plays no role.

## 3. Computation [computed] (labelled states = 24 x canonical)

| graph / hole | labelled states | Kempe classes (labelled) | N range | filled-extension degrees | DL radii |
|---|---|---|---|---|---|
| T4, v=4 | 1632 (68 canon) | 1 | -4..4 | -3..3 | 2,3,4 |
| A_3 centre | 2400 (100) | 1 | -3..3 | -2,0,2 | 2,3 |
| A_4 centre | 12480 (520) | 1 | -3..3 | -4..4 | 2 |
| A_5 centre | 65280 (2720) | 1 | -4..4 | -5..5 | 2 |
| icosahedron, any v | 480 (20) | 1 | -2,0,2 | -3, 3 only | (no DL) |
| order-14 min-deg-5 (unique, `gen_tri 14 --all`), all 12 holes | 960 (40) each | 1 each | -3..3 | -4,-3,-1,0,1,3,4 | 2 |

Canonical counts and DL radius histograms agree with MathConjectureR.md (T4: 68 canonical, DL radii {2,3,4}; A_3: radii {2,3}). Lemma 1 was asserted for every state and never failed.

DL states, (radius, |N|): T4 {(2,0):48, (2,1):96, (2,2):168, (2,3):24, (2,4):24, (3,1):96, (4,2):48}; A_3 {(2,0):120, (2,2):120, (2,3):240, (3,0):120, (3,2):120}. With sign kept, T4 radius-4 DL states have (N, sp) in {(2,1), (-2,-1)}; radius-2 DL states include 48 states with (2,1) and 48 with (-2,-1).

Parity test: is N mod 2 a function of the labelled link colouring? No: T4 168/240, A_3 120/240, A_4 240/240, order-14 48/240 link colourings occur with both parities (icosahedron: 0/240, too small to mean anything).

## 4. Answers to the questions

- **(3a) Do high-radius DL states share an invariant value? No [computed].** The radius-4 DL states of T4 have |N| = 2, N*eps fixed, but radius-2 DL states take exactly those values too. Same at A_3 radius 3 (|N| in {0,2}, shared with radius 2). KILLED: the degree does not see the radius.
- **(3b) A Kempe-class invariant that is nonzero exactly on targetless classes? None from the degree, and on this data none of any kind [computed].** At every hole tested the labelled Kempe graph is connected (1 class), so every Kempe invariant is constant on the whole state space, and there are no targetless classes to separate. Structurally [hand]: N is not invariant (Lemma 2, changes by 2t), mod 2 is the only modulus that survives link-free swaps, and link swaps change N by amounts of either parity not fixed by the link (Lemma 3), and no "N mod 2 = f(link)" law holds. KILLED.
- **(1) Where the degree could still matter [open].** In a hypothetical targetless class every state has m = apex colour forever. Lemma 1 says such a class lives in the 2-chain picture as "D wraps the sphere N times plus a face". Nothing forces N to be constrained, so I see no obstruction argument from it.

## 5. One-page sketch

- **Claim (tested):** some function of the Fisk-type degree of a state at a degree-5 hole (signed triple counts of the disc D, plus the winding class of the link loop) is constant on Kempe classes and detects classes with no filled state; or at least separates high-radius doubly locked states.
- **Why it might hold:** for Eulerian triangulations the degree mod 12 is a Kempe invariant (Mohar-Salas, abstract), and it separates Kempe classes there; the link loop's winding class is a topological datum that a fill must change (filled <=> m absent from link).
- **Hand example (icosahedron, v any vertex):** T - v has 20 canonical 4-colourings, 10 filled. Every filled state extends to a colouring of the icosahedron of degree +-3 [computed]; unfilled states have N in {0, +-2} and one of the 8 loop classes; one link-touching swap reaches a filled state from every unfilled state (radius 1), and the labelled Kempe graph is connected.
- **Kill test result:** on T4, A_3, A_4, A_5, icosahedron and all 12 holes of the order-14 triangulation, (i) the shape n = N(1,1,1,1) - eps e_m holds always (Lemma 1, proved); (ii) Kempe swaps change N by even amounts off the link and by arbitrary amounts through it, so neither N nor N mod 2 nor N mod 12 is a class invariant; (iii) each hole has a single labelled Kempe class; (iv) radius-4 DL states of T4 share (N, eps) with radius-2 DL states. **Pathway P-F is killed** for the radius question and for characterising targetless classes. The surviving piece is Lemma 1 (all degree information of a state = one integer N plus the link's reduced triangle), which may be useful as bookkeeping elsewhere but carries no filling information.

## 6. Killed lines (with reasons)

- K1 "degree mod 12 is a Kempe invariant at the hole": false here, link-free swaps change N by +-2 (non-Eulerian).
- K2 "N mod 2 is determined by the link colouring (a parity law)": false on T4, A_3, A_4, order 14.
- K3 "high-radius DL states have a distinctive (N, eps)": false, values shared with radius-2 DL states.
- K4 "a degree invariant characterises targetless classes": no data to support it (no such classes; every hole has one labelled class), and Lemmas 2-3 rule out N-based invariants.

## 7. Open

- [open] Full text of Fisk 1977 and Mohar 2006 not read; whether either has a relative (disc-with-boundary) version of the degree invariant is unchecked.
