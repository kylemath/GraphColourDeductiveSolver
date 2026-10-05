# Unequal-pole belt walk in Lean

Math integration of Long Table's complete draft, 5 October 2026. The fresh 95-source audit passed; Math accepts the theorem within the scope below.

## Statement and scope

`SimpleGraph.TwoPoleBeltWalk.belt_unequal_at` proves: for every n≥5, every belt hole h, and every proper four-colouring of Gₙ−h whose two poles have different colours, there is a path of actual singleton slides of length at most 2n ending at a filled hole. The terminal colouring is proper off its hole, that hole is on the belt, and each terminal pole colour equals its input colour. The exact Lean statement is saved in the artifact's test log.

The graph has two poles and two cyclic rings, with the six edge families stated in `TwoPoleBelt.lean`. `Filled` means a colour is absent from all neighbours of the current hole. `SlideStep` uses the actual adjacent-unique-colour slide definition; the proof does not assume an abstract controller in place of graph moves.

The formal path records actual slides and its length. The public theorem records belt membership and unchanged poles at the terminal state. It does not separately expose a certificate of belt membership and pole colours at every intermediate state. Equal poles and pole holes are outside this compiled theorem. Florek's theorem and the Four Colour Theorem are not dependencies.

## Proof and integration

Long Table supplied the complete normalized opening/controller/termination proof in `lean-drafts/BeltWalk.lean`, with graph symmetry and transport in `BeltGraph.lean`. Math reviewed the actual graph and move semantics, all opening classes, macro preservation of the original-colour interval, strict budget descent, and end caps including n=5. The controller premises are proved from properness and the concrete belt geometry.

The canonical modules rename Math Team A's graph/move library to `TwoPoleBelt`, Math's cap library to `TwoPoleBeltCaps`, and the draft transport/walk to `TwoPoleBeltTransport` and `TwoPoleBeltWalk`. Math added `TwoPoleBeltAllRoots`: rotations and the ring-swap automorphism transport the u₀ result to every belt vertex, allowing the automorphism to exchange the two poles and restoring each original pole colour at the end.

The supporting modules are `VacancyPotential` and `BeltOpeningWords`. No new graph enumeration was run. The kernel's finite colour-word classifications are proof terms, not an empirical belt census.

## Reproducible artifacts

Canonical source/test snapshots and provenance: `backgroundMaterial/planemap-structural/belt-lean/`. The incoming Long Table sources remain unchanged. Provenance binds their hashes and the graph/cap inputs separately.

The audit script is `backgroundMaterial/planemap-structural/longtable/audit/belt_source_audit.py`. It verifies the accepted 85-source baseline before rebuilding those sources plus seven belt/helper modules and three tests into a fresh library. Cached custom artifacts are excluded, upstream dependency artifacts remain available, and every audited source hash is checked again after compilation. Exact axiom guards cover the final all-root theorem, original theorem, controllers, caps and helpers.

Audit result: **95/95 source modules passed**, source hashes stable, 693 cached custom artifacts excluded, elapsed 133.503 seconds. Final theorem/controller/cap guards admit only `propext`, `Classical.choice`, and `Quot.sound` (some helpers use fewer). No `sorry` or added axioms occur in the integrated source.
