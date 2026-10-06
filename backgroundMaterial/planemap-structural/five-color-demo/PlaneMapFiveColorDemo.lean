module

import Mathlib.Combinatorics.SimpleGraph.PlaneMap.FiveColorDemo

/-! Guard tests for the Five Colour demonstration: standard axioms only. -/

open SimpleGraph

/-- info: 'SimpleGraph.PlaneMap.five_color_theorem' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms PlaneMap.five_color_theorem

/-- info: 'SimpleGraph.Icosahedron.icosahedron_colorable_five' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms Icosahedron.icosahedron_colorable_five

/-- info: 'SimpleGraph.Icosahedron.theoremColouring_valid' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms Icosahedron.theoremColouring_valid

/-- info: 'SimpleGraph.Icosahedron.explicitColouring_valid' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in
#print axioms Icosahedron.explicitColouring_valid

/-- info: 'SimpleGraph.Icosahedron.icosahedron_five_colouring' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms Icosahedron.icosahedron_five_colouring

/-- info: @PlaneMap.five_color_theorem : ∀ {n : ℕ} (M : PlaneMap n), M.graph.Colorable 5 -/
#guard_msgs in
#check @PlaneMap.five_color_theorem
