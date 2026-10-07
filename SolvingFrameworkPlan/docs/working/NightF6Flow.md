# Night: F6 as a flow theorem; Lemmas S, R, P and the one-question lemma at k = 3, 4

Night worker, 7 October 2026 (written 02:39 MDT). **Exploratory. Hand arguments plus single-core reads of Studio files (Jobs G, I, K, L). Unreviewed.**

Builds on `NightF6.md`, `NightC1Gamma.md`, `NightFloorHP2.md`, and the night-log entries for Studio Jobs I, K and L.

Labels:
- [proved]: a hand argument modulo the cited facts and the Kempe/Jordan duality (D) of `NightC1Gamma.md` §2;
- [sketch]: the argument is outlined but has a gap;
- [data]: read off `jobi-cycles.jsonl`, `jobk-records.jsonl` and `jobl-summary.txt` (script in §6);
- [conjecture]: not proved.

## Verdict

1. **[proved] F6 is a flow statement whose sinks never overflow.** For each class there is an exact identity
   Σ_class λ = Σ_{Z positive} def(Z) + Σ_{T nonpositive} rem(T)
   (§1.2). Here:
   - def(Z) = 5w(Z) − (lockless-exit credit from Z into nonpositive cycles);
   - rem(T) is T's λ-sum outside the excursions that positive cycles hit.

   Lemma R says rem ≤ 0. Lemma S says def ≤ 0. Together they give σC on every group and hence F6. Positive-to-positive exits drop out of the identity. Lemma P is what remains when def(Z) > 0.
2. **[data] Γ-cycles.** Lemma S holds in its strongest form on all 62 records: credit into nonpositive targets is at least L, with minimum ratio 31/20 = 1.55. No Γ exit ever hits a positive cycle, so Lemma P is vacuous for Γ-cycles. The Γ part of F6 is therefore **Lemma R + Lemma S_Γ**.
3. **[proved] One-question lemma (§2.1).** At every DL R3 state at k ∈ {3,4} (on any cycle), the σ-exit is lockless **iff the edge pm is a bridge of H**. Here H is the subgraph induced by v and the vertices coloured c(p) or c(m).
   - Equivalently, it is lockless iff p's two outer neighbours y, z flanking m are Kempe-joined in their own two colours.
   - y and z are **fixed vertices**, so all L/5 exit questions at k ∈ {3,4} on a Γ-cycle ask about one edge pm, in L/5 different colourings.
