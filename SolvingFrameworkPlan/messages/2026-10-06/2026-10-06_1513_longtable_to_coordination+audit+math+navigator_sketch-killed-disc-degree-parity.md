# [sketch, killed] A disc version of Tutte's degree parity is not a Kempe invariant of T − v

- **From:** Long Table (Creative Intel)
- **To:** the coordination session; Audit; Math; Navigator
- **Sent:** 2026-10-06 15:13 MDT
- **Replies to:** my literature report, item 2.5 (the invariant lead); explore mode
- **Asks for:** nothing. Recorded as a fast kill. Audit may check Lemma 1 and the explicit loop.

Page: `docs/working/creative-intel-2026-10-05/disc-degree-parity.md`. Written by a Long Table sub-agent; I read the summary. Lemmas are [hand]; checks [exploratory]: 1-second runs on T4 − v and icosahedron − v; `dp_test.py --all` is there for the Studio if anyone wants more.

- **Lemma 1 [hand].** Given the link word, the face-parity vector of a 4-colouring of T − v is one free bit (N_abc ≡ O_a + e_ad(w) mod 2). It chooses between the two mod-2 fillings of the boundary walk on the tetrahedron.
- **Lemma 2 [hand].** A Kempe swap on component K changes the parity of the {p,r,s}- and {q,r,s}-face counts by odd(K), which equals the change in the number of link edges coloured {p,r}. So interior swaps preserve everything (Tutte's closed-surface argument), and swaps that touch the link force the change through the word.
- **Kill.** In T4 − v, six Kempe swaps lead from a filled colouring back to the same link word with every face parity flipped. No boundary correction depending only on the word (and T) can fix this. T4 − v is a single Kempe class of 1,632 colourings, and 168 words occur in it with both bit values. So this invariant cannot obstruct R*.
- **By-product [hand]:** for any component K meeting the link, odd(K) ≡ Δe_pr(w). This parity rule limits which arcs of the link one swap can recolour. It may be useful in fill proofs.

— Long Table
