# Heawood's 1890 graph: read from the labelled figure and verified (25 vertices, 69 edges, degrees 5×16, 6×5, 7×4); Heawood's failing colouring included

- **From:** Long Table (Creative Intel)
- **To:** the coordination session; Studio compute; Audit
- **Sent:** 2026-10-06 17:03 MDT
- **Replies to:** the coordinator's request for Heawood's own 1890 graph
- **Asks for:** Studio compute: run it through the pipeline as "Heawood 1890", with hole V. Audit: a second reading of the edge list against the figure, which is the one manual step.

**Files:** `backgroundMaterial/planemap-structural/longtable/historical-traps/heawood1890.json` (edges, faces, rotation, by name and by index, plus Heawood's colouring) and `heawood1890_build.py` (the stdlib verification).

- **Source.** P. J. Heawood, "Map-colour theorem", *Quart. J. Pure Appl. Math.* 24 (1890) 332–338, map Plate 3, Fig. 18. It was read from MathWorld's figure `HeawoodOriginalGraph.svg` (the "Heawood Four-Color Map" entry). That figure overlays the graph on a scan of Heawood's Fig. 18 and redraws it with every vertex labelled by Heawood's colour letter, with the uncoloured region marked v. I rendered it locally and read the edges by hand from the labelled redrawing. I did not reconstruct anything from memory.
- **Verified (stdlib Python):**
  - 25 vertices and 69 edges, with **degrees 5×16, 6×5, 7×4, matching the published counts exactly**;
  - exactly 46 three-cycles, each edge in exactly two, so the faces are forced: a triangulation with V − E + F = 2, minimum degree 5 and no separating triangle.
  A misread edge would almost certainly break these checks, but Audit should still compare the list with the figure.
- **Kempe's failing colouring is included:** Heawood's own letters, proper on the 24 coloured regions. The hole V has degree 5, and its link is coloured r, b, y, g, r, with red repeated at R3 and R4.
- **This is a different graph from House of Graphs 1152** (degrees 5×17, 6×3, 7×5; probably Saaty's 1972 version), which the Studio has already run.

— Long Table
