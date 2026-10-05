# Belt Lean preparation: compiled helpers, full walk pending

Math, 5 October 2026. These are supporting results for Task B. They do not constitute the unequal-pole belt theorem.

`BeltOpeningWords.classification` proves that the locally proper, unfilled unequal-pole link words are exactly the14 listed openings, including all8 doubled-zero words. It is a kernel-checked proof over all256 assignments to four Fin4 entries. It is not a colouring search on a new graph.

`VacancyPotential.budget` proves a generic well-founded path-budget induction: if every good state has either an actual terminal path within its potential plus slack, or an actual macro path to a strictly smaller potential whose cost plus new potential is within the old potential, then an actual terminal path exists within the original budget. To obtain the belt theorem its controller premise must be proved from the belt graph, colouring and untouched-interval invariant. That premise is not an accepted substitute for the theorem.

Fresh source compilation of both helpers and a test module passed against the accepted83-module overlay. Exact axiom guards passed: budget uses propext/Quot.sound, classification uses only the standard three axioms. Source hashes stayed unchanged. The helper source snapshots, statement output and extension audit are in this directory. `longtable/audit/belt_preparation_audit.py` reconstructs the fresh extension audit.

Both teams are independently proving actual belt transitions and caps. Team A has compiled the actual doubled-one first slide and three-slide return, together with the exact neighbour lists and properness. Full Z transitions, cap/controller proof and symmetry reduction are still pending; no complete all-n belt Lean theorem is claimed here.
