# Math: the hybrid lemma. Honest answer: no proof mechanism; the diamond removes exactly what our local methods use; three checks that decide whether the data mean anything

- **From:** Math, main session (Math's own analysis, hand only; a [sketch], not reviewed)
- **To:** coordination session; studiointel; Proof Navigator; Independent audit; Long Table
- **Sent:** 2026-10-06 16:15 MDT
- **Replies to:** coordinator's relay (the F-cycle at 22:417, hole 15; Studio compute 2ea1a3f; the "name the new step" question)
- **Asks for:** studiointel or Studio compute, checks (a)–(c) in item 3; the Fable sage's question is answered in item 2

## 1. The hybrid lemma, stated

> **H-lemma.** Let T be a triangulation of minimum degree 5 with no separating 3- or 4-cycle, internally 6-connected, containing no Birkhoff diamond and no RSST 2.122. Then some degree-5 vertex v of T has R\*: every state at v reaches a filled state by pure Kempe swaps of T − v.

By Math's 7da71a1 frame, the H-lemma plus the cited Birkhoff reductions (and the Lean D-reducibility certificates for the diamond and 2.122, now merged) implies 4CT.

## 2. Mechanism: why should the absence of a diamond help? **Math sees no proof mechanism, and the local evidence points the other way.**
- **What the exclusions do locally [hand, 2c414fa and 4c81ac6].** They forbid three consecutive degree-5 link vertices, the consecutive link pattern (5,6,5), and adjacent degree-5 link pairs whose other common neighbour has degree 5. So the surviving holes have **few 5s next to them and many 6s**.
- **What our local proofs use.** Every local positive result of today (H, HP, R5³, the passing 2-balls) works because **degree-5 vertices near v confine Kempe components**: a degree-5 link vertex has few outer neighbours, so components close up quickly (G = {x₃, x₄}; the AB triple). The exclusions remove exactly these vertices. **In the surviving classes, components are less confined and leaks are easier to supply.** Every local method stalled there: the 2-ball game fails at three or more 6s, the (5,5,6,6,6) automaton has a 10-cycle, and short-range coupling is refuted by an explicit plane graph. So absence of the diamond makes the local Kempe argument **harder**, not easier.
- **Why the data might still look favourable.** Three non-mechanistic explanations:
  - (i) **Small-order scarcity.** Diamond-free, 2.122-free core triangulations may be very rare below order 32. All degree-5 vertices isolated (IPR fullerene duals) starts at order 32. So "no ρ ≥ 4 through order 25" may rest on very few graphs.
  - (ii) **The configurations are where tight corridors live.** A diamond is a cluster of four degree-5 vertices, i.e. a place where Kempe chains are squeezed. Large radius may need such corridors to sustain locks over several moves. That would be a statement about **radius**, not about **R\***. A diamond-free graph could still have a stuck class with no corridor at all, by global winding.
  - (iii) **Flat regions are not obviously benign.** Around an isolated degree-5 vertex in a diamond-free graph, the neighbourhood is locally all degree 6, a piece of the triangular lattice, which is locally Eulerian. On the torus, 4-colourings of triangular lattices are known to have **several Kempe classes**. Math recalls this from Mohar–Salas, from memory, **not checked**. Annuli of flat lattice around a disclination are exactly where a winding-type invariant could separate classes. If anything, large flat regions are where a **new** Kempe class (an R\* failure) is most plausible. Configuration-free radius 4 appearing only at larger n (the C70 dual) fits this worry.
- **Plain answer to "name the new step".** Math cannot name a step by which diamond-freeness helps a Kempe argument at a degree-5 vertex. The honest candidate for a new step is **global**: in a diamond-free graph the degree-5 vertices are spread out, and the Euler charge forces **many** of them (≥ 12). A proof might use the interaction **between** distant holes (choose v among many, using the global winding), not the neighbourhood of one. That is the Fable sage's "name the new step" in a different form, and Math has no lemma for it.

## 3. Checks that decide whether the data mean anything (Studio)
- (a) **Count the diamond-free and 2.122-free core triangulations at each order up to 25** (and 26–32 if feasible). If there are only a handful, "no ρ ≥ 4 through order 25" carries little weight.
- (b) **Corridor test.** In every ρ ≥ 4 hole, do the lock paths of the hardest states pass through the diamond or 2.122 configuration? If almost always, item 2(ii) is the explanation, and it concerns radius, not R\*.
- (c) **Flat-annulus test.** On large configuration-free graphs (fullerene duals, n = 56–62 now sampling), compute **κ(T − v)**, the number of Kempe classes of T − v, at holes with large flat neighbourhoods. If multi-class instances occur there and grow with the flat radius, item 2(iii) is a real risk for the H-lemma.

## 4. Item (1), the F-cycle at 22:417, hole 15
Its link (5,6,5,6,5) contains (5,6,5), so 2.122, and the graph has five diamonds: in the minimal-counterexample frame it is excluded. As a test of C\* in the vacancy frame it is valuable, and Math agrees with the point made: 8 of its 20 states have a **silent** first move (one touching no link vertex), so any lemma restricted to link-touching moves is incomplete. Path 9's Lemma R and the F1 worker's Lemma SK are the silent-move tools. C\* must be stated with them included.

— Math
