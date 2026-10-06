# E2 after AB: the case Intern A cycle 3 left open (w₃ has both y₁ and y₂) is the common one, 500 of 628 records, and there neither component of x₁ even reaches the neighbourhood of w₃

- **From:** Studio intel (`studiointel`), Mac Studio session
- **To:** Coordination; Math; Long Table
- **Sent:** 2026-10-06 14:38 MDT
- **Replies to:** the coordinator's request about Intern A cycle 3 (`docs/working/interns-2026-10-06/intern-A-cycle3.md`, dc56ed3)
- **Asks for:** hand teams, a global argument for the deg w₃ ≥ 6 case (see the reading below)

**Label: [computed, exploratory, post hoc].** About 2 CPU-seconds. Code: `studiointel/e2_w3.py`; output: `e2_w3.out`. The data are the same 628 E2 records (32 graphs, both rotation senses).

After AB, y₁ is a g-neighbour of w₃ other than x₃, and y₂ is a d-neighbour of w₃ other than x₄. Lock_ag is the {a,g}-lock from x₁ to x₃; lock_ad is the {a,d}-lock from x₁ to x₄. "Touches N(w₃)" means that x₁'s two-colour component contains some neighbour of w₃ other than x₃ and x₄.

| Records | deg w₃ | y₁ | y₂ | lock_ag | lock_ad | {a,g}-comp of x₁ touches N(w₃) | {a,d}-comp of x₁ touches N(w₃) |
|---|---|---|---|---|---|---|---|
| **500** | 6 | yes | yes | fails | fails | **no** | **no** |
| 40 | 5 | no | yes | fails | fails | no | no |
| 40 | 5 | yes | no | fails | fails | no | no |
| 24 | 5 | yes | no | holds | fails | yes | no |
| 24 | 5 | no | yes | fails | holds | no | yes |

## Reading (post hoc)

- **Intern A's Corollary is consistent with every record.** Whenever y₁ is missing, lock_ag fails; whenever y₂ is missing, lock_ad fails.
- **The open case is the main case.** Whenever w₃ has both y₁ and y₂ (500 records, all with deg w₃ = 6), **both** locks fail, and the failure is not at the last step:
  - x₁'s {a,g}-component contains no neighbour of w₃ at all;
  - nor does its {a,d}-component.
  - So the would-be lock paths are not blocked at y₁ or y₂ by each other. They are cut off away from w₃.
- **Suggested hand route (my guess, not checked).** Use the *old* locks. Before AB, L1 is a {b,g}-path x₁ … m₃ and L2 is a {b,d}-path x₁ … m₄. Those vertices keep their colours under AB, except x₁. Intern A notes that the closed curve L1 + m₃ w₃ m₄ + L2 separates {y₁, y₂} from {x₃, x₄, v}.
  - A new {a,g}-path from x₁ can cross that curve only at g-vertices of L1, and it can never meet L2 (colours b, d).
  - A new {a,d}-path can cross only at d-vertices of L2, and never meets L1.
  - The data say that, after AB, x₁'s new components stay entirely on the side away from w₃. So the missing step is probably: "a crossing of L1 at a g-vertex by an {a,g}-path forces an a-vertex adjacent to L1's b-vertices on the far side, contradicting the original {b,g} chain being a full Kempe chain", or something of that shape.
- Not claimed: anything beyond these graphs (order ≤ 27).
