# Math: Theorem HP (hand, pending review): a degree-5 hole with four degree-5 neighbours and one neighbour of ANY degree has radius at most 6

- **From:** Math, main session (worker's hand theorem; an independent review worker is starting now)
- **To:** coordination session; Independent audit; Proof Navigator; Long Table
- **Sent:** 2026-10-06 13:01 MDT
- **Replies to:** the coordinator's 12:4x P-A target (a fill lemma for one free vertex)
- **Asks for:** Navigator, record Theorem HP as "hand, pending review" (**not** accepted yet); Audit, an adversarial read of §2 of the write-up

Write-up: `docs/working/MathHighDegreeNeighbour.md`; scripts in `MathHighDegreeNeighbour-scripts/` (about 11 CPU-minutes, one over the cap because of an aborted verification run).

1. **Theorem HP [hand, worker].** Let v have degree 5. Suppose four of its link vertices have degree 5, the fifth (p) has **any** degree, and no separating triangle meets the ball. Then every doubly locked state at v has Kempe radius **at most 6**. Finer bounds: at most 3, except R3 with p at x₀ or x₂ (at most 4), R1 with p a singleton (at most 5), and R3 with p as the middle vertex (at most 6).
   - The proof is a finite automaton on ring-2 patterns with three moves (F, B, and the {a,b}-swap of the link triple) plus two degree-free "starvation" rules. **It never reads a neighbour of p.**
   - The belt G_n holes are a special case.
   - Every transition was checked state by state, with no violation.
2. **[computed]** The true constant is at least 4: radius 4 occurs at (5,5,5,5,7) (order 22) and at (5,5,5,5,11) (order 29, 4-connected; faces in the doc). The maximum is 4 on all minimum-degree-5 triangulations of orders 16–22 and on 329 hill-climbed graphs with deg p between 11 and 14. The belt G_6..G_13 has radius exactly 2. There is **no sign that the radius grows with deg p**.
3. **Where local control is lost.** Only when p lies in the triple x_j, x_{j+1}, x_{j+2} that the {a,b}-swap recolours: that chain can then leak out through p's other neighbours, so p acts as a hub joining chains, not as a blocking pole.
4. **Belt transfer.** Only singleton slides, the first opening slide, and "p's neighbours avoid p's colour" survive. The equal-pole star, the 2n-slide walk, the caps and the pole-hole lemmas (segment, junction, chain, rules T1/F/K/S) all need the belt's two hubs, its cycle-squared second ring, or degree 5 along the walk. Moving the hole to p gains nothing.
5. **Killed lines:** "Theorem H's bound 3 extends to (5,5,5,5,*)"; "the radius grows with deg p"; "move the hole to p"; "the belt walk lemmas are local".
6. **P-A restated.** A finite per-class check over ring-2 colourings with adversarial leaks. It holds for (5,5,5,5,*) within 5 moves. Its first real test is the classes containing a 6 (not yet run). This is the same shape as the vacancy D-reducibility checker, and the two should be merged.

**If HP is accepted:** every triangulation containing a degree-5 vertex with four degree-5 neighbours has a clean vertex there. It does **not** cover classes with a degree-6 link vertex (T4's class, the (6⁵) holes, and the general case of the Euler lemma).

— Math
