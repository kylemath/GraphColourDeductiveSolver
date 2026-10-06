# Studio Math: link D1 (rotation-tracking subgraph carrier) compiles

- **From:** Studio Math (Mac Studio, branch `studio-math`)
- **To:** coordination; audit; navigator
- **Sent:** 2026-10-06 14:54 MDT
- **Replies to:** coordinator, go-ahead for link D
- **Asks for:** Audit, module audit of `PlaneMap/SideTriangle.lean` (hash in `docs/working/StudioMathLean/SHA256SUMS`)

**`SphericalMap.subgraph_tracked`.** Let H be a spanning subgraph of a spherical map M. Then there is a spherical map N with `N.graph = H` whose rotation successor of every dart d is the first H-dart reached from d along M's rotation (`RunTo M H`: k ≥ 1 steps, every intermediate dart outside H).

This strengthens the library's `subgraph_closed`, which only asserts that some rotation exists. The proof follows the same edge-by-edge erasure:
- `eraseEdge_runTo`: one erasure moves the successor by 1 or 2 old steps and skips only the erased darts. It is read off from `erasePoint` = `swap a (σ a) * σ`.
- `runTo_eraseEdge`: composes those runs.

**Checks.** Standard axioms; no `sorry`; `check.sh` builds all four Studio Math modules in order.

**Why D1 is needed.** Link D3 builds the side of a separating triangle as the subgraph left after isolating the far side, and must show that its faces are triangles. Only a tracked rotation makes that provable.

**Next:** D2, the algebraic sides of a non-facial triangle via `Fills`.
