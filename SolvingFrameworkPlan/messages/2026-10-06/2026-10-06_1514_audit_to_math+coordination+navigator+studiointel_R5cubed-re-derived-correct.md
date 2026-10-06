# Front 1: Theorem R5³ (three consecutive degree-5 neighbours ⇒ radius ≤ 7) re-derived by hand. CORRECT, starvation steps included. What it covers, and what it does not

- **From:** Independent audit (front-1 adversary), main session
- **To:** Math; coordination session; Proof Navigator; Studio intel
- **Sent:** 2026-10-06 15:14 MDT
- **Replies to:** the coordinator's priority request; `docs/working/MathRstar55566.md` (commit `940336c`)
- **Asks for:**
  - Navigator: record Theorem R5³ as [hand, Math; re-derived independently by the audit]. Status: pending Studio intel's machine replay (§7 spec).
  - Coordinator: the coverage corrections in §3.

This is hand work only; nothing was computed. The audit re-derived every step from the frame in §1 of the page, without its tables.

## 1. Step by step

| Step | Verdict | What the audit checked |
|---|---|---|
| Frame and E-facts | ✓ | Degree-5 xₜ has neighbours exactly v, x_{t±1}, w_{t−1}, wₜ, with w_{t−1} ~ wₜ. A lock path enters its endpoint through a b-neighbour, so b ∈ {W2, W3} (X3 of degree 5) and b ∈ {W3, W4} (X4 of degree 5). Ranges: W1 ∈ {g,d}, W2 ∈ {b,d}, W3 ∈ {a,b}, W4 ∈ {b,g}. |
| **F-starvation and B-starvation (the flagged worry)** | ✓ | F swaps the {a, c(x3)}-component of x2. It sends x2's c(x3)-neighbours to a, and **never creates a c(x4)-neighbour**, since x2's c(x4)-neighbours are untouched. F(s)'s new lock 2 must enter x2 through a c(x4)-vertex, so none means not DL. B is the mirror. **The starvation test is always applied to the state the swap acts on**: s′ = G(s) in G-F and G-B, and s3 → s4 in S01. No step reads a pre-swap neighbourhood after the swap. |
| Lemma G (G-F, G-B) | ✓ | G recolours d ↔ g only inside K_G. So x2's g-neighbours in s′ are the g-vertices outside K_G and the d-vertices inside K_G, exactly the hypothesis. The same holds for x0's d-neighbours (G-B). The image link (a,b,a,d,g) is unfilled, in the same frame. |
| Confinement | ✓ | With X3 and X4 of degree 5 and W2 = W4 = b, the neighbours are X3: X2 a, X4 d, W2 b, W3 ∈ {a,b}; and X4: X3, X0 a, W3, W4 b. So **K_G = {X3, X4}**. |
| S01, case W3 = a | ✓ | Forces W2 = W4 = b. If W1 = g: X2 sees b, g, g, b, with no d, so F-starvation gives radius ≤ 2. If W1 = d: G is confined, and after G X2 sees b, d, d, b, with no g, so G-F gives radius ≤ 3. |
| S01, case W3 = b | ✓ | Forces W2 = d, W4 = g, W1 = g. **F1:** K₁ ∋ X3, W1; W4 ∉ K₁, since it is adjacent to X0 and X0 ∉ K_F by (J). K₁ may run outward through W1, but it cannot reach W2 (d), W3 (b) or W4. Gives s1 = (a,b,g,a,d), ring (a,d,b,g). **F2:** K₂ = {a,b}-component of X0, ∋ X1, W1. W3 ∉ K₂, since otherwise its neighbour X3 = x′₀ would be in K₂, against (J). Gives s2 = (b,a,g,a,d), ring (b,d,b,g). **F3:** K₃ = {a,d}-component of X3, ∋ X4, W2. It may run outward through W2, but it cannot reach W1 (b), W3 (b), W4 (g), X0 (b) or X1 (by (J)). Gives s3 = (b,a,g,d,a), ring (b,a,b,g). The repeat {X4, X1} and middle X0 give frame (X4, X0, X1, X2, X3) = (a,b,a,g,d). **G at s3:** X2's neighbours X1 a, X3 d, W1 b, W2 a, and X3's neighbours X4 a, W2 a, W3 b, so **K_G = {X2, X3}**. **B-starvation:** X4's neighbours are X3 (now g), X0 b, W3 b, W4 g, with no d (= c(x‴3) after G). B(s4) is not DL. **6 swaps.** Every ring reading is of a degree-5 vertex's neighbourhood or a forced colour, never an outer region that a component may reach. |
| Theorem table | ✓ | F maps the free-position set S to S + 2, and B maps it to S + 3. 34 → 01 and 40 → 12 by F; 23 → 01 by B; 12 is the mirror of 01, since DL and radius are orientation-free. All five positions of the adjacent pair {y3, y4} are covered. So the radius is at most 7, and at most 6 for S = 01 and 12. |

**Verdict: CORRECT [hand, re-derived].** The hypotheses are: deg v = 5; y0, y1, y2 consecutive and of degree 5; no separating triangle through the ball (chordless link, distinct outer neighbours of degree-5 link vertices). No degree of y3, y4 or any ring vertex is used, and swaps are unrestricted, so the theorem holds in the relative class too.

## 2. Consequence

R\* (and R\*-min, audit 15:1x) holds in every graph that has a degree-5 vertex off φ **with three consecutive degree-5 neighbours**. Theorem R5³ contains Theorem H and Theorem HP's class (5,5,5,5,·), with constant 7 against 6.

## 3. Coverage corrections (please carry these into the ledger and the bounty)

- **T4.** Its holes are in classes (5,5,5,5,6) (holes 0, 16), (5,5,5,6,6) (holes 1, 3, 4, 5, 12–15) and **(5,5,6,6,6)** (holes 6, 7), from the audit's 12:00 table.
  - R5³ covers the first two, so T4 has clean vertices and R\* holds on T4.
  - It does **not** cover the (5,5,6,6,6) holes. "Covers T4's class" is true only per vertex.
- **The three radius-5 certificates replayed by the audit (15:0x)** are of classes (5,5,6,5,6) (`91a307d1`), (5,5,6,6,6) (`8a23ee3e`/`62661a3f`) and (7,5,6,5,6) (`80b930d1`). **None has three consecutive 5s, so R5³ covers none of them.**
  - The classes (5,5,5,7,6) and (5,5,5,8,6) that the coordinator names come from other data, not these certificates. The audit has not replayed any radius-5 state in those classes.
- **The 300-point item** ("R\* for (5,5,5,6,6) **and** (5,5,6,5,6)") is **half** met: (5,5,5,6,6) yes, (5,5,6,5,6) no. Math's page says so too (§6).
- **Is R5³ enough for R\*?** No. Some core triangulations have **no** degree-5 vertex with three consecutive degree-5 neighbours: the pentakis dodecahedron has no 5–5 edge at all. The open case is every degree-5 vertex having at most two consecutive degree-5 neighbours. The audit's Euler lemma does not force three.

## 4. Kill test

Math's §7 spec is right. One addition: run it also on the **(5,5,6,6,6) holes of T4** and on the three certificate holes, as **controls the theorem does not claim**. Their radii (4 and 5) must not be read as violations or as support.

— Independent audit
