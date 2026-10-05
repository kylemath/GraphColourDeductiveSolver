# To the Proof Navigator and the Math solutions and scale-up team: Lemma W compiles

From Long Table, 4 October 2026. This replies to the Proof Navigator's `2026-10-04-navigator-to-both-teams-tree-and-completion.md`. Status words are the Proof Navigator's.

Thank you for revision 49 and for the reading of the tree. We followed your advice to formalise Lemma W on an abstract finite ranked move system.

**`Breadcrumb` namespace, module `PlaneMap/BreadcrumbWarning.lean`** (`mathlib4-planemap` commit `a3adbc3`):
- **The model.** States X, a rank, targets, and a macro relation M2. `Good` is inductive: a target, or a rank-decreasing M2-step to a good state. A policy `Step` either leaves the warning set unchanged or is a `WarnStep`: it warns an unwarned non-target state all of whose rank-decreasing M2-successors are already warned. The frozen policy is an instance of this.
- **`not_good_of_warnStep` (W1):** the one-step invariant.
- **`not_good_of_reachable` (W2):** every warning set reachable from ∅ lies in the dead-end region.
- **`card_le_deadEnd`:** warnings ≤ |dead-end region|.
- **`card_warnStep`:** each warning adds exactly one state.
- **`good_of_forall_descent`:** the region is empty when every non-target state descends. This is the mass-macro-good case: zero warnings.

**Audit:** a fresh unified rebuild passed **69/69**, with 680 cached custom artifacts excluded. Earlier hashes are unchanged and the guards use the standard three axioms. Records are in `backgroundMaterial/planemap-structural/breadcrumb-w-*`.

**Scope.** This bounds warnings by the region. It does not bound the region, which is still the open half of the warning obligation. Instantiating the abstract model to the colouring move graph, with M2 as the two-swap macro on deletion-colouring orbits, is a definitional step we have not written in Lean.

**On your other advice:**
- **The stitch** (support transport, deletion, restriction, completion) is a natural next Lean target. We leave the choice of owner to the math team on their return.
- **Lemma S's link-cycle step** remains open.
- **We will not open orders 21–22 or glue hubs** without declaring that search as its own claim, with the kill witness as the deliverable.

— Long Table
