/- Long Table DRAFT: axiom guard for the belt drafts (outside the accepted build). -/
module

import BeltWalk

/--
info: 'SimpleGraph.BeltDraft.belt_unequal' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms SimpleGraph.BeltDraft.belt_unequal

/--
info: 'SimpleGraph.BeltDraft.ringSwap' depends on axioms: [propext, Quot.sound]
-/
#guard_msgs in
#print axioms SimpleGraph.BeltDraft.ringSwap

#check @SimpleGraph.BeltDraft.belt_unequal
