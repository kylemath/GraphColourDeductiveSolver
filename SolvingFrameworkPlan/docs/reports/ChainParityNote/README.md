# Chain-parity note (draft of 8 Oct 2026, revised 9 Oct 2026)

This is a short standalone note: *Kempe chains around a degree-five vertex: a mod-4 parity formula and a parity law*.
- **Title change (9 Oct).** The 8 Oct title said "a mod-4 chain count". The referee (E1) pointed out that the identity 2N ≡ … (mod 4) determines N only mod 2; the mod-4 content is that cw enters mod 4. The title now says "a mod-4 parity formula". Alternative if Kyle prefers: "…: a chain-count parity formula and a parity law". The working title was "A parity law for Kempe chains at a degree-five vertex".
- **Revision of 9 Oct.** `main.tex` was revised to answer `RefereeReport.md` (E1, G1–G4, M1–M6) and `LiteratureCheck.md` (prior work, relabels, bibliography). The disclosure section (§7) was left unchanged.
- It is separate from the VH∃ record (`../VHE-paper/`), following the coordinator's paper decision of 8 Oct (`docs/working/CoordinatorPlan.md`, "Paused").
- Author: Kyle Mathewson, as in the VH∃ paper.
- Not committed. Not posted anywhere.

## Files and build

- `main.tex` is self-contained, with an inline bibliography. There is no `references.bib`.
- Build: run `pdflatex -halt-on-error main.tex` twice. Last build (9 Oct, after revision): 11 pages, exit 0 on both passes, no undefined references, no overfull boxes.
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

1. **Disclosure (§7).** Still the VH∃ disclosure text, unchanged, with the LaTeX comment marking it for Kyle's approval. It still says "this paper", refers to `AUTHOR-RECORD.md` "beside" the VH∃ paper, and describes session roles that did not all touch this note. The tag-name placeholder must be set.
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

### Literature check (9 Oct): status

- **Done.** Intro now has "Prior work" and "What is new" paragraphs: Errera 1921 / Kittell 1935 (impasse = DL; π = Kittell's tangent-chain ζ, period 15, checked by a short script and against the scanned paper; DL π-cycles on Errera's map; N ≥ 8 implicit in Kittell's eight chains); Spencer-Brown's Parity Lemma via Kauffman 2005 (no-hole N mod 2 invariance; Thm 8 and the law are hole versions); BKM 2026 (parity pass loops; bad configuration; parity remark; Questions 5.1–5.2 positioned against LPC/NRC in §5); Mohar 2006 and Mohar–Salas 2009 (Kempe invariance of degree parity). Lemma 11 (Fisk mod 4) and the new Lemma 12 (Kempe invariance of cw mod 4, formerly the last sentence of Lemma F0) are [cited]. Tilley's D-resolvability equivalence is now stated definitely, with the subset-of-chains remark.
- **Done.** New consequence noted: π acts on link colours with period 15, so DL π-cycles have length divisible by 30 [hand]. (Census cycles of length 20 are counted up to renaming of colours, so there is no conflict.)
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

4. Prop. 2 converse: repaired text (G1) not re-reviewed.
5. Genus residue 2G mod 4 (§5): [hand], not reviewed; now checked numerically by the referee (35,241 torus and 3,038 genus-2 states; G = 3 occurs).
6. Matching form (§5): "a state is determined by M_t", "N = 7 + k(M_{t−1} ∪ M_t)", "every near-rigid cycle yields such a sequence": [hand, unreviewed]. The referee checked N = 7 + k(…) at 838 steps but not "determined by M_t".
7. The n = 22 example is abstract (non-planar matching form), not a surface triangulation; TrackU's off-sphere discrepancy is unresolved.
8. "π-cycles have length divisible by 30" [hand]: new in this revision, unreviewed (a one-line argument plus a finite check).
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
