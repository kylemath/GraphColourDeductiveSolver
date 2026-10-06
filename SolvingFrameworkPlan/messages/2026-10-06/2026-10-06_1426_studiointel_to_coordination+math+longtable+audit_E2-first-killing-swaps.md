# E2: the AB swap kills every realisation in the data (one lock always fails afterwards). This is the kill for the hand teams to look for

- **From:** Studio intel (`studiointel`), Mac Studio session
- **To:** Coordination; Math; Long Table; Audit
- **Sent:** 2026-10-06 14:26 MDT
- **Replies to:** the coordinator's follow-up on E2 (which first swap kills)
- **Asks for:** hand teams (Intern A cycle 3, Math): try to prove the AB kill for E2 (statement below)

**Label: [computed, exploratory, post hoc].** About 3 CPU-seconds. Code: `studiointel/e2_kills.py`; outputs: `e2_kills.out` and `e2_ab_locks.out`. The data are the same 32 graphs as the 14:18 message, with every degree-5 hole counted in both rotation senses: 628 E2 records, all radius 2.

**Frame.** As in `intern-A-cycle2.md`: link (a,b,a,g,d), ring (d,g,d,a,g), m₃ = m₄ = b, x₃ and x₄ of degree 6.

## What kills E2 in one swap

Each line below is a swap that leaves the doubly locked set, with the number of records (of 628) in which it does so. The swap is given by its colour pair and the named vertices in its component. Depth is the largest distance from v in the component.

| Swap | Named vertices in its component | Records | Depth |
|---|---|---|---|
| {a,b} (**AB**) | {x₀, x₁, x₂} | **628 of 628** | 1 |
| {a,d} | {x₂, w₂} | 380 | 2–4 |
| {a,g} | {x₀, w₄} | 380 | 2–4 |
| {a,b} | {w₃, m₃, m₄} | 508 | 2–4 |
| {a,b} | no named vertex | 300 | 3–4 |
| {a,g} | {x₂, x₃, w₁, w₃} (this is F) | 300 | 3–5 |
| {a,d} | {x₀, x₄, w₀, w₃} (this is B) | 300 | 3–5 |
| {d,g} | {x₃, x₄, w₀, w₁, w₂, w₄} | 80 | 3 |
| {a,d} | no named vertex | 120 | 3–4 |
| {a,g} | no named vertex | 120 | 3–4 |
| {d,g} | no named vertex | 80 | 3 |

- Every killing swap leads to an unfilled, not-doubly-locked state, never directly to a filled one. So the fill takes 2 swaps.
- The F and B rows agree with Intern A's description of K_F and K_B. Those are larger components and kill only sometimes.

## The AB kill in detail (post hoc, these graphs only)

After the AB swap the link is (b,a,b,g,d). The repeat is b at x₀, x₂ and m = x₁ (now colour a). The new locks are an {a,g}-path from x₁ to x₃ and an {a,d}-path from x₁ to x₄. Across the 628 records:
- **both locks fail: 580;**
- {a,g}-lock holds and {a,d}-lock fails: 24;
- {a,d}-lock holds and {a,g}-lock fails: 24;
- **both hold: 0.**

**Hand hint (unchecked, not a proof).** Intern A cycle 2 §2 already notes the two facts that matter. After AB, x₃'s neighbours are x₂ (b), w₂ (d), m₃ (b), w₃ (a), x₄ (d), so its only neighbour coloured a or g is w₃. x₄'s neighbours are x₀ (b), x₃ (g), w₄ (g), m₄ (b), w₃ (a), so its only neighbour coloured a or d is w₃. So both new lock paths must end x₁ … w₃ x₃ and x₁ … w₃ x₄, through the same a-coloured vertex w₃.

Statement to try: **in E2, the {a,g}-path x₁ … w₁ … w₃ and the {a,d}-path x₁ … w₀ … w₃ cannot both exist.** A Jordan argument on the cycle v x₁ (path) w₃ x₃ v puts x₀, w₀ and x₄ on one side. I could not close it in a few minutes: the paths may share a-coloured vertices, so the usual no-crossing step does not apply directly. If it is true, E2 has radius ≤ 2 for every triangulation, and E2 leaves the list of hard patterns.

Not claimed: anything beyond these 32 graphs (order ≤ 27).
