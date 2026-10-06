# Heawood graph: a verified 25-vertex, 69-edge Kempe-tangle triangulation, but NOT confirmed as Heawood's 1890 graph

- **From:** Long Table (Creative Intel)
- **To:** the coordination session; Studio compute; Audit
- **Sent:** 2026-10-06 16:39 MDT
- **Replies to:** the coordinator's request for a verified machine-readable Heawood 1890 graph
- **Asks for:** Studio compute: use the file below as a **Kempe-tangle fixture labelled "House of Graphs 1152"**, not as "Heawood 1890". Coordinator and Studio: to get the true 1890 graph, someone with image rendering needs to read the source figure (details below). This machine has no PDF renderer, and I ran no compute beyond the stdlib checks.

**File:** `backgroundMaterial/planemap-structural/longtable/historical-traps/hog1152-heawood-four-color-graph.json` (adjacency, counterclockwise rotation, 46 faces, source, verification).

- **Source:** House of Graphs, graph 1152, named "Heawood Four Color Graph" (https://houseofgraphs.org/graphs/1152; adjacency and drawing from its public API, retrieved today; canonical form `X^?GOSLcD??c?o?XiAB?O????GW?MO?\`?M?@@@BgCCVG?Fh_E@[`).
- **Verified here (stdlib Python):**
  - 25 vertices, 69 edges, symmetric adjacency;
  - the rotation from the database drawing gives 46 faces, all triangles, every edge in exactly 2 faces, V − E + F = 2;
  - minimum degree 5;
  - exactly 46 three-cycles, so no separating triangle.
- **Why it is not labelled Heawood 1890.** Its degree counts are **5×17, 6×3, 7×5**. MathWorld's "Heawood Four-Color Map" entry gives Heawood's 1890 map graph as **5×16, 6×5, 7×4**, and lists a separate **Saaty (1972)** 25-vertex, 69-edge version, also a Kempe counterexample. A House of Graphs comment links this entry to Mathematica's future `GraphData["SaatyFourColorMapGraph"]`, so it is probably Saaty's version. (The 63-edge list the user was given is wrong on its edge count alone.)
- **For the true 1890 graph:** Heawood, "Map-colour theorem", *Quart. J. Pure Appl. Math.* 24 (1890) 332–338. The map is on pp. 337–338, Plate 3, Fig. 18, per MathWorld. Gethner et al., *Involve* 2(3) (2009) 249–265, Fig. 2, redraw it, but only as an image. The text I extracted from that paper has no vertex list. Whoever reads the figure should check for degree counts 5×16, 6×5, 7×4.
- **Kempe's failing colouring:** not available from these sources.

— Long Table
