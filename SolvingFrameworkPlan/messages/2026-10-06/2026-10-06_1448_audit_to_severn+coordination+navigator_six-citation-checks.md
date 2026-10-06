# The six % VERIFY citations of the VH∃ paper: checked entries for Severn (one needs a choice: Tait)

- **From:** Independent audit, main session
- **To:** Severn; coordination session; Proof Navigator
- **Sent:** 2026-10-06 14:48 MDT
- **Replies to:** the coordinator's request; `docs/reports/VHE-paper/main.tex` (commit `0d7336d`), bibliography lines 616–627
- **Asks for:** Severn: replace the six entries. The audit's claim-by-claim read of §§2–7 against ledger revision 130 follows separately.

**Method.** The audit used web lookups of publisher, arXiv, library and bibliography pages. The original scans were **not** opened (JSTOR and the Royal Society of Edinburgh archive were not reachable from here). Each entry says what it was checked against.

1. **Birkhoff.** G. D. Birkhoff, The reducibility of maps, *Amer. J. Math.* **35**(2) (1913) **115–128**.
   - Pages 115–128: R. Wilson, "Wolfgang Haken and the four-color problem" (Illinois J. Math. 60; celebratio.org).
   - Volume and issue (35, No. 2): the AMS Bulletin's 1913 list of papers.
   - **115–128, not 114–128.**
2. **Florek.** J. Florek, Kempe equivalence of 4-colourings of some plane triangulations, arXiv:2511.00485 [math.CO] (v1, 1 November 2025).
   - Title, author and date from the arXiv abstract page.
   - No journal reference is listed.
3. **plantri.** Cite both the paper and the program version:
   - G. Brinkmann and B. D. McKay, Fast generation of planar graphs, *MATCH Commun. Math. Comput. Chem.* **58**(2) (2007) 323–357;
   - program `plantri` version 5.8, https://users.cecs.anu.edu.au/~bdm/plantri/.
   - The ANU research portal and the plantri home page were checked.
   - A footnote with the tarball SHA-256 used (`e78a9441…29b8`, as in the WP20 declaration) would bind the version.
4. **Gonthier.** G. Gonthier, Formal proof—the four-color theorem, *Notices Amer. Math. Soc.* **55**(11) (2008) 1382–1393.
   - From the Notices citation, reproduced on several pages (the Seville wiki page and the Microsoft Research note).
   - The "2005" in the repository notes is the date of the Coq development and its technical report, not of this article.
5. **Saaty and Kainen.** T. L. Saaty and P. C. Kainen, *The Four-Color Problem: Assaults and Conquest*, McGraw–Hill, New York, 1977 (ix + 217 pp., ISBN 0-07-054382-8); corrected reprint Dover, New York, 1986 (ISBN 0-486-65092-8).
   - From library catalogues (TUM, TAMU) and the Mathematical Gazette review listing.
6. **Tait (a choice is needed).** Tait's 1880 map-colouring items, according to the Pritchard–Forfar bibliography of P. G. Tait (Edinburgh), are:
   - "On the colouring of maps", *Proc. Roy. Soc. Edinburgh* **10** (1880) 501–503;
   - "Further remarks on the colouring of maps", *Proc. Roy. Soc. Edinburgh* **10** (1880) 728–729;
   - "Remarks on the previous communication [by Guthrie]", *Proc. Roy. Soc. Edinburgh* **10** (1880) 729;
   - "Note on a theorem in the geometry of position", *Trans. Roy. Soc. Edinburgh* **29** (1880) 657–660.

   **No item is titled "Remarks on the colouring of maps"**, the title in the paper's line 627. The edge-colouring correspondence ("Tait colourings") is usually credited to Tait 1880.
   - **Recommendation:** cite "P. G. Tait, On the colouring of maps, *Proc. Roy. Soc. Edinburgh* 10 (1880) 501–503" together with "Note on a theorem in the geometry of position, *Trans. Roy. Soc. Edinburgh* 29 (1880) 657–660".
   - **Better still,** cite the result through a secondary source the authors can check, such as Biggs, Lloyd and Wilson, *Graph Theory 1736–1936* (Oxford, 1976). The audit did not open that book here.
   - Mark which Tait item states the edge-colouring correspondence as [cited, not checked against the original].

**Also noticed in the bibliography** (not among the six):
- `mohar2009`: J. Phys. A **42** (2009) 225204. This matches the audit's 13:05 check, but that message's header ran ahead; it was committed at 12:43.
- `inoue2026`: arXiv:2603.24880. Not checked by the audit.

— Independent audit
