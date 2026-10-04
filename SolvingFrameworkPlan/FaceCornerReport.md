# Face-corner completion prerequisite

4 October 2026. `Mathlib/Combinatorics/SimpleGraph/PlaneMap/FaceCorner.lean` contains five public lemmas: fixed vertex rotation implies degree at most one; immediate facial reversal implies degree at most one; minimum positive degree two excludes immediate reversal and immediate vertex return; every dart-containing face then has length at least three. These concern arbitrary finite rotation systems, with no spherical filling hypothesis.

`MathlibTest/PlaneMapFaceCorner.lean` has five guarded axiom reports, icosahedron applications, and a two-vertex single-edge rotation demonstrating that degree one permits reversal. The fresh unified source audit passed 45 modules, excluded 493 cached custom artifacts, and preserved every previous source hash. Its evidence is in `backgroundMaterial/planemap-structural/face-corner-source-audit.json`, `face-corner-source-audit-output.txt`, and `face-corner-source-SHA256SUMS` (source paths relative to mathlib4-planemap).

Chord availability, dart insertion, filling preservation after insertion, and triangulation completion are not proved by this module. See `MathLongTableResponse3.md` for the next obligations.
