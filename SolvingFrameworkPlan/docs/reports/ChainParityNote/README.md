# Chain-parity note (draft of 8 Oct 2026, revised twice on 9 Oct 2026)

This is a short standalone note: *Kempe chains around a degree-five vertex: a mod-4 parity formula and a parity law*.
- **Title change (9 Oct).** The 8 Oct title said "a mod-4 chain count". The referee (E1) pointed out that the identity 2N ≡ … (mod 4) determines N only mod 2; the mod-4 content is that cw enters mod 4. The title now says "a mod-4 parity formula". Alternative if Kyle prefers: "…: a chain-count parity formula and a parity law". The working title was "A parity law for Kempe chains at a degree-five vertex".
- **Revision of 9 Oct.** `main.tex` was revised to answer `RefereeReport.md` (E1, G1–G4, M1–M6) and `LiteratureCheck.md` (prior work, relabels, bibliography). The disclosure section (§7) was then adapted to the note in commit 70a2eed5.
- **Second revision of 9 Oct.** `main.tex` was revised again to answer `RefereeReport2.md` (N1–N6); see the status list below.
- It is separate from the VH∃ record (`../VHE-paper/`), following the coordinator's paper decision of 8 Oct (`docs/working/CoordinatorPlan.md`, "Paused").
- Author: Kyle Mathewson, as in the VH∃ paper.
- Not committed. Not posted anywhere.

## Files and build

- `main.tex` is self-contained, with an inline bibliography. There is no `references.bib`.
- Build: run `pdflatex -halt-on-error main.tex` twice. Last build (9 Oct, after the second revision): 12 pages, exit 0 on both passes, no undefined references, no overfull boxes.
  - Note: `\S` inside `\cite[...]` breaks this TeX Live (font-expansion error with microtype), so section references are written "Sec.".
  - The build was done in a scratch directory; no PDF is kept here.
  - Packages used: amsmath, amssymb, amsthm, url, microtype, hyperref, geometry, enumitem.

## Label policy used

- Only results that are compiled in Lean **and** covered by audit J14 (`docs/working/Audit-2026-10-08`) are called Theorem, Proposition or Corollary.
- Everything else carries a label from the VH∃ convention: [hand], [computed], [cited] or [open].
- Every `\lean{…}` name in `main.tex` was checked by grep against `docs/working/StudioMathLean/Mathlib/Combinatorics/SimpleGraph/PlaneMap/*.lean`, or against the base library (`SphericalMap`, `Fills`, `Triangulated`).
- `SHA256SUMS` checks out 40/40. The five module hashes quoted in §6 match the audit's table.

## TODO before this goes anywhere

Status after the 9 Oct revision. Items marked **done** were addressed in `main.tex`; the rest remain.

### Kyle's decisions (remaining)

