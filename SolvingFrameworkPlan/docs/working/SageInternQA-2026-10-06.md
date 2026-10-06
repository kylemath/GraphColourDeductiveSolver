# Interns' questions to the Fable sage (6 October 2026)

Collected by the coordination session at 16:00 MDT on the user's request: the four interns (Sonnet, small budgets) were asked for their most basic questions and one wild idea each; the Fable sage answered in one reply. This is advice, not a ledger result: nothing here changes a status.

## Short answers

| Q | Question | Sage's answer, in one line |
|---|---|---|
| A1 / D2 | Why degree 5? | Degree 4: the two locks would cross, so one swap always fills. Degree 6: two repeats, nothing forced. Degree 5 is the one degree Euler forces to exist and Kempe's argument cannot close (an odd ring with exactly one repeat). |
| A2 | Why only two locks? | A filling swap must recolour b, g or d; exactly the {b,g} v2–v4 and {b,d} v2–v5 chains block those moves. The a-swaps are never blocked but never fill. It is a theorem (Kempe 1879). |
| A3 | Is "kill unless an outside path exists" just the nature of the problem? | Yes. That is Heesch's D-reducibility, and the single degree-5 vertex is not D-reducible (Heawood 1890). A conditional lemma has value only in a scheme that controls the outside, as R5³ does. |
| A4 / D1 | Why does deleting an edge create new classes but deleting a vertex does not? | Best guess: the quadrilateral admits rigid (frozen) colourings, while the pentagon forbids them (the ≤4-of-6 lemma), so a vertex stuck class must be large. Testable now (run 1). Nobody knows a general reason. This is the most interesting structural question on the table. |
| B1 | Is a locked state a real worry? | Locked states exist (Heawood, Errera). A stuck class is a Kempe-closed set of them. Whether one exists at a degree-5 vertex is unknown. |
| B2 | Do far swaps matter? | Yes, and that is important. A Kempe class allows every swap. Any argument that looks only at the link is incomplete (run 2). The single F-cycle supports this: 8 of its 20 states start with a silent move. |
| B3 / C3 / D3 | Is the radius bounded? | Nobody knows. Reconfiguration distances usually grow, so assume unbounded. A gluing test would settle the direction (run 3). |
| B4 | Is the lock rotation just a permutation? | The rotation is a permutation fact. Whether each chain exists is geometry, and Errera's cycle closes for a fixed strategy. |
| C1 | Why does a degree-6 neighbour break the starving trick? | A degree-5 neighbour sees a 4-path, often 2-coloured, so it has a free colour. A degree-6 neighbour sees a 5-path, almost always 3-coloured, so it is pinned. |
| C2 | Can it all be said in dual 2-factors? | Yes (Tait). This changes the notation, not the difficulty. Use it for the fullerene path. |
| C4 | Why can't counting rule out a 60-state stuck class? | No known invariant separates classes on the sphere (path 5 confirmed this). Mohar–Salas found one on the torus only. |
| D4 | Was T nearly connected? | v is a pinch point. Define the minimum number of vertex deletions that merges all classes of T. No theory exists. The table is cheap and publishable (run 4). |

## Wild ideas

| Intern | Idea | Verdict |
|---|---|---|
| A | A potential that some swap always lowers | Right shape but an old idea (path 4). Kill it on Errera's graph and the radius-5 certificates (run 5). |
| B | Dual Tait: locked-state cycles force an impossible Tait colouring | A correct reformulation, but Errera kills the claim. Worth one page of notation. |
| C | A finite automaton on the hole's 2-factor pattern | Equivalent to Heesch's ring-5 D-reducibility and to our own 74-pattern automaton; already killed. |
| D | The hole as a defect that annihilates against the 12 curvature charges | Not new in spirit (Fisk, Eliahou–Kryuchkov). No conservation law is known. One hour by hand: write the charge down and check it on the 1M states. |

## Cheap runs commissioned (Studio)

1. For each of the 16 new edge-deletion classes, count connected bichromatic pairs to see whether they are frozen (rigidity test).
2. Recompute class reachability using only link-touching swaps, to see whether any class becomes targetless.
3. Glue two radius-5 certificates, or nest an Errera gadget, to see whether radius 6 appears.
4. For the multi-class T in the census, find the minimum number of vertex deletions that merges all classes.
5. Run path-4 potentials on Errera's graph and the radius-5 certificates.

## The question the team is most afraid to ask

> "Which step of our planned proof could Heawood, Errera, Heesch, Tilley and the RSST authors not have taken, and why?"

If the answer is "none, but we can compute more", then the route is RSST with a weaker reducibility notion, and the paper must say so. If there is such a step, it goes on START-HERE in one sentence.

The coordinator's current candidate, unproved: the hybrid. Handle a few classical configurations (diamond, 2.122, …) by D-reducibility, then prove that in a core triangulation free of them, the global Kempe argument at some degree-5 vertex always succeeds. The new step would be a global (non-D-reducible) argument that works only because those configurations are absent. Today's only support is Studio Intel's exploratory finding: in every configuration-free graph tested, max radius ≤ 4, and every radius-5 hole sits in a graph with a diamond or 2.122. No one has yet said why absence should help; until someone can, this remains a candidate, not an answer.

— Coordination session
