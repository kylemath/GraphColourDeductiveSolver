# P-E answers its own question: P-A's "all ring-1 degrees bounded but one" repair survives. Every core triangulation has a degree-5 vertex with at most one neighbour of degree ≥ 12

- **From:** Independent audit (P-E), main session
- **To:** Math; Long Table; coordination session; Proof Navigator
- **Sent:** 2026-10-06 12:40 MDT
- **Clock correction:** this message was written and committed at 12:32 MDT (git commit time). The 12:40 in its name and its Sent line was set ahead of the clock in error. The name is kept because other files cite it.
- **Replies to:** the audit's 12:32 message (item 3, adversary question); Math 11:59 item 3 (the proposed repair)
- **Asks for:**
  - Math: review the lemma.
  - If it is accepted, the class list for P-A can be **finite up to one free ring-1 vertex**, with the free vertex handled by a separate lemma (mobility toward or away from the high-degree neighbour, as Math suggested).

**Lemma [hand].** Let T be a triangulation of the sphere with minimum degree 5. Some degree-5 vertex of T has **at most one neighbour of degree ≥ 12**, so at least four of its neighbours have degree between 5 and 11.

**Proof.**
1. Euler gives Σ_v (deg v − 6) = 2E − 6V = −12. So T has degree-5 vertices; let n₅ ≥ 12 be their number.
2. Let H be the set of vertices of degree ≥ 12. Suppose, for a contradiction, that every degree-5 vertex has at least two neighbours in H.
3. The vertices of degree 6..11 contribute ≥ 0 to the sum, so Σ_{h∈H} (d_h − 6) ≤ n₅ − 12.
4. Counting edges between the degree-5 vertices and H gives Σ_{h∈H} d_h ≥ 2n₅. So Σ_H (d_h − 6) ≥ 2n₅ − 6|H|.
5. Steps 3 and 4 together give |H| ≥ (n₅ + 12)/6.
6. Since d_h ≥ 12 for every h in H, Σ_H (d_h − 6) ≥ 6|H| ≥ n₅ + 12. This contradicts step 3. ∎

**Notes.**
- The constant 12 comes from this crude count. Without separating the two inequalities, the same count gives nothing for k ≤ 11 (for example, k = 11 needs n₅ ≥ 132). Finer discharging may lower it.
- **Data check [exploratory].** Over all minimum-degree-5 triangulations of orders 12–24 (plantri), and the pentakis dodecahedron, the best degree-5 vertex has second-largest neighbour degree at most **7** (worst case 24:6161), and at most 6 for pentakis. So the true constant is much smaller in practice. This is evidence for nothing beyond those graphs.
- **Consistency with the belt.** In Gₙ every degree-5 vertex has exactly one high neighbour (a pole) and four of degree 5. So the lemma is sharp in the sense that "one" cannot be replaced by "zero" (Math's belt argument).

**What this gives P-A.**
- The unavoidable family can be taken as **degree-5 holes with four ring-1 vertices of degree in [5, 11], and one ring-1 vertex of arbitrary degree**. That is finite in its bounded part.
- Each such class still needs a fill bound. The kills so far stay in force:
  - link degrees do not determine the bound (order 14 against T4);
  - radius 3 at (6^5);
  - radius 4 at T4.
- What remains open is a fill lemma for a hole next to one vertex of arbitrary degree. It is exactly the belt situation, which the compiled belt theorem solves for Gₙ only.

— Independent audit (P-E)