1. **Disclosure (§7).** Adapted to the note in commit 70a2eed5 ("this note"; coordinator and sub-agents; review/audit roles; the author's actions). It awaits Kyle's final OK, as the LaTeX comment says. The tag-name placeholder must be set.
2. **Title.** Proposed: "Kempe chains around a degree-five vertex: a mod-4 parity formula and a parity law" (see above). Kyle to confirm.
3. **Where to post, and whether to cite the VH∃ draft.** [25] still points to a draft inside the repository.

### Referee report (9 Oct): status

- **E1 (done).** Abstract: "an identity mod 4 for 2N(c) … gives the parity of N(c)". Theorem F renamed "Chain-count identity", with a sentence after it saying it determines N mod 2 only. Title changed.
- **G1 (done, not re-reviewed).** The converse of Prop. 2 now uses the boundary walk of the face R of T[U] containing x4 (U = Q ∪ {v}; v is a leaf), with the corner lists, the non-emptiness argument, and the gluing between corners written out; L1 is treated explicitly. The repaired text should get one more independent read.
- **G2 (done).** §5 "Off the sphere" now says (∗) and the link-free half of Lemma W hold off the sphere, and lists, for every other result, the torus data: Prop. 2 / Thm 3; Prop. 4 (referee: 1,607/6,381; 288/1,429 genus 2); Thm 5 (2G residue); Lemma W at π (fails only with x0 ∈ K); law; Cor. 7; Thm 8 (referee: 903/2,090; 371/752). The abstract says "Apart from one local identity and the link-free half of one lemma, every result fails on the torus".
- **G3 (done).** Law off the sphere: 282/544 (TrackC) and 1,497/3,317 (referee) at π-steps with x0 ∉ K; 2,757/3,064 with x0 ∈ K.
- **G4 (done).** Intro defines the extension of π to all states (Lean `piMove`, one specified exchange at filled and singly locked states) before "permutes each Kempe class"; §6 says the same.
- **M1 (done).** n = 22 example: "261,093 greedy reductions … to order 20 found none (not an exhaustive search)".
- **M2 (done).** Census now orders 22–34: near-rigid run reaches 8 at order 33 and stays 8 at order 34 (Census34). Also added: 98 all-DL π-cycles at order 34, all in classes with filled states.
- **M3, M4 (done).** Abstract: "a rigid colouring (eight chains, the minimum for doubly locked colourings)"; "the parity law, together with the local matching structure, does not exclude …". §2 notes that other unfilled states can have N = 6.
- **M5 (done).** Chain count is now κ(p,q); cw(c) (faces of T avoiding v) vs cw_S, cw_{T°} (all faces); one label per lemma; Lemmas 10–13 stated for loopless surfaces with faces on three distinct vertices; §3 header names the surface-general exception; Lean table says `lemmaW_linkFree` assumes `StarHyp`.
- **M6 (done).** Lemma W's hand proof is now [hand] (reviewed by the referee); its link-free step cites Lemma 12 [cited]. Lemma 10's proof is marked "checked by the referee". Prop. 2's converse is marked as repaired and not re-reviewed.
- **New label.** Off-sphere counts that come only from the referee's code are marked [computed¹] (one program, two runs), since [computed] requires a second implementation. To upgrade them, rerun with a second program.

### Second referee report (9 Oct, `RefereeReport2.md`): status

All items applied in `main.tex`.
- **N1 (done).** The false sentence "other unfilled states can have N = 6" is gone. §2 now states N ≥ 8 at every unfilled state [hand], with the referee's short argument via Prop. 2 (and the referee's sample minimum of 8 over 48,000+ non-DL states, [computed¹]). Abstract: "the minimum for unfilled colourings". §5 adds that this bound rests on Prop. 2 and is not claimed off the sphere. The provenance of the first report's N = 6 (presumably off-sphere) was not established, so the note does not attribute it to the torus.
- **N2 (done).** The remark after Cor. 7 now says: every one of the 120 unfilled link words has π-orbit length exactly 15; with the compiled `allDL_cycle_length_dvd_ten` (`QuarterBitDynamics`, 10 | L) this gives 30 | L without the law, so the law's evenness is a consistency check. Census lengths are up to renaming (length 20 up to renaming = absolute length 60; `_recol` gives 10 | 20). The §5 census sentence says "counted up to renaming the colours". `LiteratureCheck.md` row (iv) corrected by an appended note. VH∃ paper: "all of length 20 up to renaming the colours" (only that edit).
- **N3 (done).** Abstract: "every main result fails on the torus"; §5: "every other result of Section 3", noting that Lemmas 12–13 hold on every closed oriented surface.
- **N4 (done).** Kittell's ζ "(or his η, by mirror symmetry)"; parity pass cited as Kauffman Sec. 5; Kauffman Sec. 4 (4-vs-5 curve count at a 1-deficient formation) cited as the nearest published antecedent of Thm 8 and the law; BKM's configuration 𝒞 attributed in their words, with "Heawood's interlocked chains" as our reading; their parity statement "partly in Kauffman Sec. 5 and partly unpublished"; Spencer-Brown's parity mills (built from Kittell impasse-group moves, per BKM) mentioned, with "whether a mill iterates ζ = π was not determined"; Questions 5.1–5.2 reworded to "admit a looping 1-deficient colouring". Added one clause that Lemmas 12–13 for the multigraph T° follow from the note's own proof of Lemma 12.
- **N5 (done).** e₀ := e_m; leaf clause (e_i = e_{i+1}: the list is the deg − 1 ≥ 2 other neighbours); the sentence after the proof now says the repair was re-reviewed in a second round (RefereeReport2.md) and tested on 1.83M sphere states.
- **N6 (done).** LaTeX comment above §7 and README item 1 updated.

### Literature check (9 Oct): status

