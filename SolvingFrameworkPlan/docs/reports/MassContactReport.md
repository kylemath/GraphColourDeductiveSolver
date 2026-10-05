# Conditional mass-contact theorem

4 October 2026. Math solutions and scale-up team.

## Result and scope

`SphericalMap.four_color_of_empty_mass_region` proves the precise conditional contact implication:

> If every nonempty connected spherical triangulation of minimum degree five has some degree-five root whose entire proper deletion-colouring state space has an empty mass dead-end region, every spherical map is four-colourable.

`four_color_of_mass_macro_descent` gives the same conclusion from universal two-swap mass descent. **These premises remain open. Neither theorem proves the Four Colour Theorem.** They prove the assembly and identify its exact remaining hypothesis.

## The assembly

`SphericalFourContact.lean` uses strong induction on the cardinality of the nonisolated support. An edge-free map receives a constant colouring. A positive-degree vertex of degree at most four is isolated, the smaller support is coloured recursively, and spherical degree-four extension applies.

Otherwise the support carrier has minimum degree five. It is completed on the same support labels to a connected triangulation of minimum degree five. The hypothesis chooses a degree-five root of that completed triangulation. Isolation strictly decreases support cardinality, so induction supplies a deletion colouring. The root is extended inside the completed triangulation. The colouring is restricted to the old support graph and extended over the original isolated labels.

No Kempe component is transported across completion. Completion can increase edges, so edge count is not the outer induction measure. The support carrier is nonempty in this branch, satisfying the completion theorem's nonempty-carrier premise.

## The exact mass model

`SphericalMassContact.lean` names:

- `DeletionColouring`: actual proper `Fin 4` functions on all labels except the root;
- `deletionBoundary`: the root's original neighbours inside that deletion carrier;
- `deletionMassRank`: the existing boundary surplus plus six-pair component mass rank, with the original order as its carrier bound;
- `ComponentStep`: one actual whole active bichromatic component swap, including interior components;
- `TwoSwapMacro`: zero, one or two component swaps, with no restriction on intermediate rank;
- `MassGood`: a finite path of macros with strictly decreasing endpoint rank to a boundary using at most three colours;
- `EmptyMassRegionHypothesis` and `MassMacroDescentHypothesis`: the root precedes every deletion colouring.

`empty_mass_region_of_descent` and `mass_descent_of_empty_region` prove the two hypotheses equivalent. Bare Kempe reachability, breadcrumb execution, and the twelve-root trap evidence are separate notions.

State space here retains colour names rather than quotienting by colour permutations. An experimental orbit-table bridge remains a separate obligation. This conditional existence theorem supplies neither an executable selector nor a polynomial solver, warning bound, or proof of Gate D.

## Review of the completed work

All 71 sources in Long Table's shared-hub manifest matched the checkout on return. The `RotationBoundary.faceSum_even` repair changes only an instance-sensitive rewriting step, not its statement. Completion uses the required nonempty carrier. Abstract Lemma W bounds warnings by the dead-end region but does not bound that region. Lemma S constrains a singleton-colour neighbour at one hub, not different hubs or larger components.

## Validation

A fresh unified build passed **75/75** modules and tests, excluding **693** cached custom artifacts. All 71 earlier source hashes are unchanged. Six new guarded axiom reports use only `propext`, `Classical.choice` and `Quot.sound`. No proof placeholders or additional axioms occur in the new sources. Records are in `backgroundMaterial/planemap-structural/mass-contact-*`. An earlier run failed only because the new guard expected multiline output while Lean printed the same axiom list on one line; the guard was corrected before the fresh final rebuild.

Source commits: `1e4d990` (contact assembly) and `a4a95dd` (guard whitespace and final source manifest). All reviewed completion, W/S and contact commits were applied to the local source-only backup. No remote push was made.
