# Quarter floor, part (a): a map injective for each j (at most 2-to-1 overall) from non-doubly-locked unfilled states to filled states

Math lead, 6 October 2026. **[hand]: a complete proof is given below. Reviewed by the audit: CORRECT per j (relayed by the coordinator; its message file is not yet filed). Its three fixes are applied.** The statement is the non-DL half of local compute's counting lemma (8ab6f1d, message 1811):

  U_j ≤ F_{j+1} + F_{j+3} + F_{j+4}.

## Setting

- T is a triangulation, v is a vertex of degree 5, and its link x₀..x₄ is in rotation order. Indices are mod 5.
- A **state** is a proper 4-colouring of T − v, considered up to renaming or labelled; everything below commutes with renaming.
- **Filled:** the link uses at most 3 colours. A filled state uses exactly 3 colours on the link, because a proper colouring of a 5-cycle needs 3.
  - Its colour pattern has exactly one colour appearing once on the link, its **singleton**, at some position i.
  - Positions i+1 and i+3 then share a colour X, and positions i+2 and i+4 share a colour Y.
  - **F_i** is the set of filled states of a class S whose singleton is at position i.
- **Unfilled:** the link uses 4 colours, with exactly one repeated colour α at two positions j and j+2.
  - **U_j** is the set of unfilled states of S with repeat pair {j, j+2}.
  - Write m = x_{j+1} (colour μ), a = x_{j+3} (colour A) and b = x_{j+4} (colour B).
- **Lock 1:** m and a lie in one {μ, A}-component of T − v. **Lock 2:** m and b lie in one {μ, B}-component.
  - **D_j ⊆ U_j** is the set of doubly locked states (both locks hold).

## Lemma A

For every Kempe class S of T − v and every j:

  |U_j ∖ D_j| ≤ |F_{j+3}| + |F_{j+4}|.

Summing over j gives Σ_j |U_j ∖ D_j| ≤ 2 Σ_i |F_i|. **The non-doubly-locked unfilled states of any class are at most twice its filled states.**

## Proof

Define φ on U_j ∖ D_j as follows.

**Case 1: lock 1 fails.**
- Let K be the {μ, A}-component of a in T − v. It does not contain m, because lock 1 fails.
- The only link vertices coloured μ or A are m and a: x_j and x_{j+2} are α, and b is B. So **K meets the link only in a**.
- Swap K, and call the result φ(s). Only a changes on the link, from A to μ. The new link is (α, μ, α, μ, B) at positions j, …, j+4.
- So φ(s) is filled. Its singleton is B at position j+4, and positions j, j+2 carry α while j+1, j+3 carry μ. **φ(s) ∈ F_{j+4}.**

**Case 2: lock 1 holds, so lock 2 fails** (s is not doubly locked).
- Let K be the {μ, B}-component of b. It misses m and meets the link only in b.
- Swapping K turns b from B into μ. The link becomes (α, μ, α, A, μ), which is filled with singleton A at position j+3. **φ(s) ∈ F_{j+3}.**

In both cases φ(s) is one Kempe swap from s, so **φ(s) ∈ S**.

**Injectivity.** Fix j and the case.
- **Case 1.** Let f = φ(s) ∈ F_{j+4}.
  - f determines μ as the colour of x_{j+3} in f.
  - f determines A as the **one colour missing from f's link**, which uses only α, μ and B.
  - A Kempe swap does not change the vertex set of any component of its own colour pair, so K is again a {μ, A}-component in f, and it contains x_{j+3}.
  - Hence s is obtained from f by swapping the {μ, A}-component of x_{j+3}, which f determines. So s is determined by f.
- **Case 2.** It is the same with x_{j+4}: s is f with the {μ, B}-component of x_{j+4} swapped, where μ = f(x_{j+4}) and B is the colour missing from f's link.
- Case 1 lands in F_{j+4} and Case 2 in F_{j+3}, which are disjoint (different singleton positions).
- So φ is injective from U_j ∖ D_j into F_{j+3} ⊔ F_{j+4}. ∎

## Remarks

1. **Multiplicity.** A filled state f ∈ F_i has at most two preimages over all j:
   - j = i + 1, by Case 1 (j + 4 = i), recovered by swapping the {μ, A}-component of x_{j+3} = x_{i+4};
   - j = i + 2, by Case 2 (j + 3 = i), recovered by swapping the {μ, B}-component of x_{j+4} = x_{i+1}.

   So the total multiplicity is at most 2. This gives the summed form 2ΣF.
2. **Origin.** This is Kempe's own single-swap step, made injective for each j: a failing lock is cut by swapping the component of the far endpoint. Local compute reports 0 collisions in 353,812 states. **What that count measured is not recorded here.** If it was per (j, case), it confirms the proof. If it was across all j, it is a separate data fact: the two-preimage pattern of Remark 1 (intern C's configuration) never occurred at orders 12–21. **The lemma does not depend on it either way.**
3. **What remains: part (b).** The full counting lemma needs an injection of D_j (the doubly locked states) into F_{j+1} plus whatever of F_{j+3} and F_{j+4} that φ leaves unused. Doubly locked states are at least two swaps from any filled state.

   (b) for all triangulations is **at least as strong as** R\* at every degree-5 vertex. It implies a filled fraction ≥ 1/4 in every class, which implies R\*, and so the Four Colour Theorem. The converse is not claimed. So (b) must contain a genuinely global step. Lemma A is local and contains none.
4. **The degree-5 hypothesis is used only through the shape of the link**: one repeated colour at distance 2, three singletons, and the blocking adjacencies. That matches the data: the floor fails at degrees 6 and 7.

## Addendum (after intern C's review, 63821de)

- Intern C confirms that the map is injective **per (j, branch)**, and that the two branches land at different singleton positions. That is exactly the per-j statement above.
- **Across different j the map is not injective in general.** A filled f ∈ F_i can be the image of j = i+1 (branch 1) and of j = i+2 (branch 2). This is Remark 1: multiplicity at most 2. Intern C gives a local configuration where both occur; its realisability is unchecked. The summed form Σ_j |U_j ∖ D_j| ≤ 2 Σ|F| is unaffected.
- **The DL target, in counting form.** The floor ΣU ≤ 3ΣF is equivalent to

  Σ_j |D_j| ≤ Σ|F| + s, where s := 2Σ|F| − Σ_j |U_j ∖ D_j| ≥ 0

  is the **slack**: each filled state counted with (2 − its number of φ-preimages). So the doubly locked states must be paid for by one unit per filled state plus the filled states that φ uses fewer than twice. Per j, local compute's form is |D_j| ≤ |F_{j+1}| + (|F_{j+3}| + |F_{j+4}| − |U_j ∖ D_j|). Part (b) should target an injection of D_j into F_{j+1} ⊔ (the part of F_{j+3} ⊔ F_{j+4} not hit by φ restricted to U_j).
