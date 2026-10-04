# Gossip brief before wave 3

Already gated. Do not recompute these, and do not report them as new.

- K1-safe length \(s_1 \le d+1\) holds for triangulations \(n=6,\ldots,10\). It does not 4-colour \(G\). Witness: \(T_{6,0}\), vertex 0, colouring \(0{:}5,1{:}1,2{:}2,3{:}3,4{:}4,5{:}2\), \(d=s_1=0\), \(d_2=s_2=2\). On that same run \(s_2 \le d_2+1\). Files: `groups/K4_report.md`, `K4_results.json`.
- Strict monotone reduction is dead. Witness: \(T_{5,0}\), colouring \((1,2,3,5,4)\). Non-strict monotone reduction has 0 failures for triangulations \(n\le 11\); the longest plateau is 5. Files: `groups/K5_report.md`.
- For triangulations \(n\le 11\), the 5-colouring Kempe graph is connected and every class contains a 4-colouring. Given Meyniel, J. Combin. Theory B 24 (1978), that universal sentence is a reformulation of the Four Colour Theorem. Meyniel is not proved in this repo.
- KC5 has 0 bad classes for \(n\le 11\), the icosahedron, and Errera's 12 degree-5 vertices (max distance 3). Errera kills Kempe's two-swap procedure, not KC5. The stored Kittell graph is not planar and has the wrong number of edges. Files: `groups/K6_report.md`.
- A real chromatic root in \((3,4)\) kills root-bounding. Witness \(T_{8,13}\), about \(3.606\), \(P=72\). Counts at \(n=8,9,10,11\): 1, 2, 22, 138. \(P(G,4)>0\) is not killed. Golden identity holds through \(n=11\). Royle, arXiv:math/0511304. File: `groups/A1_report.md`.
- For triangulations \(n\le 9\), Tait colourings of the dual equal nowhere-zero 4-flows and equal \(P(T,4)/4\). Duals are cubic, so Jaeger's 4-edge-connected 4-flow theorem does not apply. The planar 4-flow statement is a reformulation of the Four Colour Theorem. File: `groups/D1_report.md`.
- Lean 4.15.0 is installed. Mathlib oleans for `lean4/KempeReconfiguration` are downloaded. Do not rebuild the `cache` executable (`BUILD_NOTES.md`).
