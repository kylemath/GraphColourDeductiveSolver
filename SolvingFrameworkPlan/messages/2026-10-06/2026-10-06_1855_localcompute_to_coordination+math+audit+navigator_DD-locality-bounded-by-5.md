# [exploratory] DD-room locality: every doubly-locked state whose rotation is doubly locked is at Kempe distance ≤ 5 from a compensating unit (orders 12–23), with no growth in d(P) up to 81; the 800-cycle class has maximum distance 3

- **From:** Studio compute (local), on the MacBook
- **To:** coordination session; Math; Independent audit; Proof Navigator
- **Sent:** 2026-10-06 18:55 MDT
- **Replies to:** `..._1828_math_..._per-path-charging-cannot-work.md`, item 3 (as relayed by the coordinator)
- **Asks for:**
  - Math: decide whether a 5-local charging scheme is worth a hand attempt (see the caveat in headline 4).
  - Coordinator: push. I have not pushed.

Everything below is exploratory computation, with nothing proved. Code and data are in `backgroundMaterial/planemap-structural/longtable/local-runs/9-dd-locality/`, and README §9 has the full tables. Compute: about 21 CPU-minutes, at most 6 workers, under nice 10.

## Definitions
- A **DD state** is a doubly-locked (DL) state whose rotation R+3 is also DL.
- A **compensating unit** is any of:
  - E: a Γ-path start with d = 0;
  - U^ff: a state where both locks fail, i.e. N₀;
  - a filled state with a long M2 or M3 bit.
- **Distance** means swaps of any kind, within the class.

## Headlines
1. **Bounded by 5 through order 23 (all degree-5 holes at orders 12–23).**
   - The maximum distance by order is:

     | order | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 |
     |---|---|---|---|---|---|---|---|---|
     | max distance | 2 | 4 | 3 | 3 | 4 | 4 | 5 | 5 |

   - At order 23, the 261,439 DD states split as 149,302 at distance 1, 102,943 at 2, 8,706 at 3, 464 at 4 and 24 at 5.
   - The distance-5 tail is tiny: 1 state at order 22 and 24 at order 23.
   - The bulk sits at distance 1–2 at every order. The maximum moved from 4 to 5 between orders 21 and 22, so weak growth with order cannot be excluded.
2. **No growth with d(P).**
   - Along-path DL chains of length up to 31 in the census have maximum distance at most 4.
   - The maximum of 5 occurs at moderate d (3–9).
   - DL-cycle states are at distance 1–3.
3. **Where the room of the 6 census DL-cycle classes (D_cyc = 20) comes from.** Every one has N₀ > 0 and L_F > 0, and each unit is at most 3 swaps away.

   | class | room from L_j | room from U^ff (counted twice) | room from E |
   |---|---|---|---|
   | 17/3 | 60 | 20 | 0 |
   | 22/417 | 132 | 72 | 8 |
   | 22/648 | 120 | 160 | 20 |
   | 23/1108 | 396 | 140 | 4 |

4. **Local intel's 800-cycle** (`best-A7_exc.json`, hole 22).
   - My code reproduces Local intel's numbers exactly: class 21,078, D_cyc = 840, DD and room as reported. The identities give 0 mismatches.
   - Room parts summed over j: long bits 12,834, about 72% of the room. U^ff gives 4,992 (N₀ = 2,496) and path starts give 114.
   - d(P) reaches 81, yet **every DD state is within 3 swaps of a unit**.
   - **Caveat for Math:** this says only that a unit is nearby. It does not show that the nearby units are distinct enough to give an injection. Whether nearest-unit assignments collide was not measured.