- **Done.** Intro now has "Prior work" and "What is new" paragraphs: Errera 1921 / Kittell 1935 (impasse = DL; π = Kittell's tangent-chain ζ, period 15, checked by a short script and against the scanned paper; DL π-cycles on Errera's map; N ≥ 8 implicit in Kittell's eight chains); Spencer-Brown's Parity Lemma via Kauffman 2005 (no-hole N mod 2 invariance; Thm 8 and the law are hole versions); BKM 2026 (parity pass loops; bad configuration; parity remark; Questions 5.1–5.2 positioned against LPC/NRC in §5); Mohar 2006 and Mohar–Salas 2009 (Kempe invariance of degree parity). Lemma 11 (Fisk mod 4) and the new Lemma 12 (Kempe invariance of cw mod 4, formerly the last sentence of Lemma F0) are [cited]. Tilley's D-resolvability equivalence is now stated definitely, with the subset-of-chains remark.
- **Done, then corrected (N2).** π-orbits of link words have length exactly 15, so DL π-cycles have length divisible by 30 [hand]; this follows from 15 | L and the compiled 10 | L without the law (see the correction appended to `LiteratureCheck.md`). Census cycles of length 20 are counted up to renaming of colours (absolute length 60), so there is no conflict.
- **Done.** Bibliography: Mohar–Singer → EJC 91 (2021) 103221, doi, with "journal numbering to check"; DOIs added for Appel–Haken, RSST, Kempe, Fisk 1977 (issue 3), Tilley (initial J. A.); entries added for Kittell, Errera, Kauffman 2005, Spencer-Brown, BKM, Mohar 2006, Mohar–Salas, Tutte 1948, Fisk 1973, Fisk 1978, Mohar 1985, Gonthier 2005 report. Verified on 9 Oct via arXiv abstract pages (BKM, Kauffman, Mohar–Salas), arXiv HTML (BKM questions), Crossref (Mohar–Singer, Kauffman, Mohar 2006, Kittell, Fisk 1973/1977/1978, Mohar 1985, Kempe, RSST, Appel–Haken, Tutte 1948) and the scanned Kittell paper.
- **Remaining.**
  - Read Fisk 1973, 1977, 1978 and Mohar 1985 in full (paywalled). The note says they were not read and must be checked before submission; they are the most likely overlap with the hole identity and lock parity.
  - Check Mohar–Singer's theorem numbers in the published version (the note cites arXiv v1 numbering).
  - Tutte 1969: editor (F. Harary) unverified; omitted from the entry.
  - Gonthier 2005 technical report: not re-fetched in this revision; check the exact report title/number.
  - Errera 1921 and Spencer-Brown's *Laws of Form* were not read; marked so in the bibliography.
  - Spencer-Brown's unpublished parity-pass parity statement (Royal Society MS 734, via BKM) was not seen; the note says so.
  - Optional: Tilley 2018 (Math. Intelligencer; Kempe-locking configurations) for the intro.

### Claims still unreviewed or hand-only

4. ~~Prop. 2 converse: repaired text (G1) not re-reviewed.~~ **Closed:** re-reviewed line by line in `RefereeReport2.md` §3, 0 failures on 1.83M states.
5. Genus residue 2G mod 4 (§5): [hand], not reviewed; now checked numerically by the referee (35,241 torus and 3,038 genus-2 states; G = 3 occurs).
6. Matching form (§5): "a state is determined by M_t", "N = 7 + k(M_{t−1} ∪ M_t)", "every near-rigid cycle yields such a sequence": [hand, unreviewed]. The referee checked N = 7 + k(…) at 838 steps but not "determined by M_t".
7. The n = 22 example is abstract (non-planar matching form), not a surface triangulation; TrackU's off-sphere discrepancy is unresolved.
8. "π-cycles have length divisible by 30" [hand]: checked by the second referee (`RefereeReport2.md` N2, §4: all 120 link words have orbit length exactly 15); it follows from 15 | L and the compiled `allDL_cycle_length_dvd_ten`, without the law.
8a. "N ≥ 8 at every unfilled state" [hand]: the second referee's argument (N1), not separately re-reviewed; 48,000+ sampled states [computed¹].
9. Numbers: all figures in the 8 Oct draft were checked against sources by the referee (RefereeReport §6). New figures added in this revision come from RefereeReport §2 (marked [computed¹]) and `docs/working/Census34/README.md`.

### Lean follow-ups (optional, unchanged)

10. Write a frozen challenge file and bridge for `ConjectureF` / `ChainParityLaw`. None exists, and the note says so.
11. Write a two-line Lean corollary "no Kempe class consists only of rigid states" (audit W2). It is labelled [hand] in the note.
12. Optionally drop the no-isolated-vertex hypothesis from the law and rigid-isolation corollaries (TrackC §9.4).
13. Rigid states are not exhibited in Lean, so the hypothesis of `rigid_isolation` is shown satisfiable only through its `DoublyLocked` part. The note says this.

## Sanity check run while writing

The note fixes these conventions:
- the link is labelled along the face orientation;
- η is read from (α+β, α+γ, α+δ);
- the fill faces and their cw status are as in the proof of Theorem 5 and Lemma W.

Two independent scripts were written in the session scratchpad; they are not in the repository.
- A table check: T1, the fill-face statuses for c and for πc, and η(πc) = η(c). Result: 0 mismatches.
- Random sphere triangulations, n = 10–30, with Kempe walks: 27,046 unfilled states, 7,417 of them doubly locked. There were 0 failures of:
  - F;
  - Lemma W at π;
  - Kempe duality;
  - L1(πc) = 1;
  - the law.
