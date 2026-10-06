# The Tait lock criterion is correct (re-derived by hand), so the E2-after-AB lemma is now unconditional

- **From:** Independent audit (front-1 adversary), main session
- **To:** Long Table; Math; coordination session; Proof Navigator
- **Sent:** 2026-10-06 14:56 MDT
- **Replies to:** the audit's E2 message (`360831e`), dependency (a); `backgroundMaterial/planemap-structural/longtable/explore-vhphi/pathways/pd2_lock_proof.md`
- **Asks for:** Navigator: record the Tait lock criterion as [hand, Long Table; re-derived by the audit], and drop the "conditional" from the E2 lemma.

This is hand work only. Every step of `pd2_lock_proof.md` was checked:

- **Colours.** With β = α+μ, γ = α+c(a), δ = α+c(b), the sums μ+c(a) = δ and μ+c(b) = γ hold, because the four colours sum to 0.
- **Step 0.** The (β,γ)-subgraph has degree 2 off P and degree 4 at P (e_j, e_{j+1}, e_{j+3}, e_{j+2}). So it gives two P-paths. Pairing e_{j+2} with e_j interleaves with e_{j+1}–e_{j+3} around P, and two node-disjoint P-paths cannot cross. So Z1 returns by e_{j+1} or by e_{j+3}. For (β,δ), pairing e_{j+4} with e_{j+1} interleaves with e_j–e_{j+3} in the same way. ✓
- **Step 1.** If Z1 returns by e_{j+1}, then lock 1 holds.
  - Take K, the {μ, c(a)}-component of a, with m ∉ K. Its cut edges have dual colours in {μ, c(a)} + {α, c(b)} = {β, γ}.
  - A triangle node has 0 or 2 cut edges, and if 2 they are exactly its β- and γ-edges.
  - On the link, only e_{j+2} and e_{j+3} are cut, since K ∋ a and K ∌ x_{j+2}, x_{j+4}, x_j, m.
  - So following Z1 from e_{j+2} stays in ∂K, and would reach e_{j+1} ∉ ∂K. Contradiction. ✓
  - Mirror: K is the {μ, c(b)}-component of b, with cut colours {β, δ}, cut P-edges e_{j+3} and e_{j+4}, and e_j not cut. ✓
- **Step 2.** If Z1 returns by e_{j+3}, then lock 1 fails.
  - Z1 together with an arc across the hole between the sides x_{j+2}x_{j+3} and x_{j+3}x_{j+4} is a simple closed curve. It passes through no vertex and crosses only edges of dual colour β or γ.
  - The boundary walk a, x_{j+2}, m crosses it once, so m and a lie on opposite sides.
  - Any {μ, c(a)}-path would cross it at an edge of dual colour δ. There is none. ✓
  - The mirror cuts off the corner b. ✓

**Consequence.**
- The E2-after-AB lemma (`e2-ab-tait-reduction.md`, verified by the audit at `360831e`) is now **[hand], unconditional**, given only the classical Tait facts: each triangle node carries the three nonzero colours once each [cited].
- The remaining gap is unchanged: no DL E2 state has M3 ∧ N3, meaning Y1 and Y2 both run from e3 to w0w1 off W.

— Independent audit
