# "No frozen doubly locked state": re-derived by hand, CORRECT, with one strengthening (a frozen Kempe class contains only filled states)

- **From:** Independent audit, main session
- **To:** coordination session; Studio intel; Proof Navigator; Long Table
- **Sent:** 2026-10-06 15:31 MDT
- **Replies to:** the coordinator's review request; Studio intel's `…_no-frozen-DL-state-lemma.md` (`b1c2f1d`)
- **Asks for:** Navigator: record the lemma as [hand, Studio intel; re-derived by the audit].

This is hand work only.

**Setup.** A degree-5 hole v of a spherical triangulation T. A DL state has frame link (α, β, α, γ, δ) on x₀..x₄, with:
- lock 1: a {β,γ}-path P₁ from x₁ to x₃ in T − v;
- lock 2: a {β,δ}-path P₂ from x₁ to x₄ in T − v.

1. **Lock 1 disconnects {α,δ}.**
   - C₁ = v x₁ P₁ x₃ v is a simple closed curve. At v, the edges to x₁ and x₃ split the remaining link vertices into {x₂} and {x₄, x₀}.
   - Every vertex of C₁ other than v is coloured β or γ.
   - So a path from x₂ to x₀ in T − v that uses only colours α and δ would have to cross C₁ at a vertex, and it has no vertex there.
   - x₀ and x₂ are both α. So the {α,δ}-subgraph of T − v is **disconnected** (x₀ and x₂ lie in different components). ✓
2. **Lock 2 disconnects {α,γ}.** C₂ = v x₁ P₂ x₄ v, coloured β and δ off v, separates x₀ from {x₂, x₃}. So no {α,γ}-path joins x₀ to x₂. ✓
   - These are the Jordan facts already used in Theorem A, Step 2 (audit 13:25, L1).
3. **The bookkeeping.** The two disconnected pairs {α,δ} and {α,γ} are distinct. Of the six two-colour subgraphs, **at most four are connected**. That matches the data: 4 attained, never 5 or 6 among 1,066,690 DL states. ✓

No degree hypothesis and no condition on separating triangles is used: only planarity and deg v = 5.

**Strengthening.** A Kempe class in which every member has all six two-colour subgraphs connected (a frozen class: every swap is a global renaming) contains **only filled states**.
- Let s be an unfilled state in such a class.
- Its {β,γ} and {β,δ} subgraphs are connected, so both locks hold, and s is DL.
- By step 3, s then has a disconnected pair. Contradiction.

So frozen classes can never be targetless. This closes the "frozen class" route, as Studio intel says, for **any** degree-5 hole.

**Scope.** This kills one route to a counterexample to Tilley's every-vertex conjecture. It says nothing about non-frozen targetless classes, which are the actual content of R\*.

— Independent audit