4. **[correction to the coordinator's relay] "5a ≥ L suffices" is not valid with proved worths.** Lockless exits at k ∈ {0,1,2} can have f = 1, which is worth 2, not 5. The proved sufficient form is
   5a₃ + 8a₄ + 2a₀₁₂ ≥ L (using F₄).
   This fails by 1 at p26 #87942 h22, in both orientations: 13 + 6 = 19 < 20. No condition on k = 3, 4 alone can suffice, because the data have Γ-cycles where a quarter of the k = 3, 4 states fail (6 records).
5. **Lemma S_Γ is not proved.** It reduces to a statement about how often the edge pm is a bridge along the cycle (§2.3). This is radius-unbounded.
6. **Non-Γ positive cycles.** def > 0 in 17/37 records at (5,5,5,5,6) and 10/22 at (5,5,5,6,6). Lemma P, stated exactly in §3, is the real 4CT-strength gap.

## 1. The flow theorem

### 1.1 Objects

Fix a class (hole, orientation). Let C be its π-cycles, and write Λ(c) = Σ_c λ = 5w(c) (`NightFloorHP2.md` §1). Split C into:
- P = {c : Λ(c) > 0};
- N = {c : Λ(c) ≤ 0}.

An **exit** e of a positive cycle Z is an R3 state r ∈ Z with π⁻¹r or πr DL (a DD endpoint), whose σ-image s = σ(r) is lockless and lies on a cycle T(e) ≠ Z.
- s is a u = 1 excursion followed by f(e) ≥ 1 filled states.
- That excursion contributes 1 − 3f(e) to Λ(T(e)), so its credit is c(e) = 3f(e) − 1 ≥ 2.

Facts used [proved]:
- σ is an involution, so distinct exits have distinct images, and hence disjoint excursions (`NightC1Gamma.md` §4).
- e is a σ-link of the formal σ-group structure (from a DD endpoint), so Z and T(e) lie in one σ-group.

*Caveat.* Job K counts hits from every DL R3 state, not only DD endpoints. On Γ-cycles this makes no difference, since every state is a DD endpoint. On non-Γ cycles the group-level statements below need the endpoint restriction; the class-level statement does not.

Define:
- Cr_N(Z) = Σ c(e) over the exits e of Z with T(e) ∈ N;
- Cr_P(Z) = Σ c(e) over the exits with T(e) ∈ P;
- def(Z) = Λ(Z) − Cr_N(Z);
- for T ∈ N, hit(T) = Σ (1 − 3f(e)) over all exits e with T(e) = T, from any positive cycle;
- rem(T) = Λ(T) − hit(T), the λ-sum of T outside its hit excursions.

### 1.2 Identity [proved]

For any union g of σ-groups (in particular one group, or the class):

  Σ_{c∈g} Λ(c) = Σ_{Z∈P_g} def(Z) + Σ_{T∈N_g} rem(T).

*Proof.* Σ_{N_g} Λ = Σ_{N_g} hit + Σ_{N_g} rem. Each exit into N_g is counted once in hit(T(e)), as −c(e), and once in Cr_N of its source. Its source lies in g because exits are σ-links. Exits into P are counted on neither side. ∎

### 1.3 The flow network and what Lemma R means [proved]

The network is:
- source → Z ∈ P, with capacity Λ(Z);
- Z → T ∈ N, with capacity Σ_{e: Z→T} c(e);
- T → sink, with capacity −Λ(T).

**Lemma R** (Job K's form) is rem(T) ≤ 0 for every T ∈ N. Since −hit(T) is the total edge capacity into T, rem(T) ≤ 0 is exactly
  (total edge capacity into T) ≤ (sink capacity of T).
So **under Lemma R no sink edge is ever binding**: every target can absorb all of its incoming exits at once.

The max flow is then Σ_Z min(Λ(Z), Cr_N(Z)), with no Hall condition across positives. Hence:
- the flow saturates all supplies ⇔ **Lemma S**: def(Z) ≤ 0 for all Z ∈ P;
- by §1.2, Lemma R + Lemma S ⇒ Σ_g Λ ≤ 0 for every σ-group g (σC), and so the class floor.

F6 then follows by `sigmaCConj_imp_floor_on_family`. (The floor itself only needs the class sum. The identity also gives it directly.)

[data] Lemma R holds on all 210 targets with w ≤ 0 (Job K). The maximum of rem is 0, and it is attained, e.g. at p26 #87887 h21, where 30 hits with f = 3 use all of −240.
- The four Lemma R failures are exactly the four records with Cr_P > 0: p25 #16298 h23, p25m #16149 h3, p26m #40549 h3, p26m #75049 h16. All four are **non-Γ** sources hitting positive targets.
- Those exits drop out of §1.2, so they do no harm. Lemma R is needed only on N, where it holds.

### 1.4 Lemma P [statement]

If def(Z) > 0 for some Z, §1.2 says σC on g is equivalent to

  **Lemma P(g).** Σ_{Z∈P_g} def(Z) ≤ Σ_{T∈N_g} (−rem(T)).

That is, the positive deficits are covered by the slack of the nonpositive cycles of the group. The slack consists of:
- the non-hit cycles, at their full −Λ;
- the hit cycles, at −rem ≥ 0.

Surpluses (def < 0) of other positives in g also count, since the sum is signed.

The routing form asked for is: forward a positive target's incoming credit through its own exits. It adds nothing. Positive-to-positive credit cancels in §1.2, so Lemma P(g) is the exact remaining content, and any routing scheme is a certificate for it.

A local certificate is:

  **Lemma P₁ (one-hop Hall).** There is an assignment of each deficit def(Z) > 0 to nonpositive σ-neighbours T of Z (any σ-link from a DD endpoint of Z: lockless, single-lock or DL image) such that every T receives at most −rem(T) minus the surpluses already used.

[data] Every positive cycle is one σ-hop from a negative cycle (Jobs K, L: 37 + 22 records, hop = 1 always). The first negative neighbour has w from −7 to −119, against deficits ≤ 20 (= 5w for p26 #68224 h23 and p26 #83426 h18 with Cr = 0). P₁ needs the per-target remainder by cycle id, which the jsonl files do not carry (targets are keyed by w only). It is a Studio check (§5).

## 2. Lemma S on Γ-cycles

### 2.1 One-question lemma [proved]

Let r be a DL R3 state at k ∈ {3,4}, with p = x_k, m its extra outer neighbour (colour α, Lemma D), and y = w_{k−1}, z = w_k the two outer neighbours of p flanking m. So pmy and pmz are the two faces on the edge pm.

**(a)** σ(r) is lockless ⇔ y and z lie in one {c(y),c(z)}-component.
- *k = 4.* The criterion is w₄ ∈ K_{μ,A}(x₁) (`NightC1Gamma.md` §2). Lock1 joins x₁ to x₃ in {μ,A}, and x₃ (A) is adjacent to w₃ = y (μ). So K_{μ,A}(x₁) = K_{μ,A}(y), and the criterion reads z ∈ K_{μ,A}(y). Note {c(y),c(z)} = {μ,A}.
- *k = 3.* The criterion is w₂ ∈ K_{μ,B}(x₁). Lock2 joins x₁ to x₄ in {μ,B}, and x₄ (B) is adjacent to w₃ = z (μ). So the criterion reads y ∈ K_{μ,B}(z), with {c(y),c(z)} = {μ,B}.
- This generalises `NightF6.md` §1.2 from the pair (r, π²r) to every such state. ∎

**(b)** Let H = {v} ∪ (the vertices coloured c(p) or c(m)). Then {c(p), c(m)} is the complementary pair. The claim: σ(r) is lockless ⇔ pm is a bridge of the induced graph G[H].
- *Proof.* By (D), y ≁ z ⇔ some closed walk W in H separates y from z.
- W must cross both y–m–z and y–p–z, so it contains m and p.
- Shortcut W along the edge pm to get a cycle through pm. Any cycle through pm has the two faces pmy and pmz on opposite sides.
- Conversely, any cycle of G[H] through pm separates y from z.
- So y ≁ z ⇔ pm lies on a cycle of G[H] ⇔ pm is not a bridge. ∎

**(c) Fixed vertices.** The frame at R3@k has j = pos(p) − k. So for each k ∈ {3,4}, the vertices p, m, y, z are the same at every R3@k state of the class. The L/5 exit questions at k ∈ {3,4} on a Γ-cycle all ask whether the **one edge pm** is a bridge of its two-colour graph (plus v), in L/5 colourings.
- Along the cycle these come in pairs (r, π²r), with r at k = 4 and π²r at k = 3, two R-swaps apart. Consecutive pairs are 8 R-swaps apart.
- Failure at k = 4 means pm is on an {α,B}-cycle. Through p this cycle must leave via x₀ (α) or v. So failure ⇔ in G − p, m is {α,B}-joined to x₀ or x₂, or reaches v. The k = 3 case is the same with {α,A}.

### 2.2 What suffices, exactly [proved bookkeeping; data]

Proved worths are:
- ≥ 5 at k = 3 (`NightF6.md` §2);
- 8 at k = 4, given F₄ (conjecture, 133/133);
- ≥ 2 at k = 0, 1, 2.

Write s_k for the number of lockless exits at k (0 ≤ s_k ≤ L/10). Then Lemma S_Γ follows from

  (★) 5s₃ + 8s₄ + 2(s₀ + s₁ + s₂) ≥ L.

- If all k = 3, 4 states succeed, the k = 3, 4 exits alone give 1.3L. A uniform success fraction ρ on k ∈ {3,4} suffices alone iff ρ ≥ 10/13.
- [data, 62 records, L = 20 except 4 with L = 60] The failures per cycle at (k = 3, k = 4) are:
  - (0,0) in 50 records;
  - (1,1) in 6;
  - (1,0) in 1 and (0,1) in 1;
  - none at L = 60.
- So the sharpest supported form is "**at most one failure per k per cycle**". At L = 20 this is A₃₄, and it means ≥ half succeed.
- The minimum k = 3, 4 success fraction is exactly 1/2, below 10/13. So k = 3, 4 alone fail (★) in 7 records (5s₃ + 8s₄ = 13 or 18 < 20).
- (★) itself, with the proved k = 0, 1, 2 worth 2, fails by 1 at p26 #87942 h22 (s = (1,1,1,1,1), both orientations).
- With the actual k = 0, 1, 2 credits, 5s₃ + 8s₄ + Σ_{k≤2}(3f − 1) − L ≥ 5 on all 62 records. The tightest is p25m #16945 h3, with s = (0,0,2,2,1), k ≤ 2 credit 7 and total 31.
- Every Γ exit lands in N (Cr_P = 0, 62/62), matching Job L.

**Minimal sufficient pair of conjectures [conjecture].**
- **A₃₄′.** On a Γ-cycle, at most L/20 states fail at each of k = 3 and k = 4. With F₄ this gives 13L/20 from the k = 3, 4 exits.
- **F₀₁₂′.** On a Γ-cycle, the k ∈ {0,1,2} lockless exits carry credit ≥ 7L/20.
  - [data] The minimum of (k ≤ 2 credit − 7L/20) over the 7 records that need it is 7 − 7 = 0, at p25m #16945 h3. That record has s₃ + s₄ = 3, so its actual requirement is only 2.
  - Over all 62 records the binding quantity is (★) with true f.

### 2.3 Why §2.1 does not yet prove A₃₄′ [sketch]

Between the questions at r and π²r, the {c(p),c(m)}-graph changes only on the swapped components K₁ ∪ K₂. These swaps meet neither m nor x₀ (`NightF6.md` §1.1). So a cycle through pm survives iff it avoids the 0-vertices of K₁ ∪ K₂. Correlation, not equivalence.

What a proof needs: along one period (10 R-swaps, i.e. one pair plus 8 more swaps), pm cannot lie on a two-colour cycle in **two consecutive** pairs. That is a statement about how 10 consecutive {α,A}-type swaps around the hole move the {α,·}-cycle through pm. I see the mechanism, since every swap is anchored at x₂ and the roles 3-cycle, but no proof. Each swap component can reach arbitrarily far, so it is radius-unbounded.

## 3. Non-Γ positive cycles [data; conjecture]

At (5,5,5,5,6), in 37 records:
- Cr_N < 5w in 17;
- Cr_N = 0 in 11, of which 10 have a = 0 and one (p25 #16298) has its only exit into a positive cycle.

The worst deficits are 20, at p26 #68224 h23 and #83426 h18 (w = 4). At (5,5,5,6,6), Job L: 10/22 records, minimum 0 (p26 #7490 h3).

These cycles have only 1–4 R3 states per k, so §2's counting has nothing to work with. Their payment is Lemma P(g): σ-links from their DD endpoints' DL and single-lock images (which are in the formal σ-groups) to a negative neighbour with enough slack. All are one hop from a negative cycle.

## 4. Status

| item | content | status | support |
|---|---|---|---|
| identity §1.2 | Σ_g Λ = Σ def + Σ rem | [proved] | — |
| flow §1.3 | R ⇒ sinks non-binding; R + S ⇒ σC ⇒ F6 | [proved] | — |
| Lemma R on N | rem(T) ≤ 0 | [conjecture] | 210/210, tight |
| one-question lemma §2.1 | k = 3, 4 exit ⇔ pm is a bridge of G[H] | [proved] mod (D) | consistent with Job G S1 0/464 |
| f ≥ 2 at k = 3, 4 | | [proved] (`NightF6.md` §2) | 266/266 |
| F₄ | | [conjecture] | 133/133 |
| A₃₄′ | ≤ L/20 failures per k | [conjecture], §2.3 sketch | 62/62 |
| Lemma S_Γ | Cr_N ≥ L | [conjecture]; (★) fails by 1 with proved worths | 62/62, min ratio 1.55 |
| Lemma P(g), non-Γ | deficits ≤ group slack | [conjecture] = σC restated; 4CT-strength | Job F 0 failures ≤ 26; hop 1 always |
| order ≥ 27 | | open | Job J |

What is 4CT-strength: Lemma P on non-Γ groups, and A₃₄′/F₀₁₂′ (Kempe bridge statements with unbounded radius). Lemma R also has no proof, though it is tight and looks like a per-cycle bookkeeping fact about the target's own runs.

## 5. Studio requests

1. Per positive cycle: deficit def(Z), and for each σ-neighbour T ∈ N, rem(T) by cycle id. This tests Lemma P₁ (one-hop Hall).
2. Per Γ-cycle: the sequence of k = 3, 4 successes in π-order. This tests whether failures ever occur in two consecutive pairs (§2.3).
3. A state-level check of §2.1(b) (lockless ⇔ pm is a bridge of G[H]) at orders 21–22 or 25.

## 6. Reproduction

The script is in the session scratchpad (`f6flow/a.py`, not committed). It is a single pass over `jobi-cycles.jsonl` (the exit keys `kind_k<mask>_u_f_wT`) and over `jobk-records.jsonl` (`lemmaR` tuples [w, |T|, hits, Σ(1 − 3f), rem]). It runs in under 1 s on one core.
