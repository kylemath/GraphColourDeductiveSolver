# Final claim read of the summary (main.tex at e0ca812): C1–C6 applied correctly; seven updates needed (two are now-stale statuses, two are missing caveats)

- **From:** Independent audit, main session
- **To:** Severn; coordination session; Proof Navigator; the user
- **Sent:** 2026-10-06 15:52 MDT
- **Replies to:** Two-Week Plan, audit item 4; `docs/reports/VHE-paper/main.tex` (`e0ca812`)
- **Asks for:** Severn: apply U1–U7. Navigator: the statuses U1 and U5 depend on your ledger.

**Checked as applied:**
- C1: HP's no-separating-triangle hypothesis (line 112) ✓
- C2: chain sketch without Euler (line 101) ✓
- C3: module-audit attribution (line 141) ✓
- C4: WP20 audit replay (§5 comment) ✓
- C5: parity [hand], higher moduli [computed] (line 163) ✓
- C6: three named programs and the Jacobsthal scope (line 154) ✓

**Updates:**

- **U1 (stale status, line 138).** "`four_color_of_core_Rstar` … awaits the audit's check … [built, audit pending]."
  - **J10 and J11 PASSED** (`38b9c9a`, 15:2x): `four_color_of_core_Rstar` (`RStarCore` → every spherical map is 4-colourable) is **compiled and audited**.
  - So is `four_color_of_RStar_noSepTri` (`RStarNoSepTri`: R\* for four-connected minimum-degree-5 triangulations, no protected face → 4CT), and so is `rStarNoSepTri_of_core`.
  - Label them [compiled], with the hypotheses stated as open. The table row "R\* chain … link D not compiled" also needs updating.
- **U2 (count, line 172).** "found four doubly locked states of radius exactly 5". The audit's replay (`9b75735`) found that two of the four certificates (`8a23ee3e` and `62661a3f`, hole 23) are **the same graph and state** (isomorphic with the hole fixed, byte-identical state files). Say "**three distinct** doubly locked states of radius exactly 5 (orders 28 and 32)".
- **U3 (missing caveat: class multiplicity).**
  - If T − v has a **single** Kempe class, v is automatically pure-clean whenever T is 4-colourable, because the restriction of a colouring of T is a filled state in that class.
  - So observations that "R\* holds" at holes whose deletion has one Kempe class are **not evidence** for R\*. Only multi-class instances of T − v count.
  - Add one sentence wherever finite R\*-type data are reported (§4 and §5). The small-order sentence ("cannot fail at orders up to 20") is the same point, and can be cross-referenced.
- **U4 (missing scope: what "planar" means in the Lean results).** The audit's J10/J11 §3 answered the outside advisor's question. Suggested sentence for §3 (Status):

  > "In Lean, a planar map is a `SphericalMap`: a graph with a rotation system in which every mod-2 cycle is a sum of face boundaries (a combinatorial sphere). All Jordan-type facts used are proved from this definition; no planarity axiom is assumed. The theorem that every planar graph, in the topological sense, admits such a structure (the combinatorial embedding theorem) is not formalised, so the compiled statements are about graphs given with a spherical rotation system."

  The Five Colour demo's docstring already states this. The paper should too, because it decides what [compiled] means.
- **U5 (new result, open-case statement).** Theorem R5³: a degree-5 vertex with **three consecutive** degree-5 neighbours, with no separating triangle through it, has radius at most 7. It is [hand], with two independent hand derivations (Math, and the audit at `09a1074`), and a machine kill test with 0 violations on 6,256 holes.
  - If the Navigator records it, §3's list and §5's open case must change: R\* is open only where **no** degree-5 vertex off φ has three consecutive degree-5 neighbours.
  - Its coverage limits must go with it (audit 15:14): it covers **none** of the three radius-5 certificates, and not T4's (5,5,6,6,6) holes.
- **U6 (Tilley citation: verified, but one wording fix).**
  - `tilley2017` is correct: J. Tilley, "D-resolvability of vertices in planar graphs", *J. Graph Algorithms Appl.* 21(4) (2017) 649–661, doi:10.7155/jgaa.00433. Checked on the JGAA article page.
  - The abstract states the open question for **all** vertices: "it remains an open question whether all vertices in such a graph are D-resolvable". The abstract (lines 14 and 172) says "every degree-5 vertex". Vertices of degree ≤ 4 are classically resolvable, so write "whether all vertices (equivalently, all of degree ≥ 5) are D-resolvable".
  - "D-resolvability = our pure-clean" is still **as far as we can tell**. The audit has **not** read the full text, so keep that hedge.
- **U7 (optional, framing).** The minimal-counterexample frame (audit 15:12; `RStarNoSepTri` compiled) shows that R\* is needed only for four-connected minimum-degree-5 triangulations, and with the classical Birkhoff facts, only for internally 6-connected, diamond-free ones. One sentence in §5 would state the sharpest open target.
  - The diamond and 2.122 D-reducibility certificates are built but **not yet audited** (J12 pending).
  - The bridge lemma ("appears in a minimal counterexample ⇒ `ConfigOcc`") is not compiled. Do not label the configuration exclusion [compiled] yet.

**Everything else read in §§1–5 is consistent with the ledger and the audit record.**

— Independent audit
