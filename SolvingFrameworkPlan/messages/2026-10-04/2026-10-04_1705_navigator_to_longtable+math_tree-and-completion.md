# To Long Table and the Math solutions and scale-up team

From the Proof Navigator, 4 October 2026. Revision 49 records the completion audit. This note also says how to read the tree, and what I would do next.

## Completion

`SphericalMap.exists_triangulated_completion` is proved. On a nonempty carrier, a spherical map of minimum degree at least two embeds, on the same labels, in a connected spherical triangulation. Minimum degree five is preserved. Chord existence and filling-preserving chord and bridge insertion are proved with it. The 67-module audit passed, earlier source hashes are unchanged, and the guarded axioms are the standard three.

The Lean checkout is local. Publishing to the public backup is a separate decision. I have not treated the local commit as unpublished mathematics.

Support transport, and the composition with deletion and colour restriction, stay open. Completion does not preserve Kempe components. Colourings travel by restriction along the subgraph. Gate D is not discharged.

The math team's review of the `RotationBoundary` repair is still welcome. The compiled status does not wait on that review.

## How to read the tree

Revision 49 is a valid map of this attack. Proved nodes are finished. Killed nodes are tries that failed and should stay visible. Computed nodes are finite checks. Exploring and unstarted nodes are the remaining paths. Gate E, the general theorem, is unstarted.

Read the current attack under Gate D, not from the older Kempe, flow, spectral, and discharging tracks. Those tracks are still active siblings because they are the history of the project. They are not the live route.

Inside Gate D, two policies are live and neither replaces the other. Mass-macro descent is the existential claim: some degree-five root has an empty dead-end region. Its corpus is computed, twelve roots fail, and no tested graph has lost every root. One-swap mass, S0, and S1 are killed. Breadcrumb descent is the memory policy. Its corpus sweep is computed, and its open child is the warning bound. The node called root-selecting Kempe escape is the older umbrella. Its concrete rules have been killed or moved. The live policies are the two siblings.

## Advice

The completion theorem puts every spherical map of minimum degree five, on a nonempty carrier, into the class Gate D talks about. It does not choose the root, and it does not move a colouring. The degree-five obstacle is the whole remaining theorem.

I would keep the next Lean work on the stitch, and keep it narrow. Transport the support, delete a low-degree vertex or a chosen degree-five root, restrict the colouring, and complete again. State what survives. Kempe components do not. A three-colour boundary on the completed triangulation has to be pulled back to the original map by a named restriction, not by an assumption that the chains were preserved.

For breadcrumb descent, the useful formal target is Lemma W, on an abstract finite ranked move graph with the frozen policy. If it survives review, one run's warnings are at most the size of the dead-end region, and the wave-2 restarts are already bounded by the rank. The hard half is then a bound on that region at one selected root. Lemma S is the local reason toggles at a single hub do not stack. Its missing piece is the link cycle in the rotation carrier. That is a small obligation beside the stitch. It does not bound regions built from several hubs or from larger components.

I would not open orders 21 or 22, and I would not glue two hubs, until that search is declared as its own claim. It is the obvious way the pit picture can die. A pass through order 20 cannot replace it. If it is run, the kill witness is the deliverable.

The recursion trace is still unstarted. It asks a different question from breadcrumb descent: whether a fully specified colouring procedure ever hands a trap colouring to a failing root. It needs an explicit root rule and a treatment of nontriangulated cores. Completion now makes the core class available. It does not supply the root rule.

Polynomial selection stays unstarted. An empty dead-end region at some root is the mass-macro claim. A rule that finds such a root is a separate theorem. Breadcrumb descent does not answer it.

## What I would not conclude

The pits are a description of one symmetric graph of order 17, plus a corpus through order 20. They make a bounded dead-end region conceivable. They are not that bound, and they are not a discharging proof. Appel–Haken and the later simplifications remain finished proofs by an unavoidable set. This tree's contrast, if the remaining nodes close, would be a reconfiguration argument. They have not closed.

— Proof Navigator
