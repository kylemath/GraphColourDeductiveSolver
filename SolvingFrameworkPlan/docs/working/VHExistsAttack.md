# Aim at VH∃

Proof Navigator, 5 October 2026. This is a working decision, not a proof. Leads written under it are leads. Finite passes stay finite.

## The only open step

The vacancy induction is accepted as a hand deduction: if VH∃ holds, every spherical triangulation is 4-colourable. VH∃ itself is open. It says that some degree-5 vertex and some legal fan work for every start on that deletion. Because the deduction is already written, VH∃ is at least as hard as the Four Colour Theorem. Mapping the neighbourhood of that hypothesis is not an attack on it.

## What the last two days actually finished

Compiled: the short-fill theorem (`SimpleGraph.VacancyShortFill`) and the three-move obstruction (`SimpleGraph.VacancyThreeMoveObstruction`, 85-module audit).

Accepted by hand: the belt theorem for Florek's two-pole graphs, including the potential that shrinks a linear unprocessed interval; the infinite family of order \(14k+3\) with fan-selection length exactly 3.

Killed, with certificates: \(m\le 2\), M2 (\(\kappa\le\ell+1\)), C3, the axis-symmetry conjecture S, and any fixed Kempe budget at a frozen hole. Kittell, 23 vertices, is already a passed fixture for the fixed-hole candidate in `docs/core/StructuralFourColourCandidate.md`: every tested state reaches a target in at most four Kempe moves, and the boundary-only policy fails. Retesting Kittell as if that were unknown does not help.

## Fixtures already used [lead]

This is a reading of existing reports, not a new check.

- **Kittell.** No targetless Kempe class at any of the 15 degree-5 roots (`replay-results.json`). The pooled boundary signature fails: 5 of 40 signatures lose. Low value as a new vacancy-hypothesis kill.
- **Errera.** It is plantri order 17 graph 3, already inside the orders 12–20 search that found no targetless class (`SearchReport.md`). It is not a separate named fixture.
- **The order-14 dipyramid** with link \((0,1,0,2,3)\). This is the Kempe objection that kills "one swap is enough" (`fan-link.md`). It still fills, so it is not a vacancy-hypothesis kill. The 14-vertex Heawood graph, the cage, has not been used as a fixture here.
- **The Birkhoff diamond.** Checked for D-reducibility in the older configuration work. It is not a vacancy-hypothesis fixture.

## Where the work is spinning

The live tasks are the belt walk in Lean, a Florek-free pole case, local facts about fills of length at most 3, and statistics of \(\kappa\), \(\ell\) and \(m\). None of them is "prove VH∃" or "say what a smallest failure must look like." The belt is one family. A compiled belt theorem would still cite Florek on the pole hole, and it would not move VH∃. The pattern of the kills is that bounded length keeps dying. Proving VH∃ by "fills are always short" is the wrong shape. The one termination argument that works on an infinite family is the belt potential. It has not been tried off the belt.

## Three lines

Each line states the step of a VH∃ proof it advances. A task that cannot say that is a side project.

1. **Minimal failure.** [open] What must a smallest triangulation with no good pair \((v,\tau)\) satisfy? The lead is `VHExistsMinimalCounterexample.md`. A finite fan-selection length already supplies a good pair, so every \(H_k\), including the order-31 chain, satisfies the hypothesis: the good pair is at most three Kempe swaps at a vertex off the interface. The glue does not automatically preserve the hypothesis. The written component-restriction lemma needs the hole off the triangle, and it uses all three vertices of that triangle. A smallest failure, if one exists, has no interior-staying fill off any separating triangle. Whether the hypothesis on both completed sides implies it on the glue is open. The four-connected form of S remains open and is not settled by \(H_2\). Owner: Long Table, as a hand page. Math reviews. No new census.

2. **A potential that is not the belt.** [open] Lift the belt's interval potential, or show the lift fails. The lead is `VHExistsPotential.md`. On the belt, \(\Phi\) is the size of a linear unprocessed interval. The rails, the poles, and the unwrapped index do not have a sentence at a general degree-5 hole. The one piece that might is an untouched set remembered against the start colouring. The untouched-set candidate is already dead on that path. Its size is 23, 22, 16, 12 along the mixed path and 23, 15, 9, 4, 4, 10 along the five-swap path, so it rises. Defect count, chain length and degree height also fail to fall on the mixed path. The plan stays **Low**. A different piece could still be proposed. Surviving this one path would leave the question open. Owner: Long Table for the candidate, Math if it survives the kill test. No new census.

3. **Task B stops at the milestone already in flight.** Finish integrating the controller, the openings and the symmetry that are already compiled in pieces. Then Math's Lean effort moves to whatever line 1 produces, or to the next obstruction after L3. It does not stay on the belt. The Florek-free pole case is a side project until line 1 or line 2 needs it.

## How the ledger will move

One revision per decision, not one per message. This file is that decision. Side projects stay visible and are labelled as side projects. Exploratory readings of saved tables, including any claim that \(\kappa\le 5\) on graphs already seen, are [post hoc]. They do not define what is open.

## Rules amendment

I recommend adopting the per-team worktrees now. The shared tree is how yesterday's meta-work started to look like research. The exploratory tier is sound only if its ledger exists before the first run under it, and if [post hoc] is written on every reading of saved data. The standing release is fine if every phase still reports its cost and its hash. The belt enumeration rule mostly serves the belt, which is now a side project.

The amendment is not in effect until the user adopts it.

## Feasibility

A universal length bound for VH∃: **Low**. The lead `VHExistsNotByShortness.md` records why. M3 and L3 describe a path that is already in hand. They do not produce a path. The next structural question is which blocks of a frozen link the circular word freezes on every interior, and which an interior change can unlock. A degree-5 start cannot be frozen. The degree-9 link on the 21-vertex graph splits six and ten, and no written path yet joins that colouring to a fan start.

A description of a minimal failure, using the separating triangle and the four-connected question: **Medium**.

A potential copied off the belt onto a general degree-5 hole: **Low**. Deciding that on the saved 7228 path: **High**. Surviving that path would raise the research plan to **Medium**, and would not be a theorem.
