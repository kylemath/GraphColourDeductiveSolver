# WP7 declaration: chain sizes and overlap at the trap

Long Table, 4 October 2026. This file is committed **before** any test of Conjecture 7.3 is run. Lemmas 7.1 and 7.2 are exact statements with proof sketches, offered for the math team's review. Conjecture 7.3 is a finite hypothesis to be tested, not a claim.

## Setting

- T is a min-degree-5 triangulation, r a degree-five root, H = T − r, and B = N(r).
- c is a proper 4-colouring of H with four colours on B. Its **repeated colour** ρ occurs twice on B; the other three colours are **singletons**.
- For a pair {x, y}, write q_xy for the sum, over the {x,y}-components K meeting B, of |K∖B|². So q = Σ q_xy.

## Lemma 7.1 (locality)

Let K be an {a,b}-component, and let c′ be c with a and b exchanged on K. Then the {a,b}-subgraph and the {c,d}-subgraph of c′ have the same components as those of c, so q_ab and q_cd are unchanged.

**Hence:** q(c′) − q(c) is a sum of four *mixed* terms, the changes in q_ac, q_ad, q_bc and q_bd.

**Proof sketch.**
- Exchanging a and b inside K leaves the set of vertices coloured in {a, b} unchanged, and leaves the edges between them unchanged.
- The vertices coloured c or d are untouched, so the {c,d}-subgraph is unchanged.

## Lemma 7.2 (re-partition of a fixed graph)

For a colour e ∉ {a, b}, let G_e be the graph on the vertices coloured a, b or e whose edges join an e-vertex to an a- or b-vertex.

Then the {a,e}-subgraph and the {b,e}-subgraph together cover G_e. Before the swap, the {a,e}-subgraph is G_e restricted to the a-vertices and the e-vertices. After the swap, it is G_e restricted to (a-vertices outside K) ∪ (b-vertices inside K) ∪ (e-vertices), and symmetrically for {b,e}.

**So a swap does not change the graph G_e.** It only re-partitions G_e's a- and b-vertices between the two mixed pairs. The change in q_ae + q_be is a function of that re-partition alone.

**Proof sketch.** G_e is determined by the colour classes, which do not change as sets of {a,b,e}-coloured vertices. There are no a–b edges in either mixed subgraph.

## Observation at the paired fixture (diagnostic, already seen)

The fixture is order 17, graph 0, with the math team's collision pair: root 4 has state (1,143) and root 8 has state (1,143).

- **Same linkage pattern.** In both, every singleton pair is linked by exactly one chain (Π), and exactly one repeated-colour pair has a chain through both repeated vertices and a singleton.
- **They differ in the masses:**
  - singleton-pair chain masses: root 4 is 6, 6, 6; root 8 is 6, 6, 4;
  - the largest exterior mass of any repeated-colour chain meeting B: root 4 is 3; root 8 is 5.
- **The mechanism at root 4.** Every swap of a repeated-colour chain *raises* q in the other repeated-colour pairs by more than it lowers the singleton pairs: +20, +24, +20. The swap of a singleton-pair chain is neutral (+0). In the language of Lemma 7.2, each such swap re-partitions some G_e so as to merge repeated-colour mass.
- **At root 8,** a repeated-colour swap splits the other repeated pairs (−16).

## Conjecture 7.3 (mass dominance; necessary condition for a two-swap trap)

**Definitions.** For a non-target state c, let
- m_sing(c) = the minimum, over the three singleton pairs, of the largest exterior mass of a chain of that pair linking two singletons, taken as 0 if the pair has no such chain;
- m_rep(c) = the maximum exterior mass |K∖B| over chains K of the three repeated-colour pairs meeting B.

**Conjecture.** For every non-target state c at every degree-five root in the discovery range (orders 12–18):

> c is two-swap stuck ⟹ Π(c) holds and m_sing(c) > m_rep(c).

**The test** reads only states; it never uses ranks derived from targets.
1. **Necessity.** Count two-swap-stuck states violating the implication. Any violation refutes 7.3 as stated.
2. **Specificity, reported, not a pass criterion.** Among non-target states satisfying Π and m_sing > m_rep, how many are two-swap stuck, one-swap stuck, or descending?

**Provenance, stated honestly.** The inequality was suggested by the single collision pair at order 17, graph 0, roots 4 and 8. The discovery range also contains order 17, graph 0's roots 6, 9 and 14 and order 17, graph 3's roots 3 and 13, which did not shape it. Orders 19–20 stay untouched. Any later use of 7.3 in a rank or candidate set goes through the joint frozen gate.

**What 7.3 would and would not give.**
- Even if true, 7.3 is only a necessary condition.
- It would point to a rank ingredient: penalise mass transfer *into* repeated-colour pairs when Π holds.
- It does not by itself bound warnings or prove descent.
