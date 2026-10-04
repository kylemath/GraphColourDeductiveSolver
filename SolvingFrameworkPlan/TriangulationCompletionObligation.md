# Triangulation completion: explicit proof obligations

Date: 4 October 2026. Status: **unproved**. This records the precise bridge required before using the triangulation-only Gate-D candidate in a theorem about arbitrary spherical maps. It introduces no Lean axiom or assumed theorem.

## Remove isolated labels without assuming a construction history

For an edge-containing `M : SphericalMap n`, put `s = Nat.card M.graph.support`. Prove a support-carrier lemma supplying:

> a spherical map `N : SphericalMap s` and an equivalence `i : M.graph.support ≃ Fin s`, such that, for all support vertices `u,v`, `N.graph.Adj (i u) (i v) ↔ M.graph.Adj u.val v.val`.

The rotation and filling proof must be transported, not inferred from an ordinary graph isomorphism without proof. If every positive degree of M is at least five, then every degree of N is at least five and `s ≥ 12`. Transport a colouring of N back to the support of M and assign a fixed colour to isolated labels. Every edge has both endpoints in the support, so this transport preserves properness.

This is separate from `subgraph_closed`, which retains the original `Fin n` labels. It need not reconstruct generated PlaneMap histories.

## Add edges with a proved spherical carrier

The required completion lemma is:

> For every `N : SphericalMap s` such that `∀ x : Fin s, 5 ≤ N.graph.degree x`, there exists `T : SphericalMap s` such that `N.graph ≤ T.graph`, T is connected, and `∀ d : T.Dart, T.rotation.faceLength (T.faceOf d) = 3`.

The returned `T.fills` is a proof obligation. Its existence is not supplied by deletion closure or an unproved graph planarity test. The same-label graph inclusion implies minimum degree at least five in T, so T lies in the candidate's graph class. Connectedness is made explicit because the original carrier allows disconnected graphs. Connecting components and adding chords within faces require legitimate corner operations and filling preservation; short or repeated face walks cannot be silently assumed away.

It is sufficient here to preserve the graph inclusion and produce a valid spherical rotation; agreement with the old rotation is needed only if an additional argument uses that agreement. Do not impose it accidentally, and do not assume it accidentally.

## Colour restriction and the induction measure

A proper four-colouring of T restricts to the same labels of N by graph inclusion, then transports to M as above. This is the colouring preservation statement needed for the general theorem. It does **not** assert that Kempe components or move sequences in N and T agree: adding edges can merge bichromatic components.

Completion adds edges, so the existing edge-count induction on M cannot directly recurse into `T − r`, whose edge count may exceed M's. The general proof must instead use a justified measure such as support size: completion retains s vertices, and isolating a positive-degree root in T leaves at most `s − 1` nonisolated vertices. The support-carrier lemma then gives the smaller recursive input. Prove that decrease before invoking the induction hypothesis.

Only after these obligations and Gate D are discharged can the argument compose into general four-colourability. A recursively produced deletion colouring must satisfy any required fallback certificate; an arbitrary four-colouring from an existence theorem is insufficient for that stronger induction interface.
